from __future__ import annotations

import argparse
import csv
import hashlib
import math
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import cv2  # type: ignore
import numpy as np


PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_ROOTS = [
    PROJECT_DIR.parent / "train_material",
    PROJECT_DIR.parent / "douyin_download",
]
PRIMARY_SOURCE_DIR = PROJECT_DIR.parent / "douyin_download" / "\u5c0f\u7f8a\u7ef5\u7ef5\u51b0"
SECONDARY_SOURCE_DIR = PROJECT_DIR.parent / "train_material" / "\u5c0f\u6069"
DEFAULT_SOURCE_CANDIDATES = [
    PRIMARY_SOURCE_DIR,
    SECONDARY_SOURCE_DIR,
]
DEFAULT_SOURCE_DIR = next(
    (path for path in DEFAULT_SOURCE_CANDIDATES if path.exists()),
    PRIMARY_SOURCE_DIR,
)
DEFAULT_ROLE_DIR = PROJECT_DIR / "characters" / "role_001"
DEFAULT_LIBRARY_DIR = PROJECT_DIR / "asset_library"
DEFAULT_FACE_MODEL_ROOT = Path("D:/sd.webui/ComfyUI/models/insightface")

VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".wmv"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}

ROLE_DIRS = [
    "raw_images",
    "raw_videos",
    "extracted_frames",
    "identity_faces",
    "upper_body",
    "full_body",
    "body_reference",
    "outfits/outfit_001",
    "outfits/outfit_002",
    "outfits/outfit_003",
    "hairstyles",
    "makeup",
    "shoes_accessories",
    "pose_refs",
    "scene_refs",
    "selected_for_faceid",
    "selected_for_lora",
    "rejected",
    "captions",
    "metadata",
]

ASSET_LIBRARY_DIRS = [
    "identity_faces",
    "body_refs",
    "outfit_refs",
    "hairstyle_refs",
    "makeup_refs",
    "leg_shoes_refs",
    "pose_refs",
    "scene_refs",
    "rejected",
    "metadata",
]

FIELDNAMES = [
    "file_path",
    "source_file",
    "source_root",
    "source_person_id",
    "source_kind",
    "frame_index",
    "timestamp_seconds",
    "category",
    "candidate_dirs",
    "library_dirs",
    "has_face",
    "face_count",
    "face_quality",
    "face_quality_score",
    "face_det_score",
    "face_height_ratio",
    "face_area_ratio",
    "blur_score",
    "body_view",
    "outfit_id",
    "hairstyle",
    "makeup",
    "pose_type",
    "scene",
    "use_for_faceid",
    "use_for_lora",
    "use_for_outfit_ref",
    "use_for_body_ref",
    "use_for_leg_shoes_ref",
    "use_for_pose_ref",
    "notes",
]

KEYWORDS = {
    "outfit_001": [
        "旗袍",
        "新中式",
        "国风",
        "东方",
        "汉服",
        "汉元素",
        "中华娘",
        "古风",
    ],
    "outfit_002": [
        "lolita",
        "洛丽塔",
        "洛可可",
        "公主",
        "小裙子",
        "甜系",
        "草莓",
        "洋娃娃",
    ],
    "outfit_003": [
        "制服",
        "jk",
        "衬衫",
        "西装",
        "通勤",
        "职场",
        "面试",
        "学院",
    ],
    "leg_shoes": ["白丝", "丝袜", "黑丝", "腿", "鞋", "袜", "高跟", "足", "靴"],
    "hairstyle": ["发型", "头发", "刘海", "马尾", "双马尾", "盘发", "卷发"],
    "makeup": ["妆", "妆容", "美妆", "口红", "眼妆", "腮红"],
    "pose": ["舞", "跳", "拍照", "姿势", "坐姿", "手势", "宅舞", "舞蹈"],
    "scene": [
        "海边",
        "湖",
        "江滩",
        "街",
        "房间",
        "室内",
        "办公室",
        "农村",
        "菜地",
        "北京",
        "秋天",
        "春天",
        "夜",
        "公园",
        "学校",
        "毕业",
    ],
    "sensitive": [
        "r18",
        "vip",
        "内裤",
        "蕾丝",
        "护士",
        "捆绑",
        "私房",
        "显性",
    ],
}


@dataclass
class SourceAsset:
    path: Path
    source_root: Path
    source_person_id: str


