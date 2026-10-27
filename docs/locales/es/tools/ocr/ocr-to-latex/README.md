<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="ocr-to-latex"></a>
# OCR a LaTeX

Comando: `onekit run ocr-to-latex`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **OCR**. Fidelidad: **con limitaciones**. El reconocimiento depende de la calidad del escaneo y de los paquetes de idiomas instalados. Las ecuaciones y el diseño pueden necesitar corrección manual.

Tipos admitidos: `pdf, png, jpeg, webp, gif, bmp, tiff, ico`. Tipo de salida: `latex`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `language`, `dpi`.

Paquetes Python: pytesseract, Pillow, pypdfium2, python-docx. Motores externos: tesseract.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/ocr/__init__.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
