<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="color-picker"></a>
# Farbwähler

Befehl: `onekit run color-picker`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Design**. Wiedergabetreue: **exakt**. Lesen Sie einen sechsstelligen HEX-Farbwert aus einer TXT-Datei oder entnehmen Sie einen Pixelwert aus einem Bild, dessen Ausrichtung anhand der EXIF-Daten angepasst wurde. Gibt den sichtbaren sRGB-Farbwert, den ursprünglichen RGBA-Wert, den OKLCH-Farbwert und den Textkontrast aus. Transparente Pixel werden auf einem weißen Hintergrund zusammengesetzt.

Akzeptierte Typen: `png, jpeg, webp, gif, bmp, tiff, ico, txt`. Ausgabetyp: `json`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **nach Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `x`, `y`.

Python-Pakete: Pillow. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/photo_tools.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
