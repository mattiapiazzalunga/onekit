# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
import json
from pathlib import Path

allowed = {"MIT", "ISC", "BSD-2-Clause", "BSD-3-Clause", "Apache-2.0", "(Apache-2.0 WITH LLVM-exception)", "0BSD", "BlueOak-1.0.0", "CC0-1.0"}
for file in (Path("package-lock.json"), Path("src/onekit/tools/developer/node/package-lock.json")):
    for name, info in json.loads(file.read_text())["packages"].items():
        if not name:
            continue
        approved_runtime = name == "node_modules/pyodide" and info["version"] == "314.0.7" and info.get("license") == "MPL-2.0"
        if info.get("license") not in allowed and not approved_runtime:
            raise SystemExit(f"License review required: {file}: {name} {info['version']}: {info.get('license')}")
print("Node engine and browser-runtime license policy passed.")
