# Project Docs Index

Project: `基于 ComfyUI 的可控式虚拟角色换装与多体型生成系统`

Current phase: P0 asset pipeline validation. The project is organizing and reviewing local virtual character assets. It is not in LoRA training, ComfyUI batch generation, final manga production, or full 3D character editor production.

## Recommended Reading Order

1. `00_project_overview/current_stage_report.md`
2. `01_p0_asset_pipeline/p0_asset_pipeline_report.md`
3. `00_project_overview/project_state.md`
4. `01_p0_asset_pipeline/asset_triage_pipeline.md`
5. `role_001_review_workflow.md`
6. `03_model_strategy/model_upgrade_strategy.md`
7. `99_safety_scope/safety_and_scope_boundary.md`
8. `../skills/comfyui-character-system-context/SKILL.md`

## Categories

### `00_project_overview/`

Project status, roadmap, next actions, Git policy, and ComfyUI troubleshooting notes.

### `01_p0_asset_pipeline/`

P0 material standards, triage pipeline notes, role_001 asset standards, dataset requirements, and P0 run report.

### `role_001_review_workflow.md`

Manual review workflow for contact sheets, `cluster_review.csv`, role_001 candidate export, and the gate for FaceID / IPAdapter testing.

### `02_character_system/`

Role asset strategy, game-like character editor route, parameter system, role_001 MVP plan, and character consistency planning.

### `03_model_strategy/`

Model upgrade policy, P0/P1/P2 model route, model test plan, evaluation matrix, shortlist, and required model inventory.

### `04_lora_strategy/`

LoRA boundaries, role/outfit/style LoRA strategy, and future LoRA training decision template.

### `05_hf_3d_research/`

Hugging Face model research notes and image-to-3D pipeline planning.

### `99_safety_scope/`

Safety and scope boundaries for local asset handling, model use, and repository uploads.

## Repository Boundary

The repository can store docs, scripts, workflow JSON files, parameters, skills, and empty directory placeholders.

Do not commit images, videos, generated frames, contact sheets, CSV/NPZ manifests, model weights, local logs, or ComfyUI outputs.
