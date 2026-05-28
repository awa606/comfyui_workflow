# Local AI Start Kit

这个小工具包用于两件事：

1. 扫描你电脑上的 LoRA、Checkpoint、VAE、ControlNet、Upscaler、GGUF 等本地模型文件。
2. 用同一张图片批量测试多个 Ollama 视觉模型，看哪个更适合“风格提取”。

## 1. 扫描 LoRA / Checkpoint 等模型

PowerShell 进入本目录后运行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scan_ai_assets.ps1
```

默认会扫描常见目录：

- 当前用户 Downloads / Documents / Desktop
- C:\AI
- D:\AI
- ComfyUI / stable-diffusion-webui 常见路径
- 你也可以手动传入路径：

```powershell
.\scan_ai_assets.ps1 -Roots "D:\ComfyUI","D:\stable-diffusion-webui","E:\AIModels"
```

输出：

```text
ai_asset_inventory.csv
ai_asset_inventory.md
```

## 2. 测试 Ollama 视觉模型

先安装 Python 依赖：

```powershell
pip install requests pillow
```

然后运行：

```powershell
python .\test_ollama_vision_models.py --image "D:\test.jpg" --models qwen3-vl:4b,qwen3-vl:8b,qwen2.5vl:7b,openbmb/minicpm-v4.6
```

输出：

```text
ollama_vision_test_results.json
ollama_vision_test_results.md
```

## 推荐第一批测试模型

```text
openbmb/minicpm-v4.6
qwen3-vl:4b
qwen3-vl:8b
qwen2.5vl:7b
blaifa/InternVL3_5:8b
llama3.2-vision:11b
gemma4:e2b
gemma4:e4b-it-q4_K_M
```

8GB 显存下，建议先从 4B/轻量模型开始，确认能稳定输出 JSON 后，再测试 8B/11B。
