#!/usr/bin/env python3
"""
classify_with_llm.py

使用 LLM 进行智能标题分类，替代硬编码的正则匹配。
适用于结构不规则、或非标准编号格式的文档。

工作流程：
1. 提取文档前 50-100 段（或全部段落，如果较短）
2. 让 LLM 一次性分析整个文档结构，输出每段的层级标签
3. 应用格式化规则

优势：
- 理解语义（"核心竞争力"是标题，"公司成立于..."是正文）
- 识别不规则编号（"Chapter 1"、"Part A"、自定义编号）
- 适应多语言/多行业文档
- 可以从用户示例中学习
"""

import json
import sys
from typing import List, Dict, Optional


def extract_paragraphs_context(doc_paragraphs: List[str], max_chars=8000) -> str:
    """
    提取文档段落的文本上下文，供 LLM 分析。
    限制总字符数避免 token 过多。

    返回格式：
    [0] 第一段文本内容
    [1] 第二段文本内容
    ...
    """
    lines = []
    total_chars = 0
    for i, para in enumerate(doc_paragraphs):
        text = para.strip()
        if not text:
            continue
        line = f"[{i}] {text}"
        if total_chars + len(line) > max_chars:
            lines.append(f"... (后续 {len(doc_paragraphs) - i} 段省略)")
            break
        lines.append(line)
        total_chars += len(line)
    return "\n".join(lines)


CLASSIFICATION_PROMPT = """你是一个文档结构分析专家。请分析以下中文正式文档的段落，判断每个段落的类型和层级。

## 文档段落

{paragraphs}

## 任务

为每个段落分配一个标签：
- `cover` - 封面大标题（通常是第一段，如"招股说明书"、"年度报告"）
- `h1` - 一级标题（章节标题，如"第一章 公司基本情况"、"一、业务概述"）
- `h2` - 二级标题（小节标题，如"（一）主营业务"、"1. 产品介绍"）
- `h3` - 三级标题（更细的分类）
- `h4` - 四级标题（最细粒度）
- `body` - 正文段落
- `empty` - 空段落或占位符

## 判断依据

**标题特征：**
- 简短（通常 < 50 字）
- 总结性、概括性（如"核心竞争力"、"风险因素"）
- 可能有编号前缀（"第X节"、"一、"、"1."），但不一定
- 上下文独立，不是叙述性句子的一部分

**正文特征：**
- 较长（> 50 字）
- 叙述性、描述性（如"公司成立于2020年，主要从事..."）
- 包含完整句子结构

**层级判断：**
- h1：最顶层划分，通常对应文档的主要章节
- h2：h1 的子标题
- h3/h4：更细的分类

## 输出格式

严格按照 JSON 格式输出，每行一个段落：

```json
[
  {{"index": 0, "label": "cover"}},
  {{"index": 1, "label": "h1"}},
  {{"index": 2, "label": "body"}},
  {{"index": 3, "label": "h2"}},
  ...
]
```

**重要：**
- 只输出 JSON，不要有任何额外解释
- index 必须和输入段落的 [N] 编号一致
- 如果不确定层级，优先标为 `body`
- 连续多个同级标题不应该跳级（h1 → h3 是可疑的）
"""


def classify_with_llm(
    paragraphs: List[str],
    llm_call_function,  # 用户提供的 LLM 调用函数
    max_context_chars=8000
) -> Dict[int, str]:
    """
    使用 LLM 批量分类段落。

    Args:
        paragraphs: 文档的所有段落文本列表
        llm_call_function: 调用 LLM 的函数，签名为 f(prompt: str) -> str
        max_context_chars: 送给 LLM 的最大字符数

    Returns:
        {段落索引: 标签} 的字典，如 {0: "cover", 1: "h1", 2: "body", ...}
    """
    context = extract_paragraphs_context(paragraphs, max_context_chars)
    prompt = CLASSIFICATION_PROMPT.format(paragraphs=context)

    response = llm_call_function(prompt)

    # 解析 LLM 返回的 JSON
    try:
        # 尝试提取 JSON（LLM 可能包裹在 ```json ... ``` 中）
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0]
        elif "```" in response:
            response = response.split("```")[1].split("```")[0]

        results = json.loads(response.strip())

        # 转换为 {index: label} 字典
        classification = {}
        for item in results:
            idx = item["index"]
            label = item["label"]
            classification[idx] = label

        return classification

    except (json.JSONDecodeError, KeyError) as e:
        print(f"警告：LLM 返回的 JSON 格式错误: {e}", file=sys.stderr)
        print(f"原始返回内容:\n{response}", file=sys.stderr)
        # 回退：全部标记为 body
        return {i: "body" for i in range(len(paragraphs))}


def hybrid_classify(
    paragraph_text: str,
    para_index: int,
    llm_classification: Optional[Dict[int, str]],
    regex_patterns: Dict[str, str]  # 来自 default_rules.json
) -> Optional[str]:
    """
    混合分类策略：
    1. 优先使用 LLM 的分类结果（如果有）
    2. 回退到正则匹配（向后兼容旧逻辑）
    3. 最后返回 None（正文）

    Args:
        paragraph_text: 段落文本
        para_index: 段落索引
        llm_classification: LLM 的分类结果字典（可能为 None）
        regex_patterns: 正则规则字典 {"h1": "^第.+节", ...}

    Returns:
        标签字符串（"cover"/"h1"/"h2"/"h3"/"h4"）或 None（正文）
    """
    import re

    # 策略 1: LLM 优先
    if llm_classification and para_index in llm_classification:
        label = llm_classification[para_index]
        if label != "body" and label != "empty":
            return label
        return None  # body 或 empty 都视为正文

    # 策略 2: 正则回退
    text = paragraph_text.strip()
    if not text:
        return None

    for level in ["h1", "h2", "h3", "h4"]:
        pattern = regex_patterns.get(level)
        if pattern and re.match(pattern, text):
            return level

    # 策略 3: 正文
    return None


# 示例：如何在 format_docx.py 中集成

def example_integration():
    """
    在 format_docx.py 的 format_document() 函数中的集成示例
    """

    # 1. 提取所有段落文本
    doc = Document("input.docx")
    paragraph_texts = [p.text for p in doc.paragraphs]

    # 2. 调用 LLM 批量分类（可选，如果用户启用了 --use-llm 参数）
    llm_classification = None
    if use_llm_mode:
        def my_llm_call(prompt: str) -> str:
            # 这里调用你的 LLM API
            # 例如：调用 Claude、GPT、或本地模型
            from anthropic import Anthropic
            client = Anthropic(api_key="...")
            message = client.messages.create(
                model="claude-sonnet-4",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text

        llm_classification = classify_with_llm(
            paragraph_texts,
            my_llm_call,
            max_context_chars=8000
        )

    # 3. 应用格式时使用混合分类
    for i, paragraph in enumerate(doc.paragraphs):
        text = paragraph.text

        level = hybrid_classify(
            text,
            i,
            llm_classification,
            rules["heading_levels"]  # 从 default_rules.json 读取的正则
        )

        if level is None:
            apply_body_style(paragraph, rules["body"])
        else:
            cfg = rules["heading_levels"][level]
            apply_heading_style(paragraph, cfg)


if __name__ == "__main__":
    print("这是一个库文件，请在 format_docx.py 中导入使用。")
    print("集成示例请参考 example_integration() 函数。")
