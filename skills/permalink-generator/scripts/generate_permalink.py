#!/usr/bin/env python3
"""
Generate permalink URL for Zensical documentation files.

Usage:
    # Single file
    python generate_permalink.py <file-path>

    # Multiple files
    python generate_permalink.py <file1> <file2> ...

    # Directory (scan all .md files recursively)
    python generate_permalink.py <directory-path>

    # Mixed
    python generate_permalink.py <file1> <dir1> <file2> ...

The permalink follows the pattern:
    https://help.cyberbiz.io/{{folder_path}}/{{filename}}

Where folder_path is the directory relative to docs/, and filename is
the file's stem (name without .md extension).

Exit codes:
    0: All files processed successfully
    1: Some files had errors
"""
import os
import sys
from pathlib import Path


def filename_from_path(file_path: str) -> str:
    """Extract the filename stem (without extension) from a file path."""
    return Path(file_path).stem


def find_docs_root(path: Path) -> Path | None:
    """Walk up from a path to find the `docs/` directory."""
    for parent in [path] + list(path.parents):
        if parent.name == "docs" and parent.is_dir():
            return parent
    docs_candidate = path / "docs"
    if docs_candidate.is_dir():
        return docs_candidate
    return None


def folder_path_from_file(file_path: str) -> str:
    """Determine the folder path relative to docs/."""
    path = Path(file_path).resolve()
    parts = path.parts

    try:
        docs_idx = parts.index("docs")
    except ValueError:
        return str(path.parent.name)

    folder_parts = parts[docs_idx + 1:-1]
    return "/".join(folder_parts)


def generate_permalink(file_path: str) -> str | None:
    """Generate the permalink URL for a Zensical doc file."""
    path_obj = Path(file_path)

    if not path_obj.exists():
        return None

    filename = filename_from_path(file_path)
    folder_path = folder_path_from_file(file_path)

    base_url = "https://help.cyberbiz.io"
    if folder_path:
        return f"{base_url}/{folder_path}/{filename}"
    else:
        return f"{base_url}/{filename}"


def collect_md_files(targets: list[str]) -> list[str]:
    """Resolve files, directories, and globs into a flat list of .md files."""
    files: list[str] = []
    errors: list[str] = []

    for target in targets:
        p = Path(target)

        if not p.exists():
            errors.append(f"Path not found: {target}")
            continue

        if p.is_file():
            if p.suffix == ".md":
                files.append(str(p))
            else:
                errors.append(f"Not a markdown file: {target}")
        elif p.is_dir():
            for md_file in sorted(p.rglob("*.md")):
                files.append(str(md_file))

    if errors:
        for err in errors:
            print(err, file=sys.stderr)

    return sorted(set(files))


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_permalink.py <file-or-dir> [file-or-dir ...]", file=sys.stderr)
        sys.exit(1)

    targets = sys.argv[1:]
    files = collect_md_files(targets)

    if not files:
        print("No markdown files found to process.", file=sys.stderr)
        sys.exit(1)

    results = []
    exit_code = 0

    for file_path in files:
        result = generate_permalink(file_path)
        if result is None:
            results.append((file_path, "ERROR: file not found or unreadable"))
            exit_code = 1
        else:
            results.append((file_path, result))

    for file_path, permalink in results:
        print(f"{file_path} -> {permalink}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
