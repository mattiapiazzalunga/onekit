<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-metadata"></a>
# 删除元数据

命令：`onekit run file-metadata-remove`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**分析**。 保真度：**精确**。 保留所选内容；验证重要输出。

接受的类型：`*`。输出类型：`*`。接受多个输入：**否**。

输入验证：**允许任意文件类型**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：无。

Python 软件包：标准库或外部引擎。外部引擎：exiftool.

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/inspector/__init__.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
