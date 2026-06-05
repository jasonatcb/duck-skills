#!/usr/bin/env python3
"""
Convert MOV (or other video) files to optimized GIFs using ffmpeg.

Smart defaults:
  fps=15, palettegen stats_mode=diff, paletteuse dither=bayer

Usage:
  mov-to-gif.py input.mov
  mov-to-gif.py input.mov -o output.gif [options]
  mov-to-gif.py "*.mov" [options]
  mov-to-gif.py /path/to/folder [options]
  mov-to-gif.py input.mov --dry-run
"""

import argparse
import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path


def check_ffmpeg():
    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg not found. Install it with 'brew install ffmpeg'.", file=sys.stderr)
        sys.exit(1)


def build_filter(fps, scale, dither, stats_mode):
    """Build -filter_complex argument for palette-based GIF encoding."""
    video = f"[0:v] fps={fps}"
    if scale:
        video += f",scale={scale}:-1:flags=lanczos"
    video += ",split [a][b]"
    parts = [video]
    parts.append(f"[a] palettegen=stats_mode={stats_mode} [p]")
    paletteuse = "[b][p] paletteuse"
    if dither:
        paletteuse += "=dither=bayer"
    parts.append(paletteuse)
    return ";".join(parts)


def resolve_inputs(input_arg):
    path = Path(input_arg)
    if path.is_dir():
        files = sorted(path.glob("*.mov")) + sorted(path.glob("*.MOV"))
        if not files:
            files = sorted(path.glob("*.*"))
        return [f for f in files if f.suffix.lower() in (".mov", ".mp4", ".avi", ".mkv", ".webm", ".m4v")]
    if path.is_file():
        return [path]
    matched = glob.glob(input_arg)
    if matched:
        return sorted(Path(f) for f in matched if Path(f).suffix.lower() in (".mov", ".mp4", ".avi", ".mkv", ".webm", ".m4v"))
    print(f"Error: no matching files for '{input_arg}'", file=sys.stderr)
    sys.exit(1)


def convert_file(input_path, output_path, fps, scale, ss, to, duration, loops, dither, stats_mode, overwrite):
    cmd = ["ffmpeg"]
    if overwrite:
        cmd.append("-y")
    if ss:
        cmd.extend(["-ss", ss])
    cmd.extend(["-i", str(input_path)])
    if to:
        cmd.extend(["-to", to])
    if duration:
        cmd.extend(["-t", str(duration)])
    cmd.extend(["-filter_complex", build_filter(fps, scale, dither, stats_mode)])
    if loops is not None:
        cmd.extend(["-loop", str(loops)])
    cmd.append(str(output_path))
    return cmd


def get_output_path(input_path, output_arg, files_count):
    if files_count == 1 and output_arg:
        return Path(output_arg)
    return input_path.with_suffix(".gif")


def main():
    check_ffmpeg()

    parser = argparse.ArgumentParser(
        description="Convert video files to optimized GIFs using ffmpeg",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  mov-to-gif.py demo.mov\n"
            "  mov-to-gif.py demo.mov -o demo.gif --fps 10 --scale 480\n"
            "  mov-to-gif.py demo.mov --ss 00:00:05 --to 00:00:10\n"
            "  mov-to-gif.py *.mov --quality small\n"
            "  mov-to-gif.py ./recordings/\n"
            "  mov-to-gif.py demo.mov --dry-run"
        ),
    )
    parser.add_argument("input", help="Input file, glob pattern, or directory")
    parser.add_argument("-o", "--output", help="Output GIF path (single file only)")
    parser.add_argument("--fps", type=int, default=15, help="Frames per second (default: 15)")
    parser.add_argument("--scale", type=int, help="Output width in pixels (height auto-scales)")
    parser.add_argument("--ss", help="Start time offset (e.g. 00:00:05 or 30 for 30s)")
    parser.add_argument("--to", help="Stop at time (e.g. 00:00:10)")
    parser.add_argument("-t", "--duration", type=float, help="Duration in seconds")
    parser.add_argument("--loops", type=int, default=0, help="Loop count (0=infinite, default: 0)")
    parser.add_argument("-q", "--quality", choices=["best", "balanced", "small"], default="best",
                        help="Quality preset (default: best)")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Print commands without running")
    parser.add_argument("-y", "--overwrite", action="store_true", help="Overwrite without asking")

    args = parser.parse_args()

    dither = True
    stats_mode = "diff"
    if args.quality == "balanced":
        dither = False
    elif args.quality == "small":
        dither = False
        stats_mode = "full"
        if args.fps == 15:
            args.fps = 10

    files = resolve_inputs(args.input)

    if args.output and len(files) > 1:
        print("Warning: --output ignored (multiple files)", file=sys.stderr)

    for f in files:
        out = get_output_path(f, args.output, len(files))
        cmd = convert_file(f, out, args.fps, args.scale, args.ss, args.to,
                           args.duration, args.loops, dither, stats_mode, args.overwrite)

        label = "[DRY RUN]" if args.dry_run else "[RUN]"
        print(f"{label} {f.name} -> {out.name}")

        if args.scale:
            print(f"       scale: {args.scale}px wide")
        print(f"       fps: {args.fps}, quality: {args.quality}, loops: {args.loops}")
        if args.ss:
            print(f"       trim: start={args.ss}", end="")
            if args.to:
                print(f" end={args.to}", end="")
            if args.duration:
                print(f" duration={args.duration}s", end="")
            print()

        if args.dry_run:
            print(f"  {' '.join(cmd)}")
        else:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"  Error: {result.stderr.strip()}", file=sys.stderr)
            else:
                size_kb = os.path.getsize(out) / 1024
                print(f"  Done: {size_kb:.1f} KB")

    if len(files) > 1 and not args.dry_run:
        total = sum(os.path.getsize(f.with_suffix(".gif")) / 1024 for f in files if f.with_suffix(".gif").exists())
        print(f"\nConverted {len(files)} files, total {total:.1f} KB")


if __name__ == "__main__":
    main()
