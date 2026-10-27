<a id="image-effects"></a>
# Efectos de imagen

```sh
onekit run image-effects photo.jpg --options '{"effect":"pixelate","strength":16}' -o output
onekit run image-effects photo.jpg --options '{"effect":"blur","strength":12,"scope":"selected","regions":[{"x":0.1,"y":0.2,"width":0.3,"height":0.25}]}' -o output
```

`strength` es un número entero de 1 a 100 píxeles (al menos 2 para pixelado). `scope` es `all` (predeterminado) o `selected`; el modo seleccionado requiere 1–500 rectángulos con coordenadas 0–1 normalizadas y `page: 1` opcional. `color` usa `#RRGGBB` para cobertura sólida. La intensidad no afecta el nivel de gris ni la cobertura sólida. Las áreas superpuestas se procesan a partir de los píxeles originales, sin desenfoque acumulativo. Se procesan como máximo 80 millones de píxeles seleccionados, contando las superposiciones.

El desenfoque y el pixelado son efectos visuales y no garantizan la eliminación de detalles sensibles. Usa la censura permanente de imágenes cuando el contenido deba quedar oculto de forma irreversible.
