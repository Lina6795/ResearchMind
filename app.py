import argparse
from pathlib import Path
from datetime import datetime
import os
import json

# 以后再补
from pdf_loader import extract_pdf_content
from prompts import build_paper_summary_prompt, build_global_summary_prompt


def parse_args():
    """
    负责读取命令行参数
    你要支持的参数：
    - --topic
    - --meeting-notes
    - --pdf  (可重复传入 1~3 次)
    - --output (可选)
    """
    # 1. 创建 ArgumentParser
    parser = argparse.ArgumentParser(description="ResearchMind")
    # 2. 添加参数
    parser.add_argument("--topic", type=str, required=True)
    parser.add_argument("--meeting-notes", type=str, required=True)
    parser.add_argument("--pdf", type=str, action="append", required=True)
    parser.add_argument("--output", type=str, default=None)
    # 3. return args
    return parser.parse_args()


def validate_inputs(args):
    """
    负责做输入校验
    你至少要检查：
    - topic 不能为空
    - meeting_notes 文件存在
    - pdf 数量在 1~3 篇之间
    - 每个 pdf 文件都存在
    """
    # 不满足条件时：
    # - 可以 raise ValueError
    # - 或者 print 错误后退出
    if not args.topic.strip():
        raise ValueError("传入的主题不能为空")

    if not Path(args.meeting_notes).exists():
        raise FileNotFoundError(f"组会记录文件不存在：{args.meeting_notes}")

    if not args.pdf:
        raise ValueError("至少需要传入 1 篇论文 PDF")

    if not (1 <= len(args.pdf) <= 3):
        raise ValueError("论文数量必须在 1 到 3 篇之间")

    for pdf_path in args.pdf:
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"论文文件不存在：{pdf_path}")


def load_meeting_notes(meeting_notes_path):
    """
    读取组会记录文本
    输入：文件路径
    输出：字符串
    """
    # 1. 打开文件
    # 2. read()
    # 3. strip()
    # 4. return 文本
    with open(meeting_notes_path, "r", encoding="utf-8") as f:
        meeting_notes = f.read().strip()
    return meeting_notes


def load_papers(pdf_paths):
    """
    批量读取论文
    输入：pdf 路径列表
    输出：papers 列表

    每篇 paper 先统一成这种结构：
    {
        'file_name': 'xxx.pdf',
        'title': '论文标题',
        'text': '论文正文'
    }
    """
    papers = []

    for pdf_path in pdf_paths:
        # 调用 pdf_loader.py 里的函数
        # paper = extract_pdf_content(pdf_path)
        # papers.append(paper)

        # 现在还没写 pdf_loader.py，可以先用假数据顶上
        fake_paper = {
            "file_name": str(pdf_path),
            "title": "TODO: paper title",
            "text": "TODO: paper text",
        }
        papers.append(fake_paper)

    return papers


def summarize_single_paper(client, paper, topic):
    """
    对单篇论文做总结
    输入：
    - client: 模型客户端
    - paper: 单篇论文 dict
    - topic: 研究主题

    输出结构建议：
    {
        'file_name': ...,
        'title': ...,
        'summary': ...,
        'method_and_contribution': ...,
        'relation_to_topic': ...,
        'evidence_quotes': [...]
    }
    """
    # # 1. 从 paper 里拿到 title / text
    # title = paper["title"]
    # text = paper["text"]
    # # 2. 构造 prompt
    # prompt = build_paper_summary_prompt(topic, text)
    # 3. 调模型
    # response = client.generate(prompt)
    # 4. 解析结果
    # summary = response.strip()
    # 5. return 结构化结果
    # 现在模型还没接好时，先返回假结果
    return {
        "file_name": paper["file_name"],
        "title": paper["title"],
        "summary": "TODO: summary",
        "method_and_contribution": "TODO: method and contribution",
        "relation_to_topic": "TODO: relation to topic",
        "evidence_quotes": ["TODO quote 1", "TODO quote 2"],
    }


def summarize_all_papers(client, papers, topic):
    """
    批量处理所有论文
    输入：papers 列表
    输出：paper_summaries 列表
    """
    paper_summaries = []

    for paper in papers:
        summary = summarize_single_paper(client, paper, topic)
        paper_summaries.append(summary)

    return paper_summaries


