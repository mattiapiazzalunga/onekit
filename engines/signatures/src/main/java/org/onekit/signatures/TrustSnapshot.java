// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
package org.onekit.signatures;

import eu.europa.esig.dss.spi.tsl.TrustedListsCertificateSource;
import java.io.Serializable;
import java.time.Instant;
import java.util.List;
import java.util.Map;

/** Build-time output only. User evidence must never be deserialized as this type. */
public final class TrustSnapshot implements Serializable {
    private static final long serialVersionUID = 2L;
    public final String schema;
    public final String dssVersion;
    public final Instant validFrom;
    public final Instant expires;
    public final String signedArchiveSha256;
    public final List<String> territories;
    public final Map<String, String> sourceSha256;
    public final TrustedListsCertificateSource source;

    public TrustSnapshot(Instant validFrom,Instant expires,String signedArchiveSha256,
                         List<String> territories,Map<String,String> sourceSha256,TrustedListsCertificateSource source) {
        this.schema="onekit-dss-trust-v2";this.dssVersion="6.5.1";
        this.validFrom=validFrom;this.expires=expires;this.signedArchiveSha256=signedArchiveSha256;
        this.territories=List.copyOf(territories);this.sourceSha256=Map.copyOf(sourceSha256);this.source=source;
    }
}
