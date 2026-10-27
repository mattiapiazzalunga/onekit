<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="calculate-checksum"></a>
# Calcola checksum

Comando: `onekit run file-checksum`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Analisi**. Fedeltà: **esatta**. Calcola localmente SHA-256, SHA-512, SHA-1 o MD5. Si può confrontare un checksum opzionale previsto con un file. Un checksum non verifica una firma digitale né garantisce la sicurezza del file.

Tipi accettati: `*`. Tipo di output: `json`. Accetta più input: **sì**.

Validazione dell’input: **qualsiasi tipo di file**. Numero di file richiesto: **1–20**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `algorithm`, `expected`.

Pacchetti Python: libreria standard o motore esterno. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/file_checksum.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
