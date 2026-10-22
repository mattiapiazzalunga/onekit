# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""OneKit's shared, offline processing API."""

__version__ = "0.5.0"

from .api import execute, pipeline
from .execution import ExecutionContext, ToolLimits
from .models import Artifact, OneKitError, Result

__all__ = ["Artifact", "OneKitError", "Result", "execute", "pipeline", "ExecutionContext", "ToolLimits"]
