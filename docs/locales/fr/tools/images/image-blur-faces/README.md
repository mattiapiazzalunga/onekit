<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="automatically-blur-faces"></a>
# Flouter automatiquement les visages

Commande : `onekit run image-blur-faces`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **images**. Fidélité : **avec compromis**. Détecte les visages localement avec YuNet et les floute dans un nouveau PNG. Vérifiez chaque visage avant de partager : la détection automatique peut en manquer et le floutage ne garantit pas l’anonymat. Images non animées, jusqu’à 16 millions de pixels.

Types acceptés : `png, jpeg, webp, gif, bmp, tiff, ico`. Type de sortie : `png`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : aucun.

Paquets Python : onnxruntime, numpy, Pillow. Moteurs externes : consultez la matrice des moteurs de développement pour les adaptateurs de langages.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/face_blur.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
