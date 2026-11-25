"""structdiff - Structural diffing, patching, and formatting for nested Python data structures."""

from structdiff.differ import DiffOp, OpType, diff
from structdiff.formatter import format_diff
from structdiff.patcher import patch

__all__ = ["diff", "patch", "format_diff", "DiffOp", "OpType"]
__version__ = "0.1.0"
