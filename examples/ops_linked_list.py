"""Module 03 - one small function per singly-linked-list operation."""
from __future__ import annotations

from typing import Any, Optional

from examples.nodes import Node


def traverse(head: Optional[Node]) -> list[Any]:
    """Following `next` is the only way to move. O(n)."""
    out = []
    current = head
    while current is not None:
        out.append(current.value)
        current = current.next            # the only way forward
    return out


def get(head: Optional[Node], k: int) -> Any:
    """Reach position k. There is no address arithmetic here - only k hops."""
    current = head
    for _ in range(k):
        if current is None:
            raise IndexError("out of range")
        current = current.next
    if current is None:
        raise IndexError("out of range")
    return current.value                  # k hops: O(n), never O(1)


def insert_after(node: Node, value: Any) -> Node:
    """Two writes, and nothing shifts. O(1) once you hold `node`."""
    fresh = Node(value)
    fresh.next = node.next                # 1. the new node adopts the rest
    node.next = fresh                     # 2. the predecessor adopts the new node
    return fresh                          # reverse these two and the tail is lost


def prepend(head: Optional[Node], value: Any) -> Node:
    """The cheapest insertion there is. Returns the new head."""
    return Node(value, head)


def delete_after(node: Node) -> Optional[Any]:
    """Nothing is erased - the node is routed around and becomes unreachable."""
    victim = node.next
    if victim is None:
        return None
    node.next = victim.next               # route around it
    return victim.value


def reverse(head: Optional[Node]) -> Optional[Node]:
    """Three pointers, because flipping a link destroys the way onwards."""
    previous, current = None, head
    while current is not None:
        following = current.next          # save it before you overwrite it
        current.next = previous           # flip the arrow
        previous, current = current, following
    return previous                       # the old tail is the new head


def has_cycle(head: Optional[Node]) -> bool:
    """Floyd's tortoise and hare. O(n) time, O(1) space."""
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next                  # one step
        fast = fast.next.next             # two steps
        if slow is fast:
            return True                   # they can only meet inside a loop
    return False
