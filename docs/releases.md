<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Release operations

Create public `mattiapiazzalunga/onekit` and private `mattiapiazzalunga/onekit-webapp`. Protect `main`, require the final `required` check, restrict stable `v*` tags and enable Dependabot/auto-merge. Configure `pypi` and `release` environments with tag restrictions; mandatory human reviewers prevent fully automatic publication.

Register PyPI pending Trusted Publisher `onekit-tools`, owner `mattiapiazzalunga`, repository `onekit`, workflow `release.yml`, environment `pypi`. No PyPI API token is needed. Make the GHCR package public. Install a GitHub App on the private webapp only, with Contents read/write. Store `WEBAPP_APP_ID` and secret `WEBAPP_APP_PRIVATE_KEY` in core release settings; dispatch uses a short-lived installation token.

Update `__version__`, lockfiles, catalog/docs and fixtures; merge reviewed code to `main`; create and push matching stable `vMAJOR.MINOR.PATCH`. Initial version is `v0.1.0`. The workflow verifies version and main ancestry, runs mandatory checks against the exact tag, builds the universal wheel/source distribution and publishes PyPI, an attested multi-architecture GHCR image and versioned GitHub assets. It dispatches the private webapp only after publication completes.

`onekit-release.json` records version, tag, source commit, Python requirement, SHA-256 digests and direct asset URLs. The webapp verifies tag/manifest consistency and rebuilds only its browser runtime source and metadata; downloadable wheels/source remain exclusively on GitHub Releases.

Retry **Release** with the same tag after an infrastructure failure. Existing published files must match; never move tags or overwrite stable assets. Registries do not share an atomic transaction, so a partial publication may need an idempotent retry. Code fixes require a new version. The downstream deploy job is blocked if synchronization, source tracking, tests, security or licenses fail; its previous Cloudflare version remains active. Worker rollback restores assets/code together; D1 has a separate backup/migration lifecycle.

Dependabot monitors universal Python locks, browser requirements, Node locks, Actions and Docker. Audits include declared extras. Unknown runtime licenses fail closed. Only Dependabot lock-only Python changes with unchanged package set, compatible major/pre-1.0 minor versions and an exact successful current CI commit can auto-merge; branch protections remain authoritative. Other changes require review.
