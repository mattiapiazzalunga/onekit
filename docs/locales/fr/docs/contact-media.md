<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="contacts-image-enlargement-and-local-media-tools"></a>
# Contacts, agrandissement d'image et outils multimédias locaux

| Outil | Entrée | Options | Sortie |
| --- | --- | --- | --- |
| `vcard-generate` | Contacter JSON, comme pour `vcard-to-qrcode` | Les champs de contact appartiennent à l'entrée JSON | VCF 3.0 / 4.0 |
| `qrcode-to-vcard` | Image QR contenant un vCard complet | Aucun | Un VCF par contact détecté |
| `image-upscale` | Image à image unique | `scale` : 2 (par défaut), 3 ou 4 | PNG |
| `image-remove-background` | Image à image unique | Aucun | PNG transparent |
| `video-compress` | Vidéo | `compression_level` : léger, équilibré (par défaut), maximum | MP4, ou original si plus petit |
| `video-speed` | Vidéo | `speed` : 0.25–4, par défaut 2 | MP4 avec audio synchronisé et conservant la hauteur |
| `video-to-gif` | Vidéo | `start` : secondes, `duration` : 0.1–30, `fps` : 1–30, `width` : 64–1280 | Boucle GIF sans audio |
| `audio-to-text` | Audio | `language` : auto (par défaut), it, en ou un autre code de langue Whisper | TXT et horodatage JSON |

Installez uniquement les extras Python nécessaires :

```sh
python -m pip install 'onekit-tools[qrcode,images,background,transcription]'
```

Les opérations vidéo nécessitent également `ffmpeg` et `ffprobe` dans le PATH. Le CLI utilise la version installée FFmpeg ; les codecs pris en charge dépendent de cette version. `onekit doctor TOOL` vérifie les moteurs et packages requis.

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

Contact exemple JSON :

```json
{"first_name":"Ada","last_name":"Lovelace","version":"3.0","emails":["ada@example.org"]}
```

L'extraction QR accepte des charges complètes vCard 3.0/4.0 avec un nom d'affichage. Elle ne suit pas les URL de téléchargement de contacts et ne convertit pas de texte QR arbitraire en données de contact. L'agrandissement utilise le rééchantillonnage Lanczos, pas un modèle AI. La sortie est limitée à 40 millions de pixels. Les images animées sont rejetées par les adaptateurs d'image Python.

L’adaptateur CLI de suppression de l’arrière-plan charge directement U2Net avec ONNX Runtime, évitant la contrainte de dépendance Pillow <13 de rembg. Les modèles téléchargés sont vérifiés avec un checksum et mis en cache dans le cache local de modèles OneKit. Les moteurs de modèles optionnels restent séparés de l'extension portable `all`.
