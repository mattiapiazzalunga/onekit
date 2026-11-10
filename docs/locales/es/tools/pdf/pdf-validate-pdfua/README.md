<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="validate-pdfua"></a>
# Verificar PDF/UA

Comando: `onekit run pdf-validate-pdfua`. Utilice `onekit run --help` para los argumentos de entrada y salida.

Categoría: **pdf**. Fidelidad: **exacto**. Compruebe PDF/UA-1 automáticamente con un motor de validación local. Un resultado que pasa todavía requiere revisión manual de accesibilidad. El informe identifica el motor, el perfil y el archivo exacto hash.

Tipos admitidos: `pdf`. Tipo de salida: `json`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `profile`.

Paquetes Python: biblioteca estándar o motor externo. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Aplicación del proceso: [adaptador familiar compartido](../../../../../../src/onekit/tools/pdf_conformance.py). Contratos y accesorios de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motor](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
