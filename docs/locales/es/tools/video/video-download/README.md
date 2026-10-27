<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="download-video"></a>
# Descarga video

Comando: `onekit run video-download`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Vídeo**. Fidelidad: **exacta**. Descargas desde YouTube y otros sitios compatibles con yt-dlp, hasta 128 MiB. El soporte del sitio varía; se requiere conexión a internet.

Tipos admitidos: `txt`. Tipo de salida: `*`. Admite varias entradas: **no**.

Validación de entrada: **texto**. Número de archivos requerido: **1–1**. CLI: **16 384 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `quality`, `cookies`, `cookies_from_browser`, `format_id`, `referer`, `list_formats`.

Paquetes Python: yt-dlp. Motores externos: ffmpeg.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/video_download.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
