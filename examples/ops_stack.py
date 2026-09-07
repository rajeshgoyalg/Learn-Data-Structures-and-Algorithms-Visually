"""Module 05 - stack operations. A stack is a list with two ends forbidden."""
from __future__ import annotations

from typing import Any

PAIRS = {")": "(", "]": "[", "}": "{"}


def push(stack: list[Any], value: Any) -> None:
    """Put a value on the top. O(1)."""
    stack.append(value)


def pop(stack: list[Any]) -> Any:
    """Remove and return the top. O(1)."""
    if not stack:
        raise IndexError("underflow: pop from an empty stack")
    return stack.pop()                    # the value is not erased, just unreachable


def peek(stack: list[Any]) -> Any:
    """Read the top without removing it. O(1)."""
    if not stack:
        raise IndexError("empty")
    return stack[-1]


def is_empty(stack: list[Any]) -> bool:
    return not stack


def is_balanced(text: str) -> bool:
    """The canonical application: every opener is a note saying 'close me'.

    The stack guarantees they close in the reverse of the order they opened,
    which is exactly what nesting means.
    """
    stack: list[str] = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)              # remember to close this
        elif ch in ")]}":
            if not stack:
                return False              # a closer with nothing open
            if stack.pop() != PAIRS[ch]:
                return False              # closed in the wrong order
    return not stack                      # anything left open is unbalanced
