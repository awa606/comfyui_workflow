# P0.5 Main Caption Batch 001 Plan

Generated: 2026-05-30

## Scope

- This is a plan only.
- Model planned: `qwen3-vl:8b`
- Output target: `metadata\p05_caption_results_main_sample.jsonl`
- Queue source: `metadata\p05_caption_queue.csv`
- Quick screen source: `metadata\p05_caption_results_quick_sample.jsonl`
- Manual review source: `docs\02_caption_strategy\p05_quick_screen_manual_review_summary.md`

No model call was run while creating this plan. `metadata\p05_caption_queue.csv` was not modified.

## Current Gate

The quick screen summary status is `REVIEW`, not automatic pass. The `gemma4:e2b` quick sample is technically usable, but many rows contain quality negatives such as `blurry`, `occlusion`, and `low quality`. Therefore, this batch should run only after explicit user confirmation.

## Selection Rules

Batch 001 should select only rows that satisfy all of the following:

1. The source image appeared in `quick_screen`.
2. The derived `usable_for_next_step` value is `yes`.
3. The matching queue row is `image_role=main_caption`.
4. The matching queue row uses `recommended_model=qwen3-vl:8b`.
5. Do not select `face_crop_review`.
6. Do not select `styles\explicit`.
7. Do not select paths containing risk/exclusion keywords:
   - `explicit`
   - `R18`
   - `r18`
   - `03_explicit`
   - `03_explicit_action`
   - `styles\explicit`
   - `VIP`
   - `全裸`
   - `插入`
   - `扩张`
   - `ahegao`
   - `捆绑`
8. First batch size: 30 rows.
9. Prefer `source_person_id=XiaoEn`.
10. Cover different compositions: outdoor, indoor/window, bedroom, half-body, full/lower body, clothing-focused views.

`usable_for_next_step` is derived as:

```text
image_role == quick_screen
AND inference_status == ok
AND error is empty
AND safe_for_p05 == true
```

## Planned Health Check

Run these checks before any `qwen3-vl:8b` caption request:

```powershell
Invoke-RestMethod http://127.0.0.1:11434/api/tags

$body = @{
  model = "qwen3-vl:8b"
  messages = @(@{ role = "user"; content = "ping" })
  stream = $false
} | ConvertTo-Json -Depth 5

Invoke-RestMethod `
  -Uri http://127.0.0.1:11434/api/chat `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

If either check fails, stop and do not run the caption batch.

## Planned Run Command

Do not run until user confirms.

```powershell
python scripts\run_caption_queue_p05.py `
  --queue metadata\p05_caption_queue.csv `
  --output-csv metadata\p05_caption_results_main_sample.csv `
  --output-jsonl metadata\p05_caption_results_main_sample.jsonl `
  --role-limits main_caption=30 `
  --timeout-seconds 300 `
  --ollama-url http://127.0.0.1:11434
```

The original queue CSV must remain unchanged. The output CSV/JSONL are local generated artifacts and must not be committed.

## Planned Selection Summary

| metric | count |
| --- | ---: |
| planned rows | 30 |
| `source_person_id=XiaoEn` | 30 |
| `quick_screen usable_for_next_step=yes` | 30 |
| `face_crop_review` selected | 0 |
| excluded/risk paths selected | 0 |

Composition buckets:

| bucket | count |
| --- | ---: |
| outdoor | 4 |
| indoor window | 21 |
| indoor bedroom | 4 |
| general indoor/portrait | 1 |

Framing buckets:

| bucket | count |
| --- | ---: |
| seated half/full body | 23 |
| full/lower body | 6 |
| half-body/portrait | 1 |

## Planned Rows

