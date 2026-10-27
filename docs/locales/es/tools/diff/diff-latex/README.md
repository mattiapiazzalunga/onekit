<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="compare-latex-files"></a>
# Comparar archivos LaTeX

Comando: `onekit run diff-latex`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Comparación**. Fidelidad: **con limitaciones**. La comparación de cuadernos puede incluir Markdown, código o ambos. El modo de texto LaTeX omite comandos.

Tipos admitidos: `latex, txt`. Tipo de salida: `json`. Admite varias entradas: **sí**.

Validación de entrada: **texto**. Número de archivos requerido: **2–2**. CLI: **8 388 608 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `mode`.

Paquetes Python: biblioteca estándar o motor externo. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/diff/__init__.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
