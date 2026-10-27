<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="color-palette-generator"></a>
# Générateur de palette de couleurs

Commande : `onekit run color-palette`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Design**. Fidélité : **exacte**. Palettes OKLCH de cinq couleurs, avec réduction du chroma pour rester dans l’espace sRGB et contraste du texte selon WCAG. Les règles d’harmonie sont des principes de conception, pas des garanties d’accessibilité.

Types acceptés : `txt`. Type de sortie : `json`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **texte**. Nombre de fichiers requis : **1–1**. CLI : **128 octets par fichier**, **1 048 576 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `harmony`, `lightness`, `chroma`, `hue`, `format`.

Paquets Python : bibliothèque standard ou moteur externe. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/design.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
