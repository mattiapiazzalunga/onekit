<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="validate-pdfua"></a>
# 验证 PDF/UA

指挥:`onekit run pdf-validate-pdfua`. 使用`onekit run --help`作为输入和输出参数.

类别:**pdf**. 忠诚:**准确**。 请检查date=中的日期值 (帮助) PDF/UA-1自动使用本地验证引擎. 如果结果过头,仍需对无障碍情况进行人工审查。 报告确定了引擎,剖面和确切的文件散列.

接受的类型：`pdf`。输出类型：`json`。接受多个输入：**否**。

输入验证：**按文件类型验证**。所需文件数量：**1–1**。CLI：**每个文件 134,217,728 字节**，**总计 134,217,728 字节**。处理前会检查文件内容。重命名文件不会改变其实际格式。

选项：`profile`.

Python 软件包：标准库或外部引擎。外部引擎：有关编程语言适配器，请参阅开发工具引擎矩阵。

处理实施:[ 分摊家庭适配器](../../../../../../src/onekit/tools/pdf_conformance.py). 合同和回归固定装置:[ tests](../../../../../../tests/test_core.py)。 发动机安装和许可证:[engine指南](../../../docs/engines.md).

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
