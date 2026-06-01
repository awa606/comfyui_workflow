# P0.5 Quick Screen Manual Review Summary

Generated: 2026-05-30

## Scope

- Source file: `metadata/p05_caption_results_quick_sample.jsonl`
- Model: `gemma4:e2b`
- Queue file was not modified.
- No `qwen3-vl:8b` run was performed.
- No CSV, JSONL, image, video, NPZ, or model file is included in this report.

## Sample Counts

| metric | count |
| --- | ---: |
| total samples | 60 |
| `quick_screen` | 30 |
| `face_crop_review` | 30 |

## Safety / Review Fields

| safe_for_p05 | count |
| --- | ---: |
| true | 60 |
| false | 0 |

| needs_manual_review | count |
| --- | ---: |
| true | 0 |
| false | 60 |

`usable_for_next_step` is not a stored JSON field in the current output schema. This report derives it as:

```text
inference_status == ok AND error is empty AND safe_for_p05 == true
```

| usable_for_next_step | count |
| --- | ---: |
| yes | 60 |
| no | 0 |

## source_person_id Distribution

| source_person_id | count |
| --- | ---: |
| XiaoEn | 60 |

## positive_tags Top 30

| tag | count |
| --- | ---: |
| portrait | 32 |
| face | 19 |
| close-up | 19 |
| clothing | 19 |
| person | 17 |
| fashion | 12 |
| woman | 11 |
| window | 11 |
| blazer | 9 |
| sitting | 8 |
| indoor | 7 |
| tie | 7 |
| hair | 6 |
| bedroom | 5 |
| legs | 5 |
| outdoor | 3 |
| bag | 2 |
| clear focus | 2 |
| shirt | 2 |
| shorts | 2 |
| soft focus | 2 |
| striped shirt | 2 |
| clothing detail | 1 |
| doorframe | 1 |
| hair detail | 1 |
| long hair | 1 |
| outdoors | 1 |
| side profile | 1 |
| side view | 1 |
| soft lighting | 1 |

## negative_tags Top 30

| tag | count |
| --- | ---: |
| blurry | 31 |
| occlusion | 28 |
| low quality | 27 |
| poor_focus | 17 |
| poor_lighting | 4 |
| poor quality | 3 |
| low_detail | 2 |
| poor lighting | 2 |
| poor_framing | 2 |
| blur | 1 |
| distracting background | 1 |
| low detail | 1 |
| low-detail | 1 |

## Obvious Anomaly Check

The current schema does not include a separate `visual_summary` field, so this check uses `caption`, `identity_notes`, `style_notes`, and `queue_notes`.

| anomaly type | count | note |
| --- | ---: | --- |
| empty description | 0 | No empty `caption` values found. |
| mojibake / garbled text | 0 | No obvious replacement characters or mojibake patterns found. |
| unrelated to image / system text | 0 | No network, prompt, ping, or "cannot view image" style responses found. |
| style image misread as identity image | 0 | No `source_person_id=styles` rows in this sample. |
| face crop described as full-body / body shot | 1 | One `face_crop_review` row uses "standing in front of" while still describing a close-up portrait. |

Potential issue example:

| queue_row_index | image_role | note |
| --- | --- | --- |
| 65 | `face_crop_review` | Caption says close-up portrait but also says "standing in front of a plain orange wall"; this is probably a minor spatial wording issue, not a full-body misclassification. |

## Random quick_screen Text Samples

