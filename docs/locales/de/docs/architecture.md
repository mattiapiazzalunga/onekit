<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="architecture-and-extension-guide"></a>
# Architektur- und Erweiterungsleitfaden

`Artifact(name, data)` ist eine unveränderliche benannte Byte-Nutzlast. `Result(files, warnings, details)` enthält Ausgaben und Treuehinweise. `execute(tool_id, files, options)` validiert Verträge und importiert verzögert einen Verarbeitungsadapter. `pipeline(steps, files)` verknüpft Operationen und verarbeitet mehrere Ausgaben einzeln durch Schritte, die nur eine Eingabe akzeptieren.

Der Katalog definiert stabile IDs, Familien, akzeptierte und ausgegebene Typen, Multiplizität, Optionen, Genauigkeit, Grenzen und Abhängigkeiten. Verarbeitungsadapter sind unabhängig vom CLI-Dateisystemzugriff. Portable Namen verhindern Traversierung und reservierte Gerätenamen. CLI-Ausgaben überschreiben standardmäßig vorhandene Dateien nicht. Native Engine-Aufrufe verwenden Argument-Arrays, temporäre Verzeichnisse und begrenzte Timeouts.

Um ein Tool hinzuzufügen, implementiere seinen Familienadapter, deklariere den Katalogeintrag, fügen Sie semantische und fehlerhafte Eingaberegressionstests hinzu, deklariere optionale Abhängigkeiten und überprüfen Sie Lizenzen. Erstellen Sie Tool-Verzeichnisse mit `python scripts/tool_docs.py` neu. Dokumentiere Genauigkeit und Plattformanforderungen.


Die Verarbeitungs-API v1 wird in `contracts/processing-v1.json` beschrieben. Führen Sie `python scripts/check_contracts.py` aus, bevor Sie Änderungen einreichen. Hinzufügen von Tools, Formaten und Optionen ist kompatibel; Entfernen vorhandener IDs/Optionen, Ändern von Ausgabearten oder Einschränken von Eingangsverträgen erfordert eine explizite versionierte Migration. Interne Algorithmen und Handler-Organisation können sich ändern, ohne den öffentlichen Vertrag zu ändern.

`ExecutionContext` ermöglicht es Python-Aufrufern, Batch- und pro-Tool-Budgets zu senken und einen vertrauenswürdigen lokalen Medien-Metadaten-Leser bereitzustellen. Er akzeptiert keine Engine-Services über benutzerbereitgestellte Tool-Optionen. Kontexte sind unveränderlich, auf eine Ausführung beschränkt und werden von Pipeline-Schritten geteilt. CLI verwendet die standardmäßigen lokalen Engine-Services.

Der Node Quelladapter delegiert Formatierungs- und Minifizierungsregeln an `tools/developer/source_engine.mjs`. Sein Engine-Loader ist eine prozessbezogene Abhängigkeit; der Quelltext kann keine beliebigen Pakete oder ausführbaren Befehle auswählen.
