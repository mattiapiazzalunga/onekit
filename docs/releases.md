<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Release operations

Protect `main` and stable `v*` tags. Register the PyPI Trusted Publisher for repository `onekit`, workflow `release.yml` and environment `pypi`. Update the package version, lockfile, catalog and documentation, then publish a matching stable SemVer tag from a reviewed commit.

The release workflow verifies the tag, runs required CLI checks and publishes universal wheel/source distributions, the GHCR image and GitHub release assets. `onekit-release.json` contains version, source commit, asset checksums and download URLs. Publication retries must preserve existing immutable assets; code changes require a new version.

## PyPI license metadata

The PyPI package is Open Source (PolyForm Shield 1.0.0), with the noncompete restriction explained in the README displayed on its project page. `project.license` uses `LicenseRef-PolyForm-Shield-1.0.0`; the wheel and source archive include the complete LICENSE and NOTICE. The project metadata links to the license and documentation. Do not add an OSI-approved license classifier: this license restricts competing products.

Before publication, build from the intended release commit and validate the actual artifacts:

```sh
uv build
python scripts/check_distribution_licenses.py
```

CI and the release build run this check before artifacts can be published. PyPI renders the packaged README, so rebuilding is required after changing documentation or license metadata. Publish a new, unused version when replacing an already published release; existing PyPI distributions cannot be overwritten. Previously distributed versions retain their original licensing terms. The current checkout's version is not automatically advanced by a license change.

The project owner configures the PyPI account, Trusted Publisher and publication separately; local preparation does not upload packages or change the live PyPI page.

## Weekly dependency maintenance

Dependabot monitors the uv lockfile, CLI Node engine dependencies, Docker and GitHub Actions. The scheduled Checks workflow retests locked dependencies and native engines. Eligible Python lock-only updates remain subject to successful checks and branch protection.
