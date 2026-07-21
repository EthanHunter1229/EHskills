# 安装指南

## 从 GitHub 安装到 KARMA

### 方法 1:克隆到本地(推荐)

```bash
# 1. 克隆仓库到 KARMA 工作目录
cd ~/karma-skills  # 或你的 skills 目录
git clone https://github.com/EthanHunter1229/EHskills.git
cd EHskills/formal-report-formatting

# 2. 安装 Python 依赖
pip install -r requirements.txt

# 3. 验证安装
python3 scripts/format_docx.py --help
```

### 方法 2:下载 ZIP 包

1. 访问 https://github.com/EthanHunter1229/EHskills
2. 点击 Code → Download ZIP
3. 解压到你的 skills 目录
4. 进入 formal-report-formatting 目录
5. 运行 pip install -r requirements.txt

## 配置到 KARMA

### 在 KARMA 中创建 Skill

方法 A:使用 KARMA 界面

1. 打开 KARMA → Skills 管理
2. 点击创建新 Skill
3. 填写信息:
   - 名称:正式报告排版助手
   - 描述:专业的中文正式文档排版工具,支持招股说明书、企业年报等正式报告的自动排版
   - 触发词:排版、调整格式、统一字体字号、招股说明书、正式报告
   - 允许的工具:Read, Write, Edit, Bash, Glob
4. 在 Skill 提示词 中粘贴 SKILL.md 的内容

方法 B:使用命令行(KARMA CLI)

```bash
# 进入 skill 目录
cd ~/karma-skills/EHskills/formal-report-formatting

# 创建 skill(如果你的 KARMA 支持 CLI)
karma skill create   --name "正式报告排版助手"   --file SKILL.md   --tools "Read,Write,Edit,Bash,Glob"
```

方法 C:使用 API

```python
# 如果你有 KARMA Python SDK
from karma import KarmaClient

client = KarmaClient(api_key="your-key")

with open("SKILL.md", "r", encoding="utf-8") as f:
    skill_content = f.read()

client.skills.create(
    name="正式报告排版助手",
    content=skill_content,
    trigger_words=["排版", "调整格式", "统一字体字号"],
    allowed_tools=["Read", "Write", "Edit", "Bash", "Glob"]
)
```

## 验证安装

### 测试 1:命令行测试

```bash
# 创建一个测试文档
echo "第一节 测试标题

这是一段正文内容,用于测试排版功能。

一、二级标题

这是二级标题下的内容。" > test.txt

# 转换为 docx(需要先有 docx)
# 然后运行排版
python3 scripts/format_docx.py test.docx output.docx

# 检查输出
ls -lh output.docx
```

### 测试 2:在 KARMA 中测试

在 KARMA 对话中说:

```
请帮我排版一份招股说明书
```

或上传一个 Word 文档后说:

```
按照正式报告规范排版这个文档
```

## 更新 Skill

### 从 GitHub 更新

```bash
cd ~/karma-skills/EHskills
git pull origin main

# 重新安装依赖(如有更新)
cd formal-report-formatting
pip install -r requirements.txt
```

### 在 KARMA 中更新

如果 SKILL.md 有更新,需要在 KARMA 中重新导入:

```bash
# 方法 1:使用 KARMA 界面
# Skills 管理 → 找到"正式报告排版助手" → 编辑 → 更新提示词

# 方法 2:使用命令行
karma skill update formal-report-formatting --file SKILL.md
```

## 目录结构

安装完成后,你的目录应该是这样的:

```
~/karma-skills/EHskills/
├── README.md                              # 项目说明
├── INSTALL.md                             # 本安装指南
├── CONTRIBUTING.md                        # 贡献指南
├── LICENSE                                # MIT 许可
├── SKILL_TEMPLATE.md                      # 新 Skill 模板
├── SKILLS_INDEX.md                        # Skill 索引
└── formal-report-formatting/              # 正式报告排版 Skill
    ├── SKILL.md                           # Skill 定义(核心文件)
    ├── requirements.txt                   # Python 依赖
    ├── assets/
    │   └── default_rules.json             # 排版规则配置
    ├── scripts/
    │   ├── format_docx.py                 # 主排版脚本
    │   └── classify_with_llm.py           # LLM 智能识别
    └── references/
        ├── formatting_rules.md            # 排版规范说明
        └── llm_vs_regex.md                # 技术方案对比
```

## 快速开始示例

### 示例 1:标准招股说明书排版

```bash
# 使用正则模式(快速)
python3 scripts/format_docx.py   input.docx   output.docx   --rules assets/default_rules.json
```

### 示例 2:复杂文档智能排版

```bash
# 使用 LLM 模式(智能)
python3 scripts/format_docx.py   complex_doc.docx   formatted.docx   --use-llm   --rules assets/default_rules.json
```

### 示例 3:在 KARMA 中使用

```
用户:帮我排版这份企业年报,统一字体字号

Luna01:好的,我来帮你排版。请上传 Word 文档。

[用户上传 report.docx]

Luna01:收到文档。我发现这是一份标准格式的企业年报,使用正则匹配模式即可。
开始排版...

[执行 format_docx.py]

Luna01:排版完成\!已应用以下规范:
- 封面标题:22pt 黑体
- 一级标题:16pt 黑体,居中
- 正文:12pt 宋体,两端对齐,首行缩进 2 字符
- 表格:三线表样式,数字右对齐
- 页码:第 X 页共 Y 页

输出文件:formatted_report.docx

请检查以下内容:
- 标题层级是否正确
- 表格数字对齐是否整齐
- 页码是否从正确位置开始
```

## 故障排查

### 问题 1:找不到 python-docx

```bash
# 解决方案
pip install python-docx
# 或
pip3 install python-docx
```

### 问题 2:字体缺失(Linux)

```bash
# 安装中文字体
sudo apt update
sudo apt install fonts-wqy-microhei fonts-wqy-zenhei

# 验证字体
fc-list | grep -i "wqy\|simsun\|simhei"
```

### 问题 3:LLM 模式失败

检查:
1. 是否有网络连接
2. 是否配置了 LLM API key
3. 是否安装了对应的 SDK(anthropic, openai 等)

```bash
# 安装 Anthropic SDK
pip install anthropic

# 或 OpenAI SDK
pip install openai
```

### 问题 4:KARMA 找不到 Skill

确认:
1. SKILL.md 已正确导入
2. 触发词设置正确
3. 工具权限已授予(Read, Write, Edit, Bash, Glob)

## 相关文档

- README.md - 项目介绍
- SKILL.md - Skill 完整定义
- formatting_rules.md - 排版规范详解
- llm_vs_regex.md - LLM vs 正则技术对比
- IMPROVEMENT_SUMMARY.md - 设计演进总结

## 获取帮助

遇到问题?

- GitHub Issues: https://github.com/EthanHunter1229/EHskills/issues
- Email: ethanhunter@eos3.ai
- 讨论区: https://github.com/EthanHunter1229/EHskills/discussions

## 隐私与安全

- 所有处理都在本地完成(除非使用 LLM 模式)
- 文档内容不会上传到任何服务器(除了 LLM API)
- LLM 模式仅发送段落文本(不含敏感信息),用于标题分类

如有隐私顾虑,请使用正则模式(完全离线)。

## 支持项目

觉得有用?欢迎:
- Star 这个项目
- 分享给需要的朋友
- 提交你的改进建议
- 贡献新的 Skill

最后更新: 2026-07-21
