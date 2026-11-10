<a id="digital-signature-validation"></a>
# Validación de firmas digitales

La CLI y el navegador ejecutan el mismo motor Python de validación. No se sube ningún documento. Se comprueban firmas y caducidad de las listas de confianza de la UE; los servicios no compatibles se excluyen.

La integridad criptográfica y la validación AdES son resultados distintos. La validación usa evidencias locales y listas de confianza de la UE autenticadas. Si faltan evidencias, el resultado es indeterminado. La equivalencia con DSS no está certificada.

Comprueba localmente firmas PDF y CMS con validación AdES. Las firmas separadas requieren el archivo original. Puedes añadir un ZIP de evidencias de firma. Si faltan pruebas de confianza o revocación, el resultado es indeterminado.

Actualiza las listas de confianza públicas con este comando. No envía documentos ni datos de firmantes.

```sh
python -m pip install "onekit-tools[verification,trustlists]"
python -m onekit.signature_evidence eu-trust-lists.zip
onekit run signature-verify signed.pdf eu-trust-lists.zip -o report
```

El manifiesto del ZIP de evidencias usa la siguiente estructura. Los certificados adicionales nunca se convierten arbitrariamente en anclas de confianza.

```json
{"schema":"onekit-signature-evidence-v1","lotl":"lotl.xml","trusted_lists":[{"url":"https://official.example/list.xml","path":"tl/list.xml"}],"certificates":[],"crls":[],"ocsps":[]}
```

Python nativo de Windows ARM64 puede requerir herramientas de compilación para cryptography. Usa Python x64 si no hay una wheel binaria disponible.

La instantánea actual contiene 30 territorios. Las extensiones TakenOverBy admitidas conservan el historial del servicio y no transfieren la confianza a otro prestador.

La aceptación de algoritmos utiliza los umbrales de la versión fijada de DSS 6.5.1; la integridad matemática se informa por separado.

En Windows, el extra trustlists habilita TLS con verificación mediante el almacén de certificados del sistema operativo.

La instantánea de confianza tiene cobertura parcial. Sin evidencias, el resultado sigue siendo indeterminado. Las pruebas seleccionadas con DSS no demuestran una equivalencia completa eIDAS o PAdES.
