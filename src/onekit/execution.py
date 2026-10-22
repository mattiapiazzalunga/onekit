# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Resource budgets and trusted engine services for processing callers."""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Callable, Mapping

from .models import Artifact, OneKitError

MAX_BYTES = 128 * 1024 * 1024


def _budget(value):
    if type(value) is not int or not 0 < value <= MAX_BYTES:
        raise OneKitError(f"Processing budgets must be integers between 1 and {MAX_BYTES} bytes.")


@dataclass(frozen=True)
class ToolLimits:
    max_file_bytes: int = MAX_BYTES
    max_total_bytes: int = MAX_BYTES

    def __post_init__(self):
        _budget(self.max_file_bytes)
        _budget(self.max_total_bytes)
        if self.max_file_bytes > self.max_total_bytes:
            raise OneKitError("A per-file budget cannot exceed the total budget.")


@dataclass(frozen=True)
class ExecutionContext:
    """A caller may narrow limits and supply a trusted local metadata reader.

    Services are separate from untrusted tool options. Limits cannot raise the
    catalog's resource ceilings. Contexts are immutable and scoped to each call.
    """

    max_batch_bytes: int = MAX_BYTES
    tool_limits: Mapping[str, ToolLimits] = field(default_factory=dict)
    media_probe: Callable[[Artifact], dict] | None = None

    def __post_init__(self):
        _budget(self.max_batch_bytes)
        if any(not isinstance(key, str) or not isinstance(value, ToolLimits)
               for key, value in self.tool_limits.items()):
            raise OneKitError("Tool budgets must map tool identifiers to ToolLimits.")
        if self.media_probe is not None and not callable(self.media_probe):
            raise OneKitError("The media metadata reader must be callable.")
        object.__setattr__(self, "tool_limits", MappingProxyType(dict(self.tool_limits)))

    def constrain(self, tool):
        limits = self.tool_limits.get(tool.id, ToolLimits())
        total = min(tool.max_total_bytes, self.max_batch_bytes, limits.max_total_bytes)
        return replace(tool, max_total_bytes=total,
                       max_file_bytes=min(tool.max_file_bytes, total, limits.max_file_bytes))


DEFAULT_CONTEXT = ExecutionContext()
_context = ContextVar("onekit_execution_context", default=DEFAULT_CONTEXT)


def current_context():
    return _context.get()


@contextmanager
def use_context(context):
    token = _context.set(context)
    try:
        yield
    finally:
        _context.reset(token)
