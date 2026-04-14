---
template_version: 3
doc_type: week_plan
ssot_role: week_definition
week: "Week 2"
milestone: "M1"
phase: "Phase 1 基线建立"
goal_ids:
  - G1
  - G2
  - G3
status_vocab:
  - 已完成
  - 部分完成
  - 未完成
  - 阻塞
research_output_vocab:
  - 对比实验
  - 失败案例记录
  - Prompt 修订日志
  - Related-work 笔记
  - 研究问题表述
evidence_type_vocab:
  - 命令
  - 文件
  - 输出
---

# Week 2 目标规划

> 正文像日志，关系像数据库：`G#` 负责引用，`验收标准 / 证据 / 承接点` 负责串起周计划、日执行和周总结。

## 路线图对照
- 路线图 goal：接入 arXiv / Semantic Scholar 查询工具，让系统能搜索、挑选、回答，并记录来源。
- 路线图 task：先用 LangGraph 串起 Week 1 的 run.py 逻辑，形成 graph.py 最小图结构。然后接入至少一个搜索工具（arXiv 或 Semantic Scholar），第二个为 optional。让 Agent 对同一批 10 个问题分别跑 plain chat 和 tool-using 两个版本，并输出结构化结果表。
- 路线图 output：可运行 baseline Agent、graph.py、至少一种工具、A/B 实验 CSV 或 Markdown 表、第一次失败日志。
- 路线图 paper_goal：写 baseline 章节草稿（追加到 docs/paper_memo.md）：没有工具时表现如何、有工具后改进了什么。
- 路线图 minimum_bar：能基于外部搜索结果回答至少 10 个问题，并留下来源。
- 路线图 must_do：接入 arXiv / Semantic Scholar 至少一个搜索工具；固定 search → select → answer 的最小流程；完成 plain chat vs tool-use 的第一次 A/B 表。
- 路线图 linkage（承接关系）：承接 Week 1 的骨架。为 Week 3 铺路：先有搜索基线，后面才知道 memory 带来了什么增益。

## 本周起点
- 承接点：Week 1 已完成最小骨架（run.py + 结构化 JSON + LLM 调用 + 10 题评测集 + paper_memo.md 问题定义）
- 核心问题：如何让系统从"凭内部知识回答"进化到"基于外部证据回答"？
- 一句话周目标：接入检索工具 + 用 LangGraph 建图 + 完成第一次 A/B 对比实验
- 为什么这周先做它：没有工具调用就没有 grounding，后续的记忆、规划都建立在"先能搜到东西"的前提上
- 不做会造成什么影响：系统永远停留在"聊天式问答"，无法区别于 ChatGPT 直接使用

## 本周目标

### G1 [必填] — LangGraph 最小图 + 检索工具接入
- 这一周要把什么推进到什么状态：将 run.py 的逻辑迁移到 LangGraph 图结构（graph.py），并接入至少一个检索工具（arXiv 或 Semantic Scholar）
- 验收标准：
  - `graph.py` 存在且可运行
  - 系统能接受研究主题输入，调用外部检索 API，返回带来源的结构化输出
  - 输出中包含至少 1 条来自 arXiv/S2 的真实论文引用
- 落地路径：
  1. 学习 LangGraph 基本概念（StateGraph, nodes, edges）
  2. 将 run.py 的 prompt → LLM → parse 流程改写为 graph 节点
  3. 添加 arXiv API 工具节点（search → select → answer）
  4. 端到端测试：输入主题 → 检索 → 输出带引用的 JSON
- 证据形式：文件（graph.py）/ 命令（运行截图）/ 输出（带引用的 JSON）

### G2 [必填] — A/B 对比实验（plain chat vs tool-use）
- 这一周要把什么推进到什么状态：用同一批 10 个评测题，分别跑 plain chat（无工具）和 tool-use（有工具）两个版本，输出对比表
- 验收标准：
  - 10 个问题 × 2 个版本 = 20 条输出结果
  - 对比表以 CSV 或 Markdown 格式保存在 `outputs/` 目录
  - 至少人工标注 10 个问题的"哪个版本更好"
- 落地路径：
  1. 用 run.py 跑 plain chat 版本，保存 10 条输出
  2. 用 graph.py 跑 tool-use 版本，保存 10 条输出
  3. 制作对比表，逐题标注差异
- 证据形式：文件（outputs/ab_comparison_w2.md 或 .csv）/ 输出（对比表截图）

### G3 [可选] — 研究轨：继续论文阅读 + paper_memo 更新
- 这一周要把什么推进到什么状态：在 paper_memo.md 中累计 8-10 篇论文阅读记录，并写 baseline 章节草稿
- 验收标准：
  - paper_memo.md 的论文记录数 ≥ 8
  - 新增 baseline 章节草稿（有工具 vs 无工具的对比描述）
- 落地路径：
  1. 每天读 1 篇论文的 Abstract + Introduction（30-60 分钟）
  2. 追加到 paper_memo.md 的阅读记录表
  3. W2 结束时写 baseline 章节草稿
- 证据形式：文件（docs/paper_memo.md 更新记录）

## 时间预算表
| 项目 | 预算 |
| --- | --- |
| 本周总投入时长 / 任务块 | 20-25 小时 / 约 14 个任务块 |
| 深度工作（G1 + G2） | 14-16 小时 |
| 研究轨（G3 论文阅读） | 4-5 小时 |
| 维护 / 收尾（journal、整理） | 2-3 小时 |
| 缓冲 | 2 小时 |

## 边界
- 本周不做：向量数据库接入、跨轮记忆、Planner 节点
- 如果超出范围，优先砍掉什么：G3 的论文阅读量可降至 6 篇；A/B 实验可先只做 5 题

## 资源
- 必读：arXiv API 官方文档 (https://info.arxiv.org/help/api/index.html)、LangGraph 官方总览
- 选读：ReAct 论文 (https://arxiv.org/abs/2210.03629)、Semantic Scholar API 文档

## 风险
- 这周最可能卡住的一点：LangGraph 学习曲线 + Python 基础不足导致图结构写不出来
- 提前怎么应对：先看官方 quickstart 示例照搬最小结构，不追求复杂设计；如果 LangGraph 卡太久，退化为用简单函数链模拟图结构

## 科研产出
- 本周至少留下一项：第一次 A/B 对比实验
- 类型：对比实验
- 关联目标ID：G2
- 想回答的问题：工具检索对 Research Copilot 输出质量的提升有多大？
- 最低产出：10 题对比表 + 3 句结论
- 落地路径：outputs/ab_comparison_w2.md

对比实验补充：
- 对比对象：plain chat (run.py) vs tool-use (graph.py)
- 控制变量：同一模型、同一 prompt 模板、同一 10 题评测集
- 指标：人工判断（哪个版本回答更准确/更有依据）、是否包含真实引用、幻觉数量
- 样本：eval_questions.json 中的 10 道题

## 最低完成线
- 写出 `承接点`、`核心问题`、至少 1 个 `G#`。
- 给这个 `G#` 写清 `验收标准`、`落地路径`、`证据形式`。
- 留下 1 条 `本周不做`。
- 留下 1 项 `科研产出`。
- `路线图对照` 的 7 个字段已填写（从 HTML 提取，含 paper_goal）。
