"""Module 10 - binary search tree operations."""
from __future__ import annotations

from typing import Any, Optional

from examples.nodes import TreeNode


def search(root: Optional[TreeNode], target: Any) -> bool:
    """Every comparison discards an entire subtree, unexamined."""
    node = root
    while node is not None:
        if target == node.value:
            return True
        node = node.left if target < node.value else node.right
    return False                          # you fell off the tree: not present


def insert(node: Optional[TreeNode], value: Any) -> TreeNode:
    """A failed search that plants a node where it ran out of tree."""
    if node is None:
        return TreeNode(value)            # this empty slot is its home
    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    return node                           # equal values are ignored


def minimum(node: TreeNode) -> Any:
    """The leftmost node. O(height)."""
    while node.left is not None:
        node = node.left
    return node.value


def maximum(node: TreeNode) -> Any:
    while node.right is not None:
        node = node.right
    return node.value


def delete(node: Optional[TreeNode], value: Any) -> Optional[TreeNode]:
    """Three cases, and only the third is interesting."""
    if node is None:
        return None
    if value < node.value:
        node.left = delete(node.left, value)
    elif value > node.value:
        node.right = delete(node.right, value)
    else:
        if node.left is None:
            return node.right             # no children, or a right child only
        if node.right is None:
            return node.left              # a left child only
        successor = node.right            # two children: the in-order successor
        while successor.left is not None:
            successor = successor.left    # is the smallest value larger than this
        node.value = successor.value      # one, so the invariant survives
        node.right = delete(node.right, successor.value)
    return node


def in_order(node: Optional[TreeNode]) -> list[Any]:
    """LEFT, node, RIGHT -> sorted output, for any valid BST."""
    if node is None:
        return []
    return in_order(node.left) + [node.value] + in_order(node.right)


def pre_order(node: Optional[TreeNode]) -> list[Any]:
    """node, LEFT, RIGHT -> serialise or copy a tree."""
    if node is None:
        return []
    return [node.value] + pre_order(node.left) + pre_order(node.right)


def post_order(node: Optional[TreeNode]) -> list[Any]:
    """LEFT, RIGHT, node -> free a tree, or evaluate an expression."""
    if node is None:
        return []
    return post_order(node.left) + post_order(node.right) + [node.value]


def level_order(root: Optional[TreeNode]) -> list[Any]:
    """Row by row. The only traversal that needs an explicit queue."""
    if root is None:
        return []
    out, queue = [], [root]
    while queue:
        node = queue.pop(0)
        out.append(node.value)
        queue.extend(n for n in (node.left, node.right) if n is not None)
    return out


def height(node: Optional[TreeNode]) -> int:
    """Every complexity in this module is really this number."""
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))
