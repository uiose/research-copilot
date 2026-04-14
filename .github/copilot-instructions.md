# Project Guidelines

## 项目概述
Research Copilot：面向初级研究者的 AI Agent 原型。12 周路线图迭代推进。
详见 [docs/project_definition.md](docs/project_definition.md) 和 [README.md](README.md)。

## 技术栈
- Python 3.x + LangGraph + Chat Model API (GitHub Models)
- Chroma（向量数据库，后续引入）
- arXiv / Semantic Scholar（检索工具，后续引入）

## 项目结构约定
- `run.py`：程序入口
- `graph.py`：LangGraph 图结构（Week 2 开始引入）
- `src/`：核心模块
- `data/eval_questions.json`：固定评测题集
- `docs/paper_memo.md`：文献产出累积文档（每周追加，不散落）
- `journal/`：学习日志，遵循模板格式（见 `.github/instructions/journal-format.instructions.md`）
- `outputs/`：运行产出
- `tests/`：测试
- `note/`：技术笔记

## 代码约定
- 环境变量通过 `.env` 加载，不要硬编码 API key / token
- 结构化输出字段：`topic`, `assumptions`, `next_step`（当前 baseline）
- 评测题集字段变更需同步更新 `REQUIRED_OUTPUT_FIELDS`

## 路线图数据源
- 唯一权威数据源：`ai_agent_research_12week_workbench_2026-V4.html` 中 `DATA.weeks` 数组
- Week 1 不涉及 graph.py（留到 Week 2 与 LangGraph 一起引入）

## 学习日志规范
- 文件格式和命名规范见 `.github/instructions/journal-format.instructions.md`
- 科研训练标签：`#对比实验` / `#失败记录` / `#prompt日志` / `#related-work` / `#问题表述`
- 证据格式：`[G#][类型] 描述`

## 状态判断证据优先级
- 状态判断时，最终以工程文件、仓库产物与可复核证据为准
- `journal/` 只作为辅助线索，不作为最终完成判定依据
- 若日志自述与工程现实冲突，优先相信代码、数据、测试、输出与可验证结果
- 占位文件不等于功能完成；计划、意图和 Todo 不等于交付完成

## Agent 协作体系

### 定制文件总览
```
.github/
├── copilot-instructions.md          ← 全局指令（本文件），所有对话自动加载
├── agents/
│   ├── learning-diagnosis-planner.agent.md   ← 规划者（读写）
│   ├── status-evaluator.agent.md             ← 状态验收官（只读）
│   ├── learning-coach.agent.md               ← 学习教练（只读）
│   └── code-review-coach.agent.md            ← 代码教练（只读）
└── instructions/
    └── journal-format.instructions.md        ← 编辑 journal/ 时自动加载
```

### Agent 职责边界

| Agent | 一句话职责 | 读写 | 什么时候用 | 不要用来做 |
|---|---|---|---|---|
| **Learning Diagnosis Planner** | 诊断进度 → 生成按天计划 | 读写 | 周初规划、周中重排、卡住需要重新拆计划 | 问概念、要资源、review 代码 |
| **Status Evaluator** | 对照路线图与工程证据判断真实完成状态 | 只读 | 周中核查进度、周末验收、确认 minimum_bar / output / exit_criteria 是否真正落地 | 生成新计划、改代码、只凭日志判定完成 |
| **Learning Coach** | 概念引导 + 资源推荐 + 任务逐步陪跑 | 只读 | 不懂某个概念、想要学习资源、需要有人引导思考、做任务时逐步引导 | 生成计划、改代码、跑命令 |
| **Code Review Coach** | 指出问题 → 解释原因 → 引导改进 | 只读 | 写完代码想要反馈、不确定设计是否合理 | 直接帮你写代码、生成计划 |
| *（默认 agent）* | 写代码、改文件、跑命令 | 读写 | 实际编码、文件修改、终端操作、一般问答 | — |

### 典型工作流

```
1. 周初/卡住 → @Learning Diagnosis Planner 诊断并出计划
2. 周中核查/周末验收 → @Status Evaluator 判断真实完成情况
3. 学习过程中不懂 → @Learning Coach 引导理解 + 推荐资源
4. 写完代码 → @Code Review Coach 审查反馈
5. 动手改代码 → 默认 agent 执行
```

### Prompt 示例

**@Learning Diagnosis Planner** — 规划与重排
```
今天是周日，本周还剩今天，帮我诊断 Week 1 进度并出今天的计划
```
```
我卡在 LLM 调用这块两天了，帮我重排本周剩余计划
```
```
这周只剩 3 天，每天大概 4 小时，帮我出一个压缩版计划
```

**@Status Evaluator** — 状态验收与完成判断
```
帮我判断当前 Week 1 的真实完成情况，按状态矩阵输出，并指出日志和工程文件是否一致
```
```
检查一下本周 minimum_bar 和 output 有没有真正落到仓库里，不要只看 journal
```
```
请按 milestone 验收视角看当前状态：哪些是已完成，哪些只是占位，哪些还缺证据
```

**@Learning Coach** — 概念引导
```
什么是 structured output？为什么 Agent 需要结构化输出？
```
```
ReAct 和 function calling 有什么区别？我总搞混
```
```
Tool calling 的原理是什么？有没有推荐的入门资源？
```

**@Learning Coach** — 任务陪跑
```
我要给 run.py 接入 LLM API，一步步带我做
```
```
我想跑通评测流程，不知道从哪开始，引导我
```
```
路线图说这周要做 prompt 工程实验，帮我拆步骤然后逐步引导
```

**@Code Review Coach** — 代码审查
```
帮我看看 run.py 的错误处理是否合理
```
```
graph.py 的状态设计有没有问题？
```
```
我刚写完 prompt 构造函数，review 一下
```

**默认 agent** — 编码执行
```
在 run.py 里加一个 --verbose 参数
```
```
帮我把 eval_questions.json 的字段校验提取成独立函数
```
```
跑一下 python run.py "transformer architecture" 看看输出
```

### 边界红线
- Learning Coach 和 Code Review Coach **绝不修改文件**，只提供引导
- Learning Diagnosis Planner 只写 journal 和 memory，不改项目代码
- Status Evaluator **绝不修改文件**，只做状态判断；且必须以工程产物为准，不得仅凭 journal 认定完成
- 需要实际编码时，回到默认 agent
