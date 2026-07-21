# EHskills

> Ethan Hunter 的 Karma Skills 精选收藏库

这个仓库收集了我在使用 Karma AI 过程中创建和优化的各种实用技能(skills)。每个 skill 都经过实战检验,开箱即用。

[![Skills](https://img.shields.io/badge/skills-1-blue)](https://github.com/EthanHunter1229/EHskills)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 快速安装

```bash
git clone https://github.com/EthanHunter1229/EHskills.git
cd EHskills/formal-report-formatting
pip install -r requirements.txt
```

导入 KARMA: 查看 QUICKSTART.md | INSTALL.md

## 技能列表

### 文档处理

#### formal-report-formatting
正式报告格式化工具 - 自动格式化 Word 文档,应用专业报告的排版规范。

核心特性:
- 智能标题识别 - 支持正则匹配 + LLM 语义理解双模式
- 标题层级格式化(五级层级,自动编号)
- 段落间距统一(两端对齐、首行缩进)
- 三线表样式(数字右对齐、跨页表头)
- 字体颜色强制(纯黑色,去除模板主题色)
- 页码生成(第 X 页共 Y 页)

适用场景: 招股说明书、企业年报、技术文档、项目方案、内部报告

推荐用法:
- 标准格式文档 - 正则模式(快速)
- 不规则/多语言文档 - LLM 模式(智能)

## 快速开始

### 1. 在 Karma 中使用

```bash
# 克隆仓库
git clone https://github.com/EthanHunter1229/EHskills.git

# 进入 skill 目录查看使用说明
cd EHskills/formal-report-formatting
cat SKILL.md
```

### 2. 目录结构

每个技能目录包含:
```
skill-name/
├── SKILL.md              # 技能描述和触发词
├── scripts/              # 执行脚本
│   └── *.py
├── references/           # 参考文档
│   └── *.md
└── assets/              # 配置和资源
    └── *.json
```

### 3. 依赖安装

大多数 skills 需要 Python 3.8+,具体依赖查看各 skill 的 SKILL.md。

## 分类索引

- 文档处理 (1) - Word/PDF 格式化、转换、生成
- 数据分析 (即将推出) - 表格处理、数据可视化
- 自动化工具 (即将推出) - 批量操作、定时任务
- AI 增强 (即将推出) - 智能分析、内容生成

## 贡献

欢迎提交你的优质 skills!

1. Fork 本仓库
2. 创建新的 skill 目录
3. 按照贡献指南组织文件
4. 提交 Pull Request

## 相关资源

- Karma AI 官网: https://karma.eos3.ai
- EOS3 平台: https://eos3.ai
- Skill 开发文档: https://docs.karma.eos3.ai

## 许可

MIT License - 详见 LICENSE 文件

## 联系方式

- GitHub: @EthanHunter1229
- Email: ethanhunter@eos3.ai

如果觉得有用,欢迎 Star!
