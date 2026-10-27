<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="color-palette-generator"></a>
# 调色板生成器

命令：`onekit run color-palette`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**设计**。 保真度：**精确**。 生成五色 OKLCH 调色板，通过降低色度使颜色落入 sRGB 色域，并计算 WCAG 文本对比度。配色配色方案规则只是设计启发式方法，并不保证无障碍可访问性。

接受的类型：`txt`。输出类型：`json`。接受多个输入：**否**。

输入验证：**文本**。所需文件数量：**1–1**。CLI：**每个文件 128 字节**，**总计 1,048,576 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`harmony`, `lightness`, `chroma`, `hue`, `format`.

Python 软件包：标准库或外部引擎。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/design.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
