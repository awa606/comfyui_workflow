from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import subprocess
import sys

import cv2  # type: ignore
import numpy as np

from p0_common import (
    FRAME_DIR,
    METADATA_DIR,
    as_posix,
    ascii_video_link,
    ensure_dirs,
    read_csv,
    resolve_path,
    safe_name,
    write_csv,
    write_image,
)


FIELDNAMES = [
    "frame_id",
    "source_file_id",
    "source_path",
    "source_person_id",
    "frame_path",
    "frame_index",
    "timestamp_seconds",
    "width",
    "height",
    "extract_status",
    "notes",
]


def timestamps_for(duration: float, fps: float, max_frames: int) -> list[float]:
    if duration <= 0:
        return [0.0]
    interval = 1.0 / fps
    values = [i * interval for i in range(int(duration / interval) + 1)]
    if max_frames > 0 and len(values) > max_frames:
        if max_frames == 1:
            return [duration / 2]
        return np.linspace(0, max(0.0, duration - 0.05), max_frames).tolist()
    return values


def extract_video(row: dict[str, str], sample_fps: float, max_frames: int) -> list[dict[str, object]]:
    source_path = Path(row["source_path"])
    video_path = ascii_video_link(source_path)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return [
            {
                "source_file_id": row["file_id"],
                "source_path": row["source_path"],
                "source_person_id": row["source_person_id"],
                "extract_status": "unreadable",
                "notes": "opencv_open_failed",
            }
        ]

    source_fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    duration = frame_count / source_fps if source_fps > 0 else 0.0
    out_dir = FRAME_DIR / safe_name(row["source_person_id"]) / row["file_id"]
    rows: list[dict[str, object]] = []
    try:
        for sample_index, timestamp in enumerate(timestamps_for(duration, sample_fps, max_frames), start=1):
            frame_index = int(round(timestamp * source_fps)) if source_fps > 0 else 0
            if frame_count > 0:
                frame_index = min(frame_index, frame_count - 1)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ok, frame = cap.read()
            if not ok:
                continue
            frame_id = f"{row['file_id']}_f{sample_index:04d}"
            frame_path = out_dir / f"{frame_id}.jpg"
            if not write_image(frame_path, frame):
                continue
            height, width = frame.shape[:2]
            rows.append(
                {
                    "frame_id": frame_id,
                    "source_file_id": row["file_id"],
                    "source_path": row["source_path"],
                    "source_person_id": row["source_person_id"],
                    "frame_path": as_posix(frame_path),
                    "frame_index": frame_index,
                    "timestamp_seconds": f"{timestamp:.3f}",
                    "width": width,
                    "height": height,
                    "extract_status": "ok",
                    "notes": "",
                }
            )
    finally:
        cap.release()
    return rows


def extract_one_with_timeout(row: dict[str, str], timeout_seconds: int) -> list[dict[str, object]]:
    frame_id = f"{row['file_id']}_f0001"
    existing = FRAME_DIR / safe_name(row["source_person_id"]) / row["file_id"] / f"{frame_id}.jpg"
    if existing.exists():
        return [
            {
                "frame_id": frame_id,
                "source_file_id": row["file_id"],
                "source_path": row["source_path"],
                "source_person_id": row["source_person_id"],
                "frame_path": as_posix(existing),
                "frame_index": 0,
                "timestamp_seconds": "0.000",
                "width": "",
                "height": "",
                "extract_status": "ok",
                "notes": "existing_frame",
            }
        ]
    command = [
        sys.executable,
        str(Path(__file__).with_name("extract_single_video_frame.py")),
        "--file-id",
        row["file_id"],
        "--source-path",
        row["source_path"],
        "--source-person-id",
        row["source_person_id"],
        "--output-root",
        str(FRAME_DIR),
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        return [
            {
                "source_file_id": row["file_id"],
                "source_path": row["source_path"],
                "source_person_id": row["source_person_id"],
                "extract_status": "timeout",
                "notes": f"timeout_after_{timeout_seconds}s",
            }
        ]
    if result.returncode != 0:
        return [
            {
                "source_file_id": row["file_id"],
                "source_path": row["source_path"],
                "source_person_id": row["source_person_id"],
                "extract_status": "error",
                "notes": result.stderr.strip()[:500],
            }
        ]
    try:
        return [json.loads(result.stdout.strip().splitlines()[-1])]
    except Exception as exc:
        return [
            {
                "source_file_id": row["file_id"],
                "source_path": row["source_path"],
                "source_person_id": row["source_person_id"],
                "extract_status": "error",
                "notes": f"invalid_worker_output: {exc}",
            }
        ]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P0 step 2: extract video frames.")
    parser.add_argument("--inventory", default=str(METADATA_DIR / "source_inventory.csv"))
    parser.add_argument("--output", default=str(METADATA_DIR / "frame_index.csv"))
    parser.add_argument("--fps", type=float, default=1.0)
    parser.add_argument(
        "--max-frames-per-video",
        type=int,
        default=8,
        help="Verification cap. Use 0 to extract every sampled frame.",
    )
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=20,
        help="Per-video timeout for one-frame verification extraction. Use 0 for in-process extraction.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    ensure_dirs()
    inventory = read_csv(resolve_path(args.inventory))
    videos = [row for row in inventory if row.get("source_type") == "video" and row.get("scan_status") == "ok"]
    rows: list[dict[str, object]] = []
    use_timeout_worker = args.timeout_seconds > 0 and args.max_frames_per_video == 1
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        if use_timeout_worker:
            futures = [executor.submit(extract_one_with_timeout, row, args.timeout_seconds) for row in videos]
        else:
            futures = [executor.submit(extract_video, row, args.fps, args.max_frames_per_video) for row in videos]
        for index, future in enumerate(as_completed(futures), start=1):
            rows.extend(future.result())
            if index % 100 == 0 or index == len(futures):
                print(f"Processed videos: {index}/{len(futures)}")
    output_path = resolve_path(args.output)
    write_csv(output_path, FIELDNAMES, rows)
    print(f"Wrote {output_path}")
    print(f"Extracted frames: {sum(1 for row in rows if row.get('extract_status') == 'ok')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
