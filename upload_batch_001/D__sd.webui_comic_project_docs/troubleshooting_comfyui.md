# ComfyUI 排错记录

## 当前状态

ComfyUI 已成功启动。

| 项目 | 当前值 |
|---|---|
| 地址 | `http://127.0.0.1:8188` |
| 端口 | `8188` |
| GPU | `NVIDIA GeForce RTX 5070 Laptop GPU` |
| torch | `2.12.0.dev20260408+cu128` |
| CUDA | `12.8` |
| ComfyUI 路径 | `D:\sd.webui\ComfyUI` |
| Python | `D:\sd.webui\ComfyUI\venv\Scripts\python.exe` |

日志已经显示：

- GPU 已识别为 `NVIDIA GeForce RTX 5070 Laptop GPU`
- 已添加 A1111 模型路径：
  - `D:\sd.webui\webui\models\Stable-diffusion`
  - `D:\sd.webui\webui\models\Lora`
  - `D:\sd.webui\webui\models\ControlNet`
- ComfyUI-Manager 已启动

## cu130 warning

日志中的 `You need pytorch with cu130 or higher to use optimized CUDA operations` 暂时不是致命问题。

当前 ComfyUI 已经可以用 `cu128` torch 启动并识别 RTX 5070 Laptop GPU。这个 warning 表示某些优化 CUDA 算子不可用，不表示 ComfyUI 不能运行。

## 如何启动

推荐使用：

```bat
cd /d D:\sd.webui\ComfyUI
start_comfyui.bat
```

或：

```bat
cd /d D:\sd.webui\ComfyUI
venv\Scripts\python.exe main.py --listen 127.0.0.1 --port 8188
```

## 端口占用排查

如果启动时提示 `8188` 端口被占用，先查看占用进程：

```powershell
Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort 8188 | Select-Object LocalAddress,LocalPort,OwningProcess,State
```

查看进程详情：

```powershell
Get-Process -Id <OwningProcess>
```

如果确认这是旧的 ComfyUI 进程，可以关闭对应窗口，或执行：

```powershell
Stop-Process -Id <OwningProcess>
```

再重新运行 `start_comfyui.bat`。

## 快速健康检查

检查网页是否可访问：

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8188 -UseBasicParsing
```

检查 torch/GPU：

```bat
D:\sd.webui\ComfyUI\venv\Scripts\python.exe -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```
