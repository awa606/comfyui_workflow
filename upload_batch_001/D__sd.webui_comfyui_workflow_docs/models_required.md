# 模型清单

检查时间：2026-05-25

本文记录当前本机已经存在的模型，以及 ComfyUI 角色一致性/FaceID/IPAdapter 类工作流通常还缺的模型位置。具体文件名仍以实际 `workflows/*.json` 中引用为准。

## 已检测目录

| 类型 | 目录 | 状态 |
|---|---|---|
| Checkpoint | `D:\sd.webui\webui\models\Stable-diffusion` | 存在 |
| LoRA | `D:\sd.webui\webui\models\Lora` | 存在，但未发现模型文件 |
| ControlNet | `D:\sd.webui\webui\models\ControlNet` | 存在，但未发现模型文件 |
| CLIP Vision | `D:\sd.webui\ComfyUI\models\clip_vision` | 存在，但未发现模型文件 |
| IPAdapter | `D:\sd.webui\ComfyUI\models\ipadapter` | 目录缺失 |
| InsightFace | `D:\sd.webui\ComfyUI\models\insightface` | 目录缺失 |

## 已有模型

### Checkpoint

应放目录：

```text
D:\sd.webui\webui\models\Stable-diffusion
```

当前检测到：

- `ponyDiffusionV6XL.safetensors`
- `v1-5-pruned-emaonly.safetensors`

## 当前缺失或未检测到

| 缺失项 | 应放目录 | 可能用途 | 不安装会导致什么 |
|---|---|---|---|
| LoRA 模型 | `D:\sd.webui\webui\models\Lora` | 角色风格、服装、画风或局部特征微调 | 工作流里的 LoRA 加载节点找不到文件 |
| ControlNet 模型 | `D:\sd.webui\webui\models\ControlNet` | OpenPose、Depth、Canny、Tile 等结构控制 | ControlNet 加载节点找不到模型 |
| CLIP Vision 模型 | `D:\sd.webui\ComfyUI\models\clip_vision` | IPAdapter/图像参考编码 | CLIP Vision Loader 或 IPAdapter 相关节点报错 |
| IPAdapter 模型 | `D:\sd.webui\ComfyUI\models\ipadapter` | 参考图/FaceID 风格和身份保持 | IPAdapter Loader 节点找不到模型 |
| InsightFace 模型 | `D:\sd.webui\ComfyUI\models\insightface` | FaceID 人脸特征提取 | InsightFace/FaceID 相关节点无法加载模型 |

## 备注

- A1111 的 checkpoint、LoRA、ControlNet 路径已经通过 ComfyUI `extra_model_paths.yaml` 映射。
- 当前只确认模型目录和文件是否存在，不下载、不移动、不重命名任何模型。
- 等 `workflows/faceid_test.json` 存在后，应再按工作流精确检查模型文件名是否匹配。
