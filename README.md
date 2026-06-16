# 巴菲特如是说 (Buffett Wisdom)

> 把巴菲特八十年的投资认知，压缩成一份 AI 可直接执行的决策引擎。

这不是一个提示词。这是从 67 份原始素材（巴菲特致股东的信、CNBC 专访、年会发言、研究专著）中，经过 13 批次系统蒸馏产出的可安装 Claude Code Skill。

---

## 一、功能

### 核心能力：对 7 类场景的结构化分析

| 场景 | 你问什么 | 你得到什么 |
|:--:|------|------|
| 1. 公司初判 | "帮我看看XX公司" | 四关速查表：能力圈→护城河→管理层→价格，每关 ✅/⚠️/❌ + 历史参照 |
| 2. 市场恐慌/狂热 | "大跌了怎么办" | 历史参照（过去几次类似危机的结果）+ 市场先生分析 + 行动框架 |
| 3. 商业决策 | "该收购还是回购" | 资本配置五级优先级排序 + 惯性驱使检查 + 正反历史案例 |
| 4. 管理层判断 | "这个 CEO 靠谱吗" | 嫁女儿测试 + 四个红旗信号扫描 + 激励结构检查 |
| 5. 估值判断 | "现在贵不贵" | DCF 三问 + 安全边际方向性判断 + 泰德·威廉姆斯击球区判定 |
| 6. 投资哲学/人生 | "怎么选职业" | 能力圈思维 + 长期复利 + 巴菲特自己的故事 |
| 7. 框架极限 | "比特币能用这方法吗" | 诚实声明（在不在框架内）+ 为什么不在 + 替代视角 |

### 特色机制

- **`/crazy` 犀利模式**：卸下防备的巴菲特——CNBC 专访状态。金句先出，讽刺跟上，原则不变措辞锋利。
- **纵向历史深度**：每个观点都自带时间坐标。"这个概念 1972 年从禧诗糖果开始，1985 年纺织厂关闭时被验证，2008 年金融危机时被实战检验。"
- **MCP 实时数据感知**：配置 Yahoo Finance MCP 后，自动获取实时股价/PE/ROE/财报，喂入四关框架分析。没有 MCP 时温和提示安装。

### 教学级内容

Skill 不只是回答问题——回答本身就是一堂投资课：

> **你问**："怎么看特斯拉？"
>
> **Skill 回答**：我们不了解特斯拉。这让我想起格雷厄姆教给我的一条原则——如果你不能用简单的语言说清楚一家公司为什么能持续赚钱，你就不懂它。看看历史：20 世纪初美国有超过 2000 家汽车公司，今天只剩下三家。通用汽车 2009 年破产时，市场份额仍然是全美第一。市场份额和护城河是两回事。查理有一次跟我说——大概在 1970 年代——他说："沃伦，你不必去跨越七英尺的栏杆。找那些一英尺的，跨过去就行了。"我们花了二十年才真正学会这句话。

每个回答里藏着一个概念的教学：什么是护城河、为什么市场份额不等于护城河、格雷厄姆和芒格在这一点上的分工、泰德·威廉姆斯的击球区类比。

---

## 二、项目结构

```
buffett-wisdom/
├── SKILL.md                         # 主文件：角色+原则+流程+风格+边界
├── cognitive-framework/             # L2 认知操作层
│   ├── concept-neural-network.md    # 十大概念知识神经网络总图
│   ├── decision-process-map.md      # 完整决策流程（第〇关→四关→监控）
│   ├── munger-influence.md          # 芒格影响谱系（吸收/重表达/缺失/分歧）
│   ├── buffett-voice-dna.md         # 表达风格DNA（句式/意象/语气/幽默）
│   ├── priority-rules.md            # 资本配置五级优先级排序
│   └── 管理层评估决策树.md            # 管理层四关筛选+秘书测试+嫁女儿测试
├── evolution/                       # L3 框架演化层
│   ├── blindspots/
│   │   └── blindspot-catalog.md     # 13条盲区+每条对应L3种子问题
│   ├── new-era-cases/
│   │   └── 2008-crisis-war-game.md  # 2008金融危机L2推演 vs 实际对照
│   ├── debates/                     # 待社区：框架争议
│   └── contributions/               # 待社区：新情景分析
├── evals/                           # 测试体系
│   ├── t0-trigger/  (10个)          # 触发测试：什么时候该/不该加载Skill
│   ├── t1-boundary/ (8个)           # 边界测试：不该做的事绝不能做
│   └── t2-framework/ (8个)          # 框架测试：回答是否用了正确的认知框架
├── scripts/                         # 校验脚本
│   ├── validate-evidence.py         # L1证据校验：每条规则有出处吗？
│   ├── validate-framework.py        # L2框架校验：认知操作有案例支撑吗？
│   └── validate-skill.py            # 综合校验：26个测试用例全过吗？
├── assets/templates/                # 标准化模板
│   ├── concept-card.md              # L1概念卡片模板
│   ├── cognition-record.md          # L2认知操作模板
│   ├── blindspot-entry.md           # L3盲区条目模板
│   └── test-case.md                 # 测试用例模板
└── commands/                        # 斜杠命令
    ├── distill.md    /distill        # 素材→L1卡片
    ├── cognition.md  /cognition      # 卡片→L2认知
    ├── blindspot.md  /blindspot      # 主题→L3盲区
    ├── validate.md   /validate       # 运行全量校验
    ├── buffett.md    /buffett        # 显式调用Skill
    ├── case.md       /case 公司      # 查经典案例分析
    └── crazy.md      /crazy          # 犀利模式
```

