from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from p0_common import METADATA_DIR, blur_score, ensure_dirs, phash, read_csv, read_image, resolve_path, write_csv


FIELDNAMES = [
    "asset_id",
    "asset_type",
    "file_id",
    "frame_id",
    "image_path",
    "phash",
    "blur_score",
    "duplicate_group_id",
    "is_duplicate",
    "representative_asset_id",
    "notes",
]


def visual_assets(inventory: list[dict[str, str]], frames: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in inventory:
        if row.get("source_type") == "image" and row.get("scan_status") == "ok":
            rows.append(
                {
                    "asset_id": row["file_id"],
                    "asset_type": "source_image",
                    "file_id": row["file_id"],
                    "frame_id": "",
                    "image_path": row["source_path"],
                }
            )
    for row in frames:
        if row.get("extract_status") == "ok":
            rows.append(
                {
                    "asset_id": row["frame_id"],
                    "asset_type": "video_frame",
                    "file_id": row["source_file_id"],
                    "frame_id": row["frame_id"],
                    "image_path": row["frame_path"],
                }
            )
    return rows


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P0 step 3: compute pHash, blur, and duplicate groups.")
    parser.add_argument("--inventory", default=str(METADATA_DIR / "source_inventory.csv"))
    parser.add_argument("--frames", default=str(METADATA_DIR / "frame_index.csv"))
    parser.add_argument("--output", default=str(METADATA_DIR / "duplicate_candidates.csv"))
    parser.add_argument("--workers", type=int, default=8)
    return parser


def hash_asset(asset: dict[str, str]) -> dict[str, object]:
    image = read_image(Path(asset["image_path"]))
    image_phash = phash(image)
    return {
        **asset,
        "phash": image_phash,
        "blur_score": f"{blur_score(image):.3f}",
        "duplicate_group_id": "",
        "is_duplicate": "no",
        "representative_asset_id": "",
        "notes": "" if image is not None else "unreadable_image",
    }


def main() -> int:
    args = build_parser().parse_args()
    ensure_dirs()
    assets = visual_assets(read_csv(resolve_path(args.inventory)), read_csv(resolve_path(args.frames)))
    rows: list[dict[str, object]] = []
    groups: dict[str, list[dict[str, object]]] = {}
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = [executor.submit(hash_asset, asset) for asset in assets]
        for index, future in enumerate(as_completed(futures), start=1):
            row = future.result()
            rows.append(row)
            image_phash = str(row.get("phash") or "")
            if image_phash:
                groups.setdefault(image_phash, []).append(row)
            if index % 500 == 0 or index == len(futures):
                print(f"Hashed {index}/{len(futures)} visual assets", flush=True)

    group_index = 1
    for group_rows in groups.values():
        if len(group_rows) <= 1:
            continue
        group_id = f"dup_{group_index:05d}"
        representative = max(group_rows, key=lambda item: float(item.get("blur_score") or 0))
        for row in group_rows:
            row["duplicate_group_id"] = group_id
            row["representative_asset_id"] = representative["asset_id"]
            row["is_duplicate"] = "no" if row["asset_id"] == representative["asset_id"] else "yes"
        group_index += 1

    output_path = resolve_path(args.output)
    write_csv(output_path, FIELDNAMES, rows)
    print(f"Wrote {output_path}")
    print(f"Visual assets: {len(rows)}")
    print(f"Duplicate groups: {group_index - 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
