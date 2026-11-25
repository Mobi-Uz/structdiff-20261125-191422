from dataclasses import dataclass
from enum import Enum
from typing import Any


class OpType(str, Enum):
    ADD = "add"
    REMOVE = "remove"
    CHANGE = "change"


@dataclass(frozen=True)
class DiffOp:
    op: OpType
    path: tuple[Any, ...]
    old_value: Any = None
    new_value: Any = None

    def to_dict(self) -> dict[str, Any]:
        res: dict[str, Any] = {
            "op": self.op.value,
            "path": list(self.path),
        }
        if self.op in (OpType.REMOVE, OpType.CHANGE):
            res["old_value"] = self.old_value
        if self.op in (OpType.ADD, OpType.CHANGE):
            res["new_value"] = self.new_value
        return res


def diff(a: Any, b: Any, path: tuple[Any, ...] = ()) -> list[DiffOp]:
    ops: list[DiffOp] = []

    if a == b and type(a) is type(b):
        return ops

    if type(a) is not type(b):
        ops.append(DiffOp(OpType.CHANGE, path, old_value=a, new_value=b))
        return ops

    if isinstance(a, dict):
        keys_a = set(a.keys())
        keys_b = set(b.keys())

        for k in sorted(keys_a - keys_b, key=str):
            ops.append(DiffOp(OpType.REMOVE, path + (k,), old_value=a[k]))
        for k in sorted(keys_b - keys_a, key=str):
            ops.append(DiffOp(OpType.ADD, path + (k,), new_value=b[k]))
        for k in sorted(keys_a & keys_b, key=str):
            ops.extend(diff(a[k], b[k], path + (k,)))

    elif isinstance(a, (list, tuple)):
        len_a, len_b = len(a), len(b)
        min_len = min(len_a, len_b)

        for i in range(min_len):
            ops.extend(diff(a[i], b[i], path + (i,)))

        if len_a > len_b:
            for i in range(len_b, len_a):
                ops.append(DiffOp(OpType.REMOVE, path + (i,), old_value=a[i]))
        elif len_b > len_a:
            for i in range(len_a, len_b):
                ops.append(DiffOp(OpType.ADD, path + (i,), new_value=b[i]))

    elif isinstance(a, set):
        removed = a - b
        added = b - a
        for item in sorted(removed, key=str):
            ops.append(DiffOp(OpType.REMOVE, path + (item,), old_value=item))
        for item in sorted(added, key=str):
            ops.append(DiffOp(OpType.ADD, path + (item,), new_value=item))

    else:
        ops.append(DiffOp(OpType.CHANGE, path, old_value=a, new_value=b))

    return ops
