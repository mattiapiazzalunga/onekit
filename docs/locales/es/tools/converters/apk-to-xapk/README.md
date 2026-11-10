<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="apk-to-xapk"></a>
# APK → XAPK

Comando: `onekit run apk-to-xapk`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **convertidores**. Fidelidad: **exacta**. Empaqueta un APK independiente y sus metadatos en un archivo XAPK sin modificar los bytes del APK. Se rechazan los APK divididos. Requiere un instalador compatible con XAPK; no se verifican las firmas.

Tipos admitidos: `apk`. Tipo de salida: `xapk`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: ninguna.

Paquetes Python: biblioteca estándar o motor externo. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/android_packages.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
