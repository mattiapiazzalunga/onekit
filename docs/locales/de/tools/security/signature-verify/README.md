<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="verify-digital-signature"></a>
# Digitale Signatur überprüfen

Befehl: `onekit run signature-verify`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Sicherheit**. Wiedergabetreue: **exakt**. Prüft PDF- und CMS-Signaturen lokal mit AdES-Validierung. Abgetrennte Signaturen benötigen die Originaldatei. Optional kann ein ZIP mit Signaturprüfdaten hinzugefügt werden. Fehlen Vertrauens- oder Sperrnachweise, ist das Ergebnis unbestimmt.

Akzeptierte Typen: `*`. Ausgabetyp: `json`. Mehrere Eingaben möglich: **ja**.

Eingabevalidierung: **beliebiger Dateityp**. Erforderliche Dateianzahl: **1–3**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: keine.

Python-Pakete: pypdf, asn1crypto, pycryptodome, pyhanko, pyhanko-certvalidator, cryptography, signxml, xsdata. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/signatures.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
