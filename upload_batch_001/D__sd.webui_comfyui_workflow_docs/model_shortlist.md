# 模型候选短名单

本文件先列类别，不固定最终模型。具体模型 URL、license、显存需求和本地运行方式需要通过 `scripts/check_hf_model_card.py` 和人工验证补齐。

## Image-to-3D

待评估类别：

- Pixal3D / Pixel3D 类 image-to-3D。
- TripoSR 类单图快速 3D。
- Hunyuan3D 类高质量 3D 生成。
- TRELLIS 类 3D asset 生成。

优先验证：

- 是否能从 role_001 全身图生成可导入 Blender 的 mesh。
- 是否输出 `.glb`、`.gltf`、`.obj`、`.ply`。
- 是否需要大显存或复杂依赖。

## Depth

待评估类别：

- Depth Anything 类通用深度估计。
- DepthPro 类高质量深度估计。

优先验证：

- 深度图是否保留身体比例。
- 是否适合 ComfyUI Depth ControlNet。

## Pose

待评估类别：

- DWPose 类人体/手/脸关键点。
- OpenPose 类基础姿势控制。

优先验证：

- 全身图是否能稳定提取姿势。
- 手部和腿部关键点是否可用。

## Face Identity

待评估类别：

- IPAdapter FaceID 类身份参考。
- InstantID 类身份保持。

优先验证：

- role_001 在不同服装、姿势下是否保持同一身份。
- 是否已有 ComfyUI 节点。

## Segmentation

待评估类别：

- SAM 类通用分割。
- 可分离人物、头发、衣服、腿部、鞋袜、背景的分割方案。

优先验证：

- 是否能生成可用于 inpaint 的 mask。
- 是否能帮助拆分服装/发型/鞋袜资产。

## Image Editing

待评估类别：

- Qwen-Image-Edit 类指令式图像编辑。
- Z-Image-Edit 类图像编辑。

优先验证：

- 是否能局部修改服装、妆容、背景。
- 是否适合作为 ComfyUI 输出后的二次编辑工具。

## 暂缓评估

- 需要批量下载巨大权重的模型。
- 许可不清晰的模型。
- 输出不能进入 Blender 或 ComfyUI 的模型。
- 只能生成单张漂亮图、无法进入资产化流程的模型。
