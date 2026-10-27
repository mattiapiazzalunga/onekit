<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="download-audio"></a>
# Descargar audio

Comando: `onekit run audio-download`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Audio**. Fidelidad: **con limitaciones**. Descarga un archivo de audio directo o una fuente de audio expuesta por una página accesible. El modo original preserva los bytes descargados; la conversión MP3 es con pérdida. Hasta 128 MiB. El inicio de sesión y las transmisiones protegidas pueden impedir la descarga. Úsalo solo con permiso.

Tipos admitidos: `txt`. Tipo de salida: `*`. Admite varias entradas: **no**.

Validación de entrada: **texto**. Número de archivos requerido: **1–1**. CLI: **16 384 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `format`, `quality`.

Paquetes Python: biblioteca estándar o motor externo. Motores externos: ffmpeg, ffprobe.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/link_tools.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
