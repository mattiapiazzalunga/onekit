<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="regex-tester"></a>
# Probador de Regex

Comando: `onekit run dev-regex-test`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Desarrollo**. Fidelidad: **exacta**. Prueba expresiones regulares de JavaScript localmente con capturas, grupos nombrados, posiciones UTF-16 y reemplazo. Hasta 128 KiB de texto, 1000 coincidencias y 1 MiB de salida. La ejecución tiene límite de tiempo; el CLI requiere Node.js.

Tipos admitidos: `txt`. Tipo de salida: `json`. Admite varias entradas: **no**.

Validación de entrada: **texto**. Número de archivos requerido: **1–1**. CLI: **131 072 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `pattern`, `flags`, `max_matches`, `enable_replacement`, `replacement`.

Paquetes Python: biblioteca estándar o motor externo. Motores externos: node.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/regex_tester.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
