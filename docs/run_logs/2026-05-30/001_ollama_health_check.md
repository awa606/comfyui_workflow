# Command Log: Ollama Health Check Before Quick Screen Retry

## Basic Info

- Date: 2026-05-30
- Project directory: `D:\sd.webui\comic_project`
- Operator: Codex
- Phase: P0.5 local VLM quick screen retry gate
- Related files:
  - `docs\02_caption_strategy\p05_quick_screen_sample_report.md`
  - `metadata\p05_caption_queue.csv`
  - `metadata\p05_caption_results_quick_sample.jsonl`

## Command

```powershell
Invoke-RestMethod http://127.0.0.1:11434/api/version

Invoke-RestMethod http://127.0.0.1:11434/api/tags

$body = @{
  model = "gemma4:e2b"
  messages = @(@{ role = "user"; content = "ping" })
  stream = $false
} | ConvertTo-Json -Depth 5

Invoke-RestMethod `
  -Uri http://127.0.0.1:11434/api/chat `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

## Purpose

- Confirm the local Ollama service is reachable before retrying `gemma4:e2b` quick screening.
- Confirm the previous connection-refused failure has been resolved.
- Gate the retry so no model caption run starts if Ollama is still unavailable.

## Preconditions

- Previous 60-row `gemma4:e2b` quick sample failed with `urlopen error [WinError 10061] connection refused by target machine`.
- User reports that the Ollama service has been restored.
- Do not enter `qwen3-vl:8b`.
- Do not train LoRA.
- Do not run ComfyUI image generation.
- Do not run full captioning.
- Do not modify `metadata\p05_caption_queue.csv`.

## Output Summary

- `Invoke-RestMethod http://127.0.0.1:11434/api/version` succeeded.
- `Invoke-RestMethod http://127.0.0.1:11434/api/tags` succeeded.
- `gemma4:e2b` `/api/chat` ping succeeded and returned `done=True`.
- The previous connection-refused condition is no longer present.

## Generated / Modified Files

- `docs\run_logs\2026-05-30\001_ollama_health_check.md`

## Key Metrics

- `/api/version` reachable: yes
- Ollama version: `0.24.0`
- `/api/tags` reachable: yes
- `gemma4:e2b` chat ping successful: yes
- `gemma4:e2b` ping `done_reason`: `stop`
- `gemma4:e2b` ping total duration: `17245503700`
- Allowed to continue quick_screen retry: yes

## Problems Found

- No connection failure during the health check.
- The model response to `ping` was verbose, but the API call completed successfully; this is acceptable for a health gate.

## Solution / Handling

- Treat Ollama as available for the limited `gemma4:e2b` quick sample retry.
- Continue with only the requested 60-row sample:
  - first 30 `quick_screen`
  - first 30 `face_crop_review`
  - maximum total 60

## Next Step

- Run only the 60-row `gemma4:e2b` quick sample retry.
- Do not enter `qwen3-vl:8b` without user confirmation.

## Git Safety Check

- This log is safe to commit.
- Do not commit `metadata`, `outputs`, JSONL, CSV, images, videos, NPZ, or model files.