@dataclass
class FaceStats:
    has_face: bool
    face_count: int = 0
    quality: str = "no_face"
    quality_score: float = 0.0
    det_score: float = 0.0
    height_ratio: float = 0.0
    area_ratio: float = 0.0
    blur_score: float = 0.0
    bbox: tuple[int, int, int, int] | None = None


@dataclass
class FrameItem:
    image_path: Path
    source_file: Path
    source_root: Path
    source_person_id: str
    source_kind: str
    frame_index: int | None
    timestamp_seconds: float | None


def resolve_project_path(value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_DIR / path
    return path.resolve()


def relative_to_project(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_DIR)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def safe_print(message: str, *, error: bool = False) -> None:
    stream = sys.stderr if error else sys.stdout
    try:
        print(message, file=stream)
    except UnicodeEncodeError:
        encoding = stream.encoding or "utf-8"
        safe_message = message.encode(encoding, errors="replace").decode(encoding, errors="replace")
        print(safe_message, file=stream)


def display_default_path(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_DIR))
    except ValueError:
        return str(path)


def safe_name(value: str, max_len: int = 120) -> str:
    value = re.sub(r"[^\w.-]+", "_", value, flags=re.UNICODE).strip("._")
    return (value or "asset")[:max_len]


def safe_ascii_name(value: str, max_len: int = 80) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._")
    return (value or "asset")[:max_len]


def short_hash(path: Path) -> str:
    return hashlib.sha1(str(path).encode("utf-8", errors="ignore")).hexdigest()[:12]


def yes(value: bool) -> str:
    return "yes" if value else "no"


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def keyword_hits(text: str, group: str) -> list[str]:
    low = text.lower()
    return [word for word in KEYWORDS[group] if word.lower() in low]


def first_outfit_id(text: str) -> str:
    for outfit_id in ("outfit_001", "outfit_002", "outfit_003"):
        if keyword_hits(text, outfit_id):
            return outfit_id
    return ""


