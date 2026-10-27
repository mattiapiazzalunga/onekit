<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="word-to-png"></a>
# Da Word a PNG

Comando: `onekit run docx-to-png`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Convertitori**. Fedeltà: **con limitazioni**. La formattazione, i font, il layout, le formule o elementi non supportati potrebbero cambiare. I PDF scansionati richiedono prima OCR.

Tipi accettati: `docx`. Tipo di output: `png`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `dpi`.

Pacchetti Python: pypdfium2, Pillow. Motori esterni: soffice.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/converters/__init__.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
