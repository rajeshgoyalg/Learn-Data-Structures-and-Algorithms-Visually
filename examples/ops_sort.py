"""Module 15 - the five classic sorts, one function each."""
from __future__ import annotations

from typing import Any


def bubble_sort(values: list[Any]) -> list[Any]:
    """O(n^2), stable, in place. The flag is what makes the best case O(n)."""
    a = list(values)
    for end in range(len(a) - 1, 0, -1):
        swapped = False
        for i in range(end):              # the tail is already sorted
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        if not swapped:
            return a                      # already sorted: O(n)
    return a


def selection_sort(values: list[Any]) -> list[Any]:
    """Always O(n^2) comparisons, but only O(n) writes.

    That matters when a write costs far more than a read.
    """
    a = list(values)
    for i in range(len(a) - 1):
        smallest = i
        for j in range(i + 1, len(a)):
            if a[j] < a[smallest]:
                smallest = j
        a[i], a[smallest] = a[smallest], a[i]     # exactly one swap per pass
    return a


def insertion_sort(values: list[Any]) -> list[Any]:
    """O(n) on nearly-sorted input, stable, in place.

    Which is why real library sorts fall back to it for short runs.
    """
    a = list(values)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]               # slide right to make room
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(values: list[Any]) -> list[Any]:
    """O(n log n) guaranteed in every case, and stable - at O(n) extra space."""
    if len(values) <= 1:
        return list(values)               # a single element is sorted
    mid = len(values) // 2
    return merge(merge_sort(values[:mid]), merge_sort(values[mid:]))


def merge(left: list[Any], right: list[Any]) -> list[Any]:
    """Always take the smaller front element."""
    out: list[Any] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:           # <=, not <: THIS is what makes
            out.append(left[i])           # merge sort stable
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def partition(a: list[Any], lo: int, hi: int) -> int:
    """Lomuto. Everything <= the pivot is swapped to the front as it is met.

    A last-element pivot on sorted input is the O(n^2) worst case, which is
    why real implementations randomise the choice.
    """
    pivot = a[hi]
    i = lo - 1                            # boundary of the "smaller" region
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]     # drop the pivot into the boundary
    return i + 1                          # and it never moves again


def quick_sort(values: list[Any]) -> list[Any]:
    """O(n log n) average, in place, but O(n^2) on a bad pivot."""
    a = list(values)

    def recurse(lo: int, hi: int) -> None:
        if lo >= hi:
            return
        p = partition(a, lo, hi)
        recurse(lo, p - 1)                # the pivot itself is already final
        recurse(p + 1, hi)

    recurse(0, len(a) - 1)
    return a
