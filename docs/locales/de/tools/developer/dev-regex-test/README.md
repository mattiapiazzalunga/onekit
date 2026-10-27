<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="regex-tester"></a>
# Regex-Tester

Befehl: `onekit run dev-regex-test`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Entwicklung**. Wiedergabetreue: **exakt**. Testen Sie JavaScript reguläre Ausdrücke lokal mit Captures, benannten Gruppen, UTF-16 Positionen und Ersetzung. Bis zu 128 KiB Text, 1000 Übereinstimmungen und 1 MiB Ausgabe. Die Ausführung ist zeitlich begrenzt; das CLI erfordert Node.js.

Akzeptierte Typen: `txt`. Ausgabetyp: `json`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **Text**. Erforderliche Dateianzahl: **1–1**. CLI: **131.072 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `pattern`, `flags`, `max_matches`, `enable_replacement`, `replacement`.

Python-Pakete: Standardbibliothek oder externe Engine. Externe Engines: node.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/regex_tester.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
