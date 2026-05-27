# 模型评估矩阵

当前阶段只建立评估表，不下载大模型，不训练 LoRA。

| model_name | task_type | source_url | input_type | output_type | license | local_run_supported | comfyui_node_available | vram_requirement | test_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | pose / detection / segmentation / depth / caption / image_to_3d / image_editing | TBD | image / video / text / mask | keypoints / bbox / mask / depth / caption / mesh / edited image | TBD | yes / no / unknown | yes / no / unknown | TBD | not_tested | TBD |

## 字段说明

- `model_name`：模型或项目名称。
- `task_type`：任务类型，例如 pose、detection、segmentation、depth、caption、image_to_3d、image_editing。
- `source_url`：Hugging Face、GitHub、论文页或官方项目地址。
- `input_type`：输入类型，例如 image、video、text、mask。
- `output_type`：输出类型，例如 keypoints、bbox、mask、depth、caption、mesh、edited image。
- `license`：模型许可证。
- `local_run_supported`：是否支持本地运行。
- `comfyui_node_available`：是否已有 ComfyUI 节点或可接入工作流。
- `vram_requirement`：显存需求，未知时填 `unknown`。
- `test_status`：`not_tested`、`planned`、`tested_online`、`tested_local`、`blocked`、`rejected`。
- `notes`：记录依赖、限制、风险、下一步动作。

## 当前优先级

P0 不依赖新增大模型：

- 文件索引
- 视频抽帧
- pHash 去重
- 模糊检测
- InsightFace 人脸检测与聚类

P1 待评估：

- DWPose / OpenPose
- GroundingDINO
- SAM2
- Depth Anything V2

P2 后续评估：

- Florence-2 / Qwen-VL
- image-to-3D
- LoRA 训练脚本
- Blender 自动化脚本
