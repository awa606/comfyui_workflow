# P0.5 Main Caption Schema V2 Validation 12 Report

Generated: 2026-06-01

## Scope

- Schema: `docs\02_caption_strategy\p05_main_caption_schema_v2.md`
- Input: `metadata\p05_caption_results_main_gemma4_e4b_batch_001.jsonl`
- Manual sample list: `docs\02_caption_strategy\p05_main_caption_gemma4_e4b_batch_001_manual_checklist.md`
- Output JSONL: `metadata\p05_caption_results_main_gemma4_e4b_schema_v2_validation_12.jsonl`
- Model: `gemma4:e4b-it-q4_K_M`
- Queue rows: `1, 4, 7, 13, 19, 25, 34, 37, 49, 154, 181, 184`

Boundaries: did not run 30/100 images, did not enter `qwen3-vl`, did not train LoRA, did not run ComfyUI, and did not modify `metadata\p05_caption_queue.csv`.

## Summary

| Metric | Value |
| --- | ---: |
| Total samples | 12 |
| Success count | 12 |
| JSON valid rate | 100% |
| Missing required field count | 0 |
| `pose_needs_manual_review=true` count | 12 |
| `ambiguous_clothing` non-empty count | 12 |
| Hard lower-body detail flags | 0 |
| Over-certain complex pose flags | 5 |

## pose_confidence Distribution

| pose_confidence | Count |
| --- | ---: |
| low | 7 |
| medium | 5 |
| high | 0 |

## clothing_confidence Distribution

| clothing_confidence | Count |
| --- | ---: |
| low | 0 |
| medium | 8 |
| high | 4 |

## Required Field Check

All 12 output rows contain the required schema_v2 fields.

## Lower-Body Hard Classification Check

No obvious hard lower-body detail classification was detected by text heuristics.

## Complex Pose Over-Certainty Check

| queue_row_index | Flag |
| ---: | --- |
| 7 | pose may still be too certain for complex sample |
| 34 | pose may still be too certain for complex sample |
| 37 | pose may still be too certain for complex sample |
| 49 | pose may still be too certain for complex sample |
| 154 | pose may still be too certain for complex sample |

## Per-Row Status

| queue_row_index | status | pose_confidence | pose_review | clothing_confidence | ambiguous_clothing | hard_lower_body | overcertain_pose |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | ok | medium | true | high | true | false | false |
| 4 | ok | low | true | medium | true | false | false |
| 7 | ok | medium | true | high | true | false | true |
| 13 | ok | low | true | high | true | false | false |
| 19 | ok | low | true | medium | true | false | false |
| 25 | ok | low | true | medium | true | false | false |
| 34 | ok | medium | true | high | true | false | true |
| 37 | ok | low | true | medium | true | false | true |
| 49 | ok | medium | true | medium | true | false | true |
| 154 | ok | medium | true | medium | true | false | true |
| 181 | ok | low | true | medium | true | false | false |
| 184 | ok | low | true | medium | true | false | false |

## Conclusion

Conclusion: `FAIL`

Schema v2 still has structural or reliability issues. Continue prompt/schema revision before additional validation.

Stop here. Do not continue to 30-image or 100-image validation without user confirmation.
