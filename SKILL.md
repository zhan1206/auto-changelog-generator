---
name: "auto-changelog-generator"
description: "Auto Changelog Generator - 基于 Git 提交历史自动生成规范化的 CHANGELOG。支持 Conventional Commits 规范、多语言、semver 版本管理。触发词：生成 changelog、自动更新日志、release notes、变更日志、版本历史。"
agent_created: true
---

# Auto Changelog Generator

> 基于 Git 提交历史自动生成规范化的 CHANGELOG

## 功能概述

- **自动分类提交**：feat / fix / docs / refactor 等多类型自动识别
- **Conventional Commits 支持**：识别 `feat:`, `fix:`, `perf:` 等规范前缀
- **多格式输出**：Markdown（默认）、Text、JSON、HTML
- **多语言支持**：自动识别中英文提交
- **零依赖**：仅使用 Python 标准库

## 支持的提交类型

| 类型 | 英文 | 中文 |
|------|------|------|
| feat | Features | 新增功能 |
| fix | Bug Fixes | Bug 修复 |
| perf | Performance | 性能优化 |
| refactor | Refactoring | 代码重构 |
| docs | Documentation | 文档更新 |
| style | Styles | 样式调整 |
| test | Tests | 测试相关 |
| build | Build System | 构建系统 |
| ci | CI/CD | 持续集成 |
| chore | Chores | 杂项维护 |
| revert | Reverts | 回滚 |

## 快速使用

```bash
# 生成 Markdown 格式 CHANGELOG
python scripts/auto_changelog_generator.py . -o CHANGELOG.md

# 生成 Text 格式
python scripts/auto_changelog_generator.py . --format text

# 生成 JSON 格式
python scripts/auto_changelog_generator.py . --format json -o changelog.json

# 生成 HTML 格式
python scripts/auto_changelog_generator.py . --format html -o changelog.html

# 只获取最近 30 天的提交
python scripts/auto_changelog_generator.py . --since 2024-01-01
```

## 输出示例 (Markdown)

```markdown
# Changelog

## Features (新功能) [5]
- `a1b2c3d` add user authentication module
- `e5f6g7h` **(**api**)** add REST API endpoints

## Bug Fixes (Bug 修复) [2]
- `i9j0k1l` fix memory leak in worker pool

## Documentation (文档更新) [3]
- `m2n3o4p` update README with new usage examples
```

## Conventional Commits 建议格式

```
<type>(<scope>): <subject>

# 示例
feat(auth): add JWT token refresh
fix(api): handle null response from external service
docs: update API documentation
```

## 在 WorkBuddy 中使用

直接对 WorkBuddy 说：
- "生成这个项目的 changelog"
- "create a changelog from git history"
- "生成 release notes"

## 安装

无需安装任何依赖，直接使用 Python 3.8+ 运行。

```bash
git clone https://github.com/zhan1206/auto-changelog-generator.git
cd auto-changelog-generator
python scripts/auto_changelog_generator.py --help
```

## 授权

MIT License
