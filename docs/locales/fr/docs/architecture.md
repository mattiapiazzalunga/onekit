<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="architecture-and-extension-guide"></a>
# Guide d'architecture et d'extension

`Artifact(name, data)` est une charge utile d’octets nommée et immuable. `Result(files, warnings, details)` transporte les sorties et les avis de fidélité. `execute(tool_id, files, options)` valide les contrats et importe paresseusement un adaptateur de traitement. `pipeline(steps, files)` compose des opérations et mappe plusieurs sorties à travers des étapes à entrée unique.

Le catalogue définit les ID stables, les familles, les types acceptés et de sortie, la multiplicité, les options, la fidélité, les limites et les dépendances. Les adaptateurs de traitement sont indépendants de l’accès au système de fichiers CLI. Les noms portables refusent la traversée et les noms de périphériques réservés. Les écritures CLI conservent les fichiers existants par défaut. Les appels du moteur natif utilisent des tableaux d’arguments, des répertoires temporaires et des délais d’attente limités.

Pour ajouter un outil, implémentez son adaptateur de famille, déclarez l’entrée du catalogue, ajoutez des tests de régression sémantiques et pour entrées invalides, déclarez les dépendances optionnelles et vérifiez les licences. Régénérez les répertoires d’outils avec `python scripts/tool_docs.py`. Documentez la fidélité et les exigences de la plateforme.


L’API de traitement v1 est décrite dans `contracts/processing-v1.json`. Exécutez `python scripts/check_contracts.py` avant de soumettre des modifications. Ajouter des outils, formats et options est compatible ; supprimer des ID/options existants, changer le type de sortie ou restreindre les contrats d'entrée nécessite une migration explicite versionnée. Les algorithmes internes et l'organisation des gestionnaires peuvent changer sans modifier le contrat public.

`ExecutionContext` permet aux appelants Python de réduire les budgets par lot et par outil et de fournir un lecteur de métadonnées média local fiable. Il n'accepte pas les services moteur via des options d'outil fournies par l'utilisateur. Les contextes sont immuables, limités à une seule exécution et partagés par les étapes du pipeline. Le CLI utilise les services moteurs locaux par défaut.

L'adaptateur source Node délègue les règles de formatage et de minification à `tools/developer/source_engine.mjs`. Son chargeur de moteur est une dépendance au niveau du processus ; le texte source ne peut pas choisir des packages ou des commandes exécutables arbitraires.
