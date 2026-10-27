<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="repair-photo-defects"></a>
# Fotomängel reparieren

Befehl: `onekit run image-repair`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Bilder**. Wiedergabetreue: **mit Einschränkungen**. Entfernen Sie kleine Flecken mit einem Medianfilter oder rekonstruieren Sie ausgewählte Bereiche durch harmonische Diffusion. Schätzt umgebende Farben; kann versteckte Originale nicht wiederherstellen oder jede fotografische Unvollkommenheit reparieren. Speichert ein neues PNG.

Akzeptierte Typen: `png, jpeg, webp, gif, bmp, tiff, ico`. Ausgabetyp: `png`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **nach Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `regions`, `iterations`, `size`.

Python-Pakete: Pillow, numpy. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/photo_tools.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
