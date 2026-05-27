---
name: comfyui-character-system-context
description: Use for the project "基于 ComfyUI 的可控式虚拟角色换装与多体型生成系统" when aligning status, updating docs or scripts, running the P0 asset pipeline, managing role_001 or virtual character assets, and safely committing/pushing to GitHub without uploading media, CSVs, or model files.
---

# ComfyUI Virtual Character System Context

## Project Identity

Project name: 《基于 ComfyUI 的可控式虚拟角色换装与多体型生成系统》

Repository: `awa606/comfyui_workflow`

Local project path: `D:\sd.webui\comic_project`

Core runtime paths:

- `D:\sd.webui\ComfyUI`
- `D:\sd.webui\webui`
- `D:\sd.webui\train_material`
- `D:\sd.webui\douyin_download`

## Current Phase

Treat the project as being in P0 asset pipeline validation unless the user explicitly changes the phase.

Do not assume the project has entered:

- LoRA training
- ComfyUI batch generation
- final manga production
- P1 pose/segmentation/depth model integration
- P2 caption/image-to-3D/Blender automation

## Read These First

When the user asks about project state or next work, read these repo files first:

- `docs/00_project_overview/current_stage_report.md`
- `docs/01_p0_asset_pipeline/p0_asset_pipeline_report.md`
- `docs/00_project_overview/project_state.md`
- `docs/01_p0_asset_pipeline/asset_triage_pipeline.md`
- `docs/03_model_strategy/model_upgrade_strategy.md`
- `docs/99_safety_scope/safety_and_scope_boundary.md`

## P0 Pipeline Outputs

Local generated files are not committed:

- `metadata/source_inventory.csv`
- `metadata/frame_index.csv`
- `metadata/duplicate_candidates.csv`
- `metadata/face_index.csv`
- `metadata/face_clusters.csv`
- `metadata/cluster_review.csv`
- `metadata/master_asset_index.csv`
- `metadata/face_embeddings.npz`
- `outputs/p0_extracted_frames/`
- `outputs/cluster_contact_sheets/cluster_*.jpg`

Latest P0 validation summary:

- media files: 14433
- images: 8298
- videos: 6135
- extracted frames: 5564
- visual assets: 13862
- pHash duplicate assets: 165
- detected faces: 8485
- assets with faces: 8093
- face clusters: 474
- contact sheets: 474

## P0 Commands

Use these commands from `D:\sd.webui\comic_project`:

```powershell
python scripts\scan_sources.py --skip-hash
python scripts\extract_video_frames.py --fps 1 --max-frames-per-video 1 --workers 8 --timeout-seconds 8
python scripts\filter_duplicates.py --workers 8
python scripts\run_face_index.py --det-size 160 --max-dim 480
python scripts\cluster_faces.py --threshold 0.42 --contact-sheet-samples 24
python scripts\build_master_asset_index.py
```

For more complete video sampling later, increase `--max-frames-per-video` or use `0` for uncapped extraction. Do this only when the user explicitly asks, because the source tree has thousands of videos.

## Directory Map

`docs/`: project plans, safety boundaries, reports, model routes.

`scripts/`: P0 pipeline scripts and utility scripts.

`characters/role_001/`: sample character asset tree with raw images/videos, extracted frames, identity faces, upper/full body, outfits, hairstyles, makeup, accessories, pose refs, scene refs, FaceID/LoRA candidate dirs, rejected, captions, metadata.

`asset_library/`: shared virtual character asset library skeleton for identity faces, body refs, outfit refs, hairstyle refs, makeup refs, leg/shoes refs, pose refs, scene refs, rejected, metadata.

`metadata/`: local generated CSV/NPZ outputs. Do not commit generated files here.

`outputs/`: local generated frames/contact sheets/test outputs. Do not commit generated media here.

`models_research/`: model research skeleton for image-to-3D, depth, pose, face identity, segmentation, image editing.

## Safety Boundaries

Never train or download models unless the user explicitly changes phase and asks for it.

Do not delete, move, overwrite, upload, or expose source media.

Do not commit:

- images
- videos
- generated frames
- contact sheets
- CSV/NPZ manifests
- model weights
- logs
- ComfyUI outputs

Allowed commits:

- docs
- scripts
- workflow JSON
- `SKILL.md`
- `.gitkeep`
- safe config/templates

## GitHub Push Rule

The user wants completed repo work committed and pushed to GitHub so web ChatGPT can read it.

Before every commit:

1. Run `git status --short`.
2. Stage only task-related docs/scripts/skills/config placeholders.
3. Check staged names for forbidden extensions: images, videos, CSV, NPZ, model files.
4. Commit with a concise message.
5. Push with `git push origin HEAD`.

Leave unrelated local/untracked files alone.
