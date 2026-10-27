<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="pdf-watermark"></a>
# PDF 水印

在 PDF 类别中，上传一个 PDF，输入文本并调整不透明度、颜色、字体、旋转和位置。预览显示所选页面上的水印位置。导出以检查最终 PDF 字体渲染。选择单个水印或重复的 3 × 4 网格。文本会在需要时自动缩小，以适应页面或单元格，最小字号为 6 磅，以保持可读性。加密的 PDF 必须先解锁。修改文档后，现有数字签名不再有效；工具会在存在签名字段时发出警告。

```sh
onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"CONFIDENTIAL","pages":"1,3-5","opacity":0.25,"angle":45}'
onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"DRAFT","layout":"repeat","color":"#b00000"}'
```

| 选项 | 值 / 默认值 |
| --- | --- |
| `text` | 1–200 字符，最多五行；默认 DRAFT |
| `pages` | 从1开始的范围，例如 `1,3-5`；为空或省略表示全部 |
| `font` | Helvetica-Bold（默认）、Helvetica、Times-Roman、Courier |
| `font_size` | 8–160 点；默认 48，必要时自动适配 |
| `color` | 六位十六进制；默认 #666666 |
| `opacity` | 0.05–1; 默认 0.25 |
| `angle` | -180–180 度，逆时针；默认 45 |
| `position` | center、top-left/center/right、middle-left/right、bottom-left/center/right |
| `layout` | single（默认）或 repeat（3 × 4 网格；位置被忽略） |
| `margin` | 0–144 点；默认 24 |

字体支持西欧字符和标点，包括意大利语重音符号。不支持的字符会明确报错。最多可以处理 512 页。排版使用可视化的裁剪框，保留原始旋转和注释坐标。水印标记可见内容，但不会移除底层内容。
