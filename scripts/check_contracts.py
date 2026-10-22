# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Check backward compatibility of the versioned public processing interface."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from onekit.contracts import compatibility_errors, contract_manifest

if __name__ == "__main__":
    previous = json.loads((ROOT / "contracts/processing-v1.json").read_text(encoding="utf-8"))
    # JSON normalizes tuple-valued catalog fields to their wire representation.
    current = json.loads(json.dumps(contract_manifest()))
    errors = compatibility_errors(previous, current)
    if errors:
        raise SystemExit("Breaking processing contract changes:\n" + "\n".join(errors))
    print(f"Processing API v{current['apiVersion']}: {len(current['tools'])} compatible tool contracts.")
