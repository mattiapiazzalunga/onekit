<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-text-formatting"></a>
# 删除文本格式

命令：`onekit run text-strip-formatting`。运行 `onekit run --help` 查看输入和输出参数的帮助。

类别：**分析**。 保真度：**存在取舍**。 将粘贴的文本、UTF-8/UTF-16 文本文件、HTML、Markdown 或 Word DOCX 正文，在本地转换为 UTF-8 TXT 文件。去除样式、链接和标记，同时保留可读文本和基本段落/表格换行。纯文本保留字面标点。无 OCR；DOCX 的页眉、页脚、图像和评论会被省略。每个输入最多支持 8 MiB。

接受的类型：`txt, html, md, docx`。输出类型：`txt`。接受多个输入：**否**。

输入验证：**允许任意文件类型**。所需文件数量：**1–1**。CLI：**每个文件 8,388,608 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`input_format`.

Python 软件包：markdown-it-py, defusedxml。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实现：[工具系列共用适配器](../../../../../../src/onekit/tools/plain_text.py)。契约和回归测试数据：[测试](../../../../../../tests/test_core.py)。引擎设置和许可：[引擎指南](../../../docs/engines.md)。

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
