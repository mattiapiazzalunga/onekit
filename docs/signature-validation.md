# Digital signature validation

The CLI and browser execute the same Python validation engine. No document is uploaded. EU trust-list signatures and expiry are checked; unsupported services are excluded.

Cryptographic integrity and AdES validation are separate results. Validation uses local evidence and authenticated EU trust lists. Missing evidence is indeterminate. Equivalence with DSS is not certified.

Checks PDF and CMS signatures locally with AdES validation. Detached signatures require the original file. Optionally add one signature evidence ZIP. Missing trust or revocation evidence gives an indeterminate result.

Refresh public trust lists with this command. It sends no document or signer data.

```sh
python -m pip install "onekit-tools[verification,trustlists]"
python -m onekit.signature_evidence eu-trust-lists.zip
onekit run signature-verify signed.pdf eu-trust-lists.zip -o report
```

The evidence ZIP manifest uses the following structure. Supplementary certificates never become arbitrary trust anchors.

```json
{"schema":"onekit-signature-evidence-v1","lotl":"lotl.xml","trusted_lists":[{"url":"https://official.example/list.xml","path":"tl/list.xml"}],"certificates":[],"crls":[],"ocsps":[]}
```

Native Windows ARM64 Python may require build tools for cryptography. Use x64 Python when a binary wheel is unavailable.

The current snapshot contains 30 territories. Supported TakenOverBy extensions preserve service history and do not transfer trust to another provider.

Algorithm acceptance uses the pinned DSS 6.5.1 thresholds; mathematical integrity is reported separately.

On Windows, the trustlists extra enables verified TLS through the operating system certificate store.

The trust snapshot has partial coverage. Missing evidence remains indeterminate. Selected DSS reference tests do not establish exhaustive eIDAS or PAdES equivalence.