def read_image(path: Path) -> np.ndarray | None:
    try:
        data = np.fromfile(str(path), dtype=np.uint8)
    except OSError:
        return None
    if data.size == 0:
        return None
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def write_image(path: Path, image: np.ndarray, jpeg_quality: int) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    suffix = path.suffix.lower()
    encode_ext = ".jpg" if suffix in {".jpg", ".jpeg"} else ".png"
    params = (
        [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
        if encode_ext == ".jpg"
        else [int(cv2.IMWRITE_PNG_COMPRESSION), 3]
    )
    ok, encoded = cv2.imencode(encode_ext, image, params)
    if not ok:
        return False
    encoded.tofile(str(path))
    return True


def ascii_video_link(video_path: Path, role_dir: Path) -> Path:
    temp_dir = role_dir / "metadata" / "opencv_video_links"
    temp_dir.mkdir(parents=True, exist_ok=True)
    target = temp_dir / f"{safe_ascii_name(video_path.stem)}_{short_hash(video_path)}{video_path.suffix.lower()}"
    if target.exists():
        return target
    try:
        target.hardlink_to(video_path)
    except OSError:
        shutil.copy2(video_path, target)
    return target


def source_person_id_for(asset_path: Path, source_root: Path) -> str:
    try:
        relative = asset_path.relative_to(source_root)
    except ValueError:
        return source_root.name
    if len(relative.parts) >= 2:
        return relative.parts[0]
    return source_root.name


def iter_assets(source_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in source_dir.rglob("*")
        if path.is_file()
        and path.suffix.lower() in VIDEO_EXTENSIONS.union(IMAGE_EXTENSIONS)
    )


def discover_source_assets(source_dirs: list[Path]) -> list[SourceAsset]:
    discovered: list[SourceAsset] = []
    seen: set[Path] = set()
    for source_dir in source_dirs:
        if not source_dir.exists():
            safe_print(f"WARN: source directory not found, skipped: {source_dir}", error=True)
            continue
        for asset_path in iter_assets(source_dir):
            resolved = asset_path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            discovered.append(
                SourceAsset(
                    path=resolved,
                    source_root=source_dir.resolve(),
                    source_person_id=source_person_id_for(resolved, source_dir.resolve()),
                )
            )
    return sorted(discovered, key=lambda item: (str(item.source_root), item.source_person_id, str(item.path)))


def ensure_role_dirs(role_dir: Path, candidate_subdir: str) -> None:
    for relative in ROLE_DIRS:
        directory = role_dir / relative
        directory.mkdir(parents=True, exist_ok=True)
        gitkeep = directory / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.write_text("\n", encoding="utf-8")

    for relative in candidate_roots(candidate_subdir):
        directory = role_dir / relative
        directory.mkdir(parents=True, exist_ok=True)


def ensure_asset_library_dirs(library_dir: Path, candidate_subdir: str) -> None:
    for relative in ASSET_LIBRARY_DIRS:
        directory = library_dir / relative
        directory.mkdir(parents=True, exist_ok=True)
        gitkeep = directory / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.write_text("\n", encoding="utf-8")

    for base in ASSET_LIBRARY_DIRS:
        if base == "metadata":
            continue
        directory = library_dir / base / candidate_subdir
        directory.mkdir(parents=True, exist_ok=True)


def candidate_roots(candidate_subdir: str) -> list[str]:
    base_dirs = [
        "identity_faces",
        "upper_body",
        "full_body",
        "body_reference",
        "outfits/outfit_001",
        "outfits/outfit_002",
        "outfits/outfit_003",
        "hairstyles",
        "makeup",
        "shoes_accessories",
        "pose_refs",
        "scene_refs",
        "selected_for_faceid",
        "selected_for_lora",
        "rejected",
    ]
    return [str(Path(item) / candidate_subdir).replace("\\", "/") for item in base_dirs]


def load_face_app(model_root: Path, det_size: int):
    try:
        from insightface.app import FaceAnalysis  # type: ignore
    except ImportError:
        safe_print("ERROR: insightface is not installed in this Python environment.", error=True)
        raise SystemExit(2)

    model_dir = model_root / "models" / "buffalo_l"
    if not model_dir.exists():
        raise FileNotFoundError(
            f"InsightFace buffalo_l model not found: {model_dir}. "
            "This script will not download models automatically."
        )

    app = FaceAnalysis(name="buffalo_l", root=str(model_root), providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=-1, det_size=(det_size, det_size))
    return app


def laplacian_score(image: np.ndarray) -> float:
    if image.size == 0:
        return 0.0
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    variance = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    return clamp((variance - 35.0) / 180.0)


def detect_face(image: np.ndarray, face_app) -> FaceStats:
    if face_app is None:
        return FaceStats(has_face=False, quality="not_checked")

    faces = face_app.get(image)
    if not faces:
        return FaceStats(has_face=False, face_count=0, quality="no_face")

    height, width = image.shape[:2]
    face = max(faces, key=lambda item: float((item.bbox[2] - item.bbox[0]) * (item.bbox[3] - item.bbox[1])))
    x1, y1, x2, y2 = [int(round(value)) for value in face.bbox]
    x1 = max(0, min(width - 1, x1))
    x2 = max(0, min(width, x2))
    y1 = max(0, min(height - 1, y1))
    y2 = max(0, min(height, y2))

    face_width = max(1, x2 - x1)
    face_height = max(1, y2 - y1)
    height_ratio = face_height / max(1, height)
    area_ratio = (face_width * face_height) / max(1, width * height)
    crop = image[y1:y2, x1:x2]
    blur_score = laplacian_score(crop)
    det_score = float(getattr(face, "det_score", 0.0) or 0.0)
    size_score = clamp((height_ratio - 0.035) / 0.22)
    quality_score = clamp(0.45 * size_score + 0.35 * blur_score + 0.20 * det_score)

    if quality_score >= 0.72 and height_ratio >= 0.12 and blur_score >= 0.45:
        quality = "high"
    elif quality_score >= 0.52 and height_ratio >= 0.065:
        quality = "medium"
    else:
        quality = "low"

    return FaceStats(
        has_face=True,
        face_count=len(faces),
        quality=quality,
        quality_score=quality_score,
        det_score=det_score,
        height_ratio=height_ratio,
        area_ratio=area_ratio,
        blur_score=blur_score,
        bbox=(x1, y1, x2, y2),
    )


def body_view_for(face: FaceStats) -> str:
    if not face.has_face:
        return "no_face_or_back"
    if face.height_ratio >= 0.28:
        return "face_closeup"
    if face.height_ratio >= 0.13:
        return "upper_body"
    if face.height_ratio >= 0.055:
        return "full_body"
    return "distant_full_body"


def classify_frame(
    item: FrameItem,
    image: np.ndarray,
    face: FaceStats,
    candidate_subdir: str,
    faceid_threshold: float,
    lora_threshold: float,
) -> dict[str, str]:
    text = f"{item.source_file.name} {item.source_file.parent.name}"
    body_view = body_view_for(face)
    outfit_id = first_outfit_id(text)
    leg_hits = keyword_hits(text, "leg_shoes")
    hairstyle_hits = keyword_hits(text, "hairstyle")
    makeup_hits = keyword_hits(text, "makeup")
    pose_hits = keyword_hits(text, "pose")
    scene_hits = keyword_hits(text, "scene")
    sensitive_hits = keyword_hits(text, "sensitive")

    whole_blur = laplacian_score(image)
    use_for_faceid = (
        face.has_face
        and face.quality_score >= faceid_threshold
        and face.height_ratio >= 0.12
        and face.blur_score >= 0.45
    )
    use_for_lora = (
        face.has_face
        and face.quality_score >= lora_threshold
        and face.height_ratio >= 0.065
        and body_view in {"face_closeup", "upper_body", "full_body"}
    )
    use_for_outfit_ref = bool(outfit_id) or body_view in {"upper_body", "full_body", "distant_full_body", "no_face_or_back"}
    use_for_body_ref = body_view in {"upper_body", "full_body", "distant_full_body", "no_face_or_back"}
    use_for_leg_shoes_ref = bool(leg_hits)
    use_for_pose_ref = bool(pose_hits) and body_view != "face_closeup"
    use_for_scene_ref = bool(scene_hits)
    hairstyle = "candidate" if hairstyle_hits or (face.has_face and body_view in {"face_closeup", "upper_body"}) else ""
    makeup = "candidate" if makeup_hits or (face.has_face and body_view == "face_closeup" and face.quality != "low") else ""

    candidate_dirs: list[str] = []
    if use_for_faceid:
        candidate_dirs.append(f"selected_for_faceid/{candidate_subdir}")
    if use_for_lora:
        candidate_dirs.append(f"selected_for_lora/{candidate_subdir}")
        candidate_dirs.append(f"identity_faces/{candidate_subdir}")
    if body_view == "upper_body":
        candidate_dirs.append(f"upper_body/{candidate_subdir}")
    if body_view in {"full_body", "distant_full_body"}:
        candidate_dirs.append(f"full_body/{candidate_subdir}")
    if use_for_body_ref:
        candidate_dirs.append(f"body_reference/{candidate_subdir}")
    if outfit_id:
        candidate_dirs.append(f"outfits/{outfit_id}/{candidate_subdir}")
    if hairstyle:
        candidate_dirs.append(f"hairstyles/{candidate_subdir}")
    if makeup:
        candidate_dirs.append(f"makeup/{candidate_subdir}")
    if use_for_leg_shoes_ref:
        candidate_dirs.append(f"shoes_accessories/{candidate_subdir}")
    if use_for_pose_ref:
        candidate_dirs.append(f"pose_refs/{candidate_subdir}")
    if use_for_scene_ref:
        candidate_dirs.append(f"scene_refs/{candidate_subdir}")

    notes: list[str] = []
    if not face.has_face:
        notes.append("no_face_detected; keep as outfit/body/leg/shoes candidate if visual content is useful")
    if face.quality == "low" and face.has_face:
        notes.append("face_detected_but_low_quality")
    if whole_blur < 0.18:
        notes.append("whole_frame_blurry_review")
    if sensitive_hits:
        notes.append("sensitive_or_explicit_review_keyword; require consent and manual review before any training use")
    if not candidate_dirs:
        candidate_dirs.append(f"rejected/{candidate_subdir}")
        notes.append("no_clear_training_use_auto_rejected")

    person_dir = safe_name(item.source_person_id)
    library_dirs: list[str] = []
    if use_for_faceid or use_for_lora:
        library_dirs.append(f"identity_faces/{person_dir}/{candidate_subdir}")
    if use_for_body_ref:
        library_dirs.append(f"body_refs/{person_dir}/{candidate_subdir}")
    if use_for_outfit_ref:
        library_dirs.append(f"outfit_refs/{person_dir}/{candidate_subdir}")
    if hairstyle:
        library_dirs.append(f"hairstyle_refs/{person_dir}/{candidate_subdir}")
    if makeup:
        library_dirs.append(f"makeup_refs/{person_dir}/{candidate_subdir}")
    if use_for_leg_shoes_ref:
        library_dirs.append(f"leg_shoes_refs/{person_dir}/{candidate_subdir}")
    if use_for_pose_ref:
        library_dirs.append(f"pose_refs/{person_dir}/{candidate_subdir}")
    if use_for_scene_ref:
        library_dirs.append(f"scene_refs/{person_dir}/{candidate_subdir}")
    if not library_dirs:
        library_dirs.append(f"rejected/{person_dir}/{candidate_subdir}")

    category = primary_category(candidate_dirs)

    return {
        "file_path": relative_to_project(item.image_path),
        "source_file": relative_to_project(item.source_file),
        "source_root": relative_to_project(item.source_root),
        "source_person_id": item.source_person_id,
        "source_kind": item.source_kind,
        "frame_index": "" if item.frame_index is None else str(item.frame_index),
        "timestamp_seconds": "" if item.timestamp_seconds is None else f"{item.timestamp_seconds:.3f}",
        "category": category,
        "candidate_dirs": ";".join(dict.fromkeys(candidate_dirs)),
        "library_dirs": ";".join(dict.fromkeys(library_dirs)),
        "has_face": yes(face.has_face),
        "face_count": str(face.face_count),
        "face_quality": face.quality,
        "face_quality_score": f"{face.quality_score:.4f}",
        "face_det_score": f"{face.det_score:.4f}",
        "face_height_ratio": f"{face.height_ratio:.4f}",
        "face_area_ratio": f"{face.area_ratio:.5f}",
        "blur_score": f"{face.blur_score:.4f}",
        "body_view": body_view,
        "outfit_id": outfit_id,
        "hairstyle": hairstyle,
        "makeup": makeup,
        "pose_type": "candidate" if pose_hits else "",
        "scene": "candidate" if scene_hits else "",
        "use_for_faceid": yes(use_for_faceid),
        "use_for_lora": yes(use_for_lora),
        "use_for_outfit_ref": yes(use_for_outfit_ref),
        "use_for_body_ref": yes(use_for_body_ref),
        "use_for_leg_shoes_ref": yes(use_for_leg_shoes_ref),
        "use_for_pose_ref": yes(use_for_pose_ref),
        "notes": "; ".join(notes),
    }


def primary_category(candidate_dirs: list[str]) -> str:
    priority = [
        "selected_for_faceid",
        "selected_for_lora",
        "identity_faces",
        "upper_body",
        "full_body",
        "body_reference",
        "outfits",
        "shoes_accessories",
        "hairstyles",
        "makeup",
        "pose_refs",
        "scene_refs",
        "rejected",
    ]
    for key in priority:
        if any(item.startswith(key) for item in candidate_dirs):
            return key
    return "review"


def link_or_copy(source: Path, target: Path, mode: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        return
    if mode == "manifest-only":
        return
    if mode == "copy":
        shutil.copy2(source, target)
        return
    try:
        target.hardlink_to(source)
    except OSError:
        shutil.copy2(source, target)


def place_candidates(role_dir: Path, row: dict[str, str], image_path: Path, mode: str) -> None:
    if mode == "manifest-only":
        return
    name = image_path.name
    for relative_dir in row["candidate_dirs"].split(";"):
        target = role_dir / relative_dir / name
        link_or_copy(image_path, target, mode)


def place_library_candidates(library_dir: Path, row: dict[str, str], image_path: Path, mode: str) -> None:
    if mode in {"none", "manifest-only"}:
        return
    name = image_path.name
    for relative_dir in row["library_dirs"].split(";"):
        target = library_dir / relative_dir / name
        link_or_copy(image_path, target, mode)


def sample_video(
    video_path: Path,
    role_dir: Path,
    source_root: Path,
    source_person_id: str,
    sample_fps: float,
    max_frames: int,
    jpeg_quality: int,
) -> tuple[list[FrameItem], str]:
    capture_path = ascii_video_link(video_path, role_dir)
    capture = cv2.VideoCapture(str(capture_path))
    if not capture.isOpened():
        capture.release()
        return sample_video_with_av(
            video_path=video_path,
            role_dir=role_dir,
            source_root=source_root,
            source_person_id=source_person_id,
            sample_fps=sample_fps,
            max_frames=max_frames,
            jpeg_quality=jpeg_quality,
        )

    source_fps = float(capture.get(cv2.CAP_PROP_FPS) or 0.0)
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    if source_fps <= 0 or math.isnan(source_fps) or frame_count <= 0:
        capture.release()
        return sample_video_with_av(
            video_path=video_path,
            role_dir=role_dir,
            source_root=source_root,
            source_person_id=source_person_id,
            sample_fps=sample_fps,
            max_frames=max_frames,
            jpeg_quality=jpeg_quality,
        )

    duration = frame_count / source_fps
    interval = 1.0 / sample_fps
    timestamps = [index * interval for index in range(int(duration / interval) + 1)]
    if max_frames > 0 and len(timestamps) > max_frames:
        if max_frames == 1:
            timestamps = [duration / 2]
        else:
            timestamps = np.linspace(0, max(0.0, duration - 0.05), max_frames).tolist()

    video_name = safe_name(video_path.stem)
    output_dir = role_dir / "extracted_frames" / safe_name(source_person_id) / video_name
    output_dir.mkdir(parents=True, exist_ok=True)

    items: list[FrameItem] = []
    try:
        for sample_index, timestamp in enumerate(timestamps, start=1):
            frame_index = int(round(timestamp * source_fps))
            capture.set(cv2.CAP_PROP_POS_FRAMES, min(frame_index, frame_count - 1))
            ok, frame = capture.read()
            if not ok:
                continue

            output_path = output_dir / f"{video_name}_t{timestamp:06.2f}_{sample_index:03d}.jpg"
            if not write_image(output_path, frame, jpeg_quality):
                safe_print(f"WARN: could not write frame: {output_path}", error=True)
                continue
            items.append(
                FrameItem(
                    image_path=output_path,
                    source_file=video_path,
                    source_root=source_root,
                    source_person_id=source_person_id,
                    source_kind="video_frame",
                    frame_index=frame_index,
                    timestamp_seconds=float(timestamp),
                )
            )
    finally:
        capture.release()

    return items, "" if items else "opencv_opened_but_no_frames_extracted"


def sample_video_with_av(
    video_path: Path,
    role_dir: Path,
    source_root: Path,
    source_person_id: str,
    sample_fps: float,
    max_frames: int,
    jpeg_quality: int,
) -> tuple[list[FrameItem], str]:
    try:
        import av  # type: ignore
    except ImportError:
        return [], "opencv_failed_and_pyav_not_installed"

    capture_path = ascii_video_link(video_path, role_dir)
    try:
        container = av.open(str(capture_path))
    except Exception as exc:
        return [], f"video_unreadable: {exc}"

    try:
        if not container.streams.video:
            return [], f"audio_only_or_no_video_stream; audio_streams={len(container.streams.audio)}"

        stream = container.streams.video[0]
        duration = None
        if stream.duration is not None and stream.time_base is not None:
            duration = float(stream.duration * stream.time_base)

        interval = 1.0 / sample_fps
        if duration and max_frames > 0:
            targets = [duration / 2] if max_frames == 1 else np.linspace(0, max(0.0, duration - 0.05), max_frames).tolist()
        else:
            targets = [index * interval for index in range(max_frames or 1_000_000)]

        video_name = safe_name(video_path.stem)
        output_dir = role_dir / "extracted_frames" / safe_name(source_person_id) / video_name
        output_dir.mkdir(parents=True, exist_ok=True)

        items: list[FrameItem] = []
        target_index = 0
        decoded_index = 0
        for frame in container.decode(stream):
            timestamp = float(frame.time) if frame.time is not None else decoded_index * interval
            if target_index < len(targets) and timestamp + 1e-9 >= targets[target_index]:
                image = frame.to_ndarray(format="bgr24")
                output_path = output_dir / f"{video_name}_t{timestamp:06.2f}_{target_index + 1:03d}.jpg"
                if write_image(output_path, image, jpeg_quality):
                    items.append(
                        FrameItem(
                            image_path=output_path,
                            source_file=video_path,
                            source_root=source_root,
                            source_person_id=source_person_id,
                            source_kind="video_frame",
                            frame_index=decoded_index,
                            timestamp_seconds=timestamp,
                        )
                    )
                target_index += 1
                if max_frames > 0 and len(items) >= max_frames:
                    break
                if target_index >= len(targets):
                    break
            decoded_index += 1

        return items, "" if items else "video_stream_found_but_no_frames_decoded"
    finally:
        container.close()


def source_status_row(
    source_file: Path,
    source_root: Path,
    source_person_id: str,
    source_kind: str,
    notes: str,
) -> dict[str, str]:
    row = {field: "" for field in FIELDNAMES}
    row.update(
        {
            "source_file": relative_to_project(source_file),
            "source_root": relative_to_project(source_root),
            "source_person_id": source_person_id,
            "source_kind": source_kind,
            "category": "unreadable_or_audio_only",
            "candidate_dirs": "rejected/candidates",
            "library_dirs": f"rejected/{safe_name(source_person_id)}/candidates",
            "has_face": "no",
            "face_count": "0",
            "face_quality": "not_checked",
            "body_view": "unknown",
            "use_for_faceid": "no",
            "use_for_lora": "no",
            "use_for_outfit_ref": "no",
            "use_for_body_ref": "no",
            "use_for_leg_shoes_ref": "no",
            "use_for_pose_ref": "no",
            "notes": notes,
        }
    )
    return row


def prepare_image_item(
    image_path: Path,
    role_dir: Path,
    source_root: Path,
    source_person_id: str,
) -> FrameItem | None:
    image = read_image(image_path)
    if image is None:
        safe_print(f"WARN: could not read image: {image_path}", error=True)
        return None

    image_name = safe_name(image_path.stem) + ".jpg"
    output_dir = role_dir / "extracted_frames" / safe_name(source_person_id) / "_source_images"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / image_name
    if not write_image(output_path, image, 95):
        safe_print(f"WARN: could not write image: {output_path}", error=True)
        return None
    return FrameItem(
        image_path=output_path,
        source_file=image_path,
        source_root=source_root,
        source_person_id=source_person_id,
        source_kind="source_image",
        frame_index=None,
        timestamp_seconds=None,
    )


def process_items(
    items: Iterable[FrameItem],
    role_dir: Path,
    library_dir: Path,
    face_app,
    candidate_subdir: str,
    copy_mode: str,
    library_copy_mode: str,
    faceid_threshold: float,
    lora_threshold: float,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in items:
        image = read_image(item.image_path)
        if image is None:
            continue
        face = detect_face(image, face_app)
        row = classify_frame(
            item=item,
            image=image,
            face=face,
            candidate_subdir=candidate_subdir,
            faceid_threshold=faceid_threshold,
            lora_threshold=lora_threshold,
        )
        place_candidates(role_dir, row, item.image_path, copy_mode)
        place_library_candidates(library_dir, row, item.image_path, library_copy_mode)
        rows.append(row)
    return rows


def write_manifest(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows: list[dict[str, str]]) -> None:
    def count(field: str, value: str = "yes") -> int:
        return sum(1 for row in rows if row.get(field) == value)

    categories: dict[str, int] = {}
    for row in rows:
        categories[row["category"]] = categories.get(row["category"], 0) + 1

    safe_print(f"Frames/images analyzed: {len(rows)}")
    safe_print(f"FaceID candidates: {count('use_for_faceid')}")
    safe_print(f"Identity LoRA candidates: {count('use_for_lora')}")
    safe_print(f"Outfit reference candidates: {count('use_for_outfit_ref')}")
    safe_print(f"Body reference candidates: {count('use_for_body_ref')}")
    safe_print(f"Leg/shoes candidates: {count('use_for_leg_shoes_ref')}")
    safe_print(f"Pose candidates: {count('use_for_pose_ref')}")
    safe_print("Primary categories:")
    for category, value in sorted(categories.items(), key=lambda item: (-item[1], item[0])):
        safe_print(f"  {category}: {value}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Triage image/video sources into role and shared asset-library candidates."
    )
    parser.add_argument(
        "--source-dir",
        action="append",
        default=None,
        help=(
            "Specific folder to scan. Can be repeated. If omitted, defaults to 小羊绵绵冰 "
            "under douyin_download, falling back to train_material/小恩."
        ),
    )
    parser.add_argument(
        "--source-root",
        action="append",
        default=None,
        help=(
            "Root folder whose first-level subfolders are treated as person/material ids. "
            "Can be repeated, for example D:\\sd.webui\\train_material and D:\\sd.webui\\douyin_download."
        ),
    )
    parser.add_argument(
        "--all-default-roots",
        action="store_true",
        help="Scan existing default roots: D:\\sd.webui\\train_material and D:\\sd.webui\\douyin_download.",
    )
    parser.add_argument(
        "--role-dir",
        default=str(DEFAULT_ROLE_DIR.relative_to(PROJECT_DIR)),
        help="Role asset directory. Defaults to characters/role_001.",
    )
    parser.add_argument(
        "--manifest",
        default="characters/role_001/metadata/triage_manifest.csv",
        help="Output CSV manifest path.",
    )
    parser.add_argument(
        "--library-dir",
        default=str(DEFAULT_LIBRARY_DIR.relative_to(PROJECT_DIR)),
        help="Shared asset library directory. Defaults to asset_library.",
    )
    parser.add_argument(
        "--sample-fps",
        type=float,
        default=1.0,
        help="Frames to sample per second from videos. Defaults to 1.",
    )
    parser.add_argument(
        "--max-frames-per-file",
        type=int,
        default=8,
        help="Maximum sampled frames per video. Use 0 for no cap.",
    )
    parser.add_argument(
        "--limit-files",
        type=int,
        default=0,
        help="Limit source files for a pilot run. Use 0 for all files.",
    )
    parser.add_argument(
        "--candidate-subdir",
        default="candidates",
        help="Subdirectory used under each role category for auto-classified candidates.",
    )
    parser.add_argument(
        "--copy-mode",
        choices=["hardlink", "copy", "manifest-only"],
        default="manifest-only",
        help="How to place frames in role candidate dirs. Defaults to manifest-only for safe pilot runs.",
    )
    parser.add_argument(
        "--library-copy-mode",
        choices=["none", "hardlink", "copy", "manifest-only"],
        default="manifest-only",
        help="How to place frames in asset_library candidate dirs. Defaults to manifest-only.",
    )
    parser.add_argument(
        "--face-model-root",
        default=str(DEFAULT_FACE_MODEL_ROOT),
        help="InsightFace root containing models/buffalo_l. No models are downloaded.",
    )
    parser.add_argument("--det-size", type=int, default=640)
    parser.add_argument("--faceid-threshold", type=float, default=0.72)
    parser.add_argument("--lora-threshold", type=float, default=0.55)
    parser.add_argument("--jpeg-quality", type=int, default=95)
    parser.add_argument(
        "--no-face-detect",
        action="store_true",
        help="Skip InsightFace detection and only build keyword/body-reference candidates.",
    )
    return parser


def selected_source_dirs(args: argparse.Namespace) -> list[Path]:
    values: list[str] = []
    if args.all_default_roots:
        values.extend(str(path) for path in DEFAULT_SOURCE_ROOTS)
    if args.source_root:
        values.extend(args.source_root)
    if args.source_dir:
        values.extend(args.source_dir)
    if not values:
        values.append(display_default_path(DEFAULT_SOURCE_DIR))
    return [resolve_project_path(value) for value in values]


def main() -> int:
    args = build_parser().parse_args()
    if args.sample_fps <= 0:
        raise SystemExit("ERROR: --sample-fps must be greater than 0")
    if args.max_frames_per_file < 0:
        raise SystemExit("ERROR: --max-frames-per-file must be 0 or greater")

    source_dirs = selected_source_dirs(args)
    role_dir = resolve_project_path(args.role_dir)
    library_dir = resolve_project_path(args.library_dir)
    manifest_path = resolve_project_path(args.manifest)

    ensure_role_dirs(role_dir, args.candidate_subdir)
    ensure_asset_library_dirs(library_dir, args.candidate_subdir)
    face_app = None if args.no_face_detect else load_face_app(resolve_project_path(args.face_model_root), args.det_size)

    assets = discover_source_assets(source_dirs)
    if args.limit_files > 0:
        assets = assets[: args.limit_files]
    if not assets:
        safe_print("No video/image assets found in selected source directories.")
        return 0

    rows: list[dict[str, str]] = []
    for index, asset in enumerate(assets, start=1):
        asset_path = asset.path
        source_person_id = asset.source_person_id
        safe_print(f"[{index}/{len(assets)}] {source_person_id}: {asset_path.name}")
        if asset_path.suffix.lower() in VIDEO_EXTENSIONS:
            items, status_note = sample_video(
                video_path=asset_path,
                role_dir=role_dir,
                source_root=asset.source_root,
                source_person_id=source_person_id,
                sample_fps=args.sample_fps,
                max_frames=args.max_frames_per_file,
                jpeg_quality=args.jpeg_quality,
            )
            if not items:
                rows.append(
                    source_status_row(
                        asset_path,
                        asset.source_root,
                        source_person_id,
                        "video_source",
                        status_note,
                    )
                )
                safe_print(f"  WARN: {status_note}", error=True)
                continue
        else:
            item = prepare_image_item(asset_path, role_dir, asset.source_root, source_person_id)
            items = [] if item is None else [item]
        rows.extend(
            process_items(
                items=items,
                role_dir=role_dir,
                library_dir=library_dir,
                face_app=face_app,
                candidate_subdir=args.candidate_subdir,
                copy_mode=args.copy_mode,
                library_copy_mode=args.library_copy_mode,
                faceid_threshold=args.faceid_threshold,
                lora_threshold=args.lora_threshold,
            )
        )

    write_manifest(rows, manifest_path)
    safe_print(f"Wrote manifest: {manifest_path}")
    print_summary(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
