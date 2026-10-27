<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="blur-pixelate--image-effects"></a>
# 模糊、像素化和图像效果

命令：`onekit run image-effects`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**图片**。 保真度：**存在取舍**。 一个工具搞定模糊、像素化、方框模糊、实色覆盖或灰度处理。可应用于整个图像或选定区域，强度可调，并可导出新的 PNG。模糊和像素化不能保证永久去除敏感细节。仅支持单帧图片。

接受的类型：`png, jpeg, webp, gif, bmp, tiff, ico`。输出类型：`png`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`effect`, `scope`, `strength`, `color`, `regions`.

Python 软件包：Pillow。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/image_effects.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
