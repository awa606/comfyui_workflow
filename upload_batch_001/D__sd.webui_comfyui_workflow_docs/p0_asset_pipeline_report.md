# P0 素材管线验证报告

当前阶段只完成 P0：基础索引、视频抽帧、pHash 去重、模糊检测、InsightFace 人脸检测与聚类。

本报告是本地审核辅助文档。CSV、NPZ、抽帧图和 contact sheet 不上传到 GitHub。

## 统计摘要

- 扫描图片数量：8298
- 扫描视频数量：6135
- 抽帧数量：5564
- 检测到有人脸的素材数量：8093
- 聚类出的 face cluster 数量：474
- exact pHash 重复素材数量：165
- near pHash 近重复候选素材数量：448
- 模糊或低质量候选数量：5592

## 审核优先级统计

- A：1317，优先审核的高质量身份候选。
- B：934，可进入 role_001 候选池的次优身份/半身素材。
- C：7268，可作为服装、姿势、体态或人工复核素材。
- D：4343，重复、严重模糊、不可读或低价值素材。

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

低质量候选主要由 `blurred_frame`、`exact_duplicate`、`no_face_detected`、`unreadable_image` 标注。
人工审核时优先按 `review_priority` 排序，再参考 `reject_reason`、`duplicate_level` 和 `face_quality_score`。

## 生成物

- `metadata/source_inventory.csv`
- `metadata/frame_index.csv`
- `metadata/duplicate_candidates.csv`
- `metadata/face_index.csv`
- `metadata/face_clusters.csv`
- `metadata/cluster_review.csv`
- `metadata/master_asset_index.csv`
- `outputs/cluster_contact_sheets/cluster_*.jpg`

## 下一步

1. 打开 `outputs/cluster_contact_sheets/cluster_*.jpg` 进行人工聚类审核。
2. 在 `metadata/cluster_review.csv` 中填写 `user_confirmed_character_id=role_001`。
3. 运行 `python scripts/export_role_candidates.py --role role_001` 导出候选清单。
4. 当 FaceID 候选达到 3-8 张、role_001 候选达到 20-40 张后，再进入 FaceID / IPAdapter 测试。

## 边界

- 未训练 LoRA。
- 未进行 ComfyUI 批量出图。
- 未安装 DWPose / SAM / GroundingDINO / Depth Anything。
- 未移动、删除、覆盖原始素材。
- 生成的 CSV、NPZ、抽帧图和 contact sheet 为本地审核产物，不上传到 GitHub。
