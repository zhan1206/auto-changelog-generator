# Auto Changelog Generator

自动变更日志生成器 - 基于 Git 提交历史自动生成规范化的 CHANGELOG

## 功能特性

- **自动分类提交**：feat / fix / docs / refactor 等多类型自动识别
- **Conventional Commits 支持**：识别 `feat:`, `fix:`, `perf:` 等规范前缀
- **多格式输出**：Markdown（默认）、Text、JSON、HTML
- **多语言支持**：自动识别中英文提交
- **零依赖**：仅使用 Python 标准库

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

## Conventional Commits 建议格式

```
<type>(<scope>): <subject>

# 示例
feat(auth): add JWT token refresh
fix(api): handle null response from external service
docs: update API documentation
```

## 安装

无需安装任何依赖，直接使用 Python 3.8+ 运行。

```bash
git clone https://github.com/zhan1206/auto-changelog-generator.git
cd auto-changelog-generator
python scripts/auto_changelog_generator.py --help
```

## 授权

MIT License
