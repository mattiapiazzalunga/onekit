<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="add-watermark-to-pdf"></a>
# Ajouter un filigrane à PDF

Commande : `onekit run pdf-watermark`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **PDF**. Fidélité : **exacte**. Ajoute un texte ou un filigrane image PNG/JPEG à toutes les pages ou à certaines pages sélectionnées, en conservant le texte et les graphiques d'origine. Prend en charge le texte d'Europe de l'Ouest, une disposition simple ou répétée, la rotation et l'opacité. Le fichier original reste inchangé.

Types acceptés : `pdf`. Type de sortie : `pdf`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `text`, `pages`, `font`, `font_size`, `color`, `opacity`, `angle`, `position`, `layout`, `margin`, `watermark_type`, `image_base64`, `image_width`.

Paquets Python : pypdf, reportlab, Pillow. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/pdf.watermark/__init__.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
