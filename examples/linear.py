"""Module 02-04: arrays, singly / doubly / circular linked lists."""
from __future__ import annotations

from typing import Any, Iterator, Optional


class DynamicArray:
    """A growable array over a fixed-capacity block, to make the doubling visible.

    Python's own `list` already does this; the point here is to show the
    mechanism that makes `append` amortised O(1).
    """

    def __init__(self, capacity: int = 4) -> None:
        self._capacity = max(1, capacity)
        self._length = 0
        self._store: list[Any] = [None] * self._capacity
        self.copies = 0                      # counts elements moved by growth

    def __len__(self) -> int:
        return self._length

    @property
    def capacity(self) -> int:
        return self._capacity

    def __getitem__(self, index: int) -> Any:
        if not 0 <= index < self._length:
            raise IndexError("out of bounds")
        return self._store[index]            # one address calculation: O(1)

    def __setitem__(self, index: int, value: Any) -> None:
        if not 0 <= index < self._length:
            raise IndexError("out of bounds")
        self._store[index] = value

    def append(self, value: Any) -> None:
        if self._length == self._capacity:
            self._grow()
        self._store[self._length] = value
        self._length += 1

    def insert_at(self, index: int, value: Any) -> None:
        """O(n): every element from `index` rightwards shifts up one slot."""
        if not 0 <= index <= self._length:
            raise IndexError("out of bounds")
        if self._length == self._capacity:
            self._grow()
        for j in range(self._length, index, -1):
            self._store[j] = self._store[j - 1]      # walk backwards, or you
        self._store[index] = value                   # smear one value along
        self._length += 1

    def delete_at(self, index: int) -> Any:
        """O(n): close the gap by shifting everything after `index` down one."""
        if not 0 <= index < self._length:
            raise IndexError("out of bounds")
        removed = self._store[index]
        for j in range(index, self._length - 1):
            self._store[j] = self._store[j + 1]
        self._length -= 1
        self._store[self._length] = None
        return removed

    def _grow(self) -> None:
        """Double the block and copy across. O(n) once, amortised O(1) per append."""
        self._capacity *= 2
        bigger: list[Any] = [None] * self._capacity
        for j in range(self._length):
            bigger[j] = self._store[j]
        self.copies += self._length
        self._store = bigger

    def __iter__(self) -> Iterator[Any]:
        return (self._store[i] for i in range(self._length))


class Node:
    """A singly linked list node: one payload, one pointer."""

    __slots__ = ("value", "next")

    def __init__(self, value: Any, next: Optional["Node"] = None) -> None:
        self.value = value
        self.next = next


class SinglyLinkedList:
    def __init__(self, values: Optional[list[Any]] = None) -> None:
        self.head: Optional[Node] = None
        for v in reversed(values or []):
            self.prepend(v)

    def prepend(self, value: Any) -> Node:
        """The cheapest insertion there is: two writes, always O(1)."""
        self.head = Node(value, self.head)
        return self.head

    @staticmethod
    def insert_after(node: Node, value: Any) -> Node:
        """O(1) once you hold `node`. Order matters: adopt the tail FIRST."""
        fresh = Node(value)
        fresh.next = node.next        # 1. the new node adopts the rest
        node.next = fresh             # 2. the predecessor adopts the new node
        return fresh

    @staticmethod
    def delete_after(node: Node) -> Optional[Any]:
        """Nothing is erased -- the node is routed around and becomes garbage."""
        victim = node.next
        if victim is None:
            return None
        node.next = victim.next
        return victim.value

    def get(self, k: int) -> Any:
        """O(n): there is no index arithmetic here, only k hops."""
        current = self.head
        for _ in range(k):
            if current is None:
                raise IndexError("out of range")
            current = current.next
        if current is None:
            raise IndexError("out of range")
        return current.value

    def reverse(self) -> None:
        """Three pointers: flipping a link destroys the only route onwards."""
        previous, current = None, self.head
        while current is not None:
            following = current.next     # save it before you overwrite it
            current.next = previous      # flip the arrow
            previous, current = current, following
        self.head = previous             # the old tail is the new head

    def has_cycle(self) -> bool:
        """Floyd's tortoise and hare: O(n) time, O(1) space."""
        slow = fast = self.head
        while fast is not None and fast.next is not None:
            slow = slow.next             # type: ignore[union-attr]
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    def to_list(self) -> list[Any]:
        out, seen = [], set()
        current = self.head
        while current is not None and id(current) not in seen:
            seen.add(id(current))
            out.append(current.value)
            current = current.next
        return out


class DNode:
    """A doubly linked node: the extra pointer buys O(1) delete by reference."""

    __slots__ = ("value", "prev", "next")

    def __init__(self, value: Any) -> None:
        self.value = value
        self.prev: Optional["DNode"] = None
        self.next: Optional["DNode"] = None


class DoublyLinkedList:
    def __init__(self, values: Optional[list[Any]] = None) -> None:
        self.head: Optional[DNode] = None
        self.tail: Optional[DNode] = None
        for v in values or []:
            self.append(v)

    def append(self, value: Any) -> DNode:
        node = DNode(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        return node

    def delete(self, node: DNode) -> Any:
        """O(1) given nothing but the node itself -- impossible when singly linked."""
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = node.next = None
        return node.value

    def forward(self) -> list[Any]:
        out, n = [], self.head
        while n is not None:
            out.append(n.value)
            n = n.next
        return out

    def backward(self) -> list[Any]:
        out, n = [], self.tail
        while n is not None:
            out.append(n.value)
            n = n.prev
        return out


class CircularLinkedList:
    """The tail points back at the head, so there is no null to stop on."""

    def __init__(self, values: Optional[list[Any]] = None) -> None:
        self.head: Optional[Node] = None
        for v in values or []:
            self.append(v)

    def append(self, value: Any) -> Node:
        node = Node(value)
        if self.head is None:
            self.head = node
            node.next = node
            return node
        tail = self.head
        while tail.next is not self.head:
            tail = tail.next            # type: ignore[assignment]
        tail.next = node
        node.next = self.head
        return node

    def traverse_once(self) -> list[Any]:
        """Terminate on 'back where I started', never on None."""
        if self.head is None:
            return []
        out, current = [], self.head
        while True:
            out.append(current.value)
            current = current.next      # type: ignore[assignment]
            if current is self.head:
                return out
