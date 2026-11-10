// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
package org.onekit.signatures;

import eu.europa.esig.dss.model.InMemoryDocument;
import eu.europa.esig.dss.spi.DSSUtils;
import eu.europa.esig.dss.spi.validation.CommonCertificateVerifier;
import eu.europa.esig.dss.spi.x509.CommonCertificateSource;
import eu.europa.esig.dss.spi.x509.CommonTrustedCertificateSource;
import eu.europa.esig.dss.spi.tsl.TrustedListsCertificateSource;
import eu.europa.esig.dss.spi.x509.revocation.crl.ExternalResourcesCRLSource;
import eu.europa.esig.dss.spi.x509.revocation.ocsp.ExternalResourcesOCSPSource;
import eu.europa.esig.dss.validation.SignedDocumentValidator;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.time.Instant;
import java.util.*;
import java.util.zip.GZIPInputStream;

/** Fixed-file, offline DSS worker. The host pins the engine/trust asset manifest.
 * Evidence certificates are always adjuncts; requests cannot supply trust roots.
 */
public final class OfflineEngine {
    private static final long MAX_DOCUMENT = 64L * 1024 * 1024;
    private static final long MAX_EVIDENCE = 32L * 1024 * 1024;
    private static final int MAX_RESOURCES = 256;
    private final TrustSnapshot trust;
    private final Path jobs;
    private final Path trustedAsset;
    private final String pinnedSha256;
    private TrustedListsCertificateSource defaultSource;
    private Map<String,byte[]> baselineDocuments;
    private final String lotlUrl;
    private final Map<String,Instant> knownIssues=new HashMap<>();

