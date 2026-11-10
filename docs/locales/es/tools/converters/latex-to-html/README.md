<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="latex-to-html"></a>
# LaTeX a HTML

Comando: `onekit run latex-to-html`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Conversores**. Fidelidad: **con limitaciones**. Convierte documentos LaTeX autónomos con Pandoc 3.9. No admite archivos externos ni compilación TeX. Hasta 256 KiB por archivo de entrada.

Tipos admitidos: `latex`. Tipo de salida: `html`. Admite varias entradas: **no**.

Validación de entrada: **texto**. Número de archivos requerido: **1–1**. CLI: **8 388 608 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: ninguna.

Paquetes Python: biblioteca estándar o motor externo. Motores externos: node.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/converters/__init__.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
