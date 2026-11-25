import copy
from typing import Any

from structdiff.differ import DiffOp, OpType


def patch(target: Any, ops: list[DiffOp]) -> Any:
    result = copy.deepcopy(target)

    for op in ops:
        path = list(op.path)
        if not path:
            if op.op == OpType.CHANGE:
                result = copy.deepcopy(op.new_value)
            continue

        curr = result
        for step in path[:-1]:
            if isinstance(curr, dict):
                curr = curr[step]
            elif isinstance(curr, list):
                curr = curr[int(step)]

        last_key = path[-1]

        if op.op == OpType.ADD:
            if isinstance(curr, dict):
                curr[last_key] = copy.deepcopy(op.new_value)
            elif isinstance(curr, list):
                idx = int(last_key)
                if idx >= len(curr):
                    curr.append(copy.deepcopy(op.new_value))
                else:
                    curr.insert(idx, copy.deepcopy(op.new_value))
            elif isinstance(curr, set):
                curr.add(copy.deepcopy(op.new_value))

        elif op.op == OpType.REMOVE:
            if isinstance(curr, dict):
                curr.pop(last_key, None)
            elif isinstance(curr, list):
                idx = int(last_key)
                if 0 <= idx < len(curr):
                    curr.pop(idx)
            elif isinstance(curr, set):
                curr.discard(last_key)

        elif op.op == OpType.CHANGE:
            if isinstance(curr, dict):
                curr[last_key] = copy.deepcopy(op.new_value)
            elif isinstance(curr, list):
                idx = int(last_key)
                curr[idx] = copy.deepcopy(op.new_value)

    return result
