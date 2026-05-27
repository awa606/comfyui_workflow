from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path

from p0_common import METADATA_DIR, ensure_dirs, read_csv, resolve_path, write_csv


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
    "near_duplicate_group_id",
    "duplicate_level",
    "is_duplicate",
    "representative_asset_id",
    "blur_score",
    "has_face",
    "face_count",
    "face_cluster_id",
    "face_quality_score",
    "review_priority",
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


def number(value: object, default: float = 0.0) -> float:
    try:
        return float(value or default)
    except (TypeError, ValueError):
        return default


def body_view_from_face(score: float, face_count: int) -> str:
    if face_count <= 0:
        return "unknown"
    if score >= 0.72:
        return "face_or_upper_body_candidate"
    if score >= 0.52:
        return "body_or_full_body_candidate"
    return "low_quality_face_candidate"


def review_priority(
    face_quality: float,
    cluster_size: int,
    duplicate_level: str,
    blur: float,
    reject_reasons: list[str],
) -> str:
    reject_set = set(reject_reasons)
    if "unreadable_image" in reject_set or duplicate_level == "exact_duplicate":
        return "D"
    if blur > 0 and blur < 20:
        return "D"
    if "no_face_detected" in reject_set:
        return "C" if blur >= 25 and duplicate_level != "exact_duplicate" else "D"
    if (
        face_quality >= 0.72
        and cluster_size >= 5
        and duplicate_level == "unique"
        and blur >= 35
        and not reject_reasons
    ):
        return "A"
    if face_quality >= 0.60 and cluster_size >= 3 and duplicate_level in {"unique", "near_duplicate_strong"} and blur >= 35:
        return "B"
    if face_quality >= 0.45 or cluster_size >= 2 or duplicate_level in {"near_duplicate_strong", "near_duplicate_weak"}:
        return "C"
    return "D"


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
    cluster_counts = Counter(row.get("cluster_id") for row in clusters if row.get("cluster_id"))
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
        best_face = max(face_rows, key=lambda item: number(item.get("face_quality_score")), default={})
        cluster_id = cluster_by_face.get(best_face.get("face_id", ""), "")
        face_quality = number(best_face.get("face_quality_score"))
        face_count = len(face_rows)
        blur = number(duplicate.get("blur_score"))
        duplicate_level = duplicate.get("duplicate_level") or ("exact_duplicate" if duplicate.get("is_duplicate") == "yes" else "unique")
        cluster_size = cluster_counts.get(cluster_id, 0)

        reject_reasons: list[str] = []
        if duplicate_level == "exact_duplicate" or duplicate.get("is_duplicate") == "yes":
            reject_reasons.append("exact_duplicate")
        if duplicate.get("notes"):
            reject_reasons.append(str(duplicate["notes"]))
        if blur < 35:
            reject_reasons.append("blurred_frame")
        if not face_rows:
            reject_reasons.append("no_face_detected")

        priority = review_priority(face_quality, cluster_size, duplicate_level, blur, reject_reasons)
        is_exact_duplicate = duplicate_level == "exact_duplicate" or duplicate.get("is_duplicate") == "yes"
        is_reviewable_image = not is_exact_duplicate and blur >= 25
        is_clean_face_candidate = not is_exact_duplicate and blur >= 35

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
                "near_duplicate_group_id": duplicate.get("near_duplicate_group_id", ""),
                "duplicate_level": duplicate_level,
                "is_duplicate": duplicate.get("is_duplicate", ""),
                "representative_asset_id": duplicate.get("representative_asset_id", ""),
                "blur_score": duplicate.get("blur_score", ""),
                "has_face": "yes" if face_rows else "no",
                "face_count": face_count,
                "face_cluster_id": cluster_id,
                "face_quality_score": f"{face_quality:.4f}" if face_rows else "",
                "review_priority": priority,
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
                "use_for_faceid": "yes" if face_quality >= 0.72 and is_clean_face_candidate else "no",
                "use_for_lora": "candidate" if face_quality >= 0.55 and is_clean_face_candidate else "no",
                "use_for_outfit_ref": "candidate" if is_reviewable_image else "no",
                "use_for_pose_ref": "candidate" if is_reviewable_image else "no",
                "reject_reason": ";".join(dict.fromkeys(reason for reason in reject_reasons if reason)),
                "notes": "P0_only; P1_fields_pending",
            }
        )
    return rows


