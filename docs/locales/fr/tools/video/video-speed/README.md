<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="change-video-speed"></a>
# Changer la vitesse de la vidéo

Commande : `onekit run video-speed`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Vidéo**. Fidélité : **avec des compromis**. Traitement local avec FFmpeg. Le réencodage peut perdre de la qualité. La sortie GIF n'a pas d'audio.

Types acceptés : `mp4, webm, mkv, mov, avi, gif, mpeg, mpg, m4v, ogv, ts`. Type de sortie : `mp4`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `speed`.

Paquets Python : bibliothèque standard ou moteur externe. Moteurs externes : ffmpeg, ffprobe.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/video_edit.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
