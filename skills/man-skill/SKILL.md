---
name: man
description: Display man pages for Zensical documentation skills. Use this whenever the user types `man <skill-name>` (e.g., `man glossary-sync`, `man frontmatterer`, `man permalink-generator`) or asks to view a skill's manual, help page, usage documentation, options, flags, or command reference. Also triggers on phrases like "show me the man page", "how do I use this skill", "what are the options", "--help", "usage", "view man", "see man". If someone asks about how a skill works or what commands it supports, offer to show the man page.
version: "1.0.0"
last_updated: 2026-06-01
---

# Man Skill — Display Skill Man Pages

## What This Skill Does

When the user invokes `man <skill-name>`, find and display the skill's man page. This works for any skill installed under `~/.config/opencode/skills/` that includes a man page.

## Man Page Convention

Every skill can optionally include a man page at:

```
~/.config/opencode/skills/<skill-name>/man/<skill-name>.<section>
```

Where `<section>` is the man section number (default: `1`).

The man page is written in standard troff/nroff format (the `man` macro package), making it viewable with the `man(1)` command.

## Workflow

### Step 1: Parse the request

Extract the skill name from the user's command. Accept these formats:

| Input | Extracted skill |
| :--- | :--- |
| `man glossary-sync` | `glossary-sync` |
| `man frontmatterer` | `frontmatterer` |
| `man glossary-sync.1` | `glossary-sync` (section 1) |
| `man glossary-sync(1)` | `glossary-sync` (section 1) |
| `show me the man page for glossary-sync` | `glossary-sync` |
| `how do I use the frontmatterer skill` | `frontmatterer` |

Strip section suffixes (`.1`, `(1)`, etc.) when extracting the skill name.

### Step 2: Find the man page

Construct the path:

```
~/.config/opencode/skills/<skill-name>/man/<skill-name>.<section>
```

Default section is `1`. Try these in order:

1. `<skill-path>/man/<skill-name>.<section>` (e.g., `.1`, `.7`)
2. `<skill-path>/man/<skill-name>.1` (fallback to section 1)
3. `<skill-path>/man/<skill-name>.md` (markdown fallback)
4. `<skill-path>/README.md` (catch-all)

### Step 3: Display the man page

**Primary method** — use the system `man` command:

```bash
man <path-to-man-page>
```

The `man` command on macOS and Linux can display arbitrary man page files when given the full path. This gives correct formatting with bold, italics, and proper pagination.

**Fallback method 1** — render with groff directly if `man` fails:

```bash
groff -man -Tascii <path-to-man-page>
```

**Fallback method 2** — if neither `man` nor `groff` is available, read the man page file and display it as preformatted text, stripping troff macros to show the content cleanly.

### Step 4: If no man page exists

Tell the user: "No man page found for `<skill-name>`. Try reading the skill's SKILL.md at `~/.config/opencode/skills/<skill-name>/SKILL.md`."

## Error Handling

- **Skill not found**: `~/.config/opencode/skills/<skill-name>/` does not exist → "Skill `<skill-name>` not found. Use `ls ~/.config/opencode/skills/` to list available skills."
- **No man directory**: `<skill-path>/man/` does not exist → "Skill `<skill-name>` has no man page. Try reading `~/.config/opencode/skills/<skill-name>/SKILL.md`."
- **No man page file**: `<skill-path>/man/<skill-name>.1` does not exist → same message as above.

## Examples

```
User: man glossary-sync
You:   [run man on ~/.config/opencode/skills/glossary-sync/man/glossary-sync.1]

User: how do I use the frontmatterer skill?  
You:   [recognize this as a man request] Let me show you the man page.
       [run man on ~/.config/opencode/skills/frontmatterer/man/frontmatterer.1]
       If no man page exists, read SKILL.md instead.

User: man glossary-sync --help
You:   [recognize --help flag, strip it, show man page for glossary-sync]
