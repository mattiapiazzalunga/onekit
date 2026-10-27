<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="permanently-redact-image"></a>
# Masquer définitivement des zones d’une image

Commande : `onekit run image-redact`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Images**. Fidélité : **avec des compromis**. Remplace les pixels sélectionnés par du noir uni et exporte un nouveau PNG opaque, sans métadonnées d’origine ni pixels cachés par la transparence. Seules les images à une seule trame sont acceptées. Le fichier d’origine reste inchangé.

Types acceptés : `png, jpeg, webp, gif, bmp, tiff, ico`. Type de sortie : `png`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `regions`.

Paquets Python : Pillow. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/redaction.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
