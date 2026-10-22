# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Versioned CLI and Python processing contracts, independent of deployment."""
from dataclasses import asdict

from .catalog import TOOLS

API_VERSION = 1
_FIELDS = ("id", "accepts", "produces", "multiple", "options", "input_mode",
           "min_files", "max_files", "max_file_bytes", "max_total_bytes")


def contract_manifest():
    return {
        "format": "onekit-processing-contract",
        "version": 1,
        "apiVersion": API_VERSION,
        "artifact": {"fields": ["name", "data"], "name": "portable-relative-path", "data": "bytes"},
        "result": {"fields": ["files", "warnings", "details"]},
        "pipeline": {"minSteps": 1, "maxSteps": 16, "fields": ["tool", "options"]},
        "workflow": {"format": "onekit-workflow", "version": 1, "fields": ["format", "version", "steps"]},
        "tools": [{key: asdict(tool)[key] for key in _FIELDS} for tool in TOOLS.values()],
    }


def compatibility_errors(previous, current):
    """Return breaking changes; additional tools, options and formats are allowed."""
    errors = []
    for key in ("format", "version", "apiVersion", "artifact", "result", "pipeline", "workflow"):
        if previous.get(key) != current.get(key):
            errors.append(f"Processing interface changed: {key}")
    available = {tool["id"]: tool for tool in current["tools"]}
    for old in previous["tools"]:
        identifier = old["id"]
        new = available.get(identifier)
        if new is None:
            errors.append(f"Removed tool: {identifier}")
            continue
        for key in ("produces", "multiple", "input_mode"):
            if old[key] != new[key]:
                errors.append(f"{identifier}: changed {key}")
        if "*" not in new["accepts"] and ("*" in old["accepts"] or not set(old["accepts"]) <= set(new["accepts"])):
            errors.append(f"{identifier}: narrowed accepted formats")
        if not set(old["options"]) <= set(new["options"]):
            errors.append(f"{identifier}: removed options")
        if new["min_files"] > old["min_files"]:
            errors.append(f"{identifier}: raised minimum file count")
        for key in ("max_files", "max_file_bytes", "max_total_bytes"):
            if new[key] < old[key]:
                errors.append(f"{identifier}: lowered {key}")
    return errors
