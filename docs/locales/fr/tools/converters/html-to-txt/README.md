<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="html-to-txt"></a>
# HTML vers TXT

Commande : `onekit run html-to-txt`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Convertisseurs**. Fidélité : **avec des compromis**. Extrait le texte lisible du corps HTML sans exécuter de scripts ni récupérer de ressources. La mise en forme, les images, le contenu masqué et les styles sont omis.

Types acceptés : `html`. Type de sortie : `txt`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **texte**. Nombre de fichiers requis : **1–1**. CLI : **8 388 608 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : aucun.

Paquets Python : bibliothèque standard ou moteur externe. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/text_converters.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
