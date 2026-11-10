// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
package org.onekit.signatures;

import eu.europa.esig.dss.model.InMemoryDocument;
import eu.europa.esig.dss.model.DSSException;
import eu.europa.esig.dss.model.tsl.TLInfo;
import eu.europa.esig.dss.spi.DSSUtils;
import eu.europa.esig.dss.spi.client.http.DSSFileLoader;
import eu.europa.esig.dss.spi.tsl.TrustedListsCertificateSource;
import eu.europa.esig.dss.spi.x509.CommonTrustedCertificateSource;
import eu.europa.esig.dss.tsl.job.TLValidationJob;
import eu.europa.esig.dss.tsl.source.LOTLSource;
import java.io.*;
import java.nio.file.*;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.*;
import java.util.zip.GZIPOutputStream;

/** Offline authoring utility. Pins are LOTL signers, never document trust roots. */
public final class TrustSnapshotBuilder {
    public static void main(String[] args) throws Exception {
        Path base=Path.of(args[0]).toAbsolutePath().normalize();
        var properties=new Properties();
        try(var reader=Files.newBufferedReader(base.resolve("source.properties"))){properties.load(reader);}
        var documents=new HashMap<String,byte[]>();
        var expected=new HashMap<String,String>();
        int count=Integer.parseInt(properties.getProperty("count"));
        for(int index=0;index<count;index++){
            String url=properties.getProperty("url."+index);
            Path path=base.resolve(properties.getProperty("path."+index)).normalize();
            if(!path.startsWith(base))throw new IllegalArgumentException("source_path");
            documents.put(url,Files.readAllBytes(path));
            String territory=properties.getProperty("territory."+index);
            if(territory!=null)expected.put(url,territory);
        }
        DSSFileLoader loader=url->{
            byte[] bytes=documents.get(url);
            if(bytes==null)throw new DSSException("offline_resource_unavailable");
            return new InMemoryDocument(bytes);
        };
        var pins=new CommonTrustedCertificateSource();
        for(int index=0;index<Integer.parseInt(properties.getProperty("pins"));index++){
            pins.addCertificate(DSSUtils.loadCertificate(Files.readAllBytes(base.resolve("pin-"+index+".der"))));
        }
        var lotl=new LOTLSource();lotl.setUrl(properties.getProperty("lotl"));
        lotl.setCertificateSource(pins);lotl.setPivotSupport(false);
        var source=new TrustedListsCertificateSource();
        var executor=new ThreadPoolExecutor(4,4,0,TimeUnit.MILLISECONDS,new LinkedBlockingQueue<>()){
            @Override protected void afterExecute(Runnable task,Throwable failure){
                super.afterExecute(task,failure);
                if(task instanceof Future<?> future){
                    try{future.get();}catch(InterruptedException error){Thread.currentThread().interrupt();}
                    catch(ExecutionException error){error.getCause().printStackTrace();}
                }
            }
        };
        try {
            var job=new TLValidationJob();job.setExecutorService(executor);
            job.setOfflineDataLoader(loader);job.setListOfTrustedListSources(lotl);
            job.setTrustedListCertificateSource(source);job.offlineRefresh();
            var summary=source.getSummary();
            if(summary==null||summary.getLOTLInfos().size()!=1)throw new IllegalStateException("lotl_summary");
            var info=summary.getLOTLInfos().get(0);
            if(info.getValidationCacheInfo()==null||!info.getValidationCacheInfo().isValid()){
                System.out.println("ONEKIT_LOTL_DOWNLOAD="+info.getDownloadCacheInfo().getStatusName()+"|"+info.getDownloadCacheInfo().getExceptionMessage());
                System.out.println("ONEKIT_LOTL_PARSE="+(info.getParsingCacheInfo()==null?"-":info.getParsingCacheInfo().getStatusName()+"|"+info.getParsingCacheInfo().getExceptionMessage()));
                System.out.println("ONEKIT_LOTL_VALIDATION="+(info.getValidationCacheInfo()==null?"-":info.getValidationCacheInfo().getIndication()+"|"+info.getValidationCacheInfo().getSubIndication()+"|"+info.getValidationCacheInfo().getExceptionMessage()));
                throw new IllegalStateException("lotl_authentication");
            }
            var accepted=new TreeSet<String>();
            for(TLInfo national:info.getTLInfos()){
                if(!expected.containsKey(national.getUrl()))continue;
                boolean valid=national.getValidationCacheInfo()!=null&&national.getValidationCacheInfo().isValid()
                    &&national.getParsingCacheInfo()!=null&&national.getParsingCacheInfo().isResultExist();
                System.out.println("ONEKIT_TL="+expected.get(national.getUrl())+"|"+valid+"|"
                    +(national.getValidationCacheInfo()==null?"-":national.getValidationCacheInfo().getIndication()));
                if(!valid)throw new IllegalStateException("national_authentication");
                accepted.add(expected.get(national.getUrl()));
            }
            if(accepted.size()!=expected.size()||source.getCertificates().isEmpty())throw new IllegalStateException("trust_coverage");
            var sourceDigests=new TreeMap<String,String>();
            for(var entry:documents.entrySet())sourceDigests.put(entry.getKey(),HexFormat.of().formatHex(
                java.security.MessageDigest.getInstance("SHA-256").digest(entry.getValue())));
            var snapshot=new TrustSnapshot(Instant.parse(properties.getProperty("validFrom")),
                Instant.parse(properties.getProperty("expires")),properties.getProperty("archiveSha256"),
                new ArrayList<>(accepted),sourceDigests,source);
            try(var output=new ObjectOutputStream(new GZIPOutputStream(Files.newOutputStream(Path.of(args[1]))))){
                output.writeObject(snapshot);
            }
            System.out.println("ONEKIT_TRUST="+accepted.size()+"|"+source.getCertificates().size());
        }finally{executor.shutdownNow();}
    }
}
