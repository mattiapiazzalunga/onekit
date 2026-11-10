// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
package org.onekit.signatures;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.zip.GZIPInputStream;
import org.jose4j.json.JsonUtil;

/** Authoring only: describe an authenticated, publisher-digest-pinned build asset.
 * This utility is never called on documents or uploaded evidence.
 */
public final class DescribeSnapshot {
    public static void main(String[] args) throws Exception {
        byte[] bytes = Files.readAllBytes(Path.of(args[0]));
        String digest = HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));
        if (!args[1].matches("[a-f0-9]{64}") || !digest.equals(args[1])) throw new IOException("trust_asset_digest");
        TrustSnapshot source;
        try (var input = new ObjectInputStream(new GZIPInputStream(new ByteArrayInputStream(bytes)))) {
            input.setObjectInputFilter(ObjectInputFilter.Config.createFilter(
                "maxdepth=128;maxrefs=3000000;maxbytes=268435456;maxarray=33554432"));
            source = (TrustSnapshot) input.readObject();
        }
        var result = new LinkedHashMap<String,Object>();
        result.put("schema", source.schema);result.put("dssVersion", source.dssVersion);
        result.put("validFrom", source.validFrom.toString());result.put("expires", source.expires.toString());
        result.put("territories", source.territories);result.put("sourceSha256", source.sourceSha256);
        result.put("lotlUrl", source.source.getSummary().getLOTLInfos().get(0).getUrl());
        result.put("certificates", source.source.getCertificates().size());
        result.put("assetSha256", digest);result.put("assetBytes", bytes.length);
        result.put("archiveSha256", source.signedArchiveSha256);
        Files.writeString(Path.of(args[2]), JsonUtil.toJson(result) + "\n", StandardCharsets.UTF_8);
    }
}
