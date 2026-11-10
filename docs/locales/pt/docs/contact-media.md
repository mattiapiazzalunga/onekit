<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="contacts-image-enlargement-and-local-media-tools"></a>
# Contatos, ampliação de imagens e ferramentas de mídia locais

| Ferramenta | Entrada | Opções | Saída |
| --- | --- | --- | --- |
| `vcard-generate` | Contato JSON, como para `vcard-to-qrcode` | Os campos de contacto pertencem à entrada JSON | VCF 3.0 / 4.0 |
| `qrcode-to-vcard` | QR imagem contendo uma completa vCard | Nenhum | Um VCF por contacto detectado |
| `image-upscale` | Imagem de quadro único | `scale`: 2 (padrão), 3 ou 4 | PNG |
| `image-remove-background` | Imagem de quadro único | Nenhum | Transparente PNG |
| `video-compress` | Vídeo | `compression_level`: leve, balanceado (padrão), máximo | MP4, ou original se menor |
| `video-speed` | Vídeo | `speed`: 0,25–4, padrão 2 | MP4 com áudio sincronizado, pitch-preservando |
| `video-to-gif` | Vídeo | `start`: segundos, `duration`: 0,1–30, `fps`: 1–30, `width`: 64–1280 | Looping GIF sem áudio |
| `audio-to-text` | Áudio | `language`: auto (padrão), it, en ou outro código de linguagem Whisper | TXT e timetamp JSON |

Instale apenas os Python extras necessários:

```sh
python -m pip install 'onekit-tools[qrcode,images,background,transcription]'
```

As operações de vídeo também precisam de `ffmpeg` e `ffprobe` na PATH. O CLI usa a compilação FFmpeg instalada; codecs suportados dependem dessa compilação. `onekit doctor TOOL` verifica os motores e pacotes necessários.

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

Contato JSON exemplo:

```json
{"first_name":"Ada","last_name":"Lovelace","version":"3.0","emails":["ada@example.org"]}
```

A extração QR aceita cargas completas vCard 3.0/4.0 com um nome de exibição. Ele não segue URLs de download de contato ou converter texto QR arbitrário em dados de contato. O Upscaling usa o resampling Lanczos, não um modelo AI. A saída é limitada a 40 milhões de pixels. As imagens animadas são rejeitadas pelos adaptadores de imagem Python.

O adaptador de fundo CLI carrega U2Net diretamente com ONNX Runtime, evitando o Pillow Rembg <13 restrição de dependência. Os downloads do modelo são verificados e armazenados em cache sob o cache de modelo local OneKit. Os motores de modelo opcionais permanecem separados do extra portátil `all`.
