# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
import json
import os
import subprocess
import urllib.request

commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
payload = {"event_type": "core-released", "client_payload": {"tag": os.environ["RELEASE_TAG"], "commit": commit}}
request = urllib.request.Request("https://api.github.com/repos/mattiapiazzalunga/onekit-webapp/dispatches", data=json.dumps(payload).encode(), method="POST", headers={"Authorization": "Bearer " + os.environ["WEBAPP_DISPATCH_TOKEN"], "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "OneKit-release"})
with urllib.request.urlopen(request, timeout=30) as response:
    if response.status != 204:
        raise SystemExit("Webapp dispatch was not accepted.")
print("The private webapp update workflow has been triggered.")