def write_report(
    path: Path,
    rows: list[dict[str, object]],
    inventory: list[dict[str, str]],
    frames: list[dict[str, str]],
    clusters: list[dict[str, str]],
) -> None:
    images = sum(1 for row in inventory if row.get("source_type") == "image")
    videos = sum(1 for row in inventory if row.get("source_type") == "video")
    extracted = sum(1 for row in frames if row.get("extract_status") == "ok")
    face_assets = sum(1 for row in rows if row.get("has_face") == "yes")
    cluster_counts = Counter(row.get("face_cluster_id") for row in rows if row.get("face_cluster_id"))
    low_quality = [row for row in rows if "blurred_frame" in str(row.get("reject_reason", ""))]
    exact_duplicates = sum(1 for row in rows if row.get("duplicate_level") == "exact_duplicate")
    near_duplicates = sum(1 for row in rows if str(row.get("duplicate_level", "")).startswith("near_duplicate"))
    priority_counts = Counter(str(row.get("review_priority") or "unknown") for row in rows)
    top_clusters = cluster_counts.most_common(10)

    lines = [
        "# P0 素材管线验证报告",
        "",
        "当前阶段只完成 P0：基础索引、视频抽帧、pHash 去重、模糊检测、InsightFace 人脸检测与聚类。",
        "",
        "本报告是本地审核辅助文档。CSV、NPZ、抽帧图和 contact sheet 不上传到 GitHub。",
        "",
        "## 统计摘要",
        "",
        f"- 扫描图片数量：{images}",
        f"- 扫描视频数量：{videos}",
        f"- 抽帧数量：{extracted}",
        f"- 检测到有人脸的素材数量：{face_assets}",
        f"- 聚类出的 face cluster 数量：{len(set(row.get('cluster_id') for row in clusters if row.get('cluster_id')))}",
        f"- exact pHash 重复素材数量：{exact_duplicates}",
        f"- near pHash 近重复候选素材数量：{near_duplicates}",
        f"- 模糊或低质量候选数量：{len(low_quality)}",
        "",
        "## 审核优先级统计",
        "",
        f"- A：{priority_counts.get('A', 0)}，优先审核的高质量身份候选。",
        f"- B：{priority_counts.get('B', 0)}，可进入 role_001 候选池的次优身份/半身素材。",
        f"- C：{priority_counts.get('C', 0)}，可作为服装、姿势、体态或人工复核素材。",
        f"- D：{priority_counts.get('D', 0)}，重复、严重模糊、不可读或低价值素材。",
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
            "低质量候选主要由 `blurred_frame`、`exact_duplicate`、`no_face_detected`、`unreadable_image` 标注。",
            "人工审核时优先按 `review_priority` 排序，再参考 `reject_reason`、`duplicate_level` 和 `face_quality_score`。",
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
            "## 下一步",
            "",
            "1. 打开 `outputs/cluster_contact_sheets/cluster_*.jpg` 进行人工聚类审核。",
            "2. 在 `metadata/cluster_review.csv` 中填写 `user_confirmed_character_id=role_001`。",
            "3. 运行 `python scripts/export_role_candidates.py --role role_001` 导出候选清单。",
            "4. 当 FaceID 候选达到 3-8 张、role_001 候选达到 20-40 张后，再进入 FaceID / IPAdapter 测试。",
            "",
            "## 边界",
            "",
            "- 未训练 LoRA。",
            "- 未进行 ComfyUI 批量出图。",
            "- 未安装 DWPose / SAM / GroundingDINO / Depth Anything。",
            "- 未移动、删除、覆盖原始素材。",
            "- 生成的 CSV、NPZ、抽帧图和 contact sheet 为本地审核产物，不上传到 GitHub。",
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
    parser.add_argument("--report", default="docs/01_p0_asset_pipeline/p0_asset_pipeline_report.md")
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
