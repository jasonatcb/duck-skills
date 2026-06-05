#!/usr/bin/env python3
"""
fix_punctuation.py — Fix Chinese punctuation inconsistencies in Zensical docs.

Replaces ASCII : → ：, , → ，, ; → ；, ? → ？, ! → ！ in Chinese text context,
while preserving frontmatter, code blocks, URLs, markdown syntax, and English text.

Usage:
    python fix_punctuation.py <file.md> [<file2.md> ...] [--dry-run]
"""

import re
import sys
from pathlib import Path
from datetime import datetime


CJK = '\u4e00-\u9fff'
CJK_PUNCT = '\u3000-\u303f'
FULLWIDTH = '\uff00-\uffef'
CJK_RANGE = f'[{CJK}{CJK_PUNCT}{FULLWIDTH}]'

RE_CJK = re.compile(r'[\u4e00-\u9fff]')


def has_cjk(text: str) -> bool:
    return bool(RE_CJK.search(text))


def _has_cjk_both_sides(text: str, pos: int, window: int = 5) -> bool:
    """Check if CJK exists within `window` chars on both sides of `pos`."""
    before = text[max(0, pos - window):pos]
    after = text[pos + 1:min(len(text), pos + window + 1)]
    return bool(RE_CJK.search(before)) and bool(RE_CJK.search(after))


def fix_file(filepath: str, dry_run: bool = False) -> bool:
    content = Path(filepath).read_text(encoding='utf-8')

    # 1. Extract and store frontmatter
    fm = re.match(r'^---\n.*?\n---\n', content, re.DOTALL)
    if fm:
        frontmatter = fm.group()
        body = content[fm.end():]
    else:
        frontmatter = ''
        body = content

    # 2. Process body: split into code blocks and non-code segments
    body_fixed = process_body(body)

    new_content = frontmatter + body_fixed

    # 3. Update last_modified
    new_content = update_last_modified(new_content)

    if new_content == content:
        return False  # no changes

    if dry_run:
        print(f'[DRY RUN] Changes for: {filepath}')
        _show_diff(content, new_content)
    else:
        Path(filepath).write_text(new_content, encoding='utf-8')
        print(f'Fixed: {filepath}')

    return True


def process_body(text: str) -> str:
    """Split body into code/non-code segments and process each."""
    segments = re.split(r'(```[\s\S]*?```)', text)
    out = []
    for seg in segments:
        if seg.startswith('```'):
            out.append(seg)  # preserve code blocks
        else:
            out.append(_process_text_lines(seg))
    return ''.join(out)


def _process_text_lines(text: str) -> str:
    lines = text.split('\n')
    result = []
    for line in lines:
        result.append(_process_line(line))
    return '\n'.join(result)


def _process_line(line: str) -> str:
    # Skip lines that are purely markdown structure
    stripped = line.lstrip()
    if not stripped:
        return line

    # Table alignment row
    if re.match(r'\|[\s:]*-+[\s:]*\|', stripped):
        return line
    # Footnote definition
    if re.match(r'^\[\^.\]\s*:\s', stripped):
        return line
    # Link reference definition
    if re.match(r'^\[.+\]\s*:\s+\S', stripped):
        return line

    # Protect inline constructs with placeholders
    placeholders = {}
    counter = [0]

    def protect(pat: str):
        def _replacer(m):
            idx = counter[0]
            counter[0] += 1
            key = f'\x00ZH{idx:04d}\x00'
            placeholders[key] = m.group(0)
            return key
        return _replacer

    # Order matters: longer/more specific patterns first
    line = re.sub(r':lucide-[a-z-]+:', protect(r':lucide-[a-z-]+:'), line)
    line = re.sub(r'`[^`]+`', protect(r'`[^`]+`'), line)
    line = re.sub(r'\[([^\]]*)\]\(([^)]*)\)', protect(r'\[([^\]]*)\]\(([^)]*)\)'), line)
    line = re.sub(r'!\[([^\]]*)\]\(([^)]*)\)', protect(r'!\[([^\]]*)\]\(([^)]*)\)'), line)
    line = re.sub(r'\{[^}]*\}', protect(r'\{[^}]*\}'), line)

    # Now replace punctuation in Chinese context
    line = _replace_punct(line)

    # Fix bold text spacing in CJK context
    line = _fix_bold_spacing(line)

    # Restore placeholders in reverse order (outer → inner)
    for key in reversed(list(placeholders.keys())):
        line = line.replace(key, placeholders[key])

    return line


