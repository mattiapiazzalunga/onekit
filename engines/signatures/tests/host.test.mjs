// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {gzipSync} from 'node:zlib';
import {prepareDSS} from '../host.mjs';

test('lazy filesystem reads fetch at most four pages concurrently and verify each page',async()=>{
  const hash=async bytes=>Buffer.from(await crypto.subtle.digest('SHA-256',bytes)).toString('hex');
  const assets=new Map([['base',new Uint8Array([1])],['kernel.bin',new Uint8Array([2])],
    ['initrd.gz',new Uint8Array([3])],['fs.json',new TextEncoder().encode('{}')],
    ['state.gz',new Uint8Array(gzipSync(new Uint8Array([1])))]]);
  const source=Uint8Array.from({length:8*65536+123},(_,index)=>index%251);
  const chunks=[];
  for(let offset=0;offset<source.length;offset+=65536){
    const name=`chunks/page${chunks.length}.bin`;chunks.push(name);assets.set(name,source.slice(offset,offset+65536));
  }
  const files=Object.fromEntries(await Promise.all([...assets].map(async([name,bytes])=>
    [name,{bytes:bytes.length,sha256:await hash(bytes)}])));
  files['fs/test.bin']={bytes:source.length,sha256:await hash(source),chunkSize:65536,chunks};
  const manifest={schema:'onekit-dss-vm-v1',dssVersion:'6.5.1',v86Version:'0.5.472+gcc37f35',
    memoryBytes:512*1024*1024,files,wasm:'base',bios:'base',vga:'base',kernel:'kernel.bin',initrd:'initrd.gz',
    filesystem:'fs.json',state:'state.gz',stateExpandedBytes:1};
  let vm,active=0,peak=0;const loaded=[];
  class FakeV86{
    constructor(options){vm=this;assert.equal(options.bzimage,undefined);assert.equal(options.initrd,undefined);this.fs9p={load_from_json(){}};}
    add_listener(name,callback){if(name==='emulator-ready')queueMicrotask(callback);}
    async restore_state(){}
    async create_file(){}
    run(){}
    async stop(){}
    async destroy(){this.destroyed=true;}
  }
  const engine=await prepareDSS({V86:FakeV86,manifest,loadAsset:async name=>{
    loaded.push(name);
    if(name.startsWith('chunks/')){
      active++;peak=Math.max(peak,active);
      await new Promise(resolve=>setTimeout(resolve,5));active--;
    }
    return assets.get(name).slice();
  }});
  try{
    assert.ok(!loaded.includes('kernel.bin'));assert.ok(!loaded.includes('initrd.gz'));
    const offset=33,length=8*65536-offset;
    assert.deepEqual(await vm.fs9p.storage.read('test.bin',offset,length),source.slice(offset,offset+length));
    assert.equal(peak,4);
    assert.deepEqual(await vm.fs9p.storage.read('test.bin',65535,3),source.slice(65535,65538));
    assert.equal((await vm.fs9p.storage.read('test.bin',0,0)).length,0);
    await assert.rejects(vm.fs9p.storage.read('test.bin',source.length,1),/filesystem_range/);
    assert.equal(vm.destroyed,true);
  }finally{await engine.dispose();}
  // A new instance must reject a modified page before exposing any range.
  const second=await prepareDSS({V86:FakeV86,manifest,loadAsset:async name=>{
    const bytes=assets.get(name).slice();if(name===chunks[8])bytes[0]^=1;return bytes;
  }});
  try{await assert.rejects(vm.fs9p.storage.read('test.bin',8*65536,123),/asset_integrity/);}
  finally{await second.dispose();}
  manifest.stateCompression='zstd';manifest.stateExpandedSha256=await hash(new Uint8Array([1]));
  let decoded=false;
  const native=await prepareDSS({V86:FakeV86,manifest,loadAsset:async name=>assets.get(name),
    decodeZstd:(expected,bytes)=>{
      assert.equal(expected,1);assert.deepEqual(bytes,assets.get('state.gz'));
      decoded=true;return new Uint8Array([1]);
    }});
  assert.equal(decoded,true);await native.dispose();
  await assert.rejects(prepareDSS({V86:FakeV86,manifest,loadAsset:async name=>assets.get(name),
    decodeZstd:()=>new Uint8Array([2])}),/state_integrity/);
});
