#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Changelog Generator - 自动生成规范化的变更日志
基于 Git 提交历史和 conventional commits 规范生成 CHANGELOG
支持 semver 版本管理和多语言
"""

import os
import re
import json
import argparse
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from collections import defaultdict


def find_git():
    """自动查找 git 可执行文件路径"""
    git_exe = shutil.which('git')
    if git_exe:
        return git_exe
    fallback = r"C:\Program Files\Git\cmd\git.exe"
    if os.path.exists(fallback):
        return fallback
    fallback2 = r"C:\Program Files (x86)\Git\cmd\git.exe"
    if os.path.exists(fallback2):
        return fallback2
    return 'git'


# Conventional commit types
COMMIT_TYPES = {
    'feat': ('Features', '新增功能'),
    'fix': ('Bug Fixes', 'Bug 修复'),
    'perf': ('Performance Improvements', '性能优化'),
    'refactor': ('Refactoring', '代码重构'),
    'docs': ('Documentation', '文档更新'),
    'style': ('Styles', '样式调整'),
    'test': ('Tests', '测试相关'),
    'build': ('Build System', '构建系统'),
    'ci': ('CI/CD', '持续集成'),
    'chore': ('Chores', '杂项维护'),
    'revert': ('Reverts', '回滚'),
    'wip': ('Work in Progress', '开发中'),
}

CONVENTIONAL_PATTERN = re.compile(
    r'^(feat|fix|perf|refactor|docs|style|test|build|ci|chore|revert|wip)'
    r'(?:\(([^)]+)\))?\s*:\s*(.+)$'
)


def run_git_log(path, fmt='%H|%s|%an|%ae|%ad|%D', num=500, since=None):
    """运行 git log 获取提交历史"""
    git_exe = find_git()
    cmd = [git_exe, 'log', f'--format={fmt}', f'--max-count={num}']
    if since:
        cmd.extend(['--since', since])
    cmd.extend(['--date=iso'])
    try:
        result = subprocess.run(
            cmd,
            cwd=path,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=30
        )
        return result.stdout.strip()
    except Exception:
        return ''


def get_tag_versions(path):
    """获取所有版本标签"""
    git_exe = find_git()
    result = subprocess.run(
        [git_exe, 'tag', '--sort=-version:refname'],
        cwd=path,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    if result.returncode != 0:
        return []
    return [t.strip() for t in result.stdout.splitlines() if t.strip()]


def parse_commit(commit_line):
    """解析单条提交"""
    if not commit_line or '|' not in commit_line:
        return None

    parts = commit_line.split('|')
    if len(parts) < 4:
        return None

    return {
        'hash': parts[0].strip(),
        'subject': parts[1].strip(),
        'author_name': parts[2].strip(),
        'author_email': parts[3].strip(),
        'date': parts[4].strip() if len(parts) > 4 else '',
        'refs': parts[5].strip() if len(parts) > 5 else '',
    }


def categorize_commit(subject):
    """将提交归类"""
    subject_lower = subject.lower()

    # Conventional commit
    m = CONVENTIONAL_PATTERN.match(subject)
    if m:
        commit_type = m.group(1)
        scope = m.group(2) or ''
        desc = m.group(3).strip()
        return commit_type, scope, desc

    # 自动检测
    for key in ['fix', 'bug', 'patch']:
        if key in subject_lower and ('fix' in subject_lower or 'bug' in subject_lower):
            return 'fix', '', subject
    for key in ['feat', 'feature', 'add', '新增', '新功能']:
        if key in subject_lower:
            return 'feat', '', subject
    for key in ['doc', 'readme', '文档']:
        if key in subject_lower:
            return 'docs', '', subject

    return 'chore', '', subject


def generate_changelog(project_path, options=None):
    """主生成函数"""
    options = options or {}
    project_path = os.path.abspath(project_path)

    git_dir = os.path.join(project_path, '.git')
    if not os.path.exists(git_dir):
        return {'error': f'不是 Git 仓库: {project_path}'}

    since = options.get('since')
    output = run_git_log(project_path, since=since)
    if not output:
        return {'error': '无法获取 Git 提交历史'}

    commits = []
    for line in output.splitlines():
        commit = parse_commit(line)
        if commit:
            commits.append(commit)

    if not commits:
        return {'error': '没有找到提交记录'}

    # 按类型分组
    by_type = defaultdict(list)
    for commit in commits:
        ctype, scope, desc = categorize_commit(commit['subject'])
        entry = {
            'hash': commit['hash'][:8],
            'subject': desc or commit['subject'],
            'author': commit['author_name'],
            'date': commit['date'][:10] if commit['date'] else '',
            'scope': scope,
        }
        by_type[ctype].append(entry)

    return {
        'project_path': project_path,
        'total_commits': len(commits),
        'commits': commits[:10],
        'by_type': dict(by_type),
        'types': list(by_type.keys()),
    }


def format_markdown(result):
    """生成 Markdown 格式的 CHANGELOG"""
    if result.get('error'):
        return f"# CHANGELOG Error\n\n{result['error']}\n"

    lines = [
        "# Changelog",
        "",
        f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        "---",
        "",
    ]

    by_type = result.get('by_type', {})
    type_order = ['feat', 'fix', 'perf', 'refactor', 'docs', 'style',
                  'test', 'build', 'ci', 'chore', 'revert', 'wip']

    for ctype in type_order:
        if ctype not in by_type:
            continue

        type_en, type_cn = COMMIT_TYPES.get(ctype, (ctype, ctype))
        entries = by_type[ctype]

        lines.append(f"## {type_en} ({type_cn})")
        lines.append("")

        for entry in entries:
            scope = f"**({entry['scope']})** " if entry['scope'] else ""
            hash_link = f"[`{entry['hash']}`](#) "
            date = f"({entry['date']}) " if entry['date'] else ""
            lines.append(f"- {hash_link}{scope}{entry['subject']} {date}~{entry['author']}")

        lines.append("")

    lines.append("---")
    lines.append(f"*Total commits: {result['total_commits']}*")

    return '\n'.join(lines)


def format_json(result):
    """JSON 格式输出"""
    output = {k: v for k, v in result.items() if k != 'commits'}
    output['recent_commits'] = result.get('commits', [])
    return json.dumps(output, ensure_ascii=False, indent=2)


def format_text(result):
    """文本格式输出"""
    if result.get('error'):
        return f"错误: {result['error']}"

    lines = [
        "=" * 60,
        "Auto Changelog Generator - CHANGELOG",
        "=" * 60,
        f"项目: {result['project_path']}",
        f"总提交数: {result['total_commits']}",
        "",
    ]

    by_type = result.get('by_type', {})
    type_order = ['feat', 'fix', 'perf', 'refactor', 'docs', 'style',
                  'test', 'build', 'ci', 'chore', 'revert', 'wip']

    for ctype in type_order:
        if ctype not in by_type:
            continue

        type_en, type_cn = COMMIT_TYPES.get(ctype, (ctype, ctype))
        entries = by_type[ctype]

        lines.append(f"{type_en} ({type_cn}) [{len(entries)}]")
        for entry in entries:
            scope = f"({entry['scope']}) " if entry['scope'] else ""
            lines.append(f"  * {entry['hash']} {scope}{entry['subject']}")

        lines.append("")

    return '\n'.join(lines)


def format_html(result):
    """HTML 格式输出"""
    if result.get('error'):
        return f"<h1>Error: {result['error']}</h1>"

    by_type = result.get('by_type', {})
    type_order = ['feat', 'fix', 'perf', 'refactor', 'docs', 'style',
                  'test', 'build', 'ci', 'chore', 'revert', 'wip']

    sections = ''
    for ctype in type_order:
        if ctype not in by_type:
            continue

        type_en, type_cn = COMMIT_TYPES.get(ctype, (ctype, ctype))
        entries = by_type[ctype]
        items = ''
        for entry in entries:
            scope = f'<span class="scope">({entry["scope"]})</span>' if entry['scope'] else ''
            items += f'<li><code>{entry["hash"]}</code> {scope} {entry["subject"]} <span class="date">{entry["date"]}</span></li>'

        sections += f'''
        <section>
            <h3>{type_en} <span class="badge">{type_cn} ({len(entries)})</span></h3>
            <ul>{items}</ul>
        </section>
        '''

    return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Changelog</title>
<style>
body {{ font-family: -apple-system, sans-serif; margin: 40px; background: #f9f9f9; }}
h1 {{ color: #333; }}
section {{ background: white; margin: 20px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
h3 {{ margin-top: 0; border-bottom: 2px solid #eee; padding-bottom: 8px; }}
.badge {{ font-size: 12px; background: #e9ecef; padding: 2px 8px; border-radius: 10px; color: #666; }}
.scope {{ color: #6f42c1; font-weight: bold; }}
code {{ background: #f1f3f5; padding: 2px 6px; border-radius: 3px; font-size: 13px; }}
.date {{ color: #999; font-size: 12px; }}
ul {{ list-style: none; padding: 0; }}
li {{ padding: 6px 0; border-bottom: 1px solid #f8f9fa; }}
</style></head><body>
<h1>Changelog</h1>
<p>Project: {result['project_path']} | Total commits: {result['total_commits']}</p>
{sections}
</body></html>'''


def main():
    parser = argparse.ArgumentParser(
        description='Auto Changelog Generator - 基于 Git 提交历史生成 CHANGELOG'
    )
    parser.add_argument('project_path', nargs='?', default='.',
                        help='Git 仓库路径 (默认当前目录)')
    parser.add_argument('--format', choices=['text', 'json', 'markdown', 'html'],
                        default='markdown', help='输出格式 (默认 markdown)')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--since', help='只获取指定日期之后的提交 (如: 2024-01-01)')
    args = parser.parse_args()

    result = generate_changelog(args.project_path, {'since': args.since})

    formatters = {
        'text': format_text,
        'json': format_json,
        'markdown': format_markdown,
        'html': format_html,
    }
    output = formatters[args.format](result)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f'Changelog 已保存到: {args.output}')
    else:
        print(output)


if __name__ == '__main__':
    main()
