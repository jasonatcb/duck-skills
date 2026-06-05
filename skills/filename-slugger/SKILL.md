---
name: filename-slugger
description: >
  Convert Chinese-named documentation files to English kebab-case filenames
  while automatically updating all internal references (wikilinks, markdown
  links, navigation, frontmatter permalinks). Use this whenever the user
  asks to rename files, convert filenames, change file names, slugify docs,
  standardize filenames, fix filenames, or maintain consistent URL slugs.
  Also triggers when the user mentions Chinese filenames, kebab-case
  conversion, filename convention, or slug strategy. Use it even when
  the user only talks about "fixing filenames" or "cleaning up file names"
  without stating the specific convention — this skill handles the
  complete workflow of renaming + reference updating.
version: "1.0.0"
last_updated: "2026-06-03"
---

# filename-slugger

Convert Chinese-named Zensical documentation files to English kebab-case
filenames, automatically updating all internal references so nothing breaks.

## Why this matters

Zensical auto-generates URL slugs from filenames. Chinese filenames produce
URL-encoded, unreadable slugs (e.g., `%E8%A8%82%E5%96%AE...`). English
kebab-case filenames produce clean, readable, SEO-friendly URLs. However,
renaming files without updating cross-references will break wikilinks,
markdown links, navigation entries, and frontmatter permalinks. This skill
handles all of that automatically so you can rename with confidence.

## Command Reference

Present these commands to the user as a CLI-like interface:

```
filename-slugger rename <old-path> <new-name> [options]
filename-slugger check  <old-path> <new-name> [options]
filename-slugger scan   [--project-root DIR]
```

### Commands

| Command | Description |
| :--- | :--- |
| `rename` | Rename a single file + update all references |
| `check`  | Dry-run: preview all changes without modifying anything |
| `scan`   | List all Chinese-named `.md` files in the project |

### Options

| Option | Description |
| :--- | :--- |
| `--dry-run`, `-n` | Preview only, no changes |
| `--verbose`, `-v` | Show detailed progress per reference |
| `--no-nav` | Skip `zensical.toml` / `zensical.en.toml` updates |
| `--no-links` | Skip wikilink and markdown link updates |
| `--force`, `-f` | Skip confirmation prompts |
| `--project-root DIR` | Project root (auto-detected if omitted) |

### Arguments

| Argument | Description |
| :--- | :--- |
| `old-path` | Path to the Chinese-named `.md` file (e.g., `docs/ec/orders/訂單出貨流程.md`) |
| `new-name` | Desired English kebab-case name (e.g., `order-shipping-flow` — `.md` optional) |

## Workflow

When the user asks to rename a file, follow this sequence:

### Step 1: Identify target file

The user provides the file path, or you can use `scan` to discover Chinese-named files:

```
filename-slugger scan
```

This lists all Chinese-named `.md` files with their permalink status so the
user can decide which files to convert.

### Step 2: Preview before acting

Always run `check` first to show the user what will change:

```
filename-slugger check docs/ec/orders/訂單出貨流程.md order-shipping-flow -v
```

This lists every reference that will be updated. Show the output to the user
and ask for confirmation before proceeding.

### Step 3: Execute the rename

Once confirmed, run `rename`:

```
filename-slugger rename docs/ec/orders/訂單出貨流程.md order-shipping-flow
```

Add `--verbose` to show live progress. Add `--no-nav` if the user only wants
file-level changes. Add `--no-links` if they only want the file renamed
without touching references.

### Step 4: Verify

After renaming, verify the changes:

1. **Read the renamed file** — confirm frontmatter `permalink` is updated:
   ```
   permalink: https://help.cyberbiz.io/ec/orders/order-shipping-flow
   ```
2. **Spot-check 1-2 referencing files** — confirm wikilinks/markdown links
   point to the new name
3. **Run `git diff --stat`** to see all files changed
4. **Optionally serve locally** (`uv run zensical serve`) and check a few
   pages that link to the renamed file

## Slug Naming Convention

Follow the existing project convention when suggesting names:

**Do:**
- All lowercase (`order-shipping-flow`)
- Kebab-case hyphens (`edit-order-content`)
- Start with a letter, end with a letter or digit (`cancel-order`)
- Keep it meaningful but concise (`repurchase-order` not
  `how-to-repurchase-a-previous-order`)
