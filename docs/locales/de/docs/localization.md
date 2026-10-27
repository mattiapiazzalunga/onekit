<a id="cli-localization"></a>
# CLI-Lokalisierung

Sprachen: `en`, `it`, `fr`, `es`, `de`, `ru`, `zh` (vereinfachtes Chinesisch). Wählen Sie eine mit `onekit --language it ...` oder `ONEKIT_LANGUAGE=it`. Die Betriebssystem-Lokalisierung wird verwendet, wenn keine von beiden eingestellt ist. Nicht unterstützte Lokalisierungen verwenden Englisch. Befehlsnamen, Optionsschlüssel, Pfade, Formatkennungen und maschinenlesbare JSON-Verträge bleiben unverändert. Menschliche Hilfe, Status, Warnungen und bekannte Fehler werden lokalisiert. Externe Engine-Diagnosen behalten ihren ursprünglichen Text.

Jede Person oder KI, die ein Werkzeug hinzufügt oder ändert, MUSS alle sieben Textkataloge in derselben Änderung aktualisieren. Namen, Hilfe, Beschreibungen, Fehlermeldungen, Hinweise, README und Werkzeugdokumentation müssen einander eins zu eins entsprechen. Ersetzen Sie fehlende Übersetzungen nicht durch englische Texte. Platzhalter, Codebeispiele, URLs und gesetzlich vorgeschriebene wörtliche Hinweise müssen unverändert bleiben. Prüfen Sie Bedeutung und Terminologie im Zusammenhang.

Kataloge: `src/onekit/locales/{language}.json`. Präsentationscode: `i18n.py`. Englische Nachrichten sind normalisierte Schlüssel; Verarbeitungsalgorithmen bleiben unabhängig. Das unabhängige Sprachregister ist `src/onekit/locales/languages.json`, einschließlich Betriebssystem-Aliase. Fügen Sie einen Registry-Eintrag und einen vollständigen Katalog zusammen hinzu. Überprüfte Terminologie wird in `scripts/localization-reviewed.json` aufgezeichnet; wende sie mit `python scripts/apply_localization_review.py src/onekit/locales` an, bevor Sie ein Audit durchführen.

1. Bearbeiten Sie die englische Nachricht oder Dokumentation in der Originaldatei.
2. Führen Sie `python scripts/localization_inventory.py` aus.
3. Aktualisieren Sie alle anderen Sprachkataloge und entfernen Sie veraltete Einträge. Die Vorbereitungsskripte können Übersetzungsentwürfe erzeugen; generierte Texte müssen überprüft werden.
4. Führen Sie `python scripts/audit_localization.py` und `pytest tests/test_i18n.py` aus.
5. Führen Sie `python scripts/localize_docs.py` aus, um die übersetzten Markdown-Dokumente unter `docs/locales/{language}/` neu zu erzeugen und dabei die relative Struktur der Originaldokumente beizubehalten.

Der Offline-Autor-Befehl benötigt ein lokales Argos-Modellverzeichnis, gefolgt von Katalogverzeichnissen. CTranslate2 und SentencePiece sind Autor-Abhängigkeiten, keine CLI-Laufzeitanforderungen. Es wird kein Übersetzungsdienst vom CLI kontaktiert.

Die Übersetzungen und Dokumentation der CLI werden unabhängig von jeder Website gepflegt, die die Prozessbibliothek einbettet. Nur öffentliche Nutzungslinks gehören hierhin.
