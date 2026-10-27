<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="decrypt-files-or-folders"></a>
# Décrypter des fichiers ou dossiers

Commande : `onekit run security-decrypt`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Sécurité**. Fidélité : **exacte**. AES-256 chiffré ZIP, compatible avec 7-Zip. Les noms de fichiers restent visibles. Perdre le mot de passe rend la récupération impossible.

Types acceptés : `zip`. Type de sortie : `*`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `password`, `restore`.

Paquets Python : pycryptodome, stream-zip, stream-unzip. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/security/__init__.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
