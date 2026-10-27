<a id="cli-localization"></a>
# Localisation de la CLI

Langues : `en`, `it`, `fr`, `es`, `de`, `ru`, `zh` (chinois simplifié). Sélectionnez-en un avec `onekit --language it ...`, ou `ONEKIT_LANGUAGE=it`. La locale du système d'exploitation est utilisée lorsqu'aucune n'est définie. Les locales non prises en charge utilisent l'anglais. Les noms de commandes, les clés d'options, les chemins, les identifiants de format et les contrats JSON lisibles par machine restent stables. L'aide humaine, le statut, les avertissements et les erreurs connues sont localisés. Les diagnostics des moteurs externes conservent leur texte initial.

Toute personne ou IA qui ajoute ou modifie un outil DOIT mettre à jour les sept catalogues de textes dans la même modification. Les noms, l’aide, les descriptions, les messages d’erreur, les avis, le README et la documentation des outils doivent conserver une correspondance un à un. Ne remplacez pas les traductions manquantes par de l’anglais. Préservez les espaces réservés, les exemples de code, les URL et les mentions légalement requises à l’identique. Vérifiez le sens et la terminologie en contexte.

Catalogues : `src/onekit/locales/{language}.json`. Code de présentation : `i18n.py`. Les messages en anglais sont des clés normalisées ; les algorithmes de traitement restent indépendants. Le registre de langue indépendant est `src/onekit/locales/languages.json`, incluant les alias du système d’exploitation. Ajoutez une entrée au registre et un catalogue complet ensemble. La terminologie révisée est enregistrée dans `scripts/localization-reviewed.json` ; appliquez-la avec `python scripts/apply_localization_review.py src/onekit/locales` avant l’audit.

1. Modifiez le message en anglais ou la documentation dans son fichier d’origine.
2. Exécutez `python scripts/localization_inventory.py`.
3. Mettez à jour tous les autres catalogues de langues et supprimez les entrées obsolètes. Les scripts de préparation peuvent produire des brouillons de traduction ; les textes générés doivent être relus.
4. Exécuter `python scripts/audit_localization.py` et `pytest tests/test_i18n.py`.
5. Exécutez `python scripts/localize_docs.py` pour régénérer les documents Markdown traduits dans `docs/locales/{language}/`, en conservant la structure relative des documents originaux.

La commande de création hors ligne prend un répertoire de modèle Argos local suivi de répertoires de catalogues. CTranslate2 et SentencePiece sont des dépendances pour la création, pas des exigences d'exécution CLI. Aucun service de traduction n'est contacté par le CLI.

Les traductions et la documentation du CLI sont maintenues indépendamment de tout site web qui intègre la bibliothèque de traitement. Seuls les liens d'utilisation publique appartiennent ici.