---

## 三、安装

### 方式一：Claude Code 一键安装（推荐）

```bash
claude plugins install buffett-wisdom@anthropic-marketplace
```

### 方式二：Git 克隆

```bash
# 1. 克隆到 Claude Code 的 skills 目录
git clone https://github.com/你的用户名/buffett-wisdom.git \
  ~/.claude/skills/buffett-wisdom

# 2. 或者克隆到当前项目的 .claude/skills/ 下（仅当前项目生效）
git clone https://github.com/你的用户名/buffett-wisdom.git \
  .claude/skills/buffett-wisdom
```

### 方式三：手动复制

```bash
# 将整个 buffett-wisdom/ 目录复制到以下任意位置：
#   全局：~/.claude/skills/buffett-wisdom/
#   项目：.claude/skills/buffett-wisdom/
```

### 激活验证

安装后，在 Claude Code 中测试：

```
> 巴菲特怎么看价值投资？
```

如果回答以第一人称"我们"开头、引用了格雷厄姆或芒格、包含至少一个日常比喻 —— Skill 已生效。

### 可选：配置实时金融数据（Yahoo Finance MCP）

```bash
# 在全局 MCP 配置中加入
# 文件：~/.claude/.mcp.json
{
  "yfinance": {
    "command": "npx",
    "args": ["yfinance-mcp-ts"]
  }
}
```

配置后，Skill 会自动获取实时股价/PE/ROE/财报数据用于分析。未配置时不影响使用——Skill 会温和提示可安装。

---

## 四、使用

### 自然触发

直接说话就行——不需要任何命令前缀：

```
"巴菲特怎么看价值投资？"
"市场大跌了，我好慌"
"帮我分析一下可口可乐"
"该不该收购竞争对手？"
"这个 CEO 靠谱吗？"
```

### 斜杠命令

| 命令 | 做什么 |
|------|--------|
| `/buffett 问题` | 显式触发 Skill（当问题不含触发词时） |
| `/crazy 问题` | 犀利模式——CNBC 专访巴菲特 |
| `/case 公司名` | 查巴菲特历史上对该公司的经典分析 |
| `/validate` | 跑三层校验，检查 Skill 质量 |

### 维护命令（供开发者使用）

| 命令 | 做什么 |
|------|--------|
| `/distill 素材路径` | 从新素材提取概念卡片 |
| `/cognition A.md, B.md` | 从多张卡片合成认知操作 |
| `/blindspot 主题` | 记录框架不适用的新场景 |

---

## 五、质量

### 校验通过率

```
T0 触发测试: 10/10 ✅  正向：5个投资问题正确触发；负向：Python/天气/医疗等均未误触
T1 边界测试:  8/8 ✅  股票推荐/市场预测/精确估值/加密/人身攻击/政治/杠杆/承诺——全部守住
T2 框架测试:  8/8 ✅  四关流程/比喻使用/第一人称/排除思维/确定性分层/自嘲/现金期权/说不知道
────────────────
综合通过率: 26/26 (100%)
质量门状态: ✅ 可发布
```

### 素材溯源

10 张 L1 概念卡片，每张：
- ≥ 2 条巴菲特原文直接引用
- 具体章节/年报年份标注
- 正反案例均有历史锚点
- 边界条件声明

---

## 六、迭代维护

Skill 是活的。读了新传记、发现新盲区、遇到新市场环境——都可以通过内置命令更新：

```bash
# 放新素材到 raw/
# 蒸馏
/distill raw/新书/第3章.html

# 校验
/validate

# 如果通过率下降 → 修复 → 再校验
```

详细维护指南见 `.claude/skills/buffett-wisdom/README.md`。

---

## 七、许可证与致谢

- 素材来源：巴菲特致股东的信（Cunningham 编译版）、Hagstrom《巴菲特之道》、《穷查理宝典》（查理·芒格）、CNBC 专访逐字稿
- 工程方法受 [mao-chiang-wisdom-skills](https://github.com/20240610ldx-hub/mao-chiang-wisdom-skills) 项目启发
- 知识库架构遵循 [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 模式
