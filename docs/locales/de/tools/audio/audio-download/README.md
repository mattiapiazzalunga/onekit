<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="download-audio"></a>
# Audio herunterladen

Befehl: `onekit run audio-download`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Audio**. Wiedergabetreue: **mit Einschränkungen**. Laden Sie eine direkte Audiodatei oder eine Audioquelle von einer zugänglichen Seite herunter. Der Originalmodus bewahrt die heruntergeladenen Bytes; MP3-Konvertierung ist verlustbehaftet. Bis zu 128 MiB. Login und geschützte Streams können Downloads verhindern. Nur mit Erlaubnis verwenden.

Akzeptierte Typen: `txt`. Ausgabetyp: `*`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **Text**. Erforderliche Dateianzahl: **1–1**. CLI: **16.384 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `format`, `quality`.

Python-Pakete: Standardbibliothek oder externe Engine. Externe Engines: ffmpeg, ffprobe.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/link_tools.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
