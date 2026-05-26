from __future__ import annotations

import argparse
import sys
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont, ImageOps


PROJECT_DIR = Path(__file__).resolve().parents[1]
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}


def resolve_project_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_DIR / path
    return path.resolve()


def iter_images(input_dir: Path, output_path: Path) -> list[Path]:
    if not input_dir.exists():
        return []

    output_path = output_path.resolve()
    images: list[Path] = []
    for path in sorted(input_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        if path.resolve() == output_path:
            continue
        if "contact_sheet" in path.stem.lower():
            continue
        images.append(path)
    return images


def make_thumbnail(path: Path, size: int) -> Image.Image:
    with Image.open(path) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        image.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (size, size), "white")
        x = (size - image.width) // 2
        y = (size - image.height) // 2
        canvas.paste(image, (x, y))
        return canvas


def load_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def label_for(path: Path, input_dir: Path) -> str:
    try:
        label = path.relative_to(input_dir)
    except ValueError:
        label = path
    return str(label).replace("\\", "/")


def draw_wrapped_label(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    max_chars: int,
    max_lines: int,
) -> None:
    lines = wrap(text, width=max_chars)[:max_lines]
    if not lines:
        return

    line_height = 14
    x, y = xy
    for offset, line in enumerate(lines):
        draw.text((x, y + offset * line_height), line, fill=(25, 25, 25), font=font)


def build_contact_sheet(
    images: list[Path],
    input_dir: Path,
    output_path: Path,
    thumb_size: int,
    columns: int,
    label_height: int,
) -> None:
    if not images:
        raise ValueError(f"No model test images found in: {input_dir}")

    rows = (len(images) + columns - 1) // columns
    cell_width = thumb_size
    cell_height = thumb_size + label_height
    sheet = Image.new("RGB", (columns * cell_width, rows * cell_height), "white")
    draw = ImageDraw.Draw(sheet)
    font = load_font(12)

    for index, path in enumerate(images):
        row = index // columns
        col = index % columns
        x = col * cell_width
        y = row * cell_height

        thumb = make_thumbnail(path, thumb_size)
        sheet.paste(thumb, (x, y))

        label = label_for(path, input_dir)
        draw_wrapped_label(
            draw=draw,
            xy=(x + 6, y + thumb_size + 6),
            text=label,
            font=font,
            max_chars=max(18, thumb_size // 8),
            max_lines=max(1, label_height // 14),
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a contact sheet from model_tests outputs."
    )
    parser.add_argument(
        "--input-dir",
        default="model_tests",
        help="Directory containing model test outputs. Defaults to model_tests.",
    )
    parser.add_argument(
        "--output",
        default="model_tests/model_contact_sheet.png",
        help="Output contact sheet path.",
    )
    parser.add_argument("--thumb-size", type=int, default=256)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--label-height", type=int, default=56)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.thumb_size < 64:
        raise SystemExit("ERROR: --thumb-size must be at least 64")
    if args.columns < 1:
        raise SystemExit("ERROR: --columns must be at least 1")
    if args.label_height < 20:
        raise SystemExit("ERROR: --label-height must be at least 20")

    input_dir = resolve_project_path(args.input_dir)
    output_path = resolve_project_path(args.output)
    images = iter_images(input_dir, output_path)

    try:
        build_contact_sheet(
            images=images,
            input_dir=input_dir,
            output_path=output_path,
            thumb_size=args.thumb_size,
            columns=args.columns,
            label_height=args.label_height,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote model contact sheet: {output_path}")
    print(f"Images included: {len(images)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
