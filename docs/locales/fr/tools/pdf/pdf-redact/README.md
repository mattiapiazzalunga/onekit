<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="permanently-redact-pdf"></a>
# Masquer définitivement des données dans un PDF

Commande : `onekit run pdf-redact`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **PDF**. Fidélité : **avec des compromis**. Masque définitivement les zones sélectionnées et reconstruit chaque page à partir de pixels. Le texte, les pièces jointes, les commentaires, les formulaires et les métadonnées d’origine ne sont pas copiés ; le texte sélectionnable et la qualité vectorielle sont perdus. Le fichier d’origine reste inchangé.

Types acceptés : `pdf`. Type de sortie : `pdf`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `regions`, `dpi`.

Paquets Python : pypdfium2, Pillow, reportlab, pypdf. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/redaction.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
