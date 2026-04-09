import json

# 这个脚本用于加载评测题，统计类别分布，检查题目结构，并根据用户输入的研究主题构建结果。
def load_eval_questions():# 从指定路径加载评测题数据
    with open("data/eval_questions.json", "r", encoding="utf-8") as f:
        return json.load(f)


def count_categories(eval_questions):#·统计评测题中各类别的数量
    category_counts = {}
    for question in eval_questions:
        category = question["category"]
        category_counts[category] = category_counts.get(category, 0) + 1
    return category_counts


def validate_eval_questions(eval_questions):#检查评测题的结构是否完整，确保每道题都包含必要的字段
    required_fields = {"id", "category", "question"}
    has_error = False

    for i, item in enumerate(eval_questions, start=1):
        for field in required_fields:
            if field not in item:
                print(f"第 {i} 道题缺少字段：{field}")
                has_error = True

    if not has_error:
        print("评测题检查完成，所有题目结构完整。")


def build_result(topic):#根据用户输入的研究主题构建结果，包含当前版本的假设和下一步计划
    return {
        "topic": topic,
        "assumptions": [
            "当前版本暂未接入外部检索工具。",
            "当前版本的目标是先固定输入输出格式。",
        ],
        "next_step": "下一步将接入文献检索工具，以提供相关信息。",
    }


def main():#主函数，执行加载评测题、统计类别、检查结构，并根据用户输入构建结果的流程
    eval_questions = load_eval_questions()
    print(f"当前共有 {len(eval_questions)} 道评测题。")

    category_counts = count_categories(eval_questions)
    print("各类别题目数量:")
    for category, count in category_counts.items():
        print(f"  {category}: {count}")

    validate_eval_questions(eval_questions)

    topic = input("请输入研究主题: ").strip()
    if not topic:
        print("研究主题不能为空。")
        return

    result = build_result(topic)
    print(json.dumps(result, ensure_ascii=False, indent=4))

# 运行主函数
if __name__ == "__main__":
    main()
    
