<a id="digital-signature-validation"></a>
# Validierung digitaler Signaturen

CLI und Browser führen dieselbe Python-Validierungsengine aus. Es werden keine Dokumente hochgeladen. Signaturen und Ablaufdaten der EU-Vertrauenslisten werden geprüft; nicht unterstützte Dienste werden ausgeschlossen.

Kryptografische Integrität und AdES-Validierung sind getrennte Ergebnisse. Die Validierung nutzt lokale Nachweise und authentifizierte EU-Vertrauenslisten. Bei fehlenden Nachweisen ist das Ergebnis unbestimmt. Die Gleichwertigkeit mit DSS ist nicht zertifiziert.

Prüft PDF- und CMS-Signaturen lokal mit AdES-Validierung. Abgetrennte Signaturen benötigen die Originaldatei. Optional kann ein ZIP mit Signaturprüfdaten hinzugefügt werden. Fehlen Vertrauens- oder Sperrnachweise, ist das Ergebnis unbestimmt.

Aktualisieren Sie öffentliche Vertrauenslisten mit diesem Befehl. Dabei werden keine Dokumente oder Unterzeichnerdaten gesendet.

```sh
python -m pip install "onekit-tools[verification,trustlists]"
python -m onekit.signature_evidence eu-trust-lists.zip
onekit run signature-verify signed.pdf eu-trust-lists.zip -o report
```

Das Manifest des Prüfdaten-ZIP verwendet die folgende Struktur. Zusätzliche Zertifikate werden niemals willkürlich zu Vertrauensankern.

```json
{"schema":"onekit-signature-evidence-v1","lotl":"lotl.xml","trusted_lists":[{"url":"https://official.example/list.xml","path":"tl/list.xml"}],"certificates":[],"crls":[],"ocsps":[]}
```

Natives Windows-ARM64-Python benötigt für cryptography möglicherweise Build-Werkzeuge. Verwenden Sie x64-Python, wenn kein binäres Wheel verfügbar ist.

Der aktuelle Snapshot enthält 30 Gebiete. Unterstützte TakenOverBy-Erweiterungen bewahren den Dienstverlauf und übertragen das Vertrauen nicht auf einen anderen Anbieter.

Die Zulässigkeit der Algorithmen richtet sich nach den Schwellenwerten der festgelegten DSS-Version 6.5.1; die mathematische Integrität wird gesondert ausgewiesen.

Unter Windows aktiviert das Extra trustlists TLS mit Prüfung über den Zertifikatsspeicher des Betriebssystems.

Der Vertrauensdatenstand deckt nur einen Teil ab. Bei fehlenden Nachweisen bleibt das Ergebnis unbestimmt. Ausgewählte DSS-Referenztests belegen keine vollständige Gleichwertigkeit mit eIDAS oder PAdES.
