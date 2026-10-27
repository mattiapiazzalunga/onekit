<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="external-engines-and-licenses"></a>
# Motores y licencias externas

El propietario aprobó motores de código abierto instalados por separado. No están incluidos en Python wheel, descarga de fuente o imagen inicial de Docker. `onekit doctor` informa los requisitos. `ONEKIT_ALLOW_COPYLEFT=0` desactiva explícitamente los adaptadores copyleft listados. Mantén las herramientas de los proyectos de origen actualizadas; los subprocesos locales no son un entorno completamente seguro para documentos hostiles.

| Motor | Comando | Usa / consideraciones de licencia |
| --- | --- | --- |
| LibreOffice | `soffice` / `libreoffice` | Oficina → PDF/imagenes; avisos de MPL y de terceros. |
| Pandoc | `pandoc` | Conversión avanzada de marcado; GPL. |
| TeX Live/pdfTeX | `pdflatex` | LaTeX/Pandoc PDF; el motor, macros y fuentes tienen licencias separadas. |
| FFmpeg | `ffmpeg` | Medios; LGPL o GPL según la versión y los códecs. |
| veraPDF | `verapdf` | Verificación independiente opcional de los resultados archivados; requisitos ascendentes GPL/MPL y Java. |
| ExifTool | `exiftool` | Metadatos en tipos de archivo compatibles; licencia Perl original. |
| Tesseract | `tesseract` | OCR; motor Apache y datos de idioma con licencia separada. |

Si distribuyes estos programas, incluso dentro de Docker, conserva sus licencias/avisos y proporciona los materiales requeridos del código fuente correspondiente y de compilación. Evalúa las integraciones de red AGPL por separado. El uso comercial y las obligaciones de fuente/re-distribución son preguntas diferentes. Los procesos separados no eliminan obligaciones de manera universal. Lee material autoritativo [FFmpeg](https://ffmpeg.org/legal.html), [LibreOffice](https://www.libreoffice.org/licenses/), [Ghostscript](https://www.ghostscript.com/licensing/) y [MPL](https://www.mozilla.org/en-US/MPL/2.0/FAQ/) antes de crear una distribución empaquetada.

La fidelidad de los documentos de Office depende de las fuentes y los recursos. PDF a Word exporta el texto extraído; PDF a PowerPoint crea diapositivas con imágenes. La reparación de PDF no está garantizada; la compresión no tiene pérdida. La [conversión y validación de PDF/A](pdfa.md) usa bibliotecas MPL independientes mediante el adaptador Python compartido, con perfiles ICC incluidos y con licencia. No se requiere Ghostscript. Sigue siendo recomendable una validación independiente de los estándares. La precisión del OCR depende de la calidad del escaneo y de los paquetes de idiomas.

<a id="developer-tools"></a>
## Developer tools

Instala Node.js 24+ y ejecuta `onekit engines install` para Prettier/plugins con versiones fijadas, esbuild, HTML minificador, SVGO y GraphQL.js. Se instalan en la caché del usuario OneKit, no globalmente. `ONEKIT_NODE_ENGINE_PATH` selecciona una alternativa. Vuelve a ejecutar el instalador después de una actualización aprobada del motor. El grupo de parser cubre JS/TS/JSX/TSX, marcado, hojas de estilo, Markdown/MDX, GraphQL, Vue, Svelte, Astro, Solidity y PHP.

Instala compiladores/lanzadores upstream para tu SO y agrega los comandos documentados al PATH. Algunos archivos aislados necesitan sus dependencias de proyecto o el nombre de archivo exacto de la clase Java. La validación de formato/analizador no prueba la corrección de tipo en todo el proyecto.

En Windows, los adaptadores Bash/Shell prefieren un intérprete real en PATH y luego detectan Git para Windows en sus directorios estándar de instalación del sistema/usuario. El lanzador WSL de System32 no se trata como un analizador local compatible. La validación de sintaxis de PowerShell requiere `pwsh`; el formateo además requiere PSScriptAnalyzer (`Install-Module PSScriptAnalyzer -Scope CurrentUser`). `onekit doctor dev-format-powershell` verifica ese módulo por separado e informa su comando de configuración. Estos programas/módulos no se descargan mientras se procesan archivos.

<a id="platform-qualifications"></a>
## Platform qualifications

Las comprobaciones de licencias en CI también instalan y examinan el extra de firma independiente (`scripts/check_licenses.py --include-signing`). MIT-0 se reconoce como una licencia permisiva ([texto SPDX](https://spdx.org/licenses/MIT-0.html)). Los datos del almacén de confianza de Mozilla de la versión fijada de `certifi`, 2026.7.22, constituyen una excepción MPL-2.0 explícita y específica de esa versión; conserva su licencia y avisos originales sin modificaciones al redistribuirlos ([aviso original](https://github.com/certifi/python-certifi/blob/master/LICENSE)). Las nuevas versiones requieren otra revisión. Esta excepción no admite de forma general otros paquetes MPL ni cambia la licencia PolyForm-Shield-1.0.0 de OneKit.

El núcleo universal Python es compatible con Linux, Windows y macOS, incluyendo ARM64. Los extras nativos y los motores externos determinan requisitos adicionales. CI declara los runners x64/ARM en las tres familias de OS. En Windows ARM, Brotli/WOFF2 y la pila de criptografía de firma separada pueden requerir herramientas de compilación nativas o x64 Python bajo emulación. WOFF/TTF/OTF no requieren el codificador WOFF2. El extra `all` excluye la firma separada. Informa estas restricciones opcionales en lugar de decir que existe un wheel nativo cuando no lo hay.
