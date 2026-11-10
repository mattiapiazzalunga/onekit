<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="validate-pdfua"></a>
# Verifica PDF/UA

Comando: `onekit run pdf-validate-pdfua`. Utilizzare `onekit run --help` per argomenti di input e output.

Categoria: **pdf**. Fidelity: **exact**. Controllare PDF/UA-1 automaticamente con un motore di validazione locale. Un risultato di passaggio richiede ancora una revisione manuale dell'accessibilità. Il rapporto identifica il motore, il profilo e l'hash del file esatto.

Tipi accettati: `pdf`. Tipo di output: `json`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `profile`.

Pacchetti Python: libreria standard o motore esterno. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Esecuzione del processo: [shared adattatore famiglia ](../../../../../../src/onekit/tools/pdf_conformance.py). Contratti e regressioni: [tests](../../../../../../tests/test_core.py). Configurazione motore e licenze: [engine guide](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
