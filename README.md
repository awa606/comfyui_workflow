# comic_project 项目说明

这个目录用于整理漫画/视频转参考图的素材、ComfyUI 工作流和输出结果。当前已经有抽帧脚本，后续的人脸裁剪、FaceID 工作流检查和 ComfyUI 生成结果也都放在这里。

## 目录用途

| 目录 | 放什么 |
|---|---|
| `character_refs` | 角色参考图，建议放清晰正脸、半身、全身图。 |
| `face_crops` | 从角色参考图或视频帧里裁出来的人脸图。后续 FaceID/IPAdapter 类工作流会用到。 |
| `body_refs` | 身体、服装、发型、体型等参考图。 |
| `video_inputs` | 原始输入视频，例如 `video_inputs/input.mp4`。 |
| `video_frames` | 从视频中抽出来的帧，例如 `frame_0001.png`、`frame_0002.png`。 |
| `pose_refs` | 姿态参考图，后续可用于 ControlNet OpenPose、DWpose 等。 |
| `workflows` | ComfyUI 工作流 JSON，例如 `workflows/faceid_test.json`。 |
| `outputs` | ComfyUI 或脚本最终输出的图片、视频、测试结果。 |
| `logs` | 运行日志、缺失清单、排错记录。 |

`__pycache__` 是 Python 自动生成的缓存目录，可以忽略。

## 当前文件

| 文件 | 作用 |
|---|---|
| `extract_frames.py` | 从视频中按指定 FPS 抽帧，输出 PNG 到 `video_frames`。 |
| `run_extract_frames.bat` | 双击运行抽帧脚本。会先检查 ComfyUI venv 里的 OpenCV，缺少时自动安装 `opencv-python`。 |
| `README.md` | 本说明文件。 |

## 文件之间的逻辑关系

推荐流程如下：

```text
video_inputs/input.mp4
        |
        | 运行 run_extract_frames.bat
        v
video_frames/frame_0001.png, frame_0002.png, ...
        |
        | 后续运行 prepare_face_refs.py
        v
face_crops/*.png + face_crops/index.csv
        |
        | 放入/检查 workflows/faceid_test.json
        v
ComfyUI 读取模型、节点和参考图
        |
        v
outputs/
```

`extract_frames.py` 只负责视频抽帧，不做人脸检测，不调用 ComfyUI。

`run_extract_frames.bat` 是给双击使用的入口，它调用的是：

```text
D:\sd.webui\ComfyUI\venv\Scripts\python.exe
```

这样可以复用 ComfyUI 的 Python 环境。

## 如何运行抽帧

1. 把视频放到：

```text
D:\sd.webui\comic_project\video_inputs\input.mp4
```

2. 双击：

```text
D:\sd.webui\comic_project\run_extract_frames.bat
```

3. 抽帧结果会生成到：

```text
D:\sd.webui\comic_project\video_frames
```

默认每秒抽 1 帧。输出文件名类似：

```text
frame_0001.png
frame_0002.png
frame_0003.png
```

也可以手动运行：

```bat
D:\sd.webui\ComfyUI\venv\Scripts\python.exe D:\sd.webui\comic_project\extract_frames.py --input video_inputs\input.mp4 --output video_frames --fps 1
```

如果想每秒抽 2 帧：

```bat
D:\sd.webui\ComfyUI\venv\Scripts\python.exe D:\sd.webui\comic_project\extract_frames.py --input video_inputs\input.mp4 --output video_frames --fps 2
```

运行结束后，脚本会打印：

```text
Extracted N frames
```

## 后续运行关系

当前已经完成的是第一步：视频抽帧。

后续建议顺序：

1. 准备角色参考图：把图片放入 `character_refs`。
2. 准备视频：把原视频放入 `video_inputs/input.mp4`。
3. 抽帧：运行 `run_extract_frames.bat`，生成 `video_frames`。
4. 人脸裁剪：运行后续的 `prepare_face_refs.py`，从 `character_refs` 和 `video_frames` 生成 `face_crops`。
5. 工作流检查：把 ComfyUI 工作流放入 `workflows/faceid_test.json`，再检查缺失 custom nodes 和模型。
6. ComfyUI 生成：在 ComfyUI 里加载工作流，使用 `face_crops`、`pose_refs`、模型和节点生成结果。
7. 保存结果：最终图像或视频放入 `outputs`，运行记录放入 `logs`。

## 目前还缺什么

当前缺少这些内容：

| 缺少项 | 应放位置 | 影响 |
|---|---|---|
| 输入视频 `input.mp4` | `video_inputs/input.mp4` | 双击 `run_extract_frames.bat` 会提示找不到输入视频。 |
| OpenCV Python 包 | ComfyUI venv | 当前检测到还没有 `cv2`；双击 bat 时会自动安装 `opencv-python`。 |
| 角色参考图 | `character_refs` | 后续无法裁剪稳定的人脸参考。 |
| 人脸裁剪脚本 `prepare_face_refs.py` | 项目根目录 | 目前还不能自动从参考图/视频帧裁出 `face_crops`。 |
| FaceID 工作流 `faceid_test.json` | `workflows/faceid_test.json` | 还不能检查工作流缺哪些节点和模型。 |
| LoRA 模型 | `D:\sd.webui\webui\models\Lora` 或 ComfyUI 对应模型目录 | 如果工作流引用 LoRA，而目录为空，加载 LoRA 节点会报错。 |
| ControlNet 模型 | `D:\sd.webui\webui\models\ControlNet` 或 ComfyUI 对应模型目录 | 如果工作流引用 ControlNet，而目录为空，ControlNet 加载节点会报错。 |
| FaceID/IPAdapter 相关模型 | 通常在 ComfyUI 的 `models` 子目录中，具体等 workflow 确认 | FaceID、IPAdapter、CLIP Vision、InsightFace 类节点可能加载失败。 |
| FaceID/IPAdapter custom nodes | `D:\sd.webui\ComfyUI\custom_nodes` | 目前只确认安装了 ComfyUI-Manager；具体缺哪些节点要等 `faceid_test.json` 存在后检查。 |

## 注意事项

- 不要把生成结果、抽帧结果和原始视频混在一起，按目录放会更容易排错。
- 不要手动改 `video_frames` 的命名规则，后续脚本会按 `frame_0001.png` 这种格式处理。
- 不要删除 A1111 或 ComfyUI 的模型文件。这个项目目录只负责引用和整理素材，不直接管理模型。
- 如果 `run_extract_frames.bat` 自动安装 OpenCV 失败，可以手动运行：

```bat
D:\sd.webui\ComfyUI\venv\Scripts\python.exe -m pip install opencv-python --no-cache-dir --timeout 1000 --retries 20 --progress-bar off
```
