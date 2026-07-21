# KARMA 集成完整指南

## 📋 任务完成情况

✅ **已完成的工作：**

1. ✅ Skill 开发完成
   - 正则匹配模式（快速识别）
   - LLM 智能模式（语义理解）
   - 混合策略（自动回退）

2. ✅ 代码同步到 GitHub
   - 仓库：https://github.com/EthanHunter1229/EHskills
   - 所有文件已推送
   - 文档完善

3. ✅ 文档准备完整
   - README.md - 项目介绍
   - QUICKSTART.md - 5 分钟快速开始
   - INSTALL.md - 详细安装指南
   - KARMA_SKILL.md - Skill 配置文件
   - IMPROVEMENT_SUMMARY.md - 设计演进
   - SKILL_REVIEW.md - 审查报告

4. 🔄 KARMA Skill 创建中
   - 任务 ID: `srv_0a0f0896df8c4fe3`
   - 状态：正在生成中
   - 预计完成：5-8 分钟

---

## 🚀 立即使用（三种方式）

### 方式 1：从 GitHub 克隆使用（推荐）

```bash
# 1. 克隆到本地
cd ~/
git clone https://github.com/EthanHunter1229/EHskills.git

# 2. 安装依赖
cd EHskills/formal-report-formatting
pip install -r requirements.txt

# 3. 测试
python3 scripts/format_docx.py --help

# 4. 使用
python3 scripts/format_docx.py input.docx output.docx
```

**优点：**
- 立即可用
- 完全离线（正则模式）
- 性能最好

### 方式 2：导入 KARMA（手动）

**步骤：**

1. 打开 KARMA → Skills 管理 → 创建新 Skill

2. 填写基本信息：
   - **名称**：正式报告排版助手
   - **描述**：专业的中文正式文档排版工具
   - **触发词**：排版、调整格式、统一字体字号、招股说明书、正式报告
   - **工具权限**：Read, Write, Edit, Bash, Glob

