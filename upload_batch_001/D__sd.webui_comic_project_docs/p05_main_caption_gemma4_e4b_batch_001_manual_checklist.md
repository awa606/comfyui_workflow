# P0.5 Main Caption Gemma4 E4B Batch 001 Manual Checklist

Generated: 2026-06-01

## Scope

Input files:

- `metadata\p05_caption_results_main_gemma4_e4b_batch_001.jsonl`
- `docs\02_caption_strategy\p05_main_caption_gemma4_e4b_batch_001_report.md`

Boundaries:

- Did not run any new model.
- Did not enter `qwen3-vl`.
- Did not train LoRA.
- Did not run ComfyUI image generation.
- Did not upload JSONL, CSV, or images.
- Did not copy or open images.

## Selection Rationale

Selected 12 rows from the 30-row batch to cover:

- clear face
- half-body
- full-body
- indoor
- outdoor
- complex clothing
- obvious pose
- rows with more negative tags
- row(s) containing sensitive clothing observations that require manual verification

Selected `queue_row_index` values:

- `1`, `4`, `7`, `13`, `19`, `25`, `34`, `37`, `49`, `154`, `181`, `184`

## Review Instructions

For each row, manually compare the structured caption fields against the actual image at `image_path`.

Use this decision schema:

- `face_correct`: yes/no
- `clothing_correct`: yes/no
- `pose_correct`: yes/no
- `scene_correct`: yes/no
- `usable_for_asset_index`: yes/no
- `notes`: short correction or concern

Do not promote any caption result into FaceID/IPAdapter, asset index decisions, or training decisions until this manual review is complete.

## Manual Check Items

