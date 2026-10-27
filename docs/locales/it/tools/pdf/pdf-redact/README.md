<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="permanently-redact-pdf"></a>
# Oscura permanentemente un PDF

Comando: `onekit run pdf-redact`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **PDF**. Fedeltà: **con limitazioni**. Oscura permanentemente le aree selezionate e ricostruisce ogni pagina a partire da pixel raster. Testo, allegati, commenti, moduli e metadati originali non vengono copiati; si perdono il testo selezionabile e la qualità vettoriale. Il file originale resta invariato.

Tipi accettati: `pdf`. Tipo di output: `pdf`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `regions`, `dpi`.

Pacchetti Python: pypdfium2, Pillow, reportlab, pypdf. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/redaction.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
