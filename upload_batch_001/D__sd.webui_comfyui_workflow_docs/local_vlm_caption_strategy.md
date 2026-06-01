# Local VLM Caption Strategy

This project uses local VLMs for caption and tag drafting only. P0.5 does not ask VLMs to produce masks, pose maps, depth maps, or training labels that require geometric precision.

## Model Roles

- `gemma4:e2b`: quick rough screening. Use it for cheap first-pass relevance checks, obvious safety flags, duplicate notes, and whether an image is worth a deeper caption.
- `qwen3-vl:8b`: main caption model. Use it for stable visual descriptions: character identity cues, hair, face, clothing, pose, camera framing, lighting, background, and visible props.
- `gemma4:e4b-it-q4_K_M`: detailed style supplement. Use it after the main caption for art/rendering style, material detail, mood, color palette, composition, and prompt-friendly refinements.

The caption queue maps these roles as:

```text
quick_screen      -> gemma4:e2b
main_caption      -> qwen3-vl:8b
style_detail      -> gemma4:e4b-it-q4_K_M
face_crop_review  -> gemma4:e2b
```

## Why VLMs Only Caption / Tag

Captioning is semantic and reviewable: a human can quickly edit text and tags. Mask, pose, and depth outputs are spatial artifacts where small errors can break downstream ControlNet, IPAdapter, or compositing workflows.

Use specialized tools for spatial outputs instead:

- Mask: segmentation tools such as SAM-family nodes or manual masks
- Pose: OpenPose / DWPose-style preprocessors
- Depth: depth preprocessors such as Depth Anything or MiDaS-family nodes
- Face detection: InsightFace or another dedicated detector

VLM text can describe that an image may need a mask, pose, or depth pass, but it should not be treated as the source of those artifacts.

## Caption JSON Schema

Draft captions should be saved or transformed into a reviewable JSON shape like this:

```json
{
  "image_path": "D:/sd.webui/comic_project/training_data/person_a/img_0001.jpg",
  "source_person_id": "person_a",
  "safety": {
    "safe_for_p05": true,
    "needs_manual_review": false,
    "notes": ""
  },
  "identity": {
    "face_visible": true,
    "hair": "long black hair",
    "face_notes": "front-facing, neutral expression",
    "do_not_infer_real_person": true
  },
  "wardrobe": ["white shirt", "dark jacket"],
  "pose": "standing, upper body visible",
  "camera": {
    "framing": "medium close-up",
    "angle": "eye level"
  },
  "style": {
    "medium": "anime illustration",
    "lighting": "soft indoor lighting",
    "color_palette": ["black", "white", "muted blue"]
  },
  "positive_prompt_tags": [
    "consistent character",
    "medium close-up",
    "soft lighting"
  ],
  "negative_prompt_tags": [
    "extra fingers",
    "bad anatomy",
    "low quality"
  ],
  "caption_status": "draft"
}
```

## Using awesome-gpt-image-2

Treat `awesome-gpt-image-2` as a prompt template and phrasing library, not as training data.

Allowed use:

- Study prompt structures and reusable block patterns
- Adapt wording for camera, lighting, composition, and style blocks
- Keep attribution or source notes when a template directly inspires a local prompt pattern

Do not use it as a dataset source, do not copy images into training folders, and do not mix external examples into local identity material.

## ComfyUI Prompt Blocks

After caption review, generate prompt blocks instead of one long freeform prompt:

```json
{
  "identity_block": "same character, long black hair, soft facial features",
  "wardrobe_block": "white shirt, dark jacket",
  "pose_block": "standing, relaxed shoulders, upper body visible",
  "camera_block": "medium close-up, eye-level camera",
  "style_block": "anime illustration, clean linework, soft indoor lighting",
  "negative_block": "extra fingers, bad anatomy, blurry, low quality"
}
```

These blocks can later feed ComfyUI workflow inputs for prompt composition, IPAdapter / FaceID reference selection, and repeatable character-consistency experiments.
