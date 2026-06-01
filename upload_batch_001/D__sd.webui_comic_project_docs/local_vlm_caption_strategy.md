# Local VLM Caption Strategy

This project uses local VLMs for caption and tag drafting only. P0.5 does not ask VLMs to produce masks, pose maps, depth maps, or training labels that require geometric precision.

## Model Roles

- `gemma4:e2b`: quick rough screening and face crop review. Use it for cheap first-pass relevance checks, obvious safety flags, duplicate notes, face crop visibility checks, and whether an image is worth a deeper caption.
- `gemma4:e4b-it-q4_K_M`: current primary `main_caption` model. Use it for structured visual descriptions covering character visibility, face visibility, hair, broad clothing, low-confidence pose prose, framing, scene, lighting, prompt tags, and caption quality notes.
- `qwen3-vl:8b`: not the primary caption model for now. Keep it as a complex-sample second-review model after retry/repair handling is stable, because earlier small-sample testing showed stronger detail when valid but unstable JSON / empty responses.

The current P0.5 role map is:

```text
quick_screen      -> gemma4:e2b
face_crop_review  -> gemma4:e2b
main_caption      -> gemma4:e4b-it-q4_K_M
style_detail      -> gemma4:e4b-it-q4_K_M
qwen3-vl:8b       -> optional second review for complex samples only
```

## Identity vs Style Sources

Use `metadata/p05_face_crops_identity_only.csv` as the identity face crop source.
`styles/safe` images are style references only: they may enter `style_detail`
caption rows, but they must not enter `face_crop_review`, FaceID, IPAdapter
identity reference selection, or identity LoRA preparation.

The caption queue script treats `source_person_id=styles` as style-only by
default. If a style-only image contains a detectable face, that face is still
not an identity asset for this project stage.

Caption results are drafts. They must be manually reviewed before they are used
for FaceID / IPAdapter reference decisions, prompt-block promotion, dataset
selection, or any training decision.

## Main Caption Reliability Rules

Manual review of `gemma4:e4b-it-q4_K_M` batch 001 showed that face and scene
descriptions are broadly usable, while pose and lower-body clothing details are
not reliable enough for direct downstream use.

Current policy:

- Keep `gemma4:e4b-it-q4_K_M` as the main caption model.
- Treat `pose` as approximate, low-confidence descriptive prose.
- Add `pose_confidence` to future main-caption JSON.
- Add `pose_needs_manual_review` to future main-caption JSON.
- Add `clothing_confidence` to future main-caption JSON.
- Add `ambiguous_clothing` to future main-caption JSON.
- Do not hard-classify lower-body clothing, skirt hems, inner layers, or occluded clothing boundaries.
- For complex seated poses, strong perspective, or images where foreground legs dominate the frame, default `pose_confidence` to `low`.
- Do not use VLM `pose` results directly as training labels.
- Do not allow ambiguous clothing descriptions into training captions without human correction.

Downstream division of labor:

- Pose should be handled by DWPose / OpenPose-style preprocessors.
- Clothing boundaries should be handled by segmentation / mask tools or human review.
- VLM captions may continue to support face, scene, broad clothing, and prompt-tag drafting.

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
  "pose_confidence": "low | medium | high",
  "pose_needs_manual_review": true,
  "camera": {
    "framing": "medium close-up",
    "angle": "eye level"
  },
  "clothing_confidence": "low | medium | high",
  "ambiguous_clothing": [
    "lower-body garment boundary unclear"
  ],
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