def generate_global_output(client, topic, meeting_notes, paper_summaries):
    """
    生成全局输出
    输入：
    - topic
    - meeting_notes
    - paper_summaries

    输出建议：
    {
        'advisor_requirements': '...',
        'next_week_tasks': ['...', '...'],
        'background_draft': '...',
        'innovation_draft': '...'
    }
    """
    # # 1. 构造全局 prompt
    # prompt = build_global_summary_prompt(topic, meeting_notes, paper_summaries)
    # # 2. 调模型
    # response = client.generate(prompt)
    # # 3. 解析结果
    # global_output = response.strip()
    # # 4. 解析结果
    # global_output = json.loads(global_output)
    # # 4. return dict

    # 现在先返回假数据
    return {
        "advisor_requirements": "TODO: advisor requirements",
        "next_week_tasks": [
            "TODO: task 1",
            "TODO: task 2",
        ],
        "background_draft": "TODO: background draft",
        "innovation_draft": "TODO: innovation draft",
    }


def build_final_result(topic, paper_summaries, global_output):
    """
    把单篇结果和全局结果合并成最终统一结果
    """
    result = {
        "topic": topic,
        "paper_summaries": paper_summaries,
        "advisor_requirements": global_output["advisor_requirements"],
        "next_week_tasks": global_output["next_week_tasks"],
        "background_draft": global_output["background_draft"],
        "innovation_draft": global_output["innovation_draft"],
    }
    return result


def make_output_path(output_arg=None):
    """
    决定输出文件路径
    - 如果用户传了 --output，就用它
    - 否则自动生成 outputs/时间戳.md
    """
    if output_arg:
        output_path = Path(output_arg)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return str(output_path)
    
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"{timestamp}.md"
    return str(output_path)


def save_markdown_output(result, output_path):
    """
    把最终结果写成 markdown
    """
    # 1. 把 result 拼成 markdown 字符串
    lines = []
    lines.append("# ResearchMind V0 Output")
    lines.append("")

    lines.append("## 研究主题")
    lines.append(result["topic"])
    lines.append("")

    for index, paper in enumerate(result["paper_summaries"], start=1):
        lines.append(f"## 论文 {index}")
        lines.append(f"### 文件名")
        lines.append(paper["file_name"])
        lines.append("")
        lines.append("### 标题")
        lines.append(paper["title"])
        lines.append("")
        lines.append("### 核心内容")
        lines.append(paper["summary"])
        lines.append("")
        lines.append("### 方法与贡献")
        lines.append(paper["method_and_contribution"])
        lines.append("")
        lines.append("### 与当前课题关系")
        lines.append(paper["relation_to_topic"])
        lines.append("")
        lines.append("### 证据摘录")
        for quote in paper["evidence_quotes"]:
            lines.append(f"- {quote}")
        lines.append("")

    lines.append("## 导师要求")
    lines.append(result["advisor_requirements"])
    lines.append("")

    lines.append("## 下周任务")
    for task in result["next_week_tasks"]:
        lines.append(f"- {task}")
    lines.append("")

    lines.append("## 背景草稿")
    lines.append(result["background_draft"])
    lines.append("")

    lines.append("## 创新点草稿")
    lines.append(result["innovation_draft"])
    lines.append("")

    markdown_text = "\n".join(lines)

    # 2. 写入 output_path
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)


def create_llm_client():
    """
    创建模型客户端
    这一版先单独封装，main 里不要直接写一大坨初始化逻辑
    """
    # 后面再接 API key / base_url / model name
    return None


def main():
    # 1. 解析参数
    args = parse_args()

    # 2. 校验输入
    validate_inputs(args)

    # 3. 创建模型客户端
    client = create_llm_client()

    # 4. 读取组会记录
    meeting_notes = load_meeting_notes(args.meeting_notes)

    # 5. 读取 PDF，整理成 papers 列表
    papers = load_papers(args.pdf)

    # 6. 逐篇生成论文总结
    paper_summaries = summarize_all_papers(client, papers, args.topic)

    # 7. 生成全局输出
    global_output = generate_global_output(
        client=client,
        topic=args.topic,
        meeting_notes=meeting_notes,
        paper_summaries=paper_summaries,
    )

    # 8. 合并最终结果
    final_result = build_final_result(
        topic=args.topic,
        paper_summaries=paper_summaries,
        global_output=global_output,
    )

    # 9. 确定输出路径
    output_path = make_output_path(args.output)

    # 10. 保存结果
    save_markdown_output(final_result, output_path)

    # 11. 打印完成信息
    print(f"Done. Output saved to: {output_path}")


if __name__ == "__main__":
    main()