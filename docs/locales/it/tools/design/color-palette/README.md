<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="color-palette-generator"></a>
# Generatore di Palette di Colori

Comando: `onekit run color-palette`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Design**. Fedeltà: **esatta**. Palette OKLCH di cinque colori, con riduzione del croma per rientrare nello spazio sRGB e contrasto del testo secondo WCAG. Le regole di armonia sono criteri di progettazione, non garanzie di accessibilità.

Tipi accettati: `txt`. Tipo di output: `json`. Accetta più input: **no**.

Validazione dell’input: **testo**. Numero di file richiesto: **1–1**. CLI: **128 byte per file**, **1,048,576 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `harmony`, `lightness`, `chroma`, `hue`, `format`.

Pacchetti Python: libreria standard o motore esterno. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/design.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
