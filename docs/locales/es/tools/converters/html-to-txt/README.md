<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="html-to-txt"></a>
# HTML a TXT

Comando: `onekit run html-to-txt`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Conversores**. Fidelidad: **con limitaciones**. Extrae el texto del cuerpo legible HTML sin ejecutar scripts ni obtener recursos. Se omiten el formato, las imágenes, el contenido oculto y los estilos.

Tipos admitidos: `html`. Tipo de salida: `txt`. Admite varias entradas: **no**.

Validación de entrada: **texto**. Número de archivos requerido: **1–1**. CLI: **8 388 608 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: ninguna.

Paquetes Python: biblioteca estándar o motor externo. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/text_converters.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