| queue_row_index | Coverage | image_path | character_visibility | face_visibility | clothing 摘要 | pose 摘要 | scene 摘要 | lighting 摘要 | positive_tags | negative_tags | 需要人工确认的问题 |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | clear face, full-body, outdoor, standing, clothing visible | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046589594674.jpg` | full body, standing on a curb | clear, looking towards the camera | white collared shirt, striped tie, black pleated skirt, black tights/stockings, loafers, shoulder bag | standing upright, facing forward | paved outdoor area, curb, green grass | bright natural daylight | full body; school uniform; black tights; outdoor setting | blurry; distorted; bad anatomy | Confirm full-body standing pose, skirt/tights/loafers, and outdoor curb/grass scene. |
| 4 | clear face, full-body, outdoor, seated | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046589900698.jpg` | full body, seated on a ledge | clear, looking towards the camera | white collared shirt, black pleated skirt, thigh-high stockings, loafers, striped tie | seated on low ledge, legs extended/crossed | outdoor pathway, concrete curb/ledge, grass | bright natural daylight | young woman; sitting on ledge; school uniform style; black stockings; outdoor setting | blurry; distorted; bad anatomy | Confirm leg position, ledge setting, and whether clothing details are correct. |
| 7 | clear face, full-body, indoor, more negative tags | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590276558.jpg` | full body, seated on the floor | clear, looking towards the camera | black blazer, white shirt, striped tie, black skirt, tights/stockings, brown shoes | seated on floor, legs stretched, hands near lap | indoor wooden floor, window, blue curtains, urban view, black backpack | bright window light | full body; seated; blazer; striped tie; black tights; window view | outdoor; casual wear; cropped; distorted | Confirm that negative tags `outdoor` and `casual wear` are appropriate as negative prompts, not mistaken scene labels. |
| 13 | clear face, full-body, indoor, more negative tags | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590316106.jpg` | full body, seated on a wooden surface | clear, looking towards the camera | dark blazer, white shirt, striped tie, black tights/stockings, loafers | seated, legs extended, hands in lap | indoor wooden floor, large window, dark bag | bright natural window light | young woman; sitting; business attire; dark blazer; loafers | blurry; distorted; cartoon; overexposed | Confirm whether `business attire` is acceptable or should be normalized to school-uniform style. |
| 19 | sensitive clothing observation, clear face, complex clothing | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590402679.jpg` | full body, head to lower legs visible | clear | white shirt, black blazer/jacket, black pleated skirt, striped tie, thigh-high stockings/socks; model also noted a sensitive lower-clothing detail | seated on floor, leaning slightly forward, hands near lap | indoor wooden floor, large window, blue curtains, bag/strap | bright natural window light | school uniform; black stockings; striped tie; seated | real person; blurry; out of focus | Verify the sensitive clothing observation. If inaccurate or unnecessary, mark clothing_correct=no and note removal. Also check `real person` negative tag. |
| 25 | clear face, indoor, gesture, clothing visible | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590588956.jpg` | full body, seated on the floor | clear, looking directly at camera | black blazer, striped collared shirt, thigh-high stockings, shorts/skirt, loafers/shoes | seated, leaning forward, hand raised near face | indoor floor, window, blue/beige curtains, buildings outside | bright soft indoor/window light | young woman; sitting on floor; black blazer; striped shirt; thigh-high stockings; indoor setting | blurry; distorted; extra limbs | Confirm raised-hand gesture, shorts/skirt ambiguity, and face clarity. |
| 34 | half-body, clear face, indoor | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590811344.jpg` | half body, waist up with legs visible | clear | dark blazer, white shirt, striped tie, knee-high socks, black shoes | seated on round cushion, facing forward | indoor wooden floor, large window, building view, dark bag | bright natural window light | young woman; dark blazer; striped tie; black socks; sitting indoors | real person; out of focus; distorted | Confirm whether `half body` is correct or should be full-body/three-quarter. Check `real person` negative tag. |
| 37 | full-body, indoor bedroom, pose risk | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590865895.jpg` | full body, seated on a bed | clear, looking towards camera | blazer/jacket over collared shirt, striped detail, thigh-high stockings, skirt/shorts partially visible | seated on bed, leaning forward, legs open, hands near lap | bedroom, bed with white linens, gold headboard, pink bedside table | soft even indoor lighting | seated; black thigh-high stockings; school uniform style; bedroom setting | blurry; distorted; extra limbs | Confirm pose wording is accurate and appropriate; check if skirt/shorts ambiguity needs correction. |
| 49 | half-body, indoor doorway, complex clothing, more negative tags | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046591614313.jpg` | half body, upper torso to mid-thighs | clear | white shirt, striped tie, thigh-high stockings, dark fabric around lower body | leaning against doorframe, one hand near chin/neck, other holding fabric | indoor doorframe/wall structure | soft diffused indoor lighting | young woman; dark hair; white shirt; striped tie; black stockings; leaning; doorframe | blurry; deformed; extra limbs; low quality | Confirm half-body framing, fabric description, and whether negative tags are appropriate. |
| 154 | outdoor duplicate/source-path variant, full-body | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046589594674.jpg` | full body, seated on low wall | clear, looking towards camera | white collared shirt, black pleated skirt, thigh-high stockings, loafers, striped tie | seated on low concrete wall, legs down | outdoor retaining wall, grass, reddish-brown paved area | bright natural daylight | young woman; seated; school uniform; black stockings; outdoors | blurry; distorted; extra limbs | Confirm this training_data_raw path is an acceptable source for asset index review and not an unintended duplicate. |
| 181 | sensitive clothing observation, full-body, indoor, more negative tags | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590607764.jpg` | full body, head to feet visible | clear | black blazer/jacket, white shirt, red tie, black tights/stockings, dark shoes; model also noted a sensitive lower-clothing detail | seated on floor near wall/window, knees bent, feet toward viewer, upper body upright | indoor window with curtains, luggage/bag visible | bright natural window light | sitting on floor; black blazer; black tights; window background; indoor setting | blurry; distorted; outdoor setting; multiple people | Verify the sensitive clothing observation and whether `multiple people` is a wrong negative tag. |
| 184 | full-body, strong pose, indoor | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590627416.jpg` | full body, legs/torso/upper body visible | clear, looking towards viewer | black blazer/jacket, black bottoms/leggings, dark shoes with visible soles | seated on floor near window, legs raised/crossed, body angled to camera | indoor window, light curtains, blue curtain, wood/laminate floor | bright natural window light | seated; black blazer; black leggings; window light; full body | blurry; deformed; extra limbs | Confirm unusual leg pose, body visibility, and whether clothing lacks shirt/tie detail. |

## Manual Review Table

Fill this table during image review.

| queue_row_index | face_correct yes/no | clothing_correct yes/no | pose_correct yes/no | scene_correct yes/no | usable_for_asset_index yes/no | notes |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |
| 7 |  |  |  |  |  |  |
| 13 |  |  |  |  |  |  |
| 19 |  |  |  |  |  |  |
| 25 |  |  |  |  |  |  |
| 34 |  |  |  |  |  |  |
| 37 |  |  |  |  |  |  |
| 49 |  |  |  |  |  |  |
| 154 |  |  |  |  |  |  |
| 181 |  |  |  |  |  |  |
| 184 |  |  |  |  |  |  |

## Stop Point

Stop here and wait for manual confirmation before planning or running any 100-image `main_caption` batch.
