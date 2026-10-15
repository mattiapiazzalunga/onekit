// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: Apache-2.0
import {loadPyodide} from 'pyodide';
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import assert from 'node:assert/strict';
import {packageInstaller} from '../browser-loader.mjs';
process.on('uncaughtException',error=>{console.error(String(error.message));process.exit(1);});
const path=resolve('.browser-test');
const catalog=JSON.parse(await readFile(resolve(path,'catalog.json'),'utf8'));
const dependencies=JSON.parse(await readFile(resolve(path,'dependencies.json'),'utf8'));
const fixtures=JSON.parse(await readFile(resolve(path,'fixtures.json'),'utf8'));
const py=await loadPyodide({packageCacheDir:resolve(path,'packages')});
const bytes=await readFile(resolve(path,'runtime.zip'));
py.unpackArchive(new Uint8Array(bytes.buffer,bytes.byteOffset,bytes.byteLength),'zip',{extractDir:'/onekit'});py.runPython("import sys;sys.path.insert(0,'/onekit')");await py.loadPackage('micropip');
const install=packageInstaller(py,dependencies);
for(const fixture of fixtures){
  const tool=catalog.tools.find(t=>t.id===fixture.tool);
  await install(tool.packages);
  py.globals.set('_fixture',JSON.stringify(fixture));
  const result=JSON.parse(py.runPython(`
import json,base64
from onekit import Artifact, execute
def _run(raw):
    f=json.loads(raw)
    result=execute(f['tool'], [Artifact(x['name'],base64.b64decode(x['data'])) for x in f['files']], f['options'], browser=True)
    return json.dumps([{'name':x.name,'data':base64.b64encode(x.data).decode()} for x in result.files])
_run(_fixture)
`));
  assert.deepEqual(result.map(x=>x.name),fixture.expectedNames,fixture.tool);
  for(const text of fixture.expectedText||[])assert.equal(result.find(f=>f.name===text.name).data,text.data,fixture.tool);
  console.log(`PASS ${fixture.tool}`);
}
console.log(`Passed ${fixtures.length} browser runtime contracts.`);
