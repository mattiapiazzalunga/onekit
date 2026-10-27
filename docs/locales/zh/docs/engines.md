<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="external-engines-and-licenses"></a>
# 外部引擎和许可证

所有者批准了单独安装的开源引擎。它们不包含在 Python wheel、源码下载或初始 Docker 镜像中。`onekit doctor` 报告了要求。`ONEKIT_ALLOW_COPYLEFT=0` 明确禁用了列出的 copyleft 适配器。保持上游工具更新；本地子进程不是针对恶意文档的完整沙箱。

| 引擎 | 命令 | 使用 / 许可相关考虑 |
| --- | --- | --- |
| LibreOffice | `soffice` / `libreoffice` | Office → PDF/图片；MPL 和第三方声明。 |
| Pandoc | `pandoc` | 高级标记转换；GPL。 |
| TeX Live/pdfTeX | `pdflatex` | LaTeX/Pandoc PDF；引擎、宏和字体有单独的许可。 |
| FFmpeg | `ffmpeg` | 媒体；根据构建和编解码器而定为 LGPL 或 GPL。 |
| veraPDF | `verapdf` | 可选的档案输出独立验证；上游 GPL/MPL 和 Java 要求。 |
| ExifTool | `exiftool` | 支持的文件类型中的元数据；上游 Perl 许可。 |
| Tesseract | `tesseract` | OCR；Apache 引擎及单独授权的语言数据。 |

如果要分发这些程序，包括在 Docker 里，保留它们的许可证/通知，并提供所需的对应源代码/构建材料。AGPL 网络集成需要单独评估。商业使用和源代码/再分发义务是不同的问题。独立的流程并不普遍消除义务。在创建捆绑分发前，请阅读权威的 [FFmpeg](https://ffmpeg.org/legal.html)、[LibreOffice](https://www.libreoffice.org/licenses/)、[Ghostscript](https://www.ghostscript.com/licensing/) 和 [MPL](https://www.mozilla.org/en-US/MPL/2.0/FAQ/) 材料。

Office 文档的转换保真度取决于字体和资源。PDF 转 Word 会导出提取的文本；PDF 转 PowerPoint 会创建图像幻灯片。PDF 修复会尽力进行，但不保证成功；压缩为无损压缩。[PDF/A 转换与验证](pdfa.md) 通过共用 Python 适配器使用独立的 MPL 库，并包含已获许可的 ICC 配置文件。无需 Ghostscript。仍建议进行独立的标准合规验证。OCR 准确度取决于扫描质量和语言包。

<a id="developer-tools"></a>
## Developer tools

安装 Node.js 24+ 并运行 `onekit engines install` 来安装版本已锁定的 Prettier/插件、esbuild、HTML 压缩器、SVGO 和 GraphQL.js。它们会安装在用户的 OneKit 缓存中，而不是全局安装。`ONEKIT_NODE_ENGINE_PATH` 可选择替代方案。在经过批准的引擎更新后重新运行安装程序。解析器组涵盖 JS/TS/JSX/TSX、标记语言、样式表、Markdown/MDX、GraphQL、Vue、Svelte、Astro、Solidity 和 PHP。

为您的操作系统安装上游编译器/启动器，并将文档中记录的命令添加到 PATH。某些独立文件需要其项目依赖或确切的 Java 类文件名。格式化/解析验证并不保证整个项目类型的正确性。

在 Windows 上，Bash/Shell 适配器优先使用 PATH 中的实际解释器，然后在其标准系统/用户安装目录中检测 Windows 的 Git。System32 WSL 启动器不被视为兼容的本地解析器。PowerShell 语法验证需要 `pwsh`；格式化还需要 PSScriptAnalyzer（`Install-Module PSScriptAnalyzer -Scope CurrentUser`）。`onekit doctor dev-format-powershell` 会单独检查该模块并报告其安装命令。这些程序/模块在处理文件时不会下载。

<a id="platform-qualifications"></a>
## Platform qualifications

CI 许可证检查还会安装并检查独立的签名扩展依赖组（`scripts/check_licenses.py --include-signing`）。MIT-0 被认可为宽松许可证（[SPDX 文本](https://spdx.org/licenses/MIT-0.html)）。固定版本 `certifi` 2026.7.22 中的 Mozilla 信任库数据属于明确的 MPL-2.0 例外，且此例外仅适用于该版本；重新分发这些数据时，必须原样保留其上游许可证和声明（[上游声明](https://github.com/certifi/python-certifi/blob/master/LICENSE)）。新版本需要重新审查。此例外并不普遍允许其他 MPL 软件包，也不会改变 OneKit 的 PolyForm-Shield-1.0.0 许可证。

通用 Python 核心支持 Linux、Windows 和 macOS，包括 ARM64。本地附加组件和外部引擎决定额外需求。CI 在三大操作系统家族上声明 x64/ARM 运行器。在 Windows ARM 上，Brotli/WOFF2 以及独立签名加密栈可能需要本地构建工具或在仿真下的 x64 Python。WOFF/TTF/OTF 不需要 WOFF2 编码器。`all` 附加组件不包括独立签名。应报告这些可选约束，而不是声称存在本地 wheel。