| queue_row_index | source_person_id | caption | queue_notes |
| ---: | --- | --- | --- |
| 1 | XiaoEn | A person wearing black shorts and a white shirt is standing outdoors on a grassy area. | Simple full-body shot of a person in an outdoor setting. |
| 7 | XiaoEn | A person is sitting in front of a window, wearing a black blazer and red and white striped tie, with a black bag beside them. | Simple portrait of a person sitting by a window. |
| 10 | XiaoEn | A person is sitting next to a window, wearing a black blazer and tie, with a black bag nearby. | A straightforward portrait of a person sitting indoors near a window. |
| 19 | XiaoEn | A person wearing a black and red striped tie and a white shirt, sitting near a window. | A straightforward portrait focusing on the subject's attire. |
| 28 | XiaoEn | A person is sitting on the floor, wearing black and red pants, leaning against a window. | Image shows a person sitting with their legs extended, leaning near a window. |
| 37 | XiaoEn | A person is sitting on a bed with a gold frame, wearing a black and white striped shirt. | A straightforward portrait of a person in a bedroom setting. |
| 40 | XiaoEn | A person is sitting on a bed, wearing black shorts and socks, with a light-colored shirt visible. | Image primarily features the lower body and legs of a person in a bedroom setting. |
| 166 | XiaoEn | A young woman is sitting in front of a window, wearing a dark blazer and tie. | A straightforward portrait focusing on the subject's attire and pose. |
| 172 | XiaoEn | A person wearing a black and red striped tie and a white shirt, sitting near a window. | Simple portrait of a person wearing a tie and shirt. |
| 175 | XiaoEn | A young woman sitting in front of a window, wearing a black and white striped shirt and a red tie. | A straightforward portrait of a person sitting indoors. |

## Random face_crop_review Text Samples

| queue_row_index | source_person_id | caption | queue_notes |
| ---: | --- | --- | --- |
| 51 | XiaoEn | close-up portrait of a young woman with dark hair, looking directly at the camera, wearing a white collared shirt. | Good quality face crop for identity reference. No significant occlusions. |
| 63 | XiaoEn | close-up portrait of a young woman with long, dark hair, looking towards the camera. | Good quality face crop, clear identity reference. |
| 64 | XiaoEn | A close-up portrait of a person with dark hair tied in a ponytail, wearing a white collared shirt and a red and blue patterned tie, against a plain background. | The face is clearly visible and sharp. The crop effectively captures the subject and the details of the attire. |
| 65 | XiaoEn | A close-up portrait of a young woman with dark hair, wearing a white collared shirt and a red and blue patterned tie, standing in front of a plain orange wall. | The face crop is clear and suitable for identity reference. No significant occlusions are present. |
| 68 | XiaoEn | A close-up portrait of a person wearing a white shirt and a red and blue patterned tie, with a blurred background. | Good quality face crop, clear identity reference. |
| 69 | XiaoEn | A close-up shot focusing on the side profile of a person with dark hair wearing a white collared shirt and a red tie. | Good for capturing the side profile and clothing details. No major issues detected. |
| 71 | XiaoEn | A close-up portrait of a young woman with long, dark hair, wearing a white collared shirt with a red and blue patterned tie. | Good quality face crop, clear identity reference. |
| 74 | XiaoEn | A close-up portrait of a young woman with long, dark hair, looking directly at the camera. | The face is well-framed and clear. No significant occlusions are present. |
| 76 | XiaoEn | A close-up shot of a person with long, dark hair, looking down. | The crop focuses heavily on the hair and the side of the face. Identity reference seems fine for style/hair generation. |
| 77 | XiaoEn | A close-up shot of a person with long, dark hair, looking slightly to the side with a thoughtful expression, with one hand near their hair. | Good visibility of the face and hair. No significant occlusions. |

## Conclusion

Status: `REVIEW`

The 60-row `gemma4:e2b` quick sample is technically successful: all rows returned valid JSON, all rows are marked `safe_for_p05=true`, and none are marked `needs_manual_review=true`. However, the model is permissive and assigns many negative quality tags such as `blurry`, `occlusion`, and `low quality` while still marking every row usable. One face crop also has minor spatial wording that should be checked by a human.

Recommended next step: manually inspect part of the 60-row sample, especially rows with frequent quality negatives and the face crop wording issue, before deciding whether to enter `qwen3-vl:8b main_caption` small-batch testing.

Do not enter `qwen3-vl:8b` without user confirmation.

