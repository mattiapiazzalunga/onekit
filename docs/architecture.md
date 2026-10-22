<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Architecture and extension guide

`Artifact(name, data)` is an immutable named byte payload. `Result(files, warnings, details)` carries outputs and fidelity notices. `execute(tool_id, files, options)` validates contracts and lazily imports a processing adapter. `pipeline(steps, files)` composes operations and maps multiple outputs through single-input steps.

The catalog defines stable IDs, families, accepted and output kinds, multiplicity, options, fidelity, limits and dependencies. Processing adapters are independent of CLI filesystem access. Portable names reject traversal and reserved device names. CLI output writes preserve existing files by default. Native engine calls use argument arrays, temporary directories and bounded timeouts.

To add a tool, implement its family adapter, declare the catalog entry, add semantic and invalid-input regression tests, declare optional dependencies and review licenses. Regenerate tool directories with `python scripts/tool_docs.py`. Document fidelity and platform requirements.


Processing API v1 is described in `contracts/processing-v1.json`. Run `python scripts/check_contracts.py` before submitting changes. Adding tools, formats and options is compatible; removing existing IDs/options, changing output kinds or narrowing input contracts requires an explicit versioned migration. Internal algorithms and handler organization may change without changing the public contract.

`ExecutionContext` lets Python callers lower batch and per-tool budgets and supply a trusted local media metadata reader. It does not accept engine services through user-provided tool options. Contexts are immutable, scoped to one execution and shared by pipeline steps. The CLI uses the default local engine services.

The Node source adapter delegates formatting and minification rules to `tools/developer/source_engine.mjs`. Its engine loader is a process-level dependency; source text cannot choose arbitrary packages or executable commands.
