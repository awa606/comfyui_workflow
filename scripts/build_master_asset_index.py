from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path

from p0_common import METADATA_DIR, as_posix, ensure_dirs, read_csv, resolve_path, write_csv


FIELDNAMES = [
    "asset_id",
    "asset_type",
    "source_file_id",
    "source_root",
    "source_person_id",
    "source_path",
    "image_path",
    "frame_id",
    "frame_index",
    "timestamp_seconds",
    "width",
    "height",
    "phash",
    "duplicate_group_id",
    "is_duplicate",
    "representative_asset_id",
    "blur_score",
    "has_face",
    "face_count",
    "face_cluster_id",
    "face_quality_score",
    "body_view",
    "pose_type",
    "outfit_type",
    "hairstyle",
    "makeup",
    "shoes_visible",
    "hands_visible",
    "feet_visible",
    "scene_type",
    "object_tags",
    "depth_available",
    "mask_available",
    "use_for_faceid",
    "use_for_lora",
    "use_for_outfit_ref",
    "use_for_pose_ref",
    "reject_reason",
    "notes",
]


def body_view_from_face(score: float, face_count: int) -> str:
    if face_count <= 0:
        return "unknown"
    if score >= 0.72:
        return "face_or_upper_body_candidate"
    if score >= 0.52:
        return "body_or_full_body_candidate"
    return "low_quality_face_candidate"


def build_rows(
    inventory: list[dict[str, str]],
    frames: list[dict[str, str]],
    duplicates: list[dict[str, str]],
    faces: list[dict[str, str]],
    clusters: list[dict[str, str]],
) -> list[dict[str, object]]:
    inventory_by_file = {row["file_id"]: row for row in inventory}
    frame_by_id = {row["frame_id"]: row for row in frames if row.get("extract_status") == "ok"}
    dup_by_asset = {row["asset_id"]: row for row in duplicates}
    cluster_by_face = {row["face_id"]: row["cluster_id"] for row in clusters}
    faces_by_asset: dict[str, list[dict[str, str]]] = defaultdict(list)
    for face in faces:
        faces_by_asset[face["asset_id"]].append(face)

    rows: list[dict[str, object]] = []
    for asset_id, duplicate in dup_by_asset.items():
        asset_type = duplicate["asset_type"]
        file_id = duplicate["file_id"]
        frame = frame_by_id.get(duplicate.get("frame_id", ""))
        source = inventory_by_file.get(file_id, {})
        face_rows = faces_by_asset.get(asset_id, [])
        best_face = max(face_rows, key=lambda item: float(item.get("face_quality_score") or 0), default={})
        cluster_id = cluster_by_face.get(best_face.get("face_id", ""), "")
        face_quality = float(best_face.get("face_quality_score") or 0)
        face_count = len(face_rows)
        reject_reasons: list[str] = []
        if duplicate.get("is_duplicate") == "yes":
            reject_reasons.append("duplicate_candidate")
        if float(duplicate.get("blur_score") or 0) < 35:
            reject_reasons.append("blurred_frame")
        if not face_rows:
            reject_reasons.append("no_face_detected")
        rows.append(
            {
                "asset_id": asset_id,
                "asset_type": asset_type,
                "source_file_id": file_id,
                "source_root": source.get("source_root", ""),
                "source_person_id": source.get("source_person_id", ""),
                "source_path": source.get("source_path", ""),
                "image_path": duplicate.get("image_path", ""),
                "frame_id": duplicate.get("frame_id", ""),
                "frame_index": frame.get("frame_index", "") if frame else "",
                "timestamp_seconds": frame.get("timestamp_seconds", "") if frame else "",
                "width": frame.get("width", source.get("width", "")) if frame else source.get("width", ""),
                "height": frame.get("height", source.get("height", "")) if frame else source.get("height", ""),
                "phash": duplicate.get("phash", ""),
                "duplicate_group_id": duplicate.get("duplicate_group_id", ""),
                "is_duplicate": duplicate.get("is_duplicate", ""),
                "representative_asset_id": duplicate.get("representative_asset_id", ""),
                "blur_score": duplicate.get("blur_score", ""),
                "has_face": "yes" if face_rows else "no",
                "face_count": face_count,
                "face_cluster_id": cluster_id,
                "face_quality_score": f"{face_quality:.4f}" if face_rows else "",
                "body_view": body_view_from_face(face_quality, face_count),
                "pose_type": "",
                "outfit_type": "",
                "hairstyle": "",
                "makeup": "",
                "shoes_visible": "unknown",
                "hands_visible": "unknown",
                "feet_visible": "unknown",
                "scene_type": "",
                "object_tags": "",
                "depth_available": "no",
                "mask_available": "no",
                "use_for_faceid": "yes" if face_quality >= 0.72 and duplicate.get("is_duplicate") != "yes" else "no",
                "use_for_lora": "candidate" if face_quality >= 0.55 and duplicate.get("is_duplicate") != "yes" else "no",
                "use_for_outfit_ref": "candidate" if duplicate.get("is_duplicate") != "yes" else "no",
                "use_for_pose_ref": "candidate" if duplicate.get("is_duplicate") != "yes" else "no",
                "reject_reason": ";".join(reject_reasons),
                "notes": "P0_only; P1_fields_pending",
            }
        )
    return rows


