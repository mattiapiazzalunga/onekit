<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="validate-pdfa"></a>
# 验证 PDF/A

命令：`onekit run pdf-validate-pdfa`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**PDF**。 保真度：**精确**。 验证 PDF/A-1b、2b 或 3b 与 pikepdf 配合使用。不支持的结构会报告为未检查，从不报告为合规。其他符合性等级不支持。

接受的类型：`pdf`。输出类型：`json`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`profile`.

Python 软件包：pikepdf, jsonschema, fonttools。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/pdf/__init__.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
