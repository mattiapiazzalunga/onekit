<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="permanently-redact-pdf"></a>
# Censurar un PDF de forma permanente

Comando: `onekit run pdf-redact`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **PDF**. Fidelidad: **con limitaciones**. Oculta de forma permanente las áreas seleccionadas y reconstruye cada página a partir de píxeles rasterizados. No se copian el texto, los adjuntos, los comentarios, los formularios ni los metadatos originales; se pierden el texto seleccionable y la calidad vectorial. El archivo original no se modifica.

Tipos admitidos: `pdf`. Tipo de salida: `pdf`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `regions`, `dpi`.

Paquetes Python: pypdfium2, Pillow, reportlab, pypdf. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/redaction.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
