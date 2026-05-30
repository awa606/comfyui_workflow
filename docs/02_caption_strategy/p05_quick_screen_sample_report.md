# P0.5 Quick Screen Sample Report

Generated: 2026-05-30
Updated after successful retry: 2026-05-30

## Scope

- Queue file: `metadata\p05_caption_queue.csv`
- Output JSONL: `metadata\p05_caption_results_quick_sample.jsonl`
- Output CSV: `metadata\p05_caption_results_quick_sample.csv`
- Model requested: `gemma4:e2b`
- Roles processed:
  - `quick_screen`: max 30
  - `face_crop_review`: max 30
- Total sample limit: 60

The original queue CSV was not modified.

## Selection Summary

| image_role | selected |
| --- | ---: |
| quick_screen | 30 |
| face_crop_review | 30 |
| total | 60 |

Only rows with `caption_status=queued`, `recommended_model=gemma4:e2b`, and no excluded path keyword were selected.

## Exclusion Check

The selected sample did not include paths containing:

- `explicit`
- `R18`
- `r18`
- `03_explicit`
- `03_explicit_action`
- `styles\explicit`
- `VIP`

## Result Summary

| metric | count |
| --- | ---: |
| success | 60 |
| failed | 0 |
| usable_for_next_step=yes | 60 |
| usable_for_next_step=no | 0 |
| safe_for_p05=true | 60 |
| needs_manual_review=false | 60 |

## Error Summary

No errors were found in the successful retry.

| inference_status | count |
| --- | ---: |
| ok | 60 |

## Output Schema

Each JSONL row from `scripts\run_caption_queue_p05.py` uses these wrapper fields:

- `queue_row_index`
- `image_path`
- `source_person_id`
- `image_role`
- `recommended_model`
- `caption_status`
- `inference_status`
- `response_seconds`
- `caption_json`
- `raw_response`
- `error`

The parsed `caption_json` contains:

- `safe_for_p05`
- `needs_manual_review`
- `image_role`
- `source_person_id`
- `caption`
- `identity_notes`
- `style_notes`
- `positive_tags`
- `negative_tags`
- `queue_notes`

## Issues Found

- The previous Ollama connection failure was resolved before this retry.
- The retry produced valid JSON for all 60 selected rows.
- No `qwen3-vl:8b` run was performed.
- No full caption queue was run.
- `metadata\p05_caption_queue.csv` was not modified.

## Runtime Notes

| metric | value |
| --- | ---: |
| minimum response seconds | 4.28 |
| maximum response seconds | 6.00 |
| average response seconds | 4.95 |

## Recommendation

Do not proceed to `qwen3-vl:8b main_caption` automatically.

Recommended next step is manual review of the 60 successful `gemma4:e2b` quick sample outputs. Enter `qwen3-vl:8b main_caption` only after user confirmation.

## Boundaries

- Did not run a full queue.
- Did not modify `metadata\p05_caption_queue.csv`.
- Did not upload JSONL.
- Did not upload images.
- Did not process excluded explicit/R18/VIP paths.
- Did not enter `qwen3-vl:8b`.
- Did not train LoRA.
- Did not run ComfyUI image generation.
