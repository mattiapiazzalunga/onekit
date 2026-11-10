<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="automatically-blur-faces"></a>
# Desenfocar rostros automáticamente

Comando: `onekit run image-blur-faces`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **imágenes**. Fidelidad: **con limitaciones**. Detecta rostros localmente con YuNet y los desenfoca en un nuevo PNG. Revisa cada rostro antes de compartir: la detección automática puede omitir algunos y el desenfoque no garantiza el anonimato. Imágenes de un solo fotograma, hasta 16 millones de píxeles.

Tipos admitidos: `png, jpeg, webp, gif, bmp, tiff, ico`. Tipo de salida: `png`. Admite varias entradas: **no**.

Validación de entrada: **según el tipo de archivo**. Número de archivos requerido: **1–1**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: ninguna.

Paquetes de Python: onnxruntime, numpy, Pillow. Motores externos: consulta la matriz de motores de desarrollo para los adaptadores de lenguajes.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/face_blur.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
