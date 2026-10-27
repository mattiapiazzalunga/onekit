<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="generate-barcode"></a>
# Générer un code-barres

Commande : `onekit run text-to-barcode`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Codes QR**. Fidélité : **exacte**. Génère localement des codes-barres Code 128, Code 39, EAN-13, EAN-8, UPC-A, ITF et ISBN-13. Les chiffres de contrôle de détail sont vérifiés ou calculés ; les identifiants ne sont pas enregistrés ou attribués par OneKit.

Types acceptés : `txt`. Type de sortie : `png`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **texte**. Nombre de fichiers requis : **1–1**. CLI : **1 024 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `barcode_type`, `format`, `module_width`, `height`, `quiet_zone`, `show_text`, `font_size`, `dpi`.

Paquets Python : python-barcode, Pillow. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/barcode.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
