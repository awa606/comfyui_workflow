# Current CLI Stage Report

Generated: 2026-05-30

## 1. 当前阶段

阶段 P0.5-D。

## 2. 判断依据

- P0.5 本地素材接入脚本已存在。
- `metadata\p05_local_source_inventory.csv` 已存在。
- `metadata\p05_face_crops_identity_only.csv` 已存在。
- `metadata\p05_caption_queue.csv` 已存在。
- `docs\01_p0_asset_pipeline\p05_caption_queue_report.md` 在本次检查前不存在，因此 caption queue 质检尚未完成。
- 未发现标准命名的小批量 caption 结果文件：
  - `metadata\p05_caption_results_quick_screen.csv`
  - `metadata\p05_caption_results_main_caption.csv`
  - `metadata\p05_caption_results_style_detail.csv`

备注：`metadata` 下存在 smoke caption 结果文件，但当前阶段定义没有 smoke 专项，且不能替代 caption queue 质检。

## 3. 已存在文件

项目文档：

- `README.md`
- `docs\README.md`
- `docs\00_project_overview\current_stage_report.md`
- `docs\01_p0_asset_pipeline\p0_asset_pipeline_report.md`
- `docs\01_p0_asset_pipeline\p0_5_local_source_ingestion.md`
- `docs\02_caption_strategy\local_vlm_caption_strategy.md`
- `docs\03_model_strategy\model_upgrade_strategy.md`
- `docs\99_safety_scope\safety_and_scope_boundary.md`
- `docs\role_001_review_workflow.md`
- `skills\comfyui-character-system-context\SKILL.md`

P0.5 脚本：

- `scripts\ingest_local_sources_p05.py`
- `scripts\export_face_crops_p05.py`
- `scripts\prepare_safe_caption_queue_p05.py`
- `scripts\export_role_candidates.py`

本地生成物：

- `metadata\p05_local_source_inventory.csv`
- `metadata\p05_face_crops.csv`
- `metadata\p05_face_crops_identity_only.csv`
- `metadata\p05_caption_queue.csv`
- `outputs\p05_face_crops\`
- `outputs\p05_face_crops_identity_only\`

## 4. 缺失文件

- `docs\01_p0_asset_pipeline\p05_caption_queue_report.md` 在本次检查前缺失。
- `metadata\p05_caption_results_quick_screen.csv`
- `metadata\p05_caption_results_main_caption.csv`
- `metadata\p05_caption_results_style_detail.csv`

## 5. 当前不能做什么

- 不能训练 LoRA。
- 不能创建训练集。
- 不能下载大模型。
- 不能运行 ComfyUI 批量出图。
- 不能调用 qwen3-vl 或 gemma 进行全量 caption。
- 不能在未经确认前进入 gemma4:e2b quick_screen 小批量测试。
- 不能处理 `explicit`、`R18`、`03_explicit_action`、`styles\explicit`、`VIP` 或其他排除范围。
- 不能上传或提交 `metadata\p05_*.csv`。
- 不能上传或提交 `outputs\p05_face_crops_identity_only`。
- 不能上传图片、视频、CSV、NPZ、模型文件。
- 不能删除、移动、覆盖原始素材。

## 6. 下一步建议

因为 `metadata\p05_caption_queue.csv` 已存在，下一步应先完成 caption queue 质检，生成：

- `docs\01_p0_asset_pipeline\p05_caption_queue_report.md`

质检通过并经用户确认后，才可以进入 `gemma4:e2b` 的 `quick_screen` 小批量测试。

## 7. 是否需要用户确认

需要。完成 caption queue 质检后，必须由用户确认是否进入 `gemma4:e2b quick_screen` 小批量测试。
