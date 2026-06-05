---
name: frontmatterer
description: Update document frontmatter to match the zensical-zh-tw schema reference
version: "1.0.8"
last_updated: 2026-03-25
license: MIT
compatibility: opencode
metadata:
  audience: documentation maintainers
  workflow: zensical
---

## What I do

I update the frontmatter of Markdown documentation files to match the standardized schema. I:

- **Preserve existing values** - Keep all frontmatter fields that already have values
- **Add missing fields** - Insert any required or optional fields that are missing
- **Maintain proper order** - Reorder all frontmatter fields to match the reference sequence
- **Follow the schema** - Ensure all fields conform to the types and formats defined in the reference

## When to use me

Use this skill when you need to:

- Standardize frontmatter across documentation files
- Update an existing document's frontmatter to the current schema
- Add missing frontmatter fields to a document
- Ensure frontmatter consistency across the zensical-zh-tw documentation project

## How to invoke me

When invoked with a file path:

1. **Read the reference schema** from the `reference.md` file in this skill directory
2. **Read the target file** specified by the user
3. **Parse existing frontmatter** and identify:
   - Fields with values (preserve these exactly)
   - Missing fields (add with appropriate defaults)
4. **Reconstruct frontmatter** following the exact field order from `reference.md`
5. **Update last_modified** to current timestamp (`YYYY-MM-DD HH:mm`)
6. **Write the updated file** back

## Key rules

- **Never modify** existing field values unless explicitly told to
- **Never change** the `created` field
- **Always update** `last_modified` when making changes
- **Follow field order** exactly as specified in `reference.md`
- **Use correct types**: strings, arrays `[]`, integers `0`, booleans `true/false`
- **Required fields** must not be empty: `title`, `description`, `created`, `last_modified`, `lang`, `permalink`, `tags`
- **Essential content fields** - The following fields should NOT be left empty when the document has relevant content:
  - `intents` - User goals/intentions (e.g., 設定 GA4 站內搜尋追蹤)
  - `features` - System features mentioned (e.g., GA4 加強型評估)
  - `difficulty` - Document difficulty level (enum: `beginner`, `intermediate`, `advanced`)
  - `prerequisites` - Required pre-reading or tasks
    - If referencing existing doc with specific heading: use wikilink format `"[[filename#標題]]"`
    - If referencing existing doc without specific heading: use wikilink format `"[[文件標題]]"`
    - **If no existing related doc**: use plain string (e.g., `- 需先完成 Google Ads 帳號註冊`)
  - `related` - Related documentation (use wikilink format `"[[filename]]"`, MUST verify doc exists)
  - `tags` - SEO keywords (use underscores for multi-word terms)
  - `paths` - Navigation path mentioned in document body. For external services (e.g., GA4), include the service name as prefix (e.g., "GA4 後台 > 管理 > 資源設定"). For CYBERBIZ admin, use "選單項目 > 子項目" format.
- **status field** - Leave as empty string `""` unless explicitly told to set a value
- **Language consistency**: Content-related fields must match the document's `lang` value:
  - `intents` - Must be in the same language as `lang` (zh-TW docs = Chinese intents)
  - `features` - Should match document language
  - `tags` - Follow document language conventions
- **Term Formatting**: Use underscores `_` instead of spaces for multi-word terms in `intents`, `features`, and `tags` (e.g., `LINE_OA`, `Google_Analytics`).
- **modules**: Match the CYB admin console left sidebar menu items (e.g., "訂單", "商品", "會員"). **Do NOT fabricate values** - only use verified values from reference.md or existing documents. When in doubt, grep existing docs to find the correct modules value.
- **paths**: Use format "選單項目 > 子項目" (e.g., "訂單 > 訂單報表匯出")
- **related** and **prerequisites**: Use Obsidian wikilink format with double quotes `"[[filename]]"` (e.g., `"[[設定網站安全性]]"`, `"[[POS 報表列表與功能說明]]"`)

## Example

See `example.md` in this directory for before/after transformation examples.

## Files in this skill

- `reference.md` - Complete frontmatter schema specification
- `example.md` - Before/after transformation examples
- `SKILL.md` - This file
