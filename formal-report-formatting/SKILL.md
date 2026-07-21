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

3. **运行排版脚本**：

   ```bash
   python3 scripts/format_docx.py <输入.docx> <输出.docx> --rules assets/default_rules.json
   ```

   脚本会：
   - 设置 A4 页面与页边距
   - 逐段识别标题层级：优先按编号规则匹配（封面标题 / 第X节 / 一、二、三 / （一）（二） / 1.2.3），匹配不到时回退到该段落自带的 Word 标题样式（Heading 1/2/3/4、Title），所以即使文档用的是普通报告的内置标题样式而不是招股书编号惯例，也能正确分级
   - 对识别到但自身没有编号的标题（比如只套了 Heading 3 样式、文字里没有"（一）"这类前缀的小标题），按该级别的编号惯例自动加上编号，并且每次遇到上一级标题时重新从"一/（一）/1"计数，避免出现两个不同小节都叫"发现的问题"却看不出层级归属的问题
   - 项目符号/编号列表里的段落一律当正文处理，即使列表文字本身以数字开头（比如"01.碎片化信息文件夹…"）也不会被误判成标题；列表保留自己的缩进和列表符号，不强行两端对齐或加首行缩进
   - 对正文段落应用两端对齐、首行缩进 2 字符、指定行距与段前段后间距
   - 对表格应用三线表边框、缩小一号的字体、数字靠右/文本靠左或居中对齐，并将首行设为跨页重复标题行
   - 在页脚插入页码（支持"第 X 页 共 Y 页"或"- N -"两种格式）
   - 强制把标题、正文、表格、页脚的字体颜色改成规则里指定的颜色（默认纯黑）。这一步很重要：很多 Word 模板的内置标题样式自带主题色（比如蓝色），只改字体字号不改颜色的话，标题看起来会跟正文风格不统一

4. **检查结果**：脚本运行完不代表万事大吉，务必打开输出文件核对以下几点，发现问题手动修正对应段落：
   - 各级标题是否分类正确、编号是否连续合理（尤其留意结构特别不规则、层级又深又乱的文档）
   - 表格是否清晰无粘连，数字对齐是否整齐
   - 页码是否从正确的位置开始连续编号（封面、目录、释义等通常需要单独编排，脚本不会自动跳过这些页，需要人工确认或在调用前告知）

5. **交付**：把最终 `.docx` 保存到用户可访问的输出目录，并简要说明做了哪些调整、以及哪些地方建议人工复核。

## 何时不要用这个脚本硬套

- 如果文档结构极其不规则（比如标题没有任何数字/序号规律，也没有套用 Word 标题样式），先如实告诉用户自动识别可能不准，建议提供标题清单或按章节分别处理，而不是硬跑脚本产出一份看似正确实则标题分类混乱的文档。
- 如果用户要的是英文文档或完全不同的行业规范（比如学术论文、合同），先确认是否仍适用这套中文正式报告规则，必要时调整 `assets/default_rules.json` 甚至标题识别正则（在 `scripts/format_docx.py` 的 `classify_heading` 函数里）。

## 参考文件

- `references/formatting_rules.md` —— 完整的排版规范说明（页面、字体字号层级、段落、表格、页码），人类可读版本，方便和用户对齐规则细节。
- `assets/default_rules.json` —— 脚本实际读取的机器可读规则配置，字体名、字号（磅值）、行距、边距、颜色等都在这里，改规则先改这个文件。
- `scripts/format_docx.py` —— 排版执行脚本，核心逻辑是 `classify_heading()`（标题层级识别，含 Word 样式回退）、`make_heading_number()`（自动编号）和一系列 `apply_*_style()` 函数。
