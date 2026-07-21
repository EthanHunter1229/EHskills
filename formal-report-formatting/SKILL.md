---
name: formal-report-formatting
description: Reformats formal Chinese Word documents (正式报告、公文、招股说明书、上市材料等) to a rigorous, publication-ready layout — page setup, multi-level heading fonts/sizes, body paragraph justification/indentation/line spacing, three-line table styling, and page numbering. Use this skill whenever the user asks to "排版", "调整格式", "统一字体字号", "调整行间距/字间距", or mentions a Word/.docx report, 招股说明书, 科创板, IPO材料, or any formal Chinese business/legal/internal document that needs professional, consistent formatting. Also trigger when the user uploads a messy .docx and asks to make it "看起来专业" or match a standard template, even if they don't use the word "排版" explicitly.
---

# 正式报告排版助手

## 这个 skill 解决什么问题

中文招股说明书、上市材料、内部报告等正式文档对字体、字号、行距、表格样式有非常严格且细致的规范，手动逐段调整既费时又容易出错（尤其是表格里数字对齐、跨页表头这类细节）。这个 skill 把规则封装成一份可复用的配置文件 + 一个自动化脚本，让 Claude 能可靠地、一次性地把整份文档调整到位，而不是凭感觉一段段改。

默认规则来自科创板招股说明书的通行排版惯例（见 `references/formatting_rules.md` 和 `assets/default_rules.json`），但用户可以随时提供自己的规则（字体、字号、行距数值等），Claude 应该据此更新 `assets/default_rules.json` 里对应的字段，而不是重写整个脚本。

## 工作流程

1. **确认输入文件**：用户应提供一份 `.docx` 文件。如果用户只给了文本内容而没有现成文档，先用该内容生成一份基础 `.docx`（可以用 python-docx 或参考 docx skill），再套用本 skill 的排版规则。

2. **确认规则**：默认按 `assets/default_rules.json` 执行。如果用户提到任何具体的字体/字号/行距/页边距要求，在运行脚本前先编辑这个 JSON 文件里对应字段，不要在脚本里硬编码新数值。

3. **选择标题识别模式**：

   ### 模式 A：正则匹配（默认，快速）

   适用于：标准编号格式的招股说明书、IPO 材料、规范的企业报告。

   ```bash
   python3 scripts/format_docx.py <输入.docx> <输出.docx> --rules assets/default_rules.json
   ```

   **工作原理：**
   - 按编号规则匹配：`第X节`、`一、二、三`、`（一）（二）`、`1.2.3`
   - 回退到 Word 内置样式：`Heading 1/2/3/4`、`Title`
   - **优点**：速度快（秒级），规则明确，适合标准文档
   - **缺点**：只能识别固定格式，无法理解语义

   ### 模式 B：LLM 智能识别（推荐用于非标准文档）

   适用于：结构不规则、自定义编号、多语言、跨行业文档。

   ```bash
   python3 scripts/format_docx.py <输入.docx> <输出.docx> --use-llm --rules assets/default_rules.json
   ```

   **工作原理：**
   - 提取全文段落送给大模型（Claude/GPT）
   - LLM 根据语义理解判断每段的类型和层级
   - 识别特征：简短总结性（标题）vs 长叙述性（正文）
   - **优点**：理解语义，适应任意格式，准确率更高
   - **缺点**：需要 API 调用，速度较慢（10-30秒），有 token 成本

   **LLM 判断示例：**
   ```
   "核心竞争力分析" → h2（简短、总结性）
   "公司成立于2020年，主要从事..." → body（叙述性、完整句子）
   "Chapter 3: Market Analysis" → h1（英文标题，LLM 能识别）
   "2021年营收情况" → h2（虽然以年份开头，但语义是标题）
   "2021年公司实现营收100亿元..." → body（叙述性，虽然有年份）
   ```

   ### 混合模式（最佳实践）

   脚本会自动混合使用：
   1. **优先 LLM 判断**（如果启用 `--use-llm`）
   2. **回退正则匹配**（LLM 失败或未启用时）
   3. **兜底 Word 样式**（前两者都失败时）

   这样既保证了准确性，又有向后兼容的保底逻辑。

