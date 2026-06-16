从多张 L1 概念卡片中提取巴菲特的认知操作流程，按 L2 认知操作模板生成文件。

## 参数

$ARGUMENTS — 逗号分隔的 L1 卡片文件路径（至少 2 张卡片）

## 模板

读取 `assets/templates/cognition-record.md`，严格按模板结构填充。

## 规则

- 决策流程使用 ASCII 树形图（├─ └─）
- "素材支撑"表格必须列出每步决策对应的卡片出处
- 如果发现可被一次性排除的场景，填写"排除模式"
- 完成后提示："跑 `python scripts/validate-framework.py` 校验"
