<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="regex-tester"></a>
# Tester regex

Comando: `onekit run dev-regex-test`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Sviluppo**. Fedeltà: **esatta**. Testa le espressioni regolari JavaScript localmente con catture, gruppi nominati, posizioni UTF-16 e sostituzioni. Fino a 128 KiB di testo, 1000 corrispondenze e 1 MiB di output. L’esecuzione ha limiti di tempo; la CLI richiede Node.js.

Tipi accettati: `txt`. Tipo di output: `json`. Accetta più input: **no**.

Validazione dell’input: **testo**. Numero di file richiesto: **1–1**. CLI: **131,072 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `pattern`, `flags`, `max_matches`, `enable_replacement`, `replacement`.

Pacchetti Python: libreria standard o motore esterno. Motori esterni: node.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/regex_tester.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
