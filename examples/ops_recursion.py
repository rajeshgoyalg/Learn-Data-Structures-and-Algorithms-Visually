"""Module 16 - recursion and backtracking."""
from __future__ import annotations


def factorial(n: int) -> int:
    """All three required parts in four lines."""
    if n <= 1:
        return 1                          # 1. BASE CASE: returns without recursing
    return n * factorial(n - 1)           # 2. RECURSIVE CASE, 3. n-1 is PROGRESS


def solve_n_queens(n: int = 4) -> list[list[int]]:
    """Backtracking: choose, recurse, and UNDO when the branch cannot work.

    The undo is the whole difference from brute force - it abandons every
    completion of an illegal prefix without ever generating them. For 8
    queens that is ~2,000 explored states instead of 4.4 billion.
    """
    solutions: list[list[int]] = []
    placed: list[int] = []                # placed[row] = column

    def safe(row: int, col: int) -> bool:
        return all(c != col and abs(r - row) != abs(c - col)
                   for r, c in enumerate(placed))

    def place(row: int) -> None:
        if row == n:
            solutions.append(placed.copy())
            return
        for col in range(n):
            if safe(row, col):
                placed.append(col)        # CHOOSE
                place(row + 1)            # EXPLORE
                placed.pop()              # UNCHOOSE - this is backtracking

    place(0)
    return solutions
