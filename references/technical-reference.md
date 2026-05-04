# Auto Changelog Generator - Technical Reference

## Conventional Commits 规范

提交信息格式：
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型 (type)

| 类型 | 说明 | 是否记入 CHANGELOG |
|------|------|-------------------|
| feat | 新功能 | 是 |
| fix | Bug 修复 | 是 |
| perf | 性能优化 | 是 |
| refactor | 重构 | 是 |
| docs | 文档 | 否（可配置） |
| style | 格式调整 | 否 |
| test | 测试 | 否 |
| build | 构建系统 | 否 |
| ci | CI/CD | 否 |
| chore | 维护 | 否 |
| revert | 回滚 | 是 |

## 版本管理建议

### 语义化版本 (SemVer)

```
主版本.次版本.修订号
MAJOR.MINOR.PATCH

MAJOR: 不兼容的 API 变更
MINOR: 向后兼容的功能新增
PATCH: 向后兼容的 Bug 修复
```

### CHANGELOG 生成建议

1. 每个 release 对应一个版本标签 (tag)
2. 使用 `## [Unreleased]` 标记未发布内容
3. 使用 `### Added/Changed/Deprecated/Removed/Fixed/Security` 子标题
4. 按时间倒序排列（最新的在前面）

## 局限性

- 需要仓库有规范的提交信息
- 自动分类基于关键词匹配，可能不完全准确
- 回滚提交需要包含 "revert:" 前缀才能被识别
- Git 仓库外无法使用

## 扩展方向

- 集成 CI/CD 自动生成 release notes
- 支持多语言本地化的 CHANGELOG
- 生成 GitHub Releases 草稿
- 与项目管理工具（如 Jira）集成
