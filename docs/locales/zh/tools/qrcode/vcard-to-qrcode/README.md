<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="vcard-to-qr-code"></a>
# vCard 到 二维码

命令：`onekit run vcard-to-qrcode`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**二维码**。 保真度：**精确**。 本地创建标准 二维码。容量取决于内容和错误校正。保留空白区并在打印前测试二维码。

接受的类型：`json, vcf`。输出类型：`png`。接受多个输入：**否**。

输入验证：**文本**。所需文件数量：**1–1**。CLI：**每个文件 16,384 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`format`, `shape`, `corner_style`, `overlay_type`, `overlay_text`, `overlay_image_base64`, `overlay_size`, `error_correction`, `scale`, `border`, `dark`, `light`, `transparent_background`, `include_payload`.

Python 软件包：segno, Pillow。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/qrcode.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
