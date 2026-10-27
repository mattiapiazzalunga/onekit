<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="edit-pdf"></a>
# Modifier PDF

Commande : `onekit run pdf-edit`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **PDF**. Fidélité : **avec des compromis**. Modifiez les zones de texte prises en charge avec la police d’origine. Le texte plus long est ajusté à la largeur d’origine. Les documents numérisés, le texte dans les objets Form XObject réutilisables et les caractères absents de la police ne peuvent pas être modifiés. Cet outil ne permet pas le masquage définitif des données. L’ancienne option de texte ajoute une superposition.

Types acceptés : `pdf`. Type de sortie : `pdf`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `mode`, `edits`, `password`, `text`, `x`, `y`, `page`.

Paquets Python : pycryptodome, pypdf, reportlab. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/pdf/__init__.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