def _replace_punct(line: str) -> str:
    """
    Context-aware replacement for : → ：, , → ，, ; → ；, ? → ？, ! → ！.

    Three passes:
      1. Preceded by CJK         — e.g. `條件:` → `條件：`
      2. Followed by CJK          — e.g. `:**設置` → `：**設置`
      3. Broad context           — CJK within ±5 chars on both sides,
                                   catches `(選填):**` (immediate neighbors are `)` and `*`).
    """
    # ── Pass 1: preceded by CJK ──
    line = re.sub(rf'({CJK_RANGE}):', lambda m: m.group(1) + '：', line)
    line = re.sub(rf'({CJK_RANGE}),', lambda m: m.group(1) + '，', line)
    line = re.sub(rf'({CJK_RANGE});', lambda m: m.group(1) + '；', line)
    line = re.sub(rf'({CJK_RANGE})\?', lambda m: m.group(1) + '？', line)
    line = re.sub(rf'({CJK_RANGE})!', lambda m: m.group(1) + '！', line)

    # ── Pass 2: followed by CJK ──
    line = re.sub(rf'(?<!{CJK_RANGE}):(?={CJK_RANGE})', '：', line)
    line = re.sub(rf'(?<![{CJK_RANGE}\d]),(?={CJK_RANGE})', '，', line)
    line = re.sub(rf'(?<!{CJK_RANGE});(?={CJK_RANGE})', '；', line)
    line = re.sub(rf'(?<!{CJK_RANGE})\?(?={CJK_RANGE})', '？', line)
    line = re.sub(rf'(?<!{CJK_RANGE})!(?={CJK_RANGE})', '！', line)

    # ── Pass 3: broad context (CJK within ±5 on both sides) ──
    line = _broad_replace(line, ':', '：')
    line = _broad_replace(line, ',', '，')
    line = _broad_replace(line, ';', '；')
    line = _broad_replace(line, '?', '？')
    line = _broad_replace(line, '!', '！')

    return line


def _is_comma_between_digits(text: str, pos: int) -> bool:
    """Check if comma at pos is a thousands separator (e.g. 1,000)."""
    return pos > 0 and pos < len(text) - 1 and text[pos-1].isdigit() and text[pos+1].isdigit()


def _fix_bold_spacing(line: str) -> str:
    """
    Fix bold text spacing in CJK context.

    Uses a single-pass approach: finds each `**text**` span (where text doesn't
    contain `**`), then checks context on both sides:

    - Adds a space BEFORE **text** when preceded directly by CJK characters
      (e.g. `參閱**設定**` → `參閱 **設定**`)
    - Adds a space AFTER **text** when followed by CJK characters that are
      NOT Chinese punctuation (，。；：？！、), since those already provide
      adequate visual separation
      (e.g. `**設定**頁面` → `**設定** 頁面`, but `**設定**，保留` stays)
    """
    NO_SPACE_AFTER = set('，。；：？！、')
    CJK_RE = re.compile(CJK_RANGE)

    pattern = re.compile(r'\*\*(.+?)\*\*')
    parts = []
    last_end = 0
    for m in pattern.finditer(line):
        start, end = m.start(), m.end()
        before = line[start - 1] if start > 0 else ''
        after = line[end] if end < len(line) else ''

        needs_before = bool(CJK_RE.match(before))
        needs_after = bool(CJK_RE.match(after)) and after not in NO_SPACE_AFTER

        prefix = ' ' if needs_before else ''
        suffix = ' ' if needs_after else ''

        parts.append(line[last_end:start])
        parts.append(f'{prefix}{m.group(0)}{suffix}')
        last_end = end

    parts.append(line[last_end:])
    return ''.join(parts)


def _broad_replace(text: str, punct: str, fullwidth: str) -> str:
    """Replace remaining ASCII punctuation if CJK is within ±5 on both sides."""
    positions = [m.start() for m in re.finditer(re.escape(punct), text)]
    if not positions:
        return text
    # Process right-to-left to preserve positions
    for pos in reversed(positions):
        if punct == ',' and _is_comma_between_digits(text, pos):
            continue
        if _has_cjk_both_sides(text, pos):
            text = text[:pos] + fullwidth + text[pos + 1:]
    return text


def update_last_modified(content: str) -> str:
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    content = re.sub(
        r'^(last_modified:\s*).*$',
        lambda m: m.group(1) + now,
        content,
        count=1,
        flags=re.MULTILINE
    )
    return content


def _show_diff(old: str, new: str):
    old_lines = old.split('\n')
    new_lines = new.split('\n')
    import difflib
    diff = difflib.unified_diff(
        old_lines, new_lines,
        fromfile='original', tofile='fixed',
        lineterm=''
    )
    for d in diff:
        if d.startswith('+') or d.startswith('-') or d.startswith('@@'):
            print(d)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print('Usage: python fix_punctuation.py <file.md> [<file2.md> ...] [--dry-run]')
        sys.exit(1)

    dry_run = '--dry-run' in sys.argv
    files = [f for f in sys.argv[1:] if f != '--dry-run']

    any_fixed = False
    for fp in files:
        if fix_file(fp, dry_run):
            any_fixed = True

    if not any_fixed and not dry_run:
        print('No changes needed.')


if __name__ == '__main__':
    main()
