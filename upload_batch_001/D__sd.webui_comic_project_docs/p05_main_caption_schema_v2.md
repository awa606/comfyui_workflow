# P0.5 Main Caption Schema V2

Generated: 2026-06-01

## Purpose

This document defines the revised `main_caption` prompt and JSON schema after manual review of `gemma4:e4b-it-q4_K_M` batch 001.

Current model policy remains unchanged:

- `gemma4:e4b-it-q4_K_M` stays as the primary `main_caption` model.
- `gemma4:e2b` stays as `quick_screen` / `face_crop_review`.
- `qwen3-vl:8b` is reserved for future complex-sample second review after retry / repair behavior is stable.

The current issue is not just model strength. Manual review showed that face, hair, broad clothing, scene, and lighting are useful, while precise pose and lower-body clothing boundaries are unreliable.

## Core Rules

- Describe only content that is clearly visible.
- Face, hair, scene, lighting, and broad clothing can be described normally.
- Use broad clothing categories when visible.
- Do not hard-classify skirt / shorts / inner layer / underwear / occluded lower-body boundaries.
- If lower-body clothing is partly hidden, cropped, overlapped, or visually ambiguous, put it in `ambiguous_clothing`.
- Do not include `ambiguous_clothing` content in training captions unless a human reviewer corrects it.
- For complex seated poses, strong perspective, or images where legs dominate the foreground, set `pose_confidence` to `low`.
- Treat `pose_general` as approximate prose, not geometry.
- Use `pose_detail_uncertain` for uncertain limb / knee / foot / crossed-leg details.
- Do not use VLM pose output as training labels.
- Downstream pose should be handled by DWPose / OpenPose.
- Clothing boundaries should be handled by segmentation / mask tools or human review.

## Required JSON Schema

The model must return only valid JSON with this shape:

```json
{
  "image_path": "string",
  "source_person_id": "string",
  "character_visibility": "full body | half body | upper body | face close-up | partial | unclear, with short note",
  "face_visibility": "clear | partly visible | obscured | not visible | unclear, with short note",
  "hair": "visible hair color, length, style, or uncertainty",
  "clothing_upper": "upper-body clothing and accessories that are clearly visible",
  "clothing_lower_general": "broad lower-body clothing only, such as dark lower garment / skirt-like garment / shorts-like garment / unclear lower garment",
  "legwear_general": "broad legwear only, such as black stockings / tights / socks / bare legs / unclear",
  "clothing_confidence": "low | medium | high",
  "ambiguous_clothing": [
    "uncertain lower-body garment boundary",
    "possible skirt/shorts ambiguity",
    "occluded inner layer"
  ],
  "do_not_hard_classify_lower_body_detail": true,
  "pose_general": "coarse pose only, such as standing / seated on floor / seated on bed / leaning / upper body turned",
  "pose_detail_uncertain": [
    "exact leg crossing unclear",
    "feet direction uncertain",
    "hands partially occluded"
  ],
  "pose_confidence": "low | medium | high",
  "pose_needs_manual_review": true,
  "framing": "camera framing and crop",
  "scene": "environment, background, props, location cues",
  "lighting": "lighting quality and direction if visible",
  "positive_tags": ["safe broad tag 1", "safe broad tag 2"],
  "negative_tags": ["quality-control tag 1", "quality-control tag 2"],
  "caption_quality": "good | usable | weak | reject, with short reason",
  "needs_manual_review": true
}
```

## Field Guidance

### `pose_general`

Use only coarse, low-risk descriptions:

- `standing facing camera`
- `seated on floor`
- `seated on bed`
- `seated on ledge`
- `leaning near doorway`
- `upper body angled toward camera`

Do not over-specify exact limb geometry unless it is unambiguous.

### `pose_detail_uncertain`

Put uncertain pose details here instead of writing them as facts.

Examples:

- `exact leg crossing unclear`
- `feet direction uncertain due to perspective`
- `hand position partly occluded`
- `foreground legs make lower-body geometry unreliable`

### `pose_confidence`

Use:

