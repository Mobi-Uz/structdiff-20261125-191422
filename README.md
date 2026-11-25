# structdiff

`structdiff` is a zero-dependency Python 3.12 library for computing, inspecting, and applying structural diffs between nested Python data structures (dicts, lists, sets, tuples, and primitives).

## Features

- **Recursive Diffing**: Compute fine-grained change operations between arbitrary nested structures.
- **Data Patching**: Apply calculated diff operations to target structures to transform them.
- **Flexible Output Formatting**: Human-readable text format or machine-parseable JSON representations.
- **Zero External Dependencies**: Pure Python 3.12 standard library implementation.

## Quickstart

```python
from structdiff import diff, patch, format_diff

a = {"user": {"name": "Alice", "role": "admin"}, "tags": ["python", "dev"]}
b = {"user": {"name": "Alice", "role": "lead"}, "tags": ["python", "ops"], "active": True}

# Compute diff operations
ops = diff(a, b)

# Print human-readable diff
print(format_diff(ops))
# Output:
# ~ $.user.role: 'admin' -> 'lead'
# ~ $.tags[1]: 'dev' -> 'ops'
# + $.active: True

# Apply diff to recreate target structure
result = patch(a, ops)
assert result == b
```

## Running Tests

Run unittest discovery from the root directory:

```bash
python -m unittest discover -v
```
