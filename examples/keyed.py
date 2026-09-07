"""Module 07-08: hash tables and sets."""
from __future__ import annotations

from typing import Any, Iterator, Optional

LOAD_FACTOR_LIMIT = 0.75


class HashTable:
    """Separate chaining, with a load factor that triggers a rehash.

    The index is `hash(key) % capacity`, which is why changing the capacity
    moves essentially every key and makes a resize O(n).
    """

    def __init__(self, capacity: int = 8) -> None:
        self._capacity = max(1, capacity)
        self._buckets: list[list[tuple[Any, Any]]] = [[] for _ in range(self._capacity)]
        self._count = 0
        self.rehashes = 0

    def _index(self, key: Any) -> int:
        return hash(key) % self._capacity

    def put(self, key: Any, value: Any) -> None:
        chain = self._buckets[self._index(key)]
        for i, (k, _) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)      # update, never duplicate
                return
        chain.append((key, value))
        self._count += 1
        if self._count / self._capacity > LOAD_FACTOR_LIMIT:
            self._resize()

    def get(self, key: Any, default: Any = None) -> Any:
        for k, v in self._buckets[self._index(key)]:
            if k == key:                     # compare the FULL key: a matching
                return v                     # bucket only means the hashes agreed
        return default

    def delete(self, key: Any) -> bool:
        chain = self._buckets[self._index(key)]
        for i, (k, _) in enumerate(chain):
            if k == key:
                chain.pop(i)
                self._count -= 1
                return True
        return False

    def __contains__(self, key: Any) -> bool:
        return any(k == key for k, _ in self._buckets[self._index(key)])

    def __len__(self) -> int:
        return self._count

    @property
    def load_factor(self) -> float:
        return self._count / self._capacity

    def _resize(self) -> None:
        entries = [pair for chain in self._buckets for pair in chain]
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._count = 0
        self.rehashes += 1
        for k, v in entries:
            self.put(k, v)                   # every key gets a new index

    def items(self) -> Iterator[tuple[Any, Any]]:
        for chain in self._buckets:
            yield from chain


def unique(values: list[Any]) -> list[Any]:
    """De-duplicate in O(n), preserving first-seen order.

    The nested-loop alternative is O(n^2): at n = 10,000 that is 10^8
    comparisons against 10^4.
    """
    seen: set[Any] = set()
    out: list[Any] = []
    for v in values:
        if v not in seen:                    # O(1) average
            seen.add(v)
            out.append(v)
    return out


def intersection(a: set[Any], b: set[Any]) -> set[Any]:
    """Iterate the SMALLER set and probe the larger one.

    Each probe is O(1), so the loop count is the entire cost:
    O(min(|a|, |b|)) rather than O(max(|a|, |b|)).
    """
    small, large = (a, b) if len(a) <= len(b) else (b, a)
    return {x for x in small if x in large}
