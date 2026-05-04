# Auto Changelog Generator

Automatically generate changelogs from git history, supporting conventional commits format.

## Features

- **Conventional Commits parsing**: Auto-recognize feat:, fix:, docs:, etc.
- **Group by type**: Categorize commits into Features, Bug Fixes, Documentation, etc.
- **Tag range support**: Generate changelog for specific version ranges
- **Multiple output formats**: Text, JSON, Markdown, HTML
- **Zero dependencies**: Uses only Python standard library

## Supported Commit Types

| Type | Description |
|------|------------|
| feat | New features |
| fix | Bug fixes |
| docs | Documentation updates |
| style | Code style changes |
| refactor | Code refactoring |
| perf | Performance improvements |
| test | Test-related changes |
| build | Build system changes |
| ci | CI configuration |
| chore | Maintenance |
| revert | Reverted commits |
| breaking | Breaking changes |

## Usage

```bash
# Analyze current git repository
python scripts/auto_changelog_generator.py .

# Specify project path
python scripts/auto_changelog_generator.py /path/to/repo

# Output Markdown (default)
python scripts/auto_changelog_generator.py . --format markdown -o CHANGELOG.md

# Output HTML
python scripts/auto_changelog_generator.py . --format html -o changelog.html

# Specify version range
python scripts/auto_changelog_generator.py . --from-tag v1.0.0 --to-tag v1.1.0
```

## Example Output

```markdown
# Changelog

**Project**: /path/to/project
**Total Commits**: 42

---

## Features

- `a1b2c3d` Add user authentication
- `e4f5g6h` Implement dark mode

## Bug Fixes

- `i7j8k9l` Fix login timeout issue
```

## Installation

No installation needed. Requires Python 3.8+ and a git repository.

```bash
git clone https://github.com/zhan1206/auto-changelog-generator.git
cd auto-changelog-generator
python scripts/auto_changelog_generator.py --help
```

## License

MIT License
