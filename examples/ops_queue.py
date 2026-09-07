"""Module 06 - queue, circular queue, deque and priority queue operations."""
from __future__ import annotations

import heapq
import itertools
from typing import Any


def enqueue(queue: list[Any], value: Any) -> None:
    """Join at the back. O(1)."""
    queue.append(value)


def dequeue(queue: list[Any]) -> Any:
    """Served from the front. O(1) on a deque or linked list."""
    if not queue:
        raise IndexError("empty")
    return queue.pop(0)


def circular_enqueue(slots: list[Any], rear: int, count: int, value: Any) -> tuple[int, int]:
    """The modulo is the entire difference from a linear queue.

    Returns the new (rear, count).
    """
    capacity = len(slots)
    if count == capacity:
        raise OverflowError("full")
    rear = (rear + 1) % capacity          # <- the whole fix: wrap instead of run off
    slots[rear] = value
    return rear, count + 1


def circular_dequeue(slots: list[Any], front: int, count: int) -> tuple[Any, int, int]:
    """Returns (value, new front, new count)."""
    if count == 0:
        raise IndexError("empty")
    value = slots[front]
    slots[front] = None
    front = (front + 1) % len(slots)      # freed slots get reused
    return value, front, count - 1


def pq_insert(heap: list[tuple], value: Any, priority: Any, tie: itertools.count) -> None:
    """O(log n). The tie counter keeps arrival order for equal priorities and
    stops unorderable payloads from ever being compared."""
    heapq.heappush(heap, (priority, next(tie), value))


def pq_extract_min(heap: list[tuple]) -> Any:
    """The most urgent item, regardless of when it arrived. O(log n)."""
    if not heap:
        raise IndexError("empty")
    return heapq.heappop(heap)[2]
