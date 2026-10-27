<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="verify-digital-signature"></a>
# Vérifier la signature numérique

Commande : `onekit run signature-verify`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Sécurité**. Fidélité : **exacte**. Vérification cryptographique hors ligne des signatures PDF et CMS/P7M/P7S en utilisant les certificats intégrés. Les signatures détachées nécessitent le fichier original. Les chaînes de confiance, la révocation, le statut des signatures qualifiées et les horodatages de confiance ne sont pas vérifiés.

Types acceptés : `*`. Type de sortie : `json`. Accepte plusieurs entrées : **oui**.

Validation de l’entrée : **tout type de fichier**. Nombre de fichiers requis : **1–2**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : aucun.

Paquets Python : pypdf, asn1crypto, pycryptodome. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/signatures.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
