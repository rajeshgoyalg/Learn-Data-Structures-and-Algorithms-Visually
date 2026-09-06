# ❓ Quiz bank — 45 questions, three levels

These are **new** questions, not the ones inside the modules. Work through a level without looking anything up, then check. Score yourself at the bottom.

| Level | Questions | What it tests |
|:--|--:|:--|
| [🟢 Level 1 · Recall](#level-1--recall) | 15 | do you know what each structure *is* |
| [🟡 Level 2 · Apply](#level-2--apply) | 15 | can you pick the right one for a job |
| [🔴 Level 3 · Reason](#level-3--reason) | 15 | do you understand *why* the costs are what they are |

---

## Level 1 · Recall

**1.1** Which structure guarantees `O(1)` access by index?

<details><summary>Answer</summary>

**Array.** Contiguous memory makes `base + i × itemSize` a pure calculation. No other structure here offers it.
</details>

**1.2** Which two structures are defined by a *restriction* on where you may add and remove?

<details><summary>Answer</summary>

**Stack** (one end only, LIFO) and **queue** (add at one end, remove at the other, FIFO). Both are policies imposed on an ordinary container.
</details>

**1.3** What is the average-case cost of a hash table lookup, and its worst case?

<details><summary>Answer</summary>

`O(1)` average, **`O(n)` worst** — when every key collides into one bucket.
</details>

**1.4** In a min-heap, where is the largest element?

<details><summary>Answer</summary>

Somewhere in the **leaf row**, but the heap does not say where. Finding it costs `O(n)`.
</details>

**1.5** What does an in-order traversal of a BST produce?

<details><summary>Answer</summary>

The values in **sorted ascending order** — always, for any valid BST.
</details>

**1.6** Which sorting algorithms in this repo are stable?

<details><summary>Answer</summary>

**Bubble, insertion, merge** (and counting/radix). Selection, quick and heap sort are not.
</details>

**1.7** Which traversal does BFS use, and which structure powers it?

<details><summary>Answer</summary>

Level-order, powered by a **queue**.
</details>

**1.8** What is the height of a balanced BST with 1,000,000 nodes?

<details><summary>Answer</summary>

About **20**, since `log₂(1,000,000) ≈ 20`.
</details>

**1.9** In a trie, what do the nodes store?

<details><summary>Answer</summary>

A **children map** and an **isEndOfWord** flag. The characters are on the *edges*, not in the nodes.
</details>

**1.10** What are the two collision-resolution strategies for a hash table?

<details><summary>Answer</summary>

**Separate chaining** (a list per bucket) and **open addressing** (probe for the next free slot).
</details>

**1.11** Name the three required parts of a recursive function.

<details><summary>Answer</summary>

**Base case**, **recursive case**, and **progress** toward the base case.
</details>

**1.12** What does Dijkstra require of its edge weights?

<details><summary>Answer</summary>

They must be **non-negative**. One negative edge invalidates the correctness argument.
</details>

**1.13** Which is `O(n log n)` in every case: merge sort or quicksort?

<details><summary>Answer</summary>

**Merge sort.** Quicksort degrades to `O(n²)` on bad pivots.
</details>

**1.14** What is a DAG?

<details><summary>Answer</summary>

A **Directed Acyclic Graph** — directed edges with no cycles. It is the shape of any dependency relationship, and can be topologically sorted.
</details>

**1.15** Which structure has `O(1)` peek but `O(n)` search?

<details><summary>Answer</summary>

A **heap**. The root is the extreme value instantly, but the heap property says nothing about siblings, so finding anything else means scanning.
</details>

---

## Level 2 · Apply

**2.1** You are building autocomplete for a 500,000-word dictionary. Which structure?

<details><summary>Answer</summary>

A **trie**. `O(L)` to reach the prefix node, then a DFS of that subtree lists every match — without touching a single non-matching word. A hash table would have to scan all 500,000 keys.
</details>

**2.2** You must process web requests strictly in arrival order. Which structure?

<details><summary>Answer</summary>

A **queue** — FIFO is exactly the fairness guarantee you want. If some requests are more urgent, upgrade to a **priority queue**.
</details>

**2.3** You need "the 100 highest scores" from a stream of 50 million. Which structure and what does it cost?

<details><summary>Answer</summary>

A **min-heap of size 100**. Push while under 100; afterwards, replace the root whenever an item beats it. `O(n log 100)` time and `O(100)` memory — you never hold the stream.
</details>

**2.4** You need a lookup table for 10,000 config keys, read constantly, never iterated in order. Which structure?

<details><summary>Answer</summary>

A **hash map**. `O(1)` lookup and you have explicitly given up nothing, since ordering is not required.
</details>

**2.5** Same as 2.4, but you must also list keys alphabetically on a settings page. Now which?

<details><summary>Answer</summary>

A **balanced BST** (sorted map). You trade `O(1)` for `O(log n)` lookups and get ordered iteration in `O(n)`. Alternatively keep the hash map and sort on demand — fine if that page is rare, wasteful if it is not.
</details>

**2.6** You maintain a browser's back/forward navigation. Which structure(s)?

<details><summary>Answer</summary>

**Two stacks.** Navigating pushes the current page onto the back stack. Back pops it and pushes onto the forward stack. A new navigation clears the forward stack — which is exactly why the forward button greys out.
</details>

**2.7** You must detect whether a build configuration contains a circular dependency. What do you run?

<details><summary>Answer</summary>

**DFS with three-colour marking** on the directed dependency graph. Reaching a node still IN_PROGRESS means a back edge into your own path — a cycle. `O(V+E)`.
</details>

**2.8** A fixed-size audio buffer must never allocate. Which structure?

<details><summary>Answer</summary>

A **circular queue** (ring buffer). Fixed capacity, `O(1)` at both ends, indices wrap with modulo, and no allocation ever happens after startup.
</details>

**2.9** You need to remove duplicates from a 1,000,000-item list while preserving first-seen order.

<details><summary>Answer</summary>

One pass with a **hash set** of seen values, appending to an output list only on a miss. `O(n)` time and `O(n)` space. Nested-loop comparison would be `O(n²)` — 10¹² operations.
</details>

**2.10** A game must decide whose turn is next, forever, with players joining and leaving.

<details><summary>Answer</summary>

A **circular linked list**. `next` is always valid and wraps for free; insertion and removal are `O(1)` given the node. Make it circular *doubly* linked if you also need to go back a turn.
</details>

**2.11** You are asked for the shortest driving route between two cities with distances on each road.

<details><summary>Answer</summary>

**Dijkstra** with a binary heap — `O((V+E) log V)`. BFS would return the route with the fewest junctions, which is not the same thing at all. With a straight-line-distance heuristic, **A\*** explores far less.
</details>

**2.12** Sorting 10,000,000 records where stability is required and worst-case latency is bounded.

<details><summary>Answer</summary>

**Merge sort** (or Timsort). It is the only `O(n log n)` stable option, and unlike quicksort its worst case is also `O(n log n)`. Accept the `O(n)` buffer as the price.
</details>

**2.13** You need to know if a username is taken, from a set of 100,000,000, in constant time.

<details><summary>Answer</summary>

A **hash set**. (If a small false-positive rate were acceptable and memory were critical, a Bloom filter would use a fraction of the space — but that is beyond this course.)
</details>

**2.14** You have a static sorted list of 1,000,000 timestamps and must find every entry in a date range, constantly.

<details><summary>Answer</summary>

**Binary search with `lowerBound`** on the array — `O(log n)` to find the range start, then a linear walk to its end. No tree needed: the data is static, and the array is smaller and more cache-friendly.
</details>

**2.15** You must undo the last 50 operations in a text editor.

<details><summary>Answer</summary>

A **stack** (capped at 50, so really a **deque** — push and pop at the front, discard from the back). LIFO is literally the semantics of undo.
</details>

---

## Level 3 · Reason

**3.1** Why is `buildHeap` `O(n)` when it calls an `O(log n)` routine `n/2` times?

<details><summary>Answer</summary>

Because `siftDown`'s real cost is the height *below* a node, and the tree is bottom-heavy. Half the nodes are leaves (cost 0), a quarter cost 1, an eighth cost 2. The series `n/4·1 + n/8·2 + n/16·3 + …` converges to `2n`. Only the root pays the full `log n`.
</details>

**3.2** An array and a linked list both do an `O(n)` full scan. Why is the array often 10× faster in practice?

<details><summary>Answer</summary>

**Cache behaviour.** The CPU fetches contiguous cache lines and prefetches ahead, so an array scan gets many elements per memory access. Linked-list nodes can be anywhere, so nearly every hop is a cache miss. Big-O ignores this; your profiler does not.
</details>

**3.3** Why does a hash table's average `O(1)` degrade to `O(n)` in the worst case, and how do real implementations mitigate it?

<details><summary>Answer</summary>

If every key hashes to the same bucket, the table becomes one long chain. Mitigations: a well-distributed hash function, a **load factor** trigger to resize and rehash, **randomised hash seeds** so an attacker cannot craft collisions, and converting an oversized bucket chain into a balanced tree — capping the worst case at `O(log n)`.
</details>

**3.4** Why is `O(n log n)` a hard floor for comparison-based sorting but not for counting sort?

<details><summary>Answer</summary>

With `n!` possible orderings and one bit of information per comparison, you need `log₂(n!) = Θ(n log n)` comparisons to identify the ordering — an information-theoretic bound. Counting sort never compares elements; it uses the key values as array indices directly, which is extra information the bound does not account for. That only works for bounded integer keys.
</details>

**3.5** A plain BST and a hash table both store 1,000,000 keys. Explain when the BST wins despite being `O(log n)`.

<details><summary>Answer</summary>

Whenever **order** is involved: sorted iteration, min/max, predecessor/successor, and range queries — all `O(log n)` or `O(n)` on a tree and effectively impossible on a hash table. The hash table only wins the narrow case of exact-match lookup.
</details>

**3.6** Why does inserting a black node into a red-black tree break more than inserting a red one?

<details><summary>Answer</summary>

A black node increments the black-height of **every** root-to-leaf path through it, violating rule 5 globally — an expensive, non-local repair. A red node can only violate rule 4 (a red child of a red parent), which is local and often fixed by recolouring alone.
</details>

**3.7** Why does BFS find shortest paths on unweighted graphs but not weighted ones?

<details><summary>Answer</summary>

BFS expands strictly by *number of edges*, finishing distance `k` before touching `k+1`, so the first arrival at a node uses the fewest edges. With weights, "fewest edges" and "cheapest" diverge — a one-edge road of length 400 loses to a four-edge route of length 40. Ordering by cost instead of hop count is exactly what Dijkstra's priority queue provides.
</details>

**3.8** A colleague's greedy coin-change works for their test currency and fails in production. Diagnose it.

<details><summary>Answer</summary>

Greedy correctness is a property of the **coin system**, not the code. With 1/5/10/25 the greedy choice is provably safe; with a system like 1/3/4 it is not — greedy makes 6 as 4+1+1 where 3+3 is optimal. Nothing in the algorithm changed, only the input's structure. The fix is dynamic programming, which considers all combinations.
</details>

**3.9** Why is quicksort's worst case triggered by *sorted* input, of all things?

<details><summary>Answer</summary>

With a last-element (or first-element) pivot on sorted data, the pivot is always the largest (or smallest) value present. One partition is empty and the other holds `n−1` elements, so recursion depth is `n` instead of `log n` — `O(n²)`. Sorted input is common and often attacker-controllable, which is why every real implementation randomises the pivot or uses median-of-three.
</details>

**3.10** Explain why amortised `O(1)` for dynamic-array append is genuinely `O(1)` and not a trick.

<details><summary>Answer</summary>

Doubling means the `k`-th resize copies `2^k` elements but is preceded by `2^k` free appends. Summing across `n` appends, total copying is `1 + 2 + 4 + … + n < 2n` — linear total work for `n` operations, so `O(1)` each on average. It is a genuine bound on the *sequence*, though any single append can still spike to `O(n)`, which matters for latency-sensitive code.
</details>

**3.11** DFS uses less memory than BFS on some graphs and more on others. When, and why?

<details><summary>Answer</summary>

DFS holds one root-to-current path: `O(depth)`. BFS holds an entire frontier: `O(width)`. On a **wide, shallow** graph DFS wins by a large margin. On a **deep, narrow** graph BFS wins, and recursive DFS additionally risks a stack overflow — which is a crash, not a slowdown.
</details>

**3.12** Why can Dijkstra not simply be patched to handle negative weights by re-checking settled nodes?

<details><summary>Answer</summary>

You can — and that algorithm is **Bellman-Ford**, which relaxes every edge `V−1` times at `O(V·E)`. The point is that the patch destroys exactly what makes Dijkstra fast: settling a node permanently after one extraction. Once you allow revisits, the priority-queue optimisation no longer buys anything.
</details>

**3.13** Naive Fibonacci is `O(2ⁿ)` yet computes only `n` distinct values. Reconcile that.

<details><summary>Answer</summary>

It computes those `n` distinct values an exponential number of *times*. Each call spawns two more with nothing remembering earlier results, so the call tree has `~2ⁿ` nodes while containing only `n` distinct answers. That gap between distinct subproblems and total calls is precisely what memoisation eliminates, and precisely the signal that a problem is a DP problem.
</details>

**3.14** You profile a "fast `O(1)`" hash lookup and it loses to an `O(n)` scan of a 20-element array. Explain.

<details><summary>Answer</summary>

Constants. The hash lookup must compute a hash (potentially over a long string key), take a modulo, follow a pointer into a scattered bucket, and compare the full key. The 20-element scan fits in one or two cache lines and does 20 trivial comparisons with no indirection. `O(1)` bounds *growth*, not absolute cost — at `n = 20` you are nowhere near where growth matters.
</details>

**3.15** Every complexity row in the BST module says "height". What is the actual design lesson?

<details><summary>Answer</summary>

That a plain BST **has no complexity of its own** — it inherits whatever height your insertion order produced, from `log n` to `n`. Advertised performance that depends on caller-controlled input is not a guarantee. Self-balancing trees exist to convert that hope into a bound, and the same lesson recurs in hash tables (randomised seeds) and quicksort (randomised pivots): where an adversary controls the input, remove their leverage.
</details>

---

## Scoring

| Score | Reading |
|:--|:--|
| **40–45** | You have the material. Go build something with it. |
| **30–39** | Solid. Re-read the modules behind your misses — they cluster. |
| **20–29** | You know the structures but not yet the trade-offs. Level 3 is where to focus. |
| **under 20** | Work back through the modules in order with the [flashcards](flashcards.md); they are built for exactly this. |

---

⬅️ [🃏 Flashcards](flashcards.md) · [🏠 Index](../README.md) · [00 · How to read this](00-how-to-read-this.md) ➡️
