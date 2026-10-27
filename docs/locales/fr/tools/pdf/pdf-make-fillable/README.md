<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="make-pdf-fillable"></a>
# Rendre un PDF remplissable

Commande : `onekit run pdf-make-fillable`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **PDF**. Fidélité : **exacte**. Ajouter des champs de texte AcroForm nommés, des cases à cocher et des choix dans des listes déroulantes en utilisant des rectangles dont les coordonnées sont normalisées par rapport au coin supérieur gauche. Conserve les champs et contenus de page existants. Pas de détection automatique des champs vides ni de conversion XFA ; vérifiez la compatibilité avec le lecteur.

Types acceptés : `pdf`. Type de sortie : `pdf`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `fields`.

Paquets Python : pypdf. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/pdf_design.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