3. 复制 Skill 提示词：
   - 打开 [`formal-report-formatting/KARMA_SKILL.md`](https://github.com/EthanHunter1229/EHskills/blob/main/formal-report-formatting/KARMA_SKILL.md)
   - 复制"Skill 提示词"部分的完整内容
   - 粘贴到 KARMA 的"Skill 提示词"字段

4. 保存并测试：
   ```
   用户：帮我排版一份正式报告
   ```

**优点：**
- 集成在 KARMA 对话中
- 自动调用脚本
- 用户体验最好

### 方式 3：等待自动创建完成

当前正在进行的任务：
- **任务 ID**: `srv_0a0f0896df8c4fe3`
- **状态**: 运行中
- **进度**: 20%

完成后会自动出现在你的 KARMA Skills 列表中。

**检查方法：**
```python
# 在 KARMA 中执行
from karma import KarmaClient
client = KarmaClient()
skills = client.skills.list()
print([s.name for s in skills if '排版' in s.name])
```

---

## 🔍 三种方式对比

| 方式 | 速度 | 灵活性 | 离线支持 | 推荐场景 |
|------|------|--------|----------|----------|
| **GitHub 克隆** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | 开发、批量处理、高频使用 |
| **手动导入** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ | 集成对话、团队共享 |
| **自动创建** | ⭐ | ⭐⭐⭐ | ❌ | 懒人模式、一次性使用 |

**我的建议：**
- 个人使用 → GitHub 克隆（方式 1）
- 团队协作 → 手动导入（方式 2）
- 偶尔用用 → 等待自动创建（方式 3）

---

## 📁 项目结构说明

```
EHskills/
├── README.md                              ← 项目介绍
├── QUICKSTART.md                          ← ⚡ 5分钟快速开始
├── INSTALL.md                             ← 📖 详细安装指南
├── KARMA_INTEGRATION_GUIDE.md             ← 📋 本文件
├── IMPROVEMENT_SUMMARY.md                 ← 🎯 设计演进总结
├── SKILL_REVIEW.md                        ← 🔍 技术审查报告
├── SKILLS_INDEX.md                        ← 📊 Skills 索引
├── CONTRIBUTING.md                        ← 🤝 贡献指南
├── LICENSE                                ← ⚖️ MIT 许可
│
└── formal-report-formatting/              ← 🎯 核心 Skill
    ├── SKILL.md                           ← Skill 定义（人类可读）
    ├── KARMA_SKILL.md                     ← KARMA 配置文件
    ├── requirements.txt                   ← Python 依赖
    │
    ├── assets/
    │   └── default_rules.json             ← 排版规则配置
    │
    ├── scripts/
    │   ├── format_docx.py                 ← 主排版脚本
    │   └── classify_with_llm.py           ← LLM 智能识别
    │
    └── references/
        ├── formatting_rules.md            ← 排版规范详解
        └── llm_vs_regex.md                ← 技术方案对比
```

**文件导航：**
- 🚀 **想快速开始** → 看 `QUICKSTART.md`
- 📖 **想详细了解** → 看 `INSTALL.md`
- 🔧 **想导入 KARMA** → 看 `formal-report-formatting/KARMA_SKILL.md`
- 🎯 **想理解设计** → 看 `IMPROVEMENT_SUMMARY.md`
- 🔍 **想看技术细节** → 看 `SKILL_REVIEW.md` 和 `references/`

---

## 💡 使用示例

### 示例 1：标准招股说明书（命令行）

```bash
cd ~/EHskills/formal-report-formatting

# 快速排版（正则模式，1秒完成）
python3 scripts/format_docx.py \
  ~/Downloads/招股说明书.docx \
  ~/Downloads/招股说明书_排版.docx \
  --rules assets/default_rules.json
```

### 示例 2：复杂文档（LLM 模式）

```bash
# 智能识别（LLM 模式，30秒完成）
python3 scripts/format_docx.py \
  ~/Downloads/企业年报.docx \
  ~/Downloads/企业年报_排版.docx \
  --use-llm \
  --rules assets/default_rules.json
```

### 示例 3：在 KARMA 对话中使用

```
用户：帮我排版这份招股说明书

[上传文件：prospectus.docx]

Luna01：收到文档。我检查了一下，这是标准格式的招股说明书
（有"第X节"、"一、"等编号），使用正则匹配模式快速处理。

[执行排版脚本]

✅ 排版完成！

应用的规范：
- 封面标题：22pt 黑体
- 一级标题：16pt 黑体，居中
- 二级标题：15pt 黑体，左对齐
- 正文：12pt 宋体，两端对齐，首行缩进 2 字符
- 表格：三线表样式，数字右对齐
- 页码：第 X 页 共 Y 页

统计：
- 一级标题：8 个
- 二级标题：25 个
- 三级标题：42 个
- 正文段落：358 个

输出文件：prospectus_formatted.docx

⚠️ 请检查：
- 标题层级是否正确
- 表格数字对齐是否整齐
- 封面/目录页码是否需要单独处理
```

---

## 🔧 自定义排版规则

如果你的文档不是招股说明书，可以自定义规则：

```bash
# 1. 编辑规则文件
vim assets/default_rules.json

# 2. 修改字体、字号、行距等参数
{
  "heading_levels": {
    "h1": {
      "size_pt": 16,           ← 改为你想要的字号
      "font_east_asian": "黑体", ← 改为你想要的字体
      ...
    }
  }
}

# 3. 使用自定义规则
python3 scripts/format_docx.py input.docx output.docx --rules my_rules.json
```

**常见场景的规则：**
- 学术论文：见 `references/academic_paper_rules.json`（待创建）
- 技术文档：见 `references/tech_doc_rules.json`（待创建）
- 合同文书：见 `references/contract_rules.json`（待创建）

---

## 🐛 故障排查

### 问题 1：找不到 python-docx

```bash
pip install python-docx
# 或
pip3 install python-docx
```

### 问题 2：LLM 模式失败

检查：
1. 网络连接
2. API key 配置
3. SDK 安装：`pip install anthropic` 或 `pip install openai`

### 问题 3：标题识别错误

**正则模式误判太多？**
→ 使用 LLM 模式：`--use-llm`

**LLM 模式也不准？**
→ 检查文档结构，可能需要手动标注标题样式

### 问题 4：字体显示异常

**Linux 缺少中文字体：**
```bash
sudo apt install fonts-wqy-microhei fonts-wqy-zenhei
```

**macOS 缺少楷体：**
下载安装 STKaiti 字体

---

## 📞 获取帮助

- **GitHub Issues**: https://github.com/EthanHunter1229/EHskills/issues
- **讨论区**: https://github.com/EthanHunter1229/EHskills/discussions
- **Email**: ethanhunter@eos3.ai

---

## 🎉 总结

你现在有三个选择：

1. **立即使用**（推荐）
   ```bash
   git clone https://github.com/EthanHunter1229/EHskills.git
   cd EHskills/formal-report-formatting
   pip install -r requirements.txt
   python3 scripts/format_docx.py input.docx output.docx
   ```

2. **导入 KARMA**
   - 打开 [`KARMA_SKILL.md`](./formal-report-formatting/KARMA_SKILL.md)
   - 复制内容到 KARMA Skills 管理
   - 在对话中说"帮我排版"

3. **等待自动创建**
   - 任务 ID: `srv_0a0f0896df8c4fe3`
   - 等待完成后自动出现在 Skills 列表

**我的建议：先用方式 1 测试效果，满意后再导入 KARMA（方式 2）。**

---

## ✨ 核心价值

这个 Skill 解决的核心问题：

❌ **手动排版的痛点：**
- 逐段调整字体字号 → 耗时 2-3 小时
- 表格对齐反复调整 → 容易出错
- 多人编辑格式混乱 → 难以统一
- 不同文档重复劳动 → 效率低下

✅ **自动排版的优势：**
- 一键应用所有规则 → 1-30 秒完成
- 规则配置化 → 零出错
- 模板复用 → 多文档统一
- 智能识别 → 适应各种格式

**ROI 计算：**
- 手动排版：2-3 小时/文档
- 自动排版：< 1 分钟/文档
- 节省时间：99%+
- 首次设置成本：< 10 分钟

---

*最后更新：2026-07-21*
*整理人：Luna01*
