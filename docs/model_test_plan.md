# 模型测试计划

当前状态：计划模板。当前阶段不下载大模型，不训练模型，不批量测试。

## 目标

验证 role_001 是否能通过现有 checkpoint + FaceID / IPAdapter + ControlNet 保持稳定角色一致性。

## 优先路线

第一轮只测试最小组合：

- SDXL 或 Pony 类 checkpoint
- IPAdapter / FaceID
- ControlNet 姿势约束
- 固定 prompt 模板
- 固定种子或小范围种子

## 暂不作为主线

- 批量下载大量 checkpoint。
- 直接训练 LoRA。
- 完整 Blender / 3D 角色建模。
- 直接进入漫画分镜生产。
- 把 Qwen / Z-Image / FLUX 作为第一生产主线。

## 测试输入

等素材就绪后，先选择：

- 3 张 FaceID 候选脸图。
- 1 张半身参考。
- 1 张全身参考。
- 1 张姿势参考。

## 标准图目标

第一轮 FaceID 测试只生成 6 张角色标准图：

- 正面半身
- 正面全身
- 45 度半身
- 侧面
- 平静表情
- 紧张表情

## 测试记录字段

后续日志可记录到本地 `logs/role_001_faceid_test_log.csv`，该 CSV 不提交到 GitHub。

字段建议：

- batch_id
- checkpoint
- vae
- sampler
- steps
- cfg
- seed
- faceid_weight
- ipadapter_weight
- controlnet_type
- controlnet_weight
- prompt_version
- reference_images
- output_dir
- face_similarity_score
- identity_stability_score
- style_score
- notes

## 通过标准

FaceID / IPAdapter 暂时够用：

- 6 张标准图中至少 4 张能被肉眼识别为同一角色。
- 正脸和 45 度脸相似度可接受。
- 发型、眼镜、整体气质不频繁漂移。

需要准备角色身份 LoRA：

- 6 张标准图中多数脸型、五官或气质明显漂移。
- 换姿势或换服装后身份明显丢失。
- 调整 FaceID 权重后仍无法稳定。

