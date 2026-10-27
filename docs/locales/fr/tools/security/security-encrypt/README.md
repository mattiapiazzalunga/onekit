<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="encrypt-files-or-folders"></a>
# Chiffrez des fichiers ou des dossiers

Commande : `onekit run security-encrypt`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Sécurité**. Fidélité : **exacte**. AES-256 chiffré ZIP, compatible avec 7-Zip. Les noms de fichiers restent visibles. Perdre le mot de passe rend la récupération impossible.

Types acceptés : `*`. Type de sortie : `zip`. Accepte plusieurs entrées : **oui**.

Validation de l’entrée : **tout type de fichier**. Nombre de fichiers requis : **1–256**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `password`.

Paquets Python : pycryptodome, stream-zip, stream-unzip. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/security/__init__.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
