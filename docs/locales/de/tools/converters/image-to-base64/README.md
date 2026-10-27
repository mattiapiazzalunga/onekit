<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="image-to-base64"></a>
# Bilder in Base64

Befehl: `onekit run image-to-base64`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Konverter**. Wiedergabetreue: **exakt**. Strukturierte Konvertierung; die Ausgabe stellt die Quelldaten dar.

Akzeptierte Typen: `png, jpeg, webp, gif, bmp, tiff, ico`. Ausgabetyp: `base64`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **nach Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **67.108.864 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: keine.

Python-Pakete: Pillow. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/converters/__init__.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
