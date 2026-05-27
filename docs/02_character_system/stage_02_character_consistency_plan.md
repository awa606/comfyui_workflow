# 阶段 2：角色一致性与模型路线验证计划

## 当前阶段定义

阶段 2 的目标不是制作最终漫画成片，也不是立即训练 LoRA，而是建立可重复的角色一致性测试体系。当前重点是确认“林薇”这一角色在不同主模型、FaceID 权重、参考图质量和生成参数下的稳定程度，并把素材、测试图、结论文档放入清晰的资产管理目录。

本阶段的核心产出包括：

- 可复用的角色参考图筛选标准。
- 可对比的模型测试输出目录。
- FaceID 与 checkpoint 的测试记录。
- LoRA 是否必要、何时训练、训练哪一种 LoRA 的判断依据。

## 已完成内容

- ComfyUI 已经能够启动并运行。
- FaceID workflow 已经能够出图。
- 项目目录已经包含基础的 `video_inputs`、`video_frames`、`character_refs`、`face_crops`、`pose_refs`、`outputs`、`workflows`、`scripts` 和 `docs`。
- 已有抽帧和 contact sheet 辅助脚本的早期版本。
- 当前已经明确：本阶段不做最终漫画，不训练 LoRA，先验证路线。

## 当前问题

- 当前 FaceID 出图效果一般，角色身份稳定性不足。
- 尚未确认问题主要来自主模型能力、FaceID 方案、参考图质量，还是参数组合。
- 缺少统一的对比测试图命名规则，后续难以横向比较不同 checkpoint 和 FaceID 权重。
- 缺少可用于 LoRA 训练前评估的素材筛选流程。
- 缺少明确的角色一致性评估标准，例如脸型、五官、眼镜、发型、年龄感、气质是否稳定。

## 待验证假设

### 假设 1：主模型问题

当前 checkpoint 可能不擅长半写实漫画、现代都市女性、眼镜角色或稳定面部身份保持。即使 FaceID 输入正确，主模型也可能在脸型、年龄感、五官比例和发型上漂移。

验证方式：

- 固定参考图和 FaceID 权重，只替换 checkpoint。
- 使用同一 prompt、seed、分辨率、采样器和步数。
- 对比脸型、眼镜、发型、整体年龄感和漫画风格稳定性。

### 假设 2：FaceID 问题

FaceID 权重、节点组合或模型版本可能不足以稳定保留角色身份。权重过低会丢脸，权重过高可能导致僵硬、糊脸或风格不融合。

验证方式：

- 固定 checkpoint 和参考图。
- 按梯度测试 FaceID 权重，例如 `0.4`、`0.6`、`0.8`、`1.0`、`1.2`。
- 记录每档权重下的身份相似度、画面自然度、风格融合程度和失败样式。

### 假设 3：参考图问题

参考图如果角度单一、清晰度不足、妆容/光线变化过大、遮挡严重或与目标漫画形象差异过大，会直接影响 FaceID 和后续 LoRA 数据质量。

验证方式：

- 将参考图分为正脸、三分之二侧脸、轻微侧脸、不同光照、不同表情几组。
- 单图输入和多图输入分别测试。
- 排除模糊、过曝、遮挡眼镜边框或脸部比例异常的图片。

### 假设 4：参数问题

采样器、步数、CFG、分辨率、denoise、FaceID 权重、ControlNet 或 IPAdapter 权重组合可能尚未找到合适区间。

验证方式：

- 固定模型、参考图和 prompt。
- 一次只改变一个参数。
- 优先测试 FaceID 权重、CFG、步数和分辨率。
- 每组保留同一 seed 的结果，避免随机性干扰判断。

## 下一步验证顺序

1. 建立 `model_tests` 测试目录，按 checkpoint 和 FaceID 权重保存输出图。
2. 从 `datasets/linwei_character_raw` 中筛选高质量图片到 `datasets/linwei_character_selected`。
3. 用 `scripts/extract_keyframes.py` 从 `video_inputs` 每秒抽 1 帧，辅助补充候选素材。
4. 固定参考图、prompt、seed 和参数，先横向测试不同 checkpoint。
5. 选出 1 到 2 个候选 checkpoint 后，测试 FaceID 权重梯度。
6. 对最佳 checkpoint + FaceID 组合测试不同参考图组合。
7. 使用 `scripts/make_model_contact_sheet.py` 生成对比图，集中观察角色一致性。
8. 如果 FaceID 仍无法稳定角色身份，再进入角色 LoRA 数据集准备。
9. 使用 `scripts/prepare_lora_dataset.py` 生成规范命名图片和 caption。
10. 角色 LoRA 验证通过后，再考虑服装 LoRA 或风格 LoRA。
