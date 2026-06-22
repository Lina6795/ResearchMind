# Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
# V0-普通LLM Demo
## MVP 
- 每篇论文的输出：论文摘要总结；方法/贡献点；与当前课题的关系
- 全局输出：组会记录里导师的要求；下周任务列表；一段可直接拿去写作的“研究背景”或“创新点草稿”
## 目录分工
- app.py
  - 程序入口
  - 读取输入参数
  - 调用 pdf_loader.py
  - 拼装 prompt
  - 调用模型
  - 保存到 outputs/
- pdf_loader.py
  - 负责解析 PDF 文本
  - 做基础清洗，比如去掉多余换行、页眉页脚噪音
  - 返回每篇论文的标题和正文片段
- prompts.py
  - 放 prompt 模板
  - 不要把 prompt 写死在 app.py
  - 后面升级到 V2 Skill 时，这里会自然演化成任务模块
- outputs/
  - 保存生成结果，建议按时间戳命名
- examples/
  - 放 demo PDF、组会记录示例、主题示例
  - 面试展示时很重要，能直接复现
## 数据流
1. 用户提供 pdf_paths + meeting_notes + topic
2. pdf_loader.py 抽取每篇论文文本
3. app.py 对每篇论文先做一次“单篇总结”
4. 再把“所有论文总结 + 组会记录 + topic”喂给一个“综合生成”prompt
5. 输出统一写入 markdown
