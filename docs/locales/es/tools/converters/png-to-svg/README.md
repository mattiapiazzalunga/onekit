<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="png-to-svg"></a>
# PNG a SVG

Comando: `onekit run png-to-svg`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Conversores**. Fidelidad: **con limitaciones**. Vectoriza un PNG como mosaicos vectoriales basados en paleta, sin incrustar un mapa de bits. Los degradados y los detalles finos se aproximan; los píxeles transparentes se componen sobre blanco.

Tipos admitidos: `png`. Tipo de salida: `svg`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `colors`, `resolution`.

Paquetes Python: Pillow. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/vector_images.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
