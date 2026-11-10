# Linux 动画导出依赖

## 工具怎么选

| 用途 | 工具 | 是否必需 |
| --- | --- | --- |
| 合成办公室和角色、播放场景动画 | Godot 4.7.2 stable | 制作场景动画时需要 |
| 将 Godot 场景渲染成视频 | Godot Movie Maker | 随 Godot 提供，无需单独安装 |
| 将帧序列编码为 MP4 | FFmpeg | 需要 MP4 时安装 |
| 绘制或调整逐帧像素动画、导出 GIF/APNG/精灵表 | Pixelorama | 可选 |

当前仓库保存生成素材和 ComfyUI 工作流，还没有 Godot 场景工程。开始合成动画时，需要在 Godot 中创建或打开场景工程，并导入 `assets/generated/` 中的素材。

## Linux 安装

- **Godot**：使用 [Godot 官方下载页](https://godotengine.org/download/) 的 Linux 稳定版。当前素材工作流以 Godot 4.7.2 为基准；普通 2D 项目下载标准版即可，不需要 .NET 版。
- **FFmpeg**：仅在需要把 Godot 输出转成 MP4，或在 Pixelorama 中导出视频时需要。Ubuntu/Debian 可运行 `sudo apt install ffmpeg`；其他发行版从系统包管理器安装。也可查看 [FFmpeg 官方下载页](https://ffmpeg.org/download.html)。
- **Pixelorama**：可选的免费开源像素编辑器，Linux 安装方式见[官方安装说明](https://orama-interactive.github.io/Pixelorama-Docs/docs/user_manual/installation/)，源码和格式说明见[官方仓库](https://github.com/Orama-Interactive/Pixelorama)。

## Godot 导出视频

Godot Movie Maker 是 Godot 自带的离线渲染模式，适合导出已经合成好的办公室场景动画。它内置支持 OGV、AVI，以及 PNG 帧序列和 WAV 音轨；这些功能不需要额外插件。设置 Movie File 输出路径，在编辑器右上角开启胶片图标，再运行场景即可。详见 [Godot 创建影片文档](https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html) 和 [MovieWriter 格式说明](https://docs.godotengine.org/en/stable/classes/class_moviewriter.html)。

如果目标格式是 MP4，安装 FFmpeg 后再将 Movie Maker 输出的帧序列编码为视频。若 OGV 或 AVI 满足需求，则不需要 FFmpeg。

## 像素帧动画

角色需要逐帧绘制、修整或导出成 GIF、APNG、精灵表时，用 Pixelorama。它是素材编辑工具，不是 Godot 场景合成的必需依赖；只有在 Pixelorama 导出视频格式时才需要 FFmpeg。

## 建议流程

1. 用 Pixelorama 整理角色帧或精灵表（需要逐帧编辑时）。
2. 在 Godot 中导入角色和办公室素材，组合场景并制作动画。
3. 用 Godot Movie Maker 输出 OGV/AVI 或帧序列；需要 MP4 时再用 FFmpeg 编码。
