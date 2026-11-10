<a id="digital-signature-validation"></a>
# Validation des signatures numériques

La CLI et le navigateur exécutent le même moteur Python de validation. Aucun document n’est téléversé. Les signatures et échéances des listes de confiance UE sont vérifiées ; les services non pris en charge sont exclus.

L’intégrité cryptographique et la validation AdES sont des résultats distincts. La validation utilise des preuves locales et des listes de confiance UE authentifiées. Sans preuves, le résultat est indéterminé. L’équivalence avec DSS n’est pas certifiée.

Vérifie localement les signatures PDF et CMS avec validation AdES. Les signatures détachées nécessitent le fichier original. Une archive ZIP de preuves peut être ajoutée. Sans preuves de confiance ou de révocation, le résultat est indéterminé.

Actualisez les listes de confiance publiques avec cette commande. Elle n’envoie ni document ni donnée de signataire.

```sh
python -m pip install "onekit-tools[verification,trustlists]"
python -m onekit.signature_evidence eu-trust-lists.zip
onekit run signature-verify signed.pdf eu-trust-lists.zip -o report
```

Le manifeste du ZIP de preuves utilise la structure suivante. Les certificats supplémentaires ne deviennent jamais arbitrairement des ancres de confiance.

```json
{"schema":"onekit-signature-evidence-v1","lotl":"lotl.xml","trusted_lists":[{"url":"https://official.example/list.xml","path":"tl/list.xml"}],"certificates":[],"crls":[],"ocsps":[]}
```

Python natif Windows ARM64 peut nécessiter des outils de compilation pour cryptography. Utilisez Python x64 lorsqu’aucune wheel binaire n’est disponible.

L’instantané actuel contient 30 territoires. Les extensions TakenOverBy prises en charge préservent l’historique du service et ne transfèrent pas la confiance à un autre prestataire.

L’acceptation des algorithmes utilise les seuils de la version fixée de DSS 6.5.1 ; l’intégrité mathématique est indiquée séparément.

Sous Windows, l’extra trustlists active TLS avec vérification via le magasin de certificats du système d’exploitation.

L’instantané des listes de confiance a une couverture partielle. Sans preuves, le résultat reste indéterminé. Les tests sélectionnés avec DSS ne démontrent pas une équivalence exhaustive eIDAS ou PAdES.
