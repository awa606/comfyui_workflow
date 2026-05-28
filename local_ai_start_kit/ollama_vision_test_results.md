# Ollama Vision Test Results

Image: `D:\sd.webui\train_material\小恩\[紧急企划] 小恩 -【VIP】捆绑-R18(含V)\084.jpg`

## qwen3-vl:4b
Seconds: 36.03

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
Seconds: 92.91

```text
{
  "can_see_image": true,
  "style_summary_zh": "写实主义成人摄影，聚焦臀部特写与束缚元素",
  "medium": ["摄影"],
  "composition": ["特写镜头，主体聚焦臀部区域，背景虚化"],
  "linework": ["自然皮肤纹理，无明显线条笔触"],
  "color_lighting": ["自然肤色为主，红色文字点缀，柔和室内光"],
  "texture": ["皮肤细腻质感，轻微数字噪点"],
  "subject_vs_style": {
    "content_specific": ["绳索束缚的双手、红色手写文字‘肉便器 ¥1000’、透明插入物"],
    "style_transferable": ["成人摄影中的特写构图、文字标注、束缚元素"]
  },
  "sdxl_positive": ["realistic photo, close-up shot, human anatomy, rope bondage, red handwritten text, transparent object, soft lighting"],
  "sdxl_negative": ["no nudity, no sexual content, no violence, no explicit acts"],
  "flux_positive_controls": ["realistic photography, close-up, human anatomy, rope bondage, red text, transparent object, soft lighting"],
  "score_for_style_extraction": 0
}
```

## qwen2.5vl:7b
Error: `HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=240)`

## openbmb/minicpm-v4.6
Error: `500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat`
