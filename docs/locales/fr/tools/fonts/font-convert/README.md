<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="convert-font"></a>
# Convertir la police

Commande : `onekit run font-convert`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Polices**. Fidélité : **exacte**. Modifie les conteneurs de police ; ne transforme pas les contours TrueType en contours CFF ou l’inverse.

Types acceptés : `ttf, otf, woff, woff2`. Type de sortie : `*`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **16 777 216 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `format`.

Paquets Python : fonttools, brotli. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/fonts/__init__.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
