<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="cli-requirements-verification"></a>
# Verifica requisiti CLI

`tests/test_requirements.py` controlla la copertura del catalogo, le invocazioni CLI e le pipeline malformate. `tests/test_core.py` verifica i contratti di elaborazione e la semantica dell'output. La validazione dell'input, l'espansione degli archivi, la crittografia e le protezioni del filesystem hanno test di regressione dedicati.

Esegui `python -m pytest -q` per la suite predefinita. I motori installati separatamente vengono testati con `python -m pytest -q -m native`; configura le dipendenze descritte in `docs/engines.md` prima di eseguire questi controlli. Superare la suite predefinita non verifica tutti i motori esterni o ogni piattaforma supportata.
