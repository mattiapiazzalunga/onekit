<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="regex-tester"></a>
# 正则测试器

命令：`onekit run dev-regex-test`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**开发**。 保真度：**精确**。 在本地测试 JavaScript 正则表达式，包括捕获、命名组、UTF-16 位置和替换。最多处理 128 KiB 的文本，1000 个匹配和 1 MiB 的输出。执行有时间限制；CLI 需要 Node.js。

接受的类型：`txt`。输出类型：`json`。接受多个输入：**否**。

输入验证：**文本**。所需文件数量：**1–1**。CLI：**每个文件 131,072 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`pattern`, `flags`, `max_matches`, `enable_replacement`, `replacement`.

Python 软件包：标准库或外部引擎。外部引擎：node.

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/regex_tester.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
