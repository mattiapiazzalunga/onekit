<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="generate-barcode"></a>
# Genera código de barras

Comando: `onekit run text-to-barcode`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Códigos QR**. Fidelidad: **exacta**. Genera Código 128, Código 39, EAN-13, EAN-8, UPC-A, ITF y ISBN-13 localmente. Se validan o calculan los dígitos de control minoristas; los identificadores no son registrados ni asignados por OneKit.

Tipos admitidos: `txt`. Tipo de salida: `png`. Admite varias entradas: **no**.

Validación de entrada: **texto**. Número de archivos requerido: **1–1**. CLI: **1 024 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `barcode_type`, `format`, `module_width`, `height`, `quiet_zone`, `show_text`, `font_size`, `dpi`.

Paquetes Python: python-barcode, Pillow. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/barcode.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
