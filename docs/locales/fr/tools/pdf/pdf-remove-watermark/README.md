<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-pdf-watermark"></a>
# Supprimer le filigrane PDF

Commande : `onekit run pdf-remove-watermark`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **PDF**. Fidélité : **avec des compromis**. Inspectez et supprimez le texte, les images et les invocations de Form XObject sélectionnés, y compris les Form XObject imbriqués et le texte encodé à l’aide de polices. Supprime automatiquement les artefacts identifiés comme filigranes et les annotations de filigrane. Les objets non identifiés nécessitent une sélection ou le texte exact ; les marques fusionnées avec les pixels ne peuvent pas être séparées de leur image. Vérifiez chaque page.

Types acceptés : `pdf`. Type de sortie : `pdf`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `text`, `mode`, `objects`.

Paquets Python : pypdf. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/pdf_design.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
