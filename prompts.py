def build_paper_summary_prompt(topic: str, paper_text: str) -> str:
    """
    构建论文总结提示
    输入：
    - topic: 课题主题
    - paper_text: 单篇论文正文
    输出：
    - 核心内容、方法贡献、与当前课题的关系、证据摘录
    """
    prompt = f"""
你是一个科研阅读助手。你的任务是根据给定论文内容，生成一份简洁、结构化、可用于科研讨论的论文总结。

请注意：
1. 只能基于提供的论文内容回答，不要编造不存在的信息。
2. 如果论文内容中没有明确提到某项信息，请明确写“未明确提及”。
3. 输出内容要适合科研组会讨论和后续论文写作准备。
4. 语言保持准确、简洁、条理清楚。

当前研究主题：
{topic}

论文内容：
{paper_text}

请严格输出 JSON，不要输出任何额外解释，不要使用 Markdown 代码块。

返回格式如下：
{{
  "summary": "...",
  "method_and_contribution": "...",
  "relation_to_topic": "...",
  "evidence_quotes": ["...", "..."]
}}
        """
    return prompt.strip()

def build_global_summary_prompt(topic: str, meeting_notes: str, paper_summaries: list[dict]) -> str:
    """
    构建全局总结提示
    输入：
    - topic: 课题主题
    - meeting_notes: 会议记录
    - paper_summaries: 多篇论文总结
    输出：
    - 导师要求、下周任务、背景草稿、创新点草稿
    """
    # 1.先把每篇论文拼接成字符串
    paper_blocks = []

    for index, paper in enumerate(paper_summaries, start=1):
        block = f"""
                    论文 {index}
                    标题：{paper["title"]}
                    核心内容：{paper["summary"]}
                    方法与贡献：{paper["method_and_contribution"]}
                    与当前课题关系：{paper["relation_to_topic"]}
                    证据摘录：{"；".join(paper["evidence_quotes"])}
                """
        paper_blocks.append(block)

    papers_text = "\n\n".join(paper_blocks)
    prompt = f"""
你是一个面向科研资料整理与论文写作的助手。你的任务是根据研究主题、组会记录和论文总结，输出一份面向下周科研推进的结构化结果。

请注意：
1. 优先依据组会记录中的信息提炼导师要求。
2. 下周任务需要结合研究主题、导师要求和论文内容，尽量具体、可执行。
3. 背景草稿要适合后续写论文或开题材料。
4. 创新点草稿要谨慎，不要夸大；如果现有信息不足，请明确说明只是初步设想。
5. 只能基于提供的材料回答，不要编造额外实验结果或研究结论。

当前研究主题：
{topic}

组会记录：
{meeting_notes}

论文总结：
{papers_text}

请严格按照以下格式输出：
{{
  "advisor_requirements": "...",
  "next_week_tasks": ["...", "..."],
  "background_draft": "...",
  "innovation_draft": "...",
}}
        """
    return prompt.strip()

    