<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="pdf-text-editing"></a>
# Édition de texte PDF

Vérifiez le fichier source pour obtenir des identifiants de boîte de texte stables et le texte original :

```python
from onekit.api import execute
from onekit.models import Artifact

source = Artifact("document.pdf", open("document.pdf", "rb").read())
inspection = execute("pdf-edit", [source], {"mode": "inspect"})
box = inspection.details["pages"][0]["runs"][0]
result = execute("pdf-edit", [source], {
    "edits": [{"page": 1, "id": box["id"], "original": box["text"], "text": "Updated text"}]
})
open("edited.pdf", "wb").write(result.files[0].data)
```

Le CLI accepte le même objet d'options via `--options`. `edits` peut être un tableau JSON ou une chaîne contenant ce tableau. Le mode inspection produit `*.text-boxes.json` ; le mode édition produit `*.edited.pdf`. Gardez le PDF original inchangé entre l'inspection et l'édition. Les identifiants obsolètes, les modifications en double et le texte d'origine non correspondant sont rejetés.

Les documents numérisés nécessitent d’abord un OCR. La modification directe n’est pas proposée pour le texte des objets Form XObject réutilisables, les opérateurs de texte à apostrophe ou à guillemets, l’écriture verticale et le texte servant de masque de découpe. Les polices dont les tables de correspondance sont incomplètes peuvent également être indisponibles. Le caractère à insérer doit exister dans la table de correspondance de la police d’origine ; le moteur signale les caractères non pris en charge au lieu de changer de police sans avertissement. La modification porte sur une seule ligne et ne redistribue pas les paragraphes. Utilisez un outil de masquage définitif dédié pour supprimer les informations confidentielles, y compris leurs copies dans les annotations, l’historique du document, les métadonnées ou d’autres objets PDF.

Les options précédentes `text`, `x`, `y`, `page` restent disponibles pour les scripts qui ajoutent des superpositions de texte. Fournissez `edits` pour remplacer le texte existant.