def write_report(path: Path, rows: list[dict[str, object]], inventory: list[dict[str, str]], frames: list[dict[str, str]], clusters: list[dict[str, str]]) -> None:
    images = sum(1 for row in inventory if row.get("source_type") == "image")
    videos = sum(1 for row in inventory if row.get("source_type") == "video")
    extracted = sum(1 for row in frames if row.get("extract_status") == "ok")
    face_assets = sum(1 for row in rows if row.get("has_face") == "yes")
    cluster_counts = Counter(row.get("face_cluster_id") for row in rows if row.get("face_cluster_id"))
    low_quality = [row for row in rows if "blurred_frame" in str(row.get("reject_reason", ""))]
    duplicate_assets = sum(1 for row in rows if row.get("is_duplicate") == "yes")
    top_clusters = cluster_counts.most_common(10)
    lines = [
        "# P0 素材管线验证报告",
        "",
        "当前阶段只完成 P0：基础索引、视频抽帧、去重、模糊检测、InsightFace 人脸检测与聚类。",
        "",
        "本轮为 P0 验证跑：扫描全量素材源，视频抽帧采用 `--max-frames-per-video 1`，即每个视频最多抽 1 帧；后续可用 `--max-frames-per-video 0` 做全量逐秒抽帧。",
        "",
        "## 统计摘要",
        "",
        f"- 扫描图片数量：{images}",
        f"- 扫描视频数量：{videos}",
        f"- 抽帧数量：{extracted}",
        f"- 检测到有人脸的素材数量：{face_assets}",
        f"- 聚类出的 face cluster 数量：{len(set(row.get('cluster_id') for row in clusters if row.get('cluster_id')))}",
        f"- pHash 重复候选素材数量：{duplicate_assets}",
        f"- 模糊或低质量候选数量：{len(low_quality)}",
        "",
        "## 样本最多的 cluster",
        "",
    ]
    if top_clusters:
        lines.extend([f"- {cluster_id}: {count} assets" for cluster_id, count in top_clusters])
    else:
        lines.append("- 暂无 face cluster。")
    lines.extend(
        [
            "",
            "## 质量较差素材",
            "",
            "低质量候选主要由 `blurred_frame`、`duplicate_candidate`、`no_face_detected` 标注。请优先在 `metadata/master_asset_index.csv` 中按 `reject_reason` 过滤。",
            "",
            "## 生成物",
            "",
            "- `metadata/source_inventory.csv`",
            "- `metadata/frame_index.csv`",
            "- `metadata/duplicate_candidates.csv`",
            "- `metadata/face_index.csv`",
            "- `metadata/face_clusters.csv`",
            "- `metadata/cluster_review.csv`",
            "- `metadata/master_asset_index.csv`",
            "- `outputs/cluster_contact_sheets/cluster_*.jpg`",
            "",
            "## 边界",
            "",
            "- 未训练 LoRA。",
            "- 未进行 ComfyUI 批量出图。",
            "- 未安装 DWPose / SAM / GroundingDINO / Depth Anything。",
            "- 未移动、删除原始素材。",
            "- 生成的 CSV 和 contact sheet 为本地审核产物，不上传到 GitHub。",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P0 step 6: build master asset index and report.")
    parser.add_argument("--inventory", default=str(METADATA_DIR / "source_inventory.csv"))
    parser.add_argument("--frames", default=str(METADATA_DIR / "frame_index.csv"))
    parser.add_argument("--duplicates", default=str(METADATA_DIR / "duplicate_candidates.csv"))
    parser.add_argument("--faces", default=str(METADATA_DIR / "face_index.csv"))
    parser.add_argument("--clusters", default=str(METADATA_DIR / "face_clusters.csv"))
    parser.add_argument("--output", default=str(METADATA_DIR / "master_asset_index.csv"))
    parser.add_argument("--report", default="docs/p0_asset_pipeline_report.md")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    ensure_dirs()
    inventory = read_csv(resolve_path(args.inventory))
    frames = read_csv(resolve_path(args.frames))
    duplicates = read_csv(resolve_path(args.duplicates))
    faces = read_csv(resolve_path(args.faces))
    clusters = read_csv(resolve_path(args.clusters))
    rows = build_rows(inventory, frames, duplicates, faces, clusters)
    write_csv(resolve_path(args.output), FIELDNAMES, rows)
    write_report(resolve_path(args.report), rows, inventory, frames, clusters)
    print(f"Wrote {resolve_path(args.output)}")
    print(f"Wrote {resolve_path(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
