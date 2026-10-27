<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="generate-barcode"></a>
# Genera codice a barre

Comando: `onekit run text-to-barcode`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Codici QR**. Fedeltà: **esatta**. Genera codici a barre Code 128, Code 39, EAN-13, EAN-8, UPC-A, ITF e ISBN-13 localmente. Le cifre di controllo del commercio al dettaglio sono validate o calcolate; gli identificatori non sono registrati o assegnati da OneKit.

Tipi accettati: `txt`. Tipo di output: `png`. Accetta più input: **no**.

Validazione dell’input: **testo**. Numero di file richiesto: **1–1**. CLI: **1,024 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `barcode_type`, `format`, `module_width`, `height`, `quiet_zone`, `show_text`, `font_size`, `dpi`.

Pacchetti Python: python-barcode, Pillow. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/barcode.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
