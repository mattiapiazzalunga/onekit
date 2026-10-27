<a id="cli-localization"></a>
# Localizzazione della CLI

Lingue: `en`, `it`, `fr`, `es`, `de`, `ru`, `zh` (Cinese semplificato). Seleziona uno con `onekit --language it ...`, o `ONEKIT_LANGUAGE=it`. La localizzazione del sistema operativo viene usata quando nessuno dei due è impostato. Le localizzazioni non supportate usano l’inglese. I nomi dei comandi, le chiavi delle opzioni, i percorsi, gli identificatori di formato e i contratti JSON leggibili dalla macchina rimangono stabili. L’aiuto umano, lo stato, gli avvisi e gli errori conosciuti sono localizzati. Le diagnostiche del motore esterno mantengono il loro testo originale.

Ogni persona o AI che aggiunge o modifica uno strumento DEVE aggiornare tutti e sette i cataloghi dei testi nella stessa modifica. Nomi, guida, descrizioni, messaggi di errore, avvisi, README e documentazione degli strumenti devono mantenere una corrispondenza uno a uno. Non usare testi inglesi per colmare traduzioni mancanti. Mantieni intatti segnaposto, esempi di codice, URL e avvisi che la legge impone di riprodurre testualmente. Verifica significato e terminologia nel contesto.

Cataloghi: `src/onekit/locales/{language}.json`. Codice di presentazione: `i18n.py`. I messaggi in inglese sono chiavi normalizzate; gli algoritmi di elaborazione rimangono indipendenti. Il registro linguistico indipendente è `src/onekit/locales/languages.json`, inclusi alias del sistema operativo. Aggiungi una voce di registro e un catalogo completo insieme. La terminologia rivista è registrata in `scripts/localization-reviewed.json`; applicala con `python scripts/apply_localization_review.py src/onekit/locales` prima di un audit.

1. Modifica il messaggio o la documentazione in inglese nel suo file originale.
2. Esegui `python scripts/localization_inventory.py`.
3. Aggiorna tutti gli altri cataloghi linguistici e rimuovi le voci obsolete. Gli script di preparazione possono generare bozze di traduzione; i testi generati devono essere rivisti.
4. Esegui `python scripts/audit_localization.py` e `pytest tests/test_i18n.py`.
5. Esegui `python scripts/localize_docs.py` per rigenerare i documenti Markdown tradotti in `docs/locales/{language}/`, mantenendo la struttura relativa dei documenti originali.

Il comando di creazione offline richiede una directory locale del modello Argos seguita dalle directory del catalogo. CTranslate2 e SentencePiece sono dipendenze per la creazione, non requisiti di runtime CLI. Nessun servizio di traduzione viene contattato da CLI.

Le traduzioni e la documentazione della CLI sono mantenute indipendentemente da qualsiasi sito web che integri la libreria di elaborazione. Qui appartengono solo i link di utilizzo pubblico.
