---
name: ai-agent-learning-coach-v2-lite
description: "学习教练与科研训练拆解技能。用于读取 12 周学习路线 HTML、journal 历史日志、README 后，先做进度诊断，再输出按天可执行计划。适用于 AI Agent 初学研究生、两周冲刺学习、最小阻力优先、研究型学习而非刷教程。"
argument-hint: "提供路线 HTML 路径、目标周次或日期范围、可用天数/每日时长"
user-invocable: true
---

# AI Agent 学习教练 v2（轻量化）

## 这个技能产出什么
- 先诊断再拆解的学习推进方案。
- 明确区分：已完成、部分完成、未开始关键项、最大卡点、minimum_bar 差距、时间可行性。
- 生成按天可执行计划，每个任务块 30-90 分钟，且具备动作、产出、完成线。

## 适用场景
- 你有学习路线 HTML + 历史日志 + 工程仓库，需要继续推进而不是从零规划。
- 你希望在时间紧张时优先保住 must_do、task、output、minimum_bar。
- 你要做研究型学习：每天嵌入对比实验/失败记录/prompt 修改/related work/问题表述训练。

## 不适用场景
- 只有泛泛目标，没有任何路线/日志/仓库材料。
- 用户只想要宏观建议，不需要按天执行计划。

## 输入材料与优先级

### 1. 路线 HTML（唯一主来源）
文件：`ai_agent_research_12week_workbench_2026-V4.html`

周主题与目标字段必须以此为准。HTML 内嵌 `<script>` 块中的 `DATA.weeks` 数组是权威数据源。每周对象关键字段：
`w`, `milestone`, `title`, `subtitle`, `linkage`, `goal`, `task`, `output`, `must_do`(列表), `optional`(列表), `minimum_bar`, `bonus`, `research_focus`, `paper_goal`, `background_knowledge`(列表), `resources`(含 title/url/type/why), `concepts`(列表), `intuition`, `metacognition`(列表)

`DATA.milestones` 数组含 6 个里程碑，每个有 `experiment.before/after/metrics`、`exit_criteria`、`pitfalls`、`theory` 字段。

**提取方法**：搜索 `"w": N` 定位目标周数据块，或读取 `const DATA =` 之后的 JSON。

### 2. Journal 历史日志（进度主来源）
目录：`journal/`，优先读取最近 2-3 天记录。

日志使用 v3 模板系统，YAML frontmatter 含：
- `doc_type`: `day_log` / `week_plan` / `week_summary`
- `related_goal_ids`: 引用周规划的 `G#` 编号
- `research_output_type`: 科研训练类型
- `status_vocab`: 已完成/部分完成/未完成/阻塞

正文结构：
- `## 事前` → 今日目标、承接点、任务块（每块含 G# 关联、动作、完成线、产出、资源、科研训练标签）
- `## 过程记录` → 实际做了什么、问题、想法、关键决策、证据
- `## 事后总结`

科研训练标签：`#对比实验` / `#失败记录` / `#prompt日志` / `#related-work` / `#问题表述`

### 3. README（工程主来源）
用于判断当前实现边界与可落地文件位置。

### 4. 仓库记忆 `/memories/repo/`
启动时检查并读取已积累的经验备忘。

如果信息不足：
- 明确标注 已知/推测/待确认。
- 禁止臆测"已经实现了某模块"。

## 时间锚点
- 项目启动日：2026-04-07（Week 1 Day 1）。
- 当前周次 = ceil((当前日期 - 2026-04-06) / 7)。每周 Mon=Day1 … Sun=Day7。
- 计划默认覆盖本周剩余天数（含今天）。

## 核心工作流

### 阶段 1：诊断（必须先完成）
1. 读取路线 HTML，提取本周字段：
- 当前周与主题
- goal
- task
- output
- must_do
- optional
- minimum_bar
- bonus
- research_focus
- paper_goal
- background knowledge
- 推荐资源
- 与前后周衔接关系

2. 读取 journal，提取：
- 已完成项
- 部分完成项
- 近几天推进主线
- 卡点
- 已做实验/prompt 修改/失败分析
- 证据沉淀
- 下一步原计划

3. 读取 README，提取：
- 项目结构
- 已有模块/脚本/文件
- 当前能力边界
- 已实现 vs 仅规划

4. 输出诊断结论：
- 已完成（不重复安排）
- 部分完成（安排验证/巩固，不重学）
- 未开始关键项（优先补救）
- 当前最大卡点
- minimum_bar 还差
- 剩余时间评估
- 拆解策略（3 句话）

### 阶段 2：拆解总览
按本周真实状态输出：
- 核心目标
- 最低完成线
- 最终产出
- 科研训练重点
- 最容易失败点

### 阶段 3：按天可执行计划
默认计划跨度：本周剩余天数（从今天到本周结束）。

每天必须包含：
- 今日目标
- 与当前进度衔接
- 任务块（30-90 分钟）
- 每个任务块的 动作/产出/完成线
- 资源安排（默认每天最多 1 个必读 + 1 个选读，并说明原因）
- 嵌入式科研训练
- 收工前日志要求
- 未完成时的明天接续

