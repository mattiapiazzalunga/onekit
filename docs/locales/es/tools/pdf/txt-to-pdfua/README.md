<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="text-to-pdfua"></a>
# Texto a PDF/UA

Comando: `onekit run txt-to-pdfua`. Utilice `onekit run --help` para los argumentos de entrada y salida.

Categoría: **pdf**. Fidelidad: **exacto**. Cree una etiqueta PDF/UA-1 de texto plano con un título e idioma. Líneas blancas párrafos separados. Fuentes latinas solamente; repasar el orden de lectura y significado. Los cheques automáticos no reemplazan la revisión manual de accesibilidad.

Tipos admitidos: `txt`. Tipo de salida: `pdf`. Admite varias entradas: **no**.

Validación de entrada: **text**. Cuenta de archivo requerido: **1–1**. CLI: **262,144 bytes per file**, **8,388,608 bytes total**. Comprobaciones de contenido se ejecutan antes del procesamiento. Renombrar un archivo no cambia su formato real.

Opciones: `title`, `language`.

Python paquetes: reportlab, pypdf, Pillow. Motores externos: vea la matriz del motor desarrollador para adaptadores de lenguaje.

Aplicación del proceso: [adaptador familiar compartido](../../../../../../src/onekit/tools/pdfua.py). Contratos y accesorios de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motor](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
