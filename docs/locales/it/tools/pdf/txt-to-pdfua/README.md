<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="text-to-pdfua"></a>
# Testo in PDF/UA

Comando: `onekit run txt-to-pdfua`. Utilizzare `onekit run --help` per argomenti di input e output.

Categoria: **pdf**. Fidelity: **exact**. Creare un taggato PDF/UA-1 da testo semplice con un titolo e una lingua. Le linee vuote separano i paragrafi. Solo caratteri latini; rivedere l'ordine di lettura e il significato. I controlli automatici non sostituiscono la revisione manuale dell'accessibilità.

Tipi accettati: `txt`. Tipo di output: `pdf`. Accetta più input: **no**.

Convalida dell'input: **text**. Conto di file richiesto: **1-1**. CLI: **262,144 byte per file**, **8,388,608 bytes total**. I controlli dei contenuti vengono eseguiti prima dell'elaborazione. Rinominare un file non cambia il suo formato reale.

Opzioni: `title`, `language`.

Python pacchetti: reportlab, pypdf, Pillow. Motori esterni: vedere la matrice del motore dello sviluppatore per adattatori di lingua.

Esecuzione del processo: [shared adattatore famiglia ](../../../../../../src/onekit/tools/pdfua.py). Contratti e regressioni: [tests](../../../../../../tests/test_core.py). Configurazione motore e licenze: [engine guide](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
