# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from onekit import __version__
from onekit.catalog import manifest

tag = os.environ.get("RELEASE_TAG", "v" + __version__)
if not re.fullmatch(r"v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", tag) or tag[1:] != __version__:
    raise SystemExit("Release tag must be stable SemVer and match the package version.")
commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
dist = Path("dist")
assets = []
for file in sorted(dist.iterdir()):
    if file.suffix not in (".whl", ".gz"):
        continue
    assets.append({"name": file.name, "sha256": hashlib.sha256(file.read_bytes()).hexdigest(), "bytes": file.stat().st_size, "os": "any", "arch": "any", "python": ">=3.11", "url": f"https://github.com/mattiapiazzalunga/onekit/releases/download/{tag}/{file.name}"})
if len(assets) != 2:
    raise SystemExit("Expected exactly one universal wheel and one source distribution.")
(dist / "onekit-release.json").write_text(json.dumps({"schema": 1, "version": __version__, "tag": tag, "commit": commit, "repository": "mattiapiazzalunga/onekit", "assets": assets}, indent=2) + "\n", encoding="utf-8")
(dist / "catalog.json").write_text(json.dumps({"version": __version__, "tools": manifest()}, indent=2) + "\n", encoding="utf-8")
(dist / "SHA256SUMS").write_text("\n".join(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}" for f in sorted(dist.iterdir()) if f.name != "SHA256SUMS") + "\n", encoding="ascii")
