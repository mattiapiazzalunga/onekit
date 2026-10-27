<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="encrypt-files-or-folders"></a>
# Dateien oder Ordner verschlüsseln

Befehl: `onekit run security-encrypt`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Sicherheit**. Wiedergabetreue: **exakt**. Mit AES-256 verschlüsseltes ZIP-Archiv, kompatibel mit 7-Zip. Dateinamen bleiben sichtbar. Bei Verlust des Passworts ist eine Wiederherstellung unmöglich.

Akzeptierte Typen: `*`. Ausgabetyp: `zip`. Mehrere Eingaben möglich: **ja**.

Eingabevalidierung: **beliebiger Dateityp**. Erforderliche Dateianzahl: **1–256**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `password`.

Python-Pakete: pycryptodome, stream-zip, stream-unzip. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/security/__init__.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
