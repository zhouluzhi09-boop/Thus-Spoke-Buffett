#!/usr/bin/env python3
"""
validate-skill.py — SKILL.md 综合校验
读取全部测试用例，对照 SKILL.md 做静态合规检查，输出三层测试报告。

用法: python validate-skill.py [--skill path/to/SKILL.md] [--evals path/to/evals]
"""
import sys, re, json, glob, os, io
from pathlib import Path
from datetime import datetime

# Fix Windows GBK encoding for emoji output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── 路径 ───────────────────────────────────────────
SKILL_PATH = os.environ.get(
    "SKILL_PATH", ".claude/skills/buffett-wisdom/SKILL.md"
)
EVALS_DIR = os.environ.get(
    "EVALS_DIR", ".claude/skills/buffett-wisdom/evals"
)


# ── T0 触发词检查 ──────────────────────────────────
def extract_skill_triggers(skill_content):
    """从 SKILL.md frontmatter 提取触发词列表"""
    fm_match = re.match(r"^---\s*\n(.*?)\n---", skill_content, re.DOTALL)
    if not fm_match:
        return []
    fm = fm_match.group(1)
    triggers = []
    in_triggers = False
    for line in fm.split("\n"):
        if line.strip().startswith("triggers:"):
            in_triggers = True
            continue
        if in_triggers:
            if line.strip().startswith("- "):
                triggers.append(line.strip()[2:].strip())
            elif line.strip() and not line.startswith(" "):
                break
    return triggers


def load_test_cases(evals_dir):
    """加载所有测试用例文件"""
    cases = {"t0": [], "t1": [], "t2": []}

    for tier, dirname in [("t0", "t0-trigger"), ("t1", "t1-boundary"), ("t2", "t2-framework")]:
        pattern = f"{evals_dir}/{dirname}/*.md"
        for filepath in sorted(glob.glob(pattern)):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            cases[tier].append({
                "file": Path(filepath).stem,
                "content": content,
                "path": filepath,
            })
    return cases


# ── T0 检查 ────────────────────────────────────────
def check_t0_triggers(cases, triggers):
    """检查触发词是否覆盖正向用例，是否不覆盖负向用例"""
    results = []

    for case in cases["t0"]:
        content = case["content"]
        is_negative = "負向" in content or "负向" in content

        # 提取场景文本（第一个"- **场景**"后面的内容）
        scene_match = re.search(r'\*\*场景\*\*[：:]\s*"([^"]+)"', content)
        scene = scene_match.group(1) if scene_match else ""

        # 检查场景文本中是否包含任意触发词
        triggered = any(t in scene for t in triggers if len(t) >= 2)

        if is_negative:
            passed = not triggered
            fail_reason = f"负向用例被意外触发: \"{scene}\" 匹配了触发词" if not passed else ""
        else:
            passed = triggered
            fail_reason = f"正向用例未能触发: \"{scene}\" 未匹配任何触发词" if not passed else ""

        results.append({
            "id": case["file"],
            "tier": "T0",
            "type": "负向" if is_negative else "正向",
            "scene": scene,
            "passed": passed,
            "fail_reason": fail_reason,
        })

    return results


# ── T1 边界检查 ────────────────────────────────────
def check_t1_boundaries(cases, skill_content):
    """检查 SKILL.md 是否包含每个边界测试要求的禁止行为声明"""
    results = []

    boundary_checks = {
        "推荐|买入|卖出|建议": r"(不推荐|不(给|做|提供).*建议|不.*买.*卖)",
        "预测|涨|跌": r"(不预测|从不.*预测|不.*走势)",
        "精确.*估值|估值.*数字": r"(不(给|做|提供).*(精确|具体).*(数字|估值)|模糊的正确)",
        "加密|比特|区块链": r"(加密.*(不在|不投|不适用)|比特.*(不在|不适用)|不产生现金流)",
        "个人|攻击|骗子|人品": r"(不(批评|攻击|评论).*个人|系统性.*行为)",
        "杠杆|借钱|融资": r"(不.*(杠杆|借钱)|乘以.*零|永远.*不.*(借|融))",
        "政治|贸易战|地缘": r"(不.*(政治|地缘)|不是.*政治|投资者.*不是)",
        "承诺.*回报|年化|收益率": r"(不承诺.*回报|不是.*承诺|不确定)",
    }

    for case in cases["t1"]:
        content = case["content"]
        scene_match = re.search(r'\*\*场景\*\*[：:]\s*"([^"]+)"', content)
        scene = scene_match.group(1) if scene_match else ""

        passed = False
        matched_rule = None
        for keyword, required_pattern in boundary_checks.items():
            if re.search(keyword, content):
                if re.search(required_pattern, skill_content, re.IGNORECASE):
                    passed = True
                    matched_rule = keyword
                    break

        results.append({
            "id": case["file"],
            "tier": "T1",
            "scene": scene,
            "passed": passed,
            "fail_reason": f"SKILL.md 中未找到对应的边界声明" if not passed else "",
            "matched_rule": matched_rule,
        })

    return results


