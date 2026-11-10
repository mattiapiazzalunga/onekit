<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="text-to-pdfua"></a>
# 文本转 PDF/UA

指挥:`onekit run txt-to-pdfua`. 使用`onekit run --help`作为输入和输出参数.

类别:**pdf**. 忠诚:**准确**。 从纯文本中创建一个标有PDF/UA-1的标有标题和语言的标记 。 空行相分出诸段. 仅拉丁文字体;审查读取顺序和意义. 自动检查不能取代人工访问审查.

接受的类型：`txt`。输出类型：`pdf`。接受多个输入：**否**。

输入验证:**text**. 需要的文件计数 : **1–1**. CLI:**262,144个字节/每个文件**,**8,388,608个字节合计**. 处理前要检查内容 。 重命名一个文件不会改变它的实际格式 。

选项:`title`,`language`。

Python个包裹:报告栏,pypdf,Pillow. 外部引擎:参见语言适配器的开发者引擎矩阵.

处理实施:[ 分摊家庭适配器](../../../../../../src/onekit/tools/pdfua.py). 合同和回归固定装置:[ tests](../../../../../../tests/test_core.py)。 发动机安装和许可证:[engine指南](../../../docs/engines.md).

该目录由 `python scripts/tool_docs.py` 从共享目录生成。编辑注册表和家族适配器，添加回归测试数据，然后重新生成目录。
