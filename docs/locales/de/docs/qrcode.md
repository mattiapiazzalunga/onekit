<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="qr-codes"></a>
# QR Codes

<a id="standard-linear-barcodes"></a>
## Standard linear barcodes

```sh
onekit run text-to-barcode identifier.txt -o barcode.png --options '{"barcode_type":"ean13"}'
onekit run text-to-barcode identifier.txt -o barcode.svg --options '{"barcode_type":"code128","format":"svg"}'
onekit run scan-barcode photo.jpg -o decoded.json
onekit run barcode-to-text photo.jpg -o identifier.txt
```

Standards: `code128` (Standard, bis zu 60 druckbare ASCII-Zeichen), `code39` (bis zu 48 Großbuchstaben/Ziffern und unterstützte Symbole, ohne optionale Mod-43-Prüfsumme), `ean13` (12 Ziffern oder 13 einschließlich Prüfziffer), `ean8` (7/8), `upca` (11/12), `itf` (eine gerade Anzahl von Ziffern, bis zu 80), `isbn13` (EAN-13 mit dem Präfix 978/979). Angegebene Prüfziffern für Handelsbarcodes müssen korrekt sein; sie werden niemals stillschweigend ersetzt. Fehlende Prüfziffern werden berechnet. OneKit vergibt oder registriert keine Kennungen.

Installieren Sie `python -m pip install "onekit-tools[qrcode]"`. Alle QR-Verarbeitung ist lokal und funktioniert offline, nachdem die Abhängigkeiten installiert sind. Die QR-Erstellung nutzt Segno; CLI-Scans verwenden ZXing-C++ und Pillow.

| Werkzeug | Eingabe | Ausgabe |
| --- | --- | --- |
| `text-to-qrcode` | UTF-8 TXT | PNG oder SVG |
| `url-to-qrcode` | TXT, der ein HTTP(S) URL enthält | PNG oder SVG |
| `wifi-to-qrcode` | Wi-Fi JSON | PNG oder SVG |
| `vcard-to-qrcode` | Kontakt JSON oder vorhandene VCF | PNG oder SVG |
| `scan-qrcode` | PNG, JPEG, WebP, BMP oder GIF | JSON Bericht |
| `reverse-qrcode` | QR Bild | Roh- und interpretierte Inhalte in JSON |
| `qrcode-to-text` | QR Bild | Exakt gespeicherter Text |
| `qrcode-to-json` | QR Bild | Original JSON Wert oder ein Bericht für andere Payloads |

```sh
onekit run text-to-qrcode message.txt -o code.png
onekit run url-to-qrcode link.txt -o code.svg --options '{"format":"svg","error_correction":"Q"}'
onekit run wifi-to-qrcode network.json -o wifi.png
onekit run vcard-to-qrcode contact.json -o output/ --options '{"include_payload":true}'
onekit run scan-qrcode photo.jpg -o decoded.json
onekit run qrcode-to-json code.png -o recovered.json
```

Generationsoptionen: `format` (`png`/`svg`), `error_correction` (`L`/`M`/`Q`/`H`), `scale` (2–16 Pixel pro Modul), `border` (4–16 Module), `dark` und `light` (sechsstelliger Hex, Kontrast ≥4.5:1) und `include_payload` (auch kodierte TXT/JSON/VCF exportieren). Standardwerte: PNG, M, Maßstab 8, Rand 4, schwarz auf weiß. SVG skaliert für den Druck. Die Eingabe ist auf 16 KiB begrenzt, aber QR Kapazität ist kleiner und hängt von der Korrektur ab; zu große Kontakte kürzen oder Korrektur verringern. Foto-URLs werden gespeichert, ohne das Bild abzurufen.

Wi-Fi Beispiel:

```json
{"ssid":"Guest Wi-Fi","security":"WPA","password":"example-password","hidden":false}
```

Sicherheit: `WPA` (WPA/WPA2 persönlich), `WEP`, `nopass` (offen), `SAE` (WPA3), `WPA2-EAP` (Enterprise). Enterprise fügt `identity`, `anonymous_identity`, `eap`, `phase2` hinzu. WPA3 und Enterprise-Support variiert je nach Telefon. Passwörter bleiben im QR-Payload lesbar. Sonderzeichen verwenden die [ZXing Wi-Fi-Escaping-Konvention](https://github.com/zxing/zxing/wiki/Barcode-Contents#wi-fi-network-config-android-ios-11).

Kontakt Beispiel:

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

Zusätzliche Felder: `prefix`, `middle_name`, `suffix`, `nickname`, `department`, `title`, `role`, `anniversary`, `gender` (M/F/O/N/U), `language`, `timezone`, `uid`, `photo_url`, `latitude`, `longitude`. Datumsangaben verwenden YYYY-MM-DD. Adressen unterstützen auch `po_box`, `extended`, `region`, `label`, `preferred`. Wiederholte Telefon-/E-Mail-/URL-/Social-Einträge akzeptieren `value`, `type`, `label`, `preferred`, mit bis zu 20 Einträgen pro Liste. Einfache Texteingaben sind ebenfalls erlaubt. vCard 3.0 ist der Standard; 4.0 nutzt moderne Präferenzen und Textwert-Parameter. UTF-8-Zeilenfaltung und Text-Escaping folgen [vCard](https://www.rfc-editor.org/rfc/rfc6350). Benutzerdefinierte Labels nutzen gruppierte X-ABLabel-Eigenschaften; die Unterstützung optionaler Felder hängt vom Leseprogramm ab.

Die Dekodierung zeigt gespeicherten Text an und klassifiziert Links, Wi-Fi, vCard und JSON. Es kann den Generator, die ursprünglichen Einstellungen, das Originalfoto oder Inhalte hinter einem URL nicht wiederherstellen. `qrcode-to-json` gibt das ursprüngliche JSON zurück, wenn ein JSON-Symbol gefunden wird; andernfalls gibt es `{ "count": ..., "codes": [...] }` mit rohem Text und interpretierten Feldern zurück.

Modulformen: `shape=square` (Standard), `shape=rounded` oder `shape=dots`. Die ausgewählte Form gilt für Daten- und Fehlerkorrekturmodule in den PNG- und SVG-Exporten. Finder-Markierungen bleiben standardmäßig quadratisch und können mit `corner_style=rounded` abgerundete Ecken verwenden. Ausrichtungs-, Timing- und andere Funktionsmuster bleiben quadratisch. Die PNG-Abmessungen folgen weiterhin `scale` und `border`.

JPEG-Export (`format=jpeg`) ist mit allen Modulformen und einem einfarbigen Hintergrund verfügbar. Verwenden Sie PNG oder SVG, wenn Transparenz benötigt wird.

Wählen Sie `corner_style=square` (Standard) oder `rounded` für die drei Positionsmarkierungen, unabhängig von der Modulform. Fügen Sie einen zentralen Inhalt mit `overlay_type=text` und `overlay_text` (1–16 Zeichen) oder mit `overlay_type=image` und `overlay_image_base64` hinzu (Base64-PNG/JPEG, bis zu 2 MiB und 4 Millionen Pixel). `overlay_size` beträgt 10–20 Prozent des QR-Symbols, standardmäßig 16. Zentrale Inhalte erzwingen die Fehlerkorrektur H. Der Renderer findet einen zentralen Bereich, der ausschließlich Daten enthält, und kann den Inhalt verkleinern oder leicht verschieben, um Funktionsmuster zu erhalten. Der Inhalt hat auch bei transparenten Exporten einen hellen Hintergrund. Alle Optionen funktionieren mit PNG, JPEG und SVG.
