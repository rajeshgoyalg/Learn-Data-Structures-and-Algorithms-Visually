#!/usr/bin/env python3
"""Embed tested Python from examples/ into the module docs.

The snippets in docs/ are extracted from examples/ by this script, so they are
always the code the test suite actually covers. Run it after changing an
implementation; tools/verify.py fails if a doc block has drifted from its
source.

    python3 tools/sync_examples.py          # rewrite the blocks
    python3 tools/sync_examples.py --check  # report drift, change nothing
"""
from __future__ import annotations

import ast
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

ANCHOR = "## ⏱️ Complexity"
SUMMARY = "🐍 Python implementation"

# doc file -> (source file, symbols to embed, one-line framing)
MANIFEST: dict[str, tuple[str, list[str], str]] = {
    "docs/02-arrays.md": ("examples/linear.py", ["DynamicArray"],
        "A growable array over a fixed block, so the doubling is visible:"),
    "docs/03-linked-lists.md": ("examples/linear.py", ["Node", "SinglyLinkedList"],
        "Note the order of the two writes in `insert_after` — reverse them and the tail is leaked:"),
    "docs/04-doubly-and-circular-lists.md": ("examples/linear.py",
        ["DoublyLinkedList", "CircularLinkedList"],
        "`delete` here is O(1) given nothing but the node, which a singly linked list cannot do:"),
    "docs/05-stacks.md": ("examples/restricted.py", ["Stack", "is_balanced"],
        "The bracket checker is the canonical application — the stack *is* the nesting:"),
    "docs/06-queues.md": ("examples/restricted.py",
        ["CircularQueue", "Deque", "PriorityQueue"],
        "`(i + 1) % capacity` is the entire difference between a linear and a circular queue:"),
    "docs/07-hash-tables.md": ("examples/keyed.py", ["HashTable"],
        "Separate chaining with a load factor that triggers the rehash:"),
    "docs/08-sets.md": ("examples/keyed.py", ["unique", "intersection"],
        "The two things a set is actually used for:"),
    "docs/09-heaps.md": ("examples/hierarchical.py", ["MinHeap", "top_k"],
        "No pointers anywhere — the tree is complete, so position *is* index:"),
    "docs/10-binary-search-trees.md": ("examples/hierarchical.py", ["BST"],
        "All four traversals are one function with the visit line moved:"),
    "docs/11-balanced-trees.md": ("examples/hierarchical.py", ["AVLTree"],
        "Subclassing the plain BST, so the only difference is the rebalancing:"),
    "docs/12-tries.md": ("examples/hierarchical.py", ["Trie"],
        "`search` and `starts_with` are the same walk with one different final line:"),
    "docs/13-graphs.md": ("examples/graphs.py", ["Graph", "bfs", "dfs", "has_cycle"],
        "`bfs` and `dfs` differ only in queue versus stack:"),
    "docs/14-searching.md": ("examples/algorithms.py", ["binary_search", "lower_bound"],
        "Three classic bugs live in these few lines — the comments mark each one:"),
    "docs/15-sorting.md": ("examples/algorithms.py",
        ["merge_sort", "_merge", "quick_sort", "partition"],
        "The `<=` in `_merge` is what makes merge sort stable:"),
    "docs/16-recursion-and-backtracking.md": ("examples/algorithms.py",
        ["factorial", "solve_n_queens"],
        "The `placed.pop()` is the whole difference from brute force:"),
    "docs/17-paradigms.md": ("examples/algorithms.py",
        ["fib_memo", "fib_table", "coin_change_greedy", "coin_change_dp"],
        "Greedy and DP on the same problem, so you can see where greedy loses:"),
    "docs/18-dijkstra.md": ("examples/graphs.py", ["dijkstra", "path_to"],
        "`dist` gives you the cost; only `prev` gives you the route:"),
}


def extract(source: str, names: list[str]) -> str:
    """Pull top-level defs/classes out of a module, in manifest order."""
    text = open(source).read()
    tree = ast.parse(text)
    lines = text.splitlines()
    found: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name in names:
                start = min([node.lineno] + [d.lineno for d in node.decorator_list]) - 1
                found[node.name] = "\n".join(lines[start:node.end_lineno]).rstrip()
    missing = [n for n in names if n not in found]
    if missing:
        raise SystemExit(f"{source}: no top-level definition for {missing}")
    return "\n\n\n".join(found[n] for n in names)


def block(doc: str, source: str, names: list[str], framing: str) -> str:
    code = extract(source, names)
    return (f"<!-- python:{source}:{','.join(names)} -->\n"
            f"<details><summary><b>{SUMMARY}</b></summary>\n\n"
            f"{framing}\n\n"
            f"```python\n{code}\n```\n\n"
            f"Tested in [`examples/test_examples.py`](../{source.replace('.py', '')}"
            f"_test_link). Run the suite with `python3 -m unittest discover -s examples -t .`\n"
            f"</details>\n<!-- /python -->\n")


BLOCK_RE = re.compile(r"<!-- python:.*?<!-- /python -->\n", re.S)


def main() -> int:
    check = "--check" in sys.argv
    drifted = []
    for doc, (source, names, framing) in MANIFEST.items():
        text = open(doc).read()
        want = block(doc, source, names, framing)
        # normalise the tested-in line: it is generated, keep it simple
        want = want.replace(f"../{source.replace('.py', '')}_test_link",
                            "../examples/test_examples.py")
        if BLOCK_RE.search(text):
            new = BLOCK_RE.sub(lambda _: want, text, count=1)
        else:
            if ANCHOR not in text:
                raise SystemExit(f"{doc}: no '{ANCHOR}' heading to insert before")
            new = text.replace(ANCHOR, want + "\n---\n\n" + ANCHOR, 1)
        if new != text:
            drifted.append(doc)
            if not check:
                open(doc, "w").write(new)
    if check:
        if drifted:
            print("Python blocks are out of sync with examples/:")
            for d in drifted:
                print(f"  {d}")
            print("\nRun: python3 tools/sync_examples.py")
            return 1
        print("All Python blocks match examples/.")
        return 0
    print(f"Synced {len(MANIFEST)} modules ({len(drifted)} changed).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
