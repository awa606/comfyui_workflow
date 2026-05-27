# 安全边界

当前阶段：虚拟角色资产筛选系统建设。本文定义素材处理、标注、训练候选和 Git 边界。

## 项目素材声明

当前素材源：

- `D:\sd.webui\train_material`
- `D:\sd.webui\douyin_download`

项目声明：本项目当前素材均为合成数据，包括 3D 软件生成、纯 AI 生成的虚拟角色和漫画素材，不涉及真实人物隐私或授权问题。

在该声明成立的前提下，可以推进虚拟角色艺术解剖一致性训练，用于 LoRA、漫画渲染、角色身体完整性和全身艺术细节一致性。

## 绝对禁止

- 不训练真实人物任何私密或露骨内容。
- 不处理未授权真实人物素材。
- 不把真实人物敏感身体内容作为 FaceID、LoRA、caption 或图像编辑训练数据。
- 不上传真实图片、视频、生成图、模型文件、本地 manifest 或日志 CSV 到 GitHub。
- 不修改 ComfyUI 核心代码。

## 允许范围

仅在素材确认为虚拟合成角色时，允许进行：

- 虚拟角色身份一致性筛选。
- 虚拟角色艺术解剖一致性训练。
- 虚拟角色艺术化敏感区域一致性标注。
- 全身艺术渲染细节整理。
- 角色身体完整性训练（艺术用途）。
- 服装下身体轮廓训练。
- 服装、鞋、道具、发型、妆容、姿势、场景参考整理。

这些内容只用于虚拟角色资产化、LoRA、ComfyUI 漫画化和后续 3D/Blender 辅助流程。

## 推荐安全话术

中文：

- 虚拟角色艺术解剖细节一致性
- 虚拟角色艺术解剖一致性训练
- 全身艺术渲染细节
- 角色身体完整性训练（艺术用途）
- 服装下身体轮廓训练
- 虚拟角色全身细节一致性

英文：

- `virtual_character_anatomical_consistency`
- `artistic_full_body_details`
- `virtual_character_intimate_region_fidelity_artistic`
- `virtual_character_body_integrity_training`
- `clothing_underlying_body_contour_training`
- `synthetic_character_full_body_consistency`

## master_asset_index.csv 标注规范

`notes` 字段不要使用粗俗、色情化、真人化或平台高风险表达。使用安全话术标注用途。

推荐示例：

- `virtual_character_anatomical_consistency`
- `artistic_full_body_details`
- `virtual_character_body_integrity_training`
- `clothing_underlying_body_contour_training`
- `synthetic_character_only`
- `manual_review_required`

`safety_scope` 字段建议使用：

- `synthetic_virtual_character`
- `synthetic_manga_character`
- `synthetic_3d_character`
- `unknown_requires_manual_review`
- `real_person_do_not_train`

## 人工复核规则

自动模型只能做候选判断，不能代替人工审核。

必须人工复核：

- 是否确认为虚拟合成角色。
- 是否混入真实人物素材。
- 是否属于 role_001。
- 是否适合 FaceID。
- 是否适合身份 LoRA。
- 是否只适合作为服装、鞋、姿势、场景或身体轮廓参考。
- 是否需要进入 rejected。

## 真实人物素材规则

虽然当前项目声明全部素材为合成数据，但如果未来混入真实人物素材：

- 必须确认授权。
- 不得训练任何私密或露骨内容。
- 不得将真实人物敏感身体内容用于 LoRA、caption、FaceID 或图像编辑。
- 不确定来源时标注 `unknown_requires_manual_review`，并禁止进入训练集。

## Git 边界

可以提交：

- 文档
- 脚本
- 工作流 JSON
- 参数模板
- 空目录 `.gitkeep`

不能提交：

- 图片
- 视频
- 抽帧结果
- 生成图
- `.safetensors`
- `.ckpt`
- `.pt`
- `.pth`
- `.bin`
- 本地 CSV manifest
- 日志 CSV

