from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageOps


PROJECT_DIR = Path(__file__).resolve().parents[1]
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}


def resolve_project_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_DIR / path
    return path.resolve()


def iter_images(paths: Iterable[str]) -> list[Path]:
    images: list[Path] = []
    for value in paths:
        path = resolve_project_path(value)
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            images.append(path)
        elif path.is_dir():
            images.extend(
                sorted(
                    p
                    for p in path.rglob("*")
                    if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
                )
            )
    return images


def make_thumb(path: Path, size: int) -> Image.Image:
    with Image.open(path) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        image.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (size, size), "white")
        x = (size - image.width) // 2
        y = (size - image.height) // 2
        canvas.paste(image, (x, y))
        return canvas


def draw_label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str) -> None:
    draw.text(xy, text, fill=(20, 20, 20))


def build_contact_sheet(
    refs: list[Path],
    generated: list[Path],
    output_path: Path,
    thumb_size: int,
    columns: int,
) -> None:
    if not refs and not generated:
        raise ValueError("No images found in refs or generated inputs")

    items = [("REF", p) for p in refs] + [("GEN", p) for p in generated]
    label_height = 42
    cell_width = thumb_size
    cell_height = thumb_size + label_height
    rows = (len(items) + columns - 1) // columns

    sheet = Image.new("RGB", (columns * cell_width, rows * cell_height), "white")
    draw = ImageDraw.Draw(sheet)

    for index, (kind, path) in enumerate(items):
        row = index // columns
        col = index % columns
        x = col * cell_width
        y = row * cell_height

        thumb = make_thumb(path, thumb_size)
        sheet.paste(thumb, (x, y))

        relative = path
        try:
            relative = path.relative_to(PROJECT_DIR)
        except ValueError:
            pass
        name = str(relative).replace("\\", "/")
        if len(name) > 36:
            name = "..." + name[-33:]
        draw_label(draw, (x + 6, y + thumb_size + 4), f"{kind}: {name}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a contact sheet comparing reference and generated images."
    )
    parser.add_argument(
        "--refs",
        nargs="+",
        default=["character_refs", "face_crops", "body_refs", "pose_refs"],
        help="Reference image files or directories.",
    )
    parser.add_argument(
        "--generated",
        nargs="+",
        default=["outputs"],
        help="Generated image files or directories.",
    )
    parser.add_argument(
        "--output",
        default="outputs/contact_sheet.png",
        help="Output contact sheet path.",
    )
    parser.add_argument("--thumb-size", type=int, default=256)
    parser.add_argument("--columns", type=int, default=4)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.thumb_size < 64:
        raise SystemExit("ERROR: --thumb-size must be at least 64")
    if args.columns < 1:
        raise SystemExit("ERROR: --columns must be at least 1")

    refs = iter_images(args.refs)
    generated = iter_images(args.generated)
    output_path = resolve_project_path(args.output)

    build_contact_sheet(refs, generated, output_path, args.thumb_size, args.columns)
    print(f"Wrote contact sheet: {output_path}")
    print(f"Reference images: {len(refs)}")
    print(f"Generated images: {len(generated)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
