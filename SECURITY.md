<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Security policy

Report vulnerabilities privately to `security@onekit.org` with version, platform, tool, dependency versions, impact and synthetic reproduction. Do not publish sensitive files, credentials or exploit-ready private reports on public trackers. Fixes target the latest stable release; no response-time guarantee is implied.

The core bounds paths, input sizes, archive expansion, image pixels, comparisons and pipelines. Encryption uses authenticated AES-256-GCM with fresh salt/nonce and scrypt; lost passwords cannot be recovered. Existing outputs are preserved by default. Python validation parses source without executing it.

External converters/compilers are separate native programs, not a complete sandbox. Keep them updated and isolate hostile documents using OS controls. The CLI is not an unauthenticated remote conversion service. Editing a signed PDF can invalidate signatures; PDF permissions are not equivalent to encryption integrity.

Ordinary checks must never receive publication secrets. Stable tags identify reviewed protected-main commits. Dependency, license and security failures block publication. No test suite guarantees immunity to all malformed inputs or attacks.
