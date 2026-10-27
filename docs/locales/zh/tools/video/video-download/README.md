<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="download-video"></a>
# 下载视频

命令：`onekit run video-download`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**视频**。 保真度：**精确**。 从 YouTube 和其他 yt-dlp 站点下载，最多支持 128 MiB。站点支持情况不同；需要网络连接。

接受的类型：`txt`。输出类型：`*`。接受多个输入：**否**。

输入验证：**文本**。所需文件数量：**1–1**。CLI：**每个文件 16,384 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`quality`, `cookies`, `cookies_from_browser`, `format_id`, `referer`, `list_formats`.

Python 软件包：yt-dlp。外部引擎：ffmpeg.

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/video_download.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
