<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="txt-to-excel"></a>
# TXT a Excel

Comando: `onekit run txt-to-xlsx`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Conversores**. Fidelidad: **exacta**. Convierte archivos TXT con delimitadores en una hoja de cálculo de Excel. Las celdas se guardan como texto, conservando los ceros iniciales e impidiendo la ejecución de fórmulas. Todas las filas deben tener el mismo número de columnas.

Tipos admitidos: `txt`. Tipo de salida: `xlsx`. Admite varias entradas: **no**.

Validación de entrada: **texto en la codificación seleccionada**. Número de archivos requerido: **1–1**. CLI: **8 388 608 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `delimiter`, `source_encoding`.

Paquetes Python: openpyxl. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/text_converters.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
