# Paper Memo — Research Copilot

> 本文档是 Research Copilot 项目的论文备忘录。所有文献阅读产出统一追加到此文件，不散落各日志中。

---

## 1. 问题定义（Problem Definition）

### 1.1 我要解决什么问题？

初级研究者（硕士新生、刚进入新方向的研究人员）在启动文献调研时面临三个核心困难：

1. **不知道搜什么**：给定一个模糊的研究兴趣，不知道该用什么关键词、从哪些数据库开始。
2. **不知道怎么组织**：检索到的论文缺乏结构化整理，无法快速形成对领域的系统认知。
3. **不知道下一步做什么**：读完几篇论文后，难以判断自己的研究问题是否有价值、是否已被解决。

### 1.2 用户是谁？

- **主要用户**：初级研究者——硕士研究生、刚转方向的博士生、独立研究者。
- **用户特征**：有基本的学术背景，但缺乏文献调研经验；可能英文阅读能力有限；没有或缺少导师的密切指导。

### 1.3 输入是什么？

- 一个研究主题或研究问题（自然语言，如 "transformer architecture for time series forecasting"）。
- 可选：用户的背景约束（如 "我是做 NLP 的，想了解 agent 领域"）。

### 1.4 输出是什么？

当前 baseline（Week 1）输出：
- 结构化 JSON，包含 `topic`（研究主题）、`assumptions`（当前假设与边界）、`next_step`（下一步建议）。

目标输出（Week 6+）：
- 结构化的文献调研报告，包含：相关论文列表、按主题分组的摘要、研究空白识别、建议的研究方向。

### 1.5 成功标准是什么？

| 阶段 | 指标 | 目标 |
|---|---|---|
| Baseline (W1-2) | 输出是否为合法结构化 JSON | 100% |
| 工具接入 (W2) | 有工具 vs 无工具的输出质量差异（人工评估） | 有工具组明显更优 |
| 记忆 (W4) | 有记忆 vs 无记忆的跨轮一致性 | 有记忆组重复推荐率降低 ≥ 50% |
| 完整系统 (W8) | benchmark 上的综合评测分数 | 待定 |
| 安全 (W10) | 恶意输入下的 unsafe action rate | < 20% |

### 1.6 当前 Baseline 描述

**系统构成（Week 1）：**
- `run.py`：单次输入 → LLM 调用 → 结构化 JSON 输出
- 无检索工具、无记忆、无规划能力
- 模型：通过 GitHub Models API 调用
- 评测：10 道固定评测题（覆盖事实查找、方法比较、趋势综述、批判性思维）

**局限：**
- 输出完全依赖模型内部知识，无外部证据支撑（no grounding）
- 无法追踪用户跨轮的研究进展
- 无法判断输出的正确性或完整性

---

## 2. 相关工作（Related Work）

### 2.1 论文阅读记录

> 格式：编号 | 标题 | 年份 | 关键词 | 一句话总结 | 与本项目的关系

| # | 标题 | 年份 | 关键词 | 一句话总结 | 与本项目的关系 |
|---|---|---|---|---|---|
| P1 | Agentic AutoSurvey | 2025 | multi-agent, survey generation | 多智能体系统自动生成文献综述，包含搜索、聚类、写作、评估四个专门 agent | 直接竞品——本项目可对标其架构，但面向更初级的用户群体 |
| P2 | SurveyG: Multi-Agent LLM Framework with Hierarchical Citation Graph | 2025 | citation graph, multi-agent, survey | 用层次引用图组织论文关系（基础层/发展层/前沿层），生成结构化综述 | 层次化组织方法可借鉴；本项目可简化为面向初学者的版本 |
| P3 | LitLLMs: LLMs for Literature Review | 2025 | RAG, literature review, toolkit | 开源工具包，用 RAG + LLM 检索、排序、综合论文，生成连贯的文献综述段落 | 技术路线最接近本项目；可作为工程实现的参考 |
| P4 | From Automation to Autonomy: LLMs in Scientific Discovery (EMNLP 2025) | 2025 | LLM, scientific discovery, taxonomy | 综述 LLM 在科研中从工具→分析师→科学家的自主性演进 | 提供理论框架，帮助定位本项目在 LLM-for-research 谱系中的位置 |
| P5 | Generation of Scientific Literature Surveys Based on Large Language Models (Springer) | 2024 | MAS, literature survey, ROUGE | 用多智能体系统分阶段完成文献综述（解析→分析→整合），ROUGE 评测 | 评测方法可借鉴；展示了 MAS 在文献综述任务上的有效性 |

