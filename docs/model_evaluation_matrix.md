# 模型评估矩阵

每个 Hugging Face 候选模型都按同一字段记录，避免只凭样例图判断。

| model_name | source_url | task_type | input_type | output_type | license | local_run_supported | comfyui_node_available | blender_compatible | vram_requirement | test_input | test_output | score | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TBD | TBD | image_to_3d / depth / pose / face_identity / segmentation / image_editing | image / video / text / mask | mesh / depth map / pose map / identity embedding / mask / edited image | TBD | yes/no/unknown | yes/no/unknown | yes/no/unknown | TBD | role_001 test image path | local output path or Space result note | 0-5 | TBD |

## 字段说明

- `model_name`：模型或项目名称。
- `source_url`：Hugging Face 模型页、Space 或官方仓库链接。
- `task_type`：模型任务类型。
- `input_type`：输入格式，例如单图、视频、多图、prompt、mask。
- `output_type`：输出格式，例如 mesh、depth map、pose map、mask、编辑图。
- `license`：模型卡声明的 license。
- `local_run_supported`：是否支持本地运行。
- `comfyui_node_available`：是否已有 ComfyUI 节点或可接入工作流。
- `blender_compatible`：输出是否能进入 Blender 或经过简单转换后进入 Blender。
- `vram_requirement`：显存需求，未知时填 `unknown`。
- `test_input`：测试输入，优先使用 role_001 的 3 张标准图。
- `test_output`：测试输出路径或在线 Space 测试记录。
- `score`：0 到 5 分，先粗评可用性。
- `notes`：依赖、风险、失败原因、后续动作。

## 评分建议

- 5：效果好，许可清楚，能本地或可复现运行，能进入 Blender/ComfyUI。
- 4：效果可用，但依赖或流程需要整理。
- 3：有参考价值，但不能直接进入主线。
- 2：只能作为对照或局部参考。
- 1：效果差或流程不稳定。
- 0：无法使用、许可不合适或无法验证。
