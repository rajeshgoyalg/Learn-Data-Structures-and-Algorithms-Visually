"""Module 11 - AVL rotations. The only difference from a plain BST is here."""
from __future__ import annotations

from typing import Any, Optional

from examples.nodes import TreeNode
from examples.ops_bst import height


def node_height(node: Optional[TreeNode]) -> int:
    return 0 if node is None else node.height


def balance_factor(node: TreeNode) -> int:
    """height(left) - height(right). AVL keeps this in -1, 0 or +1."""
    return node_height(node.left) - node_height(node.right)


def update_height(node: TreeNode) -> None:
    node.height = 1 + max(node_height(node.left), node_height(node.right))


def rotate_right(y: TreeNode) -> TreeNode:
    """Three pointer writes, O(1), and the BST invariant cannot break:
    the subtree that changes parents was already between y and x in value."""
    x = y.left
    t = x.right                           # t is > x and < y, so it stays legal
    x.right = y
    y.left = t
    update_height(y)                      # order matters: y is now BELOW x
    update_height(x)
    return x                              # the caller must adopt the new root


def rotate_left(x: TreeNode) -> TreeNode:
    y = x.right
    t = y.left
    y.left = x
    x.right = t
    update_height(x)
    update_height(y)
    return y


def insert(node: Optional[TreeNode], value: Any) -> TreeNode:
    """Ordinary BST insert, then rebalance on the way back up."""
    if node is None:
        return TreeNode(value)
    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    else:
        return node

    update_height(node)
    balance = balance_factor(node)

    if balance > 1 and value < node.left.value:        # LL: one right rotation
        return rotate_right(node)
    if balance < -1 and value > node.right.value:      # RR: one left rotation
        return rotate_left(node)
    if balance > 1:                                    # LR: straighten, then rotate
        node.left = rotate_left(node.left)
        return rotate_right(node)
    if balance < -1:                                   # RL: the mirror image
        node.right = rotate_right(node.right)
        return rotate_left(node)
    return node                                        # already balanced
