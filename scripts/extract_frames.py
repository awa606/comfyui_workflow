from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]


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


def extract_frames(input_path: Path, output_dir: Path, target_fps: float) -> int:
    cv2 = load_cv2()

    if not input_path.exists():
        raise FileNotFoundError(f"Input video not found: {input_path}")
    if not input_path.is_file():
        raise ValueError(f"Input path is not a file: {input_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    capture = cv2.VideoCapture(str(input_path))
    if not capture.isOpened():
        raise RuntimeError(f"Could not open video: {input_path}")

    source_fps = float(capture.get(cv2.CAP_PROP_FPS) or 0.0)
    if source_fps <= 0 or math.isnan(source_fps):
        capture.release()
        raise RuntimeError("Could not determine source video FPS")

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
                output_path = output_dir / f"frame_{saved_count:04d}.png"
                if not cv2.imwrite(str(output_path), frame):
                    raise RuntimeError(f"Could not write frame: {output_path}")
                next_capture_time += interval_seconds

            frame_index += 1
    finally:
        capture.release()

    return saved_count


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract PNG frames from a video at a target FPS."
    )
    parser.add_argument("--input", required=True, help="Input video path.")
    parser.add_argument(
        "--output",
        default="video_frames",
        help="Output directory. Defaults to video_frames.",
    )
    parser.add_argument(
        "--fps",
        default=1.0,
        type=positive_float,
        help="Frames to extract per second. Defaults to 1.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_path = resolve_project_path(args.input)
    output_dir = resolve_project_path(args.output)

    try:
        count = extract_frames(input_path, output_dir, args.fps)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Extracted {count} frames")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
