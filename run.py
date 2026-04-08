import json
# 运行前先统计一下评测题的数量和类别分布
with open("data/eval_questions.json", "r", encoding="utf-8") as f:
    eval_questions = json.load(f)
print(f"当前共有 {len(eval_questions)} 道评测题。")

category_counts = {}
for q in eval_questions:
    category = q["category"]
    category_counts[category] = category_counts.get(category, 0) + 1

print("各类别题目数量:")
for category, count in category_counts.items():
    print(f"  {category}: {count}")

# 检查每道题是否包含必要的字段
required_fields = {"id", "category", "question"}
has_error = False
for i,item in enumerate(eval_questions,start=1):
    for field in required_fields:
        if field not in item:
            print(f"检查到第{i}道题，发现其缺少字段：{field}")
            has_error = True
if not has_error:
    print("评测题检查完成,所有题目结构完整。")

    
# 让用户输入研究主题
topic= input("请输出研究主题: ").strip()
if not topic:
    print("研究主题不能为空。")
else:
    result={
        "topic": topic,
        "assumptions": [
            "当前版本暂未接入外部检索工具",

        ],
        "next_step": "下一步将接入文献检索工具，以提供相关信息。",
        }
    print(json.dumps(result, ensure_ascii=False, indent=4))
    