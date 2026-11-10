// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import eu.europa.esig.dss.model.InMemoryDocument;
import eu.europa.esig.dss.spi.validation.CommonCertificateVerifier;
import eu.europa.esig.dss.validation.SignedDocumentValidator;
import eu.europa.esig.dss.spi.DSSUtils;
import eu.europa.esig.dss.spi.x509.CommonTrustedCertificateSource;
import eu.europa.esig.dss.spi.x509.revocation.crl.ExternalResourcesCRLSource;
import eu.europa.esig.dss.spi.x509.revocation.ocsp.ExternalResourcesOCSPSource;
import java.io.File;
import java.util.List;

/** Test oracle only. No document or certificate network fetching. */
public class Reference {
    private static InMemoryDocument document(String path) {
        try (var input = new java.io.FileInputStream(path)) {
            return new InMemoryDocument(input.readAllBytes(), new File(path).getName());
        } catch (java.io.IOException exception) {
            throw new java.io.UncheckedIOException(exception);
        }
    }

    public static void main(String[] args) {
        var validator = SignedDocumentValidator.fromDocument(document(args[0]));
        var verifier = new CommonCertificateVerifier();
        verifier.setCrlSource(null);
        verifier.setOcspSource(null);
        verifier.setAIASource(null);
        if (args.length > 2 && !args[2].equals("-")) {
            var trust = new CommonTrustedCertificateSource();
            trust.addCertificate(DSSUtils.loadCertificate(document(args[2]).getBytes()));
            verifier.setTrustedCertSources(trust);
        }
        if (args.length > 3 && !args[3].equals("-")) {
            verifier.setCrlSource(new ExternalResourcesCRLSource(document(args[3])));
        }
        if (args.length > 4 && !args[4].equals("-")) {
            verifier.setOcspSource(new ExternalResourcesOCSPSource(document(args[4])));
        }
        validator.setCertificateVerifier(verifier);
        if (args.length > 5 && !args[5].equals("-")) {
            validator.setValidationTime(java.util.Date.from(java.time.Instant.parse(args[5])));
        }
        if (args.length > 1 && !args[1].equals("-")) {
            validator.setDetachedContents(List.of(document(args[1])));
        }
        var report = validator.validateDocument().getSimpleReport();
        for (var id : report.getSignatureIdList()) {
            System.out.println("ONEKIT_DSS_RESULT=" + report.getIndication(id) + "|" + report.getSubIndication(id));
            System.out.println("ONEKIT_DSS_DETAILS=" + report.getSignatureFormat(id) + "|"
                + report.getSignatureQualification(id) + "|"
                + (report.getBestSignatureTime(id) == null ? "-" : report.getBestSignatureTime(id).toInstant()));
        }
    }
}