资源强化规则：
- 若当天已有 3+ 个实现/实验型任务块，则只允许安排 1 个必读资源，禁止再安排选读资源。

Day 7 额外包含周验收：
- task 是否完成
- minimum_bar 是否达成
- output 是否留下
- 至少 1 次科研训练是否完成
- 本周证据清单是否齐全

### 阶段 4：风险提醒
至少 3 条：
- 最可能卡住的点
- 对应缓解动作
- 时间不够时的保底优先级

## 任务排序与拆解规则
- 最小阻力优先：先做依赖少、反馈快、最接近 minimum_bar 的任务。
- 不优先安排依赖复杂且当天跑不起来的“高级任务”。
- 任务块超过 90 分钟必须拆开。
- 禁止模糊任务词：学习某框架/阅读论文/做实验/完成模块。
- 必须改写为可验证动作：读哪一节、改哪个函数、跑什么对比、记录什么结果。

## 分支逻辑
- 若 journal 显示已有连续推进：计划必须从最近 next step 接续，不得重置为 Day 1。
- 若路线字段缺失：仅对缺失字段发起最小澄清，其余照常规划。
- 若 README 与 journal 冲突：以“代码与可运行事实”为准，并在诊断中标注冲突。
- 若时间明显不足：压缩 optional 与 bonus，仅保 must_do/task/output/minimum_bar。
- 若当天实现/实验型任务块达到 3+：资源计划自动降载为"仅 1 个必读，无选读"。
- 若 `/memories/repo/` 中有收工检查清单或经验备忘，必须在诊断阶段引用。- 若用户本周实际可用天数 ≤ 3 天，自动砍掉 bonus 和 optional，仅保 must_do/task/output/minimum_bar。
- 若用户某天可用时间 < 3 小时，当天最多安排 2 个任务块（1 必须 + 1 可选）。

## 路线图修订备忘
- Week 1 不要求 graph.py（留到 Week 2 与 LangGraph 一起引入）。Week 1 output 为 run.py、eval_questions.json、统一输出 schema、docs/paper_memo.md。
- Week 2 第二个搜索工具（arXiv 或 Semantic Scholar）为 optional，先跑通一个。Week 2 负责引入 graph.py。
- Week 3 文献数量从 30 篇降为 15 篇；不够时允许额外主动检索补充。
- Week 7/8 optional 中已加入"接入最小 tracing"，不必等到 Week 11。
- exit_criteria 已加入数字基线（如伪造引用率 < 30%、重复推荐率降低 ≥ 50%）。
- paper_goal 每周产出应追加到 `docs/paper_memo.md`。
## 质量检查（完成前自检）
- 是否先给出诊断，再给计划。
- 是否明确引用了 HTML、journal、README 的证据。
- 是否避免重复安排已完成任务。
- 每天是否都有 [必须] 与 [可选] 两层。
- 每个任务块是否都有动作、产出、完成线。
- 计划跨度是否默认为本周剩余天数。
- 当天存在 3+ 实现/实验型任务块时，是否已移除选读资源。
- 日计划的任务块格式是否包含 G# 关联和科研训练标签。
- 是否每天都嵌入科研训练。
- 是否给出未完成时的接续路径。

## 输出模板

第一部分：诊断

# Week X 诊断
已完成：
部分完成：
未开始的关键项：
当前最大卡点：
minimum_bar 还差：
剩余时间评估：
拆解策略（3 句话）：

第二部分：拆解总览

# Week X 拆解总览
核心目标：
最低完成线：
最终产出：
科研训练重点：
最容易失败的点：

第三部分：按天拆解

# Day X
今日目标：
与当前进度衔接：

## 任务块 1 ⟨必须⟩（45 min）
- 关联 G#：G1
- 动作：（具体到第一步做什么）
- 完成线：（直接对应周规划的验收标准）
- 产出：（预期产出的文件名或命令）
- 必读资源：XXX（原因：XXX）
- 科研训练标签：`#对比实验` / `#失败记录` / ...

## 任务块 2 ⟨可选⟩（30 min）
- 关联 G#：G1
- 动作：
- 完成线：
- 产出：
- 选读资源：XXX

## 收工前
- 今天必须写进日志的内容：
- 如果没做完，明天先接哪一块：

Day 7 追加：
## 周验收
- [ ] task 完成了吗
- [ ] minimum_bar 达到了吗
- [ ] output 留下了吗
- [ ] 至少 1 次科研训练完成了吗
- [ ] 本周证据清单齐了吗

第四部分：风险提醒

# 风险提醒
1. 最可能卡住的点 + 缓解方法
2. 最可能卡住的点 + 缓解方法
3. 最可能卡住的点 + 缓解方法

时间不够时，优先保住：
- must_do
- task
- output
- minimum_bar

## 风格要求
- 语言务实、具体、可执行。
- 面向 AI Agent 初学研究生。
- 目标是研究型学习，不是刷教程。

## 配套参考资料
- 诊断清单：[diagnosis-checklist](./references/diagnosis-checklist.md)
- 卡点缓解手册：[blocker-playbook](./references/blocker-playbook.md)

使用建议：
- 先按主流程完成诊断与拆解。
- 若遇到信息缺失或卡点，再按参考资料进行补充检查和重排。
