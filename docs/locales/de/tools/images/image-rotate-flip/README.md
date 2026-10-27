<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="rotate-and-flip-image"></a>
# Bild drehen und spiegeln

Befehl: `onekit run image-rotate-flip`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Bilder**. Wiedergabetreue: **exakt**. Wenden Sie die EXIF-Ausrichtung an, drehen Sie das Bild um 0, 90, 180 oder 270 Grad im Uhrzeigersinn und spiegeln Sie es anschließend horizontal, vertikal oder in beide Richtungen. Exportiert eine PNG-Datei ohne Metadaten; dekodierte Pixel und Transparenz bleiben erhalten. Nur Bilder mit einem Einzelbild werden unterstützt; maximal 40 Millionen Pixel.

Akzeptierte Typen: `png, jpeg, webp, gif, bmp, tiff, ico`. Ausgabetyp: `png`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **nach Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `angle`, `flip`.

Python-Pakete: Pillow. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/image_transform.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
