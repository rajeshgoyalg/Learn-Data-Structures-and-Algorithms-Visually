"""Module 14 - searching."""
from __future__ import annotations

from typing import Any


def linear_search(values: list[Any], target: Any) -> int:
    """Works on anything, sorted or not. O(n), n/2 comparisons on average."""
    for i, v in enumerate(values):
        if v == target:
            return i
    return -1                             # n comparisons if it is absent


def binary_search(values: list[Any], target: Any) -> int:
    """O(log n), but only on sorted, index-addressable data.

    Three classic bugs live in these seven lines - each marked below.
    """
    lo, hi = 0, len(values) - 1
    while lo <= hi:                       # BUG 1: `<` misses a one-element range
        mid = lo + (hi - lo) // 2         # BUG 2: (lo+hi)//2 overflows in
        if values[mid] == target:         #         fixed-width integer languages
            return mid
        if values[mid] < target:
            lo = mid + 1                  # BUG 3: without the +/-1 the range
        else:                             #         never shrinks and it loops
            hi = mid - 1                  #         forever
    return -1


def lower_bound(values: list[Any], target: Any) -> int:
    """First index whose value is not less than target.

    In other words: where the target is, or where it would go. This is what
    powers range queries and insertion into a sorted array.
    """
    lo, hi = 0, len(values)               # note: len, not len - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if values[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
