<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="cli-reference"></a>
# CLI 参考

使用 `onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"CONFIDENTIAL","opacity":0.25}'` 添加 PDF 文字水印。请查看 [水印指南](watermark.md) 了解位置、旋转、页码范围和重复布局。

可通过 `onekit run pdf-redact` 和 `onekit run image-redact` 永久遮盖内容，使用 `regions` 指定选定区域。[永久遮盖指南](redaction.md)介绍坐标、栅格化以及导出文件的隐私保障。

使用 `onekit run dev-regex-test input.txt -o regex-results.json --options '{"pattern":"[0-9]+","flags":"g"}'` 测试 JavaScript 正则表达式。需要 Node.js；参考 [正则表达式测试指南](regex.md) 了解捕获、替换和执行限制。

标准条形码可通过 `onekit run text-to-barcode`、`onekit run scan-barcode` 和 `onekit run barcode-to-text` 使用。安装 `barcode` 或 `qrcode` 额外组件。查看 [条形码设置及支持的标准](qrcode.md#standard-linear-barcodes)。

`onekit --version` 报告核心版本。`python -m onekit` 调用相同的 CLI。

| 命令 | 行为 |
| --- | --- |
| `onekit list [--group GROUP] [--json]` | 查看工具、使用约定、可用性和保真度。 |
| `onekit doctor [TOOL_ID] [--json]` | 检查 Python 软件包、引擎及许可策略造成的阻止。 |
| `onekit run TOOL_ID INPUTS -o OUTPUT` | 处理文件；加密也支持目录。 |
| `onekit pipeline --steps WORKFLOW INPUTS -o OUTPUT` | 执行 JSON 文件中定义的 1–16 个有序工具步骤。 |
| `onekit engines install [--directory DIRECTORY]` | 安装锁定的 Node 开发者引擎；需要 Node/npm。 |
| `onekit download URL -o OUTPUT [--quality best\|720\|1080] [--force]` | 通过 yt-dlp 下载单个视频；需要网络和 FFmpeg。 |

`run` 接受 JSON 对象的 `--options`，以及 `--ask-password` 和 `--force`。流水线也支持密码提示和覆盖标志。对于单个输出使用文件名，多输出使用目录。没有扩展名的目标是目录。冲突的输出名称会被拒绝。

<a id="local-agents-and-automation"></a>
## Local agents and automation

**您的 CLI。您的智能代理 CLI。** OneKit 在终端使用非常有用，也可以作为本地 AI 代理的文件处理工具包，这些代理可以执行 shell 命令或启动子进程。代理可以发现工具契约，检查要求，运行所选操作并检查输出文件。

```sh
onekit list --json
onekit doctor pdf-merge --json
onekit run pdf-merge first.pdf second.pdf -o combined.pdf
onekit pipeline --steps workflow.1kit input.pdf -o output/
```

`list --json` 会显示工具ID、接受的输入、输出格式、选项、限制和保真度说明。`doctor TOOL_ID --json` 报告准备状态、缺失的依赖项和许可政策阻塞。解析这些 JSON 响应，而不是人类可读的列表。`run` 和 `pipeline` 会将结果写入 `-o` 提供的目标位置；它们没有通用的 `--json` 响应标志。有些工具会生成 JSON 报告文件。

对于本地代理，先发现工具，检查其要求，然后在需要的地方使用显式路径和 JSON 对象在 `--options` 中调用它。将子进程参数作为列表传递，以保留路径和 JSON，避免 shell 引号。使用输出前先检查退出状态：

| 退出代码 | 含义 |
| --- | --- |
| `0` | 命令已成功完成。 |
| `1` | `doctor` 发现缺少的要求或政策阻止；检查报告。 |
| `2` | 参数无效或处理/输入/输出错误；请查看 stderr。 |
| `130` | 命令已通过键盘中断取消。 |

为每个任务选择一个新的输出路径；现有输出会保留，除非提供 `--force`。`--ask-password` 需要交互式终端。在无人值守运行前准备好依赖项和模型缓存：缺少组件可能触发自动设置和网络下载，并且一些本地安装程序需要交互或提升权限。网络工具也会访问它们请求的资源。

文件处理在您的机器上运行。如果代理使用远程模型，代理对文件内容和命令结果的处理决定了会发送给该提供商的内容。同样的 [PolyForm Shield 许可 ](licenses.md) 适用于代理驱动使用。

<a id="tool-options"></a>
## Tool options

QR 生成、vCard/Wi-Fi 配置、图像扫描和反向解码在 [二维码指南](qrcode.md) 中有记录。安装 `qrcode` 扩展，然后使用 `onekit run text-to-qrcode input.txt -o code.png` 或 `onekit run scan-qrcode photo.jpg -o decoded.json`。

页码从 1 开始。`pages` 接受页码和递增范围，例如 `1,3-5`。整理和提取操作会保留指定顺序及有意重复的页面。旋转角度必须为 90 的倍数，默认应用于所有页面。PDF 编辑会在 `page` 页的 `x`/`y` 坐标处添加 `text`，坐标以 PDF 点为单位，原点位于左下角；现有内容不会重新排版。签名需要 PKCS#12 `certificate` 的路径及其 `password`。

图片 `format` 支持 PNG、JPEG、WebP、TIFF、BMP、ICO、GIF 和 PDF（视情况而定）。`quality` 是 1–100。`box` 的像素是 `[left, top, right, bottom]`。动画/元数据可能被移除；对于 JPEG/PDF，透明度会变为白色。压缩可能会增加已经优化的文件大小。

选项 `sheet` 用于选择工作表，默认是活动的工作表。Excel 读取使用缓存的公式值。JSON 到 Excel 期望的是一个对象数组。CSV `delimiter` 默认是逗号。类似公式的 XLSX 字符串会保持为文本；在电子表格应用中将不可信的 CSV 导入为文本。

编码转换接受 `source_encoding` 和 `encoding`。其他文本工具使用 UTF-8.。对于 PDF、JPEG 和 PNG，`metadata` 接受描述文本字段 `Title`、`Author`、`Subject`、`Keywords` 和 `Comment`。未指定的字段会保留；空字符串会清除字段的值。Python 辅助工具 `onekit.tools.file_metadata.read_metadata(artifact)` 可以读取这些字段而不修改资料，包括支持的 EXIF、PNG 文本和 XMP 值。其他元数据格式使用可选的 ExifTool 标签/值对，在其格式范围内。检查员签名并不能识别所有专有文件类型。

笔记本比较 `mode` 是 `both`、`markdown` 或 `code`。LaTeX 模式是 `all` 或启发式 `text`。PDF/Word 比较提取文本。Diff JSON 包含规范化的两端、修改过的代码块以及统一补丁，包括尾随新行差异。OCR `language` 使用已安装的 Tesseract 代码，`dpi` 是 36–300。PDF/A 转换需要授权的 `icc_profile`；请独立验证归档输出。

媒体选项包括 `format`、`codec` 和 `bitrate`，取决于 FFmpeg 构建版本。字体支持 `ttf`、`otf`、`woff` 和 `woff2`，同时保留轮廓技术。归档支持 ZIP 和 TAR/gzip/bzip2/xz 组合。

<a id="limits-and-errors"></a>
## Limits and errors

查看 [输入验证](input-validation.md)，了解每个工具类型、字节/计数限制、签名/容器检查和归档展开规则的强制要求。这些适用于直接的 Python API 调用以及每个管道步骤和 CLI。运行 `onekit list --json` 获取准确的机器可读合约。

核心输入上限：256 个文件、128 MiB。处理流水线：16 个步骤。图片和渲染页面：4000 万像素。对比：10 000 行、200 万字符。归档解压：128 MiB、4096 个条目，并检查解压膨胀比。外部引擎有超时限制。有效但体积较大的输入仍可能超出这些有意设置的限制。

退出代码：0 成功；1 doctor 诊断报告不完整；2 输入/处理错误；130 取消。验证器可以成功发出 `valid: false`：检查报告，而不是假设退出 0 就意味着源有效。类型/导入检查可能需要完整项目。Python 语法验证从不执行输入。

英语为默认语言。将来 CLI 的翻译使用 `onekit/locales` 下的 gettext 域 `onekit`；ID、命令名称和 JSON 键保持与语言无关。

笔记本合并接受 `merge` 与 `from`（`left` 或 `right`）以及以零为基准的已更改单元 `block` 索引，连同 `mode` 一起。它会输出更新后的目标笔记本并保留排除的单元格和笔记本元数据。统一的补丁描述了比较的表示，通常不是针对原始 PDF、Word 或笔记本容器的补丁。

<a id="image-effects"></a>
## Image effects

`onekit run image-effects photo.jpg --options '{"effect":"pixelate","strength":16}' -o output` 将模糊、像素化、方框模糊、实色覆盖和灰度组合在一个工具中。使用 `scope: "selected"` 配合标准化矩形 `regions` 来针对特定区域。有关所有选项和限制，请参阅 [图像效果指南](image-effects.md)。

<a id="portable-workflows"></a>
## Portable workflows

`onekit workflow export SOURCE -o workflow.1kit` 验证旧的步骤数组或工作流文档，并保存为可移植文档。`onekit workflow import workflow.1kit -o saved.1kit` 验证并保存导入的文档。两个命令都会忽略密码，并且在没有提供 `--force` 的情况下拒绝已存在的输出路径。这两个命令都不会处理文件。

使用 `onekit pipeline --steps saved.1kit INPUTS -o OUTPUT` 运行已导入的工作流。.1kit 扩展用于识别 OneKit 文档；旧版 .json 和 .onekit.json 工作流文件及步骤数组仍然受支持。工作流文档是 UTF-8 JSON，最多 1 MiB，结构如下：

```json
{
  "format": "onekit-workflow",
  "version": 1,
  "steps": [{"tool": "dev-format-json", "options": {}}]
}
```

<a id="automatic-setup"></a>
## Automatic setup

`onekit run`、`onekit download` 和 `onekit pipeline` 在处理之前会安装缺失的 Python 软件包和本地引擎。依赖项保存在用户 OneKit 缓存中，不会更改系统 Python 安装。Whisper 和 U2Net 模型会在首次使用时自动下载，并在以后的运行中缓存。OCR 语言数据会根据请求的语言获取。

第一次运行需要互联网连接和足够的磁盘空间。本地引擎通过私有的 micromamba 安装使用 conda-forge，或者对于那里没有的引擎使用系统包管理器；可用性取决于操作系统和架构。设置失败会以错误停止处理，并可以重试。`onekit doctor` 在不安装任何东西的情况下检查准备情况。`ONEKIT_CACHE` 更改设置缓存的位置。`ONEKIT_ALLOW_COPYLEFT=0` 继续阻止受限引擎。

<a id="local-license-and-copyright-estimates"></a>
## Local license and copyright estimates

`licenses` 组提供 `license-pdf`、`license-word`、`license-powerpoint`、`license-excel`、`license-video`、`license-audio`、`license-image`、`license-font`、`license-epub`、`license-code` 和 `license-dataset`。

```sh
onekit run license-image photo.jpg -o report.json
onekit run license-pdf --url https://example.org/document.pdf -o report.json
onekit run license-code project.zip -o report.json
onekit run license-code ./project -o report.json
onekit run license-code --url https://github.com/owner/repository --options '{"ref":"main"}' -o report.json
onekit run license-code --url https://gitlab.com/group/project -o report.json
onekit run license-dataset data.csv LICENSE metadata.json -o report.json
```

**每个结果都是未经验证的估算，需要手动核实。** 它列出了声明的元数据、版权声明、创作者名称、SPDX 语法以及与其位置对应的初步许可文本匹配。它从不认证所有权或授予使用作品的权限。缺失的声明从不意味着公共领域或可自由使用。创作者姓名不代表版权归属。请查看原始来源、完整条款和预期用途；项目依赖和资源可能有单独的许可。官方参考资料解释标准，而不是上传作品中声明的真实性或适用性。

<a id="downloads-image-transforms-and-url-inspection"></a>
## Downloads, image transforms and URL inspection

```sh
onekit run audio-download --url 'https://example.org/audio.flac' -o downloads/
onekit run audio-download --url 'https://example.org/audio.wav' --options '{"format":"mp3","quality":"320"}' -o downloads/
onekit run image-download --url 'https://example.org/photo.jpg' -o downloads/
onekit run image-rotate-flip photo.png --options '{"angle":"90","flip":"horizontal"}' -o rotated.png
onekit run url-inspect --url 'https://example.org/path?x=1#section' -o report.json
```

下载图像或音频文件并不授予重新分发或重用权利。

图像旋转首先应用 EXIF 方向，然后顺时针旋转 0/90/180/270 度，再在旋转后的坐标系中水平、垂直或同时进行翻转。它会导出一个 PNG，保留解码后的 RGBA 像素和透明度，但不包含元数据；动画和多页图像将被拒绝。最大限制为 4000万像素。

<a id="remove-text-formatting"></a>
### Remove text formatting

`onekit run text-strip-formatting document.docx -o plain.txt` 将 Word 正文导出为 UTF-8 TXT。TXT、HTML 和 Markdown 文件也受支持，最多可到 8 MiB。使用 `--options '{"input_format":"html"}'` 来解释存储在 TXT 文件中的 HTML。不执行 OCR。

<a id="contribute-to-onekit"></a>
## Contribute to OneKit

帮助建设 OneKit 的开放革命：为每个人提供日常工具，从动手任务到由本地 AI 代理运行的工作流程。贡献力量，让工具更高效、更有效：提升速度和内存使用，修复错误结果，增加回归示例，或者澄清文档和代理工作流程。

核心是开源的（PolyForm Shield 1.0.0）。请阅读 [贡献指南](https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md)，并在 [GitHub 问题列表](https://github.com/mattiapiazzalunga/onekit/issues) 中找到一个任务，或者在 [请求板](https://onekit.org/requests/) 上提出改进建议。

关于开源 (PolyForm Shield 1.0.0) 核心和贡献的问题：[developers@onekit.org](mailto:developers@onekit.org)。一般支持：[support@onekit.org](mailto:support@onekit.org)。
