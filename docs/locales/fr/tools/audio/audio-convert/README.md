<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="convert-audio"></a>
# Convertis l'audio

Commande : `onekit run audio-convert`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Audio**. Fidélité : **avec des compromis**. Les codecs disponibles dépendent de votre version FFmpeg ; le réencodage peut entraîner une perte de qualité.

Types acceptés : `mp3, wav, flac, ogg, aac, m4a, mp4, aif, aiff, opus, wma`. Type de sortie : `*`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `format`, `codec`, `bitrate`.

Paquets Python : bibliothèque standard ou moteur externe. Moteurs externes : ffmpeg, ffprobe.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/media/__init__.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
