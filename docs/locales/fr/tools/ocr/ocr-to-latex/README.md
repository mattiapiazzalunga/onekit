<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="ocr-to-latex"></a>
# OCR vers LaTeX

Commande : `onekit run ocr-to-latex`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **OCR**. Fidélité : **avec des compromis**. La reconnaissance dépend de la qualité du scan et des packs de langues installés. Les équations et la mise en page peuvent nécessiter une correction manuelle.

Types acceptés : `pdf, png, jpeg, webp, gif, bmp, tiff, ico`. Type de sortie : `latex`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **selon le type de fichier**. Nombre de fichiers requis : **1–1**. CLI : **134 217 728 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : `language`, `dpi`.

Paquets Python : pytesseract, Pillow, pypdfium2, python-docx. Moteurs externes : tesseract.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/ocr/__init__.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
