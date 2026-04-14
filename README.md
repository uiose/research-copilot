# Research Copilot

面向初级研究者与研究生的 AI Research Agent 项目。  
目标是在 12 周内，从最小 baseline 逐步构建一个可用于文献调研、结构化笔记生成与研究备忘录辅助的 `Research Copilot`。

默认主栈：`Python + LangGraph + Chat Model API + Chroma + arXiv / Semantic Scholar`

## Overview

`Research Copilot` 不是一个单纯的聊天机器人项目，而是一个围绕研究任务逐步演化的 Agent 原型。

项目将按周推进以下能力：
- 结构化输入输出
- 固定评测题集
- 大语言模型调用
- 检索与外部证据接入
- 记忆与规划
- 评测、反思与安全
- 可观测性与研究包装

当前阶段的重点不是“功能很多”，而是“边界清楚、输出可解析、可以持续迭代”。

## Current Status

当前处于 `Week 1` 收尾 → `Week 2` 过渡阶段。项目采用 **双轨并行** 策略（工程轨 60% + 研究轨 40%）。

**工程轨已完成：**
- 项目基础目录搭建
- `run.py` 最小程序入口
- 固定评测题集 [data/eval_questions.json](data/eval_questions.json)（10 题）
- 题集字段校验
- 结构化 JSON 输出
- 大语言模型接入（GitHub Models API）
- 项目定义与 journal 记录机制

**研究轨已完成：**
- [docs/paper_memo.md](docs/paper_memo.md) 问题定义（0.5 页）
- 5 篇相关论文的阅读记录

**即将推进（Week 2）：**
- LangGraph 最小图接入
- arXiv / Semantic Scholar 检索工具
- A/B 对比实验（有工具 vs 无工具）
- 继续论文阅读（目标累计 8-10 篇）

## Roadmap

### Week 1
搭建最小骨架，固定输入输出格式、评测题集与项目边界。

### Week 2
接入最小大语言模型调用，并开始引入 LangGraph 与最小检索流程。

### Week 3-4
构建文献库与记忆能力，支持跨轮研究任务。

### Week 5-6
加入显式规划与多步综合能力。

### Week 7-8
建立 benchmark，引入评测、反思与错误分析。

### Week 9-10
加入安全边界与 human-in-the-loop 机制。

### Week 11-12
完善可观测性、消融分析、研究备忘录与论文提纲。

## Repository Structure

```text
.
├─ data/       # 固定评测题集与后续实验数据
├─ docs/       # 稳定文档，如项目定义与结构说明
├─ journal/    # 按天记录的学习、实验与复盘
├─ logs/       # 运行日志
├─ outputs/    # 程序输出结果
├─ src/        # 后续模块化代码
├─ tests/      # 测试代码
└─ run.py      # 当前最小 baseline 程序入口
```

## Quick Start

```bash
python run.py
```

程序当前会：
1. 读取固定评测题集
2. 统计题目数量与类别分布
3. 检查题集字段完整性
4. 接收用户输入的研究主题
5. 输出结构化 JSON

## Current Output Contract

当前 baseline 输出固定为结构化 JSON，包含：

- `topic`
- `assumptions`
- `next_step`

这套输出协议用于保证：
- 程序结果可读
- 结果可进一步评测
- 后续接入 LLM 与检索工具时接口保持稳定

## Development Principles

项目当前遵循以下原则：

- 先做最小 baseline，再逐步加能力
- 先固定输入输出，再追求复杂功能
- 先建立固定题集，再谈评测
- 先写清边界，再接模型与工具
- 每一步都保留可复盘的记录

## Documentation

- [docs/project_definition.md](docs/project_definition.md)：按周维护的阶段性项目定义
- [docs/paper_memo.md](docs/paper_memo.md)：论文备忘录——问题定义、相关工作、研究问题、实验记录
- [journal/](journal/)：按天维护的工作记录与复盘
- [data/eval_questions.json](data/eval_questions.json)：固定评测题集
- [ai_agent_research_12week_workbench_2026-V4.html](ai_agent_research_12week_workbench_2026-V4.html)：12 周学习路线与研究工作台

## Agent Roles

项目中的协作角色目前分为：

- `Learning Diagnosis Planner`：做进度诊断与按天计划重排
- `Status Evaluator`：做状态验收与完成判断，默认先看当前周，再补一句整体状态
- `Learning Coach`：做概念引导、回答错漏诊断、资源推荐与任务陪跑
- `Code Review Coach`：做代码审查与改进建议
- 默认 agent：负责实际编码、改文件和运行命令

其中 `Status Evaluator` 有一个硬规则：

- 进度判断以工程文件、仓库产物与可复核证据为准
- `journal/` 主要提供背景、卡点和决策线索，不作为最终完成判定依据

## Learning Roadmap

[ai_agent_research_12week_workbench_2026-V4.html](ai_agent_research_12week_workbench_2026-V4.html) 是本项目的外部学习路线图与阶段参考面板。

它的主要作用是：
- 帮助快速查看 12 周整体路线，而不是只看当天任务
- 用来确认每周的目标、重点任务、最低完成线与阶段产出
- 作为 `project_definition.md`、`journal` 与实际代码推进的上层参考

在实际使用中可以这样分工：
- 路线图 HTML：看整体阶段安排与周目标
- `docs/project_definition.md`：写当前周的稳定定义
- `journal/*.md`：记录每天的推进过程
- 代码与数据文件：落实当天具体实现

## Next Step

下一步将推进（Week 2）：
- 引入 LangGraph 最小图（`graph.py`）
- 接入 arXiv / Semantic Scholar 检索工具
- 完成 A/B 对比实验（有工具 vs 无工具），结果记录到 `docs/paper_memo.md`
- 继续阅读论文，累计 8-10 篇
