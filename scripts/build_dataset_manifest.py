from __future__ import annotations

import argparse
import csv
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET_DIR = PROJECT_DIR / "datasets" / "linwei"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
FIELDNAMES = [
    "file_path",
    "category",
    "has_face",
    "face_quality",
    "body_view",
    "outfit",
    "hairstyle",
    "makeup",
    "use_for_identity_lora",
    "use_for_outfit_ref",
    "use_for_pose_ref",
    "notes",
]


DEFAULTS_BY_CATEGORY = {
    "selected_identity_faces": {
        "has_face": "yes",
        "face_quality": "pending",
        "body_view": "face",
        "use_for_identity_lora": "candidate",
    },
    "selected_upper_body": {
        "has_face": "yes",
        "face_quality": "pending",
        "body_view": "upper_body",
        "use_for_identity_lora": "candidate",
        "use_for_outfit_ref": "candidate",
    },
    "selected_full_body": {
        "has_face": "unknown",
        "face_quality": "pending",
        "body_view": "full_body",
        "use_for_identity_lora": "review",
        "use_for_outfit_ref": "candidate",
        "use_for_pose_ref": "candidate",
    },
    "outfit_refs": {
        "has_face": "unknown",
        "body_view": "outfit_reference",
        "use_for_outfit_ref": "yes",
    },
    "hairstyle_refs": {
        "has_face": "unknown",
        "hairstyle": "review",
    },
    "makeup_refs": {
        "has_face": "yes",
        "makeup": "review",
    },
    "shoes_accessories": {
        "body_view": "detail",
        "use_for_outfit_ref": "yes",
    },
    "pose_refs": {
        "body_view": "pose_reference",
        "use_for_pose_ref": "yes",
    },
    "scene_refs": {
        "body_view": "scene_reference",
    },
    "rejected": {
        "use_for_identity_lora": "no",
        "use_for_outfit_ref": "no",
        "use_for_pose_ref": "no",
    },
}


def resolve_project_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_DIR / path
    return path.resolve()


def category_for(path: Path, dataset_dir: Path) -> str:
    try:
        relative = path.relative_to(dataset_dir)
    except ValueError:
        return "unknown"
    return relative.parts[0] if len(relative.parts) > 1 else "root"


def empty_row() -> dict[str, str]:
    return {field: "" for field in FIELDNAMES}


def row_for(path: Path, dataset_dir: Path) -> dict[str, str]:
    category = category_for(path, dataset_dir)
    row = empty_row()
    row["file_path"] = str(path.relative_to(PROJECT_DIR)).replace("\\", "/")
    row["category"] = category

    defaults = DEFAULTS_BY_CATEGORY.get(category, {})
    for key, value in defaults.items():
        row[key] = value

    return row


def iter_images(dataset_dir: Path, manifest_path: Path) -> list[Path]:
    if not dataset_dir.exists():
        return []

    manifest_path = manifest_path.resolve()
    images: list[Path] = []
    for path in sorted(dataset_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.resolve() == manifest_path:
            continue
        if path.suffix.lower() in IMAGE_EXTENSIONS:
            images.append(path)
    return images


def write_manifest(dataset_dir: Path, output_path: Path) -> int:
    images = iter_images(dataset_dir, output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for image_path in images:
            writer.writerow(row_for(image_path, dataset_dir))

    return len(images)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a CSV manifest for the Linwei character dataset."
    )
    parser.add_argument(
        "--dataset-dir",
        default=str(DEFAULT_DATASET_DIR.relative_to(PROJECT_DIR)),
        help="Dataset root to scan. Defaults to datasets/linwei.",
    )
    parser.add_argument(
        "--output",
        default="datasets/linwei/metadata/dataset_manifest.csv",
        help="Manifest CSV output path.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    dataset_dir = resolve_project_path(args.dataset_dir)
    output_path = resolve_project_path(args.output)

    count = write_manifest(dataset_dir, output_path)
    print(f"Wrote manifest: {output_path}")
    print(f"Images included: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
