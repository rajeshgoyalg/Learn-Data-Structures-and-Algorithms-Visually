"""Module 13 - graph traversals on a plain adjacency dict."""
from __future__ import annotations

from collections import deque
from typing import Hashable, Optional

UNVISITED, IN_PROGRESS, DONE = 0, 1, 2


def bfs(adj: dict, start: Hashable) -> list:
    """A queue makes it breadth-first: distance k finishes before k+1 begins."""
    visited = {start}                     # mark on ENQUEUE, not on dequeue, or a
    queue = deque([start])                # node with two routes is queued twice
    order = []
    while queue:
        node = queue.popleft()            # FIFO
        order.append(node)
        for n in adj.get(node, []):
            if n not in visited:
                visited.add(n)
                queue.append(n)
    return order


def dfs(adj: dict, start: Hashable) -> list:
    """Swap the queue for a stack and the same code goes deep instead of wide."""
    visited = set()
    stack = [start]
    order = []
    while stack:
        node = stack.pop()                # LIFO - the only change from bfs
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for n in reversed(adj.get(node, [])):
            if n not in visited:
                stack.append(n)
    return order


def shortest_path_unweighted(adj: dict, start: Hashable, target: Hashable) -> Optional[list]:
    """BFS gives the fewest-EDGES path for free.

    The guarantee evaporates the moment edges have weights: a one-edge road
    of length 400 beats a four-edge route of length 40 by this measure, and
    loses badly by the real one. That is Dijkstra's job.
    """
    if start == target:
        return [start]
    visited = {start}
    prev: dict = {}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for n in adj.get(node, []):
            if n in visited:
                continue
            visited.add(n)
            prev[n] = node
            if n == target:
                path = [target]
                while path[-1] != start:
                    path.append(prev[path[-1]])
                return path[::-1]
            queue.append(n)
    return None                           # unreachable


def has_cycle(adj: dict) -> bool:
    """Three colours. Reaching an IN_PROGRESS node is a back edge into your
    own active path - a cycle. A DONE node is harmless shared structure."""
    state = {v: UNVISITED for v in adj}

    def walk(v: Hashable) -> bool:
        state[v] = IN_PROGRESS
        for n in adj.get(v, []):
            if state.get(n) == IN_PROGRESS:
                return True
            if state.get(n, UNVISITED) == UNVISITED and walk(n):
                return True
        state[v] = DONE
        return False

    return any(state[v] == UNVISITED and walk(v) for v in list(adj))


def topological_sort(adj: dict) -> Optional[list]:
    """A valid dependency order, or None when a cycle makes one impossible.

    That None is your circular-dependency error.
    """
    indegree = {v: 0 for v in adj}
    for u in adj:
        for v in adj[u]:
            indegree[v] = indegree.get(v, 0) + 1
    ready = deque(sorted((v for v, d in indegree.items() if d == 0), key=repr))
    order = []
    while ready:
        v = ready.popleft()
        order.append(v)
        for n in adj.get(v, []):
            indegree[n] -= 1
            if indegree[n] == 0:
                ready.append(n)
    return order if len(order) == len(indegree) else None
