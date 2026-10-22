// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import {createRequire} from 'node:module';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
const require=createRequire(resolve(process.argv[2],'package.json'));
const chunks=[];for await(const chunk of process.stdin)chunks.push(chunk);
const {operation,language,text}=JSON.parse(Buffer.concat(chunks).toString());
try{
  const {transformSource,pluginPackages}=await import('./source_engine.mjs');
  const result=await transformSource({operation,language,text},{
    load:async name=>require(name),
    plugins:async language=>{
      const name=pluginPackages[language];if(!name)return [];
      const loaded=await import(pathToFileURL(require.resolve(name)).href);
      return [loaded.default||loaded];
    }
  });
  process.stdout.write(result);
}catch(error){process.stderr.write(String(error.message).slice(0,2000));process.exit(1);}
