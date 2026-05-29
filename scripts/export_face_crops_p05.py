from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import sys
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageOps


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
    "crop_id",
    "source_path",
    "crop_path",
    "bbox_x1",
    "bbox_y1",
    "bbox_x2",
    "bbox_y2",
    "face_quality_score",
    "face_det_score",
    "source_person_id",
    "use_for_faceid",
    "use_for_identity_lora",
    "notes",
]

INDEX_PATH_CANDIDATES = [
    "metadata/master_asset_index.csv",
    "metadata/p05_local_source_inventory.csv",
]


def resolve_project_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_DIR / path
    return path.resolve()


def normalize_for_match(value: str) -> str:
    return value.replace("/", "\\").casefold()


def normalize_keywords(values: list[str]) -> list[str]:
    return [normalize_for_match(value) for value in values if value.strip()]


def path_has_excluded_keyword(path: Path, keywords: list[str]) -> str:
    normalized = normalize_for_match(str(path))
    for keyword in keywords:
        if keyword in normalized:
            return keyword
    return ""


def truthy(value: str | None) -> bool:
    return (value or "").strip().casefold() in {"1", "true", "yes", "y"}


def safe_label(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", value).strip(" .")
    return cleaned or "unknown"


def infer_source_person_id(path: Path) -> str:
    parent = path.parent.name or "unknown"
    return safe_label(parent)


def choose_index_path(raw_value: str | None) -> Path:
    if raw_value:
        index_path = resolve_project_path(raw_value)
        if not index_path.exists():
            raise FileNotFoundError(f"Index CSV not found: {index_path}")
        return index_path

    for candidate in INDEX_PATH_CANDIDATES:
        index_path = resolve_project_path(candidate)
        if index_path.exists():
            return index_path

    candidates = ", ".join(INDEX_PATH_CANDIDATES)
    raise FileNotFoundError(f"No index CSV found. Expected one of: {candidates}")


def get_row_path(row: dict[str, str]) -> Path | None:
    for key in ("source_path", "image_path", "file_path", "asset_path", "path"):
        value = (row.get(key) or "").strip()
        if value:
            return Path(value).expanduser().resolve()
    return None


def iter_safe_image_records(
    index_path: Path, keywords: list[str]
) -> list[tuple[Path, str]]:
    records: list[tuple[Path, str]] = []
    with index_path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if truthy(row.get("excluded")):
                continue

            source_path = get_row_path(row)
            if source_path is None:
                continue
            if source_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            if path_has_excluded_keyword(source_path, keywords):
                continue
            source_type = (row.get("source_type") or "image").strip().casefold()
            if source_type and source_type != "image":
                continue
            if not source_path.exists() or not source_path.is_file():
                continue

            person_id = (row.get("source_person_id") or "").strip()
            records.append((source_path, safe_label(person_id) if person_id else infer_source_person_id(source_path)))

    records.sort(key=lambda item: str(item[0]))
    return records


def default_insightface_root() -> Path:
    env_value = os.environ.get("INSIGHTFACE_HOME") or os.environ.get("INSIGHTFACE_ROOT")
    if env_value:
        return Path(env_value).expanduser().resolve()
    return (Path.home() / ".insightface").resolve()


def assert_local_insightface_model(root: Path, model_name: str) -> None:
    model_dir = root / "models" / model_name
    if not model_dir.exists() or not any(model_dir.glob("*.onnx")):
        raise FileNotFoundError(
            "InsightFace model files were not found locally at "
            f"{model_dir}. Copy/install the model there first; this script does not "
            "download models."
        )


def should_preload_cuda_dlls(providers: list[str] | None) -> bool:
    if providers is None:
        return True
    return any(provider == "CUDAExecutionProvider" for provider in providers)


def preload_cuda_dlls(providers: list[str] | None) -> None:
    if not should_preload_cuda_dlls(providers):
        return

    try:
        import torch  # type: ignore
    except ImportError:
        return

    # Importing torch on Windows loads its bundled CUDA/cuDNN DLLs so
    # onnxruntime-gpu can resolve CUDAExecutionProvider dependencies.
    _ = torch.cuda.is_available()


def load_face_analysis(model_name: str, model_root: Path, providers: list[str] | None) -> Any:
    preload_cuda_dlls(providers)
    try:
        from insightface.app import FaceAnalysis  # type: ignore
    except ImportError:
        print(
            "ERROR: insightface is not installed in this Python environment.",
            file=sys.stderr,
        )
        print(
            "Install it into the local ComfyUI/Python environment before running crops.",
            file=sys.stderr,
        )
        raise SystemExit(2)

    return FaceAnalysis(
        name=model_name,
        root=str(model_root),
        providers=providers,
        allowed_modules=["detection"],
    )


def load_rgb_image(path: Path) -> Image.Image:
    with Image.open(path) as image:
        return ImageOps.exif_transpose(image).convert("RGB")


def image_to_bgr_array(image: Image.Image) -> np.ndarray:
    rgb = np.asarray(image)
    return np.ascontiguousarray(rgb[:, :, ::-1])


def expanded_square_box(
    bbox: tuple[float, float, float, float],
    image_width: int,
    image_height: int,
    margin_scale: float,
) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = bbox
    width = max(1.0, x2 - x1)
    height = max(1.0, y2 - y1)

    expanded_x1 = x1 - width * margin_scale
    expanded_y1 = y1 - height * (margin_scale + 0.20)
    expanded_x2 = x2 + width * margin_scale
    expanded_y2 = y2 + height * (margin_scale + 0.10)

    center_x = (expanded_x1 + expanded_x2) / 2.0
    center_y = (expanded_y1 + expanded_y2) / 2.0
    side = max(expanded_x2 - expanded_x1, expanded_y2 - expanded_y1)

    half = side / 2.0
    crop_x1 = int(round(center_x - half))
    crop_y1 = int(round(center_y - half))
    crop_x2 = int(round(center_x + half))
    crop_y2 = int(round(center_y + half))

    if crop_x2 <= crop_x1:
        crop_x2 = crop_x1 + 1
    if crop_y2 <= crop_y1:
        crop_y2 = crop_y1 + 1

    # PIL can crop outside image bounds and will pad; clamp only absurd overflow.
    max_pad = max(image_width, image_height) * 2
    return (
        max(crop_x1, -max_pad),
        max(crop_y1, -max_pad),
        min(crop_x2, image_width + max_pad),
        min(crop_y2, image_height + max_pad),
    )


def crop_face(
    image: Image.Image,
    bbox: tuple[float, float, float, float],
    output_size: int,
    margin_scale: float,
) -> Image.Image:
    crop_box = expanded_square_box(bbox, image.width, image.height, margin_scale)
    crop = image.crop(crop_box)
    return crop.resize((output_size, output_size), Image.Resampling.LANCZOS)


def estimate_face_quality(
    bbox: tuple[float, float, float, float],
    det_score: float,
    image_width: int,
    image_height: int,
) -> float:
    x1, y1, x2, y2 = bbox
    face_width = max(1.0, x2 - x1)
    face_height = max(1.0, y2 - y1)
    min_face_side = min(face_width, face_height)
    image_side = max(1.0, min(image_width, image_height))
    size_score = min(1.0, min_face_side / max(128.0, image_side * 0.18))
    quality = max(0.0, min(1.0, det_score * (0.65 + 0.35 * size_score)))
    return quality


def make_crop_id(source_path: Path, face_index: int, bbox: tuple[float, float, float, float]) -> str:
    rounded_bbox = ",".join(f"{value:.1f}" for value in bbox)
    digest = hashlib.sha1(
        f"{source_path.as_posix()}::{face_index}::{rounded_bbox}".encode("utf-8")
    ).hexdigest()
    return f"p05_face_{digest[:16]}"


def format_float(value: float) -> str:
    return f"{value:.4f}"


def write_rows(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def parse_providers(raw_value: str) -> list[str] | None:
    providers = [item.strip() for item in raw_value.split(",") if item.strip()]
    return providers or None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Export P0.5 face crops from a safe asset index with local InsightFace. "
            "This writes processed crops and metadata only; it never changes sources."
        )
    )
    parser.add_argument(
        "--index",
        default=None,
        help=(
            "Input CSV. Defaults to metadata/master_asset_index.csv if present, "
            "otherwise metadata/p05_local_source_inventory.csv."
        ),
    )
    parser.add_argument(
        "--output-dir",
        default="outputs/p05_face_crops",
        help="Output crop directory. Defaults to outputs/p05_face_crops.",
    )
    parser.add_argument(
        "--output-csv",
        default="metadata/p05_face_crops.csv",
        help="Output crop metadata CSV. Defaults to metadata/p05_face_crops.csv.",
    )
    parser.add_argument("--crop-size", type=int, default=768)
    parser.add_argument("--det-size", type=int, default=640)
    parser.add_argument("--ctx-id", type=int, default=0)
    parser.add_argument("--model-name", default="buffalo_l")
    parser.add_argument(
        "--insightface-root",
        default=str(default_insightface_root()),
        help="Local InsightFace root. Defaults to INSIGHTFACE_HOME or ~/.insightface.",
    )
    parser.add_argument(
        "--providers",
        default="CUDAExecutionProvider,CPUExecutionProvider",
        help="ONNX Runtime providers, comma-separated.",
    )
    parser.add_argument("--min-det-score", type=float, default=0.50)
    parser.add_argument("--min-quality-score", type=float, default=0.45)
    parser.add_argument("--margin-scale", type=float, default=0.45)
    parser.add_argument(
        "--exclude-keywords",
        nargs="+",
        default=DEFAULT_EXCLUDE_KEYWORDS,
        help="Path keywords to skip before loading images.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing crop files. By default existing crops are reused.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.crop_size < 128:
        raise SystemExit("ERROR: --crop-size must be at least 128")
    if args.det_size < 320:
        raise SystemExit("ERROR: --det-size must be at least 320")

    keywords = normalize_keywords(args.exclude_keywords)
    index_path = choose_index_path(args.index)
    output_dir = resolve_project_path(args.output_dir)
    output_csv = resolve_project_path(args.output_csv)
    insightface_root = Path(args.insightface_root).expanduser().resolve()

    assert_local_insightface_model(insightface_root, args.model_name)
    app = load_face_analysis(
        args.model_name,
        insightface_root,
        parse_providers(args.providers),
    )
    app.prepare(ctx_id=args.ctx_id, det_size=(args.det_size, args.det_size))

    records = iter_safe_image_records(index_path, keywords)
    rows: list[dict[str, str]] = []
    skipped_low_score = 0
    images_without_faces = 0

    for source_path, person_id in records:
        image = load_rgb_image(source_path)
        faces = app.get(image_to_bgr_array(image))
        if not faces:
            images_without_faces += 1
            continue

        for face_index, face in enumerate(faces):
            raw_bbox = getattr(face, "bbox", None)
            if raw_bbox is None:
                continue
            bbox_values = tuple(float(value) for value in raw_bbox[:4])
            det_score = float(getattr(face, "det_score", 0.0))
            quality_score = estimate_face_quality(
                bbox_values,
                det_score,
                image.width,
                image.height,
            )
            if det_score < args.min_det_score:
                skipped_low_score += 1
                continue

            crop_id = make_crop_id(source_path, face_index, bbox_values)
            crop_dir = output_dir / safe_label(person_id)
            crop_path = crop_dir / f"{crop_id}.jpg"

            if args.overwrite or not crop_path.exists():
                crop_dir.mkdir(parents=True, exist_ok=True)
                crop = crop_face(image, bbox_values, args.crop_size, args.margin_scale)
                crop.save(crop_path, quality=95)

            use_for_faceid = "yes" if quality_score >= args.min_quality_score else "review"
            rows.append(
                {
                    "crop_id": crop_id,
                    "source_path": str(source_path),
                    "crop_path": str(crop_path),
                    "bbox_x1": str(int(round(bbox_values[0]))),
                    "bbox_y1": str(int(round(bbox_values[1]))),
                    "bbox_x2": str(int(round(bbox_values[2]))),
                    "bbox_y2": str(int(round(bbox_values[3]))),
                    "face_quality_score": format_float(quality_score),
                    "face_det_score": format_float(det_score),
                    "source_person_id": person_id,
                    "use_for_faceid": use_for_faceid,
                    "use_for_identity_lora": "no",
                    "notes": (
                        "P0.5 crop keeps hair/chin context; identity LoRA is not enabled"
                    ),
                }
            )

    write_rows(rows, output_csv)
    print(f"Read index: {index_path}")
    print(f"Safe image records: {len(records)}")
    print(f"Wrote crops: {len(rows)}")
    print(f"Images without faces: {images_without_faces}")
    print(f"Faces skipped by det score: {skipped_low_score}")
    print(f"Wrote crop metadata: {output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
