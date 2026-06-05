---
name: permalink-generator
description: Generate and update `permalink` field in Zensical markdown frontmatter using the pattern `https://help.cyberbiz.io/{{folder path}}/{{filename}}`. Use this when the user asks to add, fix, or generate permalink values for documentation files (single or batch), or when they mention "隱藏 permalink", "補上 permalink", "permalink 不正確", or are running the frontmatterer skill (permalink should be generated after frontmatterer finishes). Do NOT use for general slug, URL, or frontmatter editing tasks that don't involve the `permalink` field.
version: 1.1.0
last_updated: 2026-05-28
---

# Permalink Generator for Zensical Documentation

## Purpose

Generate and insert the `permalink` field into one or more markdown files' frontmatter using the pattern `https://help.cyberbiz.io/{{folder path}}/{{filename}}`.

## When to Use

Use this skill whenever someone asks to:
- Add permalink to a doc file
- Fix/generate permalink for a specific file or a batch of files
- Update a file's permalink
- Scan a directory and add permalink to all files that are missing it
- Check if permalink is correct for given files

## Workflow

### Step 1: Understand the Input

The user can provide input in these forms:
- **Single file**: `docs/ec/orders/使用超商大宗寄倉（B2C）出貨.md`
- **Directory (batch)**: `docs/ec/orders/` — process all `.md` files in that directory
- **Multiple explicit files**: `docs/ec/orders/file1.md docs/ec/orders/file2.md`
- **Glob pattern**: `docs/ec/orders/*.md`
- **Mixed**: A combination of files and directories

When the user provides a directory or glob, process only files that are **missing or have empty** `permalink` fields.

### Step 2: Gather Target Files

Resolve the input into a list of markdown files:
- For a single file: validate it exists and is `.md`
- For a directory: scan for all `*.md` files recursively (or non-recursively, based on user preference)
- For glob patterns: resolve the pattern

### Step 3: For Each File

For each target file, perform Steps 3a-3e:

#### 3a: Read the File

Read the file and extract its filename (stem) — the file name without the `.md` extension. For example:
- `repurchase-order.md` → filename is `repurchase-order`
- `使用超商大宗寄倉（B2C）出貨.md` → filename is `使用超商大宗寄倉（B2C）出貨`

#### 3b: Determine the Folder Path

The folder path is the file's directory relative to `docs/`. For example:
- `docs/ec/orders/使用超商大宗寄倉（B2C）出貨.md` → folder path is `ec/orders`
- `docs/ec/products/新增與更新商品.md` → folder path is `ec/products`
- `docs/index.md` → folder path is empty (just `https://help.cyberbiz.io/{{filename}}`)

#### 3c: Construct the Permalink

Format: `https://help.cyberbiz.io/{{folder path}}/{{filename}}`

The filename is the file's stem (name without `.md` extension), used as-is. Do NOT convert to a slug.

Examples:
| Filename | Folder Path | Result |
|----------|-------------|--------|
| repurchase-order | ec/orders | `https://help.cyberbiz.io/ec/orders/repurchase-order` |
| 使用超商大宗寄倉（B2C）出貨 | ec/orders | `https://help.cyberbiz.io/ec/orders/使用超商大宗寄倉（B2C）出貨` |
| 設定商品到貨通知 | ec/products/sales | `https://help.cyberbiz.io/ec/products/sales/設定商品到貨通知` |

#### 3d: Check Existing Permalink

- **No `permalink` field**: Insert the generated value.
- **`permalink` exists but empty**: Fill it with the generated value.
- **`permalink` exists with a value and it matches the generated value**: Skip (nothing to change).
- **`permalink` exists with a different value**:
  - **Single file mode**: Show the user the existing value and the generated value, then ask for confirmation before overwriting.
  - **Batch mode**: Report the conflict and skip that file (do NOT overwrite without user confirmation). At the end, provide a summary of conflicts for the user to review.

#### 3e: Insert/Update the Permalink

Add/update the `permalink` field in the frontmatter and save the file.

Insert position: right after the `title` field (if `description` follows `title`, insert between them to maintain logical ordering). Otherwise, insert at the end of the frontmatter block.

### Step 4: Report Results

After processing all files, provide a clear summary:

**Single file:**
- "Updated `file.md`: permalink set to `https://help.cyberbiz.io/...`"
- Or "Skipped: permalink already correct"

**Batch:**
```
Batch processing complete:
- 5 files updated
- 2 files skipped (already correct)
- 1 file skipped (conflict — existing value differs, needs review)
- 1 file skipped (unreadable)
```
For conflicts, list the files and their old vs new values so the user can make decisions.

## Integration with frontmatterer

When the frontmatterer skill is invoked (`/frontmatterer`), the permalink-generator should also run on the same target files **after** frontmatterer finishes its updates.

### Workflow

1. **frontmatterer** completes its frontmatter updates (adds missing fields, reorders, etc.)
2. **permalink-generator** then runs on the same files to generate/update the `permalink` field
3. Report results: summarize which files got their permalink added vs skipped

This ensures that every frontmatter update session also produces a correct permalink without requiring a separate request.

## Edge Cases

- **Multiple files**: Process each file independently, reporting results per file.
- **File outside `docs/`**: Warn the user that the path doesn't look like a Zensical doc path (expects `docs/...`).
- **File cannot be read**: Report the error clearly.
- **File not found**: Report the error clearly.
- **Index files** (`docs/something/index.md`): Folder path should be `something` (not `something/index`), same as any other file.
- **Non-md files in directory**: Only process `.md` files.
- **Empty batch**: If no files need changes, state that clearly.

## Script

A helper script is available at `scripts/generate_permalink.py` for deterministic permalink computation. Use it when batch-processing files or when precision matters.

```bash
# Single file
python scripts/generate_permalink.py "docs/ec/orders/使用超商大宗寄倉（B2C）出貨.md"

# Multiple files
python scripts/generate_permalink.py "docs/ec/orders/file1.md" "docs/ec/orders/file2.md"

# Directory (scan all .md files)
python scripts/generate_permalink.py "docs/ec/orders/"
```
