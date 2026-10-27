<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="upscale-image"></a>
# Mejorar imagen

Comando: `onekit run image-upscale`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Imágenes**. Fidelidad: **con limitaciones**. Amplía una imagen de un solo fotograma 2×, 3× o 4× con remuestreo Lanczos. No reconstruye detalles mediante inteligencia artificial. Exporta PNG, hasta 40 millones de píxeles de salida.

Tipos admitidos: `png, jpeg, webp, gif, bmp, tiff, ico`. Tipo de salida: `png`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `scale`.

Paquetes Python: Pillow. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/image_upscale.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
