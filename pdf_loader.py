import fitz
from pathlib import Path

def read_pdf_text(pdf_path: str) -> str:
    """
    读取 PDF 文本
    输入：PDF 文件路径
    输出：字符串
    """
    # 1.打开PDF
    doc = fitz.open(pdf_path)
    # 2.遍历每一页
    paper_texts = []
    for page in doc:
        text = page.get_text()
        paper_texts.append(text)
    doc.close()
    raw_text = "\n".join(paper_texts)

    return raw_text

def should_skip_line(line: str) -> bool:
    """
    判断是否为无效行
    输入：字符串
    输出：布尔值
    """
    stripped = line.strip()

    if not stripped:
        return True

    if stripped in {"目录", "摘", "要", "引", "言"}:
        return True

    if stripped.isdigit():
        return True

    if len(stripped) == 1 and stripped.isalpha():
        return True

    if "...." in stripped:
        return True

    return False

def clean_pdf_text(raw_text: str) -> str:
    """
    清理 PDF 文本
    输入：字符串
    输出：字符串
    """
    # 1.切分为文本列表
    lines = raw_text.splitlines()
    # 2.去掉首尾空白
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if should_skip_line(stripped):
            continue
        cleaned_lines.append(stripped)
    # 3.合并文本
    cleaned_text = "\n".join(cleaned_lines)
    return cleaned_text
    
def is_bad_title_line(line: str) -> bool:
    """
    判断是否为无效标题行
    输入：字符串
    输出：布尔值
    """

    lower_line = line.lower()

    if "draft version" in lower_line:
        return True

    if "目录" in line:
        return True

    if len(line.strip()) < 5:
        return True

    if len(line.strip()) > 200:
        return True

    if line.strip().isdigit():
        return True

    return False

def guess_title(cleaned_text: str, pdf_path: str) -> str:
    """
    猜标题
    输入：清理后的字符串
    输出：字符串
    """
    # 1.切分为文本列表
    lines = cleaned_text.splitlines()
    # 2.先在清洗后的前几行找到符合条件的标题
    for line in lines[:30]:
        candidate = line.strip()
        if not candidate:
            continue
        if is_bad_title_line(candidate):
            continue
        return candidate
    # 3.如果找不到，就用文件名
    return Path(pdf_path).stem # .stem 作用：提取路径里不带后缀的文件名

def extract_pdf_content(pdf_path: str) -> dict:
    """
    提取 PDF 内容
    输入：PDF 文件路径
    输出：字典
    """
    raw_text = read_pdf_text(pdf_path)

    cleaned_text = clean_pdf_text(raw_text)
    if not cleaned_text:
        raise ValueError(f"PDF 内容为空：{pdf_path}")
    
    title = guess_title(cleaned_text, pdf_path)
    return {
        "file_name": Path(pdf_path).name,
        "title": title,
        "text": cleaned_text,
    }