<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="download-image"></a>
# 下载图片

命令：`onekit run image-download`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**图片**。 保真度：**精确**。 从直接的 URL 或页面上可访问的第一张图片下载原始 PNG、JPEG、WebP、GIF、TIFF、BMP、ICO 或 AVIF 字节。最多 128 MiB。网站可能阻止访问。下载并不授予使用权。

接受的类型：`txt`。输出类型：`*`。接受多个输入：**否**。

输入验证：**文本**。所需文件数量：**1–1**。CLI：**每个文件 16,384 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：无。

Python 软件包：标准库或外部引擎。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/link_tools.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
