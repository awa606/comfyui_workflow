# P0.5 Main Caption Model Compare Report

Generated: 2026-05-31

## Scope

Input source:

- `metadata\p05_caption_results_quick_sample.jsonl`

Output:

- `metadata\p05_main_caption_model_compare_sample.jsonl`

Corrected candidate filter:

- Outer `inference_status == "ok"`
- Outer `error` is empty
- Parsed `caption_json.safe_for_p05 == true`
- Parsed `caption_json.needs_manual_review == false`
- `image_role == "quick_screen"`
- `source_person_id == "XiaoEn"`

Selected sample:

- 10 `quick_screen` source images
- 30 total model calls
- No `face_crop_review` rows

Selected `queue_row_index` values:

- `1`
- `4`
- `7`
- `16`
- `25`
- `28`
- `37`
- `40`
- `46`
- `49`

Models compared:

- `gemma4:e2b`
- `qwen3-vl:8b`
- `gemma4:e4b-it-q4_K_M`

## Quantitative Results

| Model | Calls | OK | Invalid JSON | Error | Success rate | JSON valid rate | Average response time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `gemma4:e2b` | 10 | 10 | 0 | 0 | 100% | 100% | 15.85s |
| `qwen3-vl:8b` | 10 | 7 | 3 | 0 | 70% | 70% | 79.43s |
| `gemma4:e4b-it-q4_K_M` | 10 | 10 | 0 | 0 | 100% | 100% | 22.21s |

`qwen3-vl:8b` invalid JSON cases:

| queue_row_index | status | note |
| ---: | --- | --- |
| 1 | `invalid_json` | Empty raw response |
| 40 | `invalid_json` | Empty raw response |
| 46 | `invalid_json` | Empty raw response |

## JSON Format Stability

| Model | Assessment |
| --- | --- |
| `gemma4:e2b` | Stable. All 10 responses were valid JSON and contained the requested main fields. |
| `qwen3-vl:8b` | Unstable. 3 of 10 responses were empty / invalid JSON despite `format=json`. |
| `gemma4:e4b-it-q4_K_M` | Stable. All 10 responses were valid JSON and contained the requested main fields. |

## Content Quality Review

### `gemma4:e2b`

- Person description accuracy: adequate, but often generic.
- Clothing accuracy: generally correct for obvious clothing, but less detailed than the other successful model.
- Pose / scene accuracy: usually correct but terse; useful for screening, less ideal for full `main_caption`.
- Garbled text: none found in parsed model output.
- Unrelated descriptions: none obvious in successful outputs.
- Main caption suitability: usable as a fallback, but too sparse for the primary main caption pass.

### `qwen3-vl:8b`

- Person description accuracy: strong when JSON is valid.
- Clothing accuracy: strongest detail in valid responses, including accessories and garment types.
- Pose / scene accuracy: strongest in valid responses, with more complete body pose and environment notes.
- Garbled text: none found in valid parsed output.
- Unrelated descriptions: none obvious in valid outputs.
- Main caption suitability: semantically promising, but not reliable enough yet because JSON stability was only 70% and response time was much slower.

### `gemma4:e4b-it-q4_K_M`

- Person description accuracy: good and consistent.
- Clothing accuracy: detailed enough for main caption use, generally richer than `gemma4:e2b`.
- Pose / scene accuracy: good balance of pose, environment, framing, and lighting details.
- Garbled text: none found in parsed model output.
- Unrelated descriptions: none obvious in successful outputs.
- Main caption suitability: best current choice because it combines stable JSON, complete fields, usable detail, and moderate response time.

## Qualitative Comparison

| Dimension | Best observed model | Notes |
| --- | --- | --- |
| Success rate | `gemma4:e2b`, `gemma4:e4b-it-q4_K_M` | Both reached 100%. |
| Average response time | `gemma4:e2b` | Fastest at 15.85s average. |
| JSON stability | `gemma4:e2b`, `gemma4:e4b-it-q4_K_M` | Both reached 100%; `qwen3-vl:8b` failed 3 JSON responses. |
| Person description accuracy | `qwen3-vl:8b` when valid; otherwise `gemma4:e4b-it-q4_K_M` | `qwen3-vl:8b` is detailed but unstable. |
| Clothing description accuracy | `qwen3-vl:8b` when valid; otherwise `gemma4:e4b-it-q4_K_M` | `gemma4:e2b` tends to be shorter. |
| Pose / scene accuracy | `qwen3-vl:8b` when valid; otherwise `gemma4:e4b-it-q4_K_M` | `qwen3-vl:8b` provides richer scene details but has reliability problems. |
| Garbled text | none detected | Source paths contain mojibake in folder names, but parsed model outputs did not show mojibake. |
| Unrelated descriptions | none obvious | No successful parsed output appeared unrelated to its quick caption baseline. |

## Recommendation

Recommended final `main_caption` model for the next controlled small batch:

- `gemma4:e4b-it-q4_K_M`

Rationale:

- 100% success rate on this sample.
- 100% valid JSON rate.
- More complete and useful captions than `gemma4:e2b`.
- Much more reliable than `qwen3-vl:8b` in structured JSON mode.
- Average response time is acceptable for a controlled main caption pass.

`qwen3-vl:8b` should not be the primary `main_caption` model until its empty / invalid JSON behavior is fixed or wrapped with a retry / repair step. Its valid outputs are detailed, so it may still be useful later as an optional second-pass comparison model.

`gemma4:e2b` should remain the quick screening model rather than the primary main caption model.

## Boundaries

- Did not run full caption.
- Did not train LoRA.
- Did not run ComfyUI generation.
- Did not modify `metadata\p05_caption_queue.csv`.
- Did not upload JSONL, CSV, or images.
- Stopped after the 10-image / 30-call model comparison sample.
