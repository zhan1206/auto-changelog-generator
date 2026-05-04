# Auto Changelog Generator

Automatically generate a standardized CHANGELOG from Git commit history with Conventional Commits support.

## Features

- **Automatic Commit Categorization**: feat / fix / docs / refactor and more
- **Conventional Commits Support**: Recognizes `feat:`, `fix:`, `perf:` and other standard prefixes
- **Multiple Output Formats**: Markdown (default), Text, JSON, HTML
- **Multi-language**: Automatically recognizes Chinese and English commits
- **Zero Dependencies**: Uses only Python standard library

## Supported Commit Types

| Type | Description |
|------|-------------|
| feat | New features |
| fix | Bug fixes |
| perf | Performance improvements |
| refactor | Code refactoring |
| docs | Documentation updates |
| style | Style changes |
| test | Test-related |
| build | Build system |
| ci | CI/CD |
| chore | Maintenance |
| revert | Reverts |

## Usage

```bash
# Generate Markdown CHANGELOG
python scripts/auto_changelog_generator.py . -o CHANGELOG.md

# Generate Text format
python scripts/auto_changelog_generator.py . --format text

# Generate JSON format
python scripts/auto_changelog_generator.py . --format json -o changelog.json

# Generate HTML format
python scripts/auto_changelog_generator.py . --format html -o changelog.html

# Only get commits since a date
python scripts/auto_changelog_generator.py . --since 2024-01-01
```

## Recommended Commit Format

```
<type>(<scope>): <subject>

# Examples
feat(auth): add JWT token refresh
fix(api): handle null response from external service
docs: update API documentation
```

## Installation

No installation needed. Requires Python 3.8+.

```bash
git clone https://github.com/zhan1206/auto-changelog-generator.git
cd auto-changelog-generator
python scripts/auto_changelog_generator.py --help
```

## License

MIT License
