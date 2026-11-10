# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
from __future__ import annotations

import importlib
from contextlib import contextmanager

from .catalog import TOOLS
from .execution import DEFAULT_CONTEXT, ExecutionContext, use_context
from .models import Artifact, OneKitError, Result
from .validation import MAX_BYTES, check_batch, validate_inputs


def _prepare_execution(tool_id, files, options, context):
    if not isinstance(tool_id, str):
        raise OneKitError("The tool identifier must be a string.")
    if options is not None and not isinstance(options, dict):
        raise OneKitError("Tool options must be a JSON object.")
    context = context or DEFAULT_CONTEXT
    if not isinstance(context, ExecutionContext):
        raise OneKitError("Expected an ExecutionContext.")
    tool = TOOLS.get(tool_id)
    if tool is None:
        raise OneKitError(f"Unknown tool: {tool_id}. Run 'onekit list'.")
    tool = context.constrain(tool)
    validate_inputs(tool, files, options or {})
    settings = dict(options or {})
    settings["_max_expanded_bytes"] = min(MAX_BYTES, tool.max_total_bytes)
    return tool, settings, context


@contextmanager
def _processing_errors(tool_id):
    try:
        yield
    except OneKitError:
        raise
    except ImportError as exc:
        raise OneKitError(f"Missing optional dependency '{exc.name}'. Install the matching OneKit extra; see 'onekit doctor {tool_id}'.") from exc
    except Exception as exc:
        raise OneKitError(f"Cannot process this input: {str(exc)[:500]}") from exc


def execute(tool_id: str, files: list[Artifact], options: dict | None = None, *, context: ExecutionContext | None = None) -> Result:
    with _processing_errors(tool_id):
        tool, settings, context = _prepare_execution(tool_id, files, options, context)
        with use_context(context):
            result = importlib.import_module(f"onekit.tools.{tool.handler}").run(tool, files, settings)
        return _finish_execution(tool, result)


async def execute_async(tool_id: str, files: list[Artifact], options: dict | None = None, *, context: ExecutionContext | None = None) -> Result:
    """The same processing contract for hosts with an existing async event loop."""
    with _processing_errors(tool_id):
        tool, settings, context = _prepare_execution(tool_id, files, options, context)
        handler = importlib.import_module(f"onekit.tools.{tool.handler}")
        with use_context(context):
            result = await handler.run_async(tool, files, settings) if hasattr(handler, 'run_async') else handler.run(tool, files, settings)
        return _finish_execution(tool, result)


def _finish_execution(tool, result):
    check_batch(result.files, output=True, max_bytes=tool.max_total_bytes)
    if tool.fidelity == "compromise" and tool.note not in result.warnings:
        result.warnings.insert(0, tool.note)
    if not result.files:
        raise OneKitError("The engine produced no output.")
    return result


def validate_steps(steps):
    if not isinstance(steps, list) or not steps or len(steps) > 16:
        raise OneKitError("A pipeline needs between 1 and 16 steps.")
    for step in steps:
        if not isinstance(step, dict) or not isinstance(step.get("options", {}), dict):
            raise OneKitError("Each step must be an object containing a tool and an options object.")
        tool_id = step.get("tool", "")
        if not isinstance(tool_id, str) or tool_id not in TOOLS:
            raise OneKitError(f"Unknown tool: {tool_id}.")


def pipeline(steps: list[dict], files: list[Artifact], *, context: ExecutionContext | None = None) -> Result:
    context = context or DEFAULT_CONTEXT
    if not isinstance(context, ExecutionContext):
        raise OneKitError("Expected an ExecutionContext.")
    validate_steps(steps)
    check_batch(files, max_bytes=context.max_batch_bytes)
    warnings, trace = [], []
    for step in steps:
        tool_id = step["tool"]
        tool = context.constrain(TOOLS[tool_id])
        check_batch(files,
                    max_bytes=tool.max_total_bytes)
        if len(files) > 1 and not tool.multiple:
            result = Result([])
            for file in files:
                part = execute(tool_id, [file], step.get("options", {}), context=context)
                result.files.extend(part.files)
                result.warnings.extend(part.warnings)
                check_batch(result.files, output=True,
                            max_bytes=tool.max_total_bytes)
        else:
            result = execute(tool_id, files, step.get("options", {}), context=context)
        files = result.files
        warnings.extend(result.warnings)
        trace.append({"tool": tool_id, "outputs": [file.name for file in files]})
    return Result(files, list(dict.fromkeys(warnings)), {"steps": trace})


async def pipeline_async(steps: list[dict], files: list[Artifact], *, context: ExecutionContext | None = None) -> Result:
    """Sequential pipeline with the same budgets and contracts on async hosts."""
    context = context or DEFAULT_CONTEXT
    if not isinstance(context, ExecutionContext):
        raise OneKitError("Expected an ExecutionContext.")
    validate_steps(steps)
    check_batch(files, max_bytes=context.max_batch_bytes)
    warnings, trace = [], []
    for step in steps:
        tool_id = step['tool']
        tool = context.constrain(TOOLS[tool_id])
        check_batch(files, max_bytes=tool.max_total_bytes)
        if len(files) > 1 and not tool.multiple:
            result = Result([])
            for file in files:
                part = await execute_async(tool_id, [file], step.get('options', {}), context=context)
                result.files.extend(part.files)
                result.warnings.extend(part.warnings)
                check_batch(result.files, output=True, max_bytes=tool.max_total_bytes)
        else:
            result = await execute_async(tool_id, files, step.get('options', {}), context=context)
        files = result.files
        warnings.extend(result.warnings)
        trace.append({'tool': tool_id, 'outputs': [file.name for file in files]})
    return Result(files, list(dict.fromkeys(warnings)), {'steps': trace})
