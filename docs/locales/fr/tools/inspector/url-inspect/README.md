<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="url-inspector"></a>
# Inspecteur URL

Commande : `onekit run url-inspect`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Analyse**. Fidélité : **avec des compromis**. Inspectez les composants URL, le statut HTTP, l’URL finale et les en-têtes de réponse disponibles directement depuis votre appareil. Enregistre jusqu’à 10 redirections HTTP. Les pannes réseau laissent un rapport partiel. Ce n'est pas une vérification de phishing, malware, DNS ou de propriété.

Types acceptés : `txt`. Type de sortie : `json`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **texte**. Nombre de fichiers requis : **1–1**. CLI : **16 384 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : aucun.

Paquets Python : bibliothèque standard ou moteur externe. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/link_tools.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
