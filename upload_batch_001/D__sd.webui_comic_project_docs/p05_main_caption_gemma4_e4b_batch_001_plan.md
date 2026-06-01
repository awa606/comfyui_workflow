# P0.5 Main Caption Gemma4 E4B Batch 001 Plan

Generated: 2026-05-31

## Decision

Temporary main caption model:

- `gemma4:e4b-it-q4_K_M`

Basis:

- `docs\02_caption_strategy\p05_main_caption_model_compare_report.md` recommends `gemma4:e4b-it-q4_K_M` because it had 100% success, 100% valid JSON, useful caption detail, and moderate response time in the 10-image comparison.

## Scope

This is a plan only. Do not run the batch until the user confirms.

Selection source:

- `metadata\p05_caption_results_quick_sample.jsonl`

Corrected candidate filter:

- Outer `inference_status == "ok"`
- Outer `error` is empty
- Parsed `caption_json.safe_for_p05 == true`
- Parsed `caption_json.needs_manual_review == false`
- `image_role == "quick_screen"`
- `source_person_id == "XiaoEn"`
- No excluded/risk keyword in `image_path`

Excluded/risk keywords checked:

- `explicit`
- `R18`
- `r18`
- `03_explicit`
- `03_explicit_action`
- `05_style_ryota`
- `styles\explicit`
- `VIP`
- `全裸`
- `插入`
- `扩张`
- `ahegao`
- `捆绑`

Candidate result:

- Corrected candidates: 30
- Excluded/risk path hits: 0
- Planned batch size: 30

## Batch Configuration

| Setting | Value |
| --- | --- |
| Batch id | `main_caption_gemma4_e4b_batch_001` |
| Model | `gemma4:e4b-it-q4_K_M` |
| Input role | `quick_screen` source images |
| Source person | `XiaoEn` |
| Exclude `face_crop_review` | yes |
| Output target | `metadata\p05_caption_results_main_gemma4_e4b_batch_001.jsonl` |
| Modify `metadata\p05_caption_queue.csv` | no |
| Upload JSONL / CSV / images | no |
| Full caption | no |
| Training | no |
| ComfyUI generation | no |

## Coverage Intent

The 30 planned images cover:

- clear face references
- half-body framing
- full-body or near full-body framing
- indoor scenes
- outdoor scenes
- clear clothing and accessories
- clear seated / standing / leaning poses
- window, bed, outdoor grass / ledge, and doorway settings

## Planned Rows

| queue_row_index | Coverage tags | image_path | quick caption |
| ---: | --- | --- | --- |
| 1 | outdoor, standing, full-body, clothing visible | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046589594674.jpg` | A person wearing black shorts and a white shirt is standing outdoors on a grassy area. |
| 4 | outdoor, seated, full-body, clothing visible | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046589900698.jpg` | A young woman with long dark hair is sitting on a concrete ledge outdoors, wearing a white shirt and a black skirt. |
| 7 | indoor, seated, window, uniform, bag | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590276558.jpg` | A person is sitting in front of a window, wearing a black blazer and red and white striped tie, with a black bag beside them. |
| 10 | indoor, seated, window, uniform, bag | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590296768.jpg` | A person is sitting next to a window, wearing a black blazer and tie, with a black bag nearby. |
| 13 | indoor, seated, clear face, uniform | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590316106.jpg` | A young woman is sitting in front of a window, wearing a dark blazer and tie. |
| 16 | indoor, seated, window, stockings, bag | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590338008.jpg` | A person is sitting in front of a window, wearing black stockings and a blazer with a red tie, next to a black bag. |
| 19 | indoor, seated, uniform, upper body | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590402679.jpg` | A person wearing a black and red striped tie and a white shirt, sitting near a window. |
| 22 | indoor, seated, window, striped shirt, tie | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\1704659042653.jpg` | A young woman is sitting in front of a window, wearing a black and white striped shirt and a red tie. |
| 25 | indoor, seated, clear face, blazer, shirt | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590588956.jpg` | A young woman sitting indoors, wearing a black blazer and red and white striped shirt, looking at the camera. |
| 28 | indoor, floor seated, pose visible, window | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590607764.jpg` | A person is sitting on the floor, wearing black and red pants, leaning against a window. |
| 31 | indoor, seated, legs extended, pose visible | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590627416.jpg` | A person is sitting with their legs extended, wearing black and red bottoms, next to a window. |
| 34 | indoor, clear face, blazer, tie, window | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590811344.jpg` | A young woman with long dark hair is sitting in front of a window, wearing a dark blazer and a red and blue striped tie. |
| 37 | indoor, bed, seated, striped shirt | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590865895.jpg` | A person is sitting on a bed with a gold frame, wearing a black and white striped shirt. |
| 40 | indoor, bed, seated, clothing visible | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590954188.jpg` | A person is sitting on a bed, wearing black shorts and socks, with a light-colored shirt visible. |
| 43 | indoor, bed, seated, blazer, shirt | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590971959.jpg` | A person wearing a black blazer and white shirt is sitting on a bed. |
| 46 | indoor, clear face, seated, metal grate | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046591573067.jpg` | A person with long dark hair is sitting in front of a metal grate. |
| 49 | indoor, leaning pose, doorway, fabric | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046591614313.jpg` | A person with long dark hair is leaning against a doorframe, holding a piece of dark fabric. |
| 154 | outdoor, seated, face crop source, clothing visible | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046589594674.jpg` | A young woman with long dark hair is sitting on a low concrete wall outdoors, wearing a white shirt and black shorts. |
| 157 | outdoor, seated, face crop source, clothing visible | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046589900698.jpg` | A young woman with long dark hair is sitting on a concrete ledge outdoors, wearing a white shirt and a black skirt. |
| 160 | indoor, face crop source, seated, window, uniform | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590276558.jpg` | A person is sitting in front of a window, wearing a black blazer and red and white striped tie, with a black bag beside them. |
| 163 | indoor, face crop source, seated, window, uniform | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590296768.jpg` | A person is sitting next to a window, wearing a black blazer and tie, with a black bag nearby. |
| 166 | indoor, face crop source, clear face, blazer, tie | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590316106.jpg` | A young woman is sitting in front of a window, wearing a dark blazer and tie. |
| 169 | indoor, face crop source, seated, stockings, bag | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590338008.jpg` | A person is sitting in front of a window, wearing black stockings and a blazer with a red tie, next to a black bag. |
| 172 | indoor, face crop source, upper body, tie | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590402679.jpg` | A person wearing a black and red striped tie and a white shirt, sitting near a window. |
| 175 | indoor, face crop source, window, striped shirt | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\1704659042653.jpg` | A young woman sitting in front of a window, wearing a black and white striped shirt and a red tie. |
| 178 | indoor, face crop source, clear face, blazer | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590588956.jpg` | A young woman sitting indoors, wearing a black blazer and red and white striped shirt, looking at the camera. |
| 181 | indoor, face crop source, floor seated, pose visible | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590607764.jpg` | A person is sitting on the floor, wearing black and red pants, leaning against a window. |
| 184 | indoor, face crop source, legs extended, pose visible | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590627416.jpg` | A person is sitting with their legs extended, wearing black and red bottoms, leaning against a window. |
| 187 | indoor, face crop source, clear face, blazer, tie | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590811344.jpg` | A young woman with long dark hair is sitting in front of a window, wearing a dark blazer and a red and blue striped tie. |
| 190 | indoor, face crop source, bed, seated, striped shirt | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣\17046590865895.jpg` | A person wearing a black and white striped shirt is sitting on a bed. |

## Planned Output JSONL Fields

Each output row should include:

- `queue_row_index`
- `image_path`
- `source_person_id`
- `source_image_role`
- `quick_caption`
- `model`
- `status`
- `response_seconds`
- `json_valid`
- `parsed_json`
- `raw_response`
- `error`

The `parsed_json` object should use the same main-caption schema from the model comparison run:

- `safe_for_p05`
- `needs_manual_review`
- `person_description`
- `hair_face`
- `clothing`
- `pose`
- `scene`
- `caption`
- `positive_tags`
- `negative_tags`
- `quality_notes`

## Stop Condition

Stop after writing this plan and wait for user confirmation. Do not run the batch automatically.
