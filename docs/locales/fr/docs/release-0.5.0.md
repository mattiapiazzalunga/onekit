<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="onekit-050"></a>
# OneKit 0.5.0

Première version de la CLI hors ligne et de l’API Python de traitement, avec 230 outils pour les documents, les PDF, les images, les médias, les archives, les polices, les utilitaires de développement, les codes QR, les déclarations de licence et l’inspection de fichiers. L’installation de base n’a aucune dépendance à l’exécution ; les extras facultatifs et les moteurs externes activent les outils sélectionnés.

Comprend la validation des entrées limitées, des flux de travail réutilisables, la configuration des dépendances locales, des contrats de traitement spécifiques au format et l’inspection des licences basées sur la source. Les rapports de licence restent des estimations non vérifiées qui nécessitent une révision manuelle.

Les mises à jour de performances accélèrent la préparation d’images opaques et l’inspection de texte. Les importations inutilisées et les affectations redondantes du moteur de développement ont été supprimées.

Les moteurs de modèle sont optionnels : installez le `background` ou `transcription` supplémentaire si nécessaire. Le U2Net fonctionne directement avec le ONNX Runtime et un modèle mis en cache vérifié par checksum. Le Whisper utilise faster-whisper. Les fichiers restent locaux ; lors du premier lancement, les poids du modèle sont téléchargés. Le traitement vidéo nécessite FFmpeg et ffprobe. Le téléchargement de vidéos utilise l'extension séparée `video`.

Met à jour Pillow vers la version 13 et la version verrouillée de certifi pour corriger les problèmes signalés dans les avis publiés. Le groupe portable de dépendances optionnelles `all` reste distinct des moteurs de modèles et des fonctions de signature.
