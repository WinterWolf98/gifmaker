#!/usr/bin/env python3

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def check_binary(name: str) -> None:
    if shutil.which(name) is None:
        print(f"Error: '{name}' not found in PATH.")
        print("Install with Homebrew:")
        print("  brew install ffmpeg")
        sys.exit(1)


def run_cmd(cmd: list[str]) -> None:
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        print("Command failed:")
        print(" ".join(cmd))
        sys.exit(exc.returncode)


def build_filters(speed: float, fps: int, width: int | None) -> tuple[str, str]:
    scale_filter = "scale=iw:-1:flags=lanczos" if width is None else f"scale={width}:-1:flags=lanczos"

    # speed > 1.0 means faster playback, speed < 1.0 means slower playback
    # setpts is inverted: smaller PTS = faster playback
    base_filter = f"setpts=PTS/{speed},{scale_filter},fps={fps}"
    palette_filter = f"{base_filter},palettegen=stats_mode=full"
    use_palette_filter = f"{base_filter}[x];[x][1:v]paletteuse=dither=sierra2_4a"
    return palette_filter, use_palette_filter


def make_gif(input_file: Path, output_file: Path, speed: float, fps: int, width: int | None, loop: int) -> None:
    palette_file = output_file.with_suffix(".palette.png")

    palette_filter, use_palette_filter = build_filters(speed, fps, width)

    run_cmd([
        "ffmpeg",
        "-y",
        "-i",
        str(input_file),
        "-vf",
        palette_filter,
        str(palette_file),
    ])

    run_cmd([
        "ffmpeg",
        "-y",
        "-i",
        str(input_file),
        "-i",
        str(palette_file),
        "-filter_complex",
        use_palette_filter,
        "-loop",
        str(loop),
        str(output_file),
    ])

    if palette_file.exists():
        palette_file.unlink()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="High-quality GIF maker using ffmpeg (macOS-friendly)."
    )
    parser.add_argument("input", type=Path, help="Input video file")
    parser.add_argument("output", type=Path, help="Output GIF file")
    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Playback speed multiplier (e.g. 2.0 faster, 0.5 slower). Default: 1.0",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="Frames per second in the output GIF. Default: 30",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=None,
        help="Output width in pixels. Default keeps source width.",
    )
    parser.add_argument(
        "--loop",
        type=int,
        default=0,
        help="Loop count (0 = infinite). Default: 0",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if not args.input.exists():
        print(f"Error: input file not found: {args.input}")
        sys.exit(1)
    if args.speed <= 0:
        print("Error: --speed must be > 0")
        sys.exit(1)
    if args.fps <= 0:
        print("Error: --fps must be > 0")
        sys.exit(1)
    if args.width is not None and args.width <= 0:
        print("Error: --width must be > 0")
        sys.exit(1)
    if args.loop < 0:
        print("Error: --loop must be >= 0")
        sys.exit(1)


def main() -> None:
    args = parse_args()
    validate_args(args)

    check_binary("ffmpeg")

    make_gif(
        input_file=args.input,
        output_file=args.output,
        speed=args.speed,
        fps=args.fps,
        width=args.width,
        loop=args.loop,
    )

    print(f"GIF created: {args.output}")


if __name__ == "__main__":
    main()
