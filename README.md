# 《基于 ComfyUI 的可控式虚拟角色换装与多体型生成系统》

本仓库用于管理基于 ComfyUI 的可控式虚拟角色换装与多体型生成系统。仓库只保存可复用的工作流、脚本、文档、技能说明和空目录占位，不保存素材、生成图、CSV/NPZ 索引结果或模型权重。

## 当前阶段

当前处于 **P0：素材资产化与管线验证阶段**。

本阶段目标是把本地素材源：

- `D:\sd.webui\train_material`
- `D:\sd.webui\douyin_download`

整理成可人工审核、可确认 `role_001`、可进入 FaceID / IPAdapter 测试的素材索引。

当前不进行：

- LoRA 训练
- ComfyUI 批量出图
- 大模型下载
- DWPose / SAM / GroundingDINO / Depth Anything 集成
- 最终漫画生产
- 完整 3D 角色编辑器生产

## 目录结构

| 目录 | 用途 | 上传规则 |
|---|---|---|
| `characters/role_001` | 第一个样板角色资产目录，包含 raw、抽帧、身份脸、上半身、全身、服装、姿势、候选素材等子目录 | 只提交空目录占位，不提交图片/视频/CSV |
| `asset_library` | 通用素材库骨架，用于沉淀非 role_001 专属的身份、身体、服装、发型、妆容、腿/鞋、姿势、场景素材 | 只提交空目录占位 |
| `metadata` | P0 本地生成的索引、manifest、聚类审核表、embedding NPZ | 不提交 CSV/NPZ |
| `outputs` | 抽帧、cluster contact sheet、FaceID 测试输出、模型测试输出 | 不提交图片/视频 |
| `models_research` | image-to-3D、depth、pose、face identity、segmentation、image editing 等模型调研目录 | 不提交模型或测试素材 |
| `scripts` | P0 管线脚本和项目辅助脚本 | 可提交 |
| `docs` | 项目规划、素材标准、模型路线、审核流程、安全边界 | 可提交 |
| `skills` | 给 Codex / 网页 ChatGPT 读取的项目上下文 skill | 可提交 |
| `workflows` | ComfyUI 工作流 JSON | 可提交 JSON，不提交输出图 |

## P0 命令

在 `D:\sd.webui\comic_project` 下运行：

```powershell
python scripts\scan_sources.py --skip-hash
python scripts\extract_video_frames.py --fps 1 --max-frames-per-video 1 --workers 8 --timeout-seconds 8
python scripts\filter_duplicates.py --workers 8
python scripts\run_face_index.py --det-size 160 --max-dim 480
python scripts\cluster_faces.py --threshold 0.42 --contact-sheet-samples 24
python scripts\build_master_asset_index.py
```

确认 `metadata/cluster_review.csv` 中的 `user_confirmed_character_id=role_001` 后，导出样板角色候选：

```powershell
python scripts\export_role_candidates.py --role role_001
```

默认只输出：

```text
metadata/role_001_candidate_export.csv
```

不会复制或移动原始图片。只有明确需要本地候选目录时，才使用：

```powershell
python scripts\export_role_candidates.py --role role_001 --copy-mode hardlink
```

`hardlink` 只创建硬链接，不移动、不删除原始素材。

## P0 输出

本地 P0 输出包括：

- `metadata/source_inventory.csv`
- `metadata/frame_index.csv`
- `metadata/duplicate_candidates.csv`
- `metadata/face_index.csv`
- `metadata/face_clusters.csv`
- `metadata/cluster_review.csv`
- `metadata/master_asset_index.csv`
- `metadata/role_001_candidate_export.csv`
- `metadata/face_embeddings.npz`
- `outputs/p0_extracted_frames/`
- `outputs/cluster_contact_sheets/cluster_*.jpg`

这些都是本地审核产物，不提交到 GitHub。

## 重要文档

- `docs/README.md`：文档分类入口。
- `docs/00_project_overview/current_stage_report.md`：当前阶段总报告。
- `docs/01_p0_asset_pipeline/p0_asset_pipeline_report.md`：P0 管线报告。
- `docs/01_p0_asset_pipeline/asset_triage_pipeline.md`：素材分诊流程。
- `docs/03_model_strategy/model_upgrade_strategy.md`：P0/P1/P2 模型升级路线。
- `docs/99_safety_scope/safety_and_scope_boundary.md`：安全与范围边界。
- `docs/role_001_review_workflow.md`：role_001 聚类审核和候选导出流程。
- `skills/comfyui-character-system-context/SKILL.md`：给 Codex / 网页 ChatGPT 对齐项目状态的上下文 skill。

## 上传规则

不要提交：

- 图片：`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tif`, `.tiff`
- 视频：`.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.m4v`, `.wmv`
- CSV/NPZ：`metadata/*.csv`, `metadata/*.npz`, `characters/**/metadata/*.csv`
- 模型文件：`.safetensors`, `.ckpt`, `.pt`, `.pth`, `.bin`, `.onnx`
- ComfyUI 输出图
- 抽帧结果
- contact sheet
- 本地日志和缓存

仓库只保存可复用的文档、脚本、工作流 JSON、参数说明、skill 和空目录占位。
