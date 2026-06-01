# 当前阶段报告

更新时间：2026-05-27  
项目名称：《基于 ComfyUI 的可控式虚拟角色换装与多体型生成系统》

## 1. 当前定位

当前项目仍处于素材资产化与 P0 素材管线验证阶段。

当前不进入：

- LoRA 训练阶段
- ComfyUI 批量出图阶段
- 最终漫画生产阶段
- P1 姿势/分割/深度大模型集成阶段
- P2 自动 caption / image-to-3D / Blender 自动化阶段

当前目标是把本地素材源整理成可审核、可追踪、可人工复核的角色资产索引，为后续 FaceID、IPAdapter、角色 LoRA 决策、换装系统、多体型生成系统和 ComfyUI 漫画化打基础。

## 2. 项目路径关系

根目录：

- `D:\sd.webui`

主要工程目录：

- `D:\sd.webui\comic_project`：当前 Git 仓库工作目录，保存文档、脚本、技能、空目录占位和工作流配置。
- `D:\sd.webui\ComfyUI`：ComfyUI 运行环境，不修改核心代码。
- `D:\sd.webui\webui`：A1111 运行环境和旧模型共享来源。
- `D:\sd.webui\train_material`：本地素材源之一，只读扫描。
- `D:\sd.webui\douyin_download`：本地素材源之一，只读扫描。

GitHub 仓库：

- `awa606/comfyui_workflow`
- 当前主分支：`main`

## 3. 关键安全边界

- 不训练 LoRA。
- 不下载大模型。
- 不安装 DWPose / SAM / GroundingDINO / Depth Anything。
- 不删除、移动、覆盖原始素材。
- 不上传图片、视频、抽帧图、contact sheet、CSV、NPZ、模型文件到 GitHub。
- 不修改 ComfyUI 核心代码。
- InsightFace 只作为身份层：人脸检测、质量评分、embedding、聚类。

素材来自本地目录；素材是否可用于后续训练必须经过人工审核和授权判断。当前阶段只生成可审核索引，不做训练数据集定稿。

## 4. 仓库目录分类

### `docs/`

保存项目规划、边界、模型路线、素材规范和阶段报告。当前已有约 30 个文档，重要文档包括：

- `docs/00_project_overview/current_stage_report.md`：当前阶段总报告。
- `docs/01_p0_asset_pipeline/p0_asset_pipeline_report.md`：P0 管线运行报告。
- `docs/00_project_overview/project_state.md`：项目状态对齐文档。
- `docs/01_p0_asset_pipeline/asset_triage_pipeline.md`：素材分诊流程。
- `docs/03_model_strategy/model_upgrade_strategy.md`：P0/P1/P2 模型升级路线。
- `docs/99_safety_scope/safety_and_scope_boundary.md`：安全与范围边界。
- `docs/04_lora_strategy/lora_training_decision.md`：LoRA 训练决策模板。

### `scripts/`

保存素材管线和项目辅助脚本。P0 关键脚本：

- `scripts/scan_sources.py`
- `scripts/extract_video_frames.py`
- `scripts/extract_single_video_frame.py`
- `scripts/filter_duplicates.py`
- `scripts/run_face_index.py`
- `scripts/cluster_faces.py`
- `scripts/build_master_asset_index.py`
- `scripts/p0_common.py`

旧/辅助脚本：

- `scripts/triage_douyin_assets.py`
- `scripts/build_role_manifest.py`
- `scripts/extract_keyframes_role.py`
- `scripts/make_model_contact_sheet.py`
- `scripts/check_hf_model_card.py`

### `characters/role_001/`

样板角色资产目录，当前用于 role_001 样板流程。主要子目录：

- `raw_images`
- `raw_videos`
- `extracted_frames`
- `identity_faces`
- `upper_body`
- `full_body`
- `body_reference`
- `outfits/outfit_001`
- `outfits/outfit_002`
- `outfits/outfit_003`
- `hairstyles`
- `makeup`
- `shoes_accessories`
- `pose_refs`
- `scene_refs`
- `selected_for_faceid`
- `selected_for_lora`
- `rejected`
- `captions`
- `metadata`

### `asset_library/`

