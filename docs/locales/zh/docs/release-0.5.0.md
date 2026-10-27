<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="onekit-050"></a>
# OneKit 0.5.0

离线 CLI 和 Python 处理 API 的初始版本，提供 230 个工具处理文档、PDF、图片、媒体、压缩文件、字体、开发者工具、二维码、许可证声明和文件检查。基础安装没有运行时依赖项；可选附加组件和外部引擎可以启用所选工具。

包括有限输入验证、可复用工作流、本地依赖设置、特定格式的处理合同和基于源的许可证检查。许可证报告仍然是未经验证的估计，需要手动审核。

性能更新加快了不透明图像的准备和文本检查。已删除未使用的导入和多余的开发者引擎分配。

模型引擎是可选的：在需要时安装 `background` 或 `transcription` 扩展。U2Net 可直接在 ONNX 运行时和经过校验和验证的缓存模型上运行。Whisper 使用 faster-whisper。文件保持本地；首次运行会下载模型权重。视频处理需要 FFmpeg 和 ffprobe。视频下载使用单独的 `video` 扩展。

将 Pillow 更新至版本 13，并更新锁定的 certifi 版本，以修复已发布公告中报告的问题。可跨平台使用的可选依赖组 `all` 仍与模型引擎和签名功能分开。
