<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="audio-license-checker"></a>
# Vérificateur de licence audio

Commande : `onekit run license-audio`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Licences**. Fidélité : **avec des compromis**. Une estimation basée sur des déclarations et des métadonnées, pas sur un certificat de droits ou une autorisation légale. Vérifiez chaque résultat avec la source originale et le détenteur des droits. Les informations manquantes ne signifient jamais que le contenu est libre d'utilisation. Les auteurs et les titulaires de droits peuvent être différents. Les fichiers sont analysés localement ; les liens sont téléchargés directement depuis leur source. Les archives sont limitées et les scans peuvent être incomplets.

Types acceptés : `mp3, wav, flac, ogg, aac, m4a, mp4, aif, aiff, opus, wma`. Type de sortie : `json`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **tout type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `ref`.

Paquets Python : license-expression, defusedxml. Moteurs externes : ffprobe.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/license_check.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
