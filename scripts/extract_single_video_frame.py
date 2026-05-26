from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2  # type: ignore

from p0_common import ascii_video_link, as_posix, read_csv, resolve_path, safe_name, write_image


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract one frame from one video for the P0 pipeline.")
    parser.add_argument("--file-id", required=True)
    parser.add_argument("--source-path", required=True)
    parser.add_argument("--source-person-id", required=True)
    parser.add_argument("--output-root", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    source_path = Path(args.source_path)
    output_root = resolve_path(args.output_root)
    frame_id = f"{args.file_id}_f0001"
    frame_path = output_root / safe_name(args.source_person_id) / args.file_id / f"{frame_id}.jpg"

    if frame_path.exists():
        image = cv2.imread(str(frame_path))
        width = int(image.shape[1]) if image is not None else 0
        height = int(image.shape[0]) if image is not None else 0
        print(
            json.dumps(
                {
                    "frame_id": frame_id,
                    "source_file_id": args.file_id,
                    "source_path": args.source_path,
                    "source_person_id": args.source_person_id,
                    "frame_path": as_posix(frame_path),
                    "frame_index": 0,
                    "timestamp_seconds": "0.000",
                    "width": width,
                    "height": height,
                    "extract_status": "ok",
                    "notes": "existing_frame",
                },
                ensure_ascii=False,
            )
        )
        return 0

    cap = cv2.VideoCapture(str(ascii_video_link(source_path)))
    if not cap.isOpened():
        print(
            json.dumps(
                {
                    "frame_id": "",
                    "source_file_id": args.file_id,
                    "source_path": args.source_path,
                    "source_person_id": args.source_person_id,
                    "frame_path": "",
                    "frame_index": "",
                    "timestamp_seconds": "",
                    "width": "",
                    "height": "",
                    "extract_status": "unreadable",
                    "notes": "opencv_open_failed",
                },
                ensure_ascii=False,
            )
        )
        return 0
    ok, frame = cap.read()
    cap.release()
    if not ok:
        print(
            json.dumps(
                {
                    "frame_id": "",
                    "source_file_id": args.file_id,
                    "source_path": args.source_path,
                    "source_person_id": args.source_person_id,
                    "frame_path": "",
                    "frame_index": "",
                    "timestamp_seconds": "",
                    "width": "",
                    "height": "",
                    "extract_status": "decode_failed",
                    "notes": "first_frame_read_failed",
                },
                ensure_ascii=False,
            )
        )
        return 0
    height, width = frame.shape[:2]
    write_image(frame_path, frame)
    print(
        json.dumps(
            {
                "frame_id": frame_id,
                "source_file_id": args.file_id,
                "source_path": args.source_path,
                "source_person_id": args.source_person_id,
                "frame_path": as_posix(frame_path),
                "frame_index": 0,
                "timestamp_seconds": "0.000",
                "width": width,
                "height": height,
                "extract_status": "ok",
                "notes": "",
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
