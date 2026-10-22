# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Conservative lock-only automerge, bound to the exact successful CI commit."""
import base64
import json
import os
import subprocess
import tomllib


def api(path):
    return json.loads(subprocess.check_output(["gh", "api", path], text=True))


repo = os.environ["GH_REPO"]
run = api(f"repos/{repo}/actions/runs/{os.environ['RUN_ID']}")
if run["conclusion"] != "success" or run["head_repository"]["full_name"] != repo:
    raise SystemExit("Run is not eligible.")
for linked in run.get("pull_requests", []):
    pr = api(f"repos/{repo}/pulls/{linked['number']}")
    if pr["user"]["login"] != "dependabot[bot]" or pr["draft"] or pr["state"] != "open" or pr["head"]["sha"] != run["head_sha"]:
        continue
    files = api(f"repos/{repo}/pulls/{pr['number']}/files?per_page=100")
    if not files or {file["filename"] for file in files} != {"uv.lock"}:
        print("Requires review: changes include more than the Python lock file.")
        continue
    versions = []
    for ref in (pr["base"]["sha"], pr["head"]["sha"]):
        content = api(f"repos/{repo}/contents/uv.lock?ref={ref}")
        lock = tomllib.loads(base64.b64decode(content["content"]).decode())
        versions.append({item["name"]: item.get("version", "") for item in lock["package"]})
    before, after = versions
    if before.keys() != after.keys() or any(before[name].split(".")[0] != after[name].split(".")[0] or before[name].startswith("0.") and before[name].split(".")[:2] != after[name].split(".")[:2] for name in before):
        print("Requires review: new dependencies or incompatible version change.")
        continue
    subprocess.run(["gh", "pr", "merge", str(pr["number"]), "--repo", repo, "--auto", "--squash", "--match-head-commit", pr["head"]["sha"]], check=True)
