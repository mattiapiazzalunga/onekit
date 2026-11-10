// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
package org.onekit.signatures;

import eu.europa.esig.dss.model.DSSException;
import eu.europa.esig.dss.model.InMemoryDocument;
import eu.europa.esig.dss.model.tsl.TLInfo;
import eu.europa.esig.dss.spi.tsl.TrustedListsCertificateSource;
import eu.europa.esig.dss.spi.x509.CommonTrustedCertificateSource;
import eu.europa.esig.dss.tsl.job.TLValidationJob;
import eu.europa.esig.dss.tsl.source.LOTLSource;
import java.io.IOException;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.*;

/** Authenticate complete local trust inputs with DSS itself. Nothing is fetched. */
public final class TrustCompiler {
    private static void check(TLInfo info, Instant moment, boolean historicalUK) throws IOException {
        if (info.getValidationCacheInfo() == null || !info.getValidationCacheInfo().isValid()
                || info.getParsingCacheInfo() == null || !info.getParsingCacheInfo().isResultExist())
            throw new IOException("trust_list_authentication");
        var parsed = info.getParsingCacheInfo();
        if (parsed.getIssueDate() == null || parsed.getIssueDate().toInstant().isAfter(moment))
            throw new IOException("trust_list_future_or_missing_issue_date");
        if (parsed.getNextUpdateDate() == null) {
            if (!historicalUK) throw new IOException("trust_list_expiry_missing");
        } else if (!moment.isBefore(parsed.getNextUpdateDate().toInstant()))
            throw new IOException("trust_list_expired");
    }

    public static TrustedListsCertificateSource compile(Map<String,byte[]> documents,
            CommonTrustedCertificateSource pins, String lotlUrl, Set<String> required, Instant moment,
            Map<String,Instant> knownIssues) throws Exception {
        var source = new TrustedListsCertificateSource();
        var lotl = new LOTLSource();lotl.setUrl(lotlUrl);lotl.setCertificateSource(pins);lotl.setPivotSupport(false);
        var executor = Executors.newFixedThreadPool(2);
        try {
            var job = new TLValidationJob();job.setExecutorService(executor);
            job.setOfflineDataLoader(url -> {
                byte[] data = documents.get(url);
                if (data == null) throw new DSSException("offline_resource_unavailable");
                return new InMemoryDocument(data);
            });
            job.setListOfTrustedListSources(lotl);job.setTrustedListCertificateSource(source);job.offlineRefresh();
            var summary = source.getSummary();
            if (summary == null || summary.getLOTLInfos().size() != 1) throw new IOException("lotl_summary");
            var parent = summary.getLOTLInfos().get(0);check(parent, moment, false);
            if(knownIssues.containsKey(parent.getUrl())&&parent.getParsingCacheInfo().getIssueDate().toInstant()
                .isBefore(knownIssues.get(parent.getUrl())))throw new IOException("trust_list_rollback");
            var accepted = new HashSet<String>();
            for (TLInfo national : parent.getTLInfos()) {
                boolean historical = national.getUrl().equals("https://ec.europa.eu/tools/lotl/Final_EU_TSL-UKsigned.xml")
                    && national.getParsingCacheInfo() != null && "UK".equals(national.getParsingCacheInfo().getTerritory());
                check(national, moment, historical);accepted.add(national.getUrl());
                if(knownIssues.containsKey(national.getUrl())&&national.getParsingCacheInfo().getIssueDate().toInstant()
                    .isBefore(knownIssues.get(national.getUrl())))throw new IOException("trust_list_rollback");
            }
            if (!accepted.containsAll(required) || source.getCertificates().isEmpty()) throw new IOException("trust_coverage");
            return source;
        } finally { executor.shutdownNow(); }
    }
}
