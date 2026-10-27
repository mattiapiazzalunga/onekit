<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="permanently-redact-image"></a>
# Censurar una imagen de forma permanente

Comando: `onekit run image-redact`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Imágenes**. Fidelidad: **con limitaciones**. Sustituye los píxeles seleccionados por negro sólido y exporta un nuevo PNG opaco, sin metadatos originales ni píxeles ocultos por la transparencia. Solo admite imágenes de un fotograma. El archivo original no se modifica.

Tipos admitidos: `png, jpeg, webp, gif, bmp, tiff, ico`. Tipo de salida: `png`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `regions`.

Paquetes Python: Pillow. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/redaction.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
