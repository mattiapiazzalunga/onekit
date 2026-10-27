<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-pdf-watermark"></a>
# 移除 PDF 水印

命令：`onekit run pdf-remove-watermark`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**PDF**。 保真度：**存在取舍**。 检查并删除选定的文本、图像和 Form XObject 调用，包括嵌套的 Form XObject 和通过字体编码的文本。自动删除已标记的水印工件和水印注释。未标记的对象需要手动选择或提供精确文本；已合并到图像像素中的水印无法从图像中分离。请检查每一页。

接受的类型：`pdf`。输出类型：`pdf`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`text`, `mode`, `objects`.

Python 软件包：pypdf。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/pdf_design.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
