# 类游戏角色编辑器参数系统

目标是把 ComfyUI 的生成流程组织成类似游戏角色编辑器的可调参数系统：身份稳定，外观可换，姿势可控，局部可修。

## LoRA 权重

LoRA 权重相当于角色编辑器里的“角色身份强度”或“外观套件强度”。

建议分层使用：

- 身份 LoRA：控制角色像不像林薇。
- 服装 LoRA：控制某套服装是否出现。
- 妆容 LoRA：控制妆感强弱。
- 发型 LoRA：控制发型版本。
- 风格 LoRA：控制漫画线条和上色风格。

调节方式：

- 身份 LoRA 权重过低：角色不像本人。
- 身份 LoRA 权重过高：表情僵硬、脸部过拟合、风格难融合。
- 服装 LoRA 权重过高：衣服固定化，姿势和镜头变难。
- 风格 LoRA 权重过高：可能压过角色身份。

推荐做法是每次只调一个 LoRA 权重，并记录 checkpoint、seed、prompt、权重和输出图。

## prompt 参数

prompt 相当于角色编辑器里的文本滑杆：描述身份、年龄感、服装、姿势、镜头、表情、光线和场景。

建议拆成几类：

- 身份词：`linwei woman`、`black-rimmed glasses`、`long dark brown hair`。
- 服装词：`pink cardigan`、`white blouse`、`black skirt`。
- 镜头词：`close-up`、`upper body`、`full body`、`front view`。
- 表情词：`neutral expression`、`slight smile`。
- 场景词：`office`、`street at night`、`apartment interior`。
- 质量和风格词：根据 checkpoint 习惯单独维护。

prompt 不应该承担所有控制任务。脸部身份、姿势结构和局部修复应交给 LoRA、ControlNet、IPAdapter 和 inpaint 分担。

## ControlNet

ControlNet 相当于角色编辑器里的“骨架、轮廓和构图锁定”。

常见用途：

- OpenPose：控制身体姿势、手臂位置、站姿、坐姿和动作。
- Depth：控制空间层次、身体体块和镜头透视。
- Canny/Lineart：控制轮廓、服装边界或漫画线稿结构。
- Tile：辅助高分辨率细节修复。

使用原则：

- 姿势问题优先用 OpenPose，而不是反复堆 prompt。
- 构图和身体比例问题可以尝试 Depth。
- 想保留参考图轮廓时使用 Canny 或 Lineart。
- ControlNet 权重过高会让图僵硬，过低则控制不住结构。

## IPAdapter

IPAdapter 相当于角色编辑器里的“图片参考槽”。

可以分成不同参考槽：

- 身份参考：人脸或上半身图，用于辅助角色相似度。
- 服装参考：衣服、鞋包、配饰图。
- 发型参考：发型轮廓、刘海、发长。
- 风格参考：漫画质感、线条和色彩参考。

使用原则：

- 身份参考应清晰、脸大、无遮挡。
- 服装参考可以不要求脸清晰，但衣服结构要清楚。
- 多个参考一起用时要注意权重，否则身份、衣服和风格会互相污染。
- IPAdapter 更适合“参考”，不适合替代干净的数据集管理。

## inpaint

inpaint 相当于角色编辑器里的“局部重绘”和“精修工具”。

适合处理：

- 眼镜变形。
- 眼睛不对称。
- 手部错误。
- 发型边缘不稳定。
- 衣领、纽扣、鞋子、包带等局部细节。
- 脸像但表情不对。
- 大图里局部服装穿帮。

使用原则：

- 先生成整体构图，再局部修。
- mask 要覆盖问题区域并留出少量边缘。
- denoise 低时保留原图，高时重绘幅度大。
- 脸部 inpaint 应保持身份 LoRA 或 FaceID 参与，否则容易换脸。

## 推荐参数化生产顺序

1. 用身份 LoRA 锁定林薇是谁。
2. 用 prompt 设置服装、镜头、表情和场景。
3. 用 ControlNet 锁定姿势和构图。
4. 用 IPAdapter 追加服装、发型或风格参考。
5. 用 inpaint 修复脸、眼镜、手、衣服和配饰。
6. 用 contact sheet 对比不同 checkpoint、LoRA 权重和参考组合。

这个系统的目标不是一次生成完美图，而是把角色生产拆成可调、可记录、可复现的参数组合。
