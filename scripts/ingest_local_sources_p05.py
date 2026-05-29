from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]

IMAGE_EXTENSIONS = {
    ".bmp",
    ".jpeg",
    ".jpg",
    ".png",
    ".tif",
    ".tiff",
    ".webp",
}
VIDEO_EXTENSIONS = {
    ".avi",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp4",
    ".webm",
    ".wmv",
}
SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS

DEFAULT_EXCLUDE_KEYWORDS = [
    "explicit",
    "R18",
    "r18",
    "03_explicit",
    "03_explicit_action",
    "05_style_ryota",
    r"styles\explicit",
    "VIP",
    "全裸",
    "插入",
    "扩张",
    "ahegao",
    "捆绑",
]

OUTPUT_FIELDS = [
    "asset_id",
    "source_root",
    "source_path",
    "source_person_id",
    "source_type",
    "ext",
    "file_size",
    "parent_tags",
    "excluded",
    "exclude_reason",
    "notes",
]

GENERIC_PARENT_NAMES = {
    "image",
    "images",
    "img",
    "raw",
    "ref",
    "refs",
    "reference",
    "reference_images",
    "training_data",
}


def resolve_project_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_DIR / path
    return path.resolve()


def normalize_for_match(value: str) -> str:
    return value.replace("/", "\\").casefold()


def normalize_keywords(values: list[str]) -> list[str]:
    return [normalize_for_match(value) for value in values if value.strip()]


def find_exclude_keyword(value: str, keywords: list[str]) -> str:
    normalized = normalize_for_match(value)
    for keyword in keywords:
        if keyword in normalized:
            return keyword
    return ""


def make_asset_id(source_root: Path, source_path: Path) -> str:
    digest = hashlib.sha1(
        f"{source_root.as_posix()}::{source_path.as_posix()}".encode("utf-8")
    ).hexdigest()
    return f"p05_{digest[:16]}"


def safe_label(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", value).strip(" .")
    return cleaned or "unknown"


def infer_source_person_id(source_root: Path, source_path: Path) -> str:
    try:
        relative_parent = source_path.relative_to(source_root).parent
    except ValueError:
        relative_parent = source_path.parent

    for part in relative_parent.parts:
        if part and part.casefold() not in GENERIC_PARENT_NAMES:
            return safe_label(part)

    if relative_parent.parts:
        return safe_label(relative_parent.parts[-1])
    return safe_label(source_root.name)


def parent_tags(source_root: Path, source_path: Path) -> str:
    try:
        relative_parent = source_path.relative_to(source_root).parent
    except ValueError:
        relative_parent = source_path.parent
    return "|".join(relative_parent.parts)


def classify_source_type(ext: str) -> str:
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    return "other"


def iter_media_rows(source_root: Path, keywords: list[str]) -> tuple[list[dict[str, str]], int]:
    rows: list[dict[str, str]] = []
    pruned_dirs = 0

    for dirpath, dirnames, filenames in os.walk(source_root):
        current_dir = Path(dirpath)
        kept_dirnames: list[str] = []
        for dirname in dirnames:
            candidate = current_dir / dirname
            try:
                candidate_rel = candidate.relative_to(source_root).as_posix()
            except ValueError:
                candidate_rel = candidate.as_posix()
            if find_exclude_keyword(candidate_rel, keywords):
                pruned_dirs += 1
                continue
            kept_dirnames.append(dirname)
        dirnames[:] = kept_dirnames

        for filename in filenames:
            path = current_dir / filename
            ext = path.suffix.lower()
            if ext not in SUPPORTED_EXTENSIONS:
                continue

            try:
                relative_path = path.relative_to(source_root).as_posix()
            except ValueError:
                relative_path = path.as_posix()
            exclude_reason = find_exclude_keyword(relative_path, keywords)
            excluded = "yes" if exclude_reason else "no"

            try:
                file_size = str(path.stat().st_size)
            except OSError:
                file_size = ""

            rows.append(
                {
                    "asset_id": make_asset_id(source_root, path),
                    "source_root": str(source_root),
                    "source_path": str(path),
                    "source_person_id": infer_source_person_id(source_root, path),
                    "source_type": classify_source_type(ext),
                    "ext": ext,
                    "file_size": file_size,
                    "parent_tags": parent_tags(source_root, path),
                    "excluded": excluded,
                    "exclude_reason": exclude_reason,
                    "notes": (
                        "path keyword matched; keep out of safe queues"
                        if excluded == "yes"
                        else "inventory only; no copy, frame extraction, or crop"
                    ),
                }
            )

    rows.sort(key=lambda row: (row["source_root"], row["source_path"]))
    return rows, pruned_dirs


def write_inventory(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a P0.5 local media inventory from messy source folders. "
            "This only writes metadata and never copies, deletes, moves, or extracts files."
        )
    )
    parser.add_argument(
        "--source-root",
        action="append",
        required=True,
        help="Local source directory to scan. Repeat this option for multiple roots.",
    )
    parser.add_argument(
        "--exclude-keywords",
        nargs="+",
        default=DEFAULT_EXCLUDE_KEYWORDS,
        help="Path keywords to exclude or prune. Defaults to the P0.5 safety list.",
    )
    parser.add_argument(
        "--output",
        default="metadata/p05_local_source_inventory.csv",
        help="Inventory CSV path. Defaults to metadata/p05_local_source_inventory.csv.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    keywords = normalize_keywords(args.exclude_keywords)
    output_path = resolve_project_path(args.output)

    all_rows: list[dict[str, str]] = []
    total_pruned_dirs = 0
    for raw_root in args.source_root:
        source_root = Path(raw_root).expanduser().resolve()
        if not source_root.exists():
            raise SystemExit(f"ERROR: source root does not exist: {source_root}")
        if not source_root.is_dir():
            raise SystemExit(f"ERROR: source root is not a directory: {source_root}")

        rows, pruned_dirs = iter_media_rows(source_root, keywords)
        all_rows.extend(rows)
        total_pruned_dirs += pruned_dirs

    write_inventory(all_rows, output_path)

    safe_count = sum(1 for row in all_rows if row["excluded"] == "no")
    excluded_count = len(all_rows) - safe_count
    image_count = sum(1 for row in all_rows if row["source_type"] == "image")
    video_count = sum(1 for row in all_rows if row["source_type"] == "video")

    print(f"Wrote inventory: {output_path}")
    print(f"Rows: {len(all_rows)}")
    print(f"Safe rows: {safe_count}")
    print(f"Excluded rows: {excluded_count}")
    print(f"Images: {image_count}")
    print(f"Videos: {video_count}")
    print(f"Pruned directories: {total_pruned_dirs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
