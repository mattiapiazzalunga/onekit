<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="image-to-pdf"></a>
# Images vers PDF

Commande : `onekit run image-to-pdf`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Convertisseurs**. Fidélité : **avec des compromis**. Le formatage, les polices, la mise en page, les formules ou les éléments non pris en charge peuvent changer. Les PDF scannés nécessitent OCR d'abord.

Types acceptés : `png, jpeg, webp, gif, bmp, tiff, ico`. Type de sortie : `pdf`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **67 108 864 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : aucun.

Paquets Python : Pillow. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/converters/__init__.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
