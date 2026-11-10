// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {pathToFileURL} from 'node:url';
import {prepareDSS} from '../host.mjs';

const configured=['ONEKIT_DSS_VM_MANIFEST','ONEKIT_DSS_VM_FS_ROOT',
  'ONEKIT_V86_MODULE','ONEKIT_DSS_VM_FIXTURES'].every(key=>process.env[key]);

test('original DSS isolates successive VM jobs and retains independent reports',
  {skip:!configured,timeout:360000},async t=>{
    const manifestPath=resolve(process.env.ONEKIT_DSS_VM_MANIFEST);
    const manifest=JSON.parse(await readFile(manifestPath,'utf8'));
    const fixture=JSON.parse(await readFile(process.env.ONEKIT_DSS_VM_FIXTURES,'utf8'));
    const {V86}=await import(pathToFileURL(resolve(process.env.ONEKIT_V86_MODULE)));
    const requests=[];
    const loadAsset=async name=>{
      requests.push(name);
      const path=name.startsWith('fs/')?resolve(process.env.ONEKIT_DSS_VM_FS_ROOT,name.slice(3))
        :resolve(dirname(manifestPath),name);
      return new Uint8Array(await readFile(path));
    };
    const previousFetch=globalThis.fetch;
    globalThis.fetch=async()=>{throw Error('unexpected_network_request');};
    let engine;
    try{
      await assert.rejects(prepareDSS({V86,manifest,loadAsset:async name=>{
        const bytes=await loadAsset(name);
        if(name===manifest.wasm)bytes[0]^=1;
        return bytes;
      }}),/asset_integrity/);
      const start=performance.now();
      engine=await prepareDSS({V86,manifest,loadAsset});
      t.diagnostic(`prepare_ms=${Math.round(performance.now()-start)}`);
      const decode=value=>new Uint8Array(Buffer.from(value,'base64'));
      const input={document:{...fixture.document,data:decode(fixture.document.data)},
        detached:{data:decode(fixture.detached.data)},certificates:fixture.certificates.map(decode)};
      const original=input.detached.data.slice();
      const retained=[];
      for(const altered of [false,true,false]){
        input.detached.data=altered?new TextEncoder().encode('altered original'):original;
        const mark=performance.now();
        const reports=await engine.validate(input);
        t.diagnostic(`altered=${altered};validation_ms=${Math.round(performance.now()-mark)}`);
        const simple=new TextDecoder().decode(reports['simple.xml']);
        assert.match(simple,altered?/<Indication>TOTAL_FAILED<\/Indication>/
          :/<Indication>INDETERMINATE<\/Indication>/);
        if(altered)assert.match(simple,/<SubIndication>HASH_FAILURE<\/SubIndication>/);
        retained.push({bytes:reports['simple.xml'],text:simple});
      }
      for(const item of retained)assert.equal(new TextDecoder().decode(item.bytes),item.text);
      assert(requests.every(name=>Object.hasOwn(manifest.files,name)));
      assert(requests.every(name=>!name.startsWith('jobs/')));
    }finally{if(engine)await engine.dispose();globalThis.fetch=previousFetch;}
  });
