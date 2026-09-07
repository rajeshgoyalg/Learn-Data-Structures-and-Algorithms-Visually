"""Module 09-12: heaps, binary search trees, AVL trees, tries."""
from __future__ import annotations

from typing import Any, Iterator, Optional


def parent(i: int) -> int:
    return (i - 1) // 2


def left(i: int) -> int:
    return 2 * i + 1


def right(i: int) -> int:
    return 2 * i + 2


class MinHeap:
    """A complete binary tree stored in a flat list -- no pointers at all.

    The heap property is local (parent <= both children) yet globally
    guarantees the minimum sits at index 0. Siblings are unordered: a heap is
    NOT sorted and NOT a search tree.
    """

    def __init__(self, values: Optional[list[Any]] = None) -> None:
        self._a: list[Any] = list(values or [])
        if self._a:
            self.build()

    def __len__(self) -> int:
        return len(self._a)

    def peek(self) -> Any:
        if not self._a:
            raise IndexError("empty")
        return self._a[0]                                # O(1), by the property

    def insert(self, value: Any) -> None:
        self._a.append(value)                            # the next free leaf
        self._sift_up(len(self._a) - 1)                   # keeps it complete

    def extract_min(self) -> Any:
        if not self._a:
            raise IndexError("empty")
        smallest = self._a[0]
        last = self._a.pop()
        if self._a:
            self._a[0] = last                            # the last leaf is the
            self._sift_down(0)                           # only gap-free removal
        return smallest

    def build(self) -> None:
        """O(n), not O(n log n): most nodes sift down almost no distance."""
        for i in range(len(self._a) // 2 - 1, -1, -1):
            self._sift_down(i)

    def _sift_up(self, i: int) -> None:
        while i > 0 and self._a[i] < self._a[parent(i)]:
            self._a[i], self._a[parent(i)] = self._a[parent(i)], self._a[i]
            i = parent(i)                                # at most log n swaps

    def _sift_down(self, i: int) -> None:
        n = len(self._a)
        while True:
            smallest = i
            if left(i) < n and self._a[left(i)] < self._a[smallest]:
                smallest = left(i)
            if right(i) < n and self._a[right(i)] < self._a[smallest]:
                smallest = right(i)          # swap with the SMALLER child, or the
            if smallest == i:                # other one ends up under a bigger key
                return
            self._a[i], self._a[smallest] = self._a[smallest], self._a[i]
            i = smallest

    def as_list(self) -> list[Any]:
        return list(self._a)


def heapsort(values: list[Any]) -> list[Any]:
    """O(n log n) time in O(1) extra space -- but not stable."""
    heap = MinHeap(values)
    return [heap.extract_min() for _ in range(len(heap))]


def top_k(stream: Iterator[Any], k: int) -> list[Any]:
    """Largest k of a stream in O(n log k) time and O(k) memory."""
    heap = MinHeap()
    for value in stream:
        if len(heap) < k:
            heap.insert(value)
        elif k > 0 and value > heap.peek():
            heap.extract_min()
            heap.insert(value)
    return sorted(heap.as_list(), reverse=True)


class TreeNode:
    __slots__ = ("value", "left", "right", "height")

    def __init__(self, value: Any) -> None:
        self.value = value
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None
        self.height = 1


class BST:
    """Every value in the left subtree is smaller, every value on the right larger.

    The claim is about whole subtrees, which is what licenses discarding a
    branch without inspecting it.
    """

    def __init__(self, values: Optional[list[Any]] = None) -> None:
        self.root: Optional[TreeNode] = None
        for v in values or []:
            self.insert(v)

    def search(self, target: Any) -> bool:
        node = self.root
        while node is not None:
            if target == node.value:
                return True
            node = node.left if target < node.value else node.right
        return False

    def insert(self, value: Any) -> None:
        self.root = self._insert(self.root, value)

    def _insert(self, node: Optional[TreeNode], value: Any) -> TreeNode:
        if node is None:
            return TreeNode(value)           # you fell off the tree: plant here
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        return node                          # equal values are ignored

    def delete(self, value: Any) -> None:
        self.root = self._delete(self.root, value)

    def _delete(self, node: Optional[TreeNode], value: Any) -> Optional[TreeNode]:
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right            # no children, or only a right one
            if node.right is None:
                return node.left
            successor = node.right           # two children: take the in-order
            while successor.left is not None:
                successor = successor.left   # successor -- the only value that
            node.value = successor.value     # keeps the invariant intact
            node.right = self._delete(node.right, successor.value)
        return node

    def minimum(self) -> Any:
        node = self.root
        if node is None:
            raise IndexError("empty")
        while node.left is not None:
            node = node.left
        return node.value

    def maximum(self) -> Any:
        node = self.root
        if node is None:
            raise IndexError("empty")
        while node.right is not None:
            node = node.right
        return node.value

    def height(self) -> int:
        def h(n: Optional[TreeNode]) -> int:
            return 0 if n is None else 1 + max(h(n.left), h(n.right))
        return h(self.root)

    # --- traversals: one function, the visit line in three positions ---
    def in_order(self) -> list[Any]:
        out: list[Any] = []

        def walk(n: Optional[TreeNode]) -> None:
            if n is None:
                return
            walk(n.left)
            out.append(n.value)              # LEFT, node, RIGHT -> sorted output
            walk(n.right)
        walk(self.root)
        return out

    def pre_order(self) -> list[Any]:
        out: list[Any] = []

        def walk(n: Optional[TreeNode]) -> None:
            if n is None:
                return
            out.append(n.value)              # node, LEFT, RIGHT -> serialise
            walk(n.left)
            walk(n.right)
        walk(self.root)
        return out

    def post_order(self) -> list[Any]:
        out: list[Any] = []

        def walk(n: Optional[TreeNode]) -> None:
            if n is None:
                return
            walk(n.left)
            walk(n.right)
            out.append(n.value)              # LEFT, RIGHT, node -> free / evaluate
        walk(self.root)
        return out

    def level_order(self) -> list[Any]:
        """The only one that needs an explicit queue rather than the call stack."""
        if self.root is None:
            return []
        out, queue = [], [self.root]
        while queue:
            node = queue.pop(0)
            out.append(node.value)
            queue.extend(n for n in (node.left, node.right) if n is not None)
        return out


class AVLTree(BST):
    """A BST that rotates the moment a balance factor reaches +/-2.

    Guarantees O(log n) whatever order the data arrives in -- which a plain
    BST does not, because sorted input degenerates it into a linked list.
    """

    @staticmethod
    def _h(node: Optional[TreeNode]) -> int:
        return 0 if node is None else node.height

    def _balance(self, node: TreeNode) -> int:
        return self._h(node.left) - self._h(node.right)

    def _update(self, node: TreeNode) -> None:
        node.height = 1 + max(self._h(node.left), self._h(node.right))

    def _rotate_right(self, y: TreeNode) -> TreeNode:
        x = y.left
        assert x is not None
        t = x.right                          # t is larger than x, smaller than y,
        x.right, y.left = y, t               # so it is still legal where it lands
        self._update(y)                      # order matters: y is now BELOW x
        self._update(x)
        return x

    def _rotate_left(self, x: TreeNode) -> TreeNode:
        y = x.right
        assert y is not None
        t = y.left
        y.left, x.right = x, t
        self._update(x)
        self._update(y)
        return y

    def _insert(self, node: Optional[TreeNode], value: Any) -> TreeNode:
        if node is None:
            return TreeNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        else:
            return node

        self._update(node)
        balance = self._balance(node)

        if balance > 1 and value < node.left.value:        # LL
            return self._rotate_right(node)
        if balance < -1 and value > node.right.value:      # RR
            return self._rotate_left(node)
        if balance > 1:                                    # LR: straighten first
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1:                                   # RL
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node


class TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.is_end = False                  # a prefix is not a word


class Trie:
    """Letters live on the edges; a node is just 'the prefix you have spelled'.

    Lookup is O(L) in the key length and independent of how many words are
    stored -- which is why autocomplete uses one.
    """

    def __init__(self, words: Optional[list[str]] = None) -> None:
        self.root = TrieNode()
        for w in words or []:
            self.insert(w)

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())   # create only what
        node.is_end = True                                     # does not exist

    def _walk(self, s: str) -> Optional[TrieNode]:
        node = self.root
        for ch in s:
            node = node.children.get(ch)                       # type: ignore[assignment]
            if node is None:
                return None
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_end                # the flag decides

    def starts_with(self, prefix: str) -> bool:
        return self._walk(prefix) is not None                  # reaching it is enough

    def autocomplete(self, prefix: str) -> list[str]:
        """O(L) to the prefix node, then a walk of only that subtree."""
        node = self._walk(prefix)
        if node is None:
            return []
        out: list[str] = []

        def collect(n: TrieNode, so_far: str) -> None:
            if n.is_end:
                out.append(so_far)
            for ch, child in sorted(n.children.items()):
                collect(child, so_far + ch)
        collect(node, prefix)
        return out

    def delete(self, word: str) -> bool:
        """Unset the flag; prune a node only if nothing else needs it."""
        def prune(node: TrieNode, depth: int) -> bool:
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                return not node.children
            ch = word[depth]
            child = node.children.get(ch)
            if child is None:
                return False
            if prune(child, depth + 1):
                del node.children[ch]
                return not node.children and not node.is_end
            return False
        return prune(self.root, 0)
