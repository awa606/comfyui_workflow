# Ollama Vision Test Results

Image: `D:\sd.webui\train_material\小恩\[紧急企划] 小恩 -【VIP】捆绑-R18(含V)\084.jpg`

## qwen3-vl:4b
Seconds: 12.45

```text
{
  "can_see_image": false,
  "style_summary_zh": "该请求涉及不适宜内容，无法进行图像风格分析",
  "medium": [],
  "composition": [],
  "linework": [],
  "color_lighting": [],
  "texture": [],
  "subject_vs_style": {
    "content_specific": [],
    "style_transferable": []
  },
  "sdxl_positive": [],
  "sdxl_negative": [],
  "flux_positive_controls": [],
  "score_for_style_extraction": 0
}
```

## qwen3-vl:8b
Seconds: 79.35

```text
{
  "can_see_image": true,
  "style_summary_zh": "写实摄影风格，聚焦成人主题的局部特写，细节刻画突出",
  "medium": ["数码摄影"],
  "composition": ["近距离特写镜头", "俯视角度构图"],
  "linework": ["皮肤自然纹理线条", "绳索编织纹理", "红色手写文字笔触"],
  "color_lighting": ["自然肤色为主，红色文字突出，柔和室内光影"],
  "texture": ["皮肤真实质感", "绳索编织材质", "文字手写笔触"],
  "subject_vs_style": {
    "content_specific": ["绳索捆绑的臀部", "红色手写文字'肉便器 ¥1000'", "透明插入物"],
    "style_transferable": ["写实摄影的细节刻画", "成人主题局部特写", "手写文字元素的融入"]
  },
  "sdxl_positive": ["realistic photography", "close-up shot", "adult content", "detailed skin texture", "rope bondage", "red handwritten text", "transparent object"],
  "sdxl_negative": ["cartoon", "anime", "blurry", "low quality", "text in other languages"],
  "flux_positive_controls": ["realistic", "close-up", "detailed", "adult photography", "rope bondage", "red text", "transparent object"],
  "score_for_style_extraction": 0
}
```

## qwen2.5vl:7b
Error: `HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=240)`

## openbmb/minicpm-v4.6
Error: `500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat`

## blaifa/InternVL3_5:8b
Seconds: 20.71

```text
{
  "can_see_image": true,
  "style_summary_zh": "写实风格的医疗场景",
  "medium": ["摄影"],
  "composition": ["特写镜头", "局部聚焦"],
  "linework": ["细腻笔触"],
  "color_lighting": ["柔和自然光"],
  "texture": ["皮肤质感"],
  "subject_vs_style": {
    "content_specific": ["医疗注射场景", "中文文字标记"],
    "style_transferable": ["写实风格", "细节处理"]
  },
  "sdxl_positive": ["Realistic medical scene", "Detailed close-up", "Soft natural lighting"],
  "sdxl_negative": ["Cartoonish", "Blurry", "Low resolution"],
  "flux_positive_controls": ["Realistic details", "Close-up composition", "Natural skin texture"],
  "score_for_style_extraction": 8
}
```

## llama3.2-vision:11b
Seconds: 236.54

```text
{
  "can_see_image": true,
  "style_summary_zh": "这张图的风格是色彩鲜艳、线条清晰、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腻、构图简单、镜头平面、画法传统、线条流畅、色彩饱和、光影柔和、材质细腼
  "medium": ["传统画法"],
  "composition": ["简单的构图"],
  "linework": ["流畅的线条"],
  "color_lighting": ["色彩饱和"],
  "texture": ["细腼的材质"],
  "subject_vs_style": {
    "content_specific": ["这张图的风格是传统画法"],
    "style_transferable": ["可以将这张图的风格应用到其他图像"]
  },
  "sdxl_positive": ["色彩鲜艳", "线条清晰", "光影柔和", "材质细腼", "构图简单", "镜头平面", "画法传统", "线条流畅", "色彩饱和", "光影柔和", "材质细腼", "构图简单", "镜头平面", "画法传统", "线条流畅", "色彩饱和", "光影柔和", "材质细腼", "构图简单", "镜头平面", "画法传统", "线条流畅", "色彩饱和", "光影柔和", "材质细腼", "构图简单", "镜头平面", "画法传统", "线条流畅", "色彩饱和", "光影柔和", "材质细腼", "构图简单", "镜头平面", "画法传统", "线条流畅", "色彩饱和", "光影柔和", "材质细腼", "构图简单", "镜头平面", "画法传统", "线条流畅", "色彩饱和", "光影柔和", "材质细腼", "构图简单", "镜头平面", "画法传统", "线条流畅", "色彩饱和", "光影柔和", "材质细腼", "构图简单", "镜头平面", "画法传统", "线条流畅", "色彩饱和", "光影柔和", "材质细腼", "构图简单", "镜头平
  "sdxl_negative": [],
  "flux_positive_controls": ["色彩鲜艳", "线条清晰", "光影柔和", "材质细腼", "构图简单", "镜头平
}
```

