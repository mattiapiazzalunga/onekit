<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="convert-audio"></a>
# 转换音频

命令：`onekit run audio-convert`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**音频**。 保真度：**存在取舍**。 可用编解码器取决于您的 FFmpeg 构建；重新编码可能会损失质量。

接受的类型：`mp3, wav, flac, ogg, aac, m4a, mp4, aif, aiff, opus, wma`。输出类型：`*`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`format`, `codec`, `bitrate`.

Python 软件包：标准库或外部引擎。外部引擎：ffmpeg, ffprobe.

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/media/__init__.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
