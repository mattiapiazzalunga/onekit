<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="calculate-checksum"></a>
# Calculer la somme de contrôle

Commande : `onekit run file-checksum`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Analyse**. Fidélité : **exacte**. Calcule SHA-256, SHA-512, SHA-1 ou MD5 localement. Une somme de contrôle attendue facultative peut être comparée à un fichier. Une somme de contrôle ne vérifie pas une signature numérique ni ne garantit la sécurité d'un fichier.

Types acceptés : `*`. Type de sortie : `json`. Accepte plusieurs entrées : **oui**.

Validation de l’entrée : **tout type de fichier**. Nombre de fichiers requis : **1–20**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `algorithm`, `expected`.

Paquets Python : bibliothèque standard ou moteur externe. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/file_checksum.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
