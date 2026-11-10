<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="text-to-pdfua"></a>
# Text in PDF/UA

Befehl: `onekit run txt-to-pdfua`. Verwenden Sie `onekit run --help` für Eingabe- und Ausgabeargumente.

Kategorie: **pdf*. Fidelity: **exact*. Erstellen Sie einen getaggten PDF/UA-1 aus Klartext mit einem Titel und Sprache. Leere Linien separate Absätze. Lateinische Schriften nur; Lesen von Ordnung und Bedeutung überprüfen. Automatische Kontrollen ersetzen keine manuelle Zugänglichkeitsprüfung.

Akzeptierte Typen: `txt`. Ausgabetyp: `pdf`. Mehrere Eingaben möglich: **nein**.

Eingangsvalidierung: **text*. Erforderliche Dateizahl: **1–1**. CLI: **262,144 Bytes pro Datei**, **8,388,608 Bytes insgesamt*. Inhaltskontrollen laufen vor der Verarbeitung. Die Umbenennung einer Datei ändert ihr tatsächliches Format nicht.

Optionen: `title`, `language`.

Python Pakete: reportlab, pypdf, Pillow. Externe Motoren: siehe die Entwickler-Engine-Matrix für Sprachadapter.

Implementierung der Verarbeitung: [shared family adapter](../../../../../../src/onekit/tools/pdfua.py). Verträge und Regressionsbeschläge: [tests](../../../../../../tests/test_core.py). Motor-Setup und Lizenzen: [engine guide](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
