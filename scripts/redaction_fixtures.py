# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Adversarial source fixtures for redaction privacy regressions."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]
from test_redaction import private_image, private_pdf

destination = Path(sys.argv[1])
destination.mkdir(parents=True, exist_ok=True)
(destination / "redaction-private.pdf").write_bytes(private_pdf().data)
(destination / "redaction-private.png").write_bytes(private_image().data)
