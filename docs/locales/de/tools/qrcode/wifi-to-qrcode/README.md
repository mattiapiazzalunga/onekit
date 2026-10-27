<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="wi-fi-to-qr-code"></a>
# Wi-Fi zu QR Code

Befehl: `onekit run wifi-to-qrcode`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **QR-Codes**. Wiedergabetreue: **exakt**. Erstellt lokal einen Standard-QR-Code. Die Kapazität hängt vom Inhalt und der Fehlerkorrektur ab. Halten Sie die Ruhezone ein und testen Sie den Code vor dem Drucken.

Akzeptierte Typen: `json`. Ausgabetyp: `png`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **Text**. Erforderliche Dateianzahl: **1–1**. CLI: **16.384 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `format`, `shape`, `corner_style`, `overlay_type`, `overlay_text`, `overlay_image_base64`, `overlay_size`, `error_correction`, `scale`, `border`, `dark`, `light`, `transparent_background`, `include_payload`.

Python-Pakete: segno, Pillow. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/qrcode.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
