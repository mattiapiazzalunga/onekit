<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="permanently-redact-image"></a>
# 永久遮盖图片内容

命令：`onekit run image-redact`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**图片**。 保真度：**存在取舍**。 将选定像素替换为纯黑色，导出新的不透明 PNG，不包含原始元数据或因透明度而隐藏的像素。仅支持单帧图片。原始文件保持不变。

接受的类型：`png, jpeg, webp, gif, bmp, tiff, ico`。输出类型：`png`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`regions`.

Python 软件包：Pillow。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/redaction.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
