<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="pdf-watermark"></a>
# PDF Wasserzeichen

In der Kategorie PDF laden Sie eine PDF hoch, geben Sie Text ein und passen Sie die Deckkraft, Farbe, Schriftart, Drehung und Position an. Die Vorschau zeigt die Wasserzeichenposition auf der ausgewählten Seite. Exportieren Sie, um das endgültige PDF Schriftbild zu überprüfen. Wählen Sie ein einzelnes Wasserzeichen oder ein wiederholtes 3 × 4 Raster. Der Text wird bei Bedarf automatisch verkleinert, um auf die Seite oder Zelle zu passen, bis zu einem Lesbarkeitslimit von sechs Punkten. Verschlüsselte PDFs müssen zuerst entsperrt werden. Bestehende digitale Signaturen sind nach der Bearbeitung eines Dokuments nicht mehr gültig; das Tool warnt, wenn Signaturfelder vorhanden sind.

```sh
onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"CONFIDENTIAL","pages":"1,3-5","opacity":0.25,"angle":45}'
onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"DRAFT","layout":"repeat","color":"#b00000"}'
```

| Option | Werte / Standard |
| --- | --- |
| `text` | 1–200 Zeichen, bis zu fünf Zeilen; Standard DRAFT |
| `pages` | Eins-basierte Bereiche, z. B. `1,3-5`; leer oder weggelassen bedeutet alle |
| `font` | Helvetica-Fett (Standard), Helvetica, Times-Roman, Courier |
| `font_size` | 8–160 Punkte; Standard 48, wird bei Bedarf automatisch angepasst |
| `color` | Sechsstellige Hexadezimalzahl; Standard #666666 |
| `opacity` | 0.05–1; Standard 0.25 |
| `angle` | -180–180 Grad, gegen den Uhrzeigersinn; Standard 45 |
| `position` | Zentrum, oben-links/zentral/rechts, mittig-links/rechts, unten-links/zentral/rechts |
| `layout` | einzeln (Standard) oder wiederholen (3 × 4 Raster; Position wird ignoriert) |
| `margin` | 0–144 Punkte; Standard 24 |

Schriftarten unterstützen westeuropäische Zeichen und Satzzeichen, einschließlich italienischer Akzente. Nicht unterstützte Zeichen führen zu einem offensichtlichen Fehler. Bis zu 512 Seiten können verarbeitet werden. Die Platzierung verwendet die visuell orientierte Beschnittbox und behält die ursprüngliche Drehung und Annotationskoordinaten bei. Ein Wasserzeichen kennzeichnet sichtbare Inhalte; es entfernt den zugrunde liegenden Inhalt nicht.
