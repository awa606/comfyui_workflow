from __future__ import annotations

import argparse
import csv
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_ROLE = "role_001"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
FIELDNAMES = [
    "file_path",
    "category",
    "has_face",
    "face_quality",
    "body_view",
    "outfit_id",
    "hairstyle",
    "makeup",
    "pose_type",
    "scene",
    "use_for_faceid",
    "use_for_lora",
    "use_for_outfit_ref",
    "use_for_pose_ref",
    "notes",
]


DEFAULTS_BY_CATEGORY = {
    "identity_faces": {"has_face": "yes", "use_for_lora": "candidate"},
    "upper_body": {"has_face": "yes", "body_view": "upper_body", "use_for_lora": "candidate"},
    "full_body": {"body_view": "full_body", "use_for_outfit_ref": "candidate", "use_for_pose_ref": "candidate"},
    "body_reference": {"body_view": "body_reference"},
    "selected_for_faceid": {"has_face": "yes", "use_for_faceid": "candidate"},
    "selected_for_lora": {"has_face": "yes", "use_for_lora": "candidate"},
    "hairstyles": {"hairstyle": "candidate"},
    "makeup": {"makeup": "candidate"},
    "shoes_accessories": {"use_for_outfit_ref": "candidate"},
    "pose_refs": {"use_for_pose_ref": "candidate"},
    "scene_refs": {"scene": "candidate"},
    "rejected": {"use_for_faceid": "no", "use_for_lora": "no"},
}


def resolve_project_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_DIR / path
    return path.resolve()


def category_for(path: Path, role_dir: Path) -> str:
    try:
        relative = path.relative_to(role_dir)
    except ValueError:
        return "unknown"
    return relative.parts[0] if len(relative.parts) > 1 else "root"


def outfit_id_for(path: Path, role_dir: Path) -> str:
    try:
        parts = path.relative_to(role_dir).parts
    except ValueError:
        return ""
    if len(parts) >= 2 and parts[0] == "outfits":
        return parts[1]
    return ""


def iter_images(role_dir: Path, output_path: Path) -> list[Path]:
    if not role_dir.exists():
        return []
    output_path = output_path.resolve()
    return sorted(
        path
        for path in role_dir.rglob("*")
        if path.is_file()
        and path.resolve() != output_path
        and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def row_for(path: Path, role_dir: Path) -> dict[str, str]:
    category = category_for(path, role_dir)
    row = {field: "" for field in FIELDNAMES}
    row["file_path"] = str(path.relative_to(PROJECT_DIR)).replace("\\", "/")
    row["category"] = category
    row["outfit_id"] = outfit_id_for(path, role_dir)

    for key, value in DEFAULTS_BY_CATEGORY.get(category, {}).items():
        row[key] = value

    return row


def write_manifest(role_dir: Path, output_path: Path) -> int:
    images = iter_images(role_dir, output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for image_path in images:
            writer.writerow(row_for(image_path, role_dir))
    return len(images)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a CSV manifest for one character role.")
    parser.add_argument(
        "--role",
        default=DEFAULT_ROLE,
        help="Role id under characters/, for example role_001.",
    )
    parser.add_argument(
        "--role-dir",
        default=None,
        help="Optional role directory. Defaults to characters/<role>.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional CSV path. Defaults to characters/<role>/metadata/manifest.csv.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    role_dir = resolve_project_path(args.role_dir) if args.role_dir else PROJECT_DIR / "characters" / args.role
    output_path = resolve_project_path(args.output) if args.output else role_dir / "metadata" / "manifest.csv"
    count = write_manifest(role_dir, output_path)
    print(f"Wrote manifest: {output_path}")
    print(f"Images included: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
