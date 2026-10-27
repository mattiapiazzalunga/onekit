<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="validate-json5"></a>
# Valider JSON5

Commande : `onekit run dev-validate-json5`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Développement**. Fidélité : **exacte**. La validation vérifie le parseur ou compilateur configuré ; les types à l’échelle du projet, imports et dépendances peuvent nécessiter un projet local.

Types acceptés : `json5, json, txt`. Type de sortie : `json`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **texte**. Nombre de fichiers requis : **1–1**. CLI : **8 388 608 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : aucun.

Paquets Python : json5. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/developer/__init__.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