# ── T2 框架检查 ────────────────────────────────────
def check_t2_framework(cases, skill_content):
    """检查 SKILL.md 是否包含框架测试要求的指令"""
    results = []

    framework_checks = {
        "四关":    r"(能力圈|第一关).*(护城河|第二关).*(管理层|第三关).*(价格|第四关)",
        "比喻":    r"(就像|如同|比如|想象|市场先生|泰德|击球区|护城河|烟蒂|蟑螂|船|嫁女儿|氧气|癞蛤蟆|一鸟在手)",
        "我们":    r"(我们.*做法|我们.*选择|我们.*投资|我们.*从来)",
        "排除":    r"(排除|不投|不看|不碰|放弃|默认.*不)",
        "确定性":  r"(从不|永不|绝不|必须|一定).*(我认为|我们相信|我们觉得|以我们的).*(不知道|不清楚|无法判断)",
        "幽默":    r"(自嘲|错误|失败|教训|我是.*那个|本以为|运气|幸运)",
        "现金.*期权|期权.*现金": r"(现金.*期权|期权.*现金|什么也不做|等待.*权利|耐心)",
        "不知道":  r"(我不知道|我们不知道|无法判断|毫无洞见|超出.*能力圈|不发表意见)",
    }

    for case in cases["t2"]:
        content = case["content"]
        scene_match = re.search(r'\*\*场景\*\*[：:]\s*"([^"]+)"', content)
        scene = scene_match.group(1) if scene_match else ""

        passed = False
        matched_rules = []
        for rule_name, pattern in framework_checks.items():
            if re.search(pattern, skill_content, re.IGNORECASE | re.DOTALL):
                matched_rules.append(rule_name)

        # T2 不需要每个 check 都过 — 只要有足够多的框架要素即可
        passed = len(matched_rules) >= 5

        results.append({
            "id": case["file"],
            "tier": "T2",
            "scene": scene,
            "passed": passed,
            "fail_reason": f"SKILL.md 框架要素不足 ({len(matched_rules)}/8 类)" if not passed else "",
            "matched_rules": matched_rules,
        })

    return results


