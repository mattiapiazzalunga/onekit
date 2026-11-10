<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="apk-to-xapk"></a>
# APK → XAPK

命令：`onekit run apk-to-xapk`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**转换工具**. 保真度：**精确**。将一个独立 APK 及其元数据打包为 XAPK 归档，不改写 APK 字节。拒绝拆分 APK。需要支持 XAPK 的安装程序；不验证签名。

接受的类型：`apk`。输出类型：`xapk`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：无。

Python 软件包：标准库或外部引擎。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/android_packages.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
