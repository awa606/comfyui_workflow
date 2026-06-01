# 下一步动作

## 1. 选择 role_001 的 3 张测试图

从本地候选素材中人工选择：

- 1 张正面全身图。
- 1 张三分之二角度图。
- 1 张上半身或脸部较清晰图。

这些图片只放在本地，不上传到仓库。

## 2. 每类模型只选 1 个做验证

第一轮每类只选一个：

- image-to-3D：1 个。
- depth：1 个。
- pose：1 个。
- face identity：1 个。
- segmentation：1 个。
- image editing：1 个。

目标是验证流程，不是追求一次性找全所有最佳模型。

## 3. 不要批量下载所有模型

暂时不要批量下载 Hugging Face 权重。先看模型卡、license、Space demo、依赖和输出格式。

避免：

- 下载多个大模型占满磁盘。
- 模型许可不清楚就进入生产。
- 同时测试太多变量，导致无法判断问题来源。

## 4. 先测试在线 Space 或小模型

优先策略：

- 先用在线 Space 看输出是否值得继续。
- 如果模型很小，再考虑本地脚本验证。
- 如果模型很大，先记录显存、依赖和替代方案。
- 每次测试都填入 `docs/03_model_strategy/model_evaluation_matrix.md` 中的字段。

## 5. 暂定验证顺序

1. role_001 三张测试图人工确认。
2. image-to-3D 单模型在线测试。
3. Blender 导入 mesh 检查。
4. depth 和 pose 输出测试。
5. segmentation mask 测试。
6. face identity 和 image editing 作为 ComfyUI 生产线对照。
