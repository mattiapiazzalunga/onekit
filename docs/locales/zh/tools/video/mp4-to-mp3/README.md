<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="mp4-to-mp3"></a>
# MP4 转 MP3

命令：`onekit run mp4-to-mp3`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**视频**。 保真度：**存在取舍**。 将 MP4 的第一条音轨提取为 192 kbps 的 MP3。视频必须包含音轨；重新编码可能会降低音质。

接受的类型：`mp4`。输出类型：`mp3`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：无。

Python 软件包：标准库或外部引擎。外部引擎：ffmpeg, ffprobe.

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/video_edit.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
