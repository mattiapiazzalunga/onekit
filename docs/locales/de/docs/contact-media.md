<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="contacts-image-enlargement-and-local-media-tools"></a>
# Kontakte, Bildvergrößerung und lokale Medien-Tools

| Werkzeug | Eingabe | Optionen | Ausgabe |
| --- | --- | --- | --- |
| `vcard-generate` | Kontakt JSON, wie bei `vcard-to-qrcode` | Kontaktfelder gehören in die Eingabe JSON | VCF 3.0 / 4.0 |
| `qrcode-to-vcard` | QR Bild, das ein komplettes vCard enthält | Keine | Eine VCF pro erkanntem Kontakt |
| `image-upscale` | Einzelframe-Bild | `scale`: 2 (Standard), 3 oder 4 | PNG |
| `image-remove-background` | Einzelframe-Bild | Keine | Transparent PNG |
| `video-compress` | Video | `compression_level`: leicht, ausgewogen (Standard), maximal | MP4, oder das Original, wenn kleiner |
| `video-speed` | Video | `speed`: 0.25–4, Standard 2 | MP4 mit synchronisiertem, tonhöhenerhaltendem Audio |
| `video-to-gif` | Video | `start`: Sekunden, `duration`: 0.1–30, `fps`: 1–30, `width`: 64–1280 | Schleife GIF ohne Audio |
| `audio-to-text` | Audio | `language`: automatisch (Standard), it, en oder ein anderer Whisper Sprachcode | TXT und Zeitstempel JSON |

Installieren Sie nur die Python Extras, die benötigt werden:

```sh
python -m pip install 'onekit-tools[qrcode,images,background,transcription]'
```

Videooperationen benötigen außerdem `ffmpeg` und `ffprobe` im PATH. CLI verwendet den installierten FFmpeg-Build; unterstützte Codecs hängen von diesem Build ab. `onekit doctor TOOL` prüft die erforderlichen Engines und Pakete.

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

Kontakt JSON Beispiel:

```json
{"first_name":"Ada","last_name":"Lovelace","version":"3.0","emails":["ada@example.org"]}
```

Die QR-Extraktion akzeptiert vollständige vCard-3.0/4.0-Inhalte mit einem Anzeigenamen. Sie folgt keinen Kontakt-Download-URLs und wandelt beliebigen QR-Text nicht in Kontaktdaten um. Die Vergrößerung verwendet Lanczos-Resampling, kein KI-Modell. Die Ausgabe ist auf 40 Millionen Pixel begrenzt. Animierte Bilder werden von den Python-Bildadaptern abgelehnt.

Der CLI-Adapter zur Hintergrundentfernung lädt U2Net direkt mit ONNX Runtime und umgeht die Pillow <13 Abhängigkeitsbeschränkung von rembg. Modells Downloads werden checksum-geprüft und im lokalen OneKit Modell-Cache gespeichert. Optionale Modell-Engines bleiben separat vom tragbaren `all` Zusatz.
