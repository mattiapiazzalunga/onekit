<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="xml-to-json"></a>
# XML 转 JSON

命令：`onekit run xml-to-json`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**格式转换**。 保真度：**精确**。 XML 表格使用重复的平面记录。JSON 到 XML 使用类型化的根/项模式来保留类型；XML 属性使用 @，JSON 中的文本使用 #text。电子表格公式不会被计算；默认使用第一个工作表。转换后请检查模式和值。

接受的类型：`xml`。输出类型：`json`。接受多个输入：**否**。

输入验证：**文本**。所需文件数量：**1–1**。CLI：**每个文件 8,388,608 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：无。

Python 软件包：defusedxml。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/structured_data.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
