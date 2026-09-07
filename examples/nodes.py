"""Minimal node types shared by the per-operation functions."""
from __future__ import annotations

from typing import Any, Optional


class Node:
    """A singly linked list node: one payload, one pointer."""
    __slots__ = ("value", "next")

    def __init__(self, value: Any, next: Optional["Node"] = None) -> None:
        self.value = value
        self.next = next


class DNode:
    """A doubly linked node. The extra pointer buys O(1) delete by reference."""
    __slots__ = ("value", "prev", "next")

    def __init__(self, value: Any) -> None:
        self.value = value
        self.prev: Optional["DNode"] = None
        self.next: Optional["DNode"] = None


class TreeNode:
    """A binary tree node. `height` is only used by the AVL functions."""
    __slots__ = ("value", "left", "right", "height")

    def __init__(self, value: Any) -> None:
        self.value = value
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None
        self.height = 1


class TrieNode:
    """A trie node stores no letter of its own - the path to it is the prefix."""
    __slots__ = ("children", "is_end")

    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.is_end = False
