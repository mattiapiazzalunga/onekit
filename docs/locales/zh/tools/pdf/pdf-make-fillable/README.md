<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="make-pdf-fillable"></a>
# 创建可填写的 PDF

命令：`onekit run pdf-make-fillable`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**PDF**。 保真度：**精确**。 添加具有名称的 AcroForm 文本字段、复选框和下拉选项，使用相对于页面左上角的归一化坐标指定矩形区域。保留现有字段和页面内容。不自动检测空白区域，也不转换 XFA；请检查阅读器的兼容性。

接受的类型：`pdf`。输出类型：`pdf`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`fields`.

Python 软件包：pypdf。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/pdf_design.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
