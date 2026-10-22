<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# CLI requirements verification

`tests/test_requirements.py` checks catalog coverage, CLI invocations and malformed pipelines. `tests/test_core.py` verifies processing contracts and output semantics. Input validation, archive expansion, encryption and filesystem protections have dedicated regression tests.

Run `python -m pytest -q` for the default suite. Separately installed engines are tested with `python -m pytest -q -m native`; provision the dependencies described in `docs/engines.md` before running these checks. Passing the default suite does not verify all external engines or every supported platform.
