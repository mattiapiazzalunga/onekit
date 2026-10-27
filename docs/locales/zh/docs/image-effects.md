<a id="image-effects"></a>
# 图片效果

```sh
onekit run image-effects photo.jpg --options '{"effect":"pixelate","strength":16}' -o output
onekit run image-effects photo.jpg --options '{"effect":"blur","strength":12,"scope":"selected","regions":[{"x":0.1,"y":0.2,"width":0.3,"height":0.25}]}' -o output
```

`strength` 是一个整数，范围从 1 到 100 像素（像素化至少为 2）。`scope` 可以是 `all`（默认）或 `selected`；所选模式需要 1–500 个矩形，使用归一化的 0–1 坐标，并可选 `page: 1`。`color` 使用 `#RRGGBB` 来进行实心覆盖。强度对灰度或实心覆盖没有影响。重叠区域从原始像素处理，不会累积模糊。最多处理 8000万选定像素，包括重叠部分。

模糊和像素化只是视觉效果，无法保证去除敏感细节。如果必须以不可恢复的方式覆盖内容，请使用图片永久遮盖工具。