# ── 主入口 ─────────────────────────────────────────
def main():
    # 定位 skill 文件
    skill_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not skill_path:
        for candidate in [
            Path(".claude/skills/buffett-wisdom/SKILL.md"),
            Path("D:/Obsidian/知识库/知识库/.claude/skills/buffett-wisdom/SKILL.md"),
        ]:
            if candidate.exists():
                skill_path = candidate
                break

    if not skill_path or not skill_path.exists():
        print("❌ 找不到 SKILL.md。请指定路径: python validate-skill.py path/to/SKILL.md")
        sys.exit(1)

    with open(skill_path, "r", encoding="utf-8") as f:
        skill_content = f.read()

    # 定位 evals 目录
    evals_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    if not evals_dir:
        candidates = [
            Path(".claude/skills/buffett-wisdom/evals"),
            Path("D:/Obsidian/知识库/知识库/.claude/skills/buffett-wisdom/evals"),
        ]
        for c in candidates:
            if c.exists():
                evals_dir = c
                break
        if not evals_dir:
            evals_dir = skill_path.parent / "evals"

    if not evals_dir.exists():
        print(f"❌ evals 目录不存在: {evals_dir}")
        sys.exit(1)

    triggers = extract_skill_triggers(skill_content)
    cases = load_test_cases(str(evals_dir))

    total_cases = sum(len(v) for v in cases.values())
    print(f"📋 SKILL.md: {skill_path}")
    print(f"📋 触发词: {len(triggers)} 个 — {', '.join(triggers[:8])}...")
    print(f"📋 测试用例: T0={len(cases['t0'])} T1={len(cases['t1'])} T2={len(cases['t2'])} (共{total_cases})\n")

    # 运行三层检查
    all_results = []

    t0_results = check_t0_triggers(cases, triggers)
    all_results.extend(t0_results)

    t1_results = check_t1_boundaries(cases, skill_content)
    all_results.extend(t1_results)

    t2_results = check_t2_framework(cases, skill_content)
    all_results.extend(t2_results)

    # ── 打印结果 ──
    for tier_label, tier_results in [
        ("T0 触发测试", t0_results),
        ("T1 边界测试", t1_results),
        ("T2 框架测试", t2_results),
    ]:
        print(f"\n{'─'*50}")
        print(f"📊 {tier_label}")
        tier_passed = sum(1 for r in tier_results if r["passed"])
        tier_total = len(tier_results)
        for r in tier_results:
            status = "✅" if r["passed"] else "❌"
            detail = f" — {r.get('matched_rule', '')}" if r["passed"] and r.get("matched_rule") else ""
            fail = f" — {r['fail_reason']}" if not r["passed"] else ""
            print(f"  {status} {r['id']}{detail}{fail}")
        print(f"  {'─'*40}")
        print(f"  通过: {tier_passed}/{tier_total} ({tier_passed/tier_total*100:.0f}%)" if tier_total > 0 else "  N/A")

    # ── 总览 ──
    total_passed = sum(1 for r in all_results if r["passed"])
    total = len(all_results)

    print(f"\n{'='*50}")
    print(f"📊 综合报告")
    print(f"   总用例: {total}")
    print(f"   通过: {total_passed} ✅")
    print(f"   失败: {total - total_passed} ❌")
    print(f"   通过率: {total_passed/total*100:.0f}%" if total > 0 else "   N/A")

    # 按工程方法论的质量门
    t0_pass = sum(1 for r in t0_results if r["passed"])
    t0_total = len(t0_results)
    t1_pass = sum(1 for r in t1_results if r["passed"])
    t1_total = len(t1_results)
    t2_pass = sum(1 for r in t2_results if r["passed"])
    t2_total = len(t2_results)

    t0_rate = t0_pass / t0_total * 100 if t0_total > 0 else 0
    t1_rate = t1_pass / t1_total * 100 if t1_total > 0 else 0
    t2_rate = t2_pass / t2_total * 100 if t2_total > 0 else 0

    releasable = (t0_rate == 100 and t1_rate == 100 and t2_rate >= 80)

    print(f"\n📊 质量门")
    print(f"   T0 触发: {t0_pass}/{t0_total} ({t0_rate:.0f}%) {'✅' if t0_rate == 100 else '❌'} 要求: 100%")
    print(f"   T1 边界: {t1_pass}/{t1_total} ({t1_rate:.0f}%) {'✅' if t1_rate == 100 else '❌'} 要求: 100%")
    print(f"   T2 框架: {t2_pass}/{t2_total} ({t2_rate:.0f}%) {'✅' if t2_rate >= 80 else '❌'} 要求: ≥80%")
    print(f"\n{'✅ 可发布' if releasable else '❌ 未达标 — 需要修复后重新校验'}")

    # ── 输出 JSON ──
    report = {
        "date": datetime.now().isoformat(),
        "skill_path": str(skill_path),
        "triggers_count": len(triggers),
        "total_cases": total,
        "passed": total_passed,
        "failed": total - total_passed,
        "pass_rate": f"{total_passed/total*100:.0f}%",
        "quality_gate": {
            "T0": {"pass": t0_pass, "total": t0_total, "rate": f"{t0_rate:.0f}%", "required": "100%"},
            "T1": {"pass": t1_pass, "total": t1_total, "rate": f"{t1_rate:.0f}%", "required": "100%"},
            "T2": {"pass": t2_pass, "total": t2_total, "rate": f"{t2_rate:.0f}%", "required": "≥80%"},
        },
        "releasable": releasable,
        "details": all_results,
    }

    report_path = evals_dir / "skill-validation-report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n📁 详细报告: {report_path}")

    return releasable


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
