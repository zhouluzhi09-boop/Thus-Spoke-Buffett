运行三层校验脚本，输出 SKILL.md 当前质量状态报告。

## 执行

依次运行：
1. `python scripts/validate-evidence.py raw/buffett/notes/cards`
2. `python scripts/validate-framework.py raw/buffett/notes/cognition`
3. `python scripts/validate-skill.py`

## 输出

汇总三层报告，以质量门判断结尾：
```
T0 触发: X/Y (Z%) ✅/❌ 要求 100%
T1 边界: X/Y (Z%) ✅/❌ 要求 100%
T2 框架: X/Y (Z%) ✅/❌ 要求 ≥80%
L1 证据: X/Y (Z%) ✅/❌
L2 框架: X/Y (Z%) ✅/❌

✅ 可发布 / ❌ 有 X 项未达标
```

如有失败项，列出具体问题和推荐修复方向。
