<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="color-palette-generator"></a>
# Generador de Paleta de Colores

Comando: `onekit run color-palette`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Diseño**. Fidelidad: **exacta**. Paletas OKLCH de cinco colores, con reducción del croma para ajustarse al espacio sRGB y contraste del texto según WCAG. Las reglas de armonía son criterios de diseño, no garantías de accesibilidad.

Tipos admitidos: `txt`. Tipo de salida: `json`. Admite varias entradas: **no**.

Validación de entrada: **texto**. Número de archivos requerido: **1–1**. CLI: **128 bytes por archivo**, **1 048 576 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `harmony`, `lightness`, `chroma`, `hue`, `format`.

Paquetes Python: biblioteca estándar o motor externo. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/design.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
