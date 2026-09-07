"""Module 04 - doubly linked and circular list operations."""
from __future__ import annotations

from typing import Any, Optional

from examples.nodes import DNode, Node


def insert_after(node: DNode, value: Any) -> DNode:
    """Four writes instead of two: the successor must learn about it too."""
    fresh = DNode(value)
    fresh.next = node.next
    fresh.prev = node
    if node.next is not None:
        node.next.prev = fresh            # the extra write a singly list skips
    node.next = fresh
    return fresh


def delete(node: DNode) -> Any:
    """O(1) given nothing but the node itself.

    In a singly linked list this costs O(n), because finding the predecessor
    means walking from the head. This is why doubly linked lists exist.
    """
    if node.prev is not None:
        node.prev.next = node.next
    if node.next is not None:
        node.next.prev = node.prev
    node.prev = node.next = None
    return node.value


def walk_backward(tail: Optional[DNode]) -> list[Any]:
    """Impossible-or-expensive without `prev`."""
    out = []
    current = tail
    while current is not None:
        out.append(current.value)
        current = current.prev
    return out


def traverse_once(head: Optional[Node]) -> list[Any]:
    """A circular list has no null, so terminate on 'back where I started'.

    Writing `while current is not None` here never terminates - the classic
    bug when a linear list is made circular.
    """
    if head is None:
        return []
    out = []
    current = head
    while True:
        out.append(current.value)
        current = current.next
        if current is head:               # NOT `is None` - there is no null
            return out


def next_turn(current: Node) -> Node:
    """Round-robin: always valid, never null, wraps for free."""
    return current.next
