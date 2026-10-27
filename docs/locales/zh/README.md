<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->

语言： [English](../../../README.md) · [Italiano](../it/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [Deutsch](../de/README.md) · [Русский](../ru/README.md) · [中文](README.md).

<p align="center">
  <a href="https://onekit.org"><img src="https://raw.githubusercontent.com/mattiapiazzalunga/onekit/main/images/logo.png" alt="OneKit logo" width="112" height="112"></a>
</p>
<h1 align="center">OneKit</h1>
<p align="center">一个工具箱，您的文件始终属于您。</p>
<p align="center"><a href="https://github.com/mattiapiazzalunga/onekit/stargazers"><img alt="GitHub 星标" src="https://img.shields.io/github/stars/mattiapiazzalunga/onekit"></a> <a href="https://pypi.org/project/onekit-tools/"><img alt="PyPI" src="https://img.shields.io/pypi/v/onekit-tools"></a> <img alt="PolyForm-Shield-1.0.0" src="https://img.shields.io/badge/license-PolyForm_Shield_1.0.0-blue"> <img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue"></p>

一个离线 Python 工具包，带有用于转换、PDF、图片、压缩文件、字体、文件检查、加密、开发者工具、OCR 和比较的 230 个工具。使用这个 CLI 或者在 **[onekit.org](https://onekit.org)** 的图形界面。

**源版本:** `0.6.1`。稳定下载只有在发布工作流完成后才可用。分发版本是 `onekit-tools`；独立拥有的 PyPI 项目 `onekit` 无关联。

[联系人与媒体指南](docs/contact-media.md)介绍独立 vCard 的生成、从二维码中提取 vCard、图像放大、背景移除、视频和 GIF 的压缩与速度调整，以及本地音频转写。

许可证检查：检查 PDF、Word、PowerPoint、Excel、视频、音频、图像、字体、EPUB、文件或公共 URL 中的代码/项目和数据集。分析保持在本地；报告为**未经验证的估算，而非所有权证明或使用许可**。请参阅 [许可证检查的用法和限制](docs/cli.md#local-license-and-copyright-estimates)。

**您的 CLI。您的智能代理 CLI。** 您可以自己使用 OneKit，或者让本地 AI 代理通过终端或子进程调用它。像 JSON 一样发现工具和需求，传递明确的输入/输出路径，并重用保存好的 `.1kit` 工作流来重复执行文件任务。参见 [本地代理和自动化](docs/cli.md#local-agents-and-automation)。

<a id="install"></a>
## Install

需要 Python 3.11 或更高版本。通用 wheel 安装包支持 x64/ARM64 平台上的 Windows、macOS 和 Linux。可选的原生库和外部引擎另有平台要求。

发布后：

```sh
python -m pip install onekit-tools
python -m pip install "onekit-tools[pdf,images,documents]"
onekit list
onekit doctor
```

从本地源代码仓库安装：

```sh
python -m pip install -e ".[all,test]"
python -m onekit --help
python -m pytest -q
```

基础 CLI **没有运行时依赖**。只需安装您需要的附加组件。`all` 包含标准的 Python 系列；视频下载、去背景、转录和数字签名使用单独的 `video`、`background`、`transcription` 和 `signing` 附加组件。原生引擎需单独安装。对于基于 Node 的开发工具，安装 Node.js、24+ 并运行 `onekit engines install`。CLI 会在首次使用时准备缺失的依赖和外部引擎。去背景和转录在首次使用时下载模型权重，然后重复使用本地缓存。

<a id="use"></a>
## Use

```sh
onekit run pdf-merge first.pdf second.pdf -o combined.pdf
onekit run pdf-extract-pages document.pdf --options '{"pages":"1,3-5"}' -o selected.pdf
onekit run image-convert image.png --options '{"format":"webp"}' -o image.webp
onekit run diff-notebook before.ipynb after.ipynb --options '{"mode":"code"}' -o changes.json
onekit run security-encrypt private-folder --ask-password -o private.zip
onekit run security-decrypt private.zip --ask-password -o restored
```

选项是 JSON 对象；将它们作为一个带引号的 shell 参数传递。使用 `--ask-password` 来处理机密。除非您传递 `--force`，否则现有输出会被保留。

`onekit list --group pdf`、`onekit list --json` 和 `onekit doctor TOOL_ID` 会显示合约和需求。每个工具在 [tools](../../../tools) 下都有一个目录，里面包含元数据和指向其共享实现的指针。有关选项和限制，请参见 [CLI 指南](docs/cli.md)。

<a id="toolkit"></a>
## Toolkit

| 家族 | 功能 |
| --- | --- |
| 转换器 | Markdown、HTML、LaTeX、PDF、Word、PowerPoint、图片、Base64、Excel、CSV 和 JSON |
| PDF | 合并/拆分，页面选择/顺序/删除，压缩，修复，[直接文本编辑](docs/pdf-editing.md)，文本覆盖，旋转，数字签名，加密/解锁，[本地 PDF/A 转换与验证](docs/pdfa.md) |
| 图片 | 提取嵌入的PDF图像，进行压缩、裁剪并更改格式 |
| 媒体 | 通过单独安装的 FFmpeg 进行音频/视频转换 |
| 存档 / 字体 | ZIP/TAR 变体；TTF/OTF 容器，WOFF/WOFF2 |
| 检查器 / 安全 | 文件类型标识、结构、元数据、编码、哈希、文本统计；支持身份验证的加密文件/文件夹归档 |
| 开发者 | 特定语言的格式化、解析器/编译器验证和选定的压缩 |
| OCR | 将扫描图片/PDF 转为可搜索 PDF、Word、Markdown、LaTeX、HTML 和 JSON |
| 差异 | 文本、代码、标准化 JSON、笔记本、LaTeX、PDF 和 Word 文本 |

<a id="pipelines-and-development"></a>
## Pipelines and development

`onekit pipeline --steps workflow.1kit INPUTS -o OUTPUT` 接受一个带版本的 `.1kit` 工作流程文档。每个步骤都会接收之前的输出。单输入步骤会映射到多个输出；合并步骤会接收整个集合。不兼容的类型会停止处理。

通过 [GitHub issues](https://github.com/mattiapiazzalunga/onekit/issues) 或 [网站需求看板](https://onekit.org/requests/) 报告漏洞和建议。贡献者可以在任意一个地方找到工作。

<a id="contribute-to-onekit"></a>
## Contribute to OneKit

帮助建设 OneKit 的开放革命：为每个人提供日常工具，从动手任务到由本地 AI 代理运行的工作流程。贡献力量，让工具更高效、更有效：提升速度和内存使用，修复错误结果，增加回归示例，或者澄清文档和代理工作流程。

核心是开源的（PolyForm Shield 1.0.0）。请阅读 [贡献指南](https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md)，并在 [GitHub 问题列表](https://github.com/mattiapiazzalunga/onekit/issues) 中找到一个任务，或者在 [请求板](https://onekit.org/requests/) 上提出改进建议。

<a id="license-and-creator"></a>
## License and creator

由 **[Mattia Piazzalunga](mailto:hello@mattiapiazzalunga.com)** 创建。版权所有 © 2026 Mattia Piazzalunga。开源 (PolyForm Shield 1.0.0)，根据 [PolyForm Shield 1.0.0](../../../LICENSE) 许可；参见 [NOTICE](../../../NOTICE)、[AUTHORS.txt](../../../AUTHORS.txt) 和 [CONTRIBUTORS.txt](../../../CONTRIBUTORS.txt)。第三方组件保留其许可。外部引擎是独立程序，有自己的再分发义务。

您可以为了允许的目的使用、修改和再分发核心，包括商业和内部使用。您不得用它来提供与该软件或许可方或其关联公司使用该软件提供的产品竞争的产品或服务；免费产品和不同的平台或界面也可以算作竞争。分享副本时，请附上许可文本或其 URL 以及软件提供的任何必需通知行。完整许可条款适用，包括其对新产品和已停产产品的例外、专利条款及免责声明。在这里，“开源 (PolyForm Shield 1.0.0)”指的是在这些条款下发布的源代码； 不竞争限制意味着这是可访问源码的软件，而不是完全开放源代码的自由软件。具体请参见 [ 许可指南 ](docs/licenses.md)。

导出并重新导入工作流而不处理输入文件：

```sh
onekit workflow export workflow.1kit -o exported-workflow.1kit
onekit workflow import workflow.1kit -o saved-workflow.1kit
onekit pipeline --steps saved-workflow.1kit input.json -o output.json
```

标准条形码可在 二维码和条形码类别以及 CLI: `text-to-barcode`, `scan-barcode`, `barcode-to-text` 中找到。Code 128、Code 39、 EAN-13, EAN-8, UPC-A, ITF 和 ISBN-13 支持 PNG/SVG，可配置尺寸及校验码验证。安装 `onekit-tools[barcode]` 或 `onekit-tools[qrcode]`。

可通过 `pdf-redact` 和 `image-redact` [永久遮盖 PDF 和图像中的内容](docs/redaction.md)。选定区域在重新编码的文件中变为不透明的黑色像素。PDF 将重建为纯图像文档，不包含原始文本、表单、批注、附件或元数据；图像将转换为不透明的 PNG，不包含原始元数据或因透明度而隐藏的像素。原始文件保持不变。

使用 `pdf-watermark` 添加可配置的 PDF 文字水印：不透明度、颜色、字体、页码范围、视觉位置、旋转和重复网格。文字和图形保持在 PDF 中。请参见 [水印指南](docs/watermark.md)。

<a id="contacts"></a>
## Contacts

- 一般问题和支持：[support@onekit.org](mailto:support@onekit.org)。
- 关于开源 (PolyForm Shield 1.0.0) 核心及贡献的问题：[developers@onekit.org](mailto:developers@onekit.org)。
- 隐私、GDPR 以及个人数据请求：[privacy@onekit.org](mailto:privacy@onekit.org)。
- 法律问题、许可和权限请求：[legal@onekit.org](mailto:legal@onekit.org)。
- 安全漏洞和滥用报告：[security@onekit.org](mailto:security@onekit.org)。
