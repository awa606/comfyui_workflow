# 模型升级策略

当前阶段：虚拟角色资产筛选系统建设。本文只定义模型路线和优先级，不执行模型下载、训练或批量生成。

## 总原则

不要盲目使用最大模型。

原因：

- 大模型显存和磁盘占用高，容易把 RTX Laptop 环境拖进排错泥潭。
- 当前瓶颈不是“模型越大越好”，而是素材索引、去重、身份聚类、姿势/服装/分割/深度标签是否可靠。
- 过早接入多个大模型会让失败原因混在一起，难以判断是素材、阈值、模型、工作流还是 prompt 的问题。
- 先用轻量、可解释、可复现的 P0 流程建立 `master_asset_index.csv`，再逐层验证 P1/P2。

## 当前素材声明

当前素材源：

- `D:\sd.webui\train_material`
- `D:\sd.webui\douyin_download`

项目声明：当前处理对象为完全合成数据，包括 3D 软件生成、纯 AI 生成的虚拟角色和漫画素材，不包含真实人物隐私素材。

在此前提下，本项目支持虚拟角色艺术解剖细节一致性训练，用于角色身体完整性、全身艺术渲染细节、服装下身体轮廓、后续 FaceID / LoRA / ComfyUI 漫画化等艺术用途。

推荐安全话术：

- 虚拟角色艺术解剖细节一致性
- 全身艺术渲染细节
- 角色身体完整性训练（艺术用途）
- 服装下身体轮廓训练
- virtual_character_anatomical_consistency
- artistic_full_body_details
- virtual_character_intimate_region_fidelity_artistic
- clothing_underlying_body_contour_training

## P0：立即完成的基础层

P0 不依赖新大模型，不做训练。目标是建立可复查的资产索引。

| 任务 | 模型/方法 | 输出 | 说明 |
| --- | --- | --- | --- |
| 文件索引 | 文件系统扫描 | source path、扩展名、大小、mtime、source_person_id | 建立素材来源链路 |
| 视频抽帧 | OpenCV / PyAV | extracted frame | 默认每秒 1 帧，先限制每视频最大帧数 |
| pHash 去重 | imagehash / OpenCV | duplicate_group_id、代表图 | 去掉重复帧、近似重复图 |
| 人脸检测 | InsightFace | face bbox、det_score、face_quality | 只负责身份层，不识别姿势/服装 |
| 人脸聚类 | InsightFace embedding + 聚类算法 | identity_cluster_id | 按虚拟角色身份聚类 |
| 总索引 | CSV 写出 | `master_asset_index.csv` | 后续 P1/P2 的统一入口 |

### master_asset_index.csv 建议字段

- asset_id
- file_path
- source_root
- source_person_id
- source_type
- frame_index
- timestamp_seconds
- width
- height
- file_hash
- phash
- duplicate_group_id
- is_duplicate
- has_face
- face_count
- face_quality
- face_det_score
- face_embedding_id
- identity_cluster_id
- body_view
- use_for_faceid
- use_for_identity_lora
- use_for_outfit_ref
- use_for_pose_ref
- use_for_anatomical_consistency
- safety_scope
- notes

`notes` 字段使用安全话术，例如 `virtual_character_anatomical_consistency`、`artistic_full_body_details`、`clothing_underlying_body_contour_training`。

## InsightFace 的边界

InsightFace 只负责身份层：

- 检测是否有人脸。
- 评估脸部清晰度和大小。
- 提取虚拟角色身份 embedding。
- 做身份聚类，帮助判断同一个角色是否被混在多个文件夹中。

InsightFace 不负责：

- 姿势识别。
- 服装、鞋、道具检测。
- 人物分割。
- 深度估计。
- caption。
- LoRA 训练。

## P1：待集成的结构理解层

P1 在 P0 索引稳定后逐个接入，每次只验证一个模型类别。

| 任务 | 推荐模型 | 作用 | 输出 |
| --- | --- | --- | --- |
| 姿势识别 | DWPose / OpenPose | 标注骨架、手部、身体朝向 | pose keypoints、pose_type |
| 开放目标检测 | GroundingDINO | 检测服装、鞋、道具等开放词汇目标 | object bbox、label、confidence |
| 分割 | SAM2 | 人物、服装、鞋、道具 mask | segmentation mask |
| 深度估计 | Depth Anything V2 | 生成深度图，辅助构图、3D 和 ControlNet | depth map |

P1 模型负责姿势、分割、深度和局部资产理解，不替代 InsightFace 的身份层。

## P2：后续生产增强层

P2 只在 P0/P1 输出稳定后推进。

| 任务 | 推荐模型/工具 | 作用 |
| --- | --- | --- |
| 自动 caption | Florence-2 / Qwen-VL | 为虚拟角色、服装、姿势、场景生成候选描述 |
| image-to-3D | TripoSR / Hunyuan3D / TRELLIS 类 | 生成角色、服装、道具草模 |
| LoRA 训练脚本 | kohya / sd-scripts / 自定义脚本 | 训练角色身份或模块化资产 LoRA |
| Blender 自动化 | Python bpy | 批量整理草模、渲染参考、导出姿势和构图素材 |

P2 不应跳过 P0/P1。caption、3D 和训练都依赖清晰的素材索引、身份聚类、去重和人工审核。

## 推荐验证顺序

1. P0：跑通文件索引、视频抽帧、pHash 去重、InsightFace 检测、身份聚类。
2. 生成 `master_asset_index.csv`。
3. 人工抽查 50-100 条索引，确认分类和去重质量。
4. P1：先接 DWPose / OpenPose，再接 GroundingDINO，再接 SAM2，最后接 Depth Anything V2。
5. P2：先做 caption 小样本，再做 image-to-3D 小样本，最后再决定 LoRA 训练。

## 禁止事项

- 不盲目下载最大模型。
- 不一次性接入所有 P1/P2 模型。
- 不训练万能模型。
- 不把真实人物私密或露骨素材纳入训练。
- 不上传图片、视频、生成图、模型文件或本地 CSV 到 GitHub。
- 不修改 ComfyUI 核心代码。

