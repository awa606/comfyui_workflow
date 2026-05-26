from __future__ import annotations

import argparse
import math
from pathlib import Path

import cv2  # type: ignore
import numpy as np

from p0_common import (
    CONTACT_SHEET_DIR,
    METADATA_DIR,
    cosine_similarity,
    ensure_dirs,
    read_csv,
    read_image,
    resolve_path,
    write_csv,
    write_image,
)


FACE_CLUSTER_FIELDS = [
    "face_id",
    "cluster_id",
    "asset_id",
    "image_path",
    "similarity_to_centroid",
    "face_quality_score",
    "source_person_id",
]

REVIEW_FIELDS = [
    "cluster_id",
    "sample_count",
    "face_count",
    "user_confirmed_character_id",
    "is_clean_cluster",
    "merge_with_cluster",
    "split_needed",
    "notes",
]


def load_embeddings(path: Path) -> dict[str, np.ndarray]:
    data = np.load(path)
    return {key: np.asarray(data[key], dtype=np.float32) for key in data.files}


def cluster_embeddings(face_rows: list[dict[str, str]], embeddings: dict[str, np.ndarray], threshold: float) -> list[dict[str, object]]:
    clusters: list[dict[str, object]] = []
    output: list[dict[str, object]] = []
    sorted_rows = sorted(face_rows, key=lambda item: float(item.get("face_quality_score") or 0), reverse=True)
    for row in sorted_rows:
        face_id = row["face_id"]
        embedding = embeddings.get(face_id)
        if embedding is None:
            continue
        best_idx = -1
        best_score = -1.0
        for idx, cluster in enumerate(clusters):
            score = cosine_similarity(embedding, cluster["centroid"])  # type: ignore[arg-type]
            if score > best_score:
                best_idx, best_score = idx, score
        if best_idx >= 0 and best_score >= threshold:
            cluster = clusters[best_idx]
            members = cluster["members"]  # type: ignore[assignment]
            members.append(face_id)
            centroid = np.mean([embeddings[item] for item in members], axis=0)
            cluster["centroid"] = centroid
            cluster_id = cluster["cluster_id"]
        else:
            cluster_id = f"cluster_{len(clusters) + 1:03d}"
            clusters.append({"cluster_id": cluster_id, "centroid": embedding, "members": [face_id]})
            best_score = 1.0
        output.append(
            {
                "face_id": face_id,
                "cluster_id": cluster_id,
                "asset_id": row.get("asset_id", ""),
                "image_path": row.get("image_path", ""),
                "similarity_to_centroid": f"{best_score:.4f}",
                "face_quality_score": row.get("face_quality_score", ""),
                "source_person_id": "",
            }
        )
    return sorted(output, key=lambda item: (str(item["cluster_id"]), str(item["face_id"])))


def make_contact_sheet(cluster_id: str, rows: list[dict[str, object]], face_lookup: dict[str, dict[str, str]], sample_limit: int) -> None:
    samples = sorted(rows, key=lambda item: float(item.get("face_quality_score") or 0), reverse=True)[:sample_limit]
    if not samples:
        return
    thumbs: list[np.ndarray] = []
    tile = 160
    for item in samples:
        face = face_lookup.get(str(item["face_id"]))
        if not face:
            continue
        image = read_image(Path(face["image_path"]))
        if image is None:
            continue
        x1, y1, x2, y2 = [int(float(face[key] or 0)) for key in ("bbox_x1", "bbox_y1", "bbox_x2", "bbox_y2")]
        pad_x = int((x2 - x1) * 0.45)
        pad_y = int((y2 - y1) * 0.65)
        height, width = image.shape[:2]
        crop = image[max(0, y1 - pad_y):min(height, y2 + pad_y), max(0, x1 - pad_x):min(width, x2 + pad_x)]
        if crop.size == 0:
            continue
        crop = cv2.resize(crop, (tile, tile), interpolation=cv2.INTER_AREA)
        thumbs.append(crop)
    if not thumbs:
        return
    cols = min(6, len(thumbs))
    rows_count = int(math.ceil(len(thumbs) / cols))
    sheet = np.full((rows_count * tile, cols * tile, 3), 245, dtype=np.uint8)
    for idx, thumb in enumerate(thumbs):
        y = (idx // cols) * tile
        x = (idx % cols) * tile
        sheet[y:y + tile, x:x + tile] = thumb
    write_image(CONTACT_SHEET_DIR / f"{cluster_id}.jpg", sheet, jpeg_quality=90)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P0 step 5: cluster InsightFace embeddings and make contact sheets.")
    parser.add_argument("--face-index", default=str(METADATA_DIR / "face_index.csv"))
    parser.add_argument("--embeddings", default=str(METADATA_DIR / "face_embeddings.npz"))
    parser.add_argument("--output", default=str(METADATA_DIR / "face_clusters.csv"))
    parser.add_argument("--review-output", default=str(METADATA_DIR / "cluster_review.csv"))
    parser.add_argument("--threshold", type=float, default=0.42)
    parser.add_argument("--contact-sheet-samples", type=int, default=24)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    ensure_dirs()
    face_rows = read_csv(resolve_path(args.face_index))
    embeddings = load_embeddings(resolve_path(args.embeddings))
    rows = cluster_embeddings(face_rows, embeddings, args.threshold)
    face_lookup = {row["face_id"]: row for row in face_rows}
    by_cluster: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        by_cluster.setdefault(str(row["cluster_id"]), []).append(row)
    for cluster_id, cluster_rows in by_cluster.items():
        make_contact_sheet(cluster_id, cluster_rows, face_lookup, args.contact_sheet_samples)
    review_rows = [
        {
            "cluster_id": cluster_id,
            "sample_count": min(len(cluster_rows), args.contact_sheet_samples),
            "face_count": len(cluster_rows),
            "user_confirmed_character_id": "",
            "is_clean_cluster": "",
            "merge_with_cluster": "",
            "split_needed": "",
            "notes": "",
        }
        for cluster_id, cluster_rows in sorted(by_cluster.items(), key=lambda item: (-len(item[1]), item[0]))
    ]
    write_csv(resolve_path(args.output), FACE_CLUSTER_FIELDS, rows)
    write_csv(resolve_path(args.review_output), REVIEW_FIELDS, review_rows)
    print(f"Wrote {resolve_path(args.output)}")
    print(f"Wrote {resolve_path(args.review_output)}")
    print(f"Face clusters: {len(by_cluster)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
