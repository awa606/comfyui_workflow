# P0.5 Caption Queue Report

Generated: 2026-05-30

## 1. Caption Queue 总行数

- `metadata\p05_caption_queue.csv`: 2776 行

## 2. image_role 分布

| image_role | count |
| --- | ---: |
| quick_screen | 690 |
| main_caption | 690 |
| style_detail | 1294 |
| face_crop_review | 102 |

## 3. recommended_model 分布

| recommended_model | count |
| --- | ---: |
| gemma4:e2b | 792 |
| qwen3-vl:8b | 690 |
| gemma4:e4b-it-q4_K_M | 1294 |

说明：`gemma4:e2b` 包含 `quick_screen` 与 `face_crop_review`。

## 4. source_person_id 前 30 个及数量

| source_person_id | count |
| --- | ---: |
| XiaoEn | 2172 |
| styles | 604 |

## 5. image_path 排除关键词检查

| keyword | count |
| --- | ---: |
| explicit | 0 |
| R18 | 0 |
| r18 | 0 |
| 03_explicit | 0 |
| 03_explicit_action | 0 |
| 05_style_ryota | 0 |
| styles\explicit | 0 |
| VIP | 0 |
| 全裸 | 0 |
| 插入 | 0 |
| 扩张 | 0 |
| ahegao | 0 |
| 捆绑 | 0 |

结论：当前 caption queue 中未发现上述排除关键词命中。

## 6. face_crop_review 来源检查

| check | count |
| --- | ---: |
| face_crop_review total | 102 |
| 来自 `outputs\p05_face_crops_identity_only` | 102 |
| 来自 `outputs\p05_face_crops\styles` | 0 |
| 其他来源 | 0 |

结论：`face_crop_review` 只来自 `outputs\p05_face_crops_identity_only`，未发现来自 `outputs\p05_face_crops\styles` 的记录。

## 7. styles/safe 原图进入 main_caption / style_detail 检查

| image_role | count |
| --- | ---: |
| style_detail | 604 |

结论：`styles` 来源当前进入 `style_detail`，未进入 `main_caption`。这与当前队列内容一致；如预期要求 styles/safe 同时进入 `main_caption`，需要在下一步前确认队列策略。

## 8. 执行边界

- 未上传 CSV。
- 未上传图片。
- 未运行 Ollama。
- 未调用任何视觉模型。
- 未运行 ComfyUI。
- 未修改 `metadata` 或 `outputs`。
