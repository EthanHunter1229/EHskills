# 快速开始

## 一键安装

```bash
# 克隆仓库
git clone https://github.com/EthanHunter1229/EHskills.git
cd EHskills/formal-report-formatting

# 安装依赖
pip install -r requirements.txt

# 测试
python3 scripts/format_docx.py --help
```

完成!

## 导入 KARMA

### 方法 1:手动导入(3 步)

1. 打开 formal-report-formatting/KARMA_SKILL.md
2. 复制"Skill 提示词"部分的完整内容
3. 在 KARMA Skills 管理界面粘贴创建

### 方法 2:命令行(如果你的 KARMA 支持)

```bash
karma skill create \
  --name "正式报告排版助手" \
  --file formal-report-formatting/KARMA_SKILL.md \
  --triggers "排版,调整格式,招股说明书"
```

## 立即使用

### 命令行

```bash
# 快速排版(正则模式)
python3 scripts/format_docx.py input.docx output.docx

# 智能排版(LLM 模式)
python3 scripts/format_docx.py input.docx output.docx --use-llm
```

### KARMA 对话

```
用户:帮我排版这份招股说明书
```

或上传 Word 文档后:

```
用户:按照正式报告规范排版
```

## 完整文档

- INSTALL.md - 详细安装指南
- README.md - 项目介绍
- KARMA_SKILL.md - Skill 配置

## 核心特性

- 智能识别 - 正则 + LLM 双模式
- 5 级标题 - 自动格式化和编号
- 三线表 - 数字右对齐,跨页表头
- 段落规范 - 两端对齐,首行缩进
- 颜色统一 - 强制纯黑色
- 自动页码 - 第 X 页共 Y 页

## 遇到问题?

```bash
# 检查依赖
pip list | grep docx

# 重新安装
pip install --upgrade python-docx

# 查看日志
python3 scripts/format_docx.py input.docx output.docx --verbose
```

仍有问题? 提交 Issue: https://github.com/EthanHunter1229/EHskills/issues

觉得有用? 给个 Star!

项目地址: https://github.com/EthanHunter1229/EHskills
