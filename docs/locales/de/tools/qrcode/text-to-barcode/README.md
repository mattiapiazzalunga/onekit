<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="generate-barcode"></a>
# Erstellen Sie Barcode

Befehl: `onekit run text-to-barcode`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **QR-Codes**. Wiedergabetreue: **exakt**. Generiert Code 128, Code 39, EAN-13, EAN-8, UPC-A, ITF und ISBN-13 lokal. Einzelhandelsprüfziffern werden validiert oder berechnet; Kennungen werden von OneKit nicht registriert oder zugewiesen.

Akzeptierte Typen: `txt`. Ausgabetyp: `png`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **Text**. Erforderliche Dateianzahl: **1–1**. CLI: **1.024 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `barcode_type`, `format`, `module_width`, `height`, `quiet_zone`, `show_text`, `font_size`, `dpi`.

Python-Pakete: python-barcode, Pillow. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/barcode.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
