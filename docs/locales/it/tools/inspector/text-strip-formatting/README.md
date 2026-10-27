<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-text-formatting"></a>
# Rimuovi formattazione del testo

Comando: `onekit run text-strip-formatting`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Analisi**. Fedeltà: **con limitazioni**. Trasforma testo incollato, file di testo UTF-8/UTF-16, HTML, Markdown o testo principale Word DOCX in un file UTF-8 TXT localmente. Rimuove stili, link e markup mantenendo testo leggibile e interruzioni base di paragrafi/tabelle. Il testo semplice preserva la punteggiatura letterale. Nessun OCR; intestazioni, piè di pagina, immagini e commenti DOCX sono omessi. Fino a 8 MiB per input.

Tipi accettati: `txt, html, md, docx`. Tipo di output: `txt`. Accetta più input: **no**.

Validazione dell’input: **qualsiasi tipo di file**. Numero di file richiesto: **1–1**. CLI: **8,388,608 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `input_format`.

Pacchetti Python: markdown-it-py, defusedxml. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/plain_text.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
