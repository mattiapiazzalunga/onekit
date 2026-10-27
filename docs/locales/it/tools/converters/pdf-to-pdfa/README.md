<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="pdf-to-pdfa"></a>
# Da PDF a PDF/A

Comando: `onekit run pdf-to-pdfa`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Convertitori**. Fedeltà: **con limitazioni**. Converti localmente in PDF/A-2b o 3b incorporando i font. Prima del download viene convalidato il file effettivamente prodotto. I contenuti non supportati possono essere rimossi o rifiutati; controlla il risultato.

Tipi accettati: `pdf`. Tipo di output: `pdfa`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `icc_profile`, `profile`.

Pacchetti Python: pdftopdfa, pikepdf, jsonschema, fonttools, pdfminer.six. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/converters/__init__.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
