<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="pdf-watermark"></a>
# Marca de agua PDF

En la categoría PDF, sube un PDF, ingresa texto y ajusta la opacidad, color, fuente, rotación y posición. La vista previa muestra la posición de la marca de agua en la página elegida. Exporta para inspeccionar la renderización final de la fuente PDF. Elige una sola marca de agua o una cuadrícula repetida de 3 × 4. El texto se reduce automáticamente cuando es necesario para ajustarse a la página o celda, hasta un límite de legibilidad de seis puntos. Los PDFs encriptados deben desbloquearse primero. Las firmas digitales existentes ya no se verifican después de modificar un documento; la herramienta avisa cuando hay campos de firma presentes.

```sh
onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"CONFIDENTIAL","pages":"1,3-5","opacity":0.25,"angle":45}'
onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"DRAFT","layout":"repeat","color":"#b00000"}'
```

| Opción | Valores / por defecto |
| --- | --- |
| `text` | 1–200 caracteres, hasta cinco líneas; por defecto BOCETO |
| `pages` | Rangos empezando en uno, p.ej. `1,3-5`; vacío u omitido significa todos |
| `font` | Helvetica-Negrita (predeterminado), Helvetica, Times-Roman, Courier |
| `font_size` | 8–160 puntos; predeterminado 48, ajustado automáticamente cuando sea necesario |
| `color` | Hexadecimal de seis dígitos; predeterminado #666666 |
| `opacity` | 0.05–1; por defecto 0.25 |
| `angle` | -180–180 grados, en sentido antihorario; 45 por defecto |
| `position` | centro, superior-izquierda/centro/derecha, medio-izquierda/derecha, inferior-izquierda/centro/derecha |
| `layout` | único (predeterminado) o repetir (3 × 4 cuadrícula; la posición se ignora) |
| `margin` | 0–144 puntos; por defecto 24 |

Las fuentes son compatibles con caracteres y puntuación de Europa Occidental, incluidos acentos italianos. Los caracteres no compatibles fallan explícitamente. Se pueden procesar hasta 512 páginas. La colocación usa la caja de recorte orientada visualmente, manteniendo la rotación original y las coordenadas de anotación. Una marca de agua etiqueta el contenido visible; no elimina el contenido subyacente.
