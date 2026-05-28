# 本地模型路由建议

## 视觉提取第一梯队

- openbmb/minicpm-v4.6：快速粗筛、低成本、先判断图片内容和大风格。
- qwen3-vl:4b：批量提取主力，适合 8GB 显存。
- qwen3-vl:8b：关键图片复核，质量通常比 4B 稳。
- qwen2.5vl:7b：你的现有基线，可用于和 Qwen3-VL 对比。
- blaifa/InternVL3_5:8b：第三方对照模型，适合抽样比较。
- llama3.2-vision:11b：可能比较吃显存，建议只小批量测试。
- gemma4:e2b / e4b：如果图像输入稳定，可以参与复核；否则当文本总结模型。

## 文本总结/改写

- qwen3:14b：本地风格卡片总编辑。
- qwen3.5:9b：提示词改写、JSON 合并、FLUX/SDXL 版本转换。
- qwen3:8b：快速改写。
- qwen2.5-coder:7b：脚本、自动化、ComfyUI 工作流 JSON 修改。

## 向量检索

- bge-m3：中文/英文风格卡片检索优先。
- nomic-embed-text：英文检索可用。

## 不建议做准确风格提取主力

- MythoMax
- dolphin-llama3
- abliterated 模型

这些可以做创意脑暴，但不适合作为可靠视觉分析或结构化风格提取的主模型。
