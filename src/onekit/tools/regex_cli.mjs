// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import {testRegex} from './regex_engine.mjs';
import {runInNewContext} from 'node:vm';
let source='';
for await(const chunk of process.stdin){source+=chunk;if(source.length>2*1024*1024)throw new Error('Regex request exceeds its input limit.');}
try{
  const request=JSON.parse(source);
  const report=runInNewContext('testRegex(text,options)',{testRegex,text:request.text,options:request.options},{timeout:2000});
  process.stdout.write(JSON.stringify(report));
}catch(error){process.stderr.write(error.code==='ERR_SCRIPT_EXECUTION_TIMEOUT'?'Regex exceeded its 2 second time limit.':String(error.message||error));process.exitCode=2;}
