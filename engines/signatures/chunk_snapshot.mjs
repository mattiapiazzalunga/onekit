// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
// Offline authoring: keep every served model asset below common static-host limits.
import {readFile,writeFile,mkdir,rename} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {createHash} from 'node:crypto';
const [input]=process.argv.slice(2);
if(!input)throw Error('manifest_argument');
const path=resolve(input),base=dirname(path),manifest=JSON.parse(await readFile(path,'utf8'));
if(manifest.schema!=='onekit-dss-vm-v1'||!/^[-a-zA-Z0-9_./]+$/.test(manifest.state)
    ||manifest.state.startsWith('/')||manifest.state.split('/').includes('..'))throw Error('engine_manifest');
const descriptor=manifest.files[manifest.state],bytes=await readFile(resolve(base,manifest.state));
const digest=data=>createHash('sha256').update(data).digest('hex');
if(bytes.length!==descriptor.bytes||digest(bytes)!==descriptor.sha256)throw Error('state_integrity');
const chunkSize=4*1024*1024,chunks=[];
await mkdir(resolve(base,'chunks'),{recursive:true});
for(let offset=0;offset<bytes.length;offset+=chunkSize){
  const part=bytes.subarray(offset,offset+chunkSize),sha256=digest(part),name=`chunks/${sha256}.bin`;
  await writeFile(resolve(base,name),part);
  manifest.files[name]={bytes:part.length,sha256};chunks.push(name);
}
Object.assign(descriptor,{chunkSize,chunks});
await writeFile(path+'.tmp',JSON.stringify(manifest)+'\n');await rename(path+'.tmp',path);
console.log({parts:chunks.length,maxPartBytes:chunkSize,totalBytes:bytes.length});
