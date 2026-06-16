#!/usr/bin/env python3
"""
validate-evidence.py — L1 证据校验
校验每张概念卡片的每条规则是否有原文出处支撑。

用法: python validate-evidence.py [--cards-dir path/to/cards]
"""
import sys, re, json, glob, os, io
from pathlib import Path
from datetime import datetime

# Fix Windows GBK encoding for emoji output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CARDS_DIR = os.environ.get("CARDS_DIR", "raw/buffett/notes/cards")

# 每条规则必须满足的证据标准
REQUIRED_FIELDS = {
    "原文出处":   r"(原文出处|source|原文|出处)",
    "决策规则":   r"(决策规则|应用规则|判断标准)",
    "应用示例":   r"(应用示例|案例|实例|应用)",
    "边界条件":   r"(边界条件|边界|局限|不适用)",
    "双链关联":   r"(双链关联|关联|双链|交叉引用)",
}


class EvidenceValidator:
    def __init__(self, cards_dir):
        self.cards_dir = Path(cards_dir)
        if not self.cards_dir.exists():
            self.cards_dir = Path(".") / cards_dir
            if not self.cards_dir.exists():
                # fallback: look in vault structure
                for candidate in [
                    Path("D:/Obsidian/知识库/知识库/raw/buffett/notes/cards"),
                    Path("raw/buffett/notes/cards"),
                ]:
                    if candidate.exists():
                        self.cards_dir = candidate
                        break

        self.results = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def scan_cards(self):
        """扫描所有概念卡片"""
        pattern = str(self.cards_dir / "*.md")
        files = glob.glob(pattern)
        if not files:
            print(f"❌ 未找到概念卡片: {pattern}")
            print(f"   当前目录: {os.getcwd()}")
            return False
        print(f"📄 找到 {len(files)} 张概念卡片\n")
        return files

    def check_source_attribution(self, content, card_name):
        """核心检查：每条规则必须可追溯到原文"""
        issues = []

        # 1. 检查 frontmatter 中的 source 字段
        fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        has_source_in_fm = False
        if fm_match:
            fm = fm_match.group(1)
            if re.search(r'source:', fm) or re.search(r'chapter:', fm):
                has_source_in_fm = True

        if not has_source_in_fm:
            issues.append("⚠️  frontmatter 中缺少 source 或 chapter 字段")

        # 2. 检查是否有原文引用块（> 开头）
        quotes = re.findall(r'^>.*$', content, re.MULTILINE)
        if len(quotes) < 2:
            issues.append("⚠️  原文引用少于2条（建议每条规则至少1条出处）")

        # 3. 检查是否引用了具体章节
        chapter_refs = re.findall(r'(第[0-9]+章|part\d+|Chapter\s*\d+|年报|年信)', content)
        if not chapter_refs and not re.search(r'(巴菲特原话|巴菲特在.*中|巴菲特原文)', content):
            issues.append("⚠️  未找到具体章节引用（第X章/年报年份）")

        # 4. 检查"巴菲特原文"或"巴菲特说"的引用
        buffett_direct = re.findall(r'巴菲特[:：]|巴菲特原文|巴菲特亲自|巴菲特写道', content)
        if not buffett_direct and len(quotes) < 3:
            issues.append("⚠️  缺少巴菲特的直接引语标注")

        return issues

    def check_rule_completeness(self, content, card_name):
        """检查核心字段是否齐全"""
        issues = []
        for field, pattern in REQUIRED_FIELDS.items():
            if not re.search(pattern, content):
                issues.append(f"❌ 缺少必要字段：{field}")
        return issues

    def check_rule_count(self, content, card_name):
        """检查决策规则是否有编号或明确列出"""
        rules = re.findall(r'^\d+\.\s', content, re.MULTILINE)
        if len(rules) < 2:
            issues = ["⚠️  决策规则少于2条（或未使用编号格式）"]
        else:
            issues = []
        return issues, len(rules)

    def validate_card(self, filepath):
        """校验单张卡片"""
        card_name = Path(filepath).stem
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        all_issues = []

        # 证据检查
        source_issues = self.check_source_attribution(content, card_name)
        all_issues.extend(source_issues)

        # 完整性检查
        field_issues = self.check_rule_completeness(content, card_name)
        all_issues.extend(field_issues)

        # 规则数量检查
        count_issues, rule_count = self.check_rule_count(content, card_name)
        all_issues.extend(count_issues)

        # 判定
        errors = [i for i in all_issues if i.startswith("❌")]
        warns = [i for i in all_issues if i.startswith("⚠️")]

        passed = len(errors) == 0

        result = {
            "card": card_name,
            "passed": passed,
            "errors": errors,
            "warnings": warns,
            "rule_count": rule_count,
            "file": filepath,
        }
        self.results.append(result)

        if passed:
            self.passed += 1
        else:
            self.failed += 1
        self.warnings += len(warns)

        return result

    def run(self):
        files = self.scan_cards()
        if not files:
            return False

        for f in sorted(files):
            r = self.validate_card(f)
            status = "✅" if r["passed"] else "❌"
            print(f"{status} {r['card']} ({r['rule_count']} 条规则)")
            for e in r["errors"]:
                print(f"   {e}")
            for w in r["warnings"]:
                print(f"   {w}")

        return self.report()

    def report(self):
        total = self.passed + self.failed
        print(f"\n{'='*50}")
        print(f"📊 L1 证据校验报告")
        print(f"   总卡片数: {total}")
        print(f"   通过: {self.passed} ✅")
        print(f"   失败: {self.failed} ❌")
        print(f"   警告: {self.warnings} ⚠️")
        print(f"   通过率: {self.passed/total*100:.0f}%" if total > 0 else "   通过率: N/A")

        if self.failed > 0:
            print(f"\n🔴 以下卡片未通过证据校验:")
            for r in self.results:
                if not r["passed"]:
                    print(f"   - {r['card']}: {', '.join(r['errors'])}")

        # 输出 JSON
        report_json = {
            "date": datetime.now().isoformat(),
            "total": total,
            "passed": self.passed,
            "failed": self.failed,
            "warnings": self.warnings,
            "pass_rate": f"{self.passed/total*100:.0f}%" if total > 0 else "N/A",
            "details": [
                {
                    "card": r["card"],
                    "passed": r["passed"],
                    "errors": r["errors"],
                    "warnings": r["warnings"],
                    "rule_count": r["rule_count"],
                }
                for r in self.results
            ],
        }

        report_path = self.cards_dir / "evidence-validation-report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_json, f, ensure_ascii=False, indent=2)
        print(f"\n📁 详细报告: {report_path}")

        return self.failed == 0


if __name__ == "__main__":
    cards_dir = sys.argv[1] if len(sys.argv) > 1 else CARDS_DIR
    validator = EvidenceValidator(cards_dir)
    success = validator.run()
    sys.exit(0 if success else 1)
