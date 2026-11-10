// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
// Build-only capture. No user-document validation runs in this process.
import {readFile,writeFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {gzipSync} from 'node:zlib';
import {prepareDSS} from './host.mjs';
const [manifestPath,modulePath,output]=process.argv.slice(2);
if(!manifestPath||!modulePath||!output)throw Error('capture_arguments');
const base=dirname(resolve(manifestPath)),manifest=JSON.parse(await readFile(manifestPath,'utf8'));
const {V86}=await import(pathToFileURL(resolve(modulePath)));
const start=performance.now();
const progress=setInterval(()=>console.log('AUTHORING_MS',Math.round(performance.now()-start)),30000);
let engine;
try{
  engine=await prepareDSS({V86,manifest,coldStart:true,authoring:true,timeoutMs:1800000,
    loadAsset:async name=>new Uint8Array(await readFile(resolve(base,name)))});
  const state=new Uint8Array(await engine.captureForAuthoring());
  await writeFile(output,gzipSync(state));
  console.log({expandedBytes:state.length,expandedSha256:createHash('sha256').update(state).digest('hex'),
    authoringMs:performance.now()-start});
}finally{clearInterval(progress);if(engine)await engine.dispose();}
