<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# QR codes

## Standard linear barcodes

```sh
onekit run text-to-barcode identifier.txt -o barcode.png --options '{"barcode_type":"ean13"}'
onekit run text-to-barcode identifier.txt -o barcode.svg --options '{"barcode_type":"code128","format":"svg"}'
onekit run scan-barcode photo.jpg -o decoded.json
onekit run barcode-to-text photo.jpg -o identifier.txt
```

Standards: `code128` (default, up to 60 printable ASCII characters), `code39` (up to 48 uppercase letters/digits and supported symbols, no optional Mod-43 checksum), `ean13` (12 digits or 13 including checksum), `ean8` (7/8), `upca` (11/12), `itf` (an even number of digits, up to 80), `isbn13` (EAN-13 beginning 978/979). Supplied retail check digits must be correct; they are never silently replaced. Omitted digits are calculated. Identifiers are not assigned or registered by OneKit.

Install `python -m pip install "onekit-tools[qrcode]"`. All QR processing is local and works offline after dependencies are installed. The website uses the same Segno generator as the CLI and a local JavaScript image decoder; CLI scanning uses ZXing-C++ and Pillow.

| Tool | Input | Output |
| --- | --- | --- |
| `text-to-qrcode` | UTF-8 TXT | PNG or SVG |
| `url-to-qrcode` | TXT containing an HTTP(S) URL | PNG or SVG |
| `wifi-to-qrcode` | Wi-Fi JSON | PNG or SVG |
| `vcard-to-qrcode` | Contact JSON or existing VCF | PNG or SVG |
| `scan-qrcode` | PNG, JPEG, WebP, BMP or GIF | JSON report |
| `reverse-qrcode` | QR image | Raw and interpreted content in JSON |
| `qrcode-to-text` | QR image | Exact stored text |
| `qrcode-to-json` | QR image | Original JSON value, or a report for other payloads |

```sh
onekit run text-to-qrcode message.txt -o code.png
onekit run url-to-qrcode link.txt -o code.svg --options '{"format":"svg","error_correction":"Q"}'
onekit run wifi-to-qrcode network.json -o wifi.png
onekit run vcard-to-qrcode contact.json -o output/ --options '{"include_payload":true}'
onekit run scan-qrcode photo.jpg -o decoded.json
onekit run qrcode-to-json code.png -o recovered.json
```

Generation options: `format` (`png`/`svg`), `error_correction` (`L`/`M`/`Q`/`H`), `scale` (2–16 pixels per module), `border` (4–16 modules), `dark` and `light` (six-digit hex, contrast ≥4.5:1), and `include_payload` (also export encoded TXT/JSON/VCF). Defaults: PNG, M, scale 8, border 4, black on white. SVG scales for print. Input is limited to 16 KiB, but QR capacity is smaller and depends on correction; shorten oversized contacts or lower correction. Photo URLs are stored without fetching the image.

Wi-Fi example:

```json
{"ssid":"Guest Wi-Fi","security":"WPA","password":"example-password","hidden":false}
```

Security: `WPA` (WPA/WPA2 personal), `WEP`, `nopass` (open), `SAE` (WPA3), `WPA2-EAP` (enterprise). Enterprise adds `identity`, `anonymous_identity`, `eap`, `phase2`. WPA3 and enterprise support varies by phone. Passwords remain readable in the QR payload. Special characters use the [ZXing Wi-Fi escaping convention](https://github.com/zxing/zxing/wiki/Barcode-Contents#wi-fi-network-config-android-ios-11).

Contact example:

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

Additional fields: `prefix`, `middle_name`, `suffix`, `nickname`, `department`, `title`, `role`, `anniversary`, `gender` (M/F/O/N/U), `language`, `timezone`, `uid`, `photo_url`, `latitude`, `longitude`. Dates use YYYY-MM-DD. Addresses also support `po_box`, `extended`, `region`, `label`, `preferred`. Repeated phone/email/URL/social entries accept `value`, `type`, `label`, `preferred`, with up to 20 entries per list. Simple string entries are also accepted. vCard 3.0 is the default; 4.0 uses modern preference and text-value parameters. UTF-8 folding and text escaping follow [vCard](https://www.rfc-editor.org/rfc/rfc6350). Custom labels use grouped X-ABLabel properties; optional fields depend on the reader.

Reverse reveals stored text and classifies links, Wi-Fi, vCard and JSON. It cannot recover the generator, original settings, source photo or content behind a URL. `qrcode-to-json` returns the original JSON when one JSON symbol is found; otherwise it returns `{ "count": ..., "codes": [...] }` with raw text and interpreted fields.

Module shapes: `shape=square` (default), `shape=rounded`, or `shape=dots`. The selected shape applies to data and error-correction modules in PNG and SVG exports. Finder markers stay square by default and can use rounded corners with `corner_style=rounded`. Alignment, timing and other function patterns stay square. PNG dimensions still follow `scale` and `border`.

JPEG export (`format=jpeg`) is available with all module shapes and a solid background. Use PNG or SVG when transparency is needed.

Choose `corner_style=square` (default) or `rounded` for the three finder markers, independently from module shape. Add a center mark with `overlay_type=text` and `overlay_text` (1–16 characters), or `overlay_type=image` and `overlay_image_base64` (a base64 PNG/JPEG, up to 2 MiB and 4 million pixels). `overlay_size` is 10–20 percent of the QR symbol, default 16. Center marks force H error correction. The renderer finds a central data-only area and can shrink or slightly shift the mark to preserve function patterns. The mark has a light backing even for transparent exports. All these options work with PNG, JPEG and SVG.
