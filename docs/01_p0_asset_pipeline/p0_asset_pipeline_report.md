# P0 素材管线验证报告

当前阶段只完成 P0：基础索引、视频抽帧、去重、模糊检测、InsightFace 人脸检测与聚类。

本轮为 P0 验证跑：扫描全量素材源，视频抽帧采用 `--max-frames-per-video 1`，即每个视频最多抽 1 帧；后续可用 `--max-frames-per-video 0` 做全量逐秒抽帧。

## 统计摘要

- 扫描图片数量：8298
- 扫描视频数量：6135
- 抽帧数量：5564
- 检测到有人脸的素材数量：8093
- 聚类出的 face cluster 数量：474
- pHash 重复候选素材数量：165
- 模糊或低质量候选数量：5592

## 样本最多的 cluster

- cluster_004: 1174 assets
- cluster_009: 815 assets
- cluster_001: 771 assets
- cluster_019: 668 assets
- cluster_002: 647 assets
- cluster_011: 512 assets
- cluster_015: 436 assets
- cluster_036: 434 assets
- cluster_135: 263 assets
- cluster_005: 253 assets

## 质量较差素材

低质量候选主要由 `blurred_frame`、`duplicate_candidate`、`no_face_detected` 标注。请优先在 `metadata/master_asset_index.csv` 中按 `reject_reason` 过滤。

## 生成物

- `metadata/source_inventory.csv`
- `metadata/frame_index.csv`
- `metadata/duplicate_candidates.csv`
- `metadata/face_index.csv`
- `metadata/face_clusters.csv`
- `metadata/cluster_review.csv`
- `metadata/master_asset_index.csv`
- `outputs/cluster_contact_sheets/cluster_*.jpg`

## 边界

- 未训练 LoRA。
- 未进行 ComfyUI 批量出图。
- 未安装 DWPose / SAM / GroundingDINO / Depth Anything。
- 未移动、删除原始素材。
- 生成的 CSV 和 contact sheet 为本地审核产物，不上传到 GitHub。
