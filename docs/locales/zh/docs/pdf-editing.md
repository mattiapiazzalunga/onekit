<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="pdf-text-editing"></a>
# PDF 文本编辑

检查源文件以获取稳定的文本框 ID 和原始文本：

```python
from onekit.api import execute
from onekit.models import Artifact

source = Artifact("document.pdf", open("document.pdf", "rb").read())
inspection = execute("pdf-edit", [source], {"mode": "inspect"})
box = inspection.details["pages"][0]["runs"][0]
result = execute("pdf-edit", [source], {
    "edits": [{"page": 1, "id": box["id"], "original": box["text"], "text": "Updated text"}]
})
open("edited.pdf", "wb").write(result.files[0].data)
```

CLI 可以通过 `--options` 接受相同的选项对象。`edits` 可以是 JSON 数组或包含该数组的字符串。检查模式输出 `*.text-boxes.json`；编辑模式输出 `*.edited.pdf`。在检查和编辑之间保持原始 PDF 不变。过期的 ID、重复的编辑和不匹配的原始文本会被拒绝。

扫描件需要先进行 OCR。不支持直接编辑可重用 Form XObject 内的文本、单引号或双引号文本操作符、竖排文字以及用作裁剪蒙版的文本。字符映射不完整的字体也可能不可用。要插入的字符必须存在于原始字体映射中；引擎会报告不支持的字符，而不会在未提示的情况下更换字体。编辑仅限单行，不会重新排版段落。请使用专用的永久遮盖工具去除机密信息，包括批注、文档历史、元数据或其他 PDF 对象中的副本。

之前的 `text`、`x`、`y`、`page` 选项仍然可用于添加文本覆盖。提供 `edits` 可替换现有文本。
