"""Module 09 - heap operations on a flat list. No pointers anywhere."""
from __future__ import annotations

from typing import Any


def parent(i: int) -> int:
    return (i - 1) // 2                   # because the tree is COMPLETE,


def left(i: int) -> int:
    return 2 * i + 1                      # level-order position IS the index,


def right(i: int) -> int:
    return 2 * i + 2                      # so navigation is pure arithmetic


def sift_up(heap: list[Any], i: int) -> None:
    """Climb while you are smaller than your parent. At most log n swaps."""
    while i > 0 and heap[i] < heap[parent(i)]:
        heap[i], heap[parent(i)] = heap[parent(i)], heap[i]
        i = parent(i)


def sift_down(heap: list[Any], i: int) -> None:
    """Sink while a child is smaller than you."""
    n = len(heap)
    while True:
        smallest = i
        if left(i) < n and heap[left(i)] < heap[smallest]:
            smallest = left(i)
        if right(i) < n and heap[right(i)] < heap[smallest]:
            smallest = right(i)           # swap with the SMALLER child, or the
        if smallest == i:                 # other child ends up under a bigger key
            return
        heap[i], heap[smallest] = heap[smallest], heap[i]
        i = smallest


def insert(heap: list[Any], value: Any) -> None:
    """Place at the next free leaf - the only spot that keeps the tree
    complete - then climb. O(log n)."""
    heap.append(value)
    sift_up(heap, len(heap) - 1)


def extract_min(heap: list[Any]) -> Any:
    """The root is the answer. Patch the hole with the LAST leaf, then sink.

    Moving the last leaf up is the only removal that cannot leave a gap in
    the middle of a complete tree.
    """
    if not heap:
        raise IndexError("empty")
    smallest = heap[0]
    last = heap.pop()
    if heap:
        heap[0] = last
        sift_down(heap, 0)
    return smallest


def peek(heap: list[Any]) -> Any:
    """O(1), by the heap property."""
    if not heap:
        raise IndexError("empty")
    return heap[0]


def build_heap(values: list[Any]) -> list[Any]:
    """O(n), not O(n log n).

    sift_down costs the height BELOW a node, and the tree is bottom-heavy:
    half the nodes are leaves and cost nothing, a quarter cost 1, an eighth
    cost 2. The series converges to 2n.
    """
    heap = list(values)
    for i in range(len(heap) // 2 - 1, -1, -1):
        sift_down(heap, i)
    return heap


def heapsort(values: list[Any]) -> list[Any]:
    """O(n log n) time in O(1) extra space - but not stable."""
    heap = build_heap(values)
    return [extract_min(heap) for _ in range(len(heap))]
