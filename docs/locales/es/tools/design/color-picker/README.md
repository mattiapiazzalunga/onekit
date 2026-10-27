<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="color-picker"></a>
# Selector de Color

Comando: `onekit run color-picker`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Diseño**. Fidelidad: **exacta**. Lee un color HEX de seis dígitos desde un archivo TXT o toma una muestra de un píxel de una imagen cuya orientación se ha ajustado según los datos EXIF. Muestra el color sRGB visible, el valor RGBA original, el color OKLCH y el contraste del texto. Los píxeles transparentes se componen sobre un fondo blanco.

Tipos admitidos: `png, jpeg, webp, gif, bmp, tiff, ico, txt`. Tipo de salida: `json`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `x`, `y`.

Paquetes Python: Pillow. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/photo_tools.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
