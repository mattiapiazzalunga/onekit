<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="text-to-qr-code"></a>
# Testo in codice QR

Comando: `onekit run text-to-qrcode`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Codici QR**. Fedeltà: **esatta**. Crea localmente un codice standard QR. La capacità dipende dal contenuto e dalla correzione degli errori. Mantieni il margine vuoto attorno al codice e testa il codice prima di stampare.

Tipi accettati: `txt`. Tipo di output: `png`. Accetta più input: **no**.

Validazione dell’input: **testo**. Numero di file richiesto: **1–1**. CLI: **16,384 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `format`, `shape`, `corner_style`, `overlay_type`, `overlay_text`, `overlay_image_base64`, `overlay_size`, `error_correction`, `scale`, `border`, `dark`, `light`, `transparent_background`, `include_payload`.

Pacchetti Python: segno, Pillow. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/qrcode.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
