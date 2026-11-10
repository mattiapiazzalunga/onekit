// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
// Offline Node 24+ authoring utility. The expanded VM state remains byte-identical.
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {gunzipSync,zstdCompressSync,zstdDecompressSync,constants} from 'node:zlib';
const [input,output,levelText='19']=process.argv.slice(2),level=Number(levelText);
if(!input||!output||!Number.isInteger(level)||level<1||level>22)throw Error('snapshot_arguments');
const limit=512*1024*1024;
const raw=gunzipSync(await readFile(input),{maxOutputLength:limit});
const compressed=zstdCompressSync(raw,{params:{
  [constants.ZSTD_c_compressionLevel]:level,
  [constants.ZSTD_c_windowLog]:27,
  [constants.ZSTD_c_enableLongDistanceMatching]:1,
}});
const digest=bytes=>createHash('sha256').update(bytes).digest('hex');
if(digest(zstdDecompressSync(compressed,{maxOutputLength:limit}))!==digest(raw))throw Error('snapshot_roundtrip');
await writeFile(output,compressed);
const metadata={compression:'zstd',compressionLevel:level,bytes:compressed.length,sha256:digest(compressed),
  expandedBytes:raw.length,expandedSha256:digest(raw)};
await writeFile(output+'.json',JSON.stringify(metadata,null,2)+'\n');
console.log(metadata);
