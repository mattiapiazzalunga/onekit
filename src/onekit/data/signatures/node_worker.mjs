// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import {readFile,writeFile} from 'node:fs/promises';
import {resolve,dirname,relative,isAbsolute} from 'node:path';
import {createHash} from 'node:crypto';
import {zstdDecompressSync} from 'node:zlib';
import {prepareDSS} from './host.mjs';
const [manifestPath,jobRoot]=process.argv.slice(2);
let engine,stage='bootstrap';
try{
  if(Number(process.versions.node.split('.')[0])<24)throw Error('node_version');
  const base=dirname(resolve(manifestPath)),jobs=resolve(jobRoot);
  const manifest=JSON.parse(await readFile(manifestPath,'utf8'));
  const asset=async name=>{
    if(!Object.hasOwn(manifest.files,name)||!/^[-a-zA-Z0-9_./]+$/.test(name)
        ||name.startsWith('/')||name.split('/').includes('..'))throw Error('asset_path');
    return new Uint8Array(await readFile(resolve(base,name)));
  };
  const moduleName=manifest.runtime||'libv86.mjs',moduleBytes=await asset(moduleName);
  if(createHash('sha256').update(moduleBytes).digest('hex')!==manifest.files[moduleName].sha256)throw Error('runtime_integrity');
  const {V86}=await import('data:text/javascript;base64,'+Buffer.from(moduleBytes).toString('base64'));
  globalThis.fetch=async()=>{throw Error('unexpected_network_request');};
  stage='prepare';engine=await prepareDSS({V86,manifest,loadAsset:asset,trustTimeoutMs:1800000,
    decodeZstd:(expected,bytes)=>zstdDecompressSync(bytes,{maxOutputLength:expected})});
  stage='input';
  let json='';for await(const chunk of process.stdin){json+=chunk;if(json.length>65536)throw Error('request_size');}
  const metadata=JSON.parse(json);
  const localFile=async path=>{
    const target=resolve(path),part=relative(jobs,target);
    if(isAbsolute(part)||part==='..'||part.startsWith('../')||part.startsWith('..\\'))throw Error('request_path');
    return new Uint8Array(await readFile(target));
  };
  const request={document:{name:metadata.document.name,data:await localFile(metadata.document.path)}};
  if(metadata.detached)request.detached={name:metadata.detached.name,data:await localFile(metadata.detached.path)};
  for(const key of ['certificates','crls','ocsps'])request[key]=await Promise.all((metadata[key]||[]).map(localFile));
  if(metadata.trustedLists)request.trustedLists={lotl:await localFile(metadata.trustedLists.lotl),
    lists:await Promise.all(metadata.trustedLists.lists.map(async item=>({url:item.url,data:await localFile(item.path)})))};
  stage='validation';const reports=await engine.validate(request);
  stage='output';
  for(const [name,bytes]of Object.entries(reports)){
    if(!['simple.xml','detailed.xml','diagnostic.xml','etsi.xml'].includes(name))throw Error('report_name');
    await writeFile(resolve(jobs,'output-'+name),bytes);
  }
  process.stdout.write(JSON.stringify({status:'done'})+'\n');
}catch(error){
  if(process.env.ONEKIT_DSS_DEBUG==='1')console.error(stage,error?.name,error?.message,
    String(error?.stack).split('\n').filter(line=>line.includes('/host.mjs')||line.includes('/node_worker.mjs')).slice(0,4).join('\n'),error?.diagnostic||'');
  const reason=['validation_failed','validation_timeout','engine_failed','node_version'].includes(error?.message)
    ?error.message:'engine_unavailable';
  process.exitCode=1;process.stdout.write(JSON.stringify({status:'failed',reason})+'\n');
}finally{if(engine)await engine.dispose();}
