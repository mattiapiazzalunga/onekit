<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="regex-tester"></a>
# Testeur de regex

Commande : `onekit run dev-regex-test`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Développement**. Fidélité : **exacte**. Test des expressions régulières JavaScript localement avec captures, groupes nommés, positions UTF-16 et remplacement. Jusqu’à 128 KiB de texte, 1000 correspondances et 1 MiB de sortie. L’exécution est limitée dans le temps ; CLI nécessite Node.js.

Types acceptés : `txt`. Type de sortie : `json`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **texte**. Nombre de fichiers requis : **1–1**. CLI : **131 072 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `pattern`, `flags`, `max_matches`, `enable_replacement`, `replacement`.

Paquets Python : bibliothèque standard ou moteur externe. Moteurs externes : node.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/regex_tester.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
