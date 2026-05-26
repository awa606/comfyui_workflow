# 项目进度对齐

最后对齐日期：2026-05-26

## 当前阶段

当前项目处于 **阶段 1：role_001 样板角色资产化准备阶段**。

当前不是：

- LoRA 训练阶段
- 最终漫画生产阶段
- 多角色批量阶段
- 完整 3D 角色编辑器阶段

短期目标是先完成一个最小样板角色：

role_001 素材目录 -> 图片/视频导入 -> 视频抽帧 -> 人工筛选 -> manifest.csv -> FaceID / IPAdapter 测试 -> 判断是否需要角色身份 LoRA。

## 已完成

- A1111 可运行，并可作为快速测试台和参数验证台。
- ComfyUI 可运行。
- ComfyUI 能识别 RTX 5070 Laptop GPU。
- ComfyUI 能读取 A1111 的 checkpoint、LoRA、VAE、embedding、ControlNet 路径。
- ComfyUI-Manager 已安装。
- FaceID / IPAdapter 类工作流已初步测试，但角色相似度仍不稳定。
- GitHub 仓库 `awa606/comfyui_workflow` 已存在。
- 本仓库已建立 role_001 目录框架、素材标准文档、抽帧脚本和 manifest 脚本框架。
- 本仓库已建立 `asset_library` 通用素材库框架，用于沉淀服装、身体参考、腿/鞋、发型、妆容、姿势、场景等非角色身份候选素材。

## 当前未完成

- role_001 原始图片和视频导入。
- 视频抽帧结果。
- 人工素材分类。
- `characters/role_001/metadata/manifest.csv`。
- role_001 素材审核报告的真实统计版。
- FaceID 测试批次。
- 6 张角色标准图。
- LoRA 训练决策。
- Blender / 3D 基底验证。

## 正在验证

- FaceID / IPAdapter 是否足够保持角色一致性。
- 当前 checkpoint 是否适合 role_001。
- 视频抽帧是否能提供足够角色素材。
- 是否需要训练角色身份 LoRA。
- 后续是否需要引入 3D 角色基底。

## 关键决策

- 先只做 role_001，不同时推进多个角色。
- 当前不训练 LoRA。
- 当前不进入最终漫画生产。
- 当前不做完整 3D 角色建模。
- 不训练万能模型。
- 只做角色资产化 MVP。
- 不上传真实素材、生成图、模型文件到 GitHub。

## 下一步顺序

1. 用户把图片放入 `characters/role_001/raw_images`。
2. 用户把视频放入 `characters/role_001/raw_videos`。
3. 运行 `python scripts/extract_keyframes_role.py --role role_001 --fps 1`。
4. 用户人工筛选到 `identity_faces`、`upper_body`、`full_body`、`outfits`、`pose_refs`、`rejected` 等目录。
5. 运行 `python scripts/build_role_manifest.py --role role_001`。
6. 根据 manifest 更新 `docs/role_001_material_review.md`。
7. 素材达标后再进入 FaceID / IPAdapter 测试批次。

如果素材仍集中在 `D:\sd.webui\train_material` 和 `D:\sd.webui\douyin_download`，优先使用 `scripts/triage_douyin_assets.py` 做本地分诊：

1. 小批量扫描两个默认素材根目录。
2. 视频抽样帧。
3. 本地人脸检测与质量评分。
4. 生成 triage manifest。
5. 用户人工复核后，再把候选素材固定到 role_001 或通用素材库。

## 仓库边界

可以提交：

- 文档
- 脚本
- workflow JSON
- 参数记录
- 空目录 `.gitkeep`

不能提交：

- 真实图片
- 视频
- 生成图
- `.safetensors`
- `.ckpt`
- `.pt`
- `.pth`
- `.bin`
- 本地生成的 manifest CSV 和日志 CSV