- Use standard e-commerce/logistics terminology (`cvs`, `tcat`, `sf-express`,
  `ecpay`, `b2c`, `c2c`)

**Don't:**
- Use underscores (`order_shipping`) or camelCase (`orderShipping`)
- Include file-type suffixes in the stem (no `order-flow-md`)
- Use overly generic names (`process`, `guide`, `flow`)

**Strategy for naming:**
1. Read the file's `title` frontmatter to understand its content
2. Look at neighboring files for naming patterns (e.g., if other files in
   `ec/orders/` use `cancel-order` and `edit-order-content`, your name
   should fit the same style)
3. For cross-border / international features, note the market context
   (e.g., `cross-border-refund-flow` not just `refund-flow`)

## What the script updates

When you run `rename`, the script (`scripts/rename_slug.py`) handles:

| Reference type | Example | Updated? |
| :--- | :--- | :---: |
| Wikilinks in frontmatter `related` | `[[訂單退貨流程]]` → `[[order-return-flow]]` | ✅ |
| Wikilinks in frontmatter `prerequisites` | `[[已開通服務]]` → `[[activated-service]]` | ✅ |
| Wikilinks in body text | `[[訂單退款流程]]` → `[[order-refund-flow]]` | ✅ |
| Markdown links | `](訂單退貨流程.md)` → `](order-return-flow.md)` | ✅ |
| Markdown links with relative paths | `](../orders/訂單退貨流程.md)` → `](../orders/order-return-flow.md)` | ✅ |
| Markdown links with anchors | `](舊名.md#section)` → `](new-name.md#section)` | ✅ |
| Frontmatter `permalink` | URL last segment updated | ✅ |
| `zensical.toml` nav paths | `"ec/orders/訂單出貨流程.md"` updated | ✅ |
| `zensical.en.toml` nav paths | `"zh-tw/ec/orders/訂單出貨流程.md"` updated | ✅ |

**What the script does NOT touch:**
- Body text that mentions the old name as prose (not a link) — the Chinese
  characters in headings and descriptions are preserved as-is
- Image paths or asset references (unless they happen to match the old stem)
- External URLs
- Files in `.git/`, `__pycache__`, or `node_modules/`

## Safety: Conflict Detection

Before making any changes, `rename` and `check` always verify the new
filename won't conflict with existing files in the same directory:

- **Exact match** — another file already has the same name
- **Case-insensitive match** — another file differs only by uppercase/lowercase
  (e.g., renaming to `Cancel-Order` when `cancel-order.md` already exists)

If a conflict is detected, the rename stops with an error message listing
the conflicting file. Use `--force` to override (not recommended — pick a
different name instead).

## Edge Cases

### Same Chinese text as non-reference prose

The script only replaces `[[舊名]]` (wikilinks) and `](舊名.md)` (markdown
links). If the Chinese text appears in body paragraphs or headings as plain
prose, it's left untouched. This is intentional — the content should remain
in Traditional Chinese.

### Same stem used in different directories

The script matches by exact stem string. If two files share the same Chinese
name (unlikely but possible in different subdirectories), the regex patterns
correctly match all occurrences of that stem, regardless of path prefix.

### File already renamed but references missed

If a rename was done manually and references were missed, run:

```
filename-slugger check docs/path/old-chinese-name.md new-name
```

This won't find the old file (it no longer exists), so instead you can use
`rg` to find remaining references and fix them manually, or use the script's
`--dry-run` mode on a fresh rename to see what *would* be changed.

### File references from outside docs/

References from `zensical.toml` and `zensical.en.toml` are handled
separately via the `--no-nav` flag. If you need to skip nav updates (e.g.,
the nav is maintained separately), pass `--no-nav`.

### Multiple files in batch

The `scan` command shows all Chinese-named files. Rename them one at a time
using `rename`. Each rename runs independently, so you can verify each step.

## Script path

The script is at:
```
~/.config/opencode/skills/filename-slugger/scripts/rename_slug.py
```

Run it directly:

```bash
python3 ~/.config/opencode/skills/filename-slugger/scripts/rename_slug.py rename <args>
```

Or use `cd` to the project root first for cleaner paths:

```bash
cd /path/to/project
python3 ~/.config/opencode/skills/filename-slugger/scripts/rename_slug.py rename <args>
```
