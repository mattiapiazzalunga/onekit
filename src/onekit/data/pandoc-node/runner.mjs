// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: GPL-2.0-or-later
import {pathToFileURL} from 'node:url';
import {resolve} from 'node:path';
import {convert} from './host.mjs';
try{
  const instance=await import(pathToFileURL(resolve(process.argv[2],'node_modules/pandoc-wasm/src/index.node.js')));
  const chunks=[];let bytes=0;
  for await(const chunk of process.stdin){bytes+=chunk.length;if(bytes>2*1024*1024)throw Error('Document conversion failed.');chunks.push(chunk);}
  const result=await convert(instance,JSON.parse(Buffer.concat(chunks).toString('utf8')));
  process.stdout.write(JSON.stringify(result));
}catch{process.stderr.write('Document conversion failed.');process.exitCode=1;}
