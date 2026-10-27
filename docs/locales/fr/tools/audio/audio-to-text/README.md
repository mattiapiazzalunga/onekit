<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="audio-to-text"></a>
# Audio en texte

Commande : `onekit run audio-to-text`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Audio**. Fidélité : **avec des compromis**. Transcrit localement avec Whisper tiny (multilingue). Le modèle se télécharge lors de la première utilisation ; aucun audio n’est téléversé. La reconnaissance peut faire des erreurs.

Types acceptés : `mp3, wav, flac, ogg, aac, m4a, mp4, aif, aiff, opus, wma`. Type de sortie : `txt`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `language`.

Paquets Python : faster-whisper. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/transcription.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
