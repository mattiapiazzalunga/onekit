# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import json
import shutil
import subprocess
from pathlib import Path

import pytest

NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="Node.js is an optional CLI engine")


def test_source_contract_rejects_entities_and_preserves_compiled_output_names():
    engine = (Path(__file__).parents[1] / "src/onekit/tools/developer/source_engine.mjs").as_uri()
    program = """
import {transformSource,sourceResult} from ENGINE;
let loaded=false,rejected=false;
try{await transformSource({operation:'minify',language:'svg',text:'<!DOCTYPE svg><svg/>'},{load:async()=>{loaded=true;}});}catch{rejected=true;}
if(!rejected||loaded)throw Error('Unsafe XML reached the engine');
const result=await sourceResult({id:'dev-minify-typescript',fidelity:'exact'}, {name:'source.ts',data:new TextEncoder().encode('const n:number=1')}, async()=> 'const n=1;');
const invalid=await sourceResult({id:'dev-validate-typescript',fidelity:'exact'}, {name:'source.ts',data:new TextEncoder().encode('invalid')}, async()=>{throw Error('invalid syntax');});
console.log(JSON.stringify({name:result.files[0].name,valid:invalid.details.valid}));
""".replace("ENGINE", json.dumps(engine))
    result = subprocess.run([NODE, "--input-type=module", "-e", program], capture_output=True, text=True, check=True)
    assert json.loads(result.stdout) == {"name": "source.js", "valid": False}
