<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="edit-pdf"></a>
# Modifica PDF

Comando: `onekit run pdf-edit`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **PDF**. Fedeltà: **con limitazioni**. Modifica le caselle di testo supportate usando il font originale. Il testo più lungo viene adattato alla larghezza originale. Non è possibile modificare scansioni, testo nei Form XObject riutilizzabili o caratteri non disponibili nel font. Questo strumento non oscura i dati in modo permanente. La precedente opzione per il testo aggiunge una sovrapposizione.

Tipi accettati: `pdf`. Tipo di output: `pdf`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `mode`, `edits`, `password`, `text`, `x`, `y`, `page`.

Pacchetti Python: pycryptodome, pypdf, reportlab. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/pdf/__init__.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
