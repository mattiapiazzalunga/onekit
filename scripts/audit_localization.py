"""Fail when CLI catalogs drift or interpolation tokens change."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "src/onekit/locales"
subprocess.run([sys.executable, str(ROOT / "scripts/localization_inventory.py"), "--check"], check=True)
source = json.loads((DIRECTORY / "en.json").read_text(encoding="utf-8"))
report = {"sourceTexts": len(source), "complete": True, "coverage": {}}
for language in json.loads((DIRECTORY / "languages.json").read_text(encoding="utf-8")):
    catalog = json.loads((DIRECTORY / f"{language}.json").read_text(encoding="utf-8"))
    missing, obsolete = sorted(source.keys() - catalog.keys()), sorted(catalog.keys() - source.keys())
    invalid = [key for key, value in catalog.items() if not value.strip() or sorted(re.findall(r"\{\d+\}|%\([\w]+\)[a-z]|%[a-z]", key)) != sorted(re.findall(r"\{\d+\}|%\([\w]+\)[a-z]|%[a-z]", value)) or re.search(r"__(?:OKP|ONEKIT)\d+__|(?<!\d)975\d{3}(?!\d)", value)]
    report["coverage"][language] = {"translated": len(catalog), "missing": missing, "obsolete": obsolete, "invalid": invalid}
    report["complete"] &= not (missing or obsolete or invalid)
    print(f"{language}: {len(catalog)}/{len(source)}; missing {len(missing)}, obsolete {len(obsolete)}, invalid {len(invalid)}")
(ROOT / "docs/localization-status.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
raise SystemExit(0 if report["complete"] else 1)
