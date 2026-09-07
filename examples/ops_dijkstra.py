"""Module 18 - Dijkstra. Two tables, one priority queue, one repeated move."""
from __future__ import annotations

import heapq
from typing import Hashable, Optional

INFINITY = float("inf")


def relax(dist: dict, prev: dict, u: Hashable, v: Hashable, weight: float) -> bool:
    """The whole algorithm is this one comparison.

    'Does going via u beat the best route to v that I already know?'
    """
    if dist[u] + weight < dist[v]:
        dist[v] = dist[u] + weight        # a cheaper route to v exists
        prev[v] = u                       # remember how we got there
        return True
    return False


def dijkstra(adj: dict, source: Hashable) -> tuple[dict, dict]:
    """Cheapest first, not nearest first.

    Pulling the cheapest unsettled node makes its distance final: any other
    route runs through a node already at least as expensive, and non-negative
    edges cannot reduce a total. One negative edge and that argument
    collapses - it will not error, it will quietly return a wrong answer.
    """
    if any(w < 0 for u in adj for _, w in adj[u]):
        raise ValueError("Dijkstra requires non-negative weights")

    dist = {v: INFINITY for v in adj}
    prev: dict = {v: None for v in adj}
    dist[source] = 0.0
    settled = set()
    pq = [(0.0, source)]

    while pq:
        d, u = heapq.heappop(pq)          # the cheapest unsettled node
        if u in settled:
            continue                      # a stale entry: skip it
        settled.add(u)                    # dist[u] is now FINAL
        for v, w in adj.get(u, []):
            if v not in settled and relax(dist, prev, u, v, w):
                heapq.heappush(pq, (dist[v], v))
    return dist, prev


def path_to(prev: dict, target: Hashable) -> list:
    """dist gives you the cost; only prev gives you the route."""
    out = []
    node: Optional[Hashable] = target
    while node is not None:
        out.append(node)
        node = prev.get(node)
    return out[::-1]                      # walk backwards, then reverse
