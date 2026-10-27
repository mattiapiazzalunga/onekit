<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="permanent-redaction"></a>
# 永久遮盖

<a id="pdf"></a>
## PDF

每一页都会被渲染，选中的像素会被替换为不透明的黑色，并且会从已经遮盖敏感内容的图像中重新构建一个新的 PDF。不会复制任何原始的 PDF 对象。这会从输出中移除原始的可选文本、OCR 图层、隐藏图层、表单字段、注释/评论对象、链接、脚本、附件、元数据、缩略图和增量保存历史。可见的注释外观会被展平为像素，这样已有的不透明注释就不会意外地显示它覆盖的内容。请检查预览，确认字段/注释外观的差异；不会保留任何交互对象。未选中的可见页面内容保持为像素。

<a id="images"></a>
## Images

在编码新的不透明 RGB PNG 之前，像素会被替换为纯黑色。编码区域中没有可移除的覆盖层、原始图层或原始未遮罩的像素数据。源 EXIF、GPS、XMP、评论、配置文件、缩略图和其他原始元数据不会被复制。透明度会合成到白色上，丢弃透明像素下隐藏的 RGB 值。在解释区域之前会应用 EXIF 的方向。拒绝动画和多帧输入，因此额外帧不会保留未遮盖的敏感内容；请先导出一帧。

<a id="cli-and-workflows"></a>
## CLI and workflows

安装 `onekit-tools[pdf]` 来永久遮盖 PDF 内容，或安装 `onekit-tools[images]` 来处理图片。两个工具都接受 `regions`，即一个矩形数组，可选择性地序列化为 JSON 字符串。每个矩形都有 `page`（从 1 开始，默认 1）、`x`、`y`、`width`、`height`。坐标按页面或图片的显示方向计算，为尺寸的比例，原点在左上角：`0.1` 表示 10%。对于图片，`page` 必须是 1。最多可以选择 500 个矩形。边界必须在页面内；蒙版边界会向外取整，并向外扩展一个输出像素，以覆盖边缘处不足一个像素的部分。

```sh
onekit run pdf-redact private.pdf -o redacted.pdf --options '{"regions":[{"page":1,"x":0.1,"y":0.2,"width":0.5,"height":0.1}],"dpi":200}'
onekit run image-redact private.jpg -o redacted.png --options '{"regions":[{"x":0.2,"y":0.2,"width":0.3,"height":0.2}]}'
```
