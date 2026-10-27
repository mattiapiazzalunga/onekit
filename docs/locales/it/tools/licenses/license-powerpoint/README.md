<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="powerpoint-license-checker"></a>
# Controllo licenze PowerPoint

Comando: `onekit run license-powerpoint`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Licenze**. Fedeltà: **con limitazioni**. Una stima basata su dichiarazioni e metadati, non su un certificato di diritti o autorizzazione legale. Verifica ogni risultato con la fonte originale e il detentore dei diritti. Le informazioni mancanti non significano mai libera utilizzazione. Autori e titolari dei diritti possono differire. I file vengono analizzati localmente; i link vengono scaricati direttamente dalla loro origine. Gli archivi hanno limiti e le scansioni possono essere incomplete.

Tipi accettati: `pptx, pptm, ppt`. Tipo di output: `json`. Accetta più input: **no**.

Validazione dell’input: **qualsiasi tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `ref`.

Pacchetti Python: license-expression, defusedxml, olefile. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/license_check.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
