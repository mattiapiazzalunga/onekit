<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="verify-digital-signature"></a>
# 验证数字签名

命令：`onekit run signature-verify`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**安全**。 保真度：**精确**。 在本地检查 PDF 和 CMS 签名并执行 AdES 验证。分离式签名需要原始文件。可另附一个签名证据 ZIP。缺少信任或吊销证据时，结果为不确定。

接受的类型：`*`。输出类型：`json`。接受多个输入：**是**。

输入验证：**允许任意文件类型**。所需文件数量：**1–3**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：无。

Python 软件包：pypdf, asn1crypto, pycryptodome。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/signatures.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