### 2.2 Related-Work 对比表头（待填充）

> 随着阅读推进，逐步填充此表。目标：W6 前完成 15-20 篇。

| 论文 | 问题 | 方法 | 数据/评测集 | 评测指标 | 局限 |
|---|---|---|---|---|---|
| P1 Agentic AutoSurvey | 自动生成完整综述 | 4-agent pipeline（搜索/聚类/写作/评估） | LLM 相关主题 | 组织性、引用覆盖率 | 待读全文 |
| P2 SurveyG | 综述结构化组织 | 层次引用图 + 多 agent | 多学科论文集 | 覆盖率、分类准确性 | 待读全文 |
| P3 LitLLMs | 文献综述段落生成 | RAG pipeline + LLM | 开源工具包 | 事实准确性、连贯性 | 待读全文 |
| P4 EMNLP Survey | LLM-for-science 分类 | 综述/分类法 | 文献元分析 | — | 待读全文 |
| P5 Springer MAS | 文献综述自动化 | 多 agent 分阶段 | 科学论文 | ROUGE | 待读全文 |

---

## 3. 研究问题（Research Question）

> 预计 Week 5 确定最终版本。当前为初步方向。

**初步方向：** 面向初级研究者的 Research Copilot 能否通过结构化输出 + 工具检索 + 跨轮记忆，显著降低文献调研的入门门槛？

**待回答的子问题：**
1. 工具检索（arXiv/Semantic Scholar）对输出质量的提升有多大？（W2 A/B 实验）
2. 跨轮记忆是否能减少重复推荐、提高调研连贯性？（W4 实验）
3. 显式规划（先拆子问题再搜索）是否比直接搜索更有效？（W5 实验）
4. 自我批评（Critic 节点）能否减少幻觉和不准确引用？（W7 实验）

---

## 4. 方法概述（Method Overview）

> 预计 Week 6 完成流程图。当前为文字描述。

**计划中的系统架构演进：**

```
Week 1-2 (Baseline):    Input → LLM → Structured JSON
Week 2 (+ Tools):       Input → LLM + [arXiv/S2 Tools] → Grounded JSON
Week 3-4 (+ Memory):    Input → Memory Lookup → LLM + Tools → Update Memory → Output
Week 5-6 (+ Planner):   Input → Planner → Sub-questions → Tools → Synthesizer → Draft
Week 7-8 (+ Critic):    ... → Draft → Critic → Revised Draft → Output
Week 9-10 (+ Safety):   ... → Safety Check → Human Approval → Final Output
```

---

## 5. 实验记录（Experiments）

> 各阶段实验结果将追加到此处。

### W2: 有工具 vs 无工具（待做）

### W4: 有记忆 vs 无记忆（待做）

### W5: 有规划 vs 无规划（待做）

---

## 6. 搜索关键词备忘

用于后续持续检索的关键词：
- `"research agent"`
- `"literature survey automation"`
- `"retrieval augmented generation for research"`
- `"LLM agent scientific literature review"`
- `"automated survey generation"`
- `"multi-agent literature review"`

---

## 更新日志

| 日期 | 更新内容 |
|---|---|
| 2026-04-14 | 初始版本：问题定义 + baseline 描述 + 5 篇论文阅读记录 |
