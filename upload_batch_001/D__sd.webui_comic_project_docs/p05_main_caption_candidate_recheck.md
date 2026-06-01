# P0.5 Main Caption Candidate Recheck

Generated: 2026-05-31

## Scope

Input file:

- `metadata\p05_caption_results_quick_sample.jsonl`

Corrected candidate filter:

1. Outer `inference_status == "ok"`
2. Outer `error` is empty
3. Parsed `caption_json.safe_for_p05 == true`
4. Parsed `caption_json.needs_manual_review == false`
5. `image_role == "quick_screen"`
6. `source_person_id == "XiaoEn"`

The previous hard filter on `usable_for_next_step=yes` was not used.

## Basic Counts

| Metric | Count |
| --- | ---: |
| quick sample total rows | 60 |
| `image_role=quick_screen` rows | 30 |
| `source_person_id=XiaoEn` rows | 60 |
| corrected candidate count | 30 |

## Enough For 10 Samples

Yes. The corrected filter returns 30 candidates, which is enough to select 10 images for a main caption model comparison.

## Random Candidate Sample

| queue_row_index | image_path | caption summary |
| ---: | --- | --- |
| 4 | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046589900698.jpg` | A young woman with long dark hair is sitting on a concrete ledge outdoors, wearing a white shirt and a black skirt. |
| 10 | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590296768.jpg` | A person is sitting next to a window, wearing a black blazer and tie, with a black bag nearby. |
| 13 | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590316106.jpg` | A young woman is sitting in front of a window, wearing a dark blazer and tie. |
| 16 | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590338008.jpg` | A person is sitting in front of a window, wearing black stockings and a blazer with a red tie, next to a black bag. |
| 34 | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590811344.jpg` | A young woman with long dark hair is sitting in front of a window, wearing a dark blazer and a red and blue striped tie. |
| 40 | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590954188.jpg` | A person is sitting on a bed, wearing black shorts and socks, with a light-colored shirt visible. |
| 43 | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590971959.jpg` | A person wearing a black blazer and white shirt is sitting on a bed. |
| 172 | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590402679.jpg` | A person wearing a black and red striped tie and a white shirt, sitting near a window. |
| 178 | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590588956.jpg` | A young woman sitting indoors, wearing a black blazer and red and white striped shirt, looking at the camera. |
| 181 | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590607764.jpg` | A person is sitting on the floor, wearing black and red pants, leaning against a window. |

## Main Caption Model Comparison Plan

Because candidate count is at least 10, the next step can be a controlled 10-image model comparison after user confirmation.

Planned selection rules:

- Select 10 rows only from the corrected candidate set.
- Use `image_role=quick_screen` only.
- Use `source_person_id=XiaoEn` only.
- Prefer coverage across half-body, full-body, indoor, outdoor, clear clothing, and clear face images.
- Use the same 10 image paths for all compared models.

Planned models:

- `gemma4:e2b`
- `qwen3-vl:8b`
- `gemma4:e4b-it-q4_K_M`

Planned output:

- `metadata\p05_main_caption_model_compare_sample.jsonl`

Planned report:

- `docs\02_caption_strategy\p05_main_caption_model_compare_report.md`

Planned comparison dimensions:

- Success rate
- Average response time
- JSON format stability
- Clothing description accuracy
- Pose description accuracy
- Scene description accuracy
- Garbled text / mojibake
- Unrelated image descriptions
- Suitability as `main_caption`
- Recommended final main caption model

## Boundaries

- Did not call any model.
- Did not run full caption.
- Did not train LoRA.
- Did not run ComfyUI generation.
- Did not modify `metadata\p05_caption_queue.csv`.
- Did not upload JSONL, CSV, or images.
