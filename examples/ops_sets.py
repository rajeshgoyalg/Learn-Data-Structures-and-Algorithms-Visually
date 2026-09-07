"""Module 08 - set operations. A set is a hash table that kept only the keys."""
from __future__ import annotations

from typing import Any


def unique(values: list[Any]) -> list[Any]:
    """De-duplicate in O(n), preserving first-seen order.

    The nested-loop alternative is O(n^2): at n = 10,000 that is 10^8
    comparisons against 10^4.
    """
    seen: set[Any] = set()
    out: list[Any] = []
    for v in values:
        if v not in seen:                 # O(1) average
            seen.add(v)
            out.append(v)
    return out


def intersection(a: set[Any], b: set[Any]) -> set[Any]:
    """Iterate the SMALLER set and probe the larger one.

    Each probe is O(1), so the loop count is the entire cost: O(min(|a|,|b|))
    rather than O(max(|a|,|b|)). Getting this backwards on a 10-element set
    against a 10-million-element one is a millionfold waste.
    """
    small, large = (a, b) if len(a) <= len(b) else (b, a)
    return {x for x in small if x in large}


def union(a: set[Any], b: set[Any]) -> set[Any]:
    """Everything in either. O(|a| + |b|)."""
    out = set(a)
    for x in b:
        out.add(x)                        # adding something already there is a no-op
    return out


def difference(a: set[Any], b: set[Any]) -> set[Any]:
    """In a but not b. O(|a|)."""
    return {x for x in a if x not in b}


def seen_before(start: Any, neighbours_of) -> list[Any]:
    """The other everyday use: 'have I been here?' during a traversal.

    Without the set, a cyclic graph loops forever.
    """
    visited = {start}
    queue = [start]
    order = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for n in neighbours_of(node):
            if n not in visited:
                visited.add(n)
                queue.append(n)
    return order
