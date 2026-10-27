<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="txt-to-pdf"></a>
# TXT vers PDF

Commande : `onekit run txt-to-pdf`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Convertisseurs**. Fidélité : **avec des compromis**. Crée un PDF avec un agencement de paragraphe de base à partir de texte brut. Les sauts de ligne originaux TXT deviennent des paragraphes ; les caractères non pris en charge ou le nombre excessif de pages sont signalés.

Types acceptés : `txt`. Type de sortie : `pdf`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **texte dans l’encodage sélectionné**. Nombre de fichiers requis : **1–1**. CLI : **8 388 608 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `source_encoding`.

Paquets Python : reportlab, Pillow. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/text_converters.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
