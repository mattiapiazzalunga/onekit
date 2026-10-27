<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="input-validation"></a>
# Validation des entrées

Chaque entrée de catalogue déclare les formats acceptés, le nombre de fichiers et les limites en octets. `onekit list --json` expose les valeurs. L'exécution directe et les pipelines appliquent les contrats.

<a id="limits"></a>
## Limits

Les limites globales par lot sont de 128 MiB et 256 fichiers. Les entrées textuelles sont limitées à 8 MiB par fichier, les images matricielles à 64 MiB et les polices à 16 MiB. Une comparaison nécessite exactement deux entrées. Les images matricielles décodées sont limitées à 40 millions de pixels cumulés sur toutes les images de l’animation. Le contenu décompressé des archives et des fichiers Office est limité à 128 MiB et 4096 entrées.

Les outils à entrée unique rejettent les fichiers supplémentaires. Le mappage du pipeline applique délibérément une étape à entrée unique à chaque sortie précédente. Les collections de sortie sont vérifiées progressivement afin qu’une étape mappée ne puisse pas accumuler de données illimitées renvoyées. Les décomptes de fichiers, extensions et tailles CLI sont vérifiés avant la lecture du contenu des fichiers, et les octets réellement lus sont limités même si un fichier grossit pendant la lecture.

<a id="content-rules"></a>
## Content rules

- Les outils PDF nécessitent des en-têtes PDF et un emplacement final de référence croisée cohérent. `pdf-repair` permet délibérément des références croisées endommagées après avoir vérifié l'en-tête PDF ; son analyseur doit encore récupérer un vrai PDF. Les images renommées en `.pdf` sont rejetées.
- Les entrées raster sont vérifiées avec Pillow pour leur format réel, leur structure et leurs dimensions décodées. Un PNG renommé en JPEG est rejeté. L'export Base64 décode également l'image avant de l'accepter.
- Word, Excel et PowerPoint requièrent des parties de conteneur ZIP distinctes et des racines namespaced XML. Renommer Excel en `.docx` ne le transforme pas en Word. Les décomptes de répertoire et les budgets d'expansion sont examinés avant d'allouer la table des entrées ZIP ou de lire les parties du document.
- Les polices nécessitent des en-têtes SFNT/WOFF correspondants, des plages de tables valides limitées et des tailles cohérentes pour les polices compressées. L’expansion WOFF déclarée ne peut pas dépasser le budget en octets de la police.
- Les entrées médias ont des extensions audio/vidéo explicites et des signatures de conteneur. FFprobe vérifie les types de flux avant la conversion FFmpeg ; la conversion vidéo nécessite de la vidéo, et la conversion audio nécessite de l’audio sans flux vidéo ordinaire. La pochette jointe est autorisée. Les deux exécutables sont signalés par `doctor`.
- Les archives rejettent les chemins non sécurisés/dupliqués, les liens symboliques, les entrées chiffrées ZIP, les répertoires invalides, les répertoires multi-volumes/ZIP64 et les flux compressés concaténés non pris en charge. Les ratios d’expansion ZIP sont limités. La décompression TAR est limitée avant l’analyse des membres/PAX, avec une allocation fixe supplémentaire 4 MiB pour les en-têtes/paddings TAR ; la mémoire du décodeur XZ est aussi limitée.
- Le déchiffrement accepte uniquement le format crypté OneKit et authentifie son contenu avant la restauration de l’archive limitée. Les options de l’utilisateur ne peuvent pas augmenter le budget d’expansion imposé.
- Les outils de texte nécessitent du texte décodable sans octets de contrôle binaires. Les outils de développement acceptent leurs extensions de langage et l'entrée neutre `.txt` ; les adaptateurs shell/Dockerfile permettent également les sources sans extension. Les outils de validation acceptent intentionnellement des sources syntaxiquement invalides et renvoient `valid: false`. La conversion d'encodage utilise l'encodage source sélectionné ; les autres outils de texte nécessitent UTF-8..
- L’inspection, les adaptateurs de métadonnées et le chiffrement acceptent intentionnellement tous les types de fichiers. Leurs limites de nombre/octets s’appliquent toujours. Inspecter un fichier endommagé ou inconnu est une opération prise en charge, et non une raison de le refuser uniquement à cause de son contenu.