4. **脚本执行内容**：

   无论哪种模式，脚本都会：
   - 设置 A4 页面与页边距
   - 识别标题层级（按上述模式）
   - 对无编号标题自动添加编号（`一、`、`（一）`、`1.`），每次遇到上级标题时重新计数
   - 项目符号/编号列表保留原有格式，不误判为标题
   - 对正文段落应用两端对齐、首行缩进 2 字符、固定行距 20pt
   - 对表格应用三线表边框、五号字体、数字右对齐/文本左对齐
   - 在页脚插入页码（`第 X 页 共 Y 页` 或 `- N -`）
   - 强制所有文字改为纯黑色（避免 Word 模板主题色干扰）

4. **检查结果**：脚本运行完不代表万事大吉，务必打开输出文件核对以下几点，发现问题手动修正对应段落：
   - 各级标题是否分类正确、编号是否连续合理（尤其留意结构特别不规则、层级又深又乱的文档）
   - 表格是否清晰无粘连，数字对齐是否整齐
   - 页码是否从正确的位置开始连续编号（封面、目录、释义等通常需要单独编排，脚本不会自动跳过这些页，需要人工确认或在调用前告知）

5. **交付**：把最终 `.docx` 保存到用户可访问的输出目录，并简要说明做了哪些调整、以及哪些地方建议人工复核。

## 何时不要用这个脚本硬套

- 如果文档结构极其不规则（比如标题没有任何数字/序号规律，也没有套用 Word 标题样式），先如实告诉用户自动识别可能不准，建议提供标题清单或按章节分别处理，而不是硬跑脚本产出一份看似正确实则标题分类混乱的文档。
- 如果用户要的是英文文档或完全不同的行业规范（比如学术论文、合同），先确认是否仍适用这套中文正式报告规则，必要时调整 `assets/default_rules.json` 甚至标题识别正则（在 `scripts/format_docx.py` 的 `classify_heading` 函数里）。

## 依赖与环境

### 安装依赖
```bash
pip install python-docx
```

或使用 requirements.txt：
```bash
pip install -r requirements.txt
```

### 系统要求
- Python 3.7+
- 字体要求：
  - Windows：宋体、黑体、楷体_GB2312（系统自带）
  - macOS：需安装宋体、黑体、楷体（或 STKaiti）
  - Linux：`sudo apt install fonts-wqy-microhei fonts-wqy-zenhei`

## 已知限制

1. **封面页码**：脚本从第一页开始连续编号。如需单独编排封面/目录页码（罗马数字），需在 Word 中手动分节并设置不同页码格式。
2. **字体颜色**：所有文字会统一改为纯黑色，无法保留原文档中的彩色标注（如红色警告）。
3. **表格跨页**：仅首行设为跨页重复表头，不支持多行表头重复。
4. **复杂表格**：嵌套表格或合并单元格过多时，边框样式可能异常，需人工检查。
5. **标题误判**：以"2021年"、"100.5万元"等开头的正文段落，极少数情况下可能被误判为标题，需人工复核。

## 参考文件

- `references/formatting_rules.md` —— 完整的排版规范说明（页面、字体字号层级、段落、表格、页码），人类可读版本，方便和用户对齐规则细节。
- `assets/default_rules.json` —— 脚本实际读取的机器可读规则配置，字体名、字号（磅值）、行距、边距、颜色等都在这里，改规则先改这个文件。
- `scripts/format_docx.py` —— 排版执行脚本，核心逻辑是 `classify_heading()`（标题层级识别，含 Word 样式回退）、`make_heading_number()`（自动编号）和一系列 `apply_*_style()` 函数。
- `requirements.txt` —— Python 依赖列表。
