<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="barcode-to-text"></a>
# Código de barras a texto

Comando: `onekit run barcode-to-text`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Códigos QR**. Fidelidad: **exacta**. Lee códigos de barras lineales estándar localmente desde una imagen; Usa una imagen nítida con barras completas y márgenes laterales claros.

Tipos admitidos: `png, jpeg, webp, bmp, gif`. Tipo de salida: `txt`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **16 777 216 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: ninguna.

Paquetes Python: Pillow, zxing-cpp. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/barcode.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
