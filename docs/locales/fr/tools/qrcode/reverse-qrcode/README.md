<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="reverse-qr-code"></a>
# Inverser le code QR

Commande : `onekit run reverse-qrcode`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Codes QR**. Fidélité : **exacte**. Lit localement les charges utiles QR à partir d'une image; l'inversion révèle le contenu stocké, pas l'image originale ni les paramètres du générateur. Aucun lien n'est ouvert automatiquement.

Types acceptés : `png, jpeg, webp, bmp, gif`. Type de sortie : `json`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **16 777 216 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : aucun.

Paquets Python : Pillow, zxing-cpp. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/qrcode.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
