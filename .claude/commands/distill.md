从给定的素材文件中提取巴菲特的核心概念，按 L1 概念卡片模板生成卡片。

## 参数

$ARGUMENTS — 素材文件路径（可以是 raw/ 下的任意 .md, .html, .txt 文件）

## 模板

读取 `assets/templates/concept-card.md`，严格按模板结构填充。

## 规则

- 每条决策规则必须有至少一节原文出处（> 引用块 + 章节号）
- 正面示例 ≥ 2，反面示例 ≥ 1
- 边界条件 ≥ 1
- 完成后提示："跑 `python scripts/validate-evidence.py` 校验"
