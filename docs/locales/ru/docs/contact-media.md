<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="contacts-image-enlargement-and-local-media-tools"></a>
# Контакты, увеличение изображений и локальные медиа-инструменты

| Инструмент | Входные данные | Параметры | Выходные данные |
| --- | --- | --- | --- |
| `vcard-generate` | Контакт JSON, как для `vcard-to-qrcode` | Поля контактных данных следует указывать во входном JSON | VCF 3.0 / 4.0 |
| `qrcode-to-vcard` | Изображение QR, содержащее полный vCard | Нет | Один VCF на обнаруженный контакт |
| `image-upscale` | Однокадровое изображение | `scale`: 2 (по умолчанию), 3 или 4 | PNG |
| `image-remove-background` | Однокадровое изображение | Нет | Прозрачный PNG |
| `video-compress` | Видео | `compression_level`: легкий, сбалансированный (по умолчанию), максимальный | MP4, или оригинальный, если он меньше |
| `video-speed` | Видео | `speed`: 0.25–4, по умолчанию 2 | MP4 с синхронизированным аудио и сохранением тональности |
| `video-to-gif` | Видео | `start`: секунды, `duration`: 0.1–30, `fps`: 1–30, `width`: 64–1280 | Циклический GIF без звука |
| `audio-to-text` | Аудио | `language`: авто (по умолчанию), it, en или другой языковой код Whisper | TXT и отметка времени JSON |

Устанавливайте только те дополнительные компоненты Python, которые нужны:

```sh
python -m pip install 'onekit-tools[qrcode,images,background,transcription]'
```

Для операций с видео также нужны `ffmpeg` и `ffprobe` в PATH. CLI использует установленную сборку FFmpeg; поддерживаемые кодеки зависят от этой сборки. `onekit doctor TOOL` проверяет необходимые движки и пакеты.

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

Контакт JSON пример:

```json
{"first_name":"Ada","last_name":"Lovelace","version":"3.0","emails":["ada@example.org"]}
```

Извлечение QR принимает полные полезные данные vCard 3.0/4.0 с отображаемым именем. Оно не следует за URL для загрузки контактов и не конвертирует произвольный текст QR в контактные данные. Масштабирование использует ресемплинг Lanczos, а не модель AI. Выход ограничен 40 миллионами пикселей. Анимированные изображения отклоняются адаптерами Python для изображений.

Адаптер CLI для удаления фона загружает U2Net напрямую с ONNX Runtime, избегая ограничения зависимости Pillow <13 в rembg. Загрузки моделей проверяются по контрольной сумме и кэшируются в локальном кэше моделей OneKit. Дополнительные движки моделей остаются отдельно от портативного `all`.
