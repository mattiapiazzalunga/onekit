# Image effects

```sh
onekit run image-effects photo.jpg --options '{"effect":"pixelate","strength":16}' -o output
onekit run image-effects photo.jpg --options '{"effect":"blur","strength":12,"scope":"selected","regions":[{"x":0.1,"y":0.2,"width":0.3,"height":0.25}]}' -o output
```

`strength` is an integer from 1 to 100 pixels (at least 2 for pixelation).
`scope` is `all` (default) or `selected`; selected mode requires 1–500 rectangles
with normalized 0–1 coordinates and optional `page: 1`. `color` uses `#RRGGBB`
for solid cover. Intensity has no effect on grayscale or solid cover.
Overlapping areas are processed from original pixels, without cumulative blur.
At most 80 million selected pixels are processed, counting overlaps.

Blur and pixelation are visual effects and cannot guarantee removal of sensitive
details. Use permanent image redaction when content must be irrecoverably covered.
