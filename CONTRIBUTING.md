<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Contributing

Find work in [GitHub issues](https://github.com/mattiapiazzalunga/onekit/issues) and the [website request board](https://onekit.org/requests/). Discuss contract changes and large dependencies before implementation.

Install `.[all,test]` in a virtual environment or use `uv sync --locked --extra all --extra test`. Run `python -m pytest -q`. New features and fixes require semantic tests, regression fixtures and relevant invalid-input/resource-limit cases. Browser tools also require shared Pyodide fixtures; native engine changes need integration coverage. Mandatory CI gates cover compatibility, regressions, browser/native execution, security, licenses and packaging.

Keep Artifact/Result independent of CLI/HTTP/storage. Prefer small optional dependencies and lazy imports. Never evaluate user code merely to validate it. Use argument arrays, no shell execution and bounded native timeouts. Document compromise behavior honestly. Update catalog, tool directories, guides and locks together.

Preserve original and third-party notices. New original files carry `Copyright 2026 Mattia Piazzalunga` and `SPDX-License-Identifier: Apache-2.0`. Contributions use Apache-2.0. Record appropriate attribution without claiming upstream ownership. Do not commit credentials, private files, virtual environments or dependency directories.
