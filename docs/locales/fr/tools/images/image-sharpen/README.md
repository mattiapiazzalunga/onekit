<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="sharpen-and-deblur-image"></a>
# Accentuer la netteté et réduire le flou d’une image

Commande : `onekit run image-sharpen`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Images**. Fidélité : **avec des compromis**. Masque flou ou déconvolution gaussienne Richardson-Lucy avec des limites de traitement. La réduction du flou repose sur un modèle de flou et peut amplifier le bruit ou les halos ; la récupération des détails manquants n’est pas garantie. La déconvolution est limitée à un million de pixels.

Types acceptés : `png, jpeg, webp, gif, bmp, tiff, ico`. Type de sortie : `png`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `method`, `radius`, `amount`, `iterations`.

Paquets Python : Pillow, numpy. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/photo_tools.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
