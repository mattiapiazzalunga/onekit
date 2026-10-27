<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="compress-video"></a>
# Comprimir vídeo

Comando: `onekit run video-compress`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Vídeo**. Fidelidad: **con limitaciones**. Procesos localmente con FFmpeg. La re-codificación puede perder calidad. La salida de GIF no tiene audio.

Tipos admitidos: `mp4, webm, mkv, mov, avi, gif, mpeg, mpg, m4v, ogv, ts`. Tipo de salida: `mp4`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `compression_level`.

Paquetes Python: biblioteca estándar o motor externo. Motores externos: ffmpeg, ffprobe.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/video_edit.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
