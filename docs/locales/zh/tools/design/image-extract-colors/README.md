<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="extract-image-colors"></a>
# 提取图片颜色

命令：`onekit run image-extract-colors`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**设计**。 保真度：**精确**。 从有界图像样本中提取中值切割主色。排除完全透明的像素；部分透明会在白色背景上合成。颜色比例描述的是样本，而不是语义对象。

接受的类型：`png, jpeg, webp, gif, bmp, tiff, ico`。输出类型：`json`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`colors`.

Python 软件包：Pillow。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/photo_tools.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
