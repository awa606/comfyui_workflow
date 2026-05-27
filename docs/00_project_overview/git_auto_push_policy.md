# Git 自动提交推送策略

本项目已启用本地 Codex skill：`git-safe-push-after-run`。

目标：每次完成一次项目运行或文件改动后，进行安全检查、提交，并推送到 GitHub 仓库。

## 执行规则

每次完成工作后执行：

1. 查看 `git status --short`。
2. 只暂存本次任务相关的源码、脚本、文档、配置和 `.gitkeep`。
3. 不暂存真实素材、生成图片、视频、模型文件、manifest CSV 或日志。
4. 运行必要的轻量校验，例如 Python 脚本语法检查。
5. 用 `git diff --cached --name-only` 审核 staged 文件。
6. 确认没有禁止文件后提交。
7. 推送到当前 GitHub remote。

## 默认禁止提交

- 图片：`.png`、`.jpg`、`.jpeg`、`.webp`、`.bmp`、`.tif`、`.tiff`
- 视频：`.mp4`、`.mov`、`.avi`、`.mkv`、`.webm`、`.m4v`、`.wmv`
- 模型：`.safetensors`、`.ckpt`、`.pt`、`.pth`、`.bin`、`.onnx`
- 运行产物：`characters/**/metadata/*.csv`、抽帧图、候选分类图、ComfyUI 输出图
- 本地日志、缓存、虚拟环境

如果确实需要提交某个生成文件，必须单独说明文件路径和原因。
