<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-text-formatting"></a>
# Eliminar formato de texto

Comando: `onekit run text-strip-formatting`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Análisis**. Fidelidad: **con limitaciones**. Convierte texto pegado, archivos de texto UTF-8/UTF-16, HTML, Markdown o el texto principal de Word DOCX en un archivo UTF-8 TXT localmente. Elimina estilos, enlaces y marcas mientras conserva texto legible y saltos básicos de párrafo/tabla. El texto plano conserva la puntuación literal. Sin OCR; se omiten encabezados, pies de página, imágenes y comentarios DOCX. Hasta 8 MiB por entrada.

Tipos admitidos: `txt, html, md, docx`. Tipo de salida: `txt`. Admite varias entradas: **no**.

Validación de entrada: **cualquier tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **8 388 608 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `input_format`.

Paquetes Python: markdown-it-py, defusedxml. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/plain_text.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
