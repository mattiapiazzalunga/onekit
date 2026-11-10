// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
// Shared Node/browser host. loadAsset receives only public build-asset names.
// No document, certificate, request descriptor or report is passed to it.
const MiB=1024*1024;
const encode=new TextEncoder();
const reportNames=['simple.xml','detailed.xml','diagnostic.xml','etsi.xml'];
const hex=bytes=>Array.from(new Uint8Array(bytes),b=>b.toString(16).padStart(2,'0')).join('');
const arrayBuffer=bytes=>bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength);

async function decompress(bytes,expected){
  if(!Number.isSafeInteger(expected)||expected<1||expected>512*MiB)throw Error('state_size');
  const reader=new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip')).getReader();
  const chunks=[];let size=0;
  try{for(;;){const {done,value}=await reader.read();if(done)break;
    size+=value.length;if(size>expected)throw Error('state_size');chunks.push(value);
  }}catch(error){await reader.cancel().catch(()=>{});throw error;}
  if(size!==expected)throw Error('state_size');
  const result=new Uint8Array(size);let offset=0;
  for(const chunk of chunks){result.set(chunk,offset);offset+=chunk.length;}
  return result.buffer;
}

export async function prepareDSS({V86,manifest,loadAsset,decodeZstd,coldStart=false,authoring=false,timeoutMs=300000,trustTimeoutMs=timeoutMs}){
  if(manifest?.schema!=='onekit-dss-vm-v1'||manifest.dssVersion!=='6.5.1'
      ||manifest.v86Version!=='0.5.472+gcc37f35'
      ||![384*MiB,512*MiB].includes(manifest.memoryBytes))throw Error('engine_manifest');
  const verified=new Map();
  const asset=async name=>{
    const descriptor=manifest.files[name];
    if(!descriptor||!/^[-a-zA-Z0-9_./]+$/.test(name)||name.startsWith('/')
        ||name.split('/').includes('..')||!Number.isSafeInteger(descriptor.bytes)
        ||descriptor.bytes<0||descriptor.bytes>128*MiB
        ||!/^[a-f0-9]{64}$/.test(descriptor.sha256))throw Error('asset_manifest');
    if(!verified.has(name))verified.set(name,(async()=>{
      let bytes;
      if(descriptor.chunks){
        const size=descriptor.chunkSize;
        if(!Number.isSafeInteger(size)||size<65536||size>4*MiB
            ||!Array.isArray(descriptor.chunks)||descriptor.chunks.length!==Math.ceil(descriptor.bytes/size)
            ||descriptor.chunks.some(part=>!manifest.files[part]||manifest.files[part].chunks))throw Error('asset_chunks');
        bytes=new Uint8Array(descriptor.bytes);
        for(let index=0;index<descriptor.chunks.length;index+=4){
          const parts=await Promise.all(descriptor.chunks.slice(index,index+4).map(asset));
          for(let offset=0;offset<parts.length;offset++){
            const position=(index+offset)*size;
            if(parts[offset].length!==Math.min(size,descriptor.bytes-position))throw Error('asset_chunks');
            bytes.set(parts[offset],position);
            if(name===manifest.state)verified.delete(descriptor.chunks[index+offset]);
          }
        }
      }else bytes=new Uint8Array(await loadAsset(name));
      if(bytes.byteLength!==descriptor.bytes||hex(await crypto.subtle.digest('SHA-256',bytes))!==descriptor.sha256)
        throw Error('asset_integrity');
      return bytes;
    })());
    return verified.get(name);
  };
  const fileRange=async(name,offset,length)=>{
    const key=`fs/${name}`,descriptor=manifest.files[key];
    if(!descriptor||!Number.isSafeInteger(offset)||!Number.isSafeInteger(length)
        ||offset<0||length<0||offset+length>descriptor.bytes)throw Error('filesystem_range');
    if(!descriptor.chunks)return (await asset(key)).subarray(offset,offset+length);
    const size=descriptor.chunkSize;
    if(size!==65536||descriptor.chunks.length!==Math.ceil(descriptor.bytes/size))throw Error('filesystem_chunks');
    const output=new Uint8Array(length);
    const last=Math.ceil((offset+length)/size);
    // Fetch independent, verified pages together without retaining an unbounded
    // set of in-flight requests. The guest still receives the exact byte range.
    for(let first=Math.floor(offset/size);first<last;first+=4){
      const chunks=await Promise.all(descriptor.chunks.slice(first,Math.min(first+4,last)).map(asset));
      for(let part=0;part<chunks.length;part++){
        const index=first+part,chunk=chunks[part];
        if(chunk.length!==Math.min(size,descriptor.bytes-index*size))throw Error('filesystem_chunks');
        const begin=Math.max(offset,index*size),end=Math.min(offset+length,(index+1)*size);
        output.set(chunk.subarray(begin-index*size,end-index*size),begin-offset);
      }
    }
    return output;
  };
  // A restored snapshot already contains the running kernel and initrd. Only
  // cold authoring boots need to download and load their separate boot images.
  const [wasm,bios,vga,filesystem,kernel,initrd]=await Promise.all(
    ['wasm','bios','vga','filesystem',...(coldStart?['kernel','initrd']:[])].map(key=>asset(manifest[key])));
  const fs=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(filesystem));
  let readyResolve,readyReject,pending=null,line='',disposed=false;
  const ready=new Promise((resolve,reject)=>{readyResolve=resolve;readyReject=reject;});
  const timer=setTimeout(()=>readyReject(Error('engine_start_timeout')),timeoutMs);
  const vm=new V86({
    wasm_fn:async imports=>(await WebAssembly.instantiate(wasm,imports)).instance.exports,
    bios:{buffer:arrayBuffer(bios)},vga_bios:{buffer:arrayBuffer(vga)},
    ...(coldStart?{bzimage:{buffer:arrayBuffer(kernel)},initrd:{buffer:arrayBuffer(initrd)}}:{}),
    memory_size:manifest.memoryBytes,vga_memory_size:MiB,filesystem:{},
    cmdline:'console=ttyS0,115200 loglevel=3 nowatchdog pnpbios=off init_on_free=1',autostart:false,
    disable_speaker:true,disable_keyboard:true,disable_mouse:true,
  });
  const dispose=async()=>{
    if(disposed)return;disposed=true;clearTimeout(timer);
    if(pending){clearTimeout(pending.timer);pending.reject(Error('engine_disposed'));pending=null;}
    await vm.stop();await vm.destroy();verified.clear();
  };
  vm.add_listener('serial0-output-byte',byte=>{
    if(byte!==10){if(line.length<4096)line+=String.fromCharCode(byte);return;}
    const message=line.replace(/\r$/,'');line='';
    if(message.includes('Kernel panic')||message.startsWith('Exception in thread "main"')
        ||message.includes('java.lang.OutOfMemoryError')){
      readyReject(Error('engine_failed'));
      if(pending){clearTimeout(pending.timer);pending.reject(Error('engine_failed'));pending=null;}
      void dispose();return;
    }
    if(coldStart&&message==='ONEKIT_DSS_READY=1')readyResolve();
    if(!pending)return;
    const report=/^ONEKIT_DSS_REPORT=([a-zA-Z0-9_-]+)\|([a-z]+\.xml)\|(\d+)\|([a-f0-9]{64})$/.exec(message);
    if(report&&report[1]===pending.id&&reportNames.includes(report[2]))
      pending.reports.set(report[2],{bytes:Number(report[3]),sha256:report[4]});
    if(message===`ONEKIT_DSS_DONE=${pending.id}`){clearTimeout(pending.timer);const job=pending;pending=null;job.resolve();}
    else if(message.startsWith(`ONEKIT_DSS_ERROR=${pending.id}|`)){
      clearTimeout(pending.timer);const job=pending;pending=null;job.reject(Error('validation_failed'));
    }
  });
  vm.add_listener('emulator-ready',()=>{void(async()=>{
    // v86's storage interface is pinned and tested with this exact release.
    // Replace its HTTP-backed loader: every lazy file read must pass full SHA-256.
    if(!vm.fs9p?.load_from_json)throw Error('filesystem_api');
    vm.fs9p.storage={
      read:async(...arguments_)=>{
        try{return await fileRange(...arguments_);}catch(error){
          readyReject(error);
          if(pending){clearTimeout(pending.timer);pending.reject(Error('engine_asset_failure'));pending=null;}
          await dispose();throw error;
        }
      },
      cache:async()=>{},uncache:()=>{},
    };
    vm.fs9p.load_from_json(fs);
    if(!coldStart){
      let compressed=await asset(manifest.state);
      const expected=manifest.stateExpandedBytes;
      verified.delete(manifest.state);
      for(const part of manifest.files[manifest.state]?.chunks||[])verified.delete(part);
      let state;
      if(manifest.stateCompression==='zstd'){
        if(!Number.isSafeInteger(expected)||expected<1||expected>512*MiB
            ||!/^[a-f0-9]{64}$/.test(manifest.stateExpandedSha256))throw Error('state_manifest');
        if(decodeZstd){
          // A native host can decode outside the emulator's linear memory,
          // which cannot shrink after a large temporary allocation.
          state=await decodeZstd(expected,compressed);
          if(ArrayBuffer.isView(state))state=state.byteOffset===0&&state.byteLength===state.buffer.byteLength
            ?state.buffer:arrayBuffer(state);
          if(!(state instanceof ArrayBuffer))throw Error('state_decoder');
        }else if(typeof Worker==='function'){
          // Reuse the pinned runtime's decoder in a temporary worker. Releasing
          // that worker avoids retaining its large decode arena in the VM heap.
          vm.wasm_source=arrayBuffer(wasm);
          try{state=await vm.zstd_decompress_worker(expected,compressed);}
          finally{vm.zstd_worker?.terminate();vm.zstd_worker=null;vm.wasm_source=arrayBuffer(wasm);}
        }else state=vm.zstd_decompress(expected,compressed);
      }else if(!manifest.stateCompression||manifest.stateCompression==='gzip')state=await decompress(compressed,expected);
      else throw Error('state_compression');
      compressed=undefined;
      if(manifest.stateCompression==='zstd'&&(state.byteLength!==expected
          ||hex(await crypto.subtle.digest('SHA-256',state))!==manifest.stateExpandedSha256))throw Error('state_integrity');
      await vm.restore_state(state);
    }
    await vm.create_file('seed.bin',crypto.getRandomValues(new Uint8Array(32)));
    if(coldStart){
      const jobs=vm.fs9p.SearchPath('jobs').id;
      if(jobs<0)throw Error('jobs_directory');
      if(vm.fs9p.SearchPath('jobs/boot').id<0)vm.fs9p.CreateDirectory('boot',jobs);
      const now=Date.now(),clock=new Uint8Array(16),view=new DataView(clock.buffer);
      view.setBigInt64(0,BigInt(Math.floor(now/1000)),true);
      view.setBigInt64(8,BigInt(now%1000)*1000000n,true);
      await vm.create_file('jobs/boot/host-clock.bin',clock);
      await vm.create_file('jobs/boot/seed.bin',crypto.getRandomValues(new Uint8Array(32)));
    }
    vm.run();if(!coldStart)readyResolve();
  })().catch(readyReject);});
  try{await ready;}catch(error){await dispose();throw error;}finally{clearTimeout(timer);}
  let busy=false,hasValidatedUserData=false;
  return {
    dispose,
    async captureForAuthoring(){
      if(!authoring||!coldStart||hasValidatedUserData||busy||disposed)throw Error('snapshot_capture_disabled');
      await vm.stop();return vm.save_state();
    },
    async validate({document,detached,certificates=[],crls=[],ocsps=[],trustedLists}){
      if(disposed||busy)throw Error('engine_unavailable');busy=true;
      hasValidatedUserData=true;
      // The guest kernel caches 9p dentries/pages. Replacing a host file at the
      // same path does not invalidate that cache: every job needs fresh paths.
      const id='job_'+hex(crypto.getRandomValues(new Uint8Array(16)));
      const directory=`jobs/${id}`;
      const properties=[];
      let jobTimeout=timeoutMs;
      const property=(key,value)=>properties.push(key+'='+String(value).replace(/\\/g,'\\\\')
        .replace(/\r/g,'\\r').replace(/\n/g,'\\n').replace(/\t/g,'\\t').replace(/ /g,'\\ '));
      const put=async(key,item,name,limit)=>{
        if(!(item.data instanceof Uint8Array)||item.data.byteLength>limit)throw Error('resource_size');
        try{await vm.create_file(`${directory}/${name}`,item.data.slice());}
        catch{throw Error('input_path_'+name);}
        properties.push(`${key}=${name}`);
      };
      try{
        const parent=vm.fs9p.SearchPath('jobs').id;
        if(parent<0)throw Error('jobs_directory');
        vm.fs9p.CreateDirectory(id,parent);
        const extension=/\.([a-zA-Z0-9]{1,12})$/.exec(document.name||'')?.[1]||'bin';
        await put('document',document,`document.${extension}`,64*MiB);
        property('document.name',document.name||`document.${extension}`);
        if(detached)await put('detached',detached,'detached.bin',64*MiB);
        if(detached)property('detached.name',detached.name||'detached.bin');
        let total=0,count=0;
        for(const [key,items]of [['certificate',certificates],['crl',crls],['ocsp',ocsps]]){
          count+=items.length;if(count>256)throw Error('evidence_count');
          properties.push(`${key}.count=${items.length}`);
          for(let index=0;index<items.length;index++){
            total+=items[index].length;if(total>32*MiB)throw Error('evidence_size');
            await put(`${key}.${index}`,{data:items[index]},`${key}-${index}.bin`,32*MiB);
          }
        }
        if(trustedLists){
          const trust=manifest.trustLists,now=Date.now();
          let changed=!trust||now<Date.parse(trust.validFrom)||now>=Date.parse(trust.expires);
          const hash=async bytes=>hex(await crypto.subtle.digest('SHA-256',bytes));
          if(!trust||await hash(trustedLists.lotl)!==trust.sourceSha256?.[trust.lotlUrl])changed=true;
          for(const item of trustedLists.lists)
            if(!trust||await hash(item.data)!==trust.sourceSha256?.[item.url])changed=true;
          if(changed){
            if(!manifest.trustEvidence)throw Error('trust_evidence_unsupported');
            jobTimeout=trustTimeoutMs;
            const resources=[{url:null,data:trustedLists.lotl},...trustedLists.lists];
            count+=resources.length;if(count>256)throw Error('evidence_count');
            properties.push(`tl.count=${trustedLists.lists.length}`);
            for(let index=0;index<resources.length;index++){
              const item=resources[index];total+=item.data.length;if(total>32*MiB)throw Error('evidence_size');
              if(index===0)await put('lotl',item,'lotl.xml',32*MiB);
              else{await put(`tl.${index-1}.path`,item,`tl-${index-1}.xml`,32*MiB);property(`tl.${index-1}.url`,item.url);}
            }
          }
        }
        const now=Date.now();properties.push(`validationTime=${new Date(now).toISOString()}`);
        const clock=new Uint8Array(16),view=new DataView(clock.buffer);
        view.setBigInt64(0,BigInt(Math.floor(now/1000)),true);
        view.setBigInt64(8,BigInt(now%1000)*1000000n,true);
        await vm.create_file(`${directory}/host-clock.bin`,clock);
        await vm.create_file(`${directory}/seed.bin`,crypto.getRandomValues(new Uint8Array(32)));
        await vm.create_file(`${directory}/request.properties`,encode.encode(properties.join('\n')+'\n'));
        const committed=new Map();
        await new Promise((resolve,reject)=>{
          pending={id,resolve,reject,reports:committed,timer:setTimeout(()=>{
            pending=null;reject(Error('validation_timeout'));void dispose();
          },jobTimeout)};
          vm.serial0_send(`RUN ${id}\n`);
        });
        const result={};
        for(const name of reportNames){
          const expected=committed.get(name);
          if(manifest.reportCommit&&!expected)throw Error('report_commit_missing');
          if(expected&&(!Number.isSafeInteger(expected.bytes)||expected.bytes<1||expected.bytes>64*MiB))throw Error('report_size');
          let bytes;const deadline=Date.now()+30000;
          while(Date.now()<deadline){
            try{bytes=await vm.read_file(`${directory}/${name}`);}catch{bytes=null;}
            if(bytes?.length&&bytes.length<=64*MiB&&!bytes.includes(0)){
              if(expected){
                if(bytes.length===expected.bytes&&hex(await crypto.subtle.digest('SHA-256',bytes))===expected.sha256)break;
              }else{
                const tail=new TextDecoder().decode(bytes.subarray(Math.max(0,bytes.length-160)));
                if(/<\/(?:[\w.-]+:)?(?:SimpleReport|DetailedReport|DiagnosticData|ValidationReport)>\s*$/.test(tail))break;
              }
            }
            bytes=null;await new Promise(resolve=>setTimeout(resolve,50));
          }
          if(!bytes||bytes.length>64*MiB)throw Error('report_missing_or_size');result[name]=bytes.slice();}
        return result;
      }finally{
        if(!disposed){
          const node=vm.fs9p.SearchPath(directory).id;
          if(node>=0){
            for(const name of vm.fs9p.read_dir(directory)||[]){
              const child=vm.fs9p.Search(node,name);
              if(child>=0){await vm.fs9p.DeleteData(child);vm.fs9p.Unlink(node,name);}
            }
            vm.fs9p.Unlink(vm.fs9p.SearchPath('jobs').id,id);
          }
        }
        busy=false;
      }
    },
  };
}
