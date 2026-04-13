---
description: "Use when editing or creating journal entries in journal/*.md. Enforces template structure, YAML frontmatter fields, and naming conventions for day logs, week plans, and week summaries."
applyTo: "journal/**"
---

# Journal 格式规范

## 文件命名
- 日志：`WeekXXDayYY-YYYY-M-D.md`（如 `Week01Day03-2026-4-9.md`）
- 周规划：`WeekXX目标规划.md`
- 周总结：`WeekXX总结.md`

## YAML Frontmatter 必填字段

### 日志 (day_log)
```yaml
template_version: 3
doc_type: day_log
ssot_role: daily_execution
week: "Week X"
day: "Day X"
date: "YYYY-MM-DD"
related_goal_ids: [G1]
```

### 周规划 (week_plan)
```yaml
template_version: 3
doc_type: week_plan
ssot_role: week_definition
week: "Week X"
goal_ids: [G1, G2, G3]
```

### 周总结 (week_summary)
```yaml
template_version: 3
doc_type: week_summary
ssot_role: week_summary
week: "Week X"
goal_ids: [G1, G2, G3]
```

## 日志正文结构要求
- `## 事前` 部分必须包含：承接点、主要服务目标、一句话目标、完成线
- 每个任务块必须包含：关联 G#、动作、完成线、产出、科研训练标签
- 任务块时长 30-90 分钟
- 每天至少 1 个科研训练标签：`#对比实验` / `#失败记录` / `#prompt日志` / `#related-work` / `#问题表述`

## G# 引用规则
- 日志中的 G# 必须对应当周周规划中定义的目标编号（G1/G2/G3）
- 不要发明周规划中不存在的 G#

## 证据格式
- `[G#][类型] 描述`，类型为：命令 / 文件 / 输出

## paper_memo 规则
- 涉及文献的产出统一追加到 `docs/paper_memo.md`，不散落各日志中
