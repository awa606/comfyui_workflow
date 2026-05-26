from __future__ import annotations

import argparse
from pathlib import Path

import cv2  # type: ignore
import numpy as np

from p0_common import FACE_MODEL_ROOT, METADATA_DIR, ensure_dirs, read_csv, read_image, resolve_path, write_csv


FIELDNAMES = [
    "face_id",
    "asset_id",
    "image_path",
    "face_index",
    "bbox_x1",
    "bbox_y1",
    "bbox_x2",
    "bbox_y2",
    "face_det_score",
    "face_width",
    "face_height",
    "face_area_ratio",
    "face_quality_score",
    "embedding_id",
    "notes",
]


def load_face_app(model_root: Path, det_size: int):
    from insightface.app import FaceAnalysis  # type: ignore
    import onnxruntime as ort  # type: ignore

    model_dir = model_root / "models" / "buffalo_l"
    if not model_dir.exists():
        raise FileNotFoundError(f"InsightFace buffalo_l not found: {model_dir}. No model download will be attempted.")
    available = ort.get_available_providers()
    providers = ["CUDAExecutionProvider", "CPUExecutionProvider"] if "CUDAExecutionProvider" in available else ["CPUExecutionProvider"]
    ctx_id = 0 if "CUDAExecutionProvider" in providers else -1
    print(f"InsightFace providers: {providers}", flush=True)
    app = FaceAnalysis(name="buffalo_l", root=str(model_root), providers=providers)
    app.prepare(ctx_id=ctx_id, det_size=(det_size, det_size))
    return app


def resized_for_detection(image: np.ndarray, max_dim: int) -> tuple[np.ndarray, float, float]:
    height, width = image.shape[:2]
    largest = max(height, width)
    if max_dim <= 0 or largest <= max_dim:
        return image, 1.0, 1.0
    scale = max_dim / largest
    resized = cv2.resize(image, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_AREA)
    return resized, width / resized.shape[1], height / resized.shape[0]


def face_quality(image: np.ndarray, bbox: tuple[int, int, int, int], det_score: float) -> tuple[float, float]:
    height, width = image.shape[:2]
    x1, y1, x2, y2 = bbox
    face_h = max(1, y2 - y1)
    face_w = max(1, x2 - x1)
    area_ratio = (face_w * face_h) / max(1, width * height)
    crop = image[max(0, y1):max(0, y2), max(0, x1):max(0, x2)]
    if crop.size == 0:
        blur = 0.0
    else:
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        blur = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    size_score = min(1.0, max(0.0, (face_h / max(1, height) - 0.04) / 0.22))
    blur_score = min(1.0, max(0.0, (blur - 35.0) / 180.0))
    quality = min(1.0, max(0.0, 0.45 * size_score + 0.35 * blur_score + 0.20 * det_score))
    return area_ratio, quality


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P0 step 4: run InsightFace face detection and indexing.")
    parser.add_argument("--duplicates", default=str(METADATA_DIR / "duplicate_candidates.csv"))
    parser.add_argument("--output", default=str(METADATA_DIR / "face_index.csv"))
    parser.add_argument("--embedding-output", default=str(METADATA_DIR / "face_embeddings.npz"))
    parser.add_argument("--face-model-root", default=str(FACE_MODEL_ROOT))
    parser.add_argument("--det-size", type=int, default=640)
    parser.add_argument("--max-dim", type=int, default=1280, help="Resize large images before InsightFace detection.")
    parser.add_argument("--include-duplicates", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    ensure_dirs()
    face_app = load_face_app(resolve_path(args.face_model_root), args.det_size)
    assets = read_csv(resolve_path(args.duplicates))
    if not args.include_duplicates:
        assets = [row for row in assets if row.get("is_duplicate") != "yes"]

    rows: list[dict[str, object]] = []
    embeddings: dict[str, np.ndarray] = {}
    face_counter = 1
    for index, asset in enumerate(assets, start=1):
        if index % 500 == 0:
            print(f"Face indexed {index}/{len(assets)} visual assets; faces={len(rows)}", flush=True)
        image_path = Path(asset["image_path"])
        image = read_image(image_path)
        if image is None:
            continue
        detect_image, scale_x, scale_y = resized_for_detection(image, args.max_dim)
        faces = face_app.get(detect_image)
        if not faces:
            continue
        height, width = image.shape[:2]
        for face_idx, face in enumerate(faces, start=1):
            x1, y1, x2, y2 = [int(round(value)) for value in face.bbox]
            x1, x2 = int(round(x1 * scale_x)), int(round(x2 * scale_x))
            y1, y2 = int(round(y1 * scale_y)), int(round(y2 * scale_y))
            x1, x2 = max(0, min(width - 1, x1)), max(0, min(width, x2))
            y1, y2 = max(0, min(height - 1, y1)), max(0, min(height, y2))
            det_score = float(getattr(face, "det_score", 0.0) or 0.0)
            area_ratio, quality = face_quality(image, (x1, y1, x2, y2), det_score)
            face_id = f"face_{face_counter:07d}"
            embedding = np.asarray(face.embedding, dtype=np.float32)
            embeddings[face_id] = embedding
            rows.append(
                {
                    "face_id": face_id,
                    "asset_id": asset["asset_id"],
                    "image_path": asset["image_path"],
                    "face_index": face_idx,
                    "bbox_x1": x1,
                    "bbox_y1": y1,
                    "bbox_x2": x2,
                    "bbox_y2": y2,
                    "face_det_score": f"{det_score:.4f}",
                    "face_width": max(1, x2 - x1),
                    "face_height": max(1, y2 - y1),
                    "face_area_ratio": f"{area_ratio:.6f}",
                    "face_quality_score": f"{quality:.4f}",
                    "embedding_id": face_id,
                    "notes": "",
                }
            )
            face_counter += 1

    output_path = resolve_path(args.output)
    write_csv(output_path, FIELDNAMES, rows)
    embedding_path = resolve_path(args.embedding_output)
    embedding_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(embedding_path, **embeddings)
    print(f"Wrote {output_path}")
    print(f"Wrote {embedding_path}")
    print(f"Faces: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
