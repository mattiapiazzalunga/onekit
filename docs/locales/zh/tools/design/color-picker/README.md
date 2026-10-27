<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="color-picker"></a>
# 取色器

命令：`onekit run color-picker`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**设计**。 保真度：**精确**。 从 TXT 获取六位数 HEX 颜色，或采样一个 EXIF 取向的图像像素。报告可见 sRGB、原始 RGBA、OKLCH 和文本对比度。透明像素会在白色上合成。

接受的类型：`png, jpeg, webp, gif, bmp, tiff, ico, txt`。输出类型：`json`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`x`, `y`.

Python 软件包：Pillow。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/photo_tools.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
