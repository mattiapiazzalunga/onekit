<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-image-watermark"></a>
# Bildwasserzeichen entfernen

Befehl: `onekit run image-remove-watermark`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Bilder**. Wiedergabetreue: **mit Einschränkungen**. Rekonstruieren Sie manuell ausgewählte Wasserzeichenbereiche aus den umliegenden Pixeln mit harmonischer Diffusion. Schätzt fehlende Inhalte; große Markierungen, Texturen und Gesichter lassen sich möglicherweise nicht überzeugend rekonstruieren. Keine automatische Markenerkennung.

Akzeptierte Typen: `png, jpeg, webp, gif, bmp, tiff, ico`. Ausgabetyp: `png`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **nach Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `regions`, `iterations`.

Python-Pakete: Pillow, numpy. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/photo_tools.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