    private static void commitReport(Path directory, String id, String name, String xml) throws Exception {
        byte[] bytes = xml.getBytes(StandardCharsets.UTF_8);
        // Closing a guest file is not a cross-filesystem commit barrier. Force
        // dirty 9p pages before announcing completion to the Node/browser host.
        try (var channel = java.nio.channels.FileChannel.open(directory.resolve(name),
                StandardOpenOption.CREATE_NEW, StandardOpenOption.WRITE)) {
            var buffer = java.nio.ByteBuffer.wrap(bytes);
            while (buffer.hasRemaining()) channel.write(buffer);
            channel.force(true);
        }
        String digest = HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));
        System.out.println("ONEKIT_DSS_REPORT=" + id + "|" + name + "|" + bytes.length + "|" + digest);
    }

    public OfflineEngine(Path trustedAsset, String pinnedSha256, Path jobs) throws Exception {
        this.trustedAsset=trustedAsset;this.pinnedSha256=pinnedSha256;
        TrustSnapshot loaded=readSnapshot(trustedAsset,pinnedSha256);
        this.trust=new TrustSnapshot(loaded.validFrom,loaded.expires,loaded.signedArchiveSha256,
            loaded.territories,loaded.sourceSha256,null);
        this.defaultSource=loaded.source;
        this.baselineDocuments=sourceDocuments(defaultSource);
        this.lotlUrl=defaultSource.getSummary().getLOTLInfos().get(0).getUrl();
        for(var parent:defaultSource.getSummary().getLOTLInfos()){
            knownIssues.put(parent.getUrl(),parent.getParsingCacheInfo().getIssueDate().toInstant());
            for(var national:parent.getTLInfos())if(national.getParsingCacheInfo()!=null
                &&national.getParsingCacheInfo().getIssueDate()!=null)
                knownIssues.put(national.getUrl(),national.getParsingCacheInfo().getIssueDate().toInstant());
        }
        Files.createDirectories(jobs);
        this.jobs=jobs.toRealPath();
    }

    private static TrustSnapshot readSnapshot(Path trustedAsset,String pinnedSha256) throws Exception {
        if (!pinnedSha256.matches("[a-f0-9]{64}")) throw new IOException("trust_asset_digest");
        if (Files.size(trustedAsset) > MAX_EVIDENCE) throw new IOException("trust_asset_size");
        byte[] asset = Files.readAllBytes(trustedAsset);
        String actual = HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(asset));
        if (!MessageDigest.isEqual(actual.getBytes(StandardCharsets.US_ASCII),
                pinnedSha256.getBytes(StandardCharsets.US_ASCII))) throw new IOException("trust_asset_digest");
        // Only a digest-pinned build artifact reaches Java deserialization. Never user evidence.
        TrustSnapshot trust;
        try (var input = new ObjectInputStream(new GZIPInputStream(new ByteArrayInputStream(asset)))) {
            input.setObjectInputFilter(ObjectInputFilter.Config.createFilter(
                "maxdepth=128;maxrefs=3000000;maxbytes=268435456;maxarray=33554432"));
            trust = (TrustSnapshot) input.readObject();
        }
        if (!"onekit-dss-trust-v2".equals(trust.schema) || !"6.5.1".equals(trust.dssVersion)
                || trust.source == null || trust.source.getCertificates().isEmpty()
                || trust.sourceSha256 == null || trust.sourceSha256.size() != trust.territories.size() + 1
                || trust.validFrom == null || trust.expires == null
                || !trust.validFrom.isBefore(trust.expires)) throw new IOException("trust_asset_schema");
        return trust;
    }

    private static Map<String,byte[]> sourceDocuments(TrustedListsCertificateSource source) throws IOException {
        var result=new HashMap<String,byte[]>();
        for(var parent:source.getSummary().getLOTLInfos()){
            var infos=new ArrayList<eu.europa.esig.dss.model.tsl.TLInfo>();
            infos.add(parent);infos.addAll(parent.getTLInfos());
            for(var info:infos){
                var record=info.getDownloadCacheInfo();
                if(record==null||record.getDocument()==null)continue;
                var document=record.getDocument();
                if(document instanceof InMemoryDocument memory)result.put(info.getUrl(),memory.getBytes());
                else try(var stream=document.openStream()){result.put(info.getUrl(),stream.readAllBytes());}
            }
        }
        return result;
    }

    private TrustedListsCertificateSource defaultSource() throws Exception {
        if(defaultSource==null){
            System.gc();defaultSource=readSnapshot(trustedAsset,pinnedSha256).source;
            baselineDocuments=sourceDocuments(defaultSource);
        }
        return defaultSource;
    }

    private TrustedListsCertificateSource validationSource(Path base,Properties request,Instant moment,long[] remaining) throws Exception {
        boolean fresh=!moment.isBefore(trust.validFrom)&&moment.isBefore(trust.expires);
        if(!request.containsKey("lotl")){
            if(!fresh)throw new IOException("trust_snapshot_expired_or_not_yet_valid");
            return defaultSource();
        }
        var documents=new HashMap<>(baselineDocuments);
        var required=new HashSet<String>();
        byte[] lotl=document(base,request.getProperty("lotl"),remaining[0]).getBytes();
        remaining[0]-=lotl.length;remaining[1]--;
        documents.put(lotlUrl,lotl);
        int count=Integer.parseInt(request.getProperty("tl.count","0"));
        if(count<0||count>100||count>remaining[1])throw new IOException("evidence_count");
        remaining[1]-=count;
        for(int index=0;index<count;index++){
            String url=request.getProperty("tl."+index+".url");
            if(url==null||url.equals(lotlUrl)||!required.add(url))throw new IOException("trust_list_url");
            byte[] bytes=document(base,request.getProperty("tl."+index+".path"),remaining[0]).getBytes();
            remaining[0]-=bytes.length;documents.put(url,bytes);
        }
        boolean changed=!fresh;
        for(var entry:documents.entrySet()){
            String hash=HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(entry.getValue()));
            if(!hash.equals(trust.sourceSha256.get(entry.getKey())))changed=true;
        }
        if(!changed)return defaultSource();
        var pins=new CommonTrustedCertificateSource();
        Path pinDirectory=Path.of(System.getProperty("onekit.lotlPinsDir","/engine/lotl-pins"));
        if(Files.isDirectory(pinDirectory)){
            try(var paths=Files.list(pinDirectory)){
                for(var path:paths.filter(path->path.getFileName().toString().endsWith(".der")).toList()){
                    if(Files.size(path)>131072||pins.getCertificates().size()>=16)throw new IOException("lotl_pins");
                    pins.addCertificate(DSSUtils.loadCertificate(Files.readAllBytes(path)));
                }
            }
        }else pins.addCertificate(defaultSource().getSummary().getLOTLInfos().get(0).getValidationCacheInfo().getSigningCertificate());
        // User-supplied lists get a separate authenticated source. Never union
        // new/withdrawn services with old grants, or retain this source for later jobs.
        defaultSource=null;System.gc();
        return TrustCompiler.compile(documents,pins,lotlUrl,required,moment,knownIssues);
    }

    private static Path resource(Path base, String name) throws IOException {
        if (name == null || name.isBlank()) throw new IOException("resource_missing");
        Path path = base.resolve(name).normalize().toRealPath();
        if (!path.startsWith(base) || !Files.isRegularFile(path)) throw new IOException("resource_path");
        return path;
    }

    private static InMemoryDocument document(Path base, String name, long limit) throws IOException {
        Path path = resource(base, name);
        if (Files.size(path) > limit) throw new IOException("resource_size");
        byte[] bytes = Files.readAllBytes(path);
        if (bytes.length > limit) throw new IOException("resource_size");
        return new InMemoryDocument(bytes, path.getFileName().toString());
    }

    private static List<InMemoryDocument> evidence(Path base, Properties request, String key,
            long[] remaining) throws IOException {
        int count = Integer.parseInt(request.getProperty(key + ".count", "0"));
        if (count < 0 || count > MAX_RESOURCES || count > remaining[1]) throw new IOException("evidence_count");
        remaining[1] -= count;
        var result = new ArrayList<InMemoryDocument>();
        for (int index = 0; index < count; index++) {
            var item = document(base, request.getProperty(key + "." + index), remaining[0]);
            remaining[0] -= item.getBytes().length;
            result.add(item);
        }
        return result;
    }

    public void validate(String id) throws Exception {
        if (!id.matches("[a-zA-Z0-9_-]{1,64}")) throw new IOException("job_id");
        Path base = resource(jobs, id + "/request.properties").getParent();
        if (Boolean.getBoolean("onekit.vmRefresh")) {
            var refresh = new ProcessBuilder("/refresh-state", base.toString()).redirectOutput(ProcessBuilder.Redirect.DISCARD)
                .redirectError(ProcessBuilder.Redirect.DISCARD).start();
            if (!refresh.waitFor(5, java.util.concurrent.TimeUnit.SECONDS)) {
                refresh.destroyForcibly();
                throw new IOException("host_state_refresh_timeout");
            }
            if (refresh.exitValue() != 0) throw new IOException("host_state_refresh_failed");
        }
        for (String report : List.of("simple.xml", "detailed.xml", "diagnostic.xml", "etsi.xml"))
            Files.deleteIfExists(base.resolve(report));
        var request = new Properties();
        var descriptor = document(base, "request.properties", 16384);
        try (var reader = new StringReader(new String(descriptor.getBytes(), StandardCharsets.UTF_8))) {
            request.load(reader);
        }
        Instant moment = Instant.parse(request.getProperty("validationTime"));
        // Restored VM wall clocks are not authoritative: every request supplies the current host time.
        var verifier = new CommonCertificateVerifier();
        verifier.setAIASource(null);
        verifier.setCrlSource(null);
        verifier.setOcspSource(null);
        long[] remaining = {MAX_EVIDENCE, MAX_RESOURCES};
        verifier.setTrustedCertSources(validationSource(base,request,moment,remaining));
        var adjuncts = new CommonCertificateSource();
        for (var certificate : evidence(base, request, "certificate", remaining))
            adjuncts.addCertificate(DSSUtils.loadCertificate(certificate.getBytes()));
        verifier.setAdjunctCertSources(adjuncts);
        var crls = evidence(base, request, "crl", remaining);
        if (!crls.isEmpty()) verifier.setCrlSource(new ExternalResourcesCRLSource(
            crls.toArray(InMemoryDocument[]::new)));
        var ocsps = evidence(base, request, "ocsp", remaining);
        if (!ocsps.isEmpty()) verifier.setOcspSource(new ExternalResourcesOCSPSource(
            ocsps.toArray(InMemoryDocument[]::new)));
        var signed=document(base,request.getProperty("document"),MAX_DOCUMENT);
        signed.setName(request.getProperty("document.name",signed.getName()));
        var validator = SignedDocumentValidator.fromDocument(signed);
        validator.setCertificateVerifier(verifier);
        validator.setValidationTime(Date.from(moment));
        if (request.containsKey("detached")) {
            var detached=document(base,request.getProperty("detached"),MAX_DOCUMENT);
            detached.setName(request.getProperty("detached.name",detached.getName()));
            validator.setDetachedContents(List.of(detached));
        }
        var reports = validator.validateDocument();
        commitReport(base, id, "simple.xml", reports.getXmlSimpleReport());
        commitReport(base, id, "detailed.xml", reports.getXmlDetailedReport());
        commitReport(base, id, "diagnostic.xml", reports.getXmlDiagnosticData());
        commitReport(base, id, "etsi.xml", reports.getXmlValidationReport());
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 3) throw new IllegalArgumentException("engine_arguments");
        System.setProperty("org.slf4j.simpleLogger.defaultLogLevel", "off");
        var engine = new OfflineEngine(Path.of(args[0]), args[1], Path.of(args[2]));
        if (Boolean.getBoolean("onekit.authoringWarmup")) {
            AuthoringWarmup.prepare(engine, Path.of(args[2]), Path.of(System.getProperty("onekit.authoringCertificate")));
            System.clearProperty("onekit.authoringWarmup");
            System.gc();System.gc();
            if (Boolean.getBoolean("onekit.authoringCompactSnapshot")) AuthoringWarmup.compactSnapshot();
            System.out.println("ONEKIT_SNAPSHOT_READY=1");
        }
        System.out.println("ONEKIT_DSS_READY=1");
        try (var input = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.US_ASCII))) {
            String line;
            while ((line = input.readLine()) != null) {
                if (!line.matches("RUN [a-zA-Z0-9_-]{1,64}")) {
                    System.out.println("ONEKIT_DSS_PROTOCOL_ERROR=1");
                    continue;
                }
                String id = line.substring(4);
                try {
                    engine.validate(id);
                    System.out.println("ONEKIT_DSS_DONE=" + id);
                } catch (Exception error) {
                    // No document paths, XML, certificate identifiers or user bytes in the protocol/log.
                    System.out.println("ONEKIT_DSS_ERROR=" + id + "|" + error.getClass().getSimpleName());
                }
            }
        }
    }
}
