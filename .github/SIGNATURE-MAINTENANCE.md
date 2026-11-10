# Signature dependency notifications

Dependabot checks the Maven project in `engines/signatures` daily at 07:00
Europe/Rome. It groups DSS modules and assigns update PRs to the repository owner.
The existing conservative automerge accepts only eligible Python lock changes;
Maven/DSS changes require review.

The `Signature dependency alerts` workflow runs daily at 06:37 UTC and can also
be started manually. It checks the official `esig/dss` stable release and compares
each bundled European trust list, including the LOTL, with its public source.
Changes, expiry within seven days, missing expiry information, mismatched engine
locks and unavailable sources open or update one issue assigned to
`mattiapiazzalunga`. A clean check closes that issue. Failed checks remain visible
as workflow failures and never produce an all-clear report. Reports are retained
as workflow artifacts; GitHub notification delivery follows the owner's settings.

This monitor does not authenticate or install remote XML, update dependencies,
rebuild binaries or publish releases. XML changes must pass the authenticated
`onekit.signature_evidence` updater before integration. New DSS binaries require
matching dependency/source hashes, license review and validation tests.

Run locally with `python scripts/check_signature_updates.py`. Its Markdown and
JSON reports are written under `.artifacts/signature-maintenance/`. The committed
Maven project, dependency lock and trust-list snapshot are required inputs.
Schedules become active only after these files are on the default branch.
