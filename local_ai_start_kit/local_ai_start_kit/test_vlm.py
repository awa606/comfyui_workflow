import ollama
from PIL import Image
import base64
import io

def analyze_image(image_path: str, model="qwen2.5vl:7b"):
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    
    # 转base64给Ollama
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    
    prompt = """你是一个专业的AI绘图提示词工程师。
请严格按照以下6步改写公式分析这张风格参考图，并输出结构化结果：

1. 气质词替换
2. 体态整体描述
3. 服装得体化
4. 场景明亮化
5. 镜头商业化
6. 加安全边界

最后给出：
- 推荐正向提示词模板（适合img2img）
- 强力负面提示词
- 安全等级（green/yellow/red）
- 是否适合与“林薇”角色结合

用中文输出，结构清晰。"""

    response = ollama.chat(
        model=model,
        messages=[{
            'role': 'user',
            'content': prompt,
            'images': [img_b64]
        }]
    )
    print(response['message']['content'])

# 使用示例（把路径改成你的一张风格参考图或林薇照片）
analyze_image(r"C:\path\to\your\style_reference.jpg")