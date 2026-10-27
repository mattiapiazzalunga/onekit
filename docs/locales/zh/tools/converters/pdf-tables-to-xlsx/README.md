<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="pdf-tables-to-excel"></a>
# PDF 表格转 Excel

命令：`onekit run pdf-tables-to-xlsx`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**格式转换**。 保真度：**存在取舍**。 从对齐的可选择文本中检测表格。扫描件需要 OCR 识别；复杂布局、合并单元格和列对齐需要复审。Excel 每张表使用一个工作表；CSV 每张表导出一个文件。

接受的类型：`pdf`。输出类型：`xlsx`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`pages`.

Python 软件包：pycryptodome, pypdf, openpyxl。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/pdf_tables.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
