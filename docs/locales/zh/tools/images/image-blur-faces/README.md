<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="automatically-blur-faces"></a>
# 自动模糊人脸

命令：`onekit run image-blur-faces`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**图像**. 保真度：**存在取舍**。使用 YuNet 在本地检测人脸并模糊处理，导出新的 PNG。分享前请逐一检查人脸：自动检测可能遗漏人脸，模糊处理不能保证匿名。仅支持不超过 1600 万像素的单帧图像。

接受的类型：`png, jpeg, webp, gif, bmp, tiff, ico`。输出类型：`png`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：无。

Python 包：onnxruntime、numpy、Pillow。 外部引擎：语言适配器请参阅开发者引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/face_blur.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
