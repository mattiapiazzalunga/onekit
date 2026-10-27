<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="add-watermark-to-pdf"></a>
# Aggiungi filigrana a PDF

Comando: `onekit run pdf-watermark`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **PDF**. Fedeltà: **esatta**. Aggiunge un testo o un watermark immagine PNG/JPEG a tutte o alcune pagine, mantenendo il testo e la grafica originali. Supporta testo dell'Europa occidentale, layout singolo o ripetuto, rotazione e opacità. Il file originale non viene modificato.

Tipi accettati: `pdf`. Tipo di output: `pdf`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `text`, `pages`, `font`, `font_size`, `color`, `opacity`, `angle`, `position`, `layout`, `margin`, `watermark_type`, `image_base64`, `image_width`.

Pacchetti Python: pypdf, reportlab, Pillow. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/pdf.watermark/__init__.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
