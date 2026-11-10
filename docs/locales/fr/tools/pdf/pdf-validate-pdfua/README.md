<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="validate-pdfua"></a>
# Vérifier PDF/UA

Commande : `onekit run pdf-validate-pdfua`. Utilisez `onekit run --help` pour les arguments d'entrée et de sortie.

Catégorie: **pdf**. Fidélité: **Exacte**. Vérifiez PDF/UA-1 automatiquement avec un moteur de validation local. Un résultat de passage nécessite toujours un examen manuel de l'accessibilité. Le rapport identifie le moteur, le profil et le hachage exact du fichier.

Types acceptés : `pdf`. Type de sortie : `json`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `profile`.

Paquets Python : bibliothèque standard ou moteur externe. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Mise en œuvre du traitement: [adaptateur familial partagé](../../../../../../src/onekit/tools/pdf_conformance.py). Contrats et appareils de régression: [tests](../../../../../../tests/test_core.py). Configuration du moteur et licences: [guide moteur](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
