from __future__ import annotations

import csv
import hashlib
import json
import math
import shutil
from datetime import datetime
from pathlib import Path
from typing import Iterable

import cv2  # type: ignore
import numpy as np


PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_ROOTS = [
    Path("D:/sd.webui/train_material"),
    Path("D:/sd.webui/douyin_download"),
]
METADATA_DIR = PROJECT_DIR / "metadata"
OUTPUTS_DIR = PROJECT_DIR / "outputs"
FRAME_DIR = OUTPUTS_DIR / "p0_extracted_frames"
CONTACT_SHEET_DIR = OUTPUTS_DIR / "cluster_contact_sheets"
FACE_MODEL_ROOT = Path("D:/sd.webui/ComfyUI/models/insightface")

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".wmv"}


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def ensure_dirs() -> None:
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    FRAME_DIR.mkdir(parents=True, exist_ok=True)
    CONTACT_SHEET_DIR.mkdir(parents=True, exist_ok=True)


def resolve_path(value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_DIR / path
    return path.resolve()


def as_posix(path: str | Path) -> str:
    return str(path).replace("\\", "/")


def safe_name(value: str, max_len: int = 90) -> str:
    import re

    cleaned = re.sub(r"[^\w.-]+", "_", value, flags=re.UNICODE).strip("._")
    return (cleaned or "asset")[:max_len]


def source_person_id_for(path: Path, root: Path) -> str:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return root.name
    return relative.parts[0] if len(relative.parts) >= 2 else root.name


def iter_media_files(roots: Iterable[Path]) -> Iterable[tuple[Path, Path]]:
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS.union(VIDEO_EXTENSIONS):
                yield root.resolve(), path.resolve()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})


def file_sha1(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_image(path: Path) -> np.ndarray | None:
    try:
        data = np.fromfile(str(path), dtype=np.uint8)
    except OSError:
        return None
    if data.size == 0:
        return None
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def write_image(path: Path, image: np.ndarray, jpeg_quality: int = 92) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    ok, encoded = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
    if not ok:
        return False
    encoded.tofile(str(path))
    return True


def image_info(path: Path) -> tuple[int, int, str]:
    image = read_image(path)
    if image is None:
        return 0, 0, "unreadable"
    height, width = image.shape[:2]
    return width, height, ""


def video_info(path: Path) -> tuple[int, int, float, float, int, str]:
    link_path = ascii_video_link(path)
    cap = cv2.VideoCapture(str(link_path))
    if not cap.isOpened():
        cap.release()
        return 0, 0, 0.0, 0.0, 0, "unreadable"
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    duration = frame_count / fps if fps > 0 else 0.0
    cap.release()
    return width, height, duration, fps, frame_count, ""


def ascii_video_link(video_path: Path) -> Path:
    link_dir = METADATA_DIR / "_opencv_video_links"
    link_dir.mkdir(parents=True, exist_ok=True)
    suffix = video_path.suffix.lower()
    digest = hashlib.sha1(str(video_path).encode("utf-8", errors="ignore")).hexdigest()[:12]
    target = link_dir / f"{safe_name(video_path.stem)}_{digest}{suffix}"
    if target.exists():
        return target
    try:
        target.hardlink_to(video_path)
    except OSError:
        shutil.copy2(video_path, target)
    return target


def blur_score(image: np.ndarray | None) -> float:
    if image is None or image.size == 0:
        return 0.0
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def phash(image: np.ndarray | None) -> str:
    if image is None or image.size == 0:
        return ""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (32, 32), interpolation=cv2.INTER_AREA)
    dct = cv2.dct(np.float32(resized))
    block = dct[:8, :8]
    median = float(np.median(block[1:, 1:]))
    bits = block > median
    value = 0
    for bit in bits.flatten():
        value = (value << 1) | int(bool(bit))
    return f"{value:016x}"


def hamming_hex(left: str, right: str) -> int:
    if not left or not right:
        return 64
    return int(left, 16).bit_count() + int(right, 16).bit_count() - 2 * (int(left, 16) & int(right, 16)).bit_count()


def json_dump(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom <= 0 or math.isnan(denom):
        return 0.0
    return float(np.dot(a, b) / denom)
