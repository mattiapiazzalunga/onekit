<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="contacts-image-enlargement-and-local-media-tools"></a>
# Contatti, ingrandimento immagini e strumenti multimediali locali

| Strumento | Input | Opzioni | Output |
| --- | --- | --- | --- |
| `vcard-generate` | Contatta JSON, come per `vcard-to-qrcode` | I campi di contatto appartengono all'input JSON | VCF 3.0 / 4.0 |
| `qrcode-to-vcard` | Immagine QR contenente un completo vCard | Nessuno | Un VCF per contatto rilevato |
| `image-upscale` | Immagine a fotogramma singolo | `scale`: 2 (predefinito), 3 o 4 | PNG |
| `image-remove-background` | Immagine a fotogramma singolo | Nessuno | Trasparente PNG |
| `video-compress` | Video | `compression_level`: leggero, bilanciato (predefinito), massimo | MP4, o originale se più piccolo |
| `video-speed` | Video | `speed`: 0.25–4, predefinito 2 | MP4 con audio sincronizzato che mantiene l'intonazione |
| `video-to-gif` | Video | `start`: secondi, `duration`: 0.1–30, `fps`: 1–30, `width`: 64–1280 | Ciclo GIF senza audio |
| `audio-to-text` | Audio | `language`: auto (predefinito), it, en o un altro codice lingua Whisper | TXT e marca temporale JSON |

Installa solo gli extra Python necessari:

```sh
python -m pip install 'onekit-tools[qrcode,images,background,transcription]'
```

Le operazioni video richiedono anche `ffmpeg` e `ffprobe` nel PATH. CLI utilizza il build FFmpeg installato; i codec supportati dipendono da quel build. `onekit doctor TOOL` controlla i motori e i pacchetti richiesti.

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

Contatta esempio JSON:

```json
{"first_name":"Ada","last_name":"Lovelace","version":"3.0","emails":["ada@example.org"]}
```

L'estrazione QR accetta payload completi vCard 3.0/4.0 con un nome visualizzato. Non segue URL di download dei contatti né converte testo arbitrario QR in dati di contatto. L'upscaling utilizza il ridimensionamento Lanczos, non un modello AI. L'output è limitato a 40 milioni di pixel. Le immagini animate vengono rifiutate dagli adattatori di immagini Python.

L’adattatore CLI per la rimozione dello sfondo carica U2Net direttamente con ONNX Runtime, evitando il vincolo di dipendenza <13 di rembg Pillow. I download dei modelli sono verificati tramite checksum e memorizzati nella cache locale modello OneKit. I motori modello opzionali restano separati dall'extra portatile `all`.
