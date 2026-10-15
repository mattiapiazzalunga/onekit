# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
import hashlib
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

tag = os.environ["RELEASE_TAG"]
repo = "mattiapiazzalunga/onekit"
check = subprocess.run(["gh", "release", "view", tag, "--repo", repo, "--json", "isDraft,assets"], capture_output=True, text=True)
files = sorted(Path("dist").iterdir())
if check.returncode == 0:
    release = json.loads(check.stdout)
    if not release["isDraft"]:
        # Published assets are never overwritten, even on a retry.
        remote = json.load(urllib.request.urlopen(f"https://github.com/{repo}/releases/download/{tag}/onekit-release.json", timeout=30))
        local = json.loads(Path("dist/onekit-release.json").read_text())
        if remote != local:
            raise SystemExit("Published release differs from these artifacts. Refusing to overwrite.")
        print("This matching release is already public.")
        raise SystemExit(0)
else:
    subprocess.run(["gh", "release", "create", tag, "--repo", repo, "--verify-tag", "--draft", "--generate-notes", "--title", f"OneKit {tag}"], check=True)
subprocess.run(["gh", "release", "upload", tag, "--repo", repo, "--clobber", *map(str, files)], check=True)
subprocess.run(["gh", "release", "edit", tag, "--repo", repo, "--draft=false", "--latest"], check=True)
