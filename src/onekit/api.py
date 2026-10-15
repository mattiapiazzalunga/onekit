# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import importlib

from .catalog import TOOLS
from .models import Artifact, OneKitError, Result

MAX_BYTES = 128 * 1024 * 1024


def execute(tool_id: str, files: list[Artifact], options: dict | None = None, *, browser=False) -> Result:
    tool = TOOLS.get(tool_id)
    if tool is None:
        raise OneKitError(f"Unknown tool: {tool_id}. Run 'onekit list'.")
    if browser and not tool.browser:
        raise OneKitError("This tool is in development for the browser. Use the CLI.")
    if not files:
        raise OneKitError("Choose at least one input file.")
    if len(files) > 256 or sum(len(file.data) for file in files) > MAX_BYTES:
        raise OneKitError("Input exceeds the limit of 256 files or 128 MiB.")
    if not tool.multiple and len(files) != 1:
        raise OneKitError("This tool accepts one input file.")
    if tool.accepts != ("*",) and any(file.kind not in tool.accepts for file in files):
        raise OneKitError(f"Expected file types: {', '.join(tool.accepts)}.")
    try:
        result = importlib.import_module(f"onekit.tools.{tool.handler}").run(tool, files, dict(options or {}))
    except OneKitError:
        raise
    except ImportError as exc:
        raise OneKitError(f"Missing optional dependency '{exc.name}'. Install the matching OneKit extra; see 'onekit doctor {tool_id}'.") from exc
    except Exception as exc:
        raise OneKitError(f"Cannot process this input: {str(exc)[:500]}") from exc
    if tool.fidelity == "compromise" and tool.note not in result.warnings:
        result.warnings.insert(0, tool.note)
    if not result.files:
        raise OneKitError("The engine produced no output.")
    return result


def pipeline(steps: list[dict], files: list[Artifact], *, browser=False) -> Result:
    if not isinstance(steps, list) or not steps or len(steps) > 16:
        raise OneKitError("A pipeline needs between 1 and 16 steps.")
    warnings, trace = [], []
    for step in steps:
        if not isinstance(step, dict) or not isinstance(step.get("options", {}), dict):
            raise OneKitError("Each step must be an object containing a tool and an options object.")
        tool_id = step.get("tool", "")
        tool = TOOLS.get(tool_id)
        if tool is None:
            raise OneKitError(f"Unknown tool: {tool_id}.")
        if len(files) > 1 and not tool.multiple:
            parts = [execute(tool_id, [file], step.get("options", {}), browser=browser) for file in files]
            result = Result([file for part in parts for file in part.files], [warning for part in parts for warning in part.warnings])
        else:
            result = execute(tool_id, files, step.get("options", {}), browser=browser)
        files = result.files
        warnings.extend(result.warnings)
        trace.append({"tool": tool_id, "outputs": [file.name for file in files]})
    return Result(files, list(dict.fromkeys(warnings)), {"steps": trace})
