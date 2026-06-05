---
name: zh-punct-fixer
description: >
  Fix Chinese punctuation inconsistencies in Zensical documentation.
  Replaces ASCII : → ：, , → ，, ; → ；, ? → ？, ! → ！ in Chinese text context,
  preserving frontmatter, code blocks, URLs, markdown syntax, and English content.
  Trigger when user mentions: fix Chinese punctuation, replace ASCII colon/semicolon/comma with fullwidth,
  修正全形半形標點, 修復標點符號, fix punctuation, punctuation inconsistency in doc.
  Also triggers when the user demonstrates a single replacement (e.g. "replace : with ：" in a file)
  and likely wants the full treatment across all three punctuation marks.
  Use this aggressively — whenever Chinese text has mixed ASCII/fullwidth punctuation, offer to fix it.
version: 1.4.0
last_updated: 2026-06-05
compatibility:
  python: ">=3.8"
---

# Chinese Punctuation Fixer (全形標點修正)

Fixes inconsistent ASCII punctuation in Traditional Chinese documentation by replacing `:` → `：`, `,` → `，`, `;` → `；` in Chinese text context, while protecting frontmatter, code blocks, URLs, markdown syntax, and English text. Also fixes bold text spacing in CJK context (`**text**` gets proper spacing around it).

## Trigger phrases

Use this skill when the user says anything like:
- "fix Chinese punctuation issues in this doc"
- "replace ASCII colon with fullwidth" / "replace , with ，"
- "fix semicolon inconsistency" / "fix ; ；"
- "修復全形半形標點" / "修正標點符號" / "修復標點"
- "clean up punctuation" / "fix punctuation mixup"
- "fix bold spacing" / "fix bold rendering" / "bold text spacing in CJK"
- **After doing one manual replacement** — if the user asks to replace `:` in a file, they likely want all three (`:`, `,`, `;`) fixed. Offer the full treatment.

Even if the user only mentions one punctuation mark (e.g. "replace : with ："), treat it as a request to fix all three — the inconsistency applies across all of them.

## How to use

Run the bundled script on the target file(s):

```bash
python <skill_path>/scripts/fix_punctuation.py <file.md> [--dry-run]
```

Options:
- **Single file**: `python fix_punctuation.py docs/ec/some-doc.md`
- **Multiple files**: `python fix_punctuation.py doc1.md doc2.md doc3.md`
- **Preview only**: `python fix_punctuation.py doc.md --dry-run` (prints diff without modifying)

After running, verify the changes with a quick scan of the diff.

## What gets fixed

| ASCII | Fullwidth | Example |
|-------|-----------|---------|
| `:` | `：` | `請檢查：` (preceded by Chinese) |
| `,` | `，` | `設定，管理` (between Chinese) |
| `;` | `；` | `一般版；企業版` (between Chinese) |
| `?` | `？` | `商品符合嗎？` (preceded by Chinese) |
| `!` | `！` | `成功了！` (preceded by Chinese) |

### Bold text spacing

| Context | Fix | Example |
|---------|-----|---------|
| Before `**text**` preceded by CJK | Add space | `參閱**設定**` → `參閱 **設定**` |
| After `**text**` followed by CJK text | Add space | `**設定**頁面` → `**設定** 頁面` |
| After `**text**` followed by Chinese punct | No change | `**設定**，保留` → unchanged |

## What's preserved

- **Frontmatter**: all content between `---` delimiters
- **Code blocks**: fenced (triple backtick) and inline (`code`)
- **URLs and paths**: in markdown links `[text](url)` and images `![alt](path)`
- **Markdown syntax**: table alignment (`| :-- |`), admonitions (`!!!`, `???`), footnote defs (`[^n]:`), link refs (`[label]:`)
- **Lucide icons**: `:lucide-*:` syntax
- **HTML/CSS attributes**: `{ .class }`, `{ data-preview }`
- **English text**: punctuation in ASCII-only contexts (e.g. `Hello, world`)
- **Numbers**: commas in digits (`1,234`)
- **Anchors**: `(#anchor-name)` in heading references

## Important rules

1. **Always update `last_modified`** in the frontmatter after fixing. The script handles this automatically.
2. **Always offer `--dry-run` first** if the user is unsure — show them what will change before applying.
3. **For multi-file fixes**, run on all files at once rather than one by one.
4. **After fixing, verify** by checking the diff — make sure frontmatter, code blocks, and URLs are untouched.
5. **If the script produces any errors** (e.g. regex issues with unusual markdown), fall back to doing the replacements manually using targeted edits, following the same rules about what to preserve.

## Script reference

The script `scripts/fix_punctuation.py` handles all the context-aware logic. Read it only if you need to debug or modify its behavior — otherwise just invoke it.
