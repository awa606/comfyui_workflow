# Command Log: Quick Screen Retry With gemma4:e2b

## Basic Info

- Date: 2026-05-30
- Project directory: `D:\sd.webui\comic_project`
- Operator: Codex
- Phase: P0.5 local VLM quick screen retry
- Related files:
  - `metadata\p05_caption_queue.csv`
  - `metadata\p05_caption_results_quick_sample.csv`
  - `metadata\p05_caption_results_quick_sample.jsonl`
  - `docs\02_caption_strategy\p05_quick_screen_sample_report.md`

## Command

```powershell
python scripts\run_caption_queue_p05.py --queue metadata\p05_caption_queue.csv --output-csv metadata\p05_caption_results_quick_sample.csv --output-jsonl metadata\p05_caption_results_quick_sample.jsonl --role-limits quick_screen=30 face_crop_review=30 --timeout-seconds 180 --ollama-url http://127.0.0.1:11434
```

## Purpose

- Retry the failed `gemma4:e2b` quick sample after Ollama health checks passed.
- Process only a bounded sample before any larger captioning decision.
- Keep `qwen3-vl:8b` out of scope until user confirmation.

## Preconditions

- `Invoke-RestMethod http://127.0.0.1:11434/api/version` succeeded.
- `Invoke-RestMethod http://127.0.0.1:11434/api/tags` succeeded.
- `gemma4:e2b` `/api/chat` ping succeeded.
- `metadata\p05_caption_queue.csv` exists and must not be modified.
- No LoRA training.
- No ComfyUI image generation.
- No full caption queue run.

## Output Summary

- Queue read: `metadata\p05_caption_queue.csv`
- Selected rows: 60
- Wrote local CSV result: `metadata\p05_caption_results_quick_sample.csv`
- Wrote local JSONL result: `metadata\p05_caption_results_quick_sample.jsonl`
- Status counts: `{"ok": 60}`

## Generated / Modified Files

- Generated local output, not for Git:
  - `metadata\p05_caption_results_quick_sample.csv`
  - `metadata\p05_caption_results_quick_sample.jsonl`
- Modified documentation:
  - `docs\02_caption_strategy\p05_quick_screen_sample_report.md`
- Created run log:
  - `docs\run_logs\2026-05-30\002_quick_screen_retry.md`
- Not modified:
  - `metadata\p05_caption_queue.csv`

## Key Metrics

- Selection rule: first 30 `quick_screen` rows and first 30 `face_crop_review` rows from queued `gemma4:e2b` rows.
- Total selected: 60
- `quick_screen`: 30
- `face_crop_review`: 30
- Successful rows: 60
- Failed rows: 0
- `usable_for_next_step=yes`: 60
- `usable_for_next_step=no`: 0
- `safe_for_p05=true`: 60
- `needs_manual_review=false`: 60
- Error type statistics: none
- Minimum response seconds: 4.28
- Maximum response seconds: 6.00
- Average response seconds: 4.95

## Problems Found

- No runtime errors in this retry.
- The generated CSV and JSONL are local outputs and must not be committed.

## Solution / Handling

- Treated `inference_status=ok` rows with valid parsed `caption_json` as usable for the next review step.
- Updated the quick screen sample report with successful retry metrics.
- Kept the original caption queue unchanged.

## Next Step

- Manually review the 60 successful `gemma4:e2b` sample outputs.
- Do not enter `qwen3-vl:8b main_caption` without user confirmation.

## Git Safety Check

- Safe to commit:
  - `docs\run_logs\`
  - `docs\02_caption_strategy\p05_quick_screen_sample_report.md`
- Do not commit:
  - `metadata\p05_caption_results_quick_sample.csv`
  - `metadata\p05_caption_results_quick_sample.jsonl`
  - `metadata\p05_caption_queue.csv`
  - `outputs\`
  - `training_data_raw\`
  - images, videos, NPZ files, or model files

