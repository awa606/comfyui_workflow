from __future__ import annotations

import argparse
from pathlib import Path

from p0_common import (
    DEFAULT_SOURCE_ROOTS,
    METADATA_DIR,
    IMAGE_EXTENSIONS,
    VIDEO_EXTENSIONS,
    as_posix,
    ensure_dirs,
    file_sha1,
    image_info,
    iter_media_files,
    now_iso,
    resolve_path,
    source_person_id_for,
    video_info,
    write_csv,
)


FIELDNAMES = [
    "file_id",
    "source_root",
    "source_person_id",
    "source_path",
    "source_type",
    "ext",
    "file_size",
    "width",
    "height",
    "duration_seconds",
    "fps",
    "frame_count",
    "file_sha1",
    "scan_status",
    "notes",
    "indexed_at",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P0 step 1: scan source image/video files.")
    parser.add_argument("--source-root", action="append", default=None)
    parser.add_argument("--output", default=str(METADATA_DIR / "source_inventory.csv"))
    parser.add_argument("--skip-hash", action="store_true", help="Skip full file sha1 hashing for faster dry runs.")
    parser.add_argument(
        "--probe-image-info",
        action="store_true",
        help="Open each image to read width/height. Off by default for fast indexing.",
    )
    parser.add_argument(
        "--probe-video-info",
        action="store_true",
        help="Open each video to read duration/fps. Off by default because large source trees can be slow.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    ensure_dirs()
    roots = [resolve_path(item) for item in args.source_root] if args.source_root else DEFAULT_SOURCE_ROOTS
    rows: list[dict[str, object]] = []
    for index, (root, path) in enumerate(iter_media_files(roots), start=1):
        ext = path.suffix.lower()
        source_type = "image" if ext in IMAGE_EXTENSIONS else "video"
        file_id = f"src_{index:07d}"
        try:
            stat = path.stat()
            if ext in IMAGE_EXTENSIONS:
                if args.probe_image_info:
                    width, height, note = image_info(path)
                else:
                    width, height, note = 0, 0, ""
                duration, fps, frame_count = 0.0, 0.0, 0
            elif ext in VIDEO_EXTENSIONS:
                if args.probe_video_info:
                    width, height, duration, fps, frame_count, note = video_info(path)
                else:
                    width, height, duration, fps, frame_count, note = 0, 0, 0.0, 0.0, 0, ""
            else:
                continue
            rows.append(
                {
                    "file_id": file_id,
                    "source_root": as_posix(root),
                    "source_person_id": source_person_id_for(path, root),
                    "source_path": as_posix(path),
                    "source_type": source_type,
                    "ext": ext,
                    "file_size": stat.st_size,
                    "width": width,
                    "height": height,
                    "duration_seconds": f"{duration:.3f}",
                    "fps": f"{fps:.3f}",
                    "frame_count": frame_count,
                    "file_sha1": "" if args.skip_hash else file_sha1(path),
                    "scan_status": "ok" if not note else note,
                    "notes": "",
                    "indexed_at": now_iso(),
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "file_id": file_id,
                    "source_root": as_posix(root),
                    "source_person_id": source_person_id_for(path, root),
                    "source_path": as_posix(path),
                    "source_type": source_type,
                    "ext": ext,
                    "scan_status": "error",
                    "notes": str(exc),
                    "indexed_at": now_iso(),
                }
            )

    output_path = resolve_path(args.output)
    write_csv(output_path, FIELDNAMES, rows)
    image_count = sum(1 for row in rows if row["source_type"] == "image")
    video_count = sum(1 for row in rows if row["source_type"] == "video")
    print(f"Wrote {output_path}")
    print(f"Images: {image_count}")
    print(f"Videos: {video_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
