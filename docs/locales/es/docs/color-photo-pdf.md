<a id="color-photo-restoration-and-pdf-forms"></a>
# Colores, restauración de fotos y formularios PDF

Estas herramientas se exponen a través del comando estándar `onekit run TOOL ... --options JSON` y los Python `execute` API. Consulta `onekit run --help` para los argumentos de entrada/salida. Todas las coordenadas abajo se refieren a la imagen después de la orientación EXIF o a la página mostrada PDF después de la rotación.

- `color-picker`: inspecciona un archivo UTF-8 que contiene `#RRGGBB`, o toma una muestra de una imagen con coordenadas enteras de píxel `x` e `y` (en el centro por defecto). Reporta HEX, RGB, OKLCH, contraste de texto negro/blanco y RGBA original para imágenes. Los colores visibles se componen sobre blanco.
- `image-extract-colors`: `colors` (2–32, por defecto 6). Cuantización por corte mediano de una miniatura limitada a 256 × 256. Los píxeles totalmente transparentes se excluyen; el alfa parcial se compone sobre blanco. Las fracciones describen esta muestra.
- `jpg-to-svg`: `colors` (2–32, por defecto 16), `resolution` (32–512, por defecto 256). Cuantiza una imagen limitada, combina tiras horizontales de color igual de manera vertical y escribe rutas SVG llenas. No se incrusta ningún mapa de bits. Esto produce mosaicos vectoriales con un aspecto posterizado, no un trazado de curvas suaves.
- `image-repair`: sin `regions`, aplica un filtro de mediana de `size` 3 o 5 a motas aisladas. Con regiones, reconstruye los píxeles seleccionados usando los píxeles circundantes fijos y difusión armónica discreta (`iterations` 10–500, por defecto 200).
- `image-remove-watermark`: requiere `regions`; usa la misma reconstrucción local. Estima los píxeles faltantes y no puede recuperar contenido original oculto. La textura, marcas grandes y fondos complejos pueden dar resultados pobres.
- `image-sharpen`: `method` puede ser `unsharp` (predeterminado) o `deconvolution`. `radius`, entre 0.3 y 5, establece el radio de la máscara de enfoque o la dispersión gaussiana estimada de un punto. Para la máscara de enfoque, `amount` va de 0 a 300 por ciento (150 por defecto). Richardson–Lucy utiliza de 1 a 30 `iterations` (10 por defecto), extensión de bordes por reflexión y convolución FFT, con un máximo de un millón de píxeles de origen. Presupone un desenfoque gaussiano y no corrige movimientos arbitrarios. Ambos métodos pueden amplificar el ruido y los halos.
- `pdf-remove-watermark`: por defecto, `mode: "remove"` elimina los grupos `/Artifact` etiquetados como `/Subtype /Watermark` (incluyendo recursos de propiedades con nombre) y las anotaciones `/Watermark`. Opcionalmente, `text` coincide con objetos de texto completo con espacios normalizados, decodificando glifos a través de su codificación de fuente/mapa ToUnicode. Los Form XObjects anidados se procesan de forma recursiva. Usa `mode: "inspect"` para obtener un informe JSON de IDs de texto, imagen e invocación de Form XObject; pasa los IDs seleccionados como `objects` en modo de eliminación. Seleccionar un objeto Form XObject elimina todo su grupo gráfico. Los objetos Form XObject modificados se copian por invocación, así que los usos no seleccionados de un recurso compartido permanecen sin cambios. Los IDs se refieren al mismo PDF original y deben ser reinspeccionados después de los cambios. Esto es eliminación de objetos de dibujo, no una censura segura de datos: los objetos de recursos no usados pueden permanecer en el resultado. No identifica automáticamente contenido arbitrario sin etiquetar como marca de agua, y una marca fusionada en una imagen escaneada no se puede separar de esa imagen. Un informe contiene hasta 2000 elementos candidatos, la recursión está limitada a 12 niveles y el procesamiento a 300 000 operaciones gráficas. Si no se encuentra ninguna coincidencia, se genera un error explícito.
- `pdf-make-fillable`: `fields` es un array JSON de componentes AcroForm estándar. Cada componente tiene un `name` ASCII único, un `type` (`text`, `checkbox`, `choice`), una `page` numerada desde 1 y coordenadas normalizadas `x`, `y`, `width`, `height`. Se admiten el parámetro opcional `required`, `multiline` para texto y `choices` para las opciones de selección. Se conservan los campos existentes y el contenido de las páginas. Se rechazan los nombres duplicados, los PDF cifrados y XFA. No hay detección automática de espacios en blanco.

Las regiones de la imagen son arreglos de objetos como `{"page":1,"x":0.2,"y":0.3,"width":0.1,"height":0.05}`. Las coordenadas están normalizadas a 0–1 desde la esquina superior izquierda. La reconstrucción admite hasta 100 rectángulos, como máximo 35% de la imagen y una caja delimitadora (incluyendo el relleno) de un millón de píxeles. Solo RGB dentro de la máscara cambia; se mantiene el alfa original. Los resultados son PNG sin metadatos de origen. Las imágenes animadas/multicuadro son rechazadas. La decodificación general de imágenes está limitada a 40 millones de píxeles. Los PDFs están limitados a 256 páginas y los formularios a 200 campos nuevos.

Ejemplo de uso de Python:

```python
from onekit import Artifact, execute

result = execute("pdf-make-fillable", [Artifact("source.pdf", pdf_bytes)], {
    "fields": [{"name": "Name", "type": "text", "page": 1,
                "x": 0.1, "y": 0.2, "width": 0.4, "height": 0.05}]
})
```

Revisa los archivos resultantes y conserva los originales. Se necesita un lector PDF compatible para llenar y guardar formularios.
