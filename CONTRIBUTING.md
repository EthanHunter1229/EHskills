# 贡献指南

感谢你对 EHskills 项目的关注！

## 如何贡献

### 1. 提交新的 Skill

如果你有优质的 Karma Skill 想要分享：

1. Fork 本仓库
2. 在根目录创建新的 skill 目录（使用 kebab-case 命名）
3. 按照标准结构组织文件
4. 提交 Pull Request

### 2. Skill 目录结构

每个 skill 应该包含以下文件：

```
skill-name/
├── SKILL.md              # 技能描述（必需）
├── scripts/              # 执行脚本
│   └── main.py
├── references/           # 参考文档
│   └── documentation.md
└── assets/              # 配置和资源
    └── config.json
```

### 3. SKILL.md 模板

```markdown
# Skill 名称

简短描述（一句话）

## 触发词
- 关键词1
- 关键词2

## 功能特性
- 功能1
- 功能2

## 使用示例
具体的使用场景和示例

## 依赖
列出所需的 Python 包或其他依赖

## 配置
如何配置参数

## 作者
[@你的GitHub用户名](https://github.com/yourusername)
```

### 4. 代码规范

- Python 代码使用 PEP 8 规范
- 添加适当的注释
- 包含错误处理
- 提供清晰的日志输出

### 5. 提交规范

提交信息格式：
```
类型: 简短描述

详细描述（可选）
```

类型：
- `feat`: 新增 skill
- `fix`: 修复 bug
- `docs`: 文档更新
- `refactor`: 代码重构

## 行为准则

- 尊重他人
- 保持代码质量
- 遵守开源协议
- 不包含恶意代码

## 问题反馈

发现问题？请通过 Issues 反馈。
