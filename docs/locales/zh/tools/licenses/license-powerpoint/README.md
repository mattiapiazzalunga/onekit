<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="powerpoint-license-checker"></a>
# PowerPoint 许可证检查器

命令：`onekit run license-powerpoint`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**许可证**。 保真度：**存在取舍**。 基于声明和元数据的估算，而不是权利证书或法律许可。请务必通过原始来源和权利持有者核实每一项发现。缺失信息绝不意味着可以自由使用。作者和版权持有者可能不同。文件在本地分析；链接直接从源下载。归档文件是有限的，扫描可能不完整。

接受的类型：`pptx, pptm, ppt`。输出类型：`json`。接受多个输入：**否**。

输入验证：**允许任意文件类型**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`ref`.

Python 软件包：license-expression, defusedxml, olefile。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/license_check.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
