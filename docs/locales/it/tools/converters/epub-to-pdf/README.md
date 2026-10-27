<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="epub-to-pdf"></a>
# Da EPUB a PDF

Comando: `onekit run epub-to-pdf`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Convertitori**. Fedeltà: **con limitazioni**. Esporta testo base in ordine di lettura EPUB. CSS, immagini, layout fisso e contenuti interattivi sono omessi; i libri criptati o protetti da DRM vengono rifiutati.

Tipi accettati: `epub`. Tipo di output: `pdf`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: nessuna.

Pacchetti Python: reportlab, Pillow, defusedxml. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/epub_pdf.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
