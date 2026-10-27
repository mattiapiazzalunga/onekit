<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="add-watermark-to-pdf"></a>
# 给PDF添加水印

命令：`onekit run pdf-watermark`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**PDF**。 保真度：**精确**。 在所有或选定页面上添加文本或 PNG/JPEG 图像水印，同时保留源文本和图形。支持西欧文本、单一或重复布局、旋转和不透明度。原始文件保持不变。

接受的类型：`pdf`。输出类型：`pdf`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`text`, `pages`, `font`, `font_size`, `color`, `opacity`, `angle`, `position`, `layout`, `margin`, `watermark_type`, `image_base64`, `image_width`.

Python 软件包：pypdf, reportlab, Pillow。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/pdf.watermark/__init__.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
