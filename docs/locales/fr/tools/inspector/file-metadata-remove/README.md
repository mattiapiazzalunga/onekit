<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-metadata"></a>
# Supprimer les métadonnées

Commande : `onekit run file-metadata-remove`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Analyse**. Fidélité : **exacte**. Conserve le contenu sélectionné ; validez les résultats importants.

Types acceptés : `*`. Type de sortie : `*`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **tout type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : aucun.

Paquets Python : bibliothèque standard ou moteur externe. Moteurs externes : exiftool.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/inspector/__init__.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
