# 模型路线

本文件用于角色资产化准备阶段的路线判断。当前不下载模型、不训练模型，只定义后续测试顺序和判断标准。

## 当前优先路线

当前优先路线：

```text
SDXL/Pony + IPAdapter + ControlNet + 角色 LoRA
```

理由：

- SDXL/Pony 的 ComfyUI 工作流成熟，节点、ControlNet、IPAdapter 和 LoRA 生态更容易串起来。
- Pony 路线更贴近漫画角色和二次元/半二次元表达。
- SDXL 路线适合建立较稳定的通用角色生产底座。
- 角色身份 LoRA 可以先解决“林薇是否稳定像同一个人”。
- IPAdapter 可继续承担临时参考图输入。
- ControlNet 可控制姿势、构图和身体比例。
- inpaint 可用于眼镜、眼睛、手部、衣服细节等局部修复。

当前主线的目标不是追求最新模型，而是建立可复现、可记录、可排错的角色生产系统。

## Qwen-Image-Edit 的适用场景

Qwen-Image-Edit 更适合放在“编辑器”位置，而不是第一阶段身份训练底座。

适用场景：

- 已有一张接近可用的图，需要按自然语言进行局部或整体编辑。
- 替换文字、调整画面元素、改变局部外观。
- 对中文指令和复杂语义编辑有需求。
- 后期对单张图进行修补、变体或语义改写。

它适合做编辑增强和对照测试，但第一阶段不把它作为主线训练底座。

## Z-Image-Edit 的适用场景

Z-Image-Edit 更适合放在后续图像编辑和结构保真测试中。

适用场景：

- 对已有角色图进行自然语言编辑。
- 调整局部服装、背景、光线或小范围外观。
- 测试中文指令驱动的编辑效果。
- 作为 SDXL/Pony 工作流外的编辑路线对照。

现阶段可以记录为候选路线，不急于并入第一生产线。

## FLUX 的适用场景

FLUX 适合做高质量生成路线验证。

适用场景：

- 高质量单图生成。
- 更强提示词遵循和视觉质量测试。
- 后续测试 FLUX LoRA 或相关控制方案。
- 与 SDXL/Pony 输出进行风格、质感和角色稳定性对比。

FLUX 的潜力很高，但它不是 SDXL/Pony LoRA 的直接替代品。若进入主线，需要重新验证 LoRA、ControlNet、IPAdapter 或等价控制工具的可用性。

## 为什么现阶段不把 Qwen/Z-Image 作为第一主线

当前第一目标是角色资产化，而不是测试所有新模型。

暂不作为第一主线的原因：

- 第一阶段需要稳定的 LoRA 训练和加载生态。
- 需要成熟的姿势控制、参考图控制和局部修复链路。
- Qwen/Z-Image 更适合编辑和对照测试，未必最适合先建立身份 LoRA 生产线。
- 如果同时切换底模、编辑模型、控制节点和训练路线，排错成本会急剧上升。
- 当前已有 ComfyUI + FaceID workflow 基础，应先在熟悉链路上建立标准化测试。

结论：SDXL/Pony 作为第一主线，Qwen-Image-Edit、Z-Image-Edit 和 FLUX 作为后续对照路线。

## 后续模型测试矩阵

建议按以下维度记录测试：

| 维度 | 测试项 | 记录内容 |
|---|---|---|
| 主模型 | SDXL checkpoint / Pony checkpoint / FLUX / Qwen / Z-Image | 模型名、版本、路径、加载方式 |
| 身份控制 | FaceID / IPAdapter / 角色 LoRA | 权重、参考图、seed、相似度 |
| 姿势控制 | OpenPose / Depth / Lineart / Canny | 控制图来源、权重、是否僵硬 |
| 服装控制 | prompt / outfit refs / IPAdapter / 服装 LoRA | 衣服还原度、是否污染身份 |
| 局部修复 | inpaint / 编辑模型 | mask 范围、denoise、修复前后对比 |
| 输出评价 | 角色一致性 / 画风 / 手部 / 眼镜 / 可编辑性 | 评分、失败原因、可复现参数 |

推荐命名方式：

```text
model_tests/
  sdxl_checkpoint_name/
    faceid_0.6_seed_0001.png
    faceid_0.8_seed_0001.png
  pony_checkpoint_name/
    ipadapter_0.7_seed_0001.png
```

每次只改变一个主要变量，避免测试结果无法解释。
