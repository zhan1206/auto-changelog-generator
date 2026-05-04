---
name: "auto-changelog-generator"
description: "Auto Changelog Generator - 从 git 历史自动生成 changelog，按提交类型分类。适用于发布管理、版本记录、自动化发布流程。触发词：changelog、变更日志、git history、release notes、版本记录。"
agent_created: true
---

# Auto Changelog Generator

从 git 历史自动生成规范的 changelog，支持 conventional commits 格式。

## 功能特性

- **Conventional Commits 解析**：自动识别 feat:、fix:、docs: 等提交类型
- **按类型分组**：将提交按新增功能、Bug 修复、文档更新等分类
- **支持标签范围**：可指定 from-tag 和 to-tag 生成特定版本的 changelog
- **多格式输出**：Text、JSON、Markdown、HTML
- **零依赖**：仅使用 Python 标准库

## 支持的提交类型

| 类型 | 说明 |
|------|------|
| feat | 新增功能 |
| fix | Bug 修复 |
| docs | 文档更新 |
| style | 代码格式 |
| refactor | 代码重构 |
| perf | 性能优化 |
| test | 测试相关 |
| build | 构建相关 |
| ci | CI 配置 |
| chore | 维护更新 |
| revert | 回滚提交 |
| breaking | 破坏性变更 |

## 使用方法

```bash
# 分析当前 git 仓库
python scripts/auto_changelog_generator.py .

# 指定项目路径
python scripts/auto_changelog_generator.py /path/to/repo

# 输出 Markdown（默认）
python scripts/auto_changelog_generator.py . --format markdown -o CHANGELOG.md

# 输出 HTML
python scripts/auto_changelog_generator.py . --format html -o changelog.html

# 指定版本范围
python scripts/auto_changelog_generator.py . --from-tag v1.0.0 --to-tag v1.1.0
```

## 输出示例

```markdown
# Changelog

**项目**: /path/to/project
**总提交数**: 42

---

## Features (新增功能)

- `a1b2c3d` Add user authentication
- `e4f5g6h` Implement dark mode (`feat`)

## Bug Fixes (Bug 修复)

- `i7j8k9l` Fix login timeout issue
```

## 安装

无需安装，直接使用 Python 3.8+ 运行（必须是 git 仓库）。

```bash
git clone https://github.com/zhan1206/auto-changelog-generator.git
cd auto-changelog-generator
python scripts/auto_changelog_generator.py --help
```

## 授权

MIT License
