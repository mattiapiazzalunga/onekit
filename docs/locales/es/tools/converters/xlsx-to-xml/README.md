<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="excel-to-xml"></a>
# Excel a XML

Comando: `onekit run xlsx-to-xml`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Conversores**. Fidelidad: **exacta**. Las tablas XML usan registros planos repetidos. JSON a XML preserva los tipos usando un esquema tipado de raíz/item; los atributos XML usan @ y el texto usa #text en JSON. Las fórmulas de la hoja de cálculo no se evalúan; se usa la primera hoja por defecto. Revisa el esquema y los valores después de la conversión.

Tipos admitidos: `xlsx`. Tipo de salida: `xml`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `sheet`.

Paquetes Python: openpyxl. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/structured_data.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
