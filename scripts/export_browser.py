# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
"""Export runtime source, not a downloadable release distribution."""
import argparse
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from onekit import __version__
from onekit.catalog import manifest


def export(destination):
    destination.mkdir(parents=True, exist_ok=True)
    files = sorted((ROOT / "src" / "onekit").rglob("*.py"))
    stream = io.BytesIO()
    digest = hashlib.sha256()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file in files:
            relative = file.relative_to(ROOT / "src").as_posix()
            data = file.read_bytes()
            digest.update(relative.encode() + b"\x00" + data)
            info = zipfile.ZipInfo(relative, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    (destination / "runtime.zip").write_bytes(stream.getvalue())
    record = {"version": __version__, "sourceSha256": digest.hexdigest(), "runtimeSha256": hashlib.sha256(stream.getvalue()).hexdigest(), "tools": manifest()}
    (destination / "catalog.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    dependencies = json.loads((ROOT / "browser-dependencies.json").read_text())
    for line in (ROOT / "browser" / "requirements.txt").read_text().splitlines():
        if "==" in line and not line.startswith("#"):
            name, version = line.strip().split("==", 1)
            dependencies["packages"][name] = version
    (destination / "dependencies.json").write_text(json.dumps(dependencies, indent=2) + "\n", encoding="utf-8")
    (destination / "loader.mjs").write_bytes((ROOT / "browser-loader.mjs").read_bytes())
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    export(parser.parse_args().destination)
