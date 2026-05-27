# 安全与范围边界

当前项目聚焦虚拟角色的非露骨角色资产系统。当前不进入训练阶段，不下载大模型。

## 项目范围

支持整理和筛选：

- 脸
- 发型
- 服装
- 妆容
- 体态
- 姿势
- 场景
- 漫画风格

目标是建立可复查的虚拟角色资产库，为后续 FaceID、IPAdapter、LoRA 决策、ComfyUI 漫画化和 3D 调研提供干净素材。

## 当前不做

- 不建立真实人物隐私数据集。
- 不训练私密部位模型。
- 不训练 LoRA。
- 不下载大模型。
- 不做最终漫画生产。
- 不做完整 3D 角色建模。

## 真实人物边界

本项目不把真实人物隐私素材纳入训练或数据集建设。

如果未来混入真实人物素材：

- 必须确认授权。
- 不得作为私密、露骨或敏感内容训练数据。
- 不确定来源时标注为 `unknown_requires_manual_review`。
- 未确认授权前不得进入训练候选。

## 虚拟角色边界

虚拟角色素材可以用于非露骨角色资产管理：

- 身份一致性。
- 发型一致性。
- 服装与配饰参考。
- 体态和姿势参考。
- 场景与构图参考。
- 漫画风格参考。

所有自动标注只作为候选，最终是否进入 FaceID、LoRA 候选或参考素材，需要人工复核。

## GitHub 边界

可以上传：

- 文档
- 脚本
- 配置模板
- 空目录 `.gitkeep`
- 工作流 JSON

不要上传：

- 图片
- 视频
- 抽帧结果
- 生成图
- 模型文件
- `.safetensors`
- `.ckpt`
- `.pt`
- `.pth`
- `.bin`
- 本地生成的 CSV manifest
- 日志 CSV

## master_asset_index.csv 标注边界

`master_asset_index.csv` 是本地生成物，不提交到 GitHub。

建议字段：

- `face_cluster_id`
- `face_quality_score`
- `body_view`
- `pose_type`
- `outfit_type`
- `hairstyle`
- `makeup`
- `shoes_visible`
- `hands_visible`
- `feet_visible`
- `scene_type`
- `object_tags`
- `depth_available`
- `mask_available`
- `use_for_faceid`
- `use_for_lora`
- `use_for_outfit_ref`
- `use_for_pose_ref`
- `reject_reason`

`notes` 和 `reject_reason` 字段应使用中性工程话术，例如：

- `low_face_quality`
- `blurred_frame`
- `duplicate_frame`
- `wrong_identity_cluster`
- `not_role_001`
- `manual_review_required`
- `unknown_requires_manual_review`

