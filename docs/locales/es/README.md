<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->

Idiomas: [English](../../../README.md) · [Italiano](../it/README.md) · [Français](../fr/README.md) · [Español](README.md) · [Deutsch](../de/README.md) · [Русский](../ru/README.md) · [中文](../zh/README.md).

<p align="center">
  <a href="https://onekit.org"><img src="https://raw.githubusercontent.com/mattiapiazzalunga/onekit/main/images/logo.png" alt="OneKit logo" width="112" height="112"></a>
</p>
<h1 align="center">OneKit</h1>
<p align="center">Un solo conjunto de herramientas. Tus archivos siguen siendo tuyos.</p>
<p align="center"><a href="https://github.com/mattiapiazzalunga/onekit/stargazers"><img alt="Estrellas en GitHub" src="https://img.shields.io/github/stars/mattiapiazzalunga/onekit"></a> <a href="https://pypi.org/project/onekit-tools/"><img alt="PyPI" src="https://img.shields.io/pypi/v/onekit-tools"></a> <img alt="PolyForm-Shield-1.0.0" src="https://img.shields.io/badge/license-PolyForm_Shield_1.0.0-blue"> <img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue"></p>

Un kit de herramientas Python sin conexión con 230 herramientas para conversiones, PDFs, imágenes, archivos, fuentes, inspección de archivos, encriptación, utilidades de desarrollador, OCR y comparaciones. Usa este CLI o la interfaz gráfica en **[onekit.org](https://onekit.org)**.

**Versión del origen:** `0.6.0`. Las descargas estables solo existen después de que se complete el flujo de trabajo de lanzamiento. La distribución es `onekit-tools`; el proyecto PyPI de propiedad separada llamado `onekit` no está relacionado.

La [guía de contactos y archivos multimedia](docs/contact-media.md) explica la creación de vCard independientes, la extracción de vCard a partir de códigos QR, el aumento de resolución de imágenes, la eliminación de fondos, la compresión y el ajuste de velocidad de vídeos y GIF, y la transcripción de audio local.

Verificación de licencias: inspeccionar PDF, Word, PowerPoint, Excel, video, audio, imágenes, fuentes, EPUB, código/proyectos y conjuntos de datos de archivos o URLs públicas. El análisis se mantiene local; los informes son **estimaciones no verificadas, no certificados de propiedad ni permisos de uso**. Consulta [uso y límites de la verificación de licencias](docs/cli.md#local-license-and-copyright-estimates).

**Tu CLI. Tu CLI para agentes.** Usa OneKit tú mismo o deja que un agente local AI lo llame a través de un terminal o subproceso. Descubre herramientas y requisitos como JSON, pasa rutas de entrada/salida explícitas y reutiliza flujos de trabajo guardados `.1kit` para tareas de archivos repetibles. Ver [agentes locales y automatización](docs/cli.md#local-agents-and-automation).

<a id="install"></a>
## Install

Se requiere Python 3.11 o posterior. El paquete wheel universal es compatible con Windows, macOS y Linux en x64/ARM64. Las bibliotecas nativas opcionales y los motores externos tienen requisitos de plataforma adicionales.

Después de la publicación:

```sh
python -m pip install onekit-tools
python -m pip install "onekit-tools[pdf,images,documents]"
onekit list
onekit doctor
```

Desde una copia del repositorio fuente:

```sh
python -m pip install -e ".[all,test]"
python -m onekit --help
python -m pytest -q
```

La base CLI **no tiene dependencias en tiempo de ejecución**. Instala solo los extras que necesites. `all` incluye las familias estándar Python; la descarga de videos, la eliminación de fondo, la transcripción y la firma criptográfica usan los extras separados `video`, `background`, `transcription` y `signing`. Instala los motores nativos por separado. Para herramientas de desarrollo basadas en Node, instala Node.js 24+ y ejecuta `onekit engines install`. CLI prepara las dependencias faltantes y los motores externos en el primer uso. La eliminación de fondo y la transcripción descargan los pesos del modelo en el primer uso y luego reutilizan la caché local.

<a id="use"></a>
## Use

```sh
onekit run pdf-merge first.pdf second.pdf -o combined.pdf
onekit run pdf-extract-pages document.pdf --options '{"pages":"1,3-5"}' -o selected.pdf
onekit run image-convert image.png --options '{"format":"webp"}' -o image.webp
onekit run diff-notebook before.ipynb after.ipynb --options '{"mode":"code"}' -o changes.json
onekit run security-encrypt private-folder --ask-password -o private.zip
onekit run security-decrypt private.zip --ask-password -o restored
```

Las opciones son objetos JSON; pásalos como un argumento de shell entre comillas. Usa `--ask-password` para secretos. Se conservan los resultados existentes a menos que pases `--force`.

`onekit list --group pdf`, `onekit list --json` y `onekit doctor TOOL_ID` exponen contratos y requerimientos. Cada herramienta tiene un directorio bajo [tools](../../../tools), que contiene metadatos y un enlace a su implementación compartida. Consulta la guía [CLI](docs/cli.md) para opciones y límites.

<a id="toolkit"></a>
## Toolkit

| Familia | Capacidades |
| --- | --- |
| Convertidores | Markdown, HTML, LaTeX, PDF, Word, PowerPoint, imágenes, Base64, Excel, CSV y JSON |
| PDF | Fusionar/dividir, selección/orden/eliminación de páginas, compresión, reparación, [edición directa de texto](docs/pdf-editing.md), superposición de texto, rotación, firmas digitales, encriptación/desbloqueo, [conversión y validación locales de PDF/A](docs/pdfa.md) |
| Imágenes | Extrae imágenes incrustadas PDF, comprímelas, recórtalas y cambia el formato. |
| Medios | Conversión de audio/video a través de FFmpeg instalado por separado |
| Archivos / fuentes | Variantes ZIP/TAR; contenedores TTF/OTF y WOFF/WOFF2 |
| Inspector / seguridad | Escribe firmas, estructura, metadatos, codificación, hashes, conteos de texto; archivos/carpetas autenticados y cifrados |
| Desarrollador | Formateo específico del idioma, validación del parser/compilador y minificación seleccionada |
| OCR | Imágenes escaneadas/PDF a PDF, Word, Markdown, LaTeX, HTML y JSON buscables |
| Diferencia | Texto, código, JSON normalizado, cuadernos, LaTeX, PDF y Word texto |

<a id="pipelines-and-development"></a>
## Pipelines and development

`onekit pipeline --steps workflow.1kit INPUTS -o OUTPUT` acepta un documento de flujo de trabajo `.1kit` versionado. Cada paso recibe los resultados anteriores. Los pasos de entrada única se aplican sobre múltiples resultados; los pasos de fusión reciben la colección. Los tipos incompatibles detienen el procesamiento.

Comunica errores y sugerencias a través de las [incidencias de GitHub](https://github.com/mattiapiazzalunga/onekit/issues) o de la [sección de solicitudes del sitio web](https://onekit.org/requests/). Las personas que contribuyen pueden encontrar tareas en ambos lugares.

<a id="contribute-to-onekit"></a>
## Contribute to OneKit

Ayuda a construir la revolución abierta de OneKit: herramientas diarias para todos, desde tareas prácticas hasta flujos de trabajo manejados por agentes locales AI. Contribuye para hacer las herramientas más eficientes y efectivas: mejora la velocidad y el uso de memoria, corrige resultados incorrectos, agrega ejemplos de regresión o aclara la documentación y los flujos de trabajo de los agentes.

El núcleo es de código abierto (PolyForm Shield 1.0.0). Lee la [guía de contribución](https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md) y encuentra una tarea en [GitHub issues](https://github.com/mattiapiazzalunga/onekit/issues), o sugiere una mejora en la [panel de solicitudes](https://onekit.org/requests/).

<a id="license-and-creator"></a>
## License and creator

Creado por **[Mattia Piazzalunga](mailto:hello@mattiapiazzalunga.com)**. Copyright © 2026 Mattia Piazzalunga. Código abierto (PolyForm Shield 1.0.0), con licencia bajo [PolyForm Shield 1.0.0](../../../LICENSE); vea [NOTICE](../../../NOTICE), [AUTHORS.txt](../../../AUTHORS.txt) y [CONTRIBUTORS.txt](../../../CONTRIBUTORS.txt). Los componentes de terceros conservan sus licencias. Los motores externos son programas separados con sus propias obligaciones de redistribución.

Puedes usar, modificar y redistribuir el núcleo para fines permitidos, incluyendo uso comercial e interno. No puedes usarlo para ofrecer un producto o servicio que compita con el software o con un producto que el licenciante o sus afiliados ofrezcan usando el software; las ofertas gratuitas y diferentes plataformas o interfaces también pueden competir. Al compartir copias, incluye el texto de la licencia o su URL y cualquier línea de Aviso Requerido proporcionada con el software. La licencia completa gobierna, incluyendo sus excepciones para productos nuevos y descontinuados, términos de patentes y exención de garantía. Aquí, “Código Abierto (PolyForm Shield 1.0.0)” describe el código publicado bajo estos términos; la restricción de no competencia significa que este es un software con código accesible en lugar de código abierto sin restricciones según la Definición de Código Abierto. Consulta [la guía de licencias](docs/licenses.md).

Exporta y reimporta flujos de trabajo sin procesar archivos de entrada:

```sh
onekit workflow export workflow.1kit -o exported-workflow.1kit
onekit workflow import workflow.1kit -o saved-workflow.1kit
onekit pipeline --steps saved-workflow.1kit input.json -o output.json
```

Los códigos de barras estándar están disponibles en la categoría Códigos QR y códigos de barras y en la CLI: `text-to-barcode`, `scan-barcode`, `barcode-to-text`. Código 128, Código 39, EAN-13, EAN-8, UPC-A, ITF y ISBN-13 soportan PNG/SVG, dimensiones configurables y validación de dígito de control. Instala `onekit-tools[barcode]` o `onekit-tools[qrcode]`.

La [censura permanente de PDF e imágenes](docs/redaction.md) está disponible mediante `pdf-redact` y `image-redact`. Las áreas seleccionadas se sustituyen por píxeles negros opacos en los nuevos archivos. Los PDF se reconstruyen como documentos formados solo por imágenes, sin texto, formularios, comentarios, adjuntos ni metadatos originales; las imágenes se convierten en PNG opacos sin metadatos originales ni píxeles ocultos por la transparencia. Los archivos originales no se modifican.

Agrega marcas de agua de texto PDF configurables con `pdf-watermark`: opacidad, color, fuentes, rangos de páginas, posiciones visuales, rotación y rejillas repetidas. El texto y los gráficos permanecen en PDF. Consulta la [guía de marcas de agua](docs/watermark.md).

<a id="contacts"></a>
## Contacts

- Preguntas generales y soporte: [support@onekit.org](mailto:support@onekit.org).
- Preguntas sobre el núcleo de Código Abierto (PolyForm Shield 1.0.0) y contribuciones: [developers@onekit.org](mailto:developers@onekit.org).
- Privacidad, GDPR y solicitudes de datos personales: [privacy@onekit.org](mailto:privacy@onekit.org).
- Preguntas legales, licencias y solicitudes de permiso: [legal@onekit.org](mailto:legal@onekit.org).
- Vulnerabilidades de seguridad e informes de abuso: [security@onekit.org](mailto:security@onekit.org).
