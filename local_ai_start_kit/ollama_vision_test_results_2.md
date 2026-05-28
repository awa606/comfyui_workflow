# Ollama Vision Test Results

Image: `C:\Users\AWA007\Pictures\微信图片\1613896a0fc54329063a4e9f290541b6.jpg`

## qwen3-vl:4b
Seconds: 25.19

```text
{
  "can_see_image": true,
  "style_summary_zh": "柔和自然的写实风格，突出人物柔美气质与细腻光影",
  "medium": ["数码摄影", "写实风格"],
  "composition": ["中景构图", "平视角度", "自然光运用"],
  "linework": ["柔和的轮廓线", "自然流畅的线条"],
  "color_lighting": ["柔和的粉色调", "自然光照明", "低对比度光影"],
  "texture": ["细腻的数码质感", "无明显颗粒感"],
  "subject_vs_style": {
    "content_specific": ["粉色针织开衫", "吊带短上衣", "牛仔短裤", "窗边室内场景", "抖音号水印"],
    "style_transferable": ["柔和粉色调", "自然光照明", "中景构图", "人物自然姿态"]
  },
  "sdxl_positive": ["soft lighting, natural pose, pastel colors, casual outfit, indoor setting, high detail, realistic photography"],
  "sdxl_negative": ["blurry, distorted, low quality, text, watermark"],
  "flux_positive_controls": ["soft lighting, natural pose, pastel colors, casual outfit, indoor setting, high detail, realistic photography"],
  "score_for_style_extraction": 8
}
```

## qwen3-vl:8b
Seconds: 43.65

```text
{
  "can_see_image": true,
  "style_summary_zh": "柔和自然的写实摄影风格，融合日系清新感与细腻质感",
  "medium": ["摄影"],
  "composition": ["中景构图，人物侧身站立于窗边，平视角度突出自然姿态"],
  "linework": ["自然柔和的轮廓线条，无明显笔触，光影过渡细腻"],
  "color_lighting": ["柔和粉色调为主，自然光营造均匀通透的光影层次"],
  "texture": ["细腻的皮肤质感，轻微胶片颗粒感，针织面料纹理清晰"],
  "subject_vs_style": {
    "content_specific": ["抖音号nyu8866，人物撩发姿态，窗边背景中的海报元素"],
    "style_transferable": ["柔和色调搭配自然光，写实构图突出人物姿态，细腻质感与胶片感结合"]
  },
  "sdxl_positive": ["realistic photo, soft natural lighting, pink knitted cardigan, denim shorts, delicate skin texture, window light, natural pose"],
  "sdxl_negative": ["blurry, low quality, cartoon, anime, bad anatomy"],
  "flux_positive_controls": ["realistic, soft lighting, natural pose, window light, delicate skin"],
  "score_for_style_extraction": 0
}
```

## qwen2.5vl:7b
Error: `HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=240)`

## openbmb/minicpm-v4.6
Error: `500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat`

## blaifa/InternVL3_5:8b
Seconds: 21.77

```text
{
  "can_see_image": true,
  "style_summary_zh": "柔和的自然光与时尚穿搭",
  "medium": ["摄影"],
  "composition": ["人像特写", "三分法构图"],
  "linework": ["无明显线条"],
  "color_lighting": ["柔和色调", "自然光"],
  "texture": ["光滑质感", "胶片感"],
  "subject_vs_style": {
    "content_specific": ["模特穿搭", "室内环境"],
    "style_transferable": ["柔和色调", "自然光影"]
  },
  "sdxl_positive": ["Soft natural lighting", "Fashion photography", "Portrait close-up"],
  "sdxl_negative": ["Harsh shadows", "High contrast", "Vivid colors"],
  "flux_positive_controls": ["Soft lighting", "Natural tones", "Smooth texture"],
  "score_for_style_extraction": 8
}
```

## llama3.2-vision:11b
Error: `HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=240)`

## gemma4:e2b
Seconds: 62.37

```text
```json
{
  "can_see_image": true,
  "style_summary_zh": "柔和的自然光下的时尚肖像摄影，强调柔和的色彩和细腻的质感。",
  "medium": [
    "摄影",
    "数字艺术渲染"
  ],
  "composition": [
    "特写肖像",
    "垂直构图",
    "人物占据画面主体"
  ],
  "linework": [
    "柔和的轮廓",
    "细腻的细节",
    "无生硬的线条"
  ],
  "color_lighting": [
    "自然光",
    "柔和的散射光",
    "温暖的色调"
  ],
  "texture": [
    "柔软的针织纹理",
    "光滑的皮肤",
    "柔和的氛围感"
  ],
  "subject_vs_style": {
    "content_specific": [
      "粉色针织衫",
      "长发",
      "窗边光线"
    ],
    "style_transferable": [
      "柔光摄影",
      "时尚肖像",
      "自然光氛围",
      "高细节纹理"
    ]
  },
  "sdxl_positive": [
    "masterpiece",
    "photorealistic",
    "soft focus",
    "cinematic lighting",
    "detailed skin texture",
    "soft fabric texture",
    "natural light",
    "fashion portrait",
    "high quality"
  ],
  "sdxl_negative": [
    "low quality",
    "deformed",
    "ugly",
    "harsh shadows",
    "grainy",
    "oversaturated",
    "poor composition"
  ],
  "flux_positive_controls": [
    "soft lighting",
    "detailed texture",
    "cinematic color grading",
    "fashion photography"
  ],
  "score_for_style_extraction": 9
}
```
```

## gemma4:e4b-it-q4_K_M
Seconds: 125.97

```text
```json
{
  "can_see_image": true,
  "style_summary_zh": "一张以自然光为主要光源，采用柔和色调和生活化场景的女性肖像照，整体风格清新、温柔、文艺。",
  "medium": [
    "摄影",
    "胶片摄影",
    "数码摄影"
  ],
  "composition": [
    "中景肖像",
    "自然构图",
    "景深虚化（Bokeh）",
    "三分法"
  ],
  "linework": [
    "柔和的轮廓线",
    "自然流畅的线条",
    "强调材质的细节描绘"
  ],
  "color_lighting": [
    "柔和的自然光（Soft Daylight）",
    "高光柔和，阴影过渡平滑",
    "低对比度",
    "马卡龙色系/柔和的粉彩调（Pastel Palette）"
  ],
  "texture": [
    "针织面料的纹理",
    "牛仔布的粗粝感",
    "皮肤的细腻感",
    "轻微的胶片颗粒感（Film Grain）"
  ],
  "subject_vs_style": {
    "content_specific": [
      "穿着针织开衫和吊带的休闲穿搭",
      "在窗边拍摄的室内场景"
    ],
    "style_transferable": [
      "使用柔和自然光进行人像拍摄",
      "采用低饱和度的清新色调",
      "营造生活化、慵懒的氛围感"
    ]
  },
  "sdxl_positive": [
    "soft portrait",
    "natural daylight",
    "pastel color palette",
    "knitted cardigan",
    "denim shorts",
    "bokeh background",
    "cinematic lighting",
    "high detail",
    "aesthetic lifestyle photography"
  ],
  "sdxl_negative": [
    "harsh shadows",
    "oversaturated",
    "low quality",
    "ugly",
    "deformed",
    "poorly drawn",
    "too dark"
  ],
  "flux_positive_controls": [
    "soft focus",
    "natural light",
    "pastel aesthetic",
    "candid moment",
    "gentle mood"
  ],
  "score_for_style_extraction": 0.9
}
```
```
