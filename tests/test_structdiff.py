import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from structdiff.differ import DiffOp, OpType, diff
from structdiff.formatter import format_diff
from structdiff.patcher import patch


class TestStructDiff(unittest.TestCase):

    def test_primitive_diff(self):
        ops = diff(10, 20)
        self.assertEqual(len(ops), 1)
        self.assertEqual(ops[0].op, OpType.CHANGE)
        self.assertEqual(ops[0].old_value, 10)
        self.assertEqual(ops[0].new_value, 20)

    def test_dict_diff_and_patch(self):
        dict1 = {"a": 1, "b": {"x": 10}, "c": [1, 2]}
        dict2 = {"a": 1, "b": {"x": 20}, "c": [1, 3], "d": True}

        ops = diff(dict1, dict2)
        self.assertEqual(len(ops), 3)

        patched = patch(dict1, ops)
        self.assertEqual(patched, dict2)

    def test_list_diff_length(self):
        a = [1, 2, 3]
        b = [1, 2]
        ops = diff(a, b)
        self.assertEqual(len(ops), 1)
        self.assertEqual(ops[0].op, OpType.REMOVE)
        self.assertEqual(ops[0].path, (2,))

        patched = patch(a, ops)
        self.assertEqual(patched, b)

    def test_set_diff(self):
        s1 = {"apple", "banana"}
        s2 = {"banana", "cherry"}
        ops = diff(s1, s2)
        self.assertEqual(len(ops), 2)

        patched = patch(s1, ops)
        self.assertEqual(patched, s2)

    def test_format_diff_text(self):
        a = {"x": 1}
        b = {"x": 2, "y": 3}
        ops = diff(a, b)
        fmt = format_diff(ops, style="text")
        self.assertIn("~ $.x: 1 -> 2", fmt)
        self.assertIn("+ $.y: 3", fmt)

    def test_format_diff_json(self):
        a = {"x": 1}
        b = {"x": 2}
        ops = diff(a, b)
        fmt_json = format_diff(ops, style="json")
        self.assertIn('"op": "change"', fmt_json)
        self.assertIn('"old_value": 1', fmt_json)
        self.assertIn('"new_value": 2', fmt_json)

    def test_identical_structures(self):
        a = {"nested": [1, 2, {"k": "v"}]}
        ops = diff(a, a)
        self.assertEqual(len(ops), 0)
        patched = patch(a, ops)
        self.assertEqual(patched, a)

    def test_type_mismatch(self):
        a = {"key": 123}
        b = {"key": "123"}
        ops = diff(a, b)
        self.assertEqual(len(ops), 1)
        self.assertEqual(ops[0].op, OpType.CHANGE)
        patched = patch(a, ops)
        self.assertEqual(patched, b)


if __name__ == "__main__":
    unittest.main()
