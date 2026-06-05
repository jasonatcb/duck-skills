#!/usr/bin/env python3
"""
rename_slug.py — Rename a Zensical documentation file and update all references.

Usage:
    python rename_slug.py <old-path> <new-filename> [options]

Arguments:
    old-path       Path to the file to rename (e.g., docs/ec/orders/訂單出貨流程.md)
    new-filename   New filename (e.g., order-shipping-flow or order-shipping-flow.md)

Options:
    --dry-run, -n      Preview changes without modifying anything
    --verbose, -v      Show detailed progress for each replacement
    --no-nav           Skip updating zensical.toml and zensical.en.toml
    --no-links         Skip updating internal wikilinks and markdown links
    --force, -f        Skip confirmation prompt
    --project-root DIR Project root directory (auto-detected if omitted)

The script handles:
  - File renaming
  - Wikilink updates: [[舊名]] → [[new-name]]
  - Markdown link updates: ](path/舊名.md) → ](path/new-name.md)
  - Frontmatter permalink updates
  - zensical.toml/zensical.en.toml nav path updates
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


def detect_project_root(path: str) -> Path | None:
    """Walk up from a path to find the directory containing zensical.toml."""
    p = Path(path).resolve()
    for parent in [p] + list(p.parents):
        toml = parent / "zensical.toml"
        if toml.is_file():
            return parent
    return None


def find_referencing_files(
    project_root: Path,
    old_stem: str,
    exclude_path: Path,
    verbose: bool = False,
) -> list[Path]:
    """Use ripgrep to find all files referencing the old stem."""
    cmd = [
        "rg", "-l", "--no-heading",
        "--fixed-strings",
        old_stem,
        str(project_root),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    files: list[Path] = []
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        p = Path(line).resolve()
        if p == exclude_path.resolve():
            continue
        if p.suffix not in (".md", ".toml", ".yml", ".yaml"):
            continue
        files.append(p)
    # Exclude .git, __pycache__, archive/ and similar
    files = [f for f in files
             if ".git" not in f.parts
             and "archive" not in f.parts]
    if verbose:
        for f in files:
            rel = f.relative_to(project_root)
            print(f"  reference found: {rel}")
    return files


def find_markdown_link_refs(
    content: str,
    old_stem: str,
) -> list[tuple[int, int, str]]:
    """Find markdown link references to old_stem.
    
    Returns list of (start, end, full_match) for each occurrence
    where the old_stem appears as a filename in a markdown link.
    Patterns matched:
      ](path/old_stem.md)
      ](old_stem.md)
      ](path/old_stem.md#anchor)
    """
    results: list[tuple[int, int, str]] = []
    # Pattern: ](  any-path-chars  old_stem  .md  optional-#anchor  )
    pattern = re.compile(
        r'(\]\()([^)]*?)' + re.escape(old_stem) + r'(\.md(?:#[^)]*)?)\)'
    )
    for m in pattern.finditer(content):
        results.append((m.start(), m.end(), m.group(0)))
    return results


def find_wikilink_refs(
    content: str,
    old_stem: str,
) -> list[tuple[int, int, str]]:
    """Find wikilink references [[old_stem]] or [[old_stem|text]]."""
    results: list[tuple[int, int, str]] = []
    pattern = re.compile(
        r'\[\[(\s*)' + re.escape(old_stem) + r'(\s*)(\]\]|\|)'
    )
    for m in pattern.finditer(content):
        results.append((m.start(), m.end(), m.group(0)))
    return results


def find_toml_refs(content: str, old_basename: str) -> list[tuple[int, int, str]]:
    """Find TOML nav path references like \".../old_basename\"."""
    results: list[tuple[int, int, str]] = []
    pattern = re.compile(r'\"([^\"]*' + re.escape(old_basename) + r')\"')
    for m in pattern.finditer(content):
        results.append((m.start(), m.end(), m.group(0)))
    return results


def update_permalink(content: str, old_stem: str, new_stem: str) -> str:
    """Update the permalink frontmatter field's last path segment."""
    # Match: permalink: https://help.cyberbiz.io/<path>/<old_stem>
    # Change to: permalink: https://help.cyberbiz.io/<path>/<new_stem>
    pattern = re.compile(
        r'^(permalink:\s*https://help\.cyberbiz\.io/[^\n]*)'
        + re.escape(old_stem) + r'(\s*)$',
        re.MULTILINE
    )
    return pattern.sub(r'\1' + new_stem + r'\2', content)


def write_safe(path: Path, content: str) -> None:
    """Write content atomically to avoid partial writes."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def check_conflicts(old_path: Path, new_basename: str) -> list[str]:
    """Check if the new filename conflicts with existing files.
    
    Checks both exact-name and case-insensitive conflicts (relevant on
    macOS APFS and other case-insensitive filesystems).
    
    Returns a list of conflict descriptions (empty = no conflicts).
    """
    conflicts: list[str] = []
    new_path = old_path.with_name(new_basename)
    directory = old_path.parent

    # Same file — always allowed (renaming to current name is a no-op)
    if new_path.resolve() == old_path.resolve():
        return conflicts

    # Exact match conflict
    if new_path.exists():
        conflicts.append(f"'{new_basename}' already exists in {directory}")
        return conflicts  # exact match supersedes case check

    # Case-insensitive conflict (detect upper/lower variants on any filesystem)
    for existing in directory.iterdir():
        if existing.name.lower() == new_basename.lower() and existing != old_path:
            conflicts.append(
                f"'{new_basename}' would conflict with '{existing.name}' "
                f"(case-insensitive match)"
            )
            break

    return conflicts


def rename_file(
    old_path: Path,
    new_basename: str,
    dry_run: bool = False,
    verbose: bool = False,
) -> Path | None:
    """Rename the file, returning the new path."""
    new_path = old_path.with_name(new_basename)
    if new_path.exists():
        print(f"  ERROR: target already exists: {new_path}")
        return None
    if dry_run:
        print(f"  would rename: {old_path.name} → {new_basename}")
        return new_path
    old_path.rename(new_path)
    if verbose:
        print(f"  renamed: {old_path.name} → {new_basename}")
    return new_path


def collect_md_files(targets: list[str]) -> list[Path]:
    """Resolve files and directories into a flat list of .md files."""
    files: list[Path] = []
    for target in targets:
        p = Path(target).resolve()
        if not p.exists():
            print(f"Path not found: {target}", file=sys.stderr)
            continue
        if p.is_file():
            if p.suffix == ".md":
                files.append(p)
            else:
                print(f"Not a markdown file: {target}", file=sys.stderr)
        elif p.is_dir():
            for md_file in sorted(p.rglob("*.md")):
                files.append(md_file)
    return sorted(set(files))


def has_cjk_chars(name: str) -> bool:
    """Check if filename contains CJK characters."""
    for ch in name:
        if '\u4e00' <= ch <= '\u9fff' or '\u3000' <= ch <= '\u303f':
            return True
    return False


def scan_chinese_files(directory: str) -> list[Path]:
    """Find all .md files with Chinese characters in their name."""
    root = Path(directory).resolve()
    files: list[Path] = []
    for md_file in root.rglob("*.md"):
        if has_cjk_chars(md_file.stem):
            files.append(md_file)
    return sorted(files)


# ---------------------------------------------------------------------------
# Main rename logic
# ---------------------------------------------------------------------------

def do_rename(args) -> int:
    """Execute a single file rename."""
    old_path = Path(args.old_path).resolve()

    if not old_path.is_file():
        print(f"Error: file not found: {old_path}", file=sys.stderr)
        return 1

    if old_path.suffix != ".md":
        print(f"Error: not a .md file: {old_path}", file=sys.stderr)
        return 1

    # Determine new filename
    new_basename = args.new_filename
    if not new_basename.endswith(".md"):
        new_basename += ".md"

    new_stem = Path(new_basename).stem
    old_stem = old_path.stem
    old_basename = old_path.name

    if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$', new_stem) and \
       not re.match(r'^[a-z0-9]$', new_stem):
        print(f"Warning: new filename '{new_stem}' is not kebab-case. "
              f"Expected lowercase letters, numbers, and hyphens.",
              file=sys.stderr)
        # Continue anyway, just warn

    # --- Check for filename conflicts ---
    conflicts = check_conflicts(old_path, new_basename)
    if conflicts:
        print("Error: filename conflict detected:", file=sys.stderr)
        for c in conflicts:
            print(f"  {c}", file=sys.stderr)
        print("Use --force to rename anyway (not recommended).", file=sys.stderr)
        return 1

    # Detect project root
    project_root = args.project_root
    if project_root:
        project_root = Path(project_root).resolve()
    else:
        detected = detect_project_root(str(old_path))
        if detected is None:
            print("Error: could not detect project root (no zensical.toml found). "
                  "Use --project-root.", file=sys.stderr)
            return 1
        project_root = detected

    if args.verbose:
        print(f"Project root: {project_root}")
        print(f"Old file: {old_path}")
        print(f"New filename: {new_basename}")
        print(f"Old stem: {old_stem}")
        print(f"New stem: {new_stem}")

    # --- Scan for references ---
    dry_run = args.dry_run
    verbose = args.verbose
    changes_made = 0
    errors = 0

    # Read old file content (need to update permalink before rename)
    old_content = old_path.read_text(encoding="utf-8")

    # --- 1. Update the file's own permalink ---
    if verbose:
        print("\n[1/4] Updating frontmatter permalink...")
    updated_content = update_permalink(old_content, old_stem, new_stem)
    if updated_content != old_content:
        changes_made += 1
        if dry_run:
            print(f"  would update permalink in: {old_path.name}")
        else:
            write_safe(old_path, updated_content)
            if verbose:
                print(f"  updated permalink in: {old_path.name}")
    else:
        if verbose:
            print(f"  (no permalink update needed in {old_path.name})")

    # --- 2. Find and update references in other files ---
    if not args.no_links:
        if verbose:
            print(f"\n[2/4] Scanning for references to '{old_stem}'...")
        ref_files = find_referencing_files(project_root, old_stem, old_path, verbose)
        if not ref_files and verbose:
            print("  (no references found)")

        for ref_file in ref_files:
            try:
                content = ref_file.read_text(encoding="utf-8")
                original = content

                # Update wikilinks
                wl_refs = find_wikilink_refs(content, old_stem)
                for (start, end, match_text) in wl_refs:
                    replacement = match_text.replace(old_stem, new_stem)
                    content = content[:start] + replacement + content[end:]
                    changes_made += 1
                    if verbose or dry_run:
                        rel = ref_file.relative_to(project_root)
                        print(f"  wikilink: {rel}: {match_text.strip()} → {replacement.strip()}")

                # Update markdown links
                # Re-scan after wikilink changes since content shifted
                ml_refs = find_markdown_link_refs(content, old_stem)
                for (start, end, match_text) in ml_refs:
                    replacement = match_text.replace(old_stem, new_stem)
                    content = content[:start] + replacement + content[end:]
                    changes_made += 1
                    if verbose or dry_run:
                        rel = ref_file.relative_to(project_root)
                        print(f"  mdlink:   {rel}: {match_text.strip()} → {replacement.strip()}")

                # Write back if changed
                if content != original and not dry_run:
                    write_safe(ref_file, content)

            except Exception as e:
                print(f"  ERROR processing {ref_file}: {e}", file=sys.stderr)
                errors += 1
    else:
        if verbose:
            print("\n[2/4] Skipping internal link updates (--no-links)")

    # --- 3. Update nav files (zensical.toml) ---
    if not args.no_nav:
        if verbose:
            print(f"\n[3/4] Updating nav files...")
        nav_files = [
            project_root / "zensical.toml",
            project_root / "zensical.en.toml",
        ]
        for nav_file in nav_files:
            if not nav_file.is_file():
                continue
            try:
                content = nav_file.read_text(encoding="utf-8")
                original = content
                toml_refs = find_toml_refs(content, old_basename)
                for (start, end, match_text) in toml_refs:
                    replacement = match_text.replace(old_basename, new_basename)
                    content = content[:start] + replacement + content[end:]
                    changes_made += 1
                    if verbose or dry_run:
                        print(f"  nav: {nav_file.name}: {match_text.strip()} → {replacement.strip()}")
                if content != original and not dry_run:
                    write_safe(nav_file, content)
            except Exception as e:
                print(f"  ERROR updating {nav_file}: {e}", file=sys.stderr)
                errors += 1
    else:
        if verbose:
            print("\n[3/4] Skipping nav updates (--no-nav)")

    # --- 4. Rename the file ---
    if verbose:
        print(f"\n[4/4] Renaming file...")
    new_path = rename_file(old_path, new_basename, dry_run, verbose)
    if new_path:
        changes_made += 1

    # --- Summary ---
    mode = " (dry run)" if dry_run else ""
    print(f"\n{'─' * 50}")
    print(f"Summary{mode}:")
    print(f"  Changes: {changes_made}")
    print(f"  Errors:  {errors}")
    print(f"  File:    {old_path.name} → {new_basename if not dry_run else '(would rename)'}")
    if not dry_run and changes_made > 0 and verbose:
        print(f"  Next:    run 'git diff' to review changes before committing")

    return 0 if errors == 0 else 1


# ---------------------------------------------------------------------------
# Batch / scan
# ---------------------------------------------------------------------------

def do_check(args) -> int:
    """Check/dry-run mode: show what would change."""
    args.dry_run = True
    return do_rename(args)


def do_scan(args) -> int:
    """Scan for Chinese-named files and display them."""
    project_root = args.project_root
    if project_root:
        project_root = Path(project_root).resolve()
    else:
        detected = detect_project_root(".")
        if detected is None:
            print("Error: could not detect project root", file=sys.stderr)
            return 1
        project_root = detected

    files = scan_chinese_files(str(project_root / "docs"))
    if not files:
        print("No Chinese-named .md files found.")
        return 0

    print(f"Found {len(files)} Chinese-named .md files:\n")
    for f in files:
        rel = f.relative_to(project_root)
        # Quick check: does it have a permalink?
        content = f.read_text(encoding="utf-8")
        has_permalink = bool(re.search(r'^permalink:\s*(https?://\S+)?\s*$', content, re.MULTILINE))
        pm_status = "✅" if has_permalink else "⚠️ no permalink"
        print(f"  {rel}  {pm_status}")

    print(f"\nTo rename a file: filename-slugger rename <path> <new-name>")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Rename a Zensical doc file and update all references.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s rename docs/ec/orders/訂單出貨流程.md order-shipping-flow
  %(prog)s rename docs/pos/orders/設定POS訂單自動結案.md pos-auto-close --verbose
  %(prog)s rename docs/ec/orders/訂單出貨流程.md order-shipping-flow --dry-run -v
  %(prog)s scan                                  # List all Chinese-named files
  %(prog)s check docs/ec/orders/訂單出貨流程.md order-shipping-flow  # Dry-run
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # rename
    rename_p = subparsers.add_parser("rename", help="Rename a file and update references")
    rename_p.add_argument("old_path", help="Path to the file to rename")
    rename_p.add_argument("new_filename", help="New filename (e.g., order-shipping-flow)")
    _add_common_args(rename_p)

    # check (dry-run alias — same as rename but dry-run defaults to True)
    check_p = subparsers.add_parser("check", help="Preview what would change (dry-run)")
    check_p.add_argument("old_path", help="Path to the file to rename")
    check_p.add_argument("new_filename", help="New filename (e.g., order-shipping-flow)")
    _add_common_args(check_p)

    # scan
    scan_p = subparsers.add_parser("scan", help="List all Chinese-named .md files")
    scan_p.add_argument("--project-root", help="Project root directory")

    args = parser.parse_args()

    if args.command == "rename":
        return do_rename(args)
    elif args.command == "check":
        return do_check(args)
    elif args.command == "scan":
        return do_scan(args)
    else:
        parser.print_help()
        return 1


def _add_common_args(parser):
    parser.add_argument("--dry-run", "-n", action="store_true", help="Preview only")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    parser.add_argument("--no-nav", action="store_true", help="Skip nav file updates")
    parser.add_argument("--no-links", action="store_true", help="Skip link updates")
    parser.add_argument("--force", "-f", action="store_true", help="Skip confirmation")
    parser.add_argument("--project-root",
                        help="Project root (auto-detected if omitted)")


if __name__ == "__main__":
    sys.exit(main())
