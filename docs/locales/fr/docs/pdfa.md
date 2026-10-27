<a id="pdfa-conversion-and-validation"></a>
# Conversion et validation PDF/A

Les CLI et Python API appellent `onekit.tools.pdfa`. Ce module n'invoque aucun exécutable et n'ouvre aucune connexion réseau. La conversion utilise pdftopdfa 0.9.24 pour les polices, les couleurs et la normalisation, suivie de pikepdf 10.17.0 PDF/A pour la préparation et la validation des octets finaux exacts. Il n'y a aucune dépendance Ghostscript.

La conversion prend en charge PDF/A-2b (par défaut) et 3b. La validation prend en charge 1b, 2b et 3b. La conformité A/U, PDF/A-4 et l’OCR ne sont pas pris en charge par cet adaptateur. Les constructions non prises en charge sont signalées par `not_checked` et ne sont pas considérées comme conformes. Un résultat `pass` fondé sur cette liste d’autorisation restrictive ne constitue pas une certification d’archivage ; une validation indépendante avec veraPDF reste recommandée pour les dépôts institutionnels.

```
onekit run pdf-to-pdfa input.pdf --options '{"profile":"2b"}' -o output
onekit run pdf-validate-pdfa output/input.pdf -o report
onekit doctor pdf-to-pdfa --json
```

Le CLI installe automatiquement un sous-ensemble **niveau-B non-OCR** des paquets en amont, épinglé et examiné. Il n’installe volontairement pas PaddleOCR, OCRmyPDF ni le backend de cryptographie pour le parseur PDF inutilisé de pdfminer : aucune option n’est transmise aux API OCR ou A/U en amont. Le `pdftopdfa` wheel en amont n’est pas modifié. Les métadonnées de son paquet incluent des exigences plus larges pour des API que OneKit n’invoque pas. L’extra optionnel `[pdfa]` installe les prérequis examinés. Pour une utilisation directe de Python API, installez cet extra puis `pip install --no-deps pdfminer.six==20260107 pdftopdfa==0.9.24`. N’installez pas les extras OCR de l’amont pour cet adaptateur. Les dépendances OCR obligatoires en amont imposent actuellement une ancienne version de PyYAML incompatible avec OneKit. La conversion nécessite Python 3.12+ ; la validation autonome fonctionne sur Python 3.11+. Lancez `python scripts/check_licenses.py --include-pdfa` pour vérifier le runtime sélectionné.

L'ancienne option `icc_profile` reste acceptée comme un fichier local ICC optionnel ; par défaut, elle conserve les profils RGB/CMYK inclus et licenciés du convertisseur. Les PDF chiffrés et les signatures numériques sont rejetés lors de la conversion. La conversion peut remplacer les polices et supprimer les actions ou métadonnées non archivables ; des avertissements accompagnent la sortie réussie. Les candidats échoués ou vérifiés de manière incomplète ne sont jamais renvoyés sous forme de fichiers PDF/A convertis. Les entrées ne sont pas écrasées. Le rapport de validation JSON conserve les champs `compliant` et `reports` et ajoute le profil vérifié, le verdict et le moteur.
