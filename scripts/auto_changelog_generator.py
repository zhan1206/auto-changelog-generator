#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Changelog Generator - 从 git 历史自动生成 changelog
解析 conventional commits 格式，按类型分组生成清晰的变更日志
"""

import os
import re
import json
import argparse
import subprocess
from datetime import datetime
from collections import defaultdict


# ============================================================
# 1. 从 git 历史提取提交记录
# ============================================================

COMMIT_TYPES = {
    'feat': ('新增功能', 'Features'),
    'fix': ('Bug 修复', 'Bug Fixes'),
    'docs': ('文档更新', 'Documentation'),
    'style': ('代码格式', 'Styles'),
    'refactor': ('代码重构', 'Code Refactoring'),
    'perf': ('性能优化', 'Performance Improvements'),
    'test': ('测试相关', 'Tests'),
    'build': ('构建相关', 'Build System'),
    'ci': ('CI 配置', 'Continuous Integration'),
    'chore': ('维护更新', 'Chores'),
    'revert': ('回滚提交', 'Reverts'),
    'breaking': ('破坏性变更', 'Breaking Changes'),
}


def run_git_log(path, from_tag=None, to_tag=None):
    """运行 git log 获取提交历史"""
    cmd = [
        'git', 'log',
        '--date=iso',
        '--format=%H|%ae|%an|%ad|%s',
    ]
    if from_tag:
        cmd.append(f'{from_tag}..HEAD')
    elif to_tag:
        cmd.append(f'HEAD..{to_tag}')
    else:
        cmd.append('--all')

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
        if result.returncode != 0:
            return []
        return result.stdout.strip().split('\n')
    except Exception:
        return []


def parse_commit(line):
    """解析单条提交记录"""
    if not line or '|' not in line:
        return None
    parts = line.split('|')
    if len(parts) < 5:
        return None
    sha = parts[0][:8]
    author_email = parts[1]
    author_name = parts[2]
    date = parts[3]
    message = parts[4]

    # 解析 conventional commit
    commit_type = 'other'
    scope = ''
    subject = message

    # feat: fix: docs: etc.
    m = re.match(r'^(\w+)(?:\(([^)]+)\))?:\s*(.+)', message)
    if m:
        t = m.group(1).lower()
        if t in COMMIT_TYPES:
            commit_type = t
        scope = m.group(2) or ''
        subject = m.group(3)
        if '!' in message or 'BREAKING' in message.upper():
            commit_type = 'breaking'

    return {
        'sha': sha,
        'type': commit_type,
        'scope': scope,
        'subject': subject,
        'author': author_name,
        'date': date,
    }


# ============================================================
# 2. 核心分析逻辑
# ============================================================

def analyze_git_history(project_path, from_tag=None, to_tag=None):
    """分析 git 历史，生成 changelog 数据"""
    project_path = os.path.abspath(project_path)
    if not os.path.isdir(project_path):
        return {'error': f'路径不存在: {project_path}'}

    # 检查是否为 git 仓库
    git_dir = os.path.join(project_path, '.git')
    if not os.path.isdir(git_dir):
        return {'error': f'不是 git 仓库: {project_path}'}

    lines = run_git_log(project_path, from_tag, to_tag)
    commits = []
    for line in lines:
        if line:
            commit = parse_commit(line)
            if commit:
                commits.append(commit)

    # 按类型分组
    by_type = defaultdict(list)
    for commit in commits:
        by_type[commit['type']].append(commit)

    # 获取标签
    tags = []
    try:
        result = subprocess.run(
            ['git', 'tag', '--sort=-v:refname'],
            cwd=project_path,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=10
        )
        if result.returncode == 0:
            tags = [t for t in result.stdout.strip().split('\n') if t]
    except Exception:
        pass

    return {
        'project_path': project_path,
        'total_commits': len(commits),
        'commits': commits,
        'by_type': dict(by_type),
        'tags': tags[:20],  # 最多20个标签
        'from_tag': from_tag,
        'to_tag': to_tag,
    }


# ============================================================
# 3. 输出格式
# ============================================================

def format_text(result):
    """文本格式输出"""
    lines = [
        '=' * 60,
        'Auto Changelog Generator - 自动生成变更日志',
        '=' * 60,
        f'项目路径: {result["project_path"]}',
        f'总提交数: {result["total_commits"]}',
        f'标签: {", ".join(result["tags"][:5]) or "无"}',
        '',
    ]

    if result.get('error'):
        lines.append(f'错误: {result["error"]}')
        return '\n'.join(lines)

    if result['from_tag'] or result['to_tag']:
        lines.append(f'范围: {result["from_tag"] or "开始"} -> {result["to_tag"] or "最新"}')
        lines.append('')

    for commit_type, (label_cn, label_en) in COMMIT_TYPES.items():
        commits = result['by_type'].get(commit_type, [])
        if not commits:
            continue
        lines.append(f'[{label_cn}] {label_en} ({len(commits)}条)')
        lines.append('-' * 60)
        for c in commits[:20]:  # 最多20条
            scope = f'({c["scope"]}) ' if c['scope'] else ''
            lines.append(f'  - {c["subject"]} ({c["sha"]})')
        if len(commits) > 20:
            lines.append(f'  ... 还有 {len(commits) - 20} 条')
        lines.append('')

    other_commits = result.get('other', [])
    if other_commits:
        lines.append('[其他提交] Other')
        lines.append('-' * 60)
        for c in other_commits[:10]:
            lines.append(f'  - {c["subject"]} ({c["sha"]})')
        lines.append('')

    lines.append('=' * 60)
    return '\n'.join(lines)


def format_json(result):
    """JSON 格式输出"""
    output = dict(result)
    return json.dumps(output, ensure_ascii=False, indent=2)


def format_markdown(result):
    """Markdown 格式输出"""
    lines = [
        '# Changelog',
        '',
        f'**项目**: `{result["project_path"]}`',
        f'**总提交数**: {result["total_commits"]}',
        '',
        '---',
        '',
    ]

    if result.get('error'):
        lines.append(f'**错误**: {result["error"]}')
        return '\n'.join(lines)

    if result['tags']:
        lines.append(f'**标签**: {", ".join(result["tags"])}')
        lines.append('')

    if result['from_tag'] or result['to_tag']:
        lines.append(f'**范围**: `{result["from_tag"] or "开始"}` -> `{result["to_tag"] or "最新"}`')
        lines.append('')

    for commit_type, (label_cn, label_en) in COMMIT_TYPES.items():
        commits = result['by_type'].get(commit_type, [])
        if not commits:
            continue
        lines.append(f'## {label_en} ({label_cn})')
        lines.append('')
        for c in commits[:20]:
            scope = f'`{c["scope"]}` ' if c['scope'] else ''
            lines.append(f'- {scope}{c["subject"]} (`{c["sha"]}`)')
        if len(commits) > 20:
            lines.append(f'- ... 还有 {len(commits) - 20} 条提交')
        lines.append('')

    return '\n'.join(lines)


def format_html(result):
    """HTML 格式输出"""
    type_colors = {
        'feat': '#28a745',
        'fix': '#dc3545',
        'docs': '#17a2b8',
        'style': '#6c757d',
        'refactor': '#6610f2',
        'perf': '#fd7e14',
        'test': '#e85d04',
        'build': '#343a40',
        'ci': '#6f42c1',
        'chore': '#adb5bd',
        'breaking': '#ff0000',
        'other': '#6c757d',
    }

    type_labels = {
        'feat': 'New Features',
        'fix': 'Bug Fixes',
        'docs': 'Documentation',
        'style': 'Styles',
        'refactor': 'Code Refactoring',
        'perf': 'Performance',
        'test': 'Tests',
        'build': 'Build System',
        'ci': 'CI/CD',
        'chore': 'Chores',
        'breaking': 'Breaking Changes',
        'other': 'Other',
    }

    sections_html = ''
    for commit_type, (label_cn, label_en) in COMMIT_TYPES.items():
        commits = result['by_type'].get(commit_type, [])
        if not commits:
            continue
        color = type_colors.get(commit_type, '#6c757d')
        rows = ''
        for c in commits[:20]:
            scope = f'<span class="scope">{c["scope"]}</span>' if c['scope'] else ''
            rows += f'<li><code>{c["sha"]}</code> {scope}{c["subject"]}</li>'
        if len(commits) > 20:
            rows += f'<li class="more">... 还有 {len(commits) - 20} 条</li>'
        sections_html += f'''
<div class="section" style="border-left: 4px solid {color}">
  <h3>{label_en} <span class="count">{len(commits)}</span></h3>
  <ul>{rows}</ul>
</div>'''

    return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Changelog</title>
<style>
body {{ font-family: -apple-system, sans-serif; margin: 40px; background: #f9f9f9; }}
h1 {{ color: #333; }}
.meta {{ color: #666; margin-bottom: 30px; }}
.section {{ background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
.section h3 {{ margin: 0 0 15px 0; display: flex; align-items: center; gap: 10px; }}
.count {{ background: #e9ecef; padding: 2px 8px; border-radius: 12px; font-size: 0.85em; }}
.scope {{ background: #e9ecef; padding: 2px 6px; border-radius: 4px; font-size: 0.85em; margin-right: 4px; }}
ul {{ list-style: none; padding: 0; margin: 0; }}
li {{ padding: 8px 0; border-bottom: 1px solid #f0f0f0; }}
li:last-child {{ border-bottom: none; }}
li.more {{ color: #999; font-style: italic; }}
code {{ background: #f1f3f5; padding: 2px 6px; border-radius: 4px; font-size: 0.85em; }}
</style></head><body>
<h1>Changelog</h1>
<p class="meta"><strong>项目:</strong> {result['project_path']} | <strong>总提交数:</strong> {result['total_commits']}</p>
{sections_html}
</body></html>'''


# ============================================================
# 4. CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='Auto Changelog Generator - 从 git 历史生成 changelog'
    )
    parser.add_argument('project_path', nargs='?', default='.',
                        help='项目路径（必须是 git 仓库）')
    parser.add_argument('--format', choices=['text', 'json', 'markdown', 'html'],
                        default='markdown', help='输出格式')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--from-tag', help='起始标签')
    parser.add_argument('--to-tag', help='结束标签')
    args = parser.parse_args()

    result = analyze_git_history(args.project_path, args.from_tag, args.to_tag)

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
