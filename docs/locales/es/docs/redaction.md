<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="permanent-redaction"></a>
# Censura permanente

<a id="pdf"></a>
## PDF

Cada página se renderiza, los píxeles seleccionados se reemplazan con negro opaco y se construye un nuevo PDF a partir de las imágenes ya censuradas. Ningún objeto original PDF se copia. Esto elimina el texto seleccionable original, las capas OCR, capas ocultas, campos de formulario, objetos de anotación/comentario, enlaces, scripts, archivos adjuntos, metadatos, miniaturas e historial de guardado incremental del resultado. Las apariencias de anotaciones visibles se aplanan en píxeles para que una anotación opaca existente no revele inesperadamente el contenido que cubría. Revisa la vista previa para diferencias en la apariencia de campos/anotaciones; no se retienen objetos interactivos. El contenido visible de la página no seleccionado permanece como píxeles.

<a id="images"></a>
## Images

Los píxeles se reemplazan con negro sólido antes de codificar un nuevo RGB PNG opaco. No hay superposición removible, capa original ni datos de píxeles originales sin enmascarar en las regiones codificadas. Fuente EXIF, GPS, XMP, comentarios, perfiles, miniaturas y otros metadatos originales no se copian. La transparencia se mezcla con blanco, descartando valores RGB ocultos bajo los píxeles transparentes. Se aplica la orientación EXIF antes de interpretar las áreas. Entradas animadas y con múltiples fotogramas son rechazadas para que los fotogramas extra no puedan quedar sin censurar; exporta un fotograma primero.

<a id="cli-and-workflows"></a>
## CLI and workflows

Instala `onekit-tools[pdf]` para la censura permanente de PDF o `onekit-tools[images]` para imágenes. Ambas herramientas aceptan `regions`, un array de rectángulos, opcionalmente serializado como una cadena JSON. Cada rectángulo especifica `page` (numeración desde 1, valor predeterminado 1), `x`, `y`, `width`, `height`. Las coordenadas son fracciones de la página/imagen vista visualmente con el origen en la parte superior izquierda: `0.1` significa 10%. Para imágenes, `page` debe ser 1. Se pueden seleccionar hasta 500 rectángulos. Los límites deben caber dentro de la página; los límites de las máscaras se redondean hacia fuera y se amplían en un píxel de salida para cubrir las fracciones de píxel en los bordes.

```sh
onekit run pdf-redact private.pdf -o redacted.pdf --options '{"regions":[{"page":1,"x":0.1,"y":0.2,"width":0.5,"height":0.1}],"dpi":200}'
onekit run image-redact private.jpg -o redacted.png --options '{"regions":[{"x":0.2,"y":0.2,"width":0.3,"height":0.2}]}'
```
