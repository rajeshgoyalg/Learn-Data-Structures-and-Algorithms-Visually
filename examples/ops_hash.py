"""Module 07 - hash table operations with separate chaining."""
from __future__ import annotations

from typing import Any

LOAD_FACTOR_LIMIT = 0.75


def index_for(key: Any, capacity: int) -> int:
    """Compute the address instead of searching for it. O(1)."""
    return hash(key) % capacity           # change capacity and every key moves


def put(buckets: list[list[tuple]], key: Any, value: Any) -> bool:
    """Insert or update. Returns True if this was a new key."""
    chain = buckets[index_for(key, len(buckets))]
    for i, (k, _) in enumerate(chain):
        if k == key:
            chain[i] = (key, value)       # update, never duplicate
            return False
    chain.append((key, value))            # collisions just extend the chain
    return True


def get(buckets: list[list[tuple]], key: Any, default: Any = None) -> Any:
    """O(1) to find the bucket, then a walk of that chain only."""
    for k, v in buckets[index_for(key, len(buckets))]:
        if k == key:                      # compare the FULL key: a matching
            return v                      # bucket only means the hashes agreed
    return default


def delete(buckets: list[list[tuple]], key: Any) -> bool:
    chain = buckets[index_for(key, len(buckets))]
    for i, (k, _) in enumerate(chain):
        if k == key:
            chain.pop(i)
            return True
    return False


def resize(buckets: list[list[tuple]]) -> list[list[tuple]]:
    """Double the table and rehash everything. O(n).

    The index is `hash(key) % capacity`, so changing the capacity gives
    essentially every key a new home. That is why you double rather than
    grow by one.
    """
    entries = [pair for chain in buckets for pair in chain]
    bigger: list[list[tuple]] = [[] for _ in range(len(buckets) * 2)]
    for k, v in entries:
        bigger[index_for(k, len(bigger))].append((k, v))
    return bigger


def load_factor(buckets: list[list[tuple]]) -> float:
    """Above ~0.75 the chains lengthen and O(1) starts to decay."""
    return sum(len(c) for c in buckets) / len(buckets)
