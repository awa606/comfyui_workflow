from __future__ import annotations

import argparse
from pathlib import Path

from p0_common import METADATA_DIR, PROJECT_DIR, ensure_dirs, read_csv, resolve_path, safe_name, write_csv


EXPORT_PREFIX_FIELDS = [
    "confirmed_character_id",
    "candidate_bucket",
    "linked_path",
    "export_notes",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export confirmed role candidates from P0 master asset index.")
    parser.add_argument("--role", default="role_001", help="Confirmed character id to export.")
    parser.add_argument("--master", default=str(METADATA_DIR / "master_asset_index.csv"))
    parser.add_argument("--cluster-review", default=str(METADATA_DIR / "cluster_review.csv"))
    parser.add_argument("--output", default=str(METADATA_DIR / "role_001_candidate_export.csv"))
    parser.add_argument(
        "--copy-mode",
        choices=["manifest-only", "hardlink"],
        default="manifest-only",
        help="Default only writes CSV. hardlink creates local candidate hardlinks without moving originals.",
    )
    return parser


def confirmed_clusters(review_rows: list[dict[str, str]], role: str) -> set[str]:
    return {
        row.get("cluster_id", "")
        for row in review_rows
        if row.get("user_confirmed_character_id", "").strip() == role and row.get("cluster_id")
    }


def candidate_bucket(row: dict[str, str]) -> str:
    if row.get("use_for_faceid") == "yes":
        return "faceid"
    if row.get("use_for_lora") in {"yes", "candidate"}:
        return "lora"
    if row.get("use_for_outfit_ref") in {"yes", "candidate"}:
        return "outfit_ref"
    if row.get("use_for_pose_ref") in {"yes", "candidate"}:
        return "pose_ref"
    return "reference"


def bucket_dir(role: str, bucket: str) -> Path:
    role_root = PROJECT_DIR / "characters" / role
    if bucket == "faceid":
        return role_root / "selected_for_faceid"
    if bucket == "lora":
        return role_root / "selected_for_lora"
    if bucket == "outfit_ref":
        return role_root / "outfits" / "outfit_unassigned"
    if bucket == "pose_ref":
        return role_root / "pose_refs"
    return role_root / "body_reference"


def hardlink_candidate(row: dict[str, str], role: str, bucket: str) -> tuple[str, str]:
    source = Path(row.get("image_path", ""))
    if not source.exists():
        return "", "source_missing"
    target_dir = bucket_dir(role, bucket)
    target_dir.mkdir(parents=True, exist_ok=True)
    suffix = source.suffix.lower() or ".jpg"
    target = target_dir / f"{safe_name(row.get('asset_id', 'asset'))}{suffix}"
    if target.exists():
        return str(target), "already_exists"
    try:
        target.hardlink_to(source)
    except OSError as exc:
        return "", f"hardlink_failed:{exc}"
    return str(target), "hardlinked"


def export_rows(
    master_rows: list[dict[str, str]],
    confirmed_cluster_ids: set[str],
    role: str,
    copy_mode: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in master_rows:
        if row.get("face_cluster_id") not in confirmed_cluster_ids:
            continue
        bucket = candidate_bucket(row)
        linked_path = ""
        export_notes = "manifest_only"
        if copy_mode == "hardlink":
            linked_path, export_notes = hardlink_candidate(row, role, bucket)
        rows.append(
            {
                "confirmed_character_id": role,
                "candidate_bucket": bucket,
                "linked_path": linked_path,
                "export_notes": export_notes,
                **row,
            }
        )
    return rows


def main() -> int:
    args = build_parser().parse_args()
    ensure_dirs()
    master_path = resolve_path(args.master)
    review_path = resolve_path(args.cluster_review)
    output_path = resolve_path(args.output)
    master_rows = read_csv(master_path)
    review_rows = read_csv(review_path)
    cluster_ids = confirmed_clusters(review_rows, args.role)
    rows = export_rows(master_rows, cluster_ids, args.role, args.copy_mode)
    fieldnames = EXPORT_PREFIX_FIELDS + [field for field in master_rows[0].keys() if field not in EXPORT_PREFIX_FIELDS] if master_rows else EXPORT_PREFIX_FIELDS
    write_csv(output_path, fieldnames, rows)
    print(f"Wrote {output_path}")
    print(f"Confirmed clusters for {args.role}: {len(cluster_ids)}")
    print(f"Exported candidates: {len(rows)}")
    print(f"Copy mode: {args.copy_mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
