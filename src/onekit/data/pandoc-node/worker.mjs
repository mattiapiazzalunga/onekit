// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: GPL-2.0-or-later
import {createPandocInstance} from './pandoc-core.mjs';
import {convert} from './host.mjs';
let ready,queue=Promise.resolve();
async function prepare(){
  return ready??=(async()=>{
    let bytes;
    for(let attempt=0;attempt<2;attempt++){
      const response=await fetch(new URL('./pandoc.wasm.gz',import.meta.url),attempt?{cache:'reload'}:{});
      if(!response.ok)throw Error('Document conversion failed.');
      try{
        const reader=response.body.pipeThrough(new DecompressionStream('gzip')).getReader(),chunks=[];let length=0;
        try{for(;;){const {value,done}=await reader.read();if(done)break;length+=value.length;if(length>64*1024*1024)throw Error('Document conversion failed.');chunks.push(value);}}
        finally{await reader.cancel();}
        const expanded=new Uint8Array(length);let offset=0;for(const chunk of chunks){expanded.set(chunk,offset);offset+=chunk.length;}
        bytes=expanded.buffer;
        const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),b=>b.toString(16).padStart(2,'0')).join('');
        if(hash!=='b47c9de52b5b45f103c2dac6fea52591aeafe3dd6cafed13331b67575233a2ff')throw Error('Document conversion failed.');
        break;
      }catch(error){if(attempt)throw error;}
    }
    const instance=await createPandocInstance(bytes);
    // Initialization is complete only after the Haskell runtime answers.
    await convert(instance,{options:{from:'latex',to:'html',sandbox:true},stdin:'OneKit'});
    return instance;
  })().catch(error=>{ready=undefined;throw error;});
}
self.onmessage=({data})=>{
  queue=queue.then(async()=>{
    try{
      const engine=await prepare();
      const result=data.type==='prepare'?null:await convert(engine,data.request);
      self.postMessage({id:data.id,result});
    }catch{self.postMessage({id:data.id,error:'Document conversion failed.'});}
  });
};
