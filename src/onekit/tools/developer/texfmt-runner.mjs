// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import {readFile} from 'node:fs/promises';
import {init,format} from '../../data/texfmt/host.mjs';
await init({bytes:await readFile(new URL('../../data/texfmt/tex_fmt_bg.wasm',import.meta.url))});
const chunks=[];let length=0;
for await(const chunk of process.stdin){length+=chunk.length;if(length>256*1024)throw Error('Source is too complex. Split it into smaller files.');chunks.push(chunk);}
process.stdout.write(format(new TextDecoder('utf-8',{fatal:true}).decode(Buffer.concat(chunks))));
