<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="set-metadata"></a>
# Establecer metadatos

Comando: `onekit run file-metadata-set`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Análisis**. Fidelidad: **exacta**. Conserva el contenido seleccionado; valida los resultados importantes.

Tipos admitidos: `*`. Tipo de salida: `*`. Admite varias entradas: **no**.

Validación de entrada: **cualquier tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `metadata`.

Paquetes Python: biblioteca estándar o motor externo. Motores externos: exiftool.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/inspector/__init__.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
