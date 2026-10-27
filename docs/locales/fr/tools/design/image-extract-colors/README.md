<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="extract-image-colors"></a>
# Extraire les couleurs de l'image

Commande : `onekit run image-extract-colors`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Design**. Fidélité : **exacte**. Extrait les couleurs dominantes par découpage médian à partir d’un échantillon de taille limitée de l’image. Exclut les pixels entièrement transparents ; les pixels partiellement transparents sont composités sur fond blanc. Les proportions de couleurs décrivent l’échantillon, et non les objets représentés.

Types acceptés : `png, jpeg, webp, gif, bmp, tiff, ico`. Type de sortie : `json`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `colors`.

Paquets Python : Pillow. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/photo_tools.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
