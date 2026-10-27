<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="extract-audio-from-video"></a>
# Extraire l'audio d'une vidéo

Commande : `onekit run video-extract-audio`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Vidéo**. Fidélité : **avec des compromis**. Extrait la première piste audio en tant que MP3 à 192 kbps en utilisant FFmpeg. Nécessite une vidéo contenant de l'audio ; le réencodage peut entraîner une perte de qualité.

Types acceptés : `mp4, webm, mkv, mov, avi, gif, mpeg, mpg, m4v, ogv, ts`. Type de sortie : `mp3`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : aucun.

Paquets Python : bibliothèque standard ou moteur externe. Moteurs externes : ffmpeg, ffprobe.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/video_edit.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
