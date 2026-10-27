<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="download-audio"></a>
# 下载音频

命令：`onekit run audio-download`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**音频**。 保真度：**存在取舍**。 下载直接的音频文件或可访问页面公开的音频源。原始模式保留下载的字节；MP3 转换是有损的。最多支持 128 MiB。登录和受保护的流可能会阻止下载。仅在获得许可的情况下使用。

接受的类型：`txt`。输出类型：`*`。接受多个输入：**否**。

输入验证：**文本**。所需文件数量：**1–1**。CLI：**每个文件 16,384 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`format`, `quality`.

Python 软件包：标准库或外部引擎。外部引擎：ffmpeg, ffprobe.

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/link_tools.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
