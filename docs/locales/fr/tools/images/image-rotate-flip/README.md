<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="rotate-and-flip-image"></a>
# Faire pivoter et retourner l'image

Commande : `onekit run image-rotate-flip`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Images**. Fidélité : **exacte**. Appliquez l’orientation EXIF, faites pivoter de 0, 90, 180 ou 270 degrés dans le sens horaire, puis effectuez une symétrie horizontale, verticale ou les deux. Exporte un PNG sans métadonnées, en préservant les pixels décodés et la transparence. Uniquement des images à une seule trame, jusqu’à 40 millions de pixels.

Types acceptés : `png, jpeg, webp, gif, bmp, tiff, ico`. Type de sortie : `png`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `angle`, `flip`.

Paquets Python : Pillow. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/image_transform.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
