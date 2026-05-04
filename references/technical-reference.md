# Auto Changelog Generator - Technical Reference

## Conventional Commits Format

The tool follows the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Type Reference

| Type | Description | Example |
|------|-------------|---------|
| feat | New feature | `feat: add user login` |
| fix | Bug fix | `fix(auth): resolve token expiry` |
| docs | Documentation | `docs: update README` |
| style | Formatting | `style: format code` |
| refactor | Code restructure | `refactor(api): simplify logic` |
| perf | Performance | `perf(db): add index` |
| test | Tests | `test: add unit tests` |
| build | Build system | `build: upgrade webpack` |
| ci | CI/CD | `ci: add GitHub Actions` |
| chore | Maintenance | `chore: update deps` |
| revert | Revert commit | `revert: undo feat-x` |

### Breaking Changes

Breaking changes can be indicated by `!` after type or `BREAKING CHANGE:` in footer:

```
feat!: remove deprecated API
fix!: fix critical security issue
```

## Git Integration

The tool runs `git log` commands internally:

```bash
git log --date=iso --format=%H|%ae|%an|%ad|%s
```

Output format: `SHA|AuthorEmail|AuthorName|Date|Subject`

## Architecture

```
auto_changelog_generator.py
  |-- run_git_log()         # Execute git log
  |-- parse_commit()        # Parse conventional commit
  |-- analyze_git_history() # Main analysis logic
  |-- format_text()         # Text output
  |-- format_json()         # JSON output
  |-- format_markdown()     # Markdown output
  |-- format_html()         # HTML output
  |-- main()                # CLI entry point
```

## Regex Patterns

### Conventional Commit Pattern
```python
r'^(\w+)(?:\(([^)]+)\))?:\s*(.+)'
```

### Match Groups
- Group 1: Commit type (feat, fix, docs, etc.)
- Group 2: Optional scope (in parentheses)
- Group 3: Commit subject/description

## CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `project_path` | Path to git repository | `.` |
| `--format` | Output format | `markdown` |
| `--output`, `-o` | Output file path | stdout |
| `--from-tag` | Start tag for range | none |
| `--to-tag` | End tag for range | none |
