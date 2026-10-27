<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="cli-reference"></a>
# Referencia de la CLI

Usa `onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"CONFIDENTIAL","opacity":0.25}'` para añadir una marca de agua de texto PDF. Consulta la [guía de marcas de agua](watermark.md) para posición, rotación, rangos de páginas y diseños repetidos.

La censura permanente está disponible mediante `onekit run pdf-redact` y `onekit run image-redact`, indicando las áreas seleccionadas en `regions`. La [guía de censura](redaction.md) explica las coordenadas, la rasterización y las garantías de privacidad de los archivos exportados.

Usa `onekit run dev-regex-test input.txt -o regex-results.json --options '{"pattern":"[0-9]+","flags":"g"}'` para probar expresiones regulares JavaScript. Requiere Node.js; consulta la [guía del comprobador de expresiones regulares](regex.md) para capturas, reemplazos y límites de ejecución.

Los códigos de barras estándar están disponibles mediante `onekit run text-to-barcode`, `onekit run scan-barcode` y `onekit run barcode-to-text`. Instala el grupo de dependencias opcionales `barcode` o `qrcode`. Consulta la [configuración de códigos de barras y los estándares compatibles](qrcode.md#standard-linear-barcodes).

`onekit --version` informa la versión central. `python -m onekit` invoca la misma CLI.

| Comando | Comportamiento |
| --- | --- |
| `onekit list [--group GROUP] [--json]` | Descubrir herramientas, contratos, disponibilidad y fidelidad. |
| `onekit doctor [TOOL_ID] [--json]` | Revisa paquetes, motores y bloques de política de licencia de Python. |
| `onekit run TOOL_ID INPUTS -o OUTPUT` | Procesa archivos; el cifrado también acepta carpetas. |
| `onekit pipeline --steps WORKFLOW INPUTS -o OUTPUT` | Ejecuta de 1 a 16 pasos ordenados, definidos en un archivo JSON. |
| `onekit engines install [--directory DIRECTORY]` | Instala los motores de desarrollo bloqueados Node; requiere Node/npm. |
| `onekit download URL -o OUTPUT [--quality best\|720\|1080] [--force]` | Descarga un solo video a través de yt-dlp; requiere internet y FFmpeg. |

`run` acepta `--options` con un objeto JSON, `--ask-password` y `--force`. Los pipelines también soportan el aviso de contraseña y la bandera de sobrescribir. Usa un nombre de archivo para una salida o un directorio para múltiples salidas. Los destinos sin extensión son directorios. Los nombres de salida en conflicto son rechazados.

<a id="local-agents-and-automation"></a>
## Local agents and automation

**Tu CLI. Tu CLI para agentes.** OneKit es útil tanto en tu terminal como kit de herramientas de procesamiento de archivos para agentes locales AI que pueden ejecutar comandos de shell o iniciar subprocesos. Un agente puede descubrir contratos de herramientas, verificar requisitos, ejecutar una operación seleccionada e inspeccionar sus archivos de salida.

```sh
onekit list --json
onekit doctor pdf-merge --json
onekit run pdf-merge first.pdf second.pdf -o combined.pdf
onekit pipeline --steps workflow.1kit input.pdf -o output/
```

`list --json` expone los IDs de las herramientas, entradas aceptadas, formatos de salida, opciones, límites y notas sobre la fidelidad. `doctor TOOL_ID --json` informa sobre la disponibilidad, dependencias faltantes y bloqueos por políticas de licencia. Analiza estas respuestas JSON en lugar de los listados legibles por humanos. `run` y `pipeline` escriben sus resultados en el destino proporcionado con `-o`; no tienen una bandera de respuesta `--json` general. Algunas herramientas generan archivos de informe JSON.

Para un agente local, descubre primero la herramienta, verifica sus requisitos y luego llámala con rutas explícitas y un objeto JSON en `--options` cuando sea necesario. Pasa los argumentos de subprocesos como una lista para conservar las rutas y JSON sin comillas de shell. Revisa el estado de salida antes de consumir los resultados:

| Código de salida | Significado |
| --- | --- |
| `0` | Comando completado con éxito. |
| `1` | `doctor` encontró requisitos faltantes o un bloqueo de política; revisa el informe. |
| `2` | Argumentos inválidos o un error de procesamiento/entrada/salida; lea stderr. |
| `130` | Comando cancelado mediante una interrupción de teclado. |

Elige una ruta de salida nueva para cada trabajo; los resultados existentes se conservan a menos que se proporcione `--force`. `--ask-password` requiere un terminal interactivo. Prepara las dependencias y cachés del modelo antes de ejecuciones automáticas: los componentes faltantes pueden activar la configuración automática y descargas de red, y algunos instaladores nativos requieren interacción o privilegios elevados. Las herramientas de red también contactan sus fuentes solicitadas.

El procesamiento de archivos se realiza en tu equipo. Si el agente usa un modelo remoto, la forma en que el agente maneja el contenido del archivo y los resultados de los comandos determina qué se envía a ese proveedor. La misma licencia [PolyForm Shield](licenses.md) aplica para el uso dirigido por el agente.

<a id="tool-options"></a>
## Tool options

La generación QR, la configuración vCard/Wi-Fi, el escaneo de imágenes y la decodificación inversa están documentados en la guía de código [QR](qrcode.md). Instala el extra `qrcode`, luego usa `onekit run text-to-qrcode input.txt -o code.png` o `onekit run scan-qrcode photo.jpg -o decoded.json`.

Las páginas se numeran a partir de 1. `pages` acepta números e intervalos ascendentes, como `1,3-5`. Las operaciones de organización y extracción conservan el orden y las repeticiones intencionadas. La rotación acepta múltiplos de 90 y se aplica a todas las páginas de forma predeterminada. La edición de PDF añade `text` a `page` en las coordenadas `x`/`y`, expresadas en puntos PDF desde la esquina inferior izquierda; no redistribuye el contenido existente. Para firmar se necesitan la ruta de un `certificate` PKCS#12 y su `password`.

La imagen `format` es compatible con PNG, JPEG, WebP, TIFF, BMP, ICO, GIF y PDF según corresponda. `quality` es 1–100. `box` es `[left, top, right, bottom]` en píxeles. La animación/metadatos pueden eliminarse; la transparencia se aplana a blanco para JPEG/PDF. La compresión puede aumentar un archivo ya optimizado.

La opción `sheet` selecciona una hoja de cálculo; por defecto se usa la activa. La lectura Excel utiliza valores de fórmulas en caché. JSON a Excel espera un arreglo de objetos. CSV `delimiter` predetermina la coma. Las cadenas tipo fórmula XLSX permanecen como texto; importa CSV no confiables como texto en aplicaciones de hoja de cálculo.

La conversión de codificación acepta `source_encoding` y `encoding`. Otras herramientas de texto usan UTF-8. Para PDF, JPEG y PNG, `metadata` acepta los campos de texto descriptivos `Title`, `Author`, `Subject`, `Keywords` y `Comment`. Los campos no especificados se conservan; una cadena vacía borra el valor de un campo. El ayudante Python `onekit.tools.file_metadata.read_metadata(artifact)` lee esos campos sin modificar el artefacto, incluyendo los textos EXIF, PNG y los valores XMP compatibles. Otros formatos de metadatos usan pares opcionales de etiqueta/valor ExifTool, dentro del alcance de su formato. Las firmas del inspector no identifican todos los tipos de archivos propietarios.

La comparación de cuadernos `mode` es `both`, `markdown` o `code`. El modo LaTeX es `all` o heurístico `text`. La comparación PDF/Word extrae texto. Diff JSON contiene los lados normalizados, bloques cambiados y un parche unificado, incluyendo diferencias de nueva línea al final. OCR `language` usa códigos Tesseract instalados y `dpi` es 36–300. La conversión PDF/A requiere un `icc_profile` con licencia; valida de manera independiente la salida archivada.

Las opciones de medios incluyen `format`, `codec` y `bitrate`, dependiendo de la versión FFmpeg. Las fuentes admiten `ttf`, `otf`, `woff` y `woff2`, preservando la tecnología de contorno. Los archivos admiten combinaciones ZIP y TAR/gzip/bzip2/xz.

<a id="limits-and-errors"></a>
## Limits and errors

Consulta [validación de entrada](input-validation.md) para ver los tipos aplicados por herramienta, límites de bytes/contador, verificaciones de firmas/contenedores y reglas de expansión de archivos. Esto se aplica a llamadas directas Python API y a cada paso del pipeline, así como al CLI. Ejecuta `onekit list --json` para obtener contratos exactos legibles por máquina.

Entradas del núcleo: 256 archivos y 128 MiB. Flujos de procesamiento: 16 pasos. Imágenes y páginas renderizadas: 40 millones de píxeles. Comparaciones: 10 000 líneas y 2 millones de caracteres. Descompresión de archivos: 128 MiB, 4096 entradas y comprobaciones de la relación de expansión. Los motores externos tienen límites de tiempo. Las entradas válidas de gran tamaño pueden superar estos límites deliberados.

Códigos de salida: 0 éxito; 1 informe de diagnóstico de doctor incompleto; 2 error de entrada/proceso; 130 cancelación. Los validadores pueden emitir con éxito `valid: false`: revisa el informe en lugar de asumir que 0 significa fuente válida. La comprobación de tipo/importación puede requerir un proyecto completo. La validación de sintaxis de Python nunca ejecuta la entrada.

El inglés es el predeterminado. Las futuras traducciones CLI usarán el dominio gettext `onekit` bajo `onekit/locales`; los ID, nombres de comandos y las claves JSON permanecen independientes del idioma.

La fusión de notebooks acepta `merge` con `from` (`left` o `right`) y el índice de celda cambiada basado en cero `block`, junto con `mode`. Emite el notebook de destino actualizado y conserva las celdas excluidas y los metadatos del notebook. Los parches unificados describen la representación comparada y generalmente no son parches para PDF, Word o contenedores de notebooks sin procesar.

<a id="image-effects"></a>
## Image effects

`onekit run image-effects photo.jpg --options '{"effect":"pixelate","strength":16}' -o output` combina desenfoque, pixelado, desenfoque de caja, cobertura de color sólido y escala de grises en una sola herramienta. Usa `scope: "selected"` con rectángulos de coordenadas normalizadas en `regions` para seleccionar áreas concretas. Consulta la [guía de efectos de imagen](image-effects.md) para conocer todas las opciones y los límites.

<a id="portable-workflows"></a>
## Portable workflows

`onekit workflow export SOURCE -o workflow.1kit` valida un array de pasos heredado o un documento de flujo de trabajo y guarda un documento portátil. `onekit workflow import workflow.1kit -o saved.1kit` valida y guarda un documento importado. Ambos comandos omiten contraseñas y rechazan rutas de salida existentes a menos que se suministre `--force`. Ninguno de los comandos procesa archivos.

Ejecuta un flujo de trabajo importado con `onekit pipeline --steps saved.1kit INPUTS -o OUTPUT`. La extensión .1kit identifica documentos OneKit; los archivos de flujo de trabajo heredados .json y .onekit.json y los arrays de pasos siguen siendo compatibles. Los documentos de flujo de trabajo son UTF-8 JSON, como máximo 1 MiB, con la siguiente estructura:

```json
{
  "format": "onekit-workflow",
  "version": 1,
  "steps": [{"tool": "dev-format-json", "options": {}}]
}
```

<a id="automatic-setup"></a>
## Automatic setup

`onekit run`, `onekit download` y `onekit pipeline` instalan los paquetes faltantes Python y los motores nativos antes de procesar. Las dependencias se mantienen en la caché de usuario OneKit, sin cambiar la instalación del sistema Python. Los modelos Whisper y U2Net se descargan automáticamente en el primer uso y se almacenan en caché para usos posteriores. Los datos de idioma OCR se obtienen para los idiomas solicitados.

La primera ejecución necesita una conexión a internet y suficiente espacio en disco. Los motores nativos usan conda-forge mediante una instalación privada de micromamba, o el gestor de paquetes del sistema para motores que no estén disponibles allí; la disponibilidad depende del sistema operativo y la arquitectura. Los fallos de configuración detienen el proceso con un error y se pueden reintentar. `onekit doctor` verifica la preparación sin instalar nada. `ONEKIT_CACHE` cambia la ubicación de la caché de configuración. `ONEKIT_ALLOW_COPYLEFT=0` sigue bloqueando motores restringidos.

<a id="local-license-and-copyright-estimates"></a>
## Local license and copyright estimates

El grupo `licenses` proporciona `license-pdf`, `license-word`, `license-powerpoint`, `license-excel`, `license-video`, `license-audio`, `license-image`, `license-font`, `license-epub`, `license-code` y `license-dataset`.

```sh
onekit run license-image photo.jpg -o report.json
onekit run license-pdf --url https://example.org/document.pdf -o report.json
onekit run license-code project.zip -o report.json
onekit run license-code ./project -o report.json
onekit run license-code --url https://github.com/owner/repository --options '{"ref":"main"}' -o report.json
onekit run license-code --url https://gitlab.com/group/project -o report.json
onekit run license-dataset data.csv LICENSE metadata.json -o report.json
```

**Cada resultado es una estimación no verificada que requiere verificación manual.** Enumera los metadatos declarados, avisos de copyright, nombres de los creadores, sintaxis SPDX y coincidencias tentativas de textos de licencia con sus ubicaciones. Nunca certifica la propiedad ni otorga permiso para usar una obra. La ausencia de declaraciones no significa que sea de dominio público o de libre uso. Los nombres de los creadores no prueban la titularidad del copyright. Revisa la fuente original, los términos completos y el uso previsto; las dependencias y los recursos del proyecto pueden tener licencias separadas. Las referencias oficiales explican estándares, no la autenticidad o aplicabilidad de las declaraciones en una obra subida.

<a id="downloads-image-transforms-and-url-inspection"></a>
## Downloads, image transforms and URL inspection

```sh
onekit run audio-download --url 'https://example.org/audio.flac' -o downloads/
onekit run audio-download --url 'https://example.org/audio.wav' --options '{"format":"mp3","quality":"320"}' -o downloads/
onekit run image-download --url 'https://example.org/photo.jpg' -o downloads/
onekit run image-rotate-flip photo.png --options '{"angle":"90","flip":"horizontal"}' -o rotated.png
onekit run url-inspect --url 'https://example.org/path?x=1#section' -o report.json
```

Descargar una imagen o archivo de audio no otorga derechos de redistribución o reutilización.

La rotación de imágenes aplica primero la orientación EXIF, rota en el sentido de las agujas del reloj 0/90/180/270 grados, luego refleja horizontalmente, verticalmente o ambos en el sistema de coordenadas rotado. Exporta un PNG preservando los píxeles RGBA decodificados y la transparencia sin metadatos; las imágenes animadas y de varias páginas son rechazadas. El límite es de 40 millones de píxeles.

<a id="remove-text-formatting"></a>
### Remove text formatting

`onekit run text-strip-formatting document.docx -o plain.txt` exporta el texto del cuerpo Word como UTF-8 TXT. También se admiten archivos TXT, HTML y Markdown, hasta 8 MiB. Usa `--options '{"input_format":"html"}'` para interpretar HTML almacenado en un archivo TXT. No se realiza ninguna OCR.

<a id="contribute-to-onekit"></a>
## Contribute to OneKit

Ayuda a construir la revolución abierta de OneKit: herramientas diarias para todos, desde tareas prácticas hasta flujos de trabajo manejados por agentes locales AI. Contribuye para hacer las herramientas más eficientes y efectivas: mejora la velocidad y el uso de memoria, corrige resultados incorrectos, agrega ejemplos de regresión o aclara la documentación y los flujos de trabajo de los agentes.

El núcleo es de código abierto (PolyForm Shield 1.0.0). Lee la [guía de contribución](https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md) y encuentra una tarea en [GitHub issues](https://github.com/mattiapiazzalunga/onekit/issues), o sugiere una mejora en la [panel de solicitudes](https://onekit.org/requests/).

Preguntas sobre el núcleo de código abierto (PolyForm Shield 1.0.0) y contribuciones: [developers@onekit.org](mailto:developers@onekit.org). Soporte general: [support@onekit.org](mailto:support@onekit.org).
