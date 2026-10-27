<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-text-formatting"></a>
# Supprimer la mise en forme du texte

Commande : `onekit run text-strip-formatting`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Analyse**. Fidélité : **avec des compromis**. Transformez du texte collé, des fichiers texte UTF-8/UTF-16, HTML, Markdown ou le texte principal d’un document Word DOCX en un fichier UTF-8 TXT localement. Supprime les styles, les liens et le balisage tout en conservant un texte lisible et les sauts de paragraphe/tableau de base. Le texte brut conserve la ponctuation littérale. Pas de OCR ; les en-têtes, pieds de page, images et commentaires DOCX sont omis. Jusqu'à 8 MiB par entrée.

Types acceptés : `txt, html, md, docx`. Type de sortie : `txt`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **tout type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **8 388 608 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `input_format`.

Paquets Python : markdown-it-py, defusedxml. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/plain_text.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
