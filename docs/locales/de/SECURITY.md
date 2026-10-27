<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="security-policy"></a>
# Sicherheitsrichtlinie

Melden Sie Sicherheitslücken privat an `security@onekit.org` mit Version, Plattform, Tool, Abhängigkeitsversionen, Auswirkungen und synthetischer Nachstellung. Veröffentlichen Sie keine sensiblen Dateien, Zugangsdaten oder exploit-fertige private Berichte auf öffentlichen Trackern. Fixes zielen auf die neueste stabile Version; keine Reaktionszeitgarantie ist impliziert.

Der Kern begrenzt Pfade, Eingabegrößen, die Archivdekompression, Bildpixel, Vergleiche und Pipelines. Die Verschlüsselung verwendet authentifiziertes AES-256-GCM mit jeweils neuem Salt und Nonce sowie scrypt; verlorene Passwörter können nicht wiederhergestellt werden. Vorhandene Ausgabedateien bleiben standardmäßig erhalten. Die Python-Validierung analysiert den Quelltext, ohne ihn auszuführen.

Externe Konverter/Compiler sind separate native Programme, keine komplette Sandbox. Halten Sie sie aktuell und isoliere feindliche Dokumente mit OS-Kontrollen. Der CLI ist kein nicht authentifizierter Remote-Konvertierungsdienst. Das Bearbeiten eines signierten PDF kann Signaturen ungültig machen; PDF-Berechtigungen sind nicht gleichbedeutend mit der Integrität der Verschlüsselung.

Normale Prüfungen dürfen niemals Veröffentlichunggeheimnisse erhalten. Stabile Tags kennzeichnen geprüfte geschützte Haupt-Commits. Abhängigkeiten, Lizenz- und Sicherheitsfehler blockieren die Veröffentlichung. Kein Test-Suite garantiert Immunität gegen alle fehlerhaften Eingaben oder Angriffe.
