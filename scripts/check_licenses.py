# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
"""Fail closed on unreviewed runtime licenses; report exact versions and source URLs."""
import importlib.metadata as metadata
import json
import re
import sys
from pathlib import Path

from packaging.requirements import Requirement

PERMISSIVE = {"MIT", "MIT License", "MIT-CMU", "BSD", "BSD License", "BSD-2-Clause", "BSD-3-Clause", "Apache-2.0", "Apache Software License", "Python Software Foundation License", "PSF-2.0", "ISC", "ISC License (ISCL)", "Zlib", "Unlicense", "Public Domain", "CC0-1.0", "0BSD"}
# PDFium's distribution includes a complete third-party notice inventory. A new
# version requires a new explicit review rather than silently inheriting approval.
REVIEWED = {("pypdfium2", "5.14.0"): "BSD-3-Clause, Apache-2.0, dependency licenses"}


def check():
    records, seen, pending = {}, set(), [("onekit-tools", ("all",))]
    while pending:
        name, extras = pending.pop()
        key = (name.lower().replace("_", "-"), tuple(sorted(extras)))
        if key in seen:
            continue
        seen.add(key)
        distribution = metadata.distribution(name)
        info = distribution.metadata
        license = info.get("License-Expression") or info.get("License") or "UNKNOWN"
        classifiers = [c.rsplit(" :: ", 1)[-1] for c in info.get_all("Classifier", []) if c.startswith("License ::")]
        candidates = [license, *classifiers]
        approved = any(candidate in PERMISSIVE or all(term.strip(" ()") in PERMISSIVE for term in re.split(r"\s+(?:OR|AND)\s+|;\s*", candidate)) for candidate in candidates)
        approved = approved or REVIEWED.get((key[0], distribution.version)) == license
        records[key[0]] = {"name": info["Name"], "version": distribution.version, "license": license[:300], "approved": approved, "urls": info.get_all("Project-URL", [])}
        for dependency in distribution.requires or []:
            requirement = Requirement(dependency)
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
    sys.exit(check())
