<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="video-to-frames"></a>
# 视频转帧

命令：`onekit run video-to-frames`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**视频**。 保真度：**存在取舍**。 使用 FFmpeg 从视频中提取 PNG 帧。选择开始时间、持续时间和宽度。最多 120 帧：原始帧模式会保留时间区间内的每一帧；否则时间戳会按照请求的帧率采样。

接受的类型：`mp4, webm, mkv, mov, avi, gif, mpeg, mpg, m4v, ogv, ts`。输出类型：`png`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`start`, `duration`, `fps`, `width`, `all_frames`.

Python 软件包：Pillow。外部引擎：ffmpeg, ffprobe.

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/video_edit.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
