"""Module 05-06: stacks, queues, circular queues, deques, priority queues."""
from __future__ import annotations

import heapq
import itertools
from typing import Any, Optional

PAIRS = {")": "(", "]": "[", "}": "{"}


class Stack:
    """LIFO. Only one end is reachable, and that restriction is the point."""

    def __init__(self) -> None:
        self._items: list[Any] = []

    def push(self, value: Any) -> None:
        self._items.append(value)

    def pop(self) -> Any:
        if not self._items:
            raise IndexError("underflow: pop from an empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        if not self._items:
            raise IndexError("empty")
        return self._items[-1]

    def is_empty(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)


def is_balanced(text: str) -> bool:
    """Every opener is a note saying 'remember to close this'.

    The stack guarantees they close in the reverse of the order they opened,
    which is exactly what nesting means.
    """
    stack: list[str] = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack.pop() != PAIRS[ch]:
                return False
    return not stack


class Queue:
    """FIFO, backed by a linked list so both ends stay O(1)."""

    def __init__(self) -> None:
        self._front: Optional[list[Any]] = None
        self._items: list[Any] = []
        self._head = 0

    def enqueue(self, value: Any) -> None:
        self._items.append(value)

    def dequeue(self) -> Any:
        if self._head == len(self._items):
            raise IndexError("empty")
        value = self._items[self._head]
        self._items[self._head] = None       # let the object be collected
        self._head += 1
        if self._head > 32 and self._head * 2 >= len(self._items):
            self._items = self._items[self._head:]   # amortised compaction
            self._head = 0
        return value

    def peek(self) -> Any:
        if self._head == len(self._items):
            raise IndexError("empty")
        return self._items[self._head]

    def __len__(self) -> int:
        return len(self._items) - self._head


class CircularQueue:
    """Fixed capacity. `(i + 1) % capacity` is the whole difference from linear."""

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._slots: list[Any] = [None] * capacity
        self._front = 0
        self._rear = -1
        self._count = 0                      # front == rear is ambiguous without this

    def enqueue(self, value: Any) -> None:
        if self._count == self.capacity:
            raise OverflowError("full")
        self._rear = (self._rear + 1) % self.capacity
        self._slots[self._rear] = value
        self._count += 1

    def dequeue(self) -> Any:
        if self._count == 0:
            raise IndexError("empty")
        value = self._slots[self._front]
        self._slots[self._front] = None
        self._front = (self._front + 1) % self.capacity
        self._count -= 1
        return value

    def __len__(self) -> int:
        return self._count

    @property
    def is_full(self) -> bool:
        return self._count == self.capacity


class Deque:
    """A stack and a queue at once: all four operations are O(1)."""

    def __init__(self) -> None:
        self._items: list[Any] = []

    def push_front(self, value: Any) -> None:
        self._items.insert(0, value)

    def push_back(self, value: Any) -> None:
        self._items.append(value)

    def pop_front(self) -> Any:
        if not self._items:
            raise IndexError("empty")
        return self._items.pop(0)

    def pop_back(self) -> Any:
        if not self._items:
            raise IndexError("empty")
        return self._items.pop()

    def __len__(self) -> int:
        return len(self._items)


class PriorityQueue:
    """Order of service is decided by a key, not by arrival.

    The counter breaks ties by arrival order and keeps unorderable payloads
    from ever being compared.
    """

    def __init__(self) -> None:
        self._heap: list[tuple[Any, int, Any]] = []
        self._tie = itertools.count()

    def insert(self, value: Any, priority: Any) -> None:
        heapq.heappush(self._heap, (priority, next(self._tie), value))   # O(log n)

    def extract_min(self) -> Any:
        if not self._heap:
            raise IndexError("empty")
        return heapq.heappop(self._heap)[2]                              # O(log n)

    def peek(self) -> Any:
        if not self._heap:
            raise IndexError("empty")
        return self._heap[0][2]                                          # O(1)

    def __len__(self) -> int:
        return len(self._heap)
