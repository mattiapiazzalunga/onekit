# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from onekit import __version__

tag = os.environ["RELEASE_TAG"]
if not re.fullmatch(r"v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", tag) or tag[1:] != __version__:
    raise SystemExit("The stable SemVer tag must match __version__.")
subprocess.run(["git", "fetch", "origin", "main", "--no-tags"], check=True)
subprocess.run(["git", "merge-base", "--is-ancestor", "HEAD", "FETCH_HEAD"], check=True)
print(f"Verified {tag} is part of main and matches the source version.")
