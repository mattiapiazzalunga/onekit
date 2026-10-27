<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="extract-audio-from-video"></a>
# 从视频中提取音频

命令：`onekit run video-extract-audio`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**视频**。 保真度：**存在取舍**。 使用 FFmpeg 将第一个音轨提取为 MP3，比特率为 192 kbps。需要包含音频的视频；重新编码可能会损失质量。

接受的类型：`mp4, webm, mkv, mov, avi, gif, mpeg, mpg, m4v, ogv, ts`。输出类型：`mp3`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：无。

Python 软件包：标准库或外部引擎。外部引擎：ffmpeg, ffprobe.

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/video_edit.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
