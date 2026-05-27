# role_001 审核与候选导出流程

本流程用于把 P0 输出从“脚本可运行”推进到“可人工审核、可确认 role_001、可进入 FaceID / IPAdapter 测试”。

当前仍然不训练 LoRA、不下载大模型、不上传素材、CSV、NPZ、图片、视频或模型文件。

## 1. 打开 Contact Sheet

聚类脚本会生成：

```text
outputs/cluster_contact_sheets/cluster_001.jpg
outputs/cluster_contact_sheets/cluster_002.jpg
...
```

人工审核时按编号打开这些图片。每张 contact sheet 代表一个候选 face cluster，优先看：

- 脸是否明显是同一个角色。
- 是否混入其他角色。
- 是否有大量遮挡、糊脸、侧脸、低清图。
- 是否只适合作为服装、姿势、发型、鞋或体态参考。

contact sheet 是本地审核图，不提交到 GitHub。

## 2. 填写 cluster_review.csv

打开：

```text
metadata/cluster_review.csv
```

脚本会自动填充：

- `cluster_id`
- `sample_count`
- `face_count`
- `top_source_person_ids`
- `best_face_quality`
- `avg_face_quality`

人工填写字段：

| 字段 | 填写方式 |
|---|---|
| `user_confirmed_character_id` | 如果确认是样板角色，填 `role_001`。不是则留空或填其他内部编号。 |
| `is_clean_cluster` | 纯净同一角色填 `yes`；混入其他角色填 `no`。 |
| `merge_with_cluster` | 如果应该和另一个 cluster 合并，填目标 cluster id，例如 `cluster_009`。 |
| `split_needed` | 如果一个 cluster 内混了多个角色，填 `yes`。 |
| `notes` | 用安全话术记录用途，例如 `good_faceid_candidate`、`outfit_reference_only`、`pose_reference_only`、`blurred`。 |

`top_source_person_ids` 用来快速判断这个 cluster 主要来自哪个源文件夹；如果同一个 cluster 来自多个素材文件夹，要重点检查是否混人。

## 3. 导出 role_001 候选

确认 cluster 后运行：

```powershell
python scripts\export_role_candidates.py --role role_001
```

默认模式是：

```text
--copy-mode manifest-only
```

它只输出：

```text
metadata/role_001_candidate_export.csv
```

不会复制、移动、删除或覆盖原始图片。

如果需要把候选素材硬链接到 `characters/role_001` 的候选目录，可显式运行：

```powershell
python scripts\export_role_candidates.py --role role_001 --copy-mode hardlink
```

硬链接目标目录规则：

| 候选类型 | 目标目录 |
|---|---|
| FaceID 候选 | `characters/role_001/selected_for_faceid` |
| LoRA 候选 | `characters/role_001/selected_for_lora` |
| 服装参考 | `characters/role_001/outfits/outfit_unassigned` |
| 姿势参考 | `characters/role_001/pose_refs` |
| 其他参考 | `characters/role_001/body_reference` |

硬链接仍然是本地素材文件，不提交到 GitHub。

## 4. 什么时候可以进入 FaceID / IPAdapter 测试

满足以下条件后，可以进入 FaceID / IPAdapter 测试：

- `cluster_review.csv` 中至少有 1 个干净的 `role_001` cluster。
- `metadata/role_001_candidate_export.csv` 中有 3-8 张 `use_for_faceid=yes` 的高质量脸图。
- 候选脸图尽量包含正面、轻微侧脸、不同表情，但不要严重遮挡。
- `selected_for_faceid` 中没有明显混入其他角色。
- `master_asset_index.csv` 中优先级 A/B 的素材数量足够做第一轮测试。

FaceID 测试目标是先生成 6 张角色标准图：正面半身、正面全身、45 度半身、侧面、平静表情、紧张表情。

## 5. 什么时候才考虑 LoRA

当前阶段不训练 LoRA。

只有在以下情况才进入 LoRA 决策：

- FaceID / IPAdapter 用 3-8 张高质量脸图仍然无法稳定保持角色身份。
- role_001 已经有 20-40 张人工确认的候选图。
- 候选图不是大量近重复，也不是同一角度、同一服装、同一表情。
- 身份层、服装层、发型层、妆容层的边界已经分清。
- 已明确第一版只训练“角色身份 LoRA”，不训练万能 LoRA。

LoRA 决策文档参考：

```text
docs/04_lora_strategy/lora_training_decision.md
```