通用素材库框架，只提交空目录占位，不提交实际图片或 CSV。用于沉淀非 role_001 专属素材：

- `identity_faces`
- `body_refs`
- `outfit_refs`
- `hairstyle_refs`
- `makeup_refs`
- `leg_shoes_refs`
- `pose_refs`
- `scene_refs`
- `rejected`
- `metadata`

### `metadata/`

本地 P0 生成物目录。只提交 `.gitkeep`，不提交 CSV/NPZ。

当前本地生成：

- `metadata/source_inventory.csv`
- `metadata/frame_index.csv`
- `metadata/duplicate_candidates.csv`
- `metadata/face_index.csv`
- `metadata/face_clusters.csv`
- `metadata/cluster_review.csv`
- `metadata/master_asset_index.csv`
- `metadata/face_embeddings.npz`

### `outputs/`

本地输出目录。只提交 `.gitkeep`，不提交生成图片。

当前本地生成：

- `outputs/p0_extracted_frames/`
- `outputs/cluster_contact_sheets/cluster_*.jpg`
- `outputs/role_001_faceid_tests/`
- `outputs/model_tests/`

### `models_research/`

模型调研空目录框架：

- `image_to_3d`
- `depth_estimation`
- `pose_estimation`
- `face_identity`
- `segmentation`
- `image_editing`

## 5. 素材源与 P0 统计

素材源：

- `D:\sd.webui\train_material`
- `D:\sd.webui\douyin_download`

P0 验证跑口径：

- 扫描全量素材源。
- 视频抽帧采用 `--max-frames-per-video 1`，即每个视频最多抽 1 帧。
- 后续可用 `--max-frames-per-video 0` 做全量逐秒抽帧。

统计：

- 媒体文件总数：14433
- 图片：8298
- 视频：6135
- 成功抽帧：5564
- 视觉资产总数：13862
- pHash 重复候选素材：165
- pHash 重复候选组：135
- InsightFace 检测到 face：8485
- 有人脸的素材资产：8093
- face cluster：474
- cluster contact sheet：474
- 模糊或低质量候选：5592

样本最多的 cluster：

- `cluster_004`: 1174 assets
- `cluster_009`: 815 assets
- `cluster_001`: 771 assets
- `cluster_019`: 668 assets
- `cluster_002`: 647 assets
- `cluster_011`: 512 assets
- `cluster_015`: 436 assets
- `cluster_036`: 434 assets
- `cluster_135`: 263 assets
- `cluster_005`: 253 assets

## 6. P0 管线命令

```powershell
cd D:\sd.webui\comic_project
python scripts\scan_sources.py --skip-hash
python scripts\extract_video_frames.py --fps 1 --max-frames-per-video 1 --workers 8 --timeout-seconds 8
python scripts\filter_duplicates.py --workers 8
python scripts\run_face_index.py --det-size 160 --max-dim 480
python scripts\cluster_faces.py --threshold 0.42 --contact-sheet-samples 24
python scripts\build_master_asset_index.py
```

## 7. 当前待人工处理

下一步不是训练，而是人工审核：

1. 打开 `outputs/cluster_contact_sheets/cluster_*.jpg`。
2. 在 `metadata/cluster_review.csv` 中填写：
   - `user_confirmed_character_id`
   - `is_clean_cluster`
   - `merge_with_cluster`
   - `split_needed`
   - `notes`
3. 选出 role_001 对应 cluster。
4. 决定是否需要对重点 cluster 用更高 InsightFace 参数二次跑。
5. 再进入 FaceID / IPAdapter 测试。

## 8. Git 推送规则

每次完成任务后提交并推送到 GitHub，但只允许提交：

- 文档
- 脚本
- 技能 `SKILL.md`
- workflow JSON
- `.gitkeep`
- 安全配置

禁止提交：

- 图片、视频、抽帧图、contact sheet
- CSV、NPZ、本地日志
- `.safetensors`、`.ckpt`、`.pt`、`.pth`、`.bin`、`.onnx`
- 未审核素材
- ComfyUI/A1111 核心代码改动

当前 `.gitignore` 已保护 `metadata/*`、`outputs/*`、`characters/**/*.jpg`、`asset_library/**/*.jpg`、模型文件等生成物和大文件。
