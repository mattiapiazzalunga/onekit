<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-pdf-watermark"></a>
# Rimuovi filigrana PDF

Comando: `onekit run pdf-remove-watermark`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **PDF**. Fedeltà: **con limitazioni**. Esamina e rimuove testo, immagini e singoli utilizzi di Form XObject selezionati, inclusi i Form XObject annidati e il testo codificato tramite font. Rimuove automaticamente gli artefatti contrassegnati come filigrane e le annotazioni di filigrana. Gli oggetti non contrassegnati richiedono una selezione o il testo esatto; le filigrane incorporate nei pixel non possono essere separate dalla loro immagine. Controlla ogni pagina.

Tipi accettati: `pdf`. Tipo di output: `pdf`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `text`, `mode`, `objects`.

Pacchetti Python: pypdf. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/pdf_design.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
