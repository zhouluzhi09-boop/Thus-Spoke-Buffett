# KnowledgeBase Schema

本文件定义 LLM 如何维护此知识库，遵循 Karpathy LLM Wiki 模式。

## 架构

三层架构：
- **raw/** — 原始资料，不可变，LLM只读
- **wiki/** — LLM生成的markdown文件，LLM全权维护
- **CLAUDE.md**（本文件）— 模式文件，定义wiki组织规范和操作流程

## 目录结构

```
raw/
  articles/     # 网页文章、博客
  clippings/    # 浏览器剪藏、网页摘录
  papers/       # 学术论文、PDF
  books/        # 书籍章节笔记
  podcasts/     # 播客转录/笔记
  conversations/# 聊天记录、会议记录
  data/         # 数据文件、电子表格
wiki/
  index.md      # 内容导向目录（每页一行，含链接+摘要）
  log.md        # 时间线日志（只追加）
  entities/     # 人物、组织、工具等实体页面
  concepts/     # 核心概念、框架、方法论
  summaries/    # 原始资料摘要（一个来源一篇）
  comparisons/  # 对比表格（方案、工具、观点对比）
  syntheses/    # 跨来源综合报告、综述
  templates/    # 页面模板
scripts/        # 可选的本地搜索/工具脚本
```

## Digest 流程

当用户将新资料放入 `raw/` 并指示处理时：

1. 读取资料全文
2. 与用户讨论关键发现
	1. 在 `wiki/summaries/` 中创建摘要页面（命名：`{来源简称}.md`）
3. 更新 `wiki/index.md` 的对应分类
4. 更新所有相关实体页（`wiki/entities/`）和概念页（`wiki/concepts/`）
5. 在 `wiki/log.md` 追加条目

## Query 流程

当用户对wiki提问时：

1. 先读 `wiki/index.md` 定位相关页面
2. 深入阅读相关页面
3. 综合答案，附来源引用（格式：`[来源名](summaries/xxx.md)`）
4. 如答案有长期价值，征求用户同意后归档为新页面

## Lint 流程

定期（或用户触发）检查：

- 页面间是否存在矛盾声明
- 新资料是否使旧声明过时
- 是否存在无入链的孤立页面
- 重要概念是否缺少专属页面
- 交叉引用是否缺失
- 可通过网络搜索填补的数据空缺

## 页面规范

所有wiki页面遵循：

- **Frontmatter**：YAML格式，含 `title`、`type`（entity/concept/summary/comparison/synthesis）、`tags`、`date`、`sources`（关联来源数）
- **标题**：`# 页面标题`，简洁明确
- **交叉引用**：正文中主动链接到相关wiki页面
- **来源引用**：`> 来源: [资料名](summaries/xxx.md)`
- **最后更新**：页脚标注 `*更新于 YYYY-MM-DD*`

## 日志格式

```
## [YYYY-MM-DD] {ingest|query|lint} | {标题}

- **操作**: 简要描述
- **影响的页面**: [页面1](wiki/xxx.md), [页面2](wiki/xxx.md)
- **关键决定**: 如有
```

## 原则

- **LLM写，用户读**：wiki内容由LLM生成和维护，用户负责策展来源、指导分析、提出好问题
- **每次消化一个来源**：保持参与度，读摘要、检查更新、指导重点
- **好答案归档**：比较分析、新发现的联系应沉淀到wiki，不丢失在聊天历史中
- **索引优先**：查询时先读 index.md，用索引定位而非全文搜索