## gemma4:e2b
Seconds: 83.19

```text
{
  "can_see_image": true,
  "style_summary_zh": "一张柔和、细节丰富的特写肖像，强调皮肤的自然质感和亲密的氛围。",
  "medium": [
    "数字绘画",
    "摄影风格"
  ],
  "composition": [
    "特写镜头",
    "中景",
    "主体集中在躯干和双手"
  ],
  "linework": [
    "柔和的轮廓",
    "自然过渡",
    "细节丰富的阴影"
  ],
  "color_lighting": [
    "柔和的漫射光",
    "均匀的照明",
    "中性色调"
  ],
  "texture": [
    "细腻的皮肤纹理",
    "柔软的布料感",
    "高细节的表面质感"
  ],
  "subject_vs_style": {
    "content_specific": [
      "皮肤的自然纹理",
      "双手和绳索的细节",
      "衣物的柔软感"
    ],
    "style_transferable": [
      "写实肖像",
      "柔和的布光",
      "高细节的皮肤渲染",
      "亲密的氛围"
    ]
  },
  "sdxl_positive": [
    "photorealistic",
    "ultra detailed skin texture",
    "soft diffused lighting",
    "intimate portrait",
    "high resolution",
    "detailed hands",
    "soft focus"
  ],
  "sdxl_negative": [
    "poor anatomy",
    "deformed",
    "low quality",
    "blurry",
    "oversaturated",
    "artifacts",
    "cartoon"
  ],
  "flux_positive_controls": [
    "masterpiece",
    "best quality",
    "detailed",
    "photorealistic rendering"
  ],
  "score_for_style_extraction": 9
}
```

## gemma4:e4b-it-q4_K_M
Seconds: 134.52

```text
{
  "can_see_image": true,
  "style_summary_zh": "一张写实的、近距离的身体特写照片，以柔和的自然光捕捉了私密且具有观察性的场景。",
  "medium": [
    "Photography",
    "Photo-realistic"
  ],
  "composition": [
    "Close-up shot",
    "身体特写 (Torso close-up)",
    "自然构图",
    "浅景深 (Shallow depth of field)"
  ],
  "linework": [
    "自然皮肤轮廓",
    "红色笔迹/标记 (Red markings)",
    "物体边缘的清晰描绘"
  ],
  "color_lighting": [
    "柔和的自然光 (Soft natural lighting)",
    "漫射光 (Diffused light)",
    "淡雅的肤色调",
    "低饱和度的背景色"
  ],
  "texture": [
    "光滑的皮肤纹理",
    "塑料的半透明光泽",
    "编织物的粗糙纹理",
    "柔软的床垫/布料质感"
  ],
  "subject_vs_style": {
    "content_specific": [
      "皮肤上的红色文字标记",
      "乳头保护罩/医疗器械",
      "人物的卧姿和手部姿势"
    ],
    "style_transferable": [
      "私密肖像摄影风格 (Intimate portraiture)",
      "高写实主义 (High photorealism)",
      "使用柔光营造的观察性氛围"
    ]
  },
  "sdxl_positive": [
    "photorealistic, close-up portrait, torso, soft natural lighting, intimate, detailed skin texture, red markings, medical device, high resolution, cinematic"
  ],
  "sdxl_negative": [
    "cartoon, drawing, painting, blurry, low resolution, bad anatomy, oversaturated, watermark, abstract"
  ],
  "flux_positive_controls": [
    "photorealistic, close-up, skin texture, red markings, soft lighting, torso"
  ],
  "score_for_style_extraction": 0.9
}
```
