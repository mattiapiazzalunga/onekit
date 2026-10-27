<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="url-inspector"></a>
# Inspector URL

Comando: `onekit run url-inspect`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Análisis**. Fidelidad: **con limitaciones**. Inspecciona los componentes URL, el estado HTTP, el URL final y los encabezados de respuesta disponibles directamente desde tu dispositivo. Registra hasta 10 redirecciones HTTP. Las fallas de red dejan un informe parcial. Esto no es un chequeo de phishing, malware, DNS o propiedad.

Tipos admitidos: `txt`. Tipo de salida: `json`. Admite varias entradas: **no**.

Validación de entrada: **texto**. Número de archivos requerido: **1–1**. CLI: **16 384 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: ninguna.

Paquetes Python: biblioteca estándar o motor externo. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/link_tools.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
