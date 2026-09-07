"""Module 13 and 18: graphs, traversals, topological sort, Dijkstra."""
from __future__ import annotations

import heapq
from collections import deque
from typing import Any, Hashable, Optional

INFINITY = float("inf")


class Graph:
    """Adjacency list: O(V+E) space, the right default for sparse graphs.

    A matrix would answer 'is u next to v?' in O(1) but cost O(V^2) memory --
    a million vertices with ten edges each would need 10^12 mostly-zero cells.
    """

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self.adj: dict[Hashable, list[tuple[Hashable, float]]] = {}

    def add_vertex(self, v: Hashable) -> None:
        self.adj.setdefault(v, [])

    def add_edge(self, u: Hashable, v: Hashable, weight: float = 1.0) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def neighbours(self, v: Hashable) -> list[Hashable]:
        return [n for n, _ in self.adj.get(v, [])]

    def __len__(self) -> int:
        return len(self.adj)


def bfs(graph: Graph, start: Hashable) -> list[Hashable]:
    """A queue makes it breadth-first: distance k finishes before k+1 begins."""
    visited = {start}                        # mark on ENQUEUE, not on dequeue,
    queue = deque([start])                   # or a node enters the queue twice
    order: list[Hashable] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for n in graph.neighbours(node):
            if n not in visited:
                visited.add(n)
                queue.append(n)
    return order


def dfs(graph: Graph, start: Hashable) -> list[Hashable]:
    """Swap the queue for a stack and the same code goes deep instead of wide."""
    visited: set[Hashable] = set()
    stack = [start]
    order: list[Hashable] = []
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for n in reversed(graph.neighbours(node)):
            if n not in visited:
                stack.append(n)
    return order


def shortest_path_unweighted(graph: Graph, start: Hashable,
                             target: Hashable) -> Optional[list[Hashable]]:
    """BFS gives the fewest-EDGES path for free -- and only when unweighted.

    With weights, fewest edges stops meaning cheapest: see `dijkstra`.
    """
    if start == target:
        return [start]
    visited = {start}
    prev: dict[Hashable, Hashable] = {}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for n in graph.neighbours(node):
            if n in visited:
                continue
            visited.add(n)
            prev[n] = node
            if n == target:
                return _rebuild(prev, start, target)
            queue.append(n)
    return None


def _rebuild(prev: dict[Hashable, Hashable], start: Hashable,
             target: Hashable) -> list[Hashable]:
    path, node = [target], target
    while node != start:
        node = prev[node]
        path.append(node)
    return path[::-1]


UNVISITED, IN_PROGRESS, DONE = 0, 1, 2


def has_cycle(graph: Graph) -> bool:
    """Three colours. Reaching an IN_PROGRESS node is a back edge into your
    own active path -- a cycle. A DONE node is harmless shared structure.
    """
    state: dict[Hashable, int] = {v: UNVISITED for v in graph.adj}

    def walk(v: Hashable) -> bool:
        state[v] = IN_PROGRESS
        for n in graph.neighbours(v):
            if state.get(n) == IN_PROGRESS:
                return True
            if state.get(n) == UNVISITED and walk(n):
                return True
        state[v] = DONE
        return False

    return any(state[v] == UNVISITED and walk(v) for v in list(graph.adj))


def topological_sort(graph: Graph) -> Optional[list[Hashable]]:
    """A valid dependency order, or None when a cycle makes one impossible.

    That None is your circular-dependency error.
    """
    indegree: dict[Hashable, int] = {v: 0 for v in graph.adj}
    for u in graph.adj:
        for v, _ in graph.adj[u]:
            indegree[v] = indegree.get(v, 0) + 1
    ready = deque(sorted((v for v, d in indegree.items() if d == 0), key=repr))
    order: list[Hashable] = []
    while ready:
        v = ready.popleft()
        order.append(v)
        for n, _ in graph.adj[v]:
            indegree[n] -= 1
            if indegree[n] == 0:
                ready.append(n)
    return order if len(order) == len(graph.adj) else None


def dijkstra(graph: Graph, source: Hashable) -> tuple[dict, dict]:
    """Cheapest first, not nearest first.

    Pulling the cheapest unsettled node makes its distance final: any other
    route runs through a node that is already at least as expensive, and
    non-negative edges cannot reduce a total. One negative edge and that
    argument collapses -- use Bellman-Ford instead.
    """
    if any(w < 0 for u in graph.adj for _, w in graph.adj[u]):
        raise ValueError("Dijkstra requires non-negative weights")

    dist: dict[Hashable, float] = {v: INFINITY for v in graph.adj}
    prev: dict[Hashable, Optional[Hashable]] = {v: None for v in graph.adj}
    dist[source] = 0.0
    settled: set[Hashable] = set()
    pq: list[tuple[float, Hashable]] = [(0.0, source)]

    while pq:
        d, u = heapq.heappop(pq)
        if u in settled:
            continue                         # a stale entry: skip it
        settled.add(u)                       # dist[u] is now FINAL
        for v, w in graph.adj[u]:
            if v in settled:
                continue
            if d + w < dist[v]:              # the relaxation step IS the algorithm
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, prev


def path_to(prev: dict, target: Hashable) -> list[Hashable]:
    """dist tells you the cost; only prev tells you the route."""
    out: list[Hashable] = []
    node: Optional[Hashable] = target
    while node is not None:
        out.append(node)
        node = prev.get(node)
    return out[::-1]
