<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="calculate-checksum"></a>
# Calcular suma de verificación

Comando: `onekit run file-checksum`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Análisis**. Fidelidad: **exacta**. Calcula SHA-256, SHA-512, SHA-1 o MD5 localmente. Se puede comparar un checksum esperado opcional con un archivo. Un checksum no verifica una firma digital ni asegura la seguridad del archivo.

Tipos admitidos: `*`. Tipo de salida: `json`. Admite varias entradas: **sí**.

Validación de entrada: **cualquier tipo de archivo**. Número de archivos requerido: **1–20**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `algorithm`, `expected`.

Paquetes Python: biblioteca estándar o motor externo. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/file_checksum.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
