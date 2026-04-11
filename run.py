import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


API_URL = "https://models.github.ai/inference/chat/completions"
EVAL_QUESTIONS_PATH = Path("data/eval_questions.json")
REQUIRED_OUTPUT_FIELDS = {"topic", "assumptions", "next_step"}


def load_env():
    """加载 Day 03 所需的环境变量。"""
    load_dotenv()

    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("请在 .env 文件中设置 GITHUB_TOKEN 环境变量。")

    model_name = os.getenv("MODEL_NAME")
    if not model_name:
        raise ValueError("请在 .env 文件中设置 MODEL_NAME 环境变量。")

    return github_token, model_name


def build_prompt(topic):
    """构造要求模型输出固定 JSON 协议的提示词。"""
    return f"""
你是一个研究助手。

请围绕用户输入的研究主题，返回一个 JSON 对象。
要求：
1. 只能输出 JSON，不要输出额外解释
2. 不要使用 Markdown 代码块
3. JSON 中只能包含以下字段：
   - topic
   - assumptions
   - next_step

字段要求：
- topic：直接写用户输入的研究主题
- assumptions：用列表表示当前阶段的假设、限制或边界，至少写 2 条
- next_step：给出下一步建议动作

用户输入的研究主题是：
{topic}
""".strip()


def call_llm(prompt, model_name, github_token):
    """调用 GitHub Models 接口，获取模型原始输出文本。"""
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        print("模型调用失败。")
        print(f"错误信息: {exc}")
        return None

    try:
        data = response.json()
    except ValueError as exc:
        print("模型返回内容不是合法的 JSON。")
        print(f"错误信息: {exc}")
        return None

    content = data.get("choices", [{}])[0].get("message", {}).get("content")
    if not isinstance(content, str) or not content.strip():
        print("模型返回为空，或返回结构不符合预期。")
        return None

    return content.strip()


def load_eval_questions():
    """从固定路径加载评测题集。"""
    with EVAL_QUESTIONS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def count_categories(eval_questions):
    """统计评测题集中各类别的数量。"""
    category_counts = {}
    for question in eval_questions:
        category = question["category"]
        category_counts[category] = category_counts.get(category, 0) + 1
    return category_counts


def validate_eval_questions(eval_questions):
    """检查每道评测题是否包含必要字段。"""
    required_fields = {"id", "category", "question"}
    has_error = False

    for index, item in enumerate(eval_questions, start=1):
        for field in required_fields:
            if field not in item:
                print(f"第 {index} 道题缺少字段：{field}")
                has_error = True

    if not has_error:
        print("评测题检查完成，所有题目结构完整。")

    return has_error


def extract_json_text(model_output):
    """尽量从模型文本中提取 JSON 主体。"""
    cleaned_output = model_output.strip()

    if cleaned_output.startswith("```"):
        lines = cleaned_output.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            cleaned_output = "\n".join(lines[1:-1]).strip()

    try:
        json.loads(cleaned_output)
        return cleaned_output
    except json.JSONDecodeError:
        pass

    start = cleaned_output.find("{")
    end = cleaned_output.rfind("}")
    if start != -1 and end != -1 and start < end:
        candidate = cleaned_output[start : end + 1]
        try:
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            return None

    return None


def validate_model_result(data):
    """检查模型输出是否满足固定字段协议。"""
    actual_fields = set(data.keys())
    missing_fields = REQUIRED_OUTPUT_FIELDS - actual_fields
    extra_fields = actual_fields - REQUIRED_OUTPUT_FIELDS

    if missing_fields:
        print(f"模型返回缺少字段：{missing_fields}")
        return False

    if extra_fields:
        print(f"模型返回包含多余字段：{extra_fields}")
        return False

    if not isinstance(data["topic"], str) or not data["topic"].strip():
        print("字段 topic 必须是非空字符串。")
        return False

    if not isinstance(data["next_step"], str) or not data["next_step"].strip():
        print("字段 next_step 必须是非空字符串。")
        return False

    if not isinstance(data["assumptions"], list) or len(data["assumptions"]) < 2:
        print("字段 assumptions 必须是至少包含 2 条内容的列表。")
        return False

    if not all(isinstance(item, str) and item.strip() for item in data["assumptions"]):
        print("字段 assumptions 中的每一项都必须是非空字符串。")
        return False

    return True


def parse_model_output(model_output):
    """将模型原始输出解析为符合协议的 Python 字典。"""
    json_text = extract_json_text(model_output)
    if not json_text:
        print("解析模型输出失败，输出不是有效的 JSON 格式。")
        return None

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as exc:
        print("解析模型输出失败，输出不是有效的 JSON 格式。")
        print(f"错误信息: {exc}")
        return None

    if not isinstance(data, dict):
        print("模型输出必须是 JSON 对象，而不是数组或其他类型。")
        return None

    if not validate_model_result(data):
        return None

    return data


def precheck_eval_questions_structure():
    """在主流程开始前检查题集是否可用，并打印统计信息。"""
    eval_questions = load_eval_questions()
    has_error = validate_eval_questions(eval_questions)
    if has_error:
        print("评测题结构存在问题，请修正后再运行。")
        return True

    print(f"当前共有 {len(eval_questions)} 道评测题。")
    print("各类别题目数量:")
    for category, count in count_categories(eval_questions).items():
        print(f"  {category}: {count}")

    return False


def main():
    """完成题集检查、主题输入、模型调用与结果解析。"""
    if precheck_eval_questions_structure():
        return

    topic = input("请输入研究主题: ").strip()
    if not topic:
        print("研究主题不能为空。")
        return

    try:
        github_token, model_name = load_env()
    except ValueError as exc:
        print(exc)
        return

    prompt = build_prompt(topic)
    model_output = call_llm(prompt, model_name, github_token)
    if not model_output:
        print("未能获取模型输出。")
        return

    result = parse_model_output(model_output)
    if not result:
        return

    print(json.dumps(result, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()
    
