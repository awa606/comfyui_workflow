from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageOps


PROJECT_DIR = Path(__file__).resolve().parents[1]
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
DEFAULT_CAPTION = "linwei woman, black-rimmed glasses, long dark brown hair"


def resolve_project_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_DIR / path
    return path.resolve()


def iter_images(selected_dir: Path) -> list[Path]:
    if not selected_dir.exists():
        return []
    return sorted(
        path
        for path in selected_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def save_as_png(source: Path, target: Path) -> None:
    if source.suffix.lower() == ".png":
        shutil.copy2(source, target)
        return

    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGB")
        image.save(target, "PNG")


def prepare_dataset(
    selected_dir: Path,
    output_dir: Path,
    caption: str,
    prefix: str,
    overwrite: bool,
) -> int:
    images = iter_images(selected_dir)
    if not images:
        raise ValueError(f"No selected images found in: {selected_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    for index, source in enumerate(images, start=1):
        stem = f"{prefix}_{index:04d}"
        image_target = output_dir / f"{stem}.png"
        caption_target = output_dir / f"{stem}.txt"

        if not overwrite and (image_target.exists() or caption_target.exists()):
            raise FileExistsError(
                f"Target already exists: {image_target} or {caption_target}. "
                "Use --overwrite to replace generated files."
            )

        save_as_png(source, image_target)
        caption_target.write_text(caption + "\n", encoding="utf-8")

    return len(images)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare selected Linwei images and captions for LoRA training."
    )
    parser.add_argument(
        "--selected-dir",
        default="datasets/linwei_character_selected",
        help="Directory containing manually selected images.",
    )
    parser.add_argument(
        "--output-dir",
        default="datasets/linwei_character_captions",
        help="Training directory for renamed PNG images and matching .txt captions.",
    )
    parser.add_argument(
        "--caption",
        default=DEFAULT_CAPTION,
        help="Caption text written to every .txt file.",
    )
    parser.add_argument(
        "--prefix",
        default="linwei",
        help="Output filename prefix. Defaults to linwei.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing generated image/caption files in the output directory.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    selected_dir = resolve_project_path(args.selected_dir)
    output_dir = resolve_project_path(args.output_dir)

    try:
        count = prepare_dataset(
            selected_dir=selected_dir,
            output_dir=output_dir,
            caption=args.caption,
            prefix=args.prefix,
            overwrite=args.overwrite,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Prepared {count} image/caption pair(s): {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
