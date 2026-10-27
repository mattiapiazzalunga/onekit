<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="txt-to-yaml"></a>
# TXT 转 YAML

命令：`onekit run txt-to-yaml`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**格式转换**。 保真度：**精确**。 需要包含在 TXT 文件中的有效 YAML。验证并保留其源代码和注释；不支持的值、重复键和不安全标签会被拒绝。

接受的类型：`txt`。输出类型：`yaml`。接受多个输入：**否**。

输入验证：**使用所选编码的文本**。所需文件数量：**1–1**。CLI：**每个文件 8,388,608 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`source_encoding`.

Python 软件包：PyYAML。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/text_converters.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
