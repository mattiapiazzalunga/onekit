<a id="color-photo-restoration-and-pdf-forms"></a>
# 颜色、照片修复和 PDF 表单

这些工具可以通过标准的 `onekit run TOOL ... --options JSON` 命令以及 Python `execute` API 来访问。关于输入/输出参数，请参见 `onekit run --help`。下面所有的坐标都指图像在 EXIF 定向后的状态，或者旋转后显示的 PDF 页面。

- `color-picker`：检查包含 `#RRGGBB` 的 UTF-8 文件，或者用整数像素坐标 `x` 和 `y` 对图像进行采样（默认居中）。报告 HEX、RGB、OKLCH、黑白文字对比度以及图像的原始 RGBA。可见颜色在白色背景上合成。
- `image-extract-colors`：`colors`（2–32，默认 6）。对限定在 256 × 256 的缩略图进行中值分割量化。完全透明的像素会被排除；部分透明的像素会在白色上合成。分数描述了这个样本。
- `jpg-to-svg`: `colors`（2–32，默认 16），`resolution`（32–512，默认 256）。对有界图像进行量化，垂直合并水平同色区块，并写入填充的 SVG 路径。不嵌入位图。这将生成带有色阶分离效果的矢量瓦片，而不是平滑曲线追踪。
- `image-repair`：如果没有 `regions`，会对孤立的斑点应用 `size` 3 或 5 的中值滤波。有区域时，使用固定的周围像素和离散谐波扩散 (`iterations` 10–500，默认 200) 来重建选定的像素。
- `image-remove-watermark`：需要 `regions`；使用相同的本地重建方法。它会估算缺失的像素，但无法恢复被隐藏的原始内容。纹理、大的标记和复杂背景可能会导致效果不佳。
- `image-sharpen`：`method` 为 `unsharp`（默认）或 `deconvolution`。`radius` 的范围为 0.3–5，用于设置 USM 锐化半径或估计的高斯点扩散范围。USM 锐化的 `amount` 为 0–300 百分比（默认 150）。Richardson–Lucy 使用 1–30 次 `iterations`（默认 10），采用反射边界填充和 FFT 卷积，最多处理一百万个源像素。该方法假设存在高斯模糊，不能校正任意运动造成的模糊。两种方法都可能放大噪点和光晕。
- `pdf-remove-watermark`：默认情况下，`mode: "remove"` 会移除标记为 `/Subtype /Watermark` 的 `/Artifact` 组（包括具名属性资源）和 `/Watermark` 注释。可选参数 `text` 会在规范化空白后匹配完整的文本对象，通过它们的字体编码/ToUnicode 映射解码字形。嵌套的 Form XObjects 会递归处理。使用 `mode: "inspect"` 可以获取文本、图像和 Form XObject 调用 ID 的 JSON 报告；在删除模式下，将选定的 ID 作为 `objects` 传入。选择一个 Form XObject 会移除其整个图形组。修改后的 Form 对象会按每次调用分别复制，因此共享资源中未选中的调用保持不变。ID 指向同一个原始 PDF，并且在更改后必须重新检查。 这是绘图对象的移除，而不是安全的永久遮盖：未使用的资源对象可能仍会保留在输出中。它不会自动将任意未标记的内容识别为水印，而且融合到扫描图像中的标记无法从该图像中分离。报告最多包含 2,000 个候选项，递归限制为 12 层，处理限制为 300,000 个绘图操作。零匹配会产生明确错误。
- `pdf-make-fillable`：`fields` 是标准 AcroForm 控件的 JSON 数组。每个控件具有唯一的 ASCII 名称 `name`、类型 `type`（`text`、`checkbox`、`choice`）、从 1 开始编号的 `page`，以及归一化坐标 `x`、`y`、`width`、`height`。支持可选的 `required`、文本的 `multiline` 和选择控件的 `choices`。保留现有字段和页面内容。拒绝重复名称、加密 PDF 和 XFA。不自动检测空白区域。

图像区域是像 `{"page":1,"x":0.2,"y":0.3,"width":0.1,"height":0.05}` 这样的对象数组。坐标从左上角归一化到 0–1。重建最多支持 100 个矩形，占图像的最多 35%，以及一个总像素数为一百万的边界框（包括填充）。仅 RGB 内部的内容会变化；保留原始 alpha。输出为 PNG，不包含源元数据。动画/多帧图像会被拒绝。通用图像解码限制为 4000万像素。PDF 限制为 256 页，表单限制为 200 个新字段。

Python 使用示例：

```python
from onekit import Artifact, execute

result = execute("pdf-make-fillable", [Artifact("source.pdf", pdf_bytes)], {
    "fields": [{"name": "Name", "type": "text", "page": 1,
                "x": 0.1, "y": 0.2, "width": 0.4, "height": 0.05}]
})
```

查看生成的文件并保留原件。需要兼容的 PDF 阅读器来填写和保存表格。
