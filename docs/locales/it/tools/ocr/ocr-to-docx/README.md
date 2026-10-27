<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="ocr-to-word"></a>
# Da OCR a Word

Comando: `onekit run ocr-to-docx`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **OCR**. Fedeltà: **con limitazioni**. Il riconoscimento dipende dalla qualità della scansione e dai pacchetti linguistici installati. Equazioni e layout potrebbero necessitare di correzione manuale.

Tipi accettati: `pdf, png, jpeg, webp, gif, bmp, tiff, ico`. Tipo di output: `docx`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `language`, `dpi`.

Pacchetti Python: pytesseract, Pillow, pypdfium2, python-docx. Motori esterni: tesseract.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/ocr/__init__.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
