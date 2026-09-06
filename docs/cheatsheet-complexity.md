# 📋 Complexity cheat sheet

Everything in the repo, on one page. Print it, or keep it open in a tab.

---

## 📊 The cost matrix

![Operation cost matrix](../assets/infographic/operation-cost-matrix.svg)

---

## Data structures

`n` = number of elements · `L` = length of a key · `V`/`E` = vertices/edges

| Structure | Access | Search | Insert | Delete | Space | Ordered? |
|:--|:--:|:--:|:--:|:--:|:--:|:--:|
| **[Array](02-arrays.md)** | O(1) | O(n) | O(n) | O(n) | O(n) | by index |
| Array, sorted | O(1) | O(log n) | O(n) | O(n) | O(n) | ✅ |
| Dynamic array (append) | O(1) | O(n) | **O(1)** amortised | O(n) | O(n) | by index |
| **[Singly linked list](03-linked-lists.md)** | O(n) | O(n) | O(1)† | O(1)† | O(n) | insertion |
| **[Doubly linked list](04-doubly-and-circular-lists.md)** | O(n) | O(n) | O(1)† | **O(1)**‡ | O(n) | insertion |
| **[Stack](05-stacks.md)** | O(n) | O(n) | O(1) | O(1) | O(n) | LIFO |
| **[Queue](06-queues.md)** | O(n) | O(n) | O(1) | O(1) | O(n) | FIFO |
| Deque | O(n) | O(n) | O(1) both ends | O(1) both ends | O(n) | both |
| **[Hash table](07-hash-tables.md)** | — | **O(1)** avg / O(n) worst | O(1) avg | O(1) avg | O(n) | ❌ |
| **[Set](08-sets.md)** (hash) | — | O(1) avg | O(1) avg | O(1) avg | O(n) | ❌ |
| **[Heap](09-heaps.md)** | O(1) peek | O(n) | O(log n) | O(log n) | O(n) | partial |
| Priority queue | O(1) peek | O(n) | O(log n) | O(log n) | O(n) | by key |
| **[BST](10-binary-search-trees.md)**, balanced | — | O(log n) | O(log n) | O(log n) | O(n) | ✅ |
| BST, degenerate | — | **O(n)** | O(n) | O(n) | O(n) | ✅ |
| **[AVL / red-black](11-balanced-trees.md)** | — | O(log n) | O(log n) | O(log n) | O(n) | ✅ |
| **[Trie](12-tries.md)** | — | **O(L)** | O(L) | O(L) | O(n·L·A) | ✅ lexicographic |
| **[Graph](13-graphs.md)**, adjacency list | — | O(V+E) | O(1) edge | O(E) | O(V+E) | ❌ |
| Graph, adjacency matrix | **O(1)** edge test | O(V²) | O(1) | O(1) | O(V²) | ❌ |

† given a reference to the position — finding it is `O(n)`
‡ given only the node itself, which a singly linked list cannot do

---

## Sorting

| Algorithm | Best | Average | Worst | Space | Stable | Adaptive |
|:--|:--:|:--:|:--:|:--:|:--:|:--:|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | ✅ | ✅ |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | ❌ | ❌ |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | ✅ | ✅ |
| **Merge** | O(n log n) | O(n log n) | **O(n log n)** | O(n) | ✅ | ❌ |
| **Quick** | O(n log n) | O(n log n) | **O(n²)** | O(log n) | ❌ | ❌ |
| Heap | O(n log n) | O(n log n) | O(n log n) | **O(1)** | ❌ | ❌ |
| Counting | O(n+k) | O(n+k) | O(n+k) | O(k) | ✅ | ❌ |
| Radix | O(n·d) | O(n·d) | O(n·d) | O(n+k) | ✅ | ❌ |

Counting and radix sort are **not comparison-based**, which is the only reason they are allowed to beat `O(n log n)`. See [module 15](15-sorting.md).

---

## Searching

| Algorithm | Time | Space | Requires |
|:--|:--:|:--:|:--|
| Linear search | O(n) | O(1) | nothing |
| Binary search | O(log n) | O(1) iterative | sorted + random access |
| Hash lookup | O(1) avg | O(n) | a hash function |
| BST search | O(log n) balanced | O(1) | an ordering |
| Trie search | O(L) | O(n·L·A) | sequence keys |

---

## Graph algorithms

| Algorithm | Time | Space | Handles | Answers |
|:--|:--:|:--:|:--|:--|
| BFS | O(V+E) | O(V) | unweighted | shortest path in **edges** |
| DFS | O(V+E) | O(V) | any | reachability, cycles, topological order |
| **[Dijkstra](18-dijkstra.md)** | O((V+E) log V) | O(V) | non-negative weights | shortest path in **cost** |
| Bellman-Ford | O(V·E) | O(V) | **negative** weights | shortest path; detects negative cycles |
| Floyd-Warshall | O(V³) | O(V²) | negative weights | **all pairs** of shortest paths |
| A\* | O(E) with a good heuristic | O(V) | non-negative + a heuristic | shortest path, exploring far less |
| Topological sort | O(V+E) | O(V) | DAGs only | a valid dependency order |
| Kruskal / Prim | O(E log V) | O(V) | weighted, undirected | minimum spanning tree |

---

## The numbers that matter

| n | O(log n) | O(n) | O(n log n) | O(n²) | O(2ⁿ) |
|--:|--:|--:|--:|--:|--:|
| 10 | 3 | 10 | 33 | 100 | 1,024 |
| 100 | 7 | 100 | 664 | 10,000 | 10³⁰ |
| 1,000 | 10 | 1,000 | 9,966 | 1,000,000 | — |
| 1,000,000 | 20 | 10⁶ | 2 × 10⁷ | 10¹² | — |
| 1,000,000,000 | 30 | 10⁹ | 3 × 10¹⁰ | 10¹⁸ | — |

![Growth curves](../assets/infographic/big-o-growth.svg)

---

## Which structure? — the one-minute version

![Structure chooser](../assets/infographic/structure-chooser.svg)

| The question your code asks | Use |
|:--|:--|
| "is this present?" | **hash set** |
| "what is the value for this key?" | **hash map** |
| "give me these keys in sorted order" | **balanced BST** |
| "what is the most urgent item?" | **heap / priority queue** |
| "who is next in line?" | **queue** |
| "what did I do last?" | **stack** |
| "which words start with these letters?" | **trie** |
| "how are these things connected?" | **graph** + BFS/DFS |
| "give me item number 7" | **array** |

---

## Rules of thumb

- **Big-O hides constants.** Below roughly `n = 20`, insertion sort beats every `O(n log n)` sort.
- **Contiguity is worth a lot.** Arrays regularly beat linked lists in practice despite worse Big-O, because of the cache.
- **Amortised ≠ worst case.** Appending to a dynamic array averages `O(1)` but individual appends spike to `O(n)`.
- **`O(1)` does not mean fast.** It means it does not grow. An expensive hash can lose to a short scan.
- **A plain BST has no guarantees.** Its complexity is its height, and its height is your insertion order.
- **One negative edge invalidates Dijkstra**, silently. It returns a wrong answer rather than an error.
- **Unproved greedy is a guess.** If you cannot prove the greedy-choice property, use DP.
- **Space matters as much as time.** `O(depth)` recursion is real memory, and real stacks are finite.

---

⬅️ [18 · Dijkstra](18-dijkstra.md) · [🏠 Index](../README.md) · [🃏 Flashcards](flashcards.md) ➡️
