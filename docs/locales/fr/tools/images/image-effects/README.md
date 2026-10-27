<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="blur-pixelate--image-effects"></a>
# Flou, pixelisation et effets d'image

Commande : `onekit run image-effects`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Images**. Fidélité : **avec des compromis**. Flou, pixelisation, flou de boîte, couverture solide ou niveaux de gris dans un seul outil. Appliquez sur toute l'image ou sur des zones sélectionnées, avec une intensité réglable et une nouvelle exportation PNG. Le flou et la pixelisation ne garantissent pas la suppression permanente des détails sensibles. Images à une seule trame uniquement.

Types acceptés : `png, jpeg, webp, gif, bmp, tiff, ico`. Type de sortie : `png`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `effect`, `scope`, `strength`, `color`, `regions`.

Paquets Python : Pillow. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/image_effects.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
