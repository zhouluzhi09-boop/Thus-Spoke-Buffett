# 巴菲特如是说 — 维护指南

> 用户文档 → [项目主页 README](../../../README.md)
> 那里有功能介绍、安装方式、使用教程。本文档是开发者维护指南。

## 快速开始

```bash
# 1. 放素材：把新文本放到 raw/buffett/
# 2. 蒸馏概念
/distill raw/buffett/.../新素材.html

# 3. 发现盲区（可选）
/blindspot "零利率环境下 DCF 的调整"

# 4. 更新认知框架（当新概念与旧框架有张力时）
/cognition cards/A.md, cards/B.md

# 5. 校验
/validate
```

## 目录结构

```
raw/buffett/          ← 放素材（只读，不要改）
  notes/cards/        ← /distill 产出
  notes/cognition/    ← /cognition 产出
  notes/cognition/    ← 沿革考据和方案设计
evolution/            ← /blindspot 产出

.claude/skills/buffett-wisdom/
  SKILL.md            ← 最终产品（手动更新）
  evals/              ← /validate 读这里的测试用例
```

## 命令一览

| 命令 | 做什么 | 产出位置 |
|------|--------|---------|
| `/distill 素材路径` | 从原文提取概念卡片 | raw/buffett/notes/cards/ |
| `/cognition 卡片A, 卡片B` | 从多张卡片合成认知流程 | raw/buffett/notes/cognition/ |
| `/blindspot 主题` | 记录框架不适用的场景 | evolution/blindspots/ |
| `/validate` | 跑三层校验，输出通过率 | 终端 + JSON 报告 |
| `/redteam 概念` | 对抗式压力测试框架 | evolution/debates/ |
| `/crazy 问题` | 犀利模式回答 | — |
| `/buffett 问题` | 显式触发 Skill | — |

## 迭代周期

```
新素材 → /distill → /validate 确认通过 → 手动更新 SKILL.md → /validate 再次校验
```

改动 SKILL.md 后务必跑 `/validate`，确保没有改坏已有的测试用例。