| quick row | composition | framing | quick caption | planned image path |
| ---: | --- | --- | --- | --- |
| 1 | outdoor | full/lower body | A person wearing black shorts and a white shirt is standing outdoors on a grassy area. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\17046589594674.jpg` |
| 4 | outdoor | seated half/full body | A young woman with long dark hair is sitting on a concrete ledge outdoors, wearing a white shirt and a black skirt. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\17046589900698.jpg` |
| 7 | indoor window | seated half/full body | A person is sitting in front of a window, wearing a black blazer and red and white striped tie, with a black bag beside them. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\17046590276558.jpg` |
| 10 | indoor window | seated half/full body | A person is sitting next to a window, wearing a black blazer and tie, with a black bag nearby. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\17046590296768.jpg` |
| 13 | indoor window | seated half/full body | A young woman is sitting in front of a window, wearing a dark blazer and tie. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\17046590316106.jpg` |
| 16 | indoor window | seated half/full body | A person is sitting in front of a window, wearing black stockings and a blazer with a red tie, next to a black bag. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\17046590338008.jpg` |
| 19 | indoor window | seated half/full body | A person wearing a black and red striped tie and a white shirt, sitting near a window. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\17046590402679.jpg` |
| 22 | indoor window | seated half/full body | A young woman is sitting in front of a window, wearing a black and white striped shirt and a red tie. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\1704659042653.jpg` |
| 25 | indoor window | seated half/full body | A young woman sitting indoors, wearing a black blazer and red and white striped shirt, looking at the camera. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\17046590588956.jpg` |
| 28 | indoor window | full/lower body | A person is sitting on the floor, wearing black and red pants, leaning against a window. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\17046590607764.jpg` |
| 31 | indoor window | full/lower body | A person is sitting with their legs extended, wearing black and red bottoms, next to a window. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\17046590627416.jpg` |
| 34 | indoor window | seated half/full body | A young woman with long dark hair is sitting in front of a window, wearing a dark blazer and a red and blue striped tie. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\17046590811344.jpg` |
| 37 | indoor bedroom | seated half/full body | A person is sitting on a bed with a gold frame, wearing a black and white striped shirt. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\17046590865895.jpg` |
| 40 | indoor bedroom | full/lower body | A person is sitting on a bed, wearing black shorts and socks, with a light-colored shirt visible. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\17046590954188.jpg` |
| 43 | indoor bedroom | seated half/full body | A person wearing a black blazer and white shirt is sitting on a bed. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\17046590971959.jpg` |
| 46 | indoor window | seated half/full body | A person with long dark hair is sitting in front of a metal grate. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\17046591573067.jpg` |
| 49 | general indoor/portrait | half-body/portrait | A person with long dark hair is leaning against a doorframe, holding a piece of dark fabric. | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[紧急企划] 小恩 - 黑丝\17046591614313.jpg` |
| 154 | outdoor | seated half/full body | A young woman with long dark hair is sitting on a low concrete wall outdoors, wearing a white shirt and black shorts. | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[紧急企划] 小恩 - 黑丝\17046589594674.jpg` |
| 157 | outdoor | seated half/full body | A young woman with long dark hair is sitting on a concrete ledge outdoors, wearing a white shirt and a black skirt. | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[紧急企划] 小恩 - 黑丝\17046589900698.jpg` |
| 160 | indoor window | seated half/full body | A person is sitting in front of a window, wearing a black blazer and red and white striped tie, with a black bag beside them. | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[紧急企划] 小恩 - 黑丝\17046590276558.jpg` |
| 163 | indoor window | seated half/full body | A person is sitting next to a window, wearing a black blazer and tie, with a black bag nearby. | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[紧急企划] 小恩 - 黑丝\17046590296768.jpg` |
| 166 | indoor window | seated half/full body | A young woman is sitting in front of a window, wearing a dark blazer and tie. | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[紧急企划] 小恩 - 黑丝\17046590316106.jpg` |
| 169 | indoor window | seated half/full body | A person is sitting in front of a window, wearing black stockings and a blazer with a red tie, next to a black bag. | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[紧急企划] 小恩 - 黑丝\17046590338008.jpg` |
| 172 | indoor window | seated half/full body | A person wearing a black and red striped tie and a white shirt, sitting near a window. | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[紧急企划] 小恩 - 黑丝\17046590402679.jpg` |
| 175 | indoor window | seated half/full body | A young woman sitting in front of a window, wearing a black and white striped shirt and a red tie. | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[紧急企划] 小恩 - 黑丝\1704659042653.jpg` |
| 178 | indoor window | seated half/full body | A young woman sitting indoors, wearing a black blazer and red and white striped shirt, looking at the camera. | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[紧急企划] 小恩 - 黑丝\17046590588956.jpg` |
| 181 | indoor window | full/lower body | A person is sitting on the floor, wearing black and red pants, leaning against a window. | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[紧急企划] 小恩 - 黑丝\17046590607764.jpg` |
| 184 | indoor window | full/lower body | A person is sitting with their legs extended, wearing black and red bottoms, leaning against a window. | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[紧急企划] 小恩 - 黑丝\17046590627416.jpg` |
| 187 | indoor window | seated half/full body | A young woman with long dark hair is sitting in front of a window, wearing a dark blazer and a red and blue striped tie. | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[紧急企划] 小恩 - 黑丝\17046590811344.jpg` |
| 190 | indoor bedroom | seated half/full body | A person wearing a black and white striped shirt is sitting on a bed. | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[紧急企划] 小恩 - 黑丝\17046590865895.jpg` |

## Notes Before Execution

- This planned batch includes two local source roots that appear to contain overlapping visual material:
  - `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn`
  - `D:\sd.webui\comic_project\training_data_raw\XiaoEn`
- If strict visual de-duplication is required, create a separate deduped plan before running `qwen3-vl:8b`.
- Because the manual quick-screen status is `REVIEW`, user confirmation is required before execution.

## Prohibited Actions

- Do not run full captioning.
- Do not train LoRA.
- Do not run ComfyUI image generation.
- Do not process explicit/R18 paths.
- Do not modify `metadata\p05_caption_queue.csv`.
- Do not commit generated CSV/JSONL outputs.

