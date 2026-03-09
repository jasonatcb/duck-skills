---
name: frontmatterer
description: Update document frontmatter to match the zensical-zh-tw schema reference
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
- **Required fields** must not be empty: `title`, `description`, `created`, `last_modified`, `lang`, `permalink`
- **Language consistency**: Content-related fields must match the document's `lang` value:
  - `intents` - Must be in the same language as `lang` (zh-TW docs = Chinese intents)
  - `features` - Should match document language
  - `tags` - Follow document language conventions

## Example

See `example.md` in this directory for before/after transformation examples.

## Files in this skill

- `reference.md` - Complete frontmatter schema specification
- `example.md` - Before/after transformation examples
- `SKILL.md` - This file
