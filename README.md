# ComfyUI Workflow Comic Project

这个仓库用于管理 ComfyUI 角色一致性漫画分镜生成项目。它只保存工作流、说明文档、脚本和目录结构，不保存大模型、生成图片、输入视频或私人参考图。

## 目录结构

| 目录 | 用途 | 是否上传素材 |
|---|---|---|
| `workflows` | ComfyUI `.json` 工作流文件 | 只上传 JSON |
| `scripts` | 项目辅助脚本 | 上传 |
| `docs` | 模型清单、排错记录、使用说明 | 上传 |
| `character_refs` | 角色参考图 | 不上传私人图片 |
| `face_crops` | 人脸裁剪结果 | 不上传生成素材 |
| `body_refs` | 身体、服装、发型参考图 | 不上传私人图片 |
| `video_inputs` | 原始视频 | 不上传视频 |
| `video_frames` | 视频抽帧结果 | 不上传帧图 |
| `pose_refs` | 姿态参考图 | 不上传私人图片 |
| `outputs` | ComfyUI 生成结果 | 不上传生成图 |
| `logs` | 本地运行日志 | 不上传日志 |

## 运行关系

推荐流程：

```text
video_inputs/input.mp4
        |
        | scripts/extract_frames.py
        v
video_frames/frame_0001.png ...
        |
        | 后续人脸裁剪/姿态提取脚本
        v
face_crops / pose_refs
        |
        | workflows/*.json
        v
ComfyUI 角色一致性漫画分镜生成
        |
        v
outputs/
```

## 常用命令

从视频每秒抽 1 帧：

```bat
cd /d D:\sd.webui\comic_project
D:\sd.webui\ComfyUI\venv\Scripts\python.exe scripts\extract_frames.py --input video_inputs\input.mp4 --output video_frames --fps 1
```

生成参考图/结果图对比图：

```bat
cd /d D:\sd.webui\comic_project
D:\sd.webui\ComfyUI\venv\Scripts\python.exe scripts\make_contact_sheet.py --refs character_refs face_crops --generated outputs --output outputs\contact_sheet.png
```

也可以双击根目录的 `run_extract_frames.bat`，它会调用 ComfyUI venv 中的 Python，并在缺少 OpenCV 时尝试自动安装。

## 当前环境

- ComfyUI 地址：`http://127.0.0.1:8188`
- ComfyUI 路径：`D:\sd.webui\ComfyUI`
- A1111 路径：`D:\sd.webui\webui`
- Python 环境：`D:\sd.webui\ComfyUI\venv\Scripts\python.exe`
- GPU：`NVIDIA GeForce RTX 5070 Laptop GPU`
- torch：`2.12.0.dev20260408+cu128`

## 重要文档

- `docs/models_required.md`：当前已有模型与缺失模型清单。
- `docs/troubleshooting_comfyui.md`：ComfyUI 当前启动状态和常见排查。
- `workflows/README.md`：工作流目录约定。

## 上传规则

不要提交这些内容：

- `.safetensors`、`.ckpt`、`.pt`、`.pth`、`.bin` 模型文件
- 原始视频
- 抽帧图片
- 私人角色参考图
- 生成结果图
- 本地日志

仓库只保存可复用的工作流 JSON、脚本和文档。
