<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="add-page-numbers-to-pdf"></a>
# Agregar números de página a PDF

Comando: `onekit run pdf-page-numbers`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **PDF**. Fidelidad: **exacta**. Agrega números secuenciales a todas o algunas páginas, manteniendo el texto y los gráficos originales. Las firmas digitales existentes se invalidan.

Tipos admitidos: `pdf`. Tipo de salida: `pdf`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `pages`, `start_number`, `number_style`, `font_size`, `position`, `margin`, `color`.

Paquetes Python: pypdf, reportlab. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/pdf.page_numbers/__init__.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
