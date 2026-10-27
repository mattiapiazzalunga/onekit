<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="excel-to-txt"></a>
# Da Excel a TXT

Comando: `onekit run xlsx-to-txt`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Convertitori**. Fedeltà: **con limitazioni**. Esporta un foglio di lavoro Excel come testo UTF-8 separato da tabulazioni. Usa i risultati delle formule salvate senza ricalcolo; la formattazione e gli altri fogli sono omessi.

Tipi accettati: `xlsx`. Tipo di output: `txt`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `sheet`.

Pacchetti Python: openpyxl. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/text_converters.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
