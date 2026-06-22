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
        if stripped:
            cleaned_lines.append(stripped)
    # 3.合并文本
    cleaned_text = "\n".join(cleaned_lines)
    return cleaned_text
    

def guess_title(cleaned_text: str, pdf_path: str) -> str:
    """
    猜标题
    输入：清理后的字符串
    输出：字符串
    """
    # 1.切分为文本列表
    lines = cleaned_text.splitlines()
    # 2.先在清洗后的前几行找到第一个长度适中的非空行
    for line in lines[:10]:
        if 5 <= len(line) <= 200:
            return line
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