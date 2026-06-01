# P0.5 Manual Check Image Path Report

Generated: 2026-06-01

## Scope

- Source checklist: `docs\02_caption_strategy\p05_main_caption_gemma4_e4b_batch_001_manual_checklist.md`
- Batch JSONL used only to recover original existing paths for contact sheet: `metadata\p05_caption_results_main_gemma4_e4b_batch_001.jsonl`
- CSV output: `metadata\p05_manual_check_batch_001_image_paths.csv`
- Contact sheet output: `outputs\p05_manual_check_batch_001_contact_sheet.jpg`

No files or folders were renamed. `metadata\p05_caption_queue.csv` was not modified. No model, ComfyUI generation, or LoRA training was run.

## Summary

| Metric | Count |
| --- | ---: |
| Parsed checklist paths | 12 |
| Parsed checklist paths that exist as written | 0 |
| Parsed checklist paths missing as written | 12 |
| Recovered original JSONL paths that exist | 12 |
| Paths with mojibake fragments | 12 |

## Mojibake Findings

All 12 parsed checklist paths contain mojibake fragments. The likely intended folder text is inferred only for notes and was not used to rename anything:

- `??????` may correspond to `????`.
- `???` may correspond to `??`.
- `???` may correspond to `??`.
- Combined likely folder text: `[????] ?? - ??`.

## Path Table

| queue_row_index | checklist path exists | recovered JSONL path exists | file_name | parent_dir | source_root | mojibake | notes |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | false | true | `17046589594674.jpg` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images` | true | Use the recovered JSONL path in Explorer for manual review. |
| 4 | false | true | `17046589900698.jpg` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images` | true | Use the recovered JSONL path in Explorer for manual review. |
| 7 | false | true | `17046590276558.jpg` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images` | true | Use the recovered JSONL path in Explorer for manual review. |
| 13 | false | true | `17046590316106.jpg` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images` | true | Use the recovered JSONL path in Explorer for manual review. |
| 19 | false | true | `17046590402679.jpg` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images` | true | Use the recovered JSONL path in Explorer for manual review. |
| 25 | false | true | `17046590588956.jpg` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images` | true | Use the recovered JSONL path in Explorer for manual review. |
| 34 | false | true | `17046590811344.jpg` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images` | true | Use the recovered JSONL path in Explorer for manual review. |
| 37 | false | true | `17046590865895.jpg` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images` | true | Use the recovered JSONL path in Explorer for manual review. |
| 49 | false | true | `17046591614313.jpg` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣` | `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images` | true | Use the recovered JSONL path in Explorer for manual review. |
| 154 | false | true | `17046589594674.jpg` | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣` | `D:\sd.webui\comic_project\training_data_raw` | true | Use the recovered JSONL path in Explorer for manual review. |
| 181 | false | true | `17046590607764.jpg` | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣` | `D:\sd.webui\comic_project\training_data_raw` | true | Use the recovered JSONL path in Explorer for manual review. |
| 184 | false | true | `17046590627416.jpg` | `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[绱ф€ヤ紒鍒抅 灏忔仼 - 榛戜笣` | `D:\sd.webui\comic_project\training_data_raw` | true | Use the recovered JSONL path in Explorer for manual review. |

## Explorer Location Guidance

Because the checklist paths do not exist as written, use the recovered original JSONL paths or locate files by filename under these roots:

- `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images\XiaoEn\[????] ?? - ??`
- `D:\sd.webui\comic_project\training_data_raw\XiaoEn\01_face\[????] ?? - ??`

In Explorer, open the relevant root folder and search for the numeric `file_name`, for example `17046589594674.jpg`.

## Rename Recommendation

Default recommendation: do not rename files or folders now.

Reason: the actual files are still reachable through the original batch JSONL paths, and renaming would break existing metadata paths unless a path-mapping migration is prepared first.

If future cleanup requires renaming, first create and validate a metadata path mapping, then update all affected metadata references together. Do not rename ad hoc from Explorer.

## Contact Sheet

A local contact sheet was generated from the recovered existing JSONL paths, not from the corrupted checklist paths:

- `outputs\p05_manual_check_batch_001_contact_sheet.jpg`

This file is for local manual review only. Do not upload or commit it.
