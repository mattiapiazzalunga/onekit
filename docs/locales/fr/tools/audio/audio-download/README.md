<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="download-audio"></a>
# Télécharger l'audio

Commande : `onekit run audio-download`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Audio**. Fidélité : **avec des compromis**. Téléchargez un fichier audio direct ou une source audio exposée par une page accessible. Le mode original préserve les octets téléchargés ; la conversion MP3 est avec perte. Jusqu'à 128 MiB. La connexion et les flux protégés peuvent empêcher les téléchargements. Utilisez uniquement avec permission.

Types acceptés : `txt`. Type de sortie : `*`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **texte**. Nombre de fichiers requis : **1–1**. CLI : **16 384 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `format`, `quality`.

Paquets Python : bibliothèque standard ou moteur externe. Moteurs externes : ffmpeg, ffprobe.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/link_tools.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
