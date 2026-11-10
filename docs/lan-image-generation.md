# 局域网生图接口

ComfyUI 在这台 Mac 上运行模型和工作流；同一 `192.168.1.x` 局域网内的设备可用浏览器或 HTTP API 请求生图。室友不需要安装模型。

## 启动服务（运行 ComfyUI 的 Mac）

在项目目录运行：

```sh
./scripts/start-comfyui-lan.zsh
```

脚本读取 Mac 的 `en0` 地址，只在地址属于 `192.168.1.x` 时启动，并只绑定这个地址的 `8188` 端口。当前地址是 `192.168.1.170`。保持终端窗口打开，关闭进程即可停止服务。

如果更换网络后地址变化，可在 Mac 上运行 `ipconfig getifaddr en0` 查询新地址。若 ComfyUI 安装目录不在默认位置，可设置 `COMFYUI_ROOT` 后再启动：

```sh
COMFYUI_ROOT="/path/to/ComfyUI" ./scripts/start-comfyui-lan.zsh
```

## 浏览器访问

室友连接同一个 `192.168.1.x` 网络后，在浏览器打开：

```text
http://192.168.1.170:8188
```

如果主机地址变化，把网址中的 IP 换成 Mac 当前的 `en0` 地址。ComfyUI 页面可用于编辑工作流并排队生成。

## 用 HTTP API 生图

在室友的电脑上克隆仓库并安装 Python 3，然后运行：

```sh
python3 scripts/generate_image.py \
  --host 192.168.1.170 \
  --prompt "pixel art, a tiny lavender dragon girl reading a book"
```

脚本会提交默认 FLUX.2 Klein 4B 像素风工作流，等待生成完成，并把图片下载到当前目录的 `lan-output/`。可用 `--seed 12345` 固定种子，也可用 `--output ./images` 指定下载目录。把 `--host` 换成运行 ComfyUI 的 Mac 当前地址。

客户端脚本调用 ComfyUI 原生端点：

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| `POST` | `/prompt` | 提交 API 格式工作流 |
| `GET` | `/history/{prompt_id}` | 查询任务状态和输出 |
| `GET` | `/view?filename=…&subfolder=…&type=output` | 下载生成图片 |

工作流文件位于 `ComfyUI/user/default/workflows/Pixel-Dragon-Local-api.json`。图片也会保存在运行 ComfyUI 的 Mac 项目目录 `assets/generated/dragon-girl/local-comfyui/`。

## 连接不上时

- 确认运行 ComfyUI 的终端仍在工作，且主机和客户端都在同一个 `192.168.1.x` 网络。
- 在 Mac 上重新查询 `ipconfig getifaddr en0`，确认客户端使用了当前 IP。
- 如果 macOS 防火墙询问是否允许 Python 接收连接，选择允许。

此接口没有登录验证，只在指定的家庭局域网地址上监听；不要把 `8188` 端口转发到互联网。