- `high`: simple standing or clear pose with visible full body and minimal occlusion.
- `medium`: common seated or leaning pose with minor occlusion.
- `low`: complex seated pose, strong perspective, cropped body, foreground legs, crossed/raised legs, heavy occlusion, or unclear limb geometry.

Default to `low` for:

- seated floor poses with legs toward camera
- bed poses with legs in foreground
- raised or crossed legs
- strong camera perspective
- lower body cropped or partially hidden

### `pose_needs_manual_review`

Set to `true` when:

- `pose_confidence` is `low`
- limb geometry is important
- exact pose might affect asset indexing
- pose is complex, seated, crossed, raised, or foreground-heavy

### `clothing_upper`

Describe clearly visible upper-body clothing:

- shirt
- blazer / jacket
- tie
- visible bag strap
- collar
- sleeves

Avoid identity claims or unsupported style assumptions.

### `clothing_lower_general`

Use broad terms only.

Allowed examples:

- `dark lower garment`
- `black skirt-like lower garment`
- `shorts-like lower garment`
- `lower garment partly occluded`
- `unclear lower garment`

Do not hard-classify:

- exact skirt hem
- shorts vs skirt when ambiguous
- underwear / inner layer
- hidden lower-body garment boundaries

### `legwear_general`

Use broad terms:

- `black stockings`
- `black tights`
- `black socks`
- `dark legwear`
- `unclear legwear`

Do not infer exact garment boundary from partial visibility.

### `clothing_confidence`

Use:

- `high`: upper and lower clothing are clearly visible and not occluded.
- `medium`: broad category is visible, but some boundaries or details are uncertain.
- `low`: lower body is occluded, cropped, hidden by pose, or affected by strong perspective.

### `ambiguous_clothing`

List all uncertain clothing details here.

Examples:

- `skirt vs shorts unclear`
- `lower garment boundary partly hidden`
- `inner layer not safe to classify`
- `stocking/legwear boundary uncertain`
- `foreground leg perspective obscures lower garment`

This field must not be promoted into training captions without human correction.

### `do_not_hard_classify_lower_body_detail`

Always set to `true` for schema v2. This field is a guardrail for downstream code and reviewers.

## Prompt Template

Use this prompt for `gemma4:e4b-it-q4_K_M` schema v2 validation:

```text
You are writing a main_caption record for a local ComfyUI controllable character workflow.

Do not identify any real person.
Do not infer private identity.
Describe only visible content.

Important reliability rules:
- Face, hair, broad clothing, scene, and lighting may be described normally.
- Pose must be coarse and low-risk.
- For complex seated poses, strong perspective, foreground legs, crossed/raised legs, or occlusion, set pose_confidence to "low".
- Do not hard-classify skirt vs shorts, inner layers, underwear, or occluded lower-body garment boundaries.
- Put uncertain lower-body or clothing-boundary details in ambiguous_clothing.
- Do not put ambiguous_clothing into training captions.
- If lower-body clothing or exact limb geometry is uncertain, say it is uncertain.

Return only valid JSON with exactly the schema provided:
{
  "image_path": "{image_path}",
  "source_person_id": "{source_person_id}",
  "character_visibility": "...",
  "face_visibility": "...",
  "hair": "...",
  "clothing_upper": "...",
  "clothing_lower_general": "...",
  "legwear_general": "...",
  "clothing_confidence": "low | medium | high",
  "ambiguous_clothing": [],
  "do_not_hard_classify_lower_body_detail": true,
  "pose_general": "...",
  "pose_detail_uncertain": [],
  "pose_confidence": "low | medium | high",
  "pose_needs_manual_review": true,
  "framing": "...",
  "scene": "...",
  "lighting": "...",
  "positive_tags": [],
  "negative_tags": [],
  "caption_quality": "good | usable | weak | reject, with short reason",
  "needs_manual_review": true
}
```

## Validation Plan

Do not run this automatically.

After user confirmation, validate schema v2 on only 12 to 30 images from the existing reviewed sample set. Do not proceed to 100-image `batch_002` until schema v2 passes manual review.
