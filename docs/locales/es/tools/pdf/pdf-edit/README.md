<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="edit-pdf"></a>
# Editar PDF

Comando: `onekit run pdf-edit`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **PDF**. Fidelidad: **con limitaciones**. Edita los cuadros de texto compatibles con la fuente original. El texto más largo se ajusta al ancho original. No se pueden editar documentos escaneados, texto dentro de objetos Form XObject reutilizables ni caracteres ausentes de la fuente. Esta herramienta no permite censurar datos de forma permanente. La opción de texto anterior añade una superposición.

Tipos admitidos: `pdf`. Tipo de salida: `pdf`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `mode`, `edits`, `password`, `text`, `x`, `y`, `page`.

Paquetes Python: pycryptodome, pypdf, reportlab. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/pdf/__init__.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
