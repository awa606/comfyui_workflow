# Caption 模板

## 角色身份 LoRA 基础格式

角色身份 LoRA 的 caption 应该先写固定触发词，再写稳定身份特征，最后补充镜头、服装、姿势或角度。

推荐基础格式：

```text
linwei woman, black-rimmed glasses, long dark brown hair, [body view], [outfit], [view angle]
```

示例：

```text
linwei woman, black-rimmed glasses, long dark brown hair, upper body, pink cardigan, front view
```

## 字段说明

- `linwei woman`：角色触发词，建议每张身份 LoRA 训练图都保留。
- `black-rimmed glasses`：稳定身份特征，保留眼镜设定。
- `long dark brown hair`：稳定身份特征，保留发型基础设定。
- `upper body`、`close-up`、`full body`：描述景别。
- `pink cardigan`、`white blouse`：描述当前服装，但不要让服装描述压过身份。
- `front view`、`three-quarter view`、`side view`：描述角度。

## 身份 LoRA caption 原则

- 每张图都使用同一个角色触发词。
- 稳定身份特征要一致。
- 临时服装、场景和姿势可以写，但不要过度细化。
- 不要把背景、灯光或一次性造型写成角色身份。
- 如果某张图只适合服装或姿势参考，不要放入身份 LoRA 训练集。
