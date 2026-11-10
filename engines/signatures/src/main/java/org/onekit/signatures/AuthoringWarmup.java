// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
package org.onekit.signatures;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.SecureRandom;
import java.time.Instant;
import java.util.*;
import org.apache.pdfbox.Loader;
import org.apache.pdfbox.pdmodel.*;
import org.apache.pdfbox.pdmodel.font.PDType0Font;
import org.apache.pdfbox.pdmodel.interactive.digitalsignature.PDSignature;
import org.apache.pdfbox.rendering.PDFRenderer;
import org.bouncycastle.asn1.DERNull;
import org.bouncycastle.asn1.pkcs.PKCSObjectIdentifiers;
import org.bouncycastle.asn1.x509.AlgorithmIdentifier;
import org.bouncycastle.cert.X509CertificateHolder;
import org.bouncycastle.cms.*;
import org.bouncycastle.operator.ContentSigner;
import org.bouncycastle.operator.jcajce.JcaDigestCalculatorProviderBuilder;

/** Build-time initialization using public certificates and deliberately invalid
 * signatures. It never creates or installs a test root or a private signing key.
 */
public final class AuthoringWarmup {
    /** Build-only: discard reclaimable guest file pages before serializing RAM.
     * The public jars remain on the verified lazy filesystem, not in two caches.
     */
    public static void compactSnapshot() throws Exception {
        var sync = new ProcessBuilder("/bin/busybox", "sync").start();
        if (!sync.waitFor(30, java.util.concurrent.TimeUnit.SECONDS)) {
            sync.destroyForcibly();
            throw new IOException("snapshot_sync_timeout");
        }
        if (sync.exitValue() != 0) throw new IOException("snapshot_sync_failed");
        Files.writeString(Path.of("/proc/sys/vm/drop_caches"), "3\n", StandardCharsets.US_ASCII);
        System.out.println("ONEKIT_SNAPSHOT_COMPACTED=1");
    }

    private static byte[] invalidCMS(byte[] certificate, byte[] content, boolean attached) throws Exception {
        var signer = new ContentSigner() {
            private final ByteArrayOutputStream sink = new ByteArrayOutputStream();
            public AlgorithmIdentifier getAlgorithmIdentifier() {
                return new AlgorithmIdentifier(PKCSObjectIdentifiers.sha256WithRSAEncryption, DERNull.INSTANCE);
            }
            public OutputStream getOutputStream() { return sink; }
            public byte[] getSignature() { return new byte[512]; }
        };
        var generator = new CMSSignedDataGenerator();
        var holder = new X509CertificateHolder(certificate);
        generator.addCertificate(holder);
        generator.addSignerInfoGenerator(new SignerInfoGeneratorBuilder(
            new JcaDigestCalculatorProviderBuilder().build()).build(signer, holder));
        return generator.generate(new CMSProcessableByteArray(content), attached).getEncoded();
    }

    private static byte[] invalidPDF(byte[] certificate) throws Exception {
        var buffer = new ByteArrayOutputStream();
        try (var document = new PDDocument()) {
            var page = new PDPage();document.addPage(page);
            var font = PDType0Font.load(document, Path.of(System.getProperty("onekit.authoringFont",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")).toFile());
            try (var stream = new PDPageContentStream(document, page)) {
                stream.beginText();stream.setFont(font, 12);stream.newLineAtOffset(72, 720);
                stream.showText("OneKit");stream.endText();
            }
            new PDFRenderer(document).renderImage(0);
            document.save(buffer);
        }
        try (var document = Loader.loadPDF(buffer.toByteArray())) {
            var signature = new PDSignature();signature.setFilter(PDSignature.FILTER_ADOBE_PPKLITE);
            signature.setSubFilter(PDSignature.SUBFILTER_ETSI_CADES_DETACHED);
            signature.setSignDate(Calendar.getInstance(TimeZone.getTimeZone("UTC")));
            document.addSignature(signature, input -> {
                try { return invalidCMS(certificate, input.readAllBytes(), false); }
                catch (Exception error) { throw new IOException("warmup_cms", error); }
            });
            var signed = new ByteArrayOutputStream();document.saveIncremental(signed);
            return signed.toByteArray();
        }
    }

    public static void prepare(OfflineEngine engine, Path jobs, Path certificatePath) throws Exception {
        byte[] certificate = Files.readAllBytes(certificatePath);
        byte[][] documents = {invalidCMS(certificate, "OneKit".getBytes(StandardCharsets.US_ASCII), true),
                              invalidPDF(certificate)};
        for (int index = 0; index < documents.length; index++) {
            Path directory = Files.createTempDirectory(jobs, "build_warm_").toRealPath();
            if (!directory.startsWith(jobs.toRealPath()) || directory.equals(jobs.toRealPath()))
                throw new IOException("warmup_directory");
            try {
                String filename = index == 0 ? "public-invalid.p7m" : "public-invalid.pdf";
                Files.write(directory.resolve(filename), documents[index]);
                Instant moment = Instant.now();
                var clock = java.nio.ByteBuffer.allocate(16).order(java.nio.ByteOrder.LITTLE_ENDIAN)
                    .putLong(moment.getEpochSecond()).putLong(moment.getNano()).array();
                Files.write(directory.resolve("host-clock.bin"), clock);
                byte[] seed = new byte[32];new SecureRandom().nextBytes(seed);
                Files.write(directory.resolve("seed.bin"), seed);
                Files.writeString(directory.resolve("request.properties"), "document=" + filename
                    + "\nvalidationTime=" + moment + "\n", StandardCharsets.UTF_8);
                engine.validate(directory.getFileName().toString());
                String report = Files.readString(directory.resolve("simple.xml"));
                if (!report.contains("<Indication>TOTAL_FAILED</Indication>")
                        || report.contains("<Indication>TOTAL_PASSED</Indication>"))
                    throw new IOException("warmup_invalid_signature_was_not_rejected");
            } finally {
                try (var paths = Files.walk(directory)) {
                    for (Path path : paths.sorted(Comparator.reverseOrder()).toList()) Files.deleteIfExists(path);
                }
            }
        }
    }
}
