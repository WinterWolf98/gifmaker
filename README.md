# GIF Maker (macOS, ffmpeg)

A high-quality GIF maker CLI for macOS using `ffmpeg` two-pass palette workflow (`palettegen` + `paletteuse`).

## Features

- High-quality GIF generation (quality-first, not size-first)
- Speed control for the output GIF
- Adjustable FPS and optional output width

## Prerequisites (macOS)

```bash
brew install ffmpeg
```

## Usage

```bash
python3 gifmaker.py input.mp4 output.gif --speed 1.0
```

### Speed examples

- Faster GIF (2x):

```bash
python3 gifmaker.py input.mp4 output-fast.gif --speed 2.0
```

- Slower GIF (0.5x):

```bash
python3 gifmaker.py input.mp4 output-slow.gif --speed 0.5
```

### Optional quality controls

- Higher smoothness (more frames):

```bash
python3 gifmaker.py input.mp4 output.gif --fps 40
```

- Keep quality while resizing width:

```bash
python3 gifmaker.py input.mp4 output.gif --width 900
```

## Arguments

- `input`: input video file path
- `output`: output GIF path
- `--speed`: playback speed multiplier (`>1` faster, `<1` slower), default `1.0`
- `--fps`: output frames per second, default `30`
- `--width`: output width in px, default is source width
- `--loop`: loop count (`0` = infinite), default `0`
