# 数据集素材要求

## FaceID 最低素材要求

FaceID 可以从少量高质量人脸图开始测试，但素材质量比数量更重要。

最低要求：

- 1 到 3 张清晰正脸或轻微侧脸图片。
- 脸部无遮挡，眼镜边框完整可见。
- 分辨率足够，人脸区域不要太小。
- 光线均匀，不要严重过曝、欠曝或彩色灯污染。
- 表情自然，避免夸张张嘴、挤眼或大角度仰拍俯拍。

更推荐：

- 5 到 10 张高质量脸部图。
- 包含正脸、三分之二侧脸、轻微侧脸。
- 包含 2 到 3 种自然表情。
- 发型、眼镜、妆容尽量接近目标角色设定。

## 角色 LoRA 最低素材要求

角色 LoRA 的最低素材数量建议高于 FaceID，因为 LoRA 需要学习稳定身份，而不是只做单次相似度迁移。

最低要求：

- 15 到 20 张筛选后的高质量图片。
- 至少包含正脸、三分之二侧脸、轻微侧脸。
- 至少包含近景头像、胸像、半身。
- 眼镜、发型、年龄感和脸型特征稳定。
- 避免大量重复角度或同一视频连续帧。

不建议低于 10 张就开始正式训练。素材太少时，LoRA 容易记住具体照片，而不是学到角色身份。

## 推荐素材数量

推荐角色 LoRA 素材规模：

- 快速验证版：20 到 30 张。
- 稳定实验版：40 到 80 张。
- 较完整生产版：80 到 150 张。

数量增加不一定更好。比数量更重要的是角度、表情、景别和光线的均衡，以及是否去掉了低质量图片。

## 视频抽帧要求

视频可以作为候选素材来源，但不能把所有抽帧直接用于训练。

抽帧建议：

- 使用 `scripts/extract_keyframes.py` 默认每秒 1 帧。
- 如果视频变化很快，可以使用 `--fps 2`。
- 如果视频变化很慢，可以使用 `--fps 0.5`。
- 抽帧后先放入 `video_frames`，再人工筛选到 `datasets/linwei_character_raw` 或 `datasets/linwei_character_selected`。

筛选注意：

- 不要保留连续几乎相同的帧。
- 不要保留运动模糊帧。
- 不要保留脸被手、头发、强阴影或字幕遮挡的帧。
- 不要保留压缩噪点严重的帧。
- 不要保留明显不像目标角色设定的造型。

## 图片筛选标准

进入 `datasets/linwei_character_selected` 的图片应满足：

- 脸部清晰，五官可辨认。
- 黑框眼镜完整，镜片反光不过度遮挡眼睛。
- 长深棕色头发特征清楚。
- 脸型、年龄感和气质接近目标角色。
- 构图不极端，不是超大头裁切或过远全身。
- 无明显水印、字幕、贴纸或 UI 元素遮挡。
- 色彩正常，没有强滤镜或异常白平衡。
- 不与其他人物脸部重叠。
- 不包含不希望模型学习的临时服装、夸张表情或特殊妆容。

建议删除或隔离：

- 模糊图。
- 严重压缩图。
- 过曝或欠曝图。
- 多人合照且主角不明确的图。
- 角度极端的仰拍、俯拍、大侧脸和背影。
- 与目标角色设定冲突的发色、眼镜、年龄感或脸型。

## caption 规范

角色 LoRA 的 caption 应保持稳定、简洁、可控。默认触发词建议为：

```text
linwei woman
```

当前默认 caption：

```text
linwei woman, black-rimmed glasses, long dark brown hair
```

规范建议：

- 每张图都保留统一触发词 `linwei woman`。
- 稳定角色特征可以写入 caption，例如 `black-rimmed glasses`、`long dark brown hair`。
- 不要把每张图都有但不想强绑定的背景写得太重。
- 临时服装、场景、表情可以按需补充，但不要喧宾夺主。
- 如果某张图有明显角度或景别，可以补充 `front view`、`three-quarter view`、`upper body`、`close-up`。
- 如果后续要训练服装 LoRA，角色 LoRA 的 caption 中不要过度强调固定服装。

示例：

```text
linwei woman, black-rimmed glasses, long dark brown hair, close-up, neutral expression
linwei woman, black-rimmed glasses, long dark brown hair, three-quarter view, upper body
linwei woman, black-rimmed glasses, long dark brown hair, slight smile
```
