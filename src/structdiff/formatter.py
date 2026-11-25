import json
from typing import Any

from structdiff.differ import DiffOp, OpType


def _format_path(path: tuple[Any, ...]) -> str:
    if not path:
        return "$"
    res = "$"
    for step in path:
        if isinstance(step, int):
            res += f"[{step}]"
        else:
            res += f".{step}"
    return res


def format_diff(ops: list[DiffOp], style: str = "text") -> str:
    if style == "json":
        return json.dumps([op.to_dict() for op in ops], indent=2)

    lines: list[str] = []
    for op in ops:
        p_str = _format_path(op.path)
        if op.op == OpType.ADD:
            lines.append(f"+ {p_str}: {op.new_value!r}")
        elif op.op == OpType.REMOVE:
            lines.append(f"- {p_str}: {op.old_value!r}")
        elif op.op == OpType.CHANGE:
            lines.append(f"~ {p_str}: {op.old_value!r} -> {op.new_value!r}")

    return "\n".join(lines)
