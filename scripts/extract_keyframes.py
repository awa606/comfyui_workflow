from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".wmv"}


def positive_float(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("--fps must be a number") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("--fps must be greater than 0")
    return parsed


def resolve_project_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_DIR / path
    return path.resolve()


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._") or "video"


def load_cv2():
    try:
        import cv2  # type: ignore
    except ImportError:
        print(
            "ERROR: OpenCV is not installed. Install it with:\n"
            "D:\\sd.webui\\ComfyUI\\venv\\Scripts\\python.exe -m pip install opencv-python",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return cv2


def iter_videos(input_dir: Path) -> list[Path]:
    if not input_dir.exists():
        return []
    return sorted(
        path
        for path in input_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS
    )


def extract_video(video_path: Path, output_root: Path, target_fps: float) -> int:
    cv2 = load_cv2()

    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    source_fps = float(capture.get(cv2.CAP_PROP_FPS) or 0.0)
    if source_fps <= 0 or math.isnan(source_fps):
        capture.release()
        raise RuntimeError(f"Could not determine source FPS: {video_path}")

    video_stem = safe_name(video_path.stem)
    output_dir = output_root / video_stem
    output_dir.mkdir(parents=True, exist_ok=True)

    interval_seconds = 1.0 / target_fps
    next_capture_time = 0.0
    frame_index = 0
    saved_count = 0

    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break

            timestamp_seconds = frame_index / source_fps
            if timestamp_seconds + 1e-9 >= next_capture_time:
                saved_count += 1
                output_path = output_dir / f"{video_stem}_{saved_count:04d}.png"
                if not cv2.imwrite(str(output_path), frame):
                    raise RuntimeError(f"Could not write frame: {output_path}")
                next_capture_time += interval_seconds

            frame_index += 1
    finally:
        capture.release()

    return saved_count


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract keyframes from every video in datasets/linwei/raw_videos."
    )
    parser.add_argument(
        "--input-dir",
        default="datasets/linwei/raw_videos",
        help="Directory containing source videos. Defaults to datasets/linwei/raw_videos.",
    )
    parser.add_argument(
        "--output-dir",
        default="datasets/linwei/extracted_frames",
        help="Directory for extracted frames. Defaults to datasets/linwei/extracted_frames.",
    )
    parser.add_argument(
        "--fps",
        default=1.0,
        type=positive_float,
        help="Frames to extract per second. Defaults to 1.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    input_dir = resolve_project_path(args.input_dir)
    output_dir = resolve_project_path(args.output_dir)

    videos = iter_videos(input_dir)
    if not videos:
        print(f"No videos found in: {input_dir}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    for video_path in videos:
        try:
            count = extract_video(video_path, output_dir, args.fps)
        except Exception as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        total += count
        print(f"{video_path.name}: extracted {count} frames")

    print(f"Extracted {total} frames from {len(videos)} video(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
