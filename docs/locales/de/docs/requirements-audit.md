<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="cli-requirements-verification"></a>
# CLI Anforderungsprüfung

`tests/test_requirements.py` überprüft die Katalogabdeckung, CLI Aufrufe und fehlerhafte Pipelines. `tests/test_core.py` überprüft Verarbeitungskontrakte und Ausgabesemantik. Eingabevalidierung, Archivdekompression, Verschlüsselung und Dateisystemschutz haben eigene Regressionstests.

Führen Sie `python -m pytest -q` für die Standard-Suite aus. Separat installierte Engines werden mit `python -m pytest -q -m native` getestet; stellen Sie die in `docs/engines.md` beschriebenen Abhängigkeiten bereit, bevor Sie diese Prüfungen ausführen. Das Bestehen der Standardsuite überprüft nicht alle externen Engines oder jede unterstützte Plattform.
