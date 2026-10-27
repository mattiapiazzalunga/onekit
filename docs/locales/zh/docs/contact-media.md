<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="contacts-image-enlargement-and-local-media-tools"></a>
# 联系人、图片放大和本地媒体工具

| 工具 | 输入 | 选项 | 输出 |
| --- | --- | --- | --- |
| `vcard-generate` | 联系 JSON，按 `vcard-to-qrcode` 的要求 | 联系字段属于输入 JSON | VCF 3.0 / 4.0 |
| `qrcode-to-vcard` | 包含完整 vCard 的 二维码图片 | 无 | 对每个检测到的联系人生成一个 VCF |
| `image-upscale` | 单帧图像 | `scale`: 2（默认）、3 或 4 | PNG |
| `image-remove-background` | 单帧图像 | 无 | 透明 PNG |
| `video-compress` | 视频 | `compression_level`：light、balanced（默认）、maximum | MP4，或者如果更小则使用原始文件 |
| `video-speed` | 视频 | `speed`: 0.25–4，默认 2 | MP4，带同步、保留音调的音频 |
| `video-to-gif` | 视频 | `start`: 秒，`duration`: 0.1–30，`fps`: 1–30，`width`: 64–1280 | 循环播放 GIF 无音频 |
| `audio-to-text` | 音频 | `language`：auto（默认）、it、en 或其他 Whisper 语言代码 | TXT 和时间戳 JSON |

仅安装所需的 Python 附加组件：

```sh
python -m pip install 'onekit-tools[qrcode,images,background,transcription]'
```

视频操作还需要在 PATH 上的 `ffmpeg` 和 `ffprobe`。CLI 使用已安装的 FFmpeg 构建；支持的编解码器取决于该构建。`onekit doctor TOOL` 检查所需的引擎和包。

```sh
onekit run vcard-generate contact.json -o contact.vcf
onekit run qrcode-to-vcard contact-qr.png -o contacts/
onekit run image-upscale photo.png --options '{"scale":2}' -o larger.png
onekit run image-remove-background portrait.jpg -o transparent.png
onekit run video-compress clip.mov --options '{"compression_level":"balanced"}' -o compressed/
onekit run video-speed clip.mp4 --options '{"speed":0.5}' -o slower.mp4
onekit run video-to-gif clip.mp4 --options '{"start":1,"duration":3,"fps":12,"width":480}' -o clip.gif
onekit run audio-to-text voice.wav --options '{"language":"it"}' -o transcript/
```

联系 JSON 示例：

```json
{"first_name":"Ada","last_name":"Lovelace","version":"3.0","emails":["ada@example.org"]}
```

QR 提取接受完整的 vCard 3.0/4.0 负载并带有显示名称。它不会遵循联系人下载链接或将任意 QR 文本转换为联系人数据。放大使用 Lanczos 重采样，而不是 AI 模型。输出限制为 4000万像素。动态图像会被 Python 图像适配器拒绝。

CLI 背景移除适配器直接加载 U2Net 和 ONNX 运行时，避免 rembg 的 Pillow <13 依赖限制。模型下载经过校验和验证，并缓存到本地 OneKit 模型缓存中。可选模型引擎保持与可移植 `all` 附加组件分离。
