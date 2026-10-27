<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="pdf-to-pdfa"></a>
# PDF a PDF/A

Comando: `onekit run pdf-to-pdfa`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Conversores**. Fidelidad: **con limitaciones**. Convierte localmente a PDF/A-2b o 3b con las fuentes incrustadas. El archivo generado se valida antes de descargarlo. El contenido no compatible puede eliminarse o rechazarse; revisa el resultado.

Tipos admitidos: `pdf`. Tipo de salida: `pdfa`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `icc_profile`, `profile`.

Paquetes Python: pdftopdfa, pikepdf, jsonschema, fonttools, pdfminer.six. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/converters/__init__.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
