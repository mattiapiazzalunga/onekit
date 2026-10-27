<a id="image-effects"></a>
# Bildeffekte

```sh
onekit run image-effects photo.jpg --options '{"effect":"pixelate","strength":16}' -o output
onekit run image-effects photo.jpg --options '{"effect":"blur","strength":12,"scope":"selected","regions":[{"x":0.1,"y":0.2,"width":0.3,"height":0.25}]}' -o output
```

`strength` ist eine ganze Zahl von 1 bis 100 Pixel (mindestens 2 für Pixelierung). `scope` ist `all` (Standard) oder `selected`; der gewählte Modus erfordert 1–500 Rechtecke mit normalisierten 0–1-Koordinaten und optionalem `page: 1`. `color` verwendet `#RRGGBB` für eine vollständige Abdeckung. Die Intensität hat keinen Einfluss auf Graustufen oder vollständige Abdeckung. Überlappende Bereiche werden aus den Originalpixeln verarbeitet, ohne kumulativen Weichzeichner. Es werden höchstens 80 Millionen ausgewählte Pixel verarbeitet, inklusive Überlappungen.

Weichzeichnung und Verpixelung sind visuelle Effekte und können die Entfernung sensibler Details nicht garantieren. Verwenden Sie dauerhaftes Schwärzen von Bildern, wenn Inhalte unwiederherstellbar verdeckt werden müssen.
