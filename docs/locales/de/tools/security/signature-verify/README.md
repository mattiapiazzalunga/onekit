<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="verify-digital-signature"></a>
# Digitale Signatur überprüfen

Befehl: `onekit run signature-verify`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Sicherheit**. Wiedergabetreue: **exakt**. Offline-Kryptoüberprüfung von PDF- und CMS/P7M/P7S-Signaturen mit eingebetteten Zertifikaten. Abgetrennte Signaturen benötigen die Originaldatei. Vertrauenskette, Widerruf, Status qualifizierter Signaturen und vertrauenswürdige Zeitstempel werden nicht geprüft.

Akzeptierte Typen: `*`. Ausgabetyp: `json`. Mehrere Eingaben möglich: **ja**.

Eingabevalidierung: **beliebiger Dateityp**. Erforderliche Dateianzahl: **1–2**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: keine.

Python-Pakete: pypdf, asn1crypto, pycryptodome. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/signatures.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
