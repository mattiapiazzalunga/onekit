# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Fail closed on unreviewed runtime licenses; report exact versions and source URLs."""
import argparse
import hashlib
import json
import re
import sys
from importlib import metadata
from pathlib import Path

from packaging.requirements import Requirement

PERMISSIVE = {"MIT", "MIT-0", "MIT License", "MIT-CMU", "BSD", "BSD License", "BSD-2-Clause", "BSD-3-Clause", "Apache-2.0", "Apache Software License", "Python Software Foundation License", "PSF-2.0", "ISC", "ISC License (ISCL)", "Zlib", "Unlicense", "Public Domain", "CC0-1.0", "0BSD"}
# PDFium's distribution includes a complete third-party notice inventory. A new
# version requires a new explicit review rather than silently inheriting approval.
REVIEWED = {
    ("pypdfium2", "5.14.0"): "BSD-3-Clause, Apache-2.0, dependency licenses",
    # Unmodified Mozilla trust-store data. Keep upstream notices; review each update.
    ("certifi", "2026.10.19"): "MPL-2.0",
    ("pikepdf", "10.17.0"): "MPL-2.0",
    ("pdftopdfa", "0.9.24"): "MPL-2.0+",
    ("tqdm", "4.70.1"): "MPL-2.0 AND MIT",
}


def verified_file_license(distribution):
    if (distribution.metadata['Name'].lower().replace('_', '-'), distribution.version) != ('resvg-py', '0.5.0'):
        return None
    for file in distribution.files or []:
        if str(file).replace('\\', '/').endswith('.dist-info/licenses/LICENSE'):
            content = Path(distribution.locate_file(file)).read_bytes().replace(b'\r\n', b'\n')
            if hashlib.sha256(content).hexdigest() == '2f22fb1bcbf69e040d4c9c0b1f1aecbac22fd631d71fbc3a303637d896feb760':
                return 'MIT'
    return None


def check(*, include_signing=False, include_pdfa=False):
    records, seen, pending = {}, set(), [("onekit-tools", ("all", "signing") if include_signing else ("all",))]
    if include_pdfa:
        pending.extend((name, ()) for name in ("pdftopdfa", "pikepdf", "jsonschema", "referencing", "fonttools", "numpy", "tqdm", "click", "colorama", "lxml"))
    while pending:
        name, extras = pending.pop()
        key = (name.lower().replace("_", "-"), tuple(sorted(extras)))
        if key in seen:
            continue
        seen.add(key)
        distribution = metadata.distribution(name)
        info = distribution.metadata
        license = info.get("License-Expression") or info.get("License") or "UNKNOWN"
        if license == "UNKNOWN":
            license = verified_file_license(distribution) or license
        classifiers = [c.rsplit(" :: ", 1)[-1] for c in info.get_all("Classifier", []) if c.startswith("License ::")]
        candidates = [license, *classifiers]
        approved = any(candidate in PERMISSIVE or all(term.strip(" ()") in PERMISSIVE for term in re.split(r"\s+(?:OR|AND)\s+|;\s*", candidate)) for candidate in candidates)
        approved = approved or (key[0] == "onekit-tools" and license == "LicenseRef-PolyForm-Shield-1.0.0")
        approved = approved or REVIEWED.get((key[0], distribution.version)) == license
        records[key[0]] = {"name": info["Name"], "version": distribution.version, "license": license[:300], "approved": approved, "urls": info.get_all("Project-URL", [])}
        for dependency in distribution.requires or []:
            requirement = Requirement(dependency)
            # The fixed level-B API cannot invoke OCR or A/U layout tagging.
            # Their optional dependencies are not installed by OneKit setup.
            if include_pdfa and key[0] == "pdftopdfa" and requirement.name.lower() in ("paddleocr",):
                continue
            # Only CMap/encoding utilities are used; the PDF parser requiring
            # cryptography is not imported by the fixed level-B API.
            if include_pdfa and key[0] == "pdfminer.six" and requirement.name.lower() == "cryptography":
                continue
            if requirement.marker and not any(requirement.marker.evaluate({"extra": extra}) for extra in ("", *extras)):
                continue
            pending.append((requirement.name, tuple(requirement.extras)))
    report = sorted(records.values(), key=lambda item: item["name"].lower())
    Path("dependency-licenses.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    rejected = [item for item in report if not item["approved"]]
    for item in rejected:
        print(f"License review required: {item['name']} {item['version']}: {item['license']}", file=sys.stderr)
    if rejected:
        return 1
    print(f"Runtime license policy passed for {len(report)} distributions.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-signing", action="store_true", help="Also audit the separately installed signing extra (mandatory in CI).")
    parser.add_argument("--include-pdfa", action="store_true", help="Also audit the fixed non-OCR PDF/A backend installed by CLI setup.")
    args = parser.parse_args()
    sys.exit(check(include_signing=args.include_signing, include_pdfa=args.include_pdfa))
