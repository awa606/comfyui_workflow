# 素材分诊与二次筛选流程

当前阶段：阶段 1，role_001 样板角色资产化准备。本文只说明素材识别、抽帧、分流和人工复核，不涉及训练。

## 素材来源

当前素材根目录：

- `D:\sd.webui\train_material`
- `D:\sd.webui\douyin_download`

约定：

- 根目录下同一个一级文件夹视为同一个素材对象或同一个人。
- 脚本只在本地读取素材，不上传图片、视频或模型文件。
- 真实人物素材必须确认授权后才能进入任何训练用途。

## 分诊目标

素材不直接进入训练集，而是先进入候选层：

- role_001 角色库：用于样板角色的身份、FaceID、LoRA 候选、服装、姿势等分类。
- `asset_library` 通用素材库：用于沉淀暂不绑定 role_001 的服装、身体参考、腿/鞋、发型、妆容、姿势、场景等候选。
- `metadata`：输出 `master_asset_index.csv`，记录每张图片或抽帧的来源、质量评分和候选用途。

## 自动识别内容

`scripts/triage_douyin_assets.py` 当前做轻量本地分诊：

- 扫描图片和视频。
- 视频按 `--sample-fps` 抽样成图片。
- 使用本地 InsightFace `buffalo_l` 做人脸检测。
- 计算脸部大小、检测置信度、清晰度和综合质量分。
- 根据画面和文件名关键词标注服装、发型、妆容、腿/鞋、姿势、场景候选。
- 输出 CSV manifest，默认路径为 `asset_library/metadata/master_asset_index.csv`。
- 可选择只输出清单，也可把候选图片硬链接或复制到角色库和通用素材库。

它不会：

- 下载模型。
- 训练 LoRA。
- 上传真实素材。
- 自动认定图片可以训练。
- 自动处理露骨或未授权素材。

## 推荐试跑

先小批量，只生成 `master_asset_index.csv`，不搬运候选文件：

```powershell
cd D:\sd.webui\comic_project
python scripts\triage_douyin_assets.py `
  --all-default-roots `
  --limit-files 30 `
  --sample-fps 1 `
  --max-frames-per-file 5 `
  --copy-mode manifest-only `
  --library-copy-mode manifest-only
```

确认阈值和分类逻辑后，再对单个人或单个文件夹试跑候选硬链接：

```powershell
python scripts\triage_douyin_assets.py `
  --source-dir D:\sd.webui\douyin_download\小羊绵绵冰 `
  --role-dir characters\role_001 `
  --copy-mode hardlink `
  --library-copy-mode hardlink `
  --sample-fps 1 `
  --max-frames-per-file 8
```

## 分流目录

role_001 候选会进入：

- `characters/role_001/selected_for_faceid`
- `characters/role_001/selected_for_lora`
- `characters/role_001/identity_faces`
- `characters/role_001/upper_body`
- `characters/role_001/full_body`
- `characters/role_001/body_reference`
- `characters/role_001/outfits/outfit_001`
- `characters/role_001/hairstyles`
- `characters/role_001/makeup`
- `characters/role_001/shoes_accessories`
- `characters/role_001/pose_refs`
- `characters/role_001/scene_refs`
- `characters/role_001/rejected`

通用素材会进入：

- `asset_library/identity_faces`
- `asset_library/body_refs`
- `asset_library/outfit_refs`
- `asset_library/hairstyle_refs`
- `asset_library/makeup_refs`
- `asset_library/leg_shoes_refs`
- `asset_library/pose_refs`
- `asset_library/scene_refs`
- `asset_library/rejected`

## 人工复核规则

自动分诊只做第一层过滤。进入训练或 FaceID 前必须人工复核：

- FaceID：只保留清晰正脸或 45 度脸，避免强滤镜、遮挡、过曝、严重压缩。
- 身份 LoRA 候选：必须身份一致，角度和表情有变化，服装和背景不能过度单一。
- 服装参考：可以不露脸，但服装结构要清楚。
- 腿/鞋参考：只作为非露骨服饰与配件参考，不进入身份 LoRA。
- 姿势参考：优先全身或半身，动作轮廓清晰。
- 场景参考：不参与身份训练，只用于后续构图或背景。
- rejected：不清晰、遮挡严重、身份混杂、未授权、敏感或不适合项目方向的素材。

## 阈值调整

关键参数：

- `--faceid-threshold`：FaceID 候选阈值，默认 `0.72`。
- `--lora-threshold`：身份 LoRA 候选阈值，默认 `0.55`。
- `--sample-fps`：视频抽样频率，默认每秒 1 帧。
- `--max-frames-per-file`：每个视频最多抽样帧数，默认 8。

建议先保守：

- 小批量 `--limit-files 30`。
- 先 `manifest-only`。
- 看 `master_asset_index.csv` 后再决定是否硬链接候选文件。

## Git 边界

可以提交：

- 脚本
- 文档
- 空目录 `.gitkeep`

不能提交：

- 真实图片
- 视频
- 抽帧结果
- 生成图
- 本地 CSV manifest，包括 `master_asset_index.csv`
- 日志 CSV
- 模型文件
