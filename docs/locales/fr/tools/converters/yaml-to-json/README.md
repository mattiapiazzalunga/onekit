<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="yaml-to-json"></a>
# YAML vers JSON

Commande : `onekit run yaml-to-json`. Utilisez `onekit run --help` pour les arguments d’entrée et de sortie.

Catégorie : **Convertisseurs**. Fidélité : **exacte**. Les tableaux XML utilisent des enregistrements plats répétés. La conversion de JSON vers XML préserve les types à l’aide d’un schéma typé avec une racine et des éléments ; les attributs XML sont représentés par @ et le texte par #text dans le JSON. Les formules des feuilles de calcul ne sont pas évaluées ; la première feuille est utilisée par défaut. Vérifiez le schéma et les valeurs après la conversion.

Types acceptés : `yaml`. Type de sortie : `json`. Accepte plusieurs entrées : **non**.

Validation de l’entrée : **texte**. Nombre de fichiers requis : **1–1**. CLI : **8 388 608 octets par fichier**, **134 217 728 octets au total**. Le contenu est vérifié avant le traitement. Renommer un fichier ne modifie pas son format réel.

Options : aucun.

Paquets Python : PyYAML. Moteurs externes : consultez la matrice des moteurs pour les outils de développement afin de connaître les adaptateurs des langages de programmation.

Implémentation du traitement : [adaptateur partagé de la famille d’outils](../../../../../../src/onekit/tools/structured_data.py). Contrats et données de test de non-régression : [tests](../../../../../../tests/test_core.py). Configuration des moteurs et licences : [guide des moteurs](../../../docs/engines.md).

Ce répertoire est généré à partir du catalogue partagé par `python scripts/tool_docs.py`. Modifiez le registre et l'adaptateur de famille, ajoutez des données de test pour les tests de régression, puis régénérez le répertoire.
