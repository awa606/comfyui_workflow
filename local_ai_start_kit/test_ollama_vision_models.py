#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import base64
import json
import time
from pathlib import Path

import requests


DEFAULT_PROMPT = """
你是图像风格分析模型。请看这张参考图，严格输出 JSON，不要输出 Markdown。

字段：
{
  "can_see_image": true,
  "style_summary_zh": "一句话说明画风",
  "medium": ["媒介/画法"],
  "composition": ["构图和镜头"],
  "linework": ["线条/轮廓/笔触"],
  "color_lighting": ["色彩和光影"],
  "texture": ["材质/颗粒/纸感/胶片感"],
  "subject_vs_style": {
    "content_specific": ["只属于这张图内容的东西"],
    "style_transferable": ["可以迁移到新图的风格规律"]
  },
  "sdxl_positive": ["英文正向提示词短语"],
  "sdxl_negative": ["英文负面提示词短语"],
  "flux_positive_controls": ["FLUX 用正向控制词，不要写 no/without/avoid"],
  "score_for_style_extraction": 0
}
"""


def encode_image(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def call_ollama(host: str, model: str, image: Path, prompt: str, temperature: float = 0.1):
    url = host.rstrip("/") + "/api/chat"
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [encode_image(image)],
            }
        ],
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }
    t0 = time.time()
    r = requests.post(url, json=payload, timeout=240)
    seconds = time.time() - t0
    r.raise_for_status()
    data = r.json()
    return data.get("message", {}).get("content", ""), seconds


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True, help="测试图片路径")
    ap.add_argument("--models", required=True, help="逗号分隔，例如 qwen3-vl:4b,qwen3-vl:8b")
    ap.add_argument("--host", default="http://localhost:11434")
    ap.add_argument("--prompt-file", default="")
    args = ap.parse_args()

    image = Path(args.image)
    if not image.exists():
        raise FileNotFoundError(image)

    prompt = DEFAULT_PROMPT
    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8")

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    results = []

    for model in models:
        print(f"\n=== Testing {model} ===")
        item = {"model": model}
        try:
            content, seconds = call_ollama(args.host, model, image, prompt)
            item["seconds"] = round(seconds, 2)
            item["raw"] = content
            print(f"OK: {seconds:.2f}s")
            print(content[:1000])
        except Exception as e:
            item["error"] = str(e)
            print(f"ERROR: {e}")
        results.append(item)

    out_json = Path("ollama_vision_test_results.json")
    out_md = Path("ollama_vision_test_results.md")

    out_json.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Ollama Vision Test Results", "", f"Image: `{image}`", ""]
    for r in results:
        lines.append(f"## {r['model']}")
        if "error" in r:
            lines.append(f"Error: `{r['error']}`")
        else:
            lines.append(f"Seconds: {r['seconds']}")
            lines.append("")
            lines.append("```text")
            lines.append(r["raw"])
            lines.append("```")
        lines.append("")
    out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nSaved: {out_json.resolve()}")
    print(f"Saved: {out_md.resolve()}")


if __name__ == "__main__":
    main()
