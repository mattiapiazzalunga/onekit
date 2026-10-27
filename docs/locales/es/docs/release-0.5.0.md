<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="onekit-050"></a>
# OneKit 0.5.0

Lanzamiento inicial de la CLI sin conexión y de la API de procesamiento de Python, con 230 herramientas para documentos, PDF, imágenes, medios, archivos comprimidos, fuentes, utilidades para desarrolladores, códigos QR, declaraciones de licencia e inspección de archivos. La instalación básica no tiene dependencias en tiempo de ejecución; los extras opcionales y los motores externos habilitan las herramientas seleccionadas.

Incluye validación de entrada limitada, flujos de trabajo reutilizables, configuración de dependencias locales, contratos de procesamiento específicos del formato e inspección de licencias basada en la fuente. Los informes de licencias siguen siendo estimaciones no verificadas que requieren revisión manual.

Las actualizaciones de rendimiento aceleran la preparación de imágenes opacas y la inspección de texto. Se han eliminado importaciones no usadas y asignaciones de motor de desarrollo redundantes.

Los motores de modelo son opcionales: instala el extra `background` o `transcription` cuando sea necesario. U2Net se ejecuta directamente con ONNX Runtime y un modelo en caché con verificación de suma. Whisper usa faster-whisper. Los archivos permanecen locales; la primera ejecución descarga los pesos del modelo. El procesamiento de video requiere FFmpeg y ffprobe. La descarga de videos utiliza el extra separado `video`.

Actualiza Pillow a la versión 13 y la versión fijada de certifi para resolver los problemas señalados en los avisos publicados. El grupo portátil de dependencias opcionales `all` sigue separado de los motores de modelos y las funciones de firma.
