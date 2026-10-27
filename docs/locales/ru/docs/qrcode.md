<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="qr-codes"></a>
# QR коды

<a id="standard-linear-barcodes"></a>
## Standard linear barcodes

```sh
onekit run text-to-barcode identifier.txt -o barcode.png --options '{"barcode_type":"ean13"}'
onekit run text-to-barcode identifier.txt -o barcode.svg --options '{"barcode_type":"code128","format":"svg"}'
onekit run scan-barcode photo.jpg -o decoded.json
onekit run barcode-to-text photo.jpg -o identifier.txt
```

Стандарты: `code128` (по умолчанию, до 60 печатаемых символов ASCII), `code39` (до 48 заглавных букв/цифр и поддерживаемых символов, без дополнительной Mod-43 контрольной суммы), `ean13` (12 цифр или 13 с контрольной суммой), `ean8` (7/8), `upca` (11/12), `itf` (четное количество цифр, до 80), `isbn13` (EAN-13 начиная с 978/979). Предоставленные розничные контрольные цифры должны быть правильными; они никогда не заменяются без уведомления. Пропущенные цифры вычисляются. Идентификаторы не присваиваются и не регистрируются OneKit.

Установите `python -m pip install "onekit-tools[qrcode]"`. Вся обработка QR происходит локально и работает офлайн после установки зависимостей. Генерация QR использует Segno; сканирование CLI использует ZXing-C++ и Pillow.

| Инструмент | Входные данные | Выходные данные |
| --- | --- | --- |
| `text-to-qrcode` | UTF-8 TXT | PNG или SVG |
| `url-to-qrcode` | TXT, содержащий HTTP(S) URL | PNG или SVG |
| `wifi-to-qrcode` | Wi-Fi JSON | PNG или SVG |
| `vcard-to-qrcode` | Контакт JSON или существующий VCF | PNG или SVG |
| `scan-qrcode` | PNG, JPEG, WebP, BMP или GIF | JSON отчет |
| `reverse-qrcode` | Изображение QR | Исходный и интерпретированный контент в JSON |
| `qrcode-to-text` | Изображение QR | Точный сохранённый текст |
| `qrcode-to-json` | Изображение QR | Значение оригинала JSON или отчёт по другим полезным нагрузкам |

```sh
onekit run text-to-qrcode message.txt -o code.png
onekit run url-to-qrcode link.txt -o code.svg --options '{"format":"svg","error_correction":"Q"}'
onekit run wifi-to-qrcode network.json -o wifi.png
onekit run vcard-to-qrcode contact.json -o output/ --options '{"include_payload":true}'
onekit run scan-qrcode photo.jpg -o decoded.json
onekit run qrcode-to-json code.png -o recovered.json
```

Варианты генерации: `format` (`png`/`svg`), `error_correction` (`L`/`M`/`Q`/`H`), `scale` (2–16 пикселей на модуль), `border` (4–16 модулей), `dark` и `light` (шестизначный hex, контраст ≥ 4.5:1), и `include_payload` (также экспортировать закодированные TXT/JSON/VCF). По умолчанию: PNG, M, масштаб 8, граница 4, черное на белом. SVG масштабируется для печати. Ввод ограничен 16 KiB, но вместимость QR меньше и зависит от коррекции; сократите слишком длинные контакты или уменьшите коррекцию. URL фотографий сохраняются без загрузки изображения.

Пример Wi-Fi:

```json
{"ssid":"Guest Wi-Fi","security":"WPA","password":"example-password","hidden":false}
```

Безопасность: `WPA` (WPA/WPA2 личный), `WEP`, `nopass` (открытый), `SAE` (WPA3), `WPA2-EAP` (корпоративный). Корпоративный добавляет `identity`, `anonymous_identity`, `eap`, `phase2`. WPA3 и поддержка корпоративного варианта зависят от телефона. Пароли остаются читаемыми в нагрузке QR. Специальные символы используют [ZXing Wi-Fi конвенцию экранирования ](https://github.com/zxing/zxing/wiki/Barcode-Contents#wi-fi-network-config-android-ios-11).

Контакт пример:

```json
{
  "version":"4.0", "formatted_name":"Ada Lovelace",
  "first_name":"Ada", "last_name":"Lovelace", "organization":"Example",
  "phones":[{"value":"+390123456789","type":"work,voice","preferred":true,"label":"Office"}],
  "emails":[{"value":"ada@example.org","type":"work"}],
  "urls":["https://example.org"],
  "addresses":[{"street":"Example Street 1","city":"Milano","postal_code":"20100","country":"Italy","type":"work"}],
  "social_profiles":[{"value":"https://www.linkedin.com/in/example","type":"linkedin"}],
  "birthday":"1815-12-10", "categories":["Work","Research"], "note":"Example contact"
}
```

Дополнительные поля: `prefix`, `middle_name`, `suffix`, `nickname`, `department`, `title`, `role`, `anniversary`, `gender` (M/F/O/N/U), `language`, `timezone`, `uid`, `photo_url`, `latitude`, `longitude`. Даты задаются в формате YYYY-MM-DD. Адреса также поддерживают `po_box`, `extended`, `region`, `label`, `preferred`. Повторяющиеся записи телефонов/email/URL/соцсетей допускают `value`, `type`, `label`, `preferred`, с максимумом 20 записей в списке. Простые строковые записи тоже принимаются. vCard 3.0 — по умолчанию; 4.0 использует современные параметры предпочтений и текстовые значения. Перенос длинных строк UTF-8 и экранирование текста следуют [vCard](https://www.rfc-editor.org/rfc/rfc6350). Пользовательские метки используют группированные свойства X-ABLabel; поддержка необязательных полей зависит от программы чтения контактов.

Обратное декодирование отображает сохраненный текст и классифицирует ссылки, данные Wi-Fi, vCard и JSON. Он не может восстановить генератор, исходные настройки, исходное фото или содержимое за URL. `qrcode-to-json` возвращает исходный JSON, когда найден один символ JSON; в противном случае он возвращает `{ "count": ..., "codes": [...] }` с необработанным текстом и интерпретированными полями.

Формы модулей: `shape=square` (по умолчанию), `shape=rounded` или `shape=dots`. Выбранная форма применяется к модулям данных и коррекции ошибок при экспорте PNG и SVG. Маркеры поиска по умолчанию остаются квадратными и могут иметь закругленные углы с `corner_style=rounded`. Шаблоны выравнивания, тайминга и другие функциональные паттерны остаются квадратными. Размеры PNG всё равно следуют `scale` и `border`.

Экспорт JPEG (`format=jpeg`) доступен со всеми формами модулей и сплошным фоном. Используйте PNG или SVG, когда нужна прозрачность.

Выберите `corner_style=square` (по умолчанию) или `rounded` для трёх поисковых маркеров независимо от формы модулей. Добавьте центральный элемент с помощью `overlay_type=text` и `overlay_text` (1–16 символов) либо `overlay_type=image` и `overlay_image_base64` (PNG/JPEG в base64, до 2 MiB и 4 миллионов пикселей). `overlay_size` составляет 10–20 процентов QR-символа, по умолчанию 16. Центральные элементы принудительно включают коррекцию ошибок H. Средство отрисовки находит центральную область, содержащую только данные, и может уменьшить или слегка сместить элемент, чтобы сохранить функциональные узоры. Элемент имеет светлую подложку даже при прозрачном экспорте. Все эти параметры работают с PNG, JPEG и SVG.
