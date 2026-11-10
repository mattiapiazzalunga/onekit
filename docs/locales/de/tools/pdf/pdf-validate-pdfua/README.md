<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="validate-pdfua"></a>
# PDF/UA prüfen

Befehl: `onekit run pdf-validate-pdfua`. Verwenden Sie `onekit run --help` für Eingabe- und Ausgabeargumente.

Kategorie: **pdf*. Fidelity: **exact*. Prüfen Sie PDF/UA-1 automatisch mit einer lokalen Validierungsmaschine. Ein vorübergehendes Ergebnis erfordert noch eine manuelle Zugänglichkeitsprüfung. Der Bericht identifiziert den Motor, das Profil und die genaue Datei Hash.

Akzeptierte Typen: `pdf`. Ausgabetyp: `json`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **nach Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `profile`.

Python-Pakete: Standardbibliothek oder externe Engine. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Implementierung der Verarbeitung: [shared family adapter](../../../../../../src/onekit/tools/pdf_conformance.py). Verträge und Regressionsbeschläge: [tests](../../../../../../tests/test_core.py). Motor-Setup und Lizenzen: [engine guide](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
