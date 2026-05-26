from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


HF_BASE = "https://huggingface.co"
README_CANDIDATES = ("README.md", "readme.md")


@dataclass
class ModelCardSummary:
    model_name: str
    source_url: str
    task_type: str
    license: str
    files: list[str]
    readme_summary: str


def parse_model_id(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("Model URL or repo id is required")

    if value.startswith("http://") or value.startswith("https://"):
        parsed = urlparse(value)
        if parsed.netloc not in {"huggingface.co", "www.huggingface.co"}:
            raise ValueError("Only Hugging Face model URLs are supported")
        parts = [part for part in parsed.path.split("/") if part]
        if parts[:1] == ["models"]:
            parts = parts[1:]
        if len(parts) < 2:
            raise ValueError("Expected a Hugging Face model URL like https://huggingface.co/org/model")
        return "/".join(parts[:2])

    if re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", value):
        return value

    raise ValueError("Expected a Hugging Face URL or repo id in owner/model format")


def fetch_json(url: str) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "comic-project-model-card-checker/0.1"})
    with urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "comic-project-model-card-checker/0.1"})
    with urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", errors="replace")


def summarize_readme(text: str, max_chars: int) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("---"):
            continue
        if line.startswith("```"):
            continue
        lines.append(line)
        if sum(len(item) for item in lines) >= max_chars:
            break
    summary = " ".join(lines)
    return summary[:max_chars].strip()


def metadata_summary(model_id: str, max_readme_chars: int) -> ModelCardSummary:
    api_url = f"{HF_BASE}/api/models/{model_id}"
    data = fetch_json(api_url)

    siblings = data.get("siblings") or []
    files = sorted(
        item.get("rfilename", "")
        for item in siblings
        if isinstance(item, dict) and item.get("rfilename")
    )

    card_data = data.get("cardData") or {}
    tags = data.get("tags") or []
    pipeline_tag = data.get("pipeline_tag") or card_data.get("pipeline_tag") or ""
    license_name = card_data.get("license") or ""
    if not license_name and isinstance(tags, list):
        license_tags = [tag.removeprefix("license:") for tag in tags if isinstance(tag, str) and tag.startswith("license:")]
        license_name = license_tags[0] if license_tags else "unknown"

    readme_summary = ""
    for readme_name in README_CANDIDATES:
        try:
            text = fetch_text(f"{HF_BASE}/{model_id}/raw/main/{readme_name}")
        except HTTPError as exc:
            if exc.code == 404:
                continue
            raise
        readme_summary = summarize_readme(text, max_readme_chars)
        break

    return ModelCardSummary(
        model_name=model_id,
        source_url=f"{HF_BASE}/{model_id}",
        task_type=pipeline_tag or "unknown",
        license=license_name or "unknown",
        files=files,
        readme_summary=readme_summary or "README not found or empty.",
    )


def offline_summary(model_id: str) -> ModelCardSummary:
    return ModelCardSummary(
        model_name=model_id,
        source_url=f"{HF_BASE}/{model_id}",
        task_type="unknown",
        license="unknown",
        files=[],
        readme_summary="Offline mode: no Hugging Face metadata was fetched.",
    )


def print_summary(summary: ModelCardSummary, max_files: int) -> None:
    print(f"model_name: {summary.model_name}")
    print(f"source_url: {summary.source_url}")
    print(f"task_type: {summary.task_type}")
    print(f"license: {summary.license}")
    print("files:")
    for filename in summary.files[:max_files]:
        print(f"  - {filename}")
    if len(summary.files) > max_files:
        print(f"  ... {len(summary.files) - max_files} more")
    print("README_summary:")
    print(summary.readme_summary)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect Hugging Face model card metadata without downloading model weights. "
            "Fetches only the model API JSON and README text unless --offline is used."
        )
    )
    parser.add_argument("model", help="Hugging Face model URL or owner/model repo id.")
    parser.add_argument("--offline", action="store_true", help="Only parse the repo id; do not contact Hugging Face.")
    parser.add_argument("--max-files", type=int, default=80, help="Maximum filenames to print.")
    parser.add_argument("--max-readme-chars", type=int, default=1200, help="README summary length.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        model_id = parse_model_id(args.model)
        summary = offline_summary(model_id) if args.offline else metadata_summary(model_id, args.max_readme_chars)
    except (ValueError, HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print_summary(summary, args.max_files)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
