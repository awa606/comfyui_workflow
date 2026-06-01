# P0.5 Main Caption Gemma4 E4B Batch 001 Manual Review Result

Generated: 2026-06-01

## Scope

Inputs reviewed:

- `metadata\p05_manual_review_batch_001_results.csv`
- `docs\02_caption_strategy\p05_main_caption_gemma4_e4b_batch_001_manual_checklist.md`
- `docs\02_caption_strategy\p05_main_caption_gemma4_e4b_batch_001_report.md`

Execution boundary:

- No new model run.
- Did not enter `qwen3-vl`.
- Did not train LoRA.
- Did not run ComfyUI image generation.
- Did not modify `metadata\p05_caption_queue.csv`.
- Did not upload images, CSV, or JSONL.

## 1. Review Sample Count

| Metric | Count |
| --- | ---: |
| Manual review rows | 12 |

Note: `metadata\p05_manual_review_batch_001_results.csv` is still a template with blank yes/no fields. The detailed counts below therefore use the user's stated manual review conclusion rather than per-row CSV values.

## 2. face_correct Statistics

| Result | Count |
| --- | ---: |
| yes | qualitative: most / basically passed |
| no | not precisely recorded |

Manual conclusion: face description is basically acceptable.

## 3. clothing_correct Statistics

| Result | Count |
| --- | ---: |
| yes | partial |
| no | partial |

Manual conclusion: clothing has some errors, especially skirt, lower-body clothing, inner-layer clothing, and edge / boundary details.

## 4. pose_correct Statistics

| Result | Count |
| --- | ---: |
| yes | few or none |
| no | most / possibly all |

Manual conclusion: pose is mostly or entirely problematic.

## 5. scene_correct Statistics

| Result | Count |
| --- | ---: |
| yes | qualitative: most / basically passed |
| no | not precisely recorded |

Manual conclusion: scene description is basically acceptable.

## 6. usable_for_asset_index Statistics

| Result | Count |
| --- | ---: |
| yes | not enough for batch_002 approval |
| no / blocked | current batch remains blocked |

Manual conclusion: current results are not sufficient to enter 100-image `batch_002`.

## 7. Pose Error Type Summary

Observed manual issue pattern:

- Complex seated poses are unreliable.
- Leg position, knees, feet direction, and crossed / raised leg details are not dependable.
- Strong perspective and foreground legs increase pose errors.
- Sitting on floor / bed / ledge is often recognized at a coarse level, but fine-grained limb geometry is unreliable.
- Pose text should be treated as approximate visual prose, not as geometric truth.

Implication:

- VLM-generated pose cannot be used as precise pose labels.
- Downstream pose should be handled by DWPose / OpenPose or equivalent pose preprocessors.
- Human review is required when pose wording matters for asset indexing.

## 8. Clothing Error Type Summary

Observed manual issue pattern:

- Skirt vs shorts vs lower garment boundaries are error-prone.
- Inner-layer clothing and edge details are unreliable.
- Occluded lower-body clothing may be over-inferred.
- Stockings / socks / tights may be broadly useful, but exact boundaries and garment category need review.
- Sensitive or uncertain lower-clothing descriptions must not be accepted without manual verification.

Implication:

- VLM captions are useful for broad clothing categories.
- VLM captions are not reliable for precise lower-body garment, skirt hem, inner-layer, or occluded boundary decisions.
- Ambiguous clothing should be marked and excluded from training captions until reviewed.
- Clothing boundaries should be handled by segmentation / masks or manual review.

## 9. Image Quality / Occlusion / Perspective Impact

Likely contributors to caption errors:

- Complex seated poses with legs in foreground.
- Strong perspective where legs or lower body dominate the image.
- Occlusion from skirt folds, stockings, bags, hands, and body overlap.
- Edge ambiguity between skirt, shorts, underlayers, and stockings.
- Cropping and camera angle can make lower-body garment labels unstable.

Face and broad scene are less affected in this batch; pose and lower clothing are the weak areas.

## 10. Current Conclusion

Conclusion: `REVIEW-BLOCKED`.

Do not enter 100-image `main_caption batch_002`.

Reasons:

- Face and scene are broadly acceptable.
- Pose accuracy is not reliable.
- Clothing has partial errors, especially lower-body and ambiguous boundary details.
- Existing prompt/schema overstates pose and clothing certainty.
- Manual review shows the current output cannot be safely expanded without schema and prompt changes.

## 11. Required Prompt And Schema Changes

The next main caption prompt/schema should be changed before any 100-image expansion:

- Keep `gemma4:e4b-it-q4_K_M` as the main caption model.
- Treat `pose` as low-confidence descriptive prose by default.
- Add `pose_confidence`.
- Add `pose_needs_manual_review`.
- Add `clothing_confidence`.
- Add `ambiguous_clothing`.
- Do not hard-classify lower-body clothing, skirt hem, inner-layer, or occluded areas.
- For complex seated poses, strong perspective, or foreground-heavy legs, default `pose_confidence` to `low`.
- Do not use VLM pose results as training labels.
- Do not allow ambiguous clothing into training captions without human correction.

## 12. Policy Clarification

- VLM caption can continue to be used for face, scene, and broad clothing descriptions.
- VLM caption must not be treated as a source of precise pose labels.
- VLM caption must not be treated as a source of precise lower-body clothing / inner-layer / clothing-boundary labels.
- DWPose / OpenPose should handle downstream pose extraction.
- Segmentation / mask tools or human review should handle clothing boundaries.
- Caption results must still be manually reviewed before they influence FaceID/IPAdapter selection or any training decision.

## 13. Next Step

Prepare a revised `main_caption` prompt/schema and run only a small validation sample after user confirmation.

Do not run 100-image `batch_002` until the revised schema passes manual review.
