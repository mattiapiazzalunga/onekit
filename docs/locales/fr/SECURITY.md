<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="security-policy"></a>
# Politique de sécurité

Signalez les vulnérabilités en privé à `security@onekit.org` avec version, plateforme, outil, versions des dépendances, impact et reproduction synthétique. Ne publiez pas de fichiers sensibles, identifiants ou rapports privés exploitables sur des trackers publics. Les correctifs visent la dernière version stable ; aucun délai de réponse n’est garanti.

Le cœur impose des limites aux chemins, aux tailles des entrées, à la décompression des archives, aux pixels des images, aux comparaisons et aux pipelines. Le chiffrement utilise AES-256-GCM authentifié avec un sel et un nonce renouvelés, ainsi que scrypt ; les mots de passe perdus ne peuvent pas être récupérés. Les fichiers de sortie existants sont préservés par défaut. La validation Python analyse le code source sans l’exécuter.

Les convertisseurs/compilateurs externes sont des programmes natifs séparés, pas un bac à sable complet. Gardez-les à jour et isolez les documents suspects en utilisant les contrôles du système d'exploitation. Le CLI n'est pas un service de conversion à distance sans authentification. Modifier un PDF signé peut invalider les signatures ; les permissions PDF ne sont pas équivalentes à l'intégrité du cryptage.

Les vérifications ordinaires ne doivent jamais recevoir de secrets de publication. Les tags stables identifient les commits protégés et examinés. Les échecs de dépendance, de licence et de sécurité bloquent la publication. Aucun ensemble de tests ne garantit l'immunité à toutes les entrées malformées ou aux attaques.
