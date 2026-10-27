<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="url-inspector"></a>
# URL Prüfer

Befehl: `onekit run url-inspect`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Analyse**. Wiedergabetreue: **mit Einschränkungen**. Untersuchen Sie URL-Bestandteile, HTTP-Status, endgültige URL und verfügbare Antwort-Header direkt auf Ihrem Gerät. Zeichnet bis zu 10 HTTP-Weiterleitungen auf. Bei Netzwerkfehlern bleibt ein unvollständiger Bericht erhalten. Dies ist keine Prüfung auf Phishing, Schadsoftware, DNS-Eigenschaften oder Eigentümerschaft.

Akzeptierte Typen: `txt`. Ausgabetyp: `json`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **Text**. Erforderliche Dateianzahl: **1–1**. CLI: **16.384 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: keine.

Python-Pakete: Standardbibliothek oder externe Engine. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/link_tools.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
