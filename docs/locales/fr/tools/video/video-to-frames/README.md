<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="video-to-frames"></a>
# Vidéo vers images

Commande : `onekit run video-to-frames`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Vidéo**. Fidélité : **avec des compromis**. Extrait des images PNG d’une vidéo à l’aide de FFmpeg. Choisissez le début, la durée et la largeur. Jusqu’à 120 images : le mode conservant les images d’origine préserve chaque image de l’intervalle ; sinon, les instants d’extraction sont échantillonnés à la fréquence d’images demandée.

Types acceptés : `mp4, webm, mkv, mov, avi, gif, mpeg, mpg, m4v, ogv, ts`. Type de sortie : `png`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `start`, `duration`, `fps`, `width`, `all_frames`.

Paquets Python : Pillow. Moteurs externes : ffmpeg, ffprobe.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/video_edit.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
