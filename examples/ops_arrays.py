"""Module 02 - one small function per array operation.

An array here is a plain fixed-size `store` list plus a `length`, because that
is what an array really is: a block of slots, only some of them in use. Keeping
the two separate is what makes `grow` and the shifting visible.
"""
from __future__ import annotations

from typing import Any


def get(store: list[Any], length: int, i: int) -> Any:
    """Read: the operation arrays exist for."""
    if not 0 <= i < length:
        raise IndexError("out of bounds")
    return store[i]                       # one address calculation, whatever i is


def insert_at(store: list[Any], length: int, i: int, value: Any) -> int:
    """Insert at an index. Returns the new length."""
    for j in range(length, i, -1):        # walk BACKWARDS: forwards would smear
        store[j] = store[j - 1]           # one value across the whole tail
    store[i] = value
    return length + 1                     # n - i elements moved: O(n)


def delete_at(store: list[Any], length: int, i: int) -> int:
    """Delete at an index - the mirror image. Returns the new length."""
    for j in range(i, length - 1):
        store[j] = store[j + 1]           # close the gap
    store[length - 1] = None              # the vacated slot holds nothing
    return length - 1


def grow(store: list[Any], length: int) -> list[Any]:
    """Grow: why appending is *amortised* O(1). Returns the new store."""
    bigger = [None] * (len(store) * 2)    # doubling is the important part
    for j in range(length):
        bigger[j] = store[j]              # every element is copied: O(n)
    return bigger                         # the old block is now garbage


def append(store: list[Any], length: int, value: Any) -> tuple[list[Any], int]:
    """Append, growing first if the block is full."""
    if length == len(store):
        store = grow(store, length)
    store[length] = value
    return store, length + 1
