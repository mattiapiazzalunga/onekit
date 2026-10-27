<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="contacts-image-enlargement-and-local-media-tools"></a>
# Contactos, ampliación de imágenes y herramientas de medios locales

| Herramienta | Entrada | Opciones | Salida |
| --- | --- | --- | --- |
| `vcard-generate` | Contacta a JSON, como para `vcard-to-qrcode` | Los campos de contacto pertenecen al input JSON | VCF 3.0 / 4.0 |
| `qrcode-to-vcard` | Imagen QR que contiene un vCard completo | Ninguno | Un VCF por contacto detectado |
| `image-upscale` | Imagen de un solo cuadro | `scale`: 2 (predeterminado), 3 o 4 | PNG |
| `image-remove-background` | Imagen de un solo cuadro | Ninguno | PNG transparente |
| `video-compress` | Video | `compression_level`: ligero, equilibrado (por defecto), máximo | MP4, o el original si es más pequeño |
| `video-speed` | Video | `speed`: 0.25–4, predeterminado 2 | MP4 con audio sincronizado que conserva el tono |
| `video-to-gif` | Video | `start`: segundos, `duration`: 0.1–30, `fps`: 1–30, `width`: 64–1280 | Reproduciendo en bucle GIF sin audio |
| `audio-to-text` | Audio | `language`: automático (predeterminado), it, en u otro código de idioma Whisper | TXT y marca de tiempo JSON |

Instala solo los extras Python que necesites:

```sh
python -m pip install 'onekit-tools[qrcode,images,background,transcription]'
```

Las operaciones de video también necesitan `ffmpeg` y `ffprobe` en PATH. El CLI usa la compilación FFmpeg instalada; los codecs soportados dependen de esa compilación. `onekit doctor TOOL` verifica los motores y paquetes requeridos.

```sh
onekit run vcard-generate contact.json -o contact.vcf
onekit run qrcode-to-vcard contact-qr.png -o contacts/
onekit run image-upscale photo.png --options '{"scale":2}' -o larger.png
onekit run image-remove-background portrait.jpg -o transparent.png
onekit run video-compress clip.mov --options '{"compression_level":"balanced"}' -o compressed/
onekit run video-speed clip.mp4 --options '{"speed":0.5}' -o slower.mp4
onekit run video-to-gif clip.mp4 --options '{"start":1,"duration":3,"fps":12,"width":480}' -o clip.gif
onekit run audio-to-text voice.wav --options '{"language":"it"}' -o transcript/
```

Ejemplo de contacto JSON:

```json
{"first_name":"Ada","last_name":"Lovelace","version":"3.0","emails":["ada@example.org"]}
```

La extracción QR acepta cargas útiles completas vCard 3.0/4.0 con un nombre para mostrar. No sigue URLs de descarga de contactos ni convierte texto arbitrario QR en datos de contacto. El escalado utiliza remuestreo Lanczos, no un modelo AI. La salida está limitada a 40 millones de píxeles. Las imágenes animadas son rechazadas por los adaptadores de imagen Python.

El adaptador CLI de eliminación del fondo carga U2Net directamente con ONNX Runtime, evitando la restricción de dependencia Pillow <13 de rembg. Las descargas de modelos se verifican con checksum y se almacenan en caché bajo el caché local de modelos OneKit. Los motores de modelos opcionales permanecen separados del extra portátil `all`.
