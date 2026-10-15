<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Architecture and extension guide

`Artifact(name, data)` is an immutable, portable named byte payload. `Result(files, warnings, details)` carries outputs and fidelity notices. `execute(tool_id, files, options, browser=False)` validates catalog contracts and lazily imports a family strategy. `pipeline(steps, files, browser=False)` composes those same operations, mapping multiple artifacts through single-input steps and stopping on the first error.

The registry defines stable IDs, family, handler, accepted/output kinds, multiplicity, options, fidelity and dependencies. Shared family adapters avoid one implementation per format combination. Each generated directory under `tools/CATEGORY/ID` points to its implementation. Regenerate with `python scripts/tool_docs.py`.

CLI filesystem operations remain outside processing. Portable names reject traversal and Windows devices. Outputs use temporary files and atomic replacement, and preserve existing files by default. External engine adapters use argument arrays, temporary directories and bounded timeouts. The registry cannot load arbitrary user plugin module names or shell fragments.

Browser export produces a deterministic source ZIP, catalog, pinned dependency manifest and shared loader. This is application code, not a mirrored CLI wheel. The worker invokes the same API with `browser=True`; native engines are rejected. Pure-Python browser pins live in `browser/requirements.txt`; compiled packages use the pinned Pyodide lock. Real shared fixtures check CPython/Pyodide text-output parity. UI checks belong to the independent webapp repository.

To add a tool: implement its family strategy; declare the catalog contract; add semantic, invalid-input, regression and resource-limit tests; declare small optional dependencies and review licenses; add a real browser fixture before enabling browser support; regenerate tool directories; document fidelity and platform requirements. Never label heuristic conversion as perfect.

The core has no web framework, database or cloud dependency. A future API should adapt Artifact/Result and add its own authentication, quotas, isolation and retention policy. The browser flag is not a native multi-tenant sandbox.
