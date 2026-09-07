"""Module 14-17: searching, sorting, recursion, backtracking, paradigms."""
from __future__ import annotations

from typing import Any, Optional

# ----------------------------------------------------------------- searching
def linear_search(values: list[Any], target: Any) -> int:
    """Works on anything, sorted or not. O(n), n/2 comparisons on average."""
    for i, v in enumerate(values):
        if v == target:
            return i
    return -1


def binary_search(values: list[Any], target: Any) -> int:
    """O(log n), but only on sorted, index-addressable data.

    Three bugs live in these few lines; see the comments.
    """
    lo, hi = 0, len(values) - 1
    while lo <= hi:                          # <=, not <: a one-element range
        mid = lo + (hi - lo) // 2            # NOT (lo+hi)//2 -- that overflows
        if values[mid] == target:            # in fixed-width integer languages
            return mid
        if values[mid] < target:
            lo = mid + 1                     # the +/-1 is what shrinks the range;
        else:                                # without it this loops forever
            hi = mid - 1
    return -1


def lower_bound(values: list[Any], target: Any) -> int:
    """First index whose value is not less than target -- i.e. where it would go.

    This is what powers range queries and insertion into a sorted array.
    """
    lo, hi = 0, len(values)                  # note: len, not len - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if values[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


# ------------------------------------------------------------------- sorting
def bubble_sort(values: list[Any]) -> list[Any]:
    """O(n^2), stable, in place. The flag is what makes the best case O(n)."""
    a = list(values)
    for end in range(len(a) - 1, 0, -1):
        swapped = False
        for i in range(end):                 # the tail is already sorted
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        if not swapped:
            return a                         # already sorted
    return a


def selection_sort(values: list[Any]) -> list[Any]:
    """Always O(n^2) comparisons but only O(n) writes.

    That matters when a write costs far more than a read.
    """
    a = list(values)
    for i in range(len(a) - 1):
        smallest = i
        for j in range(i + 1, len(a)):
            if a[j] < a[smallest]:
                smallest = j
        a[i], a[smallest] = a[smallest], a[i]    # exactly one swap per pass
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
            a[j + 1] = a[j]                  # slide right to make room
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(values: list[Any]) -> list[Any]:
    """O(n log n) guaranteed in every case, and stable -- at O(n) extra space."""
    if len(values) <= 1:
        return list(values)                  # a single element is sorted
    mid = len(values) // 2
    return _merge(merge_sort(values[:mid]), merge_sort(values[mid:]))


def _merge(left: list[Any], right: list[Any]) -> list[Any]:
    out: list[Any] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:              # <=, not <: this is what makes
            out.append(left[i])              # merge sort STABLE
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def quick_sort(values: list[Any]) -> list[Any]:
    a = list(values)
    _quick(a, 0, len(a) - 1)
    return a


def _quick(a: list[Any], lo: int, hi: int) -> None:
    if lo >= hi:
        return
    p = partition(a, lo, hi)
    _quick(a, lo, p - 1)                     # the pivot itself is already final
    _quick(a, p + 1, hi)


def partition(a: list[Any], lo: int, hi: int) -> int:
    """Lomuto. Everything <= the pivot is swapped to the front as it is met.

    A last-element pivot on sorted input is the O(n^2) worst case, which is
    why real implementations randomise the choice.
    """
    pivot = a[hi]
    i = lo - 1                               # boundary of the "smaller" region
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]        # drop the pivot into the boundary
    return i + 1


# --------------------------------------------------------------- recursion
def factorial(n: int) -> int:
    """Base case, recursive case, and progress -- all three are required."""
    if n <= 1:
        return 1                             # base case: returns without recursing
    return n * factorial(n - 1)              # n-1 is the progress


def solve_n_queens(n: int = 4) -> list[list[int]]:
    """Backtracking: choose, recurse, and UNDO when the branch cannot work.

    The undo is the whole difference from brute force -- it abandons every
    completion of an illegal prefix without ever generating them.
    """
    solutions: list[list[int]] = []
    placed: list[int] = []                   # placed[row] = column

    def safe(row: int, col: int) -> bool:
        return all(c != col and abs(r - row) != abs(c - col)
                   for r, c in enumerate(placed))

    def place(row: int) -> None:
        if row == n:
            solutions.append(placed.copy())
            return
        for col in range(n):
            if safe(row, col):
                placed.append(col)           # choose
                place(row + 1)               # explore
                placed.pop()                 # UNCHOOSE -- this is backtracking

    place(0)
    return solutions


# --------------------------------------------------------------- paradigms
def fib_naive(n: int) -> int:
    """O(2^n): the same subproblems, recomputed independently, forever."""
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


def fib_memo(n: int, memo: Optional[dict[int, int]] = None) -> int:
    """Top-down DP. Two added lines take this from O(2^n) to O(n)."""
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n in memo:
        return memo[n]                       # the entire technique
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


def fib_table(n: int) -> int:
    """Bottom-up DP: fill in dependency order, no recursion, no stack risk."""
    if n <= 1:
        return n                             # n = 0 has no table[1] to seed
    table = [0] * (n + 1)
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]
    return table[n]


def fib_two_vars(n: int) -> int:
    """Only the last two entries are ever read, so the table collapses."""
    if n <= 1:
        return n                             # without this, fib(0) returns 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def coin_change_greedy(target: int, coins: tuple[int, ...] = (25, 10, 5, 1)) -> list[int]:
    """Take the largest coin that fits and never reconsider.

    Provably optimal for 1/5/10/25. With 1/3/4 it makes 6 as 4+1+1 when 3+3
    is better -- greedy correctness is a property of the problem, not the code.
    """
    out: list[int] = []
    remaining = target
    for coin in sorted(coins, reverse=True):
        while remaining >= coin:
            out.append(coin)
            remaining -= coin
    return out


def coin_change_dp(target: int, coins: tuple[int, ...] = (1, 3, 4)) -> int:
    """Fewest coins, considering every combination -- so it cannot be fooled."""
    best = [0] + [float("inf")] * target
    for amount in range(1, target + 1):
        for coin in coins:
            if coin <= amount:
                best[amount] = min(best[amount], best[amount - coin] + 1)
    return int(best[target]) if best[target] != float("inf") else -1
