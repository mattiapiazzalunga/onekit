<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="validate-pdfa"></a>
# Valider PDF/A

Commande : `onekit run pdf-validate-pdfa`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **PDF**. Fidélité : **exacte**. Validez PDF/A-1b, 2b ou 3b avec pikepdf. Les constructions non supportées sont signalées comme non vérifiées, jamais comme conformes. Les autres niveaux de conformité ne sont pas supportés.

Types acceptés : `pdf`. Type de sortie : `json`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `profile`.

Paquets Python : pikepdf, jsonschema, fonttools. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/pdf/__init__.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
