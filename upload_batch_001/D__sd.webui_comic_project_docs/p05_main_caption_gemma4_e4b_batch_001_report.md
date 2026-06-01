# P0.5 Main Caption Gemma4 E4B Batch 001 Report

Generated: 2026-05-31

## Scope

Input:

- `metadata\p05_caption_results_main_gemma4_e4b_batch_001.jsonl`
- `docs\02_caption_strategy\local_vlm_caption_strategy.md`

Model:

- `gemma4:e4b-it-q4_K_M`

Boundaries:

- Did not run any new model.
- Did not enter `qwen3-vl`.
- Did not train LoRA.
- Did not run ComfyUI image generation.
- Did not modify `metadata\p05_caption_queue.csv`.
- Did not upload JSONL, CSV, or images.

## 1. Basic Results

| Metric | Value |
| --- | ---: |
| Total samples | 30 |
| Success count | 30 |
| Failure count | 0 |
| JSON valid count | 30 |
| JSON valid rate | 100% |

## 2. Timing

| Metric | Seconds |
| --- | ---: |
| Average response time | 13.84 |
| Shortest response time | 12.42 |
| Longest response time | 23.91 |

## 3. source_person_id Distribution

| source_person_id | Count |
| --- | ---: |
| XiaoEn | 30 |

## 4. image_role Distribution

The output uses `source_image_role` to preserve the source queue role.

| source_image_role | Count |
| --- | ---: |
| quick_screen | 30 |

## 5. caption_quality Distribution

| caption_quality | Count |
| --- | ---: |
| good | 30 |

## 6. needs_manual_review Distribution

| needs_manual_review | Count |
| --- | ---: |
| false | 30 |

## 7. positive_tags Top 30

| Tag | Count |
| --- | ---: |
| seated | 15 |
| young woman | 12 |
| black blazer | 9 |
| black stockings | 9 |
| school uniform | 8 |
| blazer | 7 |
| full body | 7 |
| striped tie | 7 |
| black tights | 6 |
| indoor setting | 5 |
| sitting | 5 |
| sitting on floor | 5 |
| thigh-high stockings | 5 |
| window background | 5 |
| school uniform style | 4 |
| window view | 4 |
| bedroom setting | 3 |
| dark blazer | 3 |
| outdoor setting | 3 |
| striped shirt | 3 |
| black thigh-high stockings | 2 |
| loafers | 2 |
| sitting indoors | 2 |
| thigh-high socks | 2 |
| window light | 2 |
| black leggings | 1 |
| black skirt | 1 |
| black socks | 1 |
| business attire | 1 |
| dark hair | 1 |

## 8. negative_tags Top 30

| Tag | Count |
| --- | ---: |
| blurry | 23 |
| distorted | 21 |
| extra limbs | 15 |
| deformed | 5 |
| out of focus | 5 |
| outdoor | 5 |
| bad anatomy | 4 |
| casual wear | 3 |
| distorted limbs | 3 |
| low quality | 3 |
| real person | 2 |
| cartoon | 1 |
| cartoonish | 1 |
| cluttered | 1 |
| cropped | 1 |
| multiple people | 1 |
| outdoor setting | 1 |
| overexposed | 1 |

## 9. Random 10 Caption Summaries

These summaries are built from the structured fields because this batch schema does not include a single freeform `caption` field.

| queue_row_index | Summary |
| ---: | --- |
| 1 | Full body, standing on a curb; face clear; white collared shirt, striped tie, black pleated skirt, black stockings, loafers, black shoulder bag; outdoor paved area with grass. |
| 4 | Full body, seated on a ledge; face clear; white collared shirt, black skirt, thigh-high stockings, loafers, striped tie; outdoor pathway and grass. |
| 13 | Full body, seated on a wooden surface; face clear; dark blazer, white shirt, striped tie, black stockings, loafers; indoor window scene. |
| 16 | Full body, seated on floor; face clear; black blazer, white shirt, striped tie, black stockings, skirt, heels; indoor window, curtains, bag. |
| 19 | Full body / lower legs visible; face clear; shirt, blazer, pleated skirt, striped tie, thigh-high stockings; seated near window. |
| 154 | Full body, seated on low wall; face clear; white shirt, black pleated skirt, thigh-high stockings, loafers, striped tie; outdoor wall and grass. |
| 157 | Full body, seated on ledge; face clear; white shirt, black skirt, thigh-high stockings, loafers, tie, shoulder bag; outdoor pathway and grass. |
| 163 | Full body, seated on floor; face clear; black blazer, white shirt, striped tie, skirt, stockings, loafers; indoor window and bag. |
| 184 | Full body, legs and torso visible; face clear; black blazer, black bottoms/leggings, dark shoes; seated against window with legs raised/crossed. |
| 190 | Full body, seated on bed; face clear; blazer over collared shirt, striped shirt/tie detail, thigh-high stockings; bedroom with bed and headboard. |

## 10. Obvious Anomaly Check

This pass did not open or inspect images directly. The checks below are based on JSON structure, generated text, and consistency against the earlier `quick_caption` text baseline.

| Check | Result | Notes |
| --- | --- | --- |
| Empty caption | No freeform `caption` field in this schema; no empty required caption fields found | Core fields such as clothing, pose, scene, lighting, face visibility, and character visibility were present in all 30 rows. |
| JSON missing fields | 0 | Required structured fields complete in 30/30 rows. |
| Garbled text | 0 obvious cases in structured caption fields | Source paths contain mojibake, but generated caption fields were usable. |
| Unrelated description | 0 obvious text-baseline conflicts | No generated row was obviously unrelated to its `quick_caption`. |
| Face / body / clothing / pose mismatch | 0 obvious text-baseline conflicts | No rule-based mismatch against quick caption was found. |

Manual review note:

- One row includes a sensitive clothing observation in the clothing field. It should be checked manually against the source image before expanding use.
- Negative tags include broad quality-control terms such as `blurry`, `distorted`, and `extra limbs`; these are normal negative-prompt style tags, not necessarily detected image defects.

## 11. Conclusion

Conclusion: `REVIEW`.

Reasoning:

- Technical quality is strong: 30/30 success, 100% valid JSON, complete required fields, stable timing.
- However, caption outputs have not been visually verified against the source images in this pass.
- Strategy policy requires human review before caption results influence FaceID/IPAdapter or training decisions.
- A small manual spot check is appropriate before expanding to 100 images.

Recommendation:

- Do not enter full caption.
- Do not enter training.
- Perform manual review on a subset of batch_001 first, especially clothing, face visibility, and pose accuracy.
- If manual review passes, it is reasonable to proceed to a controlled 100-image `main_caption` batch_002 with `gemma4:e4b-it-q4_K_M`.
