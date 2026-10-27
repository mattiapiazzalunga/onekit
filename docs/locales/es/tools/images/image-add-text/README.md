<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="add-text-to-image"></a>
# Agregar texto a la imagen

Comando: `onekit run image-add-text`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Imágenes**. Fidelidad: **con limitaciones**. Agrega texto de Europa Occidental a un nuevo PNG con tamaño, color y posición ajustables. La animación y los metadatos no se conservan.

Tipos admitidos: `png, jpeg, webp, gif, bmp, tiff, ico`. Tipo de salida: `png`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `text`, `font_size`, `color`, `position`, `margin`, `x`, `y`, `text_boxes`.

Paquetes Python: Pillow. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/image_text.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
