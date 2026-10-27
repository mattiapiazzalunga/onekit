<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="compare-pdf-files"></a>
# Confronta i file PDF

Comando: `onekit run diff-pdf`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Confronto**. Fedeltà: **con limitazioni**. Confronta il testo estratto, non il layout visivo.

Tipi accettati: `pdf`. Tipo di output: `json`. Accetta più input: **sì**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **2–2**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: nessuna.

Pacchetti Python: pycryptodome, pypdf. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/diff/__init__.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
