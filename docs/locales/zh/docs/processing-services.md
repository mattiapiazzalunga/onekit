<a id="processing-services"></a>
# 处理服务

`ExecutionContext` 可以独立于工具选项提供可信的本地引擎原语。处理 API 会继续验证输入的工件、应用预算并检查输出工件。引擎服务会返回读数或像素；公共处理处理器会解释这些读数并生成结果。服务只针对一次执行，并且不会更改默认的 CLI 引擎。

可选服务记录在 `ExecutionContext` 中，包括符号读取、OCR、语音识别、前景蒙版和 PDF 栅格化。PDF 页面记录包含已编码的栅格数据及以点为单位的物理尺寸。栅格数据编码、幻灯片组装和不可恢复的永久遮盖仍由公共处理程序处理。语音记录使用语言和 start/end/text 片段列表。OCR 记录包含每页的文本或带有可搜索文本的 PDF 字节，也可提供物理尺寸以便重新缩放。

JavaScript 处理模块可以独立于 Python 驱动使用：

- `tools/developer/source_engine.mjs` 导出源转换和结果处理、本地格式化器主机接口、语法树检查、本地 JSON 指针验证、API 规范选择和容器配方处理。引擎加载、进程隔离和解析器生命周期属于调用方。
- `tools/document_engine.mjs` 使用 Pandoc 文档节点的子集导出基本语义文档转换。它接受 Markdown 和 HTML 解析器服务，省略活动内容和外部图像加载，并写入独立的 LaTeX。PDF 写入器服务接收语义文档；布局、字体资源和渲染属于该写入器。解析器复杂性限制由调用方参数决定。

该文档子集涵盖了段落、标题、强调、代码、链接、列表、引用和水平线。表格以文本行表示。它并不宣称具有完整的文档排版引擎功能。现有的原生 CLI 文档转换仍可使用其原引擎协议。

对于没有本地文档执行程序的安装，Python 处理 API 也接受 `ExecutionContext(portable_documents=True)`。Markdown/HTML 到 PDF 或 LaTeX 然后使用 `tools/portable_documents.py`：有界本地 HTML 解析，MarkdownIt，转义 LaTeX，以及带有内置 Vera 字体的 ReportLab 布局。它从不获取资源或执行源标记。这种刻意的基础模式省略了 CSS 和活动内容，将表格表示为文本行，拒绝不支持的 PDF 字形。`DocumentLimits` 独立控制节点、嵌套、块和 PDF 页预算，而不受输入和输出字节限制的影响。安装 `documents` 和 `pdf` 附加组件。 本地 Pandoc/TeX 转换仍然是默认；仅对这些本地路径的更改不会影响可移植模式。

`tools/symbols.py` 提供原生扫描所用的 ZXing 读取器设置。调用方提供的读取器可以使用相同的格式、旋转和反色设置。条形码处理程序会先规范化格式别名，再构造公开的结果。`input_image` 和 `pixel_input` 在原生读取器与调用方提供的像素读取器之间共用图像方向处理和白色背景透明度合成方式。调用方可以独立于检测设置缩小像素处理上限。

`tools/background.py` 暴露了 U2Net 模型校验和、`foreground_input` 和 `foreground_output`。输入是形状为 `[1,3,320,320]` 的连续小端 float32 张量；提供的预测是形状为 `[1,1,320,320]` 的第一个 float32 输出。原生推理和提供的预测都使用相同的张量准备、掩码归一化和图像调整大小。推理运行环境的差异仍可能影响浮点数结果。

`tools/transcription.py` 暴露了 `recognition_parameters`，包括模型、语言、采样率、束宽和前文本条件。不同的推理主机必须明确支持这些设置；共享设置并不意味着解码实现或量化模型转换的等效性。

开发者处理程序在其 Python 环境安装 sqlparse 和 SQLFluff 后会直接使用它们。原来的独立 `sqlformat` 和 `sqlfluff` 命令在这些导入不可用时仍然受支持。SQL 验证使用请求的 SQLFluff 方言，默认使用 ANSI；它不会执行查询。
