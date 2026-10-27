<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-pdf-watermark"></a>
# Quitar marca de agua PDF

Comando: `onekit run pdf-remove-watermark`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **PDF**. Fidelidad: **con limitaciones**. Examina y elimina el texto, las imágenes y las invocaciones de Form XObject seleccionados, incluidos los Form XObject anidados y el texto codificado mediante fuentes. Elimina automáticamente los artefactos etiquetados como marcas de agua y las anotaciones de marca de agua. Los objetos sin etiquetar requieren una selección o el texto exacto; las marcas integradas en los píxeles no se pueden separar de su imagen. Revisa cada página.

Tipos admitidos: `pdf`. Tipo de salida: `pdf`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `text`, `mode`, `objects`.

Paquetes Python: pypdf. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/pdf_design.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
