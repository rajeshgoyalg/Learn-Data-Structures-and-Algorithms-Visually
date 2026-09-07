"""Module 12 - trie operations. The letters live on the edges."""
from __future__ import annotations

from typing import Optional

from examples.nodes import TrieNode


def insert(root: TrieNode, word: str) -> None:
    """Creates only the nodes that do not exist yet.

    Inserting "car" when "cat" is already stored adds exactly one node.
    """
    node = root
    for ch in word:
        if ch not in node.children:
            node.children[ch] = TrieNode()
        node = node.children[ch]
    node.is_end = True                    # the flag is what makes it a word


def walk(root: TrieNode, s: str) -> Optional[TrieNode]:
    """Follow one edge per character. O(L), whatever the word count."""
    node = root
    for ch in s:
        if ch not in node.children:
            return None
        node = node.children[ch]
    return node


def search(root: TrieNode, word: str) -> bool:
    """Reaching the node is not enough - it must be marked as a word end."""
    node = walk(root, word)
    return node is not None and node.is_end


def starts_with(root: TrieNode, prefix: str) -> bool:
    """The same walk, one different final line. This is the whole feature -
    a hash table cannot answer it without scanning every key."""
    return walk(root, prefix) is not None


def autocomplete(root: TrieNode, prefix: str) -> list[str]:
    """O(L) to reach the prefix, then a walk of only that subtree.

    Every word in that subtree starts with the prefix by construction, so no
    non-matching word is ever visited.
    """
    node = walk(root, prefix)
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


def delete(root: TrieNode, word: str) -> bool:
    """Unset the flag, then drop any node nothing else needs.

    Returns True if the word was present. Deleting "cart" must not remove the
    c-a-r chain, because "car" still needs it - so a node is only dropped when
    it has no children AND is not itself the end of a word.
    """
    node = walk(root, word)
    if node is None or not node.is_end:
        return False                      # never stored: nothing to do
    node.is_end = False                   # the word is gone from the trie

    path = [root]                         # every node on the way down
    for ch in word:
        path.append(path[-1].children[ch])

    for depth in range(len(word), 0, -1):
        child = path[depth]
        if child.children or child.is_end:
            break                         # something still needs this node
        del path[depth - 1].children[word[depth - 1]]
    return True
