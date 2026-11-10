<a id="cli-localization"></a>
# Localisation de la CLI

Langues: `en`, `it`, `fr`, `es`, `de`, `ru`, `zh` (chinois simplifié), `pt` (portugais), `hi` (hindi). Choisissez une avec `onekit --language it ...`, ou `ONEKIT_LANGUAGE=it`. Le local du système d'exploitation est utilisé lorsque ni l'un ni l'autre n'est réglé. Les locaux non pris en charge utilisent l'anglais. Les noms de commande, les touches d'option, les chemins, les identifiants de format et les contrats lisibles par machine JSON restent stables. L'aide humaine, le statut, les avertissements et les erreurs connues sont localisés. Les diagnostics externes des moteurs conservent leur texte en amont.

Chaque personne ou AI ajoutant ou modifiant un outil DOIT mettre à jour les neuf catalogues de présentation dans le même changement. Les noms, l'aide, les descriptions, les messages d'erreur, les avis, le README et la documentation de l'outil doivent demeurer dans une correspondance individuelle. Ne remplissez pas les traductions manquantes avec l'anglais comme raccourci. Garder intacts les détenteurs de place, les exemples de code, les URL et les avis écrits exigés par la loi. Examiner le sens et la terminologie dans leur contexte.

Catalogues : `src/onekit/locales/{language}.json`. Code de présentation : `i18n.py`. Les messages en anglais sont des clés normalisées ; les algorithmes de traitement restent indépendants. Le registre de langue indépendant est `src/onekit/locales/languages.json`, incluant les alias du système d’exploitation. Ajoutez une entrée au registre et un catalogue complet ensemble. La terminologie révisée est enregistrée dans `scripts/localization-reviewed.json` ; appliquez-la avec `python scripts/apply_localization_review.py src/onekit/locales` avant l’audit.

1. Modifiez le message en anglais ou la documentation dans son fichier d’origine.
2. Exécutez `python scripts/localization_inventory.py`.
3. Mettez à jour tous les autres catalogues de langues et supprimez les entrées obsolètes. Les scripts de préparation peuvent produire des brouillons de traduction ; les textes générés doivent être relus.
4. Exécuter `python scripts/audit_localization.py` et `pytest tests/test_i18n.py`.
5. Exécutez `python scripts/localize_docs.py` pour régénérer les documents Markdown traduits dans `docs/locales/{language}/`, en conservant la structure relative des documents originaux.

La commande de création hors ligne prend un répertoire de modèle Argos local suivi de répertoires de catalogues. CTranslate2 et SentencePiece sont des dépendances pour la création, pas des exigences d'exécution CLI. Aucun service de traduction n'est contacté par le CLI.

Les traductions et la documentation du CLI sont maintenues indépendamment de tout site web qui intègre la bibliothèque de traitement. Seuls les liens d'utilisation publique appartiennent ici.
