#!/usr/bin/env python3
"""Refresh the Python snippets in docs/ from the tested code in examples/.

Each snippet is marked in the doc like this:

    <!-- py:ops_arrays:insert_at -->
    ```python
    ...
    ```
    <!-- /py -->

The marker names an `examples/<module>.py` and a top-level function or class.
This script rewrites the fence from that source, so a snippet in a module is
always the code the test suite covers. tools/verify.py fails on drift.

    python3 tools/sync_examples.py          # rewrite every marked fence
    python3 tools/sync_examples.py --check  # report drift, change nothing
"""
from __future__ import annotations

import ast
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

MARKER = re.compile(r"(<!-- py:([\w./]+):(\w+) -->\n)(.*?)(<!-- /py -->)", re.S)
_cache: dict[str, tuple[str, list[str]]] = {}


def source_of(module: str, symbol: str) -> str:
    """Return the source text of one top-level def/class in examples/<module>.py."""
    path = f"examples/{module}.py"
    if not os.path.exists(path):
        raise SystemExit(f"no such source: {path}")
    if path not in _cache:
        text = open(path).read()
        _cache[path] = (text, text.splitlines())
    text, lines = _cache[path]
    for node in ast.parse(text).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name == symbol:
                start = min([node.lineno] + [d.lineno for d in node.decorator_list]) - 1
                return "\n".join(lines[start:node.end_lineno]).rstrip()
    raise SystemExit(f"{path}: no top-level definition named '{symbol}'")


def main() -> int:
    check = "--check" in sys.argv
    drifted, total = [], 0
    for doc in sorted(glob.glob("docs/*.md")):
        text = open(doc).read()

        def repl(m: re.Match) -> str:
            nonlocal total
            total += 1
            code = source_of(m.group(2), m.group(3))
            return f"{m.group(1)}```python\n{code}\n```\n{m.group(5)}"

        new = MARKER.sub(repl, text)
        if new != text:
            drifted.append(doc)
            if not check:
                open(doc, "w").write(new)

    if check:
        if drifted:
            print("Python snippets are out of sync with examples/:")
            for d in sorted(set(drifted)):
                print(f"  {d}")
            print("\nRun: python3 tools/sync_examples.py")
            return 1
        print(f"All {total} Python snippets match examples/.")
        return 0
    print(f"Synced {total} snippets across {len(glob.glob('docs/*.md'))} docs "
          f"({len(set(drifted))} file(s) changed).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
