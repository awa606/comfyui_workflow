from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from p0_common import METADATA_DIR, blur_score, ensure_dirs, hamming_hex, phash, read_csv, read_image, resolve_path, write_csv


FIELDNAMES = [
    "asset_id",
    "asset_type",
    "file_id",
    "frame_id",
    "image_path",
    "phash",
    "blur_score",
    "duplicate_group_id",
    "near_duplicate_group_id",
    "duplicate_level",
    "is_duplicate",
    "representative_asset_id",
    "notes",
]


class DisjointSet:
    def __init__(self, values: list[str]) -> None:
        self.parent = {value: value for value in values}

    def find(self, value: str) -> str:
        parent = self.parent[value]
        if parent != value:
            self.parent[value] = self.find(parent)
        return self.parent[value]

    def union(self, left: str, right: str) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            self.parent[right_root] = left_root


class BKNode:
    def __init__(self, value: str) -> None:
        self.value = value
        self.children: dict[int, BKNode] = {}


class BKTree:
    def __init__(self) -> None:
        self.root: BKNode | None = None

    def add(self, value: str) -> None:
        if self.root is None:
            self.root = BKNode(value)
            return
        node = self.root
        while True:
            distance = hamming_hex(value, node.value)
            child = node.children.get(distance)
            if child is None:
                node.children[distance] = BKNode(value)
                return
            node = child

    def query(self, value: str, max_distance: int) -> list[tuple[str, int]]:
        if self.root is None:
            return []
        matches: list[tuple[str, int]] = []
        stack = [self.root]
        while stack:
            node = stack.pop()
            distance = hamming_hex(value, node.value)
            if distance <= max_distance:
                matches.append((node.value, distance))
            low = distance - max_distance
            high = distance + max_distance
            for edge_distance, child in node.children.items():
                if low <= edge_distance <= high:
                    stack.append(child)
        return matches


def visual_assets(inventory: list[dict[str, str]], frames: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in inventory:
        if row.get("source_type") == "image" and row.get("scan_status") == "ok":
            rows.append(
                {
                    "asset_id": row["file_id"],
                    "asset_type": "source_image",
                    "file_id": row["file_id"],
                    "frame_id": "",
                    "image_path": row["source_path"],
                }
            )
    for row in frames:
        if row.get("extract_status") == "ok":
            rows.append(
                {
                    "asset_id": row["frame_id"],
                    "asset_type": "video_frame",
                    "file_id": row["source_file_id"],
                    "frame_id": row["frame_id"],
                    "image_path": row["frame_path"],
                }
            )
    return rows


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P0 step 3: compute pHash, blur, and duplicate groups.")
    parser.add_argument("--inventory", default=str(METADATA_DIR / "source_inventory.csv"))
    parser.add_argument("--frames", default=str(METADATA_DIR / "frame_index.csv"))
    parser.add_argument("--output", default=str(METADATA_DIR / "duplicate_candidates.csv"))
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--near-strong-distance", type=int, default=4)
    parser.add_argument("--near-weak-distance", type=int, default=8)
    return parser


def hash_asset(asset: dict[str, str]) -> dict[str, object]:
    image = read_image(Path(asset["image_path"]))
    image_phash = phash(image)
    return {
        **asset,
        "phash": image_phash,
        "blur_score": f"{blur_score(image):.3f}",
        "duplicate_group_id": "",
        "near_duplicate_group_id": "",
        "duplicate_level": "unique",
        "is_duplicate": "no",
        "representative_asset_id": "",
        "notes": "" if image is not None else "unreadable_image",
    }


def mark_exact_duplicates(groups: dict[str, list[dict[str, object]]]) -> int:
    group_index = 1
    for group_rows in groups.values():
        if len(group_rows) <= 1:
            continue
        group_id = f"dup_{group_index:05d}"
        representative = max(group_rows, key=lambda item: float(item.get("blur_score") or 0))
        for row in group_rows:
            row["duplicate_group_id"] = group_id
            row["representative_asset_id"] = representative["asset_id"]
            if row["asset_id"] == representative["asset_id"]:
                row["is_duplicate"] = "no"
            else:
                row["is_duplicate"] = "yes"
                row["duplicate_level"] = "exact_duplicate"
        group_index += 1
    return group_index - 1


def mark_near_duplicates(groups: dict[str, list[dict[str, object]]], strong_distance: int, weak_distance: int) -> int:
    hashes = sorted(phash_value for phash_value in groups if phash_value)
    if not hashes:
        return 0

    tree = BKTree()
    for item in hashes:
        tree.add(item)

    dsu = DisjointSet(hashes)
    best_distance: dict[str, int] = {item: 65 for item in hashes}
    seen_pairs: set[tuple[str, str]] = set()
    for item in hashes:
        for other, distance in tree.query(item, weak_distance):
            if other == item:
                continue
            pair = tuple(sorted((item, other)))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            dsu.union(item, other)
            best_distance[item] = min(best_distance[item], distance)
            best_distance[other] = min(best_distance[other], distance)

    components: dict[str, list[str]] = {}
    for item in hashes:
        components.setdefault(dsu.find(item), []).append(item)

    near_group_index = 1
    for component in sorted((items for items in components.values() if len(items) > 1), key=lambda items: (-len(items), items[0])):
        near_group_id = f"near_{near_group_index:05d}"
        for hash_value in component:
            if best_distance[hash_value] <= strong_distance:
                near_level = "near_duplicate_strong"
            else:
                near_level = "near_duplicate_weak"
            for row in groups[hash_value]:
                row["near_duplicate_group_id"] = near_group_id
                if row.get("duplicate_level") != "exact_duplicate":
                    row["duplicate_level"] = near_level
        near_group_index += 1
    return near_group_index - 1


def main() -> int:
    args = build_parser().parse_args()
    ensure_dirs()
    assets = visual_assets(read_csv(resolve_path(args.inventory)), read_csv(resolve_path(args.frames)))
    rows: list[dict[str, object]] = []
    groups: dict[str, list[dict[str, object]]] = {}
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = [executor.submit(hash_asset, asset) for asset in assets]
        for index, future in enumerate(as_completed(futures), start=1):
            row = future.result()
            rows.append(row)
            image_phash = str(row.get("phash") or "")
            if image_phash:
                groups.setdefault(image_phash, []).append(row)
            if index % 500 == 0 or index == len(futures):
                print(f"Hashed {index}/{len(futures)} visual assets", flush=True)

    exact_groups = mark_exact_duplicates(groups)
    near_groups = mark_near_duplicates(groups, args.near_strong_distance, args.near_weak_distance)

    output_path = resolve_path(args.output)
    write_csv(output_path, FIELDNAMES, rows)
    print(f"Wrote {output_path}")
    print(f"Visual assets: {len(rows)}")
    print(f"Exact duplicate groups: {exact_groups}")
    print(f"Near duplicate groups: {near_groups}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
