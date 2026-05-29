from __future__ import annotations

import argparse
import csv
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
    "image_path",
    "source_person_id",
    "image_role",
    "recommended_model",
    "caption_status",
    "notes",
]

MODEL_BY_ROLE = {
    "quick_screen": "gemma4:e2b",
    "main_caption": "qwen3-vl:8b",
    "style_detail": "gemma4:e4b-it-q4_K_M",
    "face_crop_review": "gemma4:e2b",
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


def has_excluded_keyword(path: Path, keywords: list[str]) -> bool:
    normalized = normalize_for_match(str(path))
    return any(keyword in normalized for keyword in keywords)


def truthy(value: str | None) -> bool:
    return (value or "").strip().casefold() in {"1", "true", "yes", "y"}


def safe_person_id(value: str | None, image_path: Path) -> str:
    raw = (value or "").strip()
    if raw:
        return raw
    return image_path.parent.name or "unknown"


def add_row(
    rows: list[dict[str, str]],
    image_path: Path,
    source_person_id: str,
    image_role: str,
    notes: str,
) -> None:
    rows.append(
        {
            "image_path": str(image_path),
            "source_person_id": source_person_id,
            "image_role": image_role,
            "recommended_model": MODEL_BY_ROLE[image_role],
            "caption_status": "queued",
            "notes": notes,
        }
    )


def selected_passes(raw_passes: list[str]) -> set[str]:
    passes = {item.strip().casefold() for item in raw_passes}
    if "all" in passes:
        return {"quick", "main", "style"}
    return passes


def load_inventory_rows(
    inventory_path: Path,
    keywords: list[str],
    passes: set[str],
) -> list[dict[str, str]]:
    if not inventory_path.exists():
        return []

    rows: list[dict[str, str]] = []
    with inventory_path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if truthy(row.get("excluded")):
                continue

            source_type = (row.get("source_type") or "").strip().casefold()
            if source_type and source_type != "image":
                continue

            raw_path = (row.get("source_path") or "").strip()
            if not raw_path:
                continue
            image_path = Path(raw_path).expanduser().resolve()
            if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            if not image_path.exists() or not image_path.is_file():
                continue
            if has_excluded_keyword(image_path, keywords):
                continue

            person_id = safe_person_id(row.get("source_person_id"), image_path)
            if "quick" in passes:
                add_row(
                    rows,
                    image_path,
                    person_id,
                    "quick_screen",
                    "quick safety and relevance pass before expensive captioning",
                )
            if "main" in passes:
                add_row(
                    rows,
                    image_path,
                    person_id,
                    "main_caption",
                    "primary descriptive caption pass",
                )
            if "style" in passes:
                add_row(
                    rows,
                    image_path,
                    person_id,
                    "style_detail",
                    "detail pass for clothing, rendering, lighting, and style tags",
                )

    return rows


def load_face_crop_rows(
    face_crops_path: Path,
    keywords: list[str],
    passes: set[str],
) -> list[dict[str, str]]:
    if not face_crops_path.exists() or "quick" not in passes:
        return []

    rows: list[dict[str, str]] = []
    with face_crops_path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            raw_path = (row.get("crop_path") or "").strip()
            if not raw_path:
                continue
            image_path = Path(raw_path).expanduser().resolve()
            if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            if not image_path.exists() or not image_path.is_file():
                continue
            if has_excluded_keyword(image_path, keywords):
                continue

            use_for_faceid = (row.get("use_for_faceid") or "").strip()
            person_id = safe_person_id(row.get("source_person_id"), image_path)
            add_row(
                rows,
                image_path,
                person_id,
                "face_crop_review",
                f"quick review of generated face crop; use_for_faceid={use_for_faceid or 'unset'}",
            )

    return rows


def dedupe_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    deduped: list[dict[str, str]] = []
    for row in rows:
        key = (row["image_path"], row["image_role"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    deduped.sort(key=lambda row: (row["source_person_id"], row["image_path"], row["image_role"]))
    return deduped


def write_queue(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare a P0.5 safe caption queue from the local source inventory and "
            "face crop metadata. This only writes a CSV queue."
        )
    )
    parser.add_argument(
        "--inventory",
        default="metadata/p05_local_source_inventory.csv",
        help="P0.5 local source inventory CSV.",
    )
    parser.add_argument(
        "--face-crops",
        default="metadata/p05_face_crops.csv",
        help="P0.5 face crop metadata CSV.",
    )
    parser.add_argument(
        "--output",
        default="metadata/p05_caption_queue.csv",
        help="Output queue CSV. Defaults to metadata/p05_caption_queue.csv.",
    )
    parser.add_argument(
        "--caption-passes",
        nargs="+",
        choices=["quick", "main", "style", "all"],
        default=["quick", "main", "style"],
        help=(
            "Caption passes to enqueue. quick=gemma4:e2b, main=qwen3-vl:8b, "
            "style=gemma4:e4b-it-q4_K_M."
        ),
    )
    parser.add_argument(
        "--exclude-keywords",
        nargs="+",
        default=DEFAULT_EXCLUDE_KEYWORDS,
        help="Path keywords to keep out of caption queues.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    keywords = normalize_keywords(args.exclude_keywords)
    passes = selected_passes(args.caption_passes)
    inventory_path = resolve_project_path(args.inventory)
    face_crops_path = resolve_project_path(args.face_crops)
    output_path = resolve_project_path(args.output)

    if not inventory_path.exists() and not face_crops_path.exists():
        raise SystemExit(
            "ERROR: neither inventory nor face crop CSV exists. Run P0.5 ingestion first."
        )

    rows = []
    rows.extend(load_inventory_rows(inventory_path, keywords, passes))
    rows.extend(load_face_crop_rows(face_crops_path, keywords, passes))
    rows = dedupe_rows(rows)
    write_queue(rows, output_path)

    print(f"Inventory: {inventory_path}")
    print(f"Face crops: {face_crops_path}")
    print(f"Wrote caption queue: {output_path}")
    print(f"Rows: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
