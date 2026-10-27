<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="input-validation"></a>
# Validación de entrada

Cada entrada del catálogo declara los formatos aceptados, el número de archivos y los límites de bytes. `onekit list --json` expone los valores. Tanto la ejecución directa como los pipelines hacen cumplir los contratos.

<a id="limits"></a>
## Limits

Los límites globales por lote son 128 MiB y 256 archivos. Las entradas de texto están limitadas a 8 MiB por archivo, las imágenes ráster a 64 MiB y las fuentes a 16 MiB. Una comparación requiere exactamente dos entradas. Las imágenes ráster decodificadas están limitadas a 40 millones de píxeles sumando todos los fotogramas. El contenido descomprimido de archivos y documentos de Office está limitado a 128 MiB y 4096 entradas.

Las herramientas de entrada única rechazan archivos extra. La asignación de la tubería aplica deliberadamente un paso de entrada única a cada salida anterior. Las colecciones de salida se verifican de forma incremental para que un paso mapeado no pueda acumular datos devueltos ilimitados. Se verifican los recuentos de archivos CLI, extensiones y tamaños antes de leer el contenido de los archivos, y los bytes leídos se limitan incluso si un archivo crece durante la lectura.

<a id="content-rules"></a>
## Content rules

- Las herramientas PDF requieren cabeceras PDF y una ubicación final coherente de referencias cruzadas. `pdf-repair` permite deliberadamente referencias cruzadas dañadas después de verificar la cabecera PDF; su analizador todavía tiene que recuperar un PDF real. Las imágenes renombradas a `.pdf` son rechazadas.
- Las entradas raster se verifican con Pillow para formato real, estructura y dimensiones decodificadas. Un PNG renombrado a JPEG es rechazado. La exportación Base64 también decodifica la imagen antes de aceptarla.
- Word, Excel y PowerPoint requieren partes de contenedor ZIP distintas y raíces con espacio de nombres XML. Renombrar Excel a `.docx` no lo convierte en Word. Se revisan los recuentos de directorios y los presupuestos de expansión antes de asignar la tabla de entradas ZIP o leer partes del documento.
- Las fuentes requieren encabezados SFNT/WOFF coincidentes, rangos de tablas válidos y limitados, y tamaños coherentes de fuentes comprimidas. La expansión declarada WOFF no puede exceder el presupuesto de bytes de la fuente.
- Las entradas de medios tienen extensiones de audio/video explícitas y firmas de contenedor. FFprobe verifica los tipos de flujo antes de la conversión FFmpeg; la conversión de video requiere video, y la conversión de audio requiere audio sin flujos de video ordinarios. Se permite el arte de portada adjunto. Ambos ejecutables son reportados por `doctor`.
- Los archivos rechazan rutas inseguras/duplicadas, enlaces simbólicos, entradas ZIP cifradas, directorios inválidos, directorios de múltiples volúmenes/ZIP64 y flujos comprimidos concatenados no soportados. Las proporciones de expansión ZIP están limitadas. La descompresión TAR está limitada antes del análisis de miembros/PAX, con un permiso adicional fijo 4 MiB para encabezados/relleno TAR; la memoria del decodificador XZ también es limitada.
- El descifrado acepta solo el formato cifrado OneKit y autentica su contenido antes de la restauración del archivo limitado. Las opciones del usuario no pueden aumentar el presupuesto de expansión impuesto.
- Las herramientas de texto requieren texto decodificable sin bytes de control binarios. Las herramientas de desarrollo aceptan sus extensiones de lenguaje y la entrada neutral `.txt`; los adaptadores de shell/Dockerfile también permiten código fuente sin extensión. Las herramientas de validación aceptan intencionalmente código fuente sintácticamente inválido y devuelven `valid: false`. La conversión de codificación utiliza la codificación de origen seleccionada; otras herramientas de texto requieren UTF-8..
- La inspección, los adaptadores de metadatos y la encriptación aceptan intencionalmente tipos de archivos arbitrarios. Sus límites de cantidad/bytes todavía se aplican. Inspeccionar un archivo dañado o desconocido es una operación soportada, en lugar de una razón para rechazarlo solo por su contenido.
