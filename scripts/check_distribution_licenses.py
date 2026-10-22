# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Validate the license and PyPI description in built release distributions."""
import argparse
import tarfile
import tomllib
import zipfile
from email.parser import BytesParser
from pathlib import Path


def check(directory):
    root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    expected = "LicenseRef-PolyForm-Shield-1.0.0"
    if project["license"] != expected:
        raise ValueError("Project license must be " + expected)
    wheels = list(directory.glob("*.whl"))
    sources = list(directory.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sources) != 1:
        raise ValueError("Expected exactly one wheel and one source distribution")

    def validate(files):
        for name in ("LICENSE", "NOTICE"):
            matches = [data for path, data in files.items() if path.endswith("/" + name)]
            if len(matches) != 1 or matches[0] != (root / name).read_bytes():
                raise ValueError("Missing or stale distribution " + name)
        metadata = [data for path, data in files.items() if path.endswith(("/METADATA", "/PKG-INFO"))]
        if not metadata:
            raise ValueError("Missing distribution metadata")
        for data in metadata:
            message = BytesParser().parsebytes(data)
            if message["License-Expression"] != expected:
                raise ValueError("Incorrect distribution License-Expression")
            if set(message.get_all("License-File", [])) != {"LICENSE", "NOTICE"}:
                raise ValueError("Incorrect distribution License-File metadata")
            if any(c.startswith("License ::") for c in message.get_all("Classifier", [])):
                raise ValueError("Use License-Expression rather than legacy license classifiers")
            if "Open Source (PolyForm Shield 1.0.0)" not in message.get_payload(decode=True).decode("utf-8"):
                raise ValueError("PyPI description is missing the current license explanation")

    with zipfile.ZipFile(wheels[0]) as wheel:
        validate({name: wheel.read(name) for name in wheel.namelist()})
    with tarfile.open(sources[0]) as source:
        validate({item.name: source.extractfile(item).read() for item in source if item.isfile()})
    print("Wheel and source distribution license metadata, notices and PyPI descriptions verified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=Path("dist"))
    check(parser.parse_args().directory)
