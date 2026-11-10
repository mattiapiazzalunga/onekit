<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="text-to-pdfua"></a>
# Texte vers PDF/UA

Commande : `onekit run txt-to-pdfua`. Utilisez `onekit run --help` pour les arguments d'entrée et de sortie.

Catégorie: **pdf**. Fidélité: **Exacte**. Créez un libellé marqué PDF/UA-1 à partir d'un texte simple avec un titre et une langue. Les lignes blanches séparent les paragraphes. Polices latines seulement; relire l'ordre de lecture et le sens. Les vérifications automatiques ne remplacent pas l'examen manuel de l'accessibilité.

Types acceptés : `txt`. Type de sortie : `pdf`. Accepte plusieurs entrées : **non**.

Validation des entrées : **text**. Nombre de fichiers requis : **1–1**. CLI : **262 144 octets par dossier**, **8 388 608 octets au total**. Les vérifications de contenu sont effectuées avant le traitement. Renaming d'un fichier ne change pas son format réel.

Options : `title`, `language`.

Python paquets: reportlab, pypdf, Oreiller. Moteurs externes : voir la matrice du moteur développeur pour les adaptateurs de langage.

Mise en œuvre du traitement: [adaptateur familial partagé](../../../../../../src/onekit/tools/pdfua.py). Contrats et appareils de régression: [tests](../../../../../../tests/test_core.py). Configuration du moteur et licences: [guide moteur](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
