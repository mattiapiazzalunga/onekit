# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Keep the published 0.6.2 OCI graph and delete other OneKit package versions."""
import hashlib
import json
import os
import re
import urllib.request

OWNER = "mattiapiazzalunga"
PACKAGE = "onekit"
KEEP_TAG = "v0.6.2"
API_PATH = f"/users/{OWNER}/packages/container/{PACKAGE}/versions"


def deletion_plan(versions, fetch_manifest):
    roots = [item for item in versions if KEEP_TAG in item["metadata"]["container"]["tags"]]
    if len(roots) != 1:
        raise RuntimeError("Expected exactly one published v0.6.2 package version.")
    pending = [roots[0]["name"]]
    protected = set()
    while pending:
        digest = pending.pop()
        if digest in protected:
            continue
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
            raise RuntimeError("Unexpected OCI digest.")
        manifest = fetch_manifest(digest)
        protected.add(digest)
        pending.extend(item["digest"] for item in manifest.get("manifests", []))
    available = {item["name"] for item in versions}
    if not protected <= available:
        raise RuntimeError("Incomplete package inventory; refusing deletion.")
    return protected, [item for item in versions if item["name"] not in protected]


def main():
    token = os.environ["GH_TOKEN"]

    def api(path, method="GET"):
        request = urllib.request.Request("https://api.github.com" + path, method=method, headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "User-Agent": "OneKit-package-cleanup",
        })
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read()
            return json.loads(body) if body else None

    # The package is public: registry downloads never receive the GitHub token.
    with urllib.request.urlopen(f"https://ghcr.io/token?service=ghcr.io&scope=repository:{OWNER}/{PACKAGE}:pull", timeout=30) as response:
        pull_token = json.load(response)["token"]

    def fetch_manifest(digest):
        request = urllib.request.Request(f"https://ghcr.io/v2/{OWNER}/{PACKAGE}/manifests/{digest}", headers={
            "Authorization": "Bearer " + pull_token,
            "Accept": "application/vnd.oci.image.index.v1+json, application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.list.v2+json, application/vnd.docker.distribution.manifest.v2+json",
        })
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read()
        if "sha256:" + hashlib.sha256(body).hexdigest() != digest:
            raise RuntimeError("Registry manifest checksum mismatch.")
        return json.loads(body)

    def inventory():
        result = []
        page = 1
        while True:
            batch = api(f"{API_PATH}?per_page=100&page={page}")
            result.extend(batch)
            if len(batch) < 100:
                return result
            page += 1

    versions = inventory()
    protected, obsolete = deletion_plan(versions, fetch_manifest)
    print(f"Preserving {KEEP_TAG} and {len(protected)} OCI manifests, including platform images and attestations.")
    for item in obsolete:
        print("Deleting obsolete version:", item["id"], item["name"], item["metadata"]["container"]["tags"])
        api(f"{API_PATH}/{item['id']}", "DELETE")
    remaining = inventory()
    if {item["name"] for item in remaining} != protected:
        raise RuntimeError("Package changed during cleanup or obsolete versions remain.")
    print(f"Verified: only {KEEP_TAG} and its required OCI manifests remain.")


if __name__ == "__main__":
    main()
