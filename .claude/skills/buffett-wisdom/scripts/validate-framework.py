#!/usr/bin/env python3
"""
validate-framework.py — L2 认知框架校验
校验每份认知操作文件是否有 ≥2 个独立素材支撑、逻辑链路是否完整。

用法: python validate-framework.py [--cognition-dir path/to/cognition]
"""
import sys, re, json, glob, os, io
from pathlib import Path
from datetime import datetime

# Fix Windows GBK encoding for emoji output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

COGNITION_DIR = os.environ.get(
    "COGNITION_DIR", "raw/buffett/notes/cognition"
)

# 认知操作文件的必备要素
FRAMEWORK_CHECKS = [
    {
        "name": "素材溯源",
        "pattern": r"(source|来源|素材|原文|Cunningham|Hagstrom|年报|年信|巴菲特说)",
        "min_hits": 2,
        "fail_msg": "缺少 ≥2 个可追溯的素材来源",
    },
    {
        "name": "逻辑链路",
        "pattern": r"(因为|所以|因此|→|推论|导致|结果|结论|判断)",
        "min_hits": 3,
        "fail_msg": "逻辑推理链路不足（<3 处因果/结论标记）",
    },
    {
        "name": "具体案例",
        "pattern": r"(案例|例如|比如|实例|如 |禧诗|可乐|盖可|纺织|2008|1973|所罗门)",
        "min_hits": 2,
        "fail_msg": "缺少 ≥2 个具体案例支撑",
    },
    {
        "name": "可操作输出",
        "pattern": r"(步骤|流程|决策|排除|优先级|排序|选择|检查|判断)",
        "min_hits": 3,
        "fail_msg": "缺乏可操作的决策步骤或检查点",
    },
    {
        "name": "边界说明",
        "pattern": r"(不适用的|边界|局限|例外|但.*(不是|不能)|不可|不能|不该)",
        "min_hits": 1,
        "fail_msg": "未说明框架的边界或不适用场景",
    },
]


class FrameworkValidator:
    def __init__(self, cognition_dir):
        self.cognition_dir = Path(cognition_dir)
        if not self.cognition_dir.exists():
            for candidate in [
                Path("D:/Obsidian/知识库/知识库/raw/buffett/notes/cognition"),
                Path("raw/buffett/notes/cognition"),
            ]:
                if candidate.exists():
                    self.cognition_dir = candidate
                    break

        self.results = []
        self.passed = 0
        self.failed = 0

    def scan_files(self):
        pattern = str(self.cognition_dir / "*.md")
        files = glob.glob(pattern)
        if not files:
            print(f"❌ 未找到认知操作文件: {pattern}")
            return False
        print(f"📄 找到 {len(files)} 份认知操作文件\n")
        return files

    def check_frontmatter(self, content, filename):
        issues = []
        fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not fm_match:
            issues.append("❌ 缺少 frontmatter")
            return issues

        fm = fm_match.group(1)
        for field in ["title", "source", "type"]:
            if not re.search(rf"{field}:", fm):
                issues.append(f"⚠️  frontmatter 缺少 {field} 字段")
        return issues

    def check_framework(self, content, filename):
        issues = []
        for check in FRAMEWORK_CHECKS:
            hits = len(re.findall(check["pattern"], content, re.IGNORECASE))
            if hits < check["min_hits"]:
                issues.append(
                    f"❌ {check['name']}: {check['fail_msg']} (当前 {hits}/{check['min_hits']})"
                )
        return issues

    def check_cross_refs(self, content, filename):
        refs = re.findall(r"\[\[(.*?)\]\]", content)
        if len(refs) < 1:
            return ["⚠️  缺少对其他概念卡片的交叉引用"]
        return []

    def validate_file(self, filepath):
        filename = Path(filepath).stem
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        all_issues = []
        all_issues.extend(self.check_frontmatter(content, filename))
        all_issues.extend(self.check_framework(content, filename))
        all_issues.extend(self.check_cross_refs(content, filename))

        errors = [i for i in all_issues if i.startswith("❌")]
        warns = [i for i in all_issues if i.startswith("⚠️")]
        passed = len(errors) == 0

        result = {
            "file": filename,
            "passed": passed,
            "errors": errors,
            "warnings": warns,
            "path": filepath,
        }
        self.results.append(result)

        if passed:
            self.passed += 1
        else:
            self.failed += 1

        return result

    def run(self):
        files = self.scan_files()
        if not files:
            return False

        for f in sorted(files):
            r = self.validate_file(f)
            status = "✅" if r["passed"] else "❌"
            print(f"{status} {r['file']}")
            for e in r["errors"]:
                print(f"   {e}")
            for w in r["warnings"]:
                print(f"   {w}")

        return self.report()

    def report(self):
        total = self.passed + self.failed
        print(f"\n{'='*50}")
        print(f"📊 L2 认知框架校验报告")
        print(f"   总文件数: {total}")
        print(f"   通过: {self.passed} ✅")
        print(f"   失败: {self.failed} ❌")
        print(f"   通过率: {self.passed/total*100:.0f}%" if total > 0 else "   N/A")

        report_json = {
            "date": datetime.now().isoformat(),
            "total": total,
            "passed": self.passed,
            "failed": self.failed,
            "pass_rate": f"{self.passed/total*100:.0f}%" if total > 0 else "N/A",
            "details": [
                {
                    "file": r["file"],
                    "passed": r["passed"],
                    "errors": r["errors"],
                    "warnings": r["warnings"],
                }
                for r in self.results
            ],
        }

        report_path = self.cognition_dir / "framework-validation-report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report_json, f, ensure_ascii=False, indent=2)
        print(f"\n📁 详细报告: {report_path}")

        return self.failed == 0


if __name__ == "__main__":
    cognition_dir = sys.argv[1] if len(sys.argv) > 1 else COGNITION_DIR
    validator = FrameworkValidator(cognition_dir)
    success = validator.run()
    sys.exit(0 if success else 1)
