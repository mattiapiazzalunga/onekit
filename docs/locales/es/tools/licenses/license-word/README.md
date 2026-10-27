<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="word-license-checker"></a>
# Comprobador de licencias Word

Comando: `onekit run license-word`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Licencias**. Fidelidad: **con limitaciones**. Una estimación basada en declaraciones y metadatos, no en un certificado de derechos o autorización legal. Verifica cada hallazgo con la fuente original y el titular de los derechos. La información faltante nunca significa que sea de libre uso. Los autores y titulares de derechos pueden ser diferentes. Los archivos se analizan localmente; los enlaces se descargan directamente desde su fuente. La inspección de archivos comprimidos tiene límites y puede ser incompleta.

Tipos admitidos: `docx, docm, doc`. Tipo de salida: `json`. Admite varias entradas: **no**.

Validación de entrada: **cualquier tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `ref`.

Paquetes Python: license-expression, defusedxml, olefile. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/license_check.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
