"""Module 17 - greedy, divide and conquer, dynamic programming."""
from __future__ import annotations

from typing import Optional


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
        return memo[n]                    # <- the entire technique
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


def fib_table(n: int) -> int:
    """Bottom-up DP: fill in dependency order. No recursion, no stack risk."""
    if n <= 1:
        return n                          # n = 0 has no table[1] to seed
    table = [0] * (n + 1)
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]    # one addition, no recursion
    return table[n]


def fib_two_vars(n: int) -> int:
    """Only the last two entries are ever read, so the table collapses."""
    if n <= 1:
        return n                          # without this, fib(0) returns 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def coin_change_greedy(target: int, coins: tuple[int, ...] = (25, 10, 5, 1)) -> list[int]:
    """Take the largest coin that fits and never reconsider.

    Provably optimal for 1/5/10/25. With 1/3/4 it makes 6 as 4+1+1 when 3+3
    is better - greedy correctness is a property of the problem, not the code.
    """
    out: list[int] = []
    remaining = target
    for coin in sorted(coins, reverse=True):
        while remaining >= coin:
            out.append(coin)              # never revisited
            remaining -= coin
    return out


def coin_change_dp(target: int, coins: tuple[int, ...] = (1, 3, 4)) -> int:
    """Fewest coins, considering every combination - so it cannot be fooled."""
    best = [0] + [float("inf")] * target
    for amount in range(1, target + 1):
        for coin in coins:
            if coin <= amount:
                best[amount] = min(best[amount], best[amount - coin] + 1)
    return int(best[target]) if best[target] != float("inf") else -1
