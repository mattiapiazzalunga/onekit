<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="cli-requirements-verification"></a>
# Vérification des exigences CLI

`tests/test_requirements.py` vérifie la couverture du catalogue, les appels de la CLI et les pipelines mal formés. `tests/test_core.py` vérifie les contrats de traitement et la sémantique de sortie. La validation des entrées, l'expansion des archives, le cryptage et la protection du système de fichiers disposent de tests de régression dédiés.

Exécutez `python -m pytest -q` pour la suite par défaut. Les moteurs installés séparément sont testés avec `python -m pytest -q -m native` ; fournissez les dépendances décrites dans `docs/engines.md` avant d'exécuter ces vérifications. Réussir la suite par défaut ne vérifie pas tous les moteurs externes ni toutes les plateformes supportées.
