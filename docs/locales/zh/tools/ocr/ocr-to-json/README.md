<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="ocr-to-json"></a>
# OCR 转 JSON

命令：`onekit run ocr-to-json`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**OCR**。 保真度：**存在取舍**。 识别结果取决于扫描质量和已安装的语言包。公式和布局可能需要手动修正。

接受的类型：`pdf, png, jpeg, webp, gif, bmp, tiff, ico`。输出类型：`json`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`language`, `dpi`.

Python 软件包：pytesseract, Pillow, pypdfium2, python-docx。外部引擎：tesseract.

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/ocr/__init__.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
