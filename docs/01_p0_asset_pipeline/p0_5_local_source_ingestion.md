# P0.5 Local Source Ingestion

P0.5 adds a safety-first intake layer for local reference material. The goal is to turn messy folders into an auditable metadata index before any FaceID / IPAdapter prep, captioning, or later training-set decisions.

This phase does not train LoRA, does not download large models, does not upload source media, and does not delete, move, copy, or overwrite original assets.

## New Local Sources

The current local source roots are:

- `D:\sd.webui\comic_project\training_data`
- `D:\sd.webui\code\local_ai_style_extractor_v2\reference_images`

`training_data` is treated as mixed local character/reference material. The folder may contain image and video assets, nested people/style labels, and unsafe or unrelated subtrees.

`local_ai_style_extractor_v2\reference_images` is treated as a local reference-image source for style and caption experiments. Its generated results stay local and are not committed.

## Default Skips

The P0.5 tools skip or exclude paths that match these keywords by default:

- `explicit`
- `R18`
- `r18`
- `03_explicit`
- `03_explicit_action`
- `03_explicit`
- `05_style_ryota`
- `styles\explicit`
- `VIP`
- `全裸`
- `插入`
- `扩张`
- `ahegao`
- `捆绑`

Directories matching these keywords are pruned during inventory scanning, so their contents do not enter the safe queue. Files outside pruned directories that still match an exclude keyword are marked `excluded=yes` and stay out of crop/caption steps.

## Safe Index Scope

The safe inventory can include:

- Non-excluded image files: `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tif`, `.tiff`
- Non-excluded video files: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.m4v`, `.wmv`
- Path-derived tags from parent folders
- A best-effort `source_person_id` inferred from the first useful folder below the source root

Videos are listed for audit only in P0.5. They are not frame-extracted by the ingestion script.

## Why Explicit / R18 Is Not Processed Now

Explicit and R18 folders are excluded now to prevent unsafe material from entering identity, FaceID, caption, or future training flows by accident. This also keeps the early project index reviewable: safe material can be counted, grouped, and checked without mixing in content that needs a separate policy, consent, and handling decision.

No explicit/R18 folder should be used as a source for face crops, body crops, caption queues, IPAdapter references, or LoRA preparation in P0.5.

## Why P0.5 Does Not Train

Training before the data is indexed would make the dataset hard to audit. P0.5 only prepares local review artifacts:

- Face crop candidates for FaceID / IPAdapter identity reference review
- Body crop candidates later, after safe image review and pose/body requirements are clearer
- Caption draft queues for local VLM tagging
- Inventory CSVs that show which source paths were included or excluded

Identity LoRA training remains disabled in this phase. The face crop CSV includes `use_for_identity_lora=no` by default so later training decisions remain explicit and reviewable.

## Commands

Run commands from the repository root:

```bat
cd /d D:\sd.webui\comfyui_workflow
```

Build the local inventory:

```bat
D:\sd.webui\ComfyUI\venv\Scripts\python.exe scripts\ingest_local_sources_p05.py ^
  --source-root D:\sd.webui\comic_project\training_data ^
  --source-root D:\sd.webui\code\local_ai_style_extractor_v2\reference_images
```

The default output is:

```text
metadata/p05_local_source_inventory.csv
```

Export safe face crops after confirming InsightFace model files already exist locally:

```bat
D:\sd.webui\ComfyUI\venv\Scripts\python.exe scripts\export_face_crops_p05.py ^
  --index metadata/p05_local_source_inventory.csv ^
  --crop-size 768
```

The script checks for local InsightFace files under `INSIGHTFACE_HOME`, `INSIGHTFACE_ROOT`, or `C:\Users\<user>\.insightface`. It does not download models.

On Windows, `onnxruntime-gpu` may need PyTorch's bundled CUDA/cuDNN DLLs to be loaded before InsightFace initializes. The face crop script preloads `torch` when `CUDAExecutionProvider` is requested so CUDA DLLs such as `cublasLt64_12.dll` are visible to ONNX Runtime.

If a non-identity bucket such as `styles` produces face crops, treat those crops as review artifacts only. A face crop means "a face detector found a face in a safe image"; it does not mean the image should be used for FaceID, IPAdapter identity reference, or identity LoRA.

Prepare the caption queue:

```bat
D:\sd.webui\ComfyUI\venv\Scripts\python.exe scripts\prepare_safe_caption_queue_p05.py ^
  --inventory metadata/p05_local_source_inventory.csv ^
  --face-crops metadata/p05_face_crops.csv ^
  --caption-passes quick main style
```

Generated P0.5 CSVs and processed crops are local outputs and are ignored by Git.
