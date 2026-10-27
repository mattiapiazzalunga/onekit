<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="generate-barcode"></a>
# 生成条形码

命令：`onekit run text-to-barcode`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**二维码**。 保真度：**精确**。 本地生成 Code 128、Code 39、EAN-13、EAN-8、UPC-A、ITF 和 ISBN-13。零售校验位已验证或计算；标识符未通过 OneKit 注册或分配。

接受的类型：`txt`。输出类型：`png`。接受多个输入：**否**。

输入验证：**文本**。所需文件数量：**1–1**。CLI：**每个文件 1,024 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`barcode_type`, `format`, `module_width`, `height`, `quiet_zone`, `show_text`, `font_size`, `dpi`.

Python 软件包：python-barcode, Pillow。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/barcode.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
