# 🃏 Flashcard deck — all 18 modules

The full deck, gathered from every module. Read the question, answer it **out loud or on paper**, then click to check. Getting it wrong is the useful part.

**How to use this:** work one section at a time, immediately after reading its module. Come back a day later and do the same section again — the second pass is where it sticks.

| Section | Cards |
|:--|--:|
| [Foundations](#foundations) | 6 |
| [Arrays](#arrays) | 6 |
| [Linked lists](#linked-lists) | 6 |
| [List variants](#list-variants) | 5 |
| [Stacks](#stacks) | 6 |
| [Queues](#queues) | 6 |
| [Hash tables](#hash-tables) | 6 |
| [Sets](#sets) | 6 |
| [Heaps](#heaps) | 6 |
| [Binary search trees](#binary-search-trees) | 6 |
| [Balanced trees](#balanced-trees) | 6 |
| [Tries](#tries) | 6 |
| [Graphs](#graphs) | 6 |
| [Searching](#searching) | 6 |
| [Sorting](#sorting) | 7 |
| [Recursion & backtracking](#recursion--backtracking) | 6 |
| [Paradigms](#paradigms) | 6 |
| [Dijkstra](#dijkstra) | 6 |
| **Total** | **108** |

---

## Foundations

<details><summary>Why does Big-O drop constants?</summary>
So the answer holds on any machine, in any language, in any year. Constants describe your hardware; the growth rate describes the algorithm.</details>

<details><summary>Worst case vs amortised?</summary>
Worst case is the most expensive single operation. Amortised is the average per operation across a long sequence. A dynamic array append is `O(n)` worst, `O(1)` amortised.</details>

<details><summary>Is an O(n²) algorithm unusable?</summary>
Only at scale. `n = 50` is 2,500 operations — nothing. `n = 10⁶` is a trillion.</details>

<details><summary>Why is O(n log n) the comparison-sort floor?</summary>
There are `n!` orderings and each comparison yields one bit, so you need `log₂(n!) = Θ(n log n)` comparisons. It is information-theoretic, not an engineering limit.</details>

<details><summary>What does O(1) promise?</summary>
That cost does not grow with `n` — **not** that it is fast. An expensive hash is `O(1)` and can lose to scanning ten elements.</details>

<details><summary>What counts as space complexity?</summary>
Memory beyond the input. Merge sort `O(n)` (merge buffer), quicksort `O(log n)` (recursion stack), bubble sort `O(1)` (in place).</details>

---

## Arrays

<details><summary>Why is A[i] O(1) regardless of i?</summary>
It is arithmetic, not search: `base + i × itemSize`. Works only because elements are equal-sized and contiguous.</details>

<details><summary>What happens when a full dynamic array is appended to?</summary>
Allocate double, copy every element, free the old block, then write. That single append is `O(n)`.</details>

<details><summary>Why is appending still called O(1)?</summary>
Amortised. Doubling makes resizes rarer exactly as fast as they get costlier, so `n` appends total `O(n)`.</details>

<details><summary>Why does insertAt loop backwards?</summary>
Forwards would smear one value across the tail. Walking from the end moves each element into an already-vacated slot.</details>

<details><summary>Length vs capacity?</summary>
Length is how many you put in; capacity is how many the block could hold. The gap is the spare room that keeps appends cheap.</details>

<details><summary>Is a 2D array two-dimensional in memory?</summary>
No — one flat block with rows laid end to end. `grid[r][c]` = `base + (r × columns + c) × itemSize`.</details>

---

## Linked lists

<details><summary>Why can a linked list not be binary searched?</summary>
Reaching the middle costs `O(n)` hops, so you would pay `O(n)` per halving — `O(n log n)` total, worse than one scan.</details>

<details><summary>In insertAfter, why set fresh.next first?</summary>
`node.next` is the only reference to the rest of the list. Overwrite it first and the tail is orphaned.</details>

<details><summary>Can you delete a node given only a pointer to it?</summary>
Not properly in a singly linked list. The trick is copying the successor's data in and deleting the successor — which fails on the tail.</details>

<details><summary>Why is a linked list cache-hostile?</summary>
Nodes can be anywhere, so nearly every hop is a cache miss — often 100× slower than a hit. Arrays get several elements per fetch.</details>

<details><summary>What is a sentinel head node for?</summary>
A dummy node before the first real one, so the head is never null and every node has a predecessor — removing all front-of-list special cases.</details>

<details><summary>How do you detect a cycle in a linked list?</summary>
Floyd's tortoise and hare: advance one pointer by 1 and one by 2. They meet if and only if there is a cycle. `O(n)` time, `O(1)` space.</details>

---

## List variants

<details><summary>What does the prev pointer buy you?</summary>
`O(1)` deletion given only a node reference, and `O(n)` backward traversal. Cost: one pointer per node, one extra write per edit.</details>

<details><summary>Why is deleting a held node O(n) in a singly linked list?</summary>
You must set `predecessor.next`, and the only way to find the predecessor is to walk from the head.</details>

<details><summary>What terminates a circular list traversal?</summary>
Returning to the start: `until current = head`. There is no null anywhere in a circular list.</details>

<details><summary>How does an LRU cache use a circular doubly linked list?</summary>
A hash map points at nodes; the list holds usage order. On a hit, unlink and re-insert at the front — `O(1)` only because of `prev`. Eviction removes the tail.</details>

<details><summary>How many pointers change deleting a middle node of a doubly linked list?</summary>
Two: the predecessor's `next` and the successor's `prev`. Endpoints need extra care.</details>

---

## Stacks

<details><summary>What does LIFO mean and why is it useful?</summary>
Last In, First Out. It is a memory of nesting: the last thing you started is the first thing you must finish.</details>

<details><summary>Array-backed or list-backed stack?</summary>
Array: faster, cache-friendly, lower overhead, but must be grown. List: no capacity limit or resize spike, but a pointer per node. Array by default.</details>

<details><summary>Why does pop not erase the value?</summary>
Nothing can reach it — `top` has moved below it and the next push overwrites it. (In GC languages you may null it so the object can be collected.)</details>

<details><summary>What causes a stack overflow in a real program?</summary>
Too many pending call frames — a missing base case, or legitimate recursion deeper than the fixed call stack allows.</details>

<details><summary>How do you check balanced brackets with a stack?</summary>
Push every opener; on a closer, pop and check it matches. Popping empty, or a non-empty stack at the end, means unbalanced.</details>

<details><summary>Can you build a queue from two stacks?</summary>
Yes. Push onto A. To dequeue, if B is empty pour all of A into B (reversing the order), then pop B. Amortised `O(1)`.</details>

---

## Queues

<details><summary>Why does a linear array queue fill up with free slots left?</summary>
`front` and `rear` only increase, so once `rear` hits the last index the queue refuses items even though the space before `front` is free.</details>

<details><summary>What does the modulo do in a circular queue?</summary>
Maps index `capacity` back to 0 so indices cycle. `(rear + 1) mod capacity` is the entire difference from a linear queue.</details>

<details><summary>Why is front = rear ambiguous in a circular queue?</summary>
It is true both when empty and when full. Fix it with an explicit `count`, or by always leaving one slot unused.</details>

<details><summary>A deque is which two structures at once?</summary>
A stack and a queue. Restrict to one end for a stack; push back and pop front for a queue.</details>

<details><summary>Why is priority queue insertion O(log n)?</summary>
It must restore the heap ordering by sifting the new item up, and the height of a complete binary tree is `log n`.</details>

<details><summary>Which structure makes BFS breadth-first?</summary>
The queue. It forces every node at distance `k` to be processed before any at `k+1`. Swap it for a stack and the same code becomes DFS.</details>

---

## Hash tables

<details><summary>What three properties must a hash function have?</summary>
Deterministic, uniform (scatters similar keys apart), and fast. Lose determinism and lookups fail; lose uniformity and you get long chains.</details>

<details><summary>Is a collision a bug?</summary>
No — more possible keys than buckets makes them unavoidable (pigeonhole). Hash tables are designed around them; only *too many* is a problem.</details>

<details><summary>Chaining vs open addressing?</summary>
Chaining: a list per bucket — simple, tolerates high load, costs pointers. Open addressing: probe for a free slot — cache-friendly, but degrades near full and needs tombstones on delete.</details>

<details><summary>What is the load factor and why 0.75?</summary>
`entries / buckets`. Below ~0.75 collisions stay rare; above it chains lengthen fast. It is the conventional compromise between memory waste and collision rate.</details>

<details><summary>Why does resizing require rehashing everything?</summary>
The index is `hash mod capacity`. Change the capacity and nearly every key maps somewhere new, so every entry must be relocated — `O(n)`.</details>

<details><summary>Why can a hash table not do range queries?</summary>
A good hash deliberately destroys key relationships — 10 and 11 land in unrelated buckets. Ordering is what you traded away for `O(1)`.</details>

---

## Sets

<details><summary>How does a set relate to a hash table?</summary>
A hash set is a hash table storing only keys. Every characteristic carries over: `O(1)` average, `O(n)` worst, no ordering, load factor, rehashing.</details>

<details><summary>What happens adding an element already present?</summary>
Nothing, silently. That no-op is what makes de-duplication free — you never have to check first.</details>

<details><summary>Why does set de-duplication beat nested loops?</summary>
Nested loops are `O(n²)`. A set answers "seen this?" in `O(1)`, so one pass is `O(n)`. At `n = 10,000` that is 10⁸ versus 10⁴.</details>

<details><summary>Intersecting two sets — which do you iterate?</summary>
The smaller, probing the larger. Probes are `O(1)`, so the loop count is the whole cost: `O(min(|A|,|B|))`.</details>

<details><summary>What does a sorted set give you that a hash set cannot?</summary>
Ordered iteration, `O(log n)` min/max, and range queries. The price is `O(log n)` instead of `O(1)` everywhere.</details>

<details><summary>When is a bitset the right answer?</summary>
Integers from a small dense known range. Membership is one bit test; union/intersection are bitwise ops across 64-bit words.</details>

---

## Heaps

<details><summary>Is a heap sorted?</summary>
No. Only parent-to-child is constrained; siblings are unordered. `[2, 5, 8, 9, 7]` is a valid min-heap.</details>

<details><summary>Why does a heap need no pointers?</summary>
It is a **complete** tree, so there are no gaps and level-order position maps exactly onto array index. `parent`/`left`/`right` become arithmetic.</details>

<details><summary>Why is the last leaf moved to the root on extract?</summary>
It is the only removal that cannot leave a hole in the middle, preserving completeness. `siftDown` then repairs the value.</details>

<details><summary>Why swap with the smaller child in a min-heap?</summary>
The promoted child becomes the parent of the other. Only the smaller is guaranteed ≤ its new sibling; the larger would break the property immediately.</details>

<details><summary>Why is build-heap O(n), not O(n log n)?</summary>
`siftDown` costs the height *below* a node, and the tree is bottom-heavy: half the nodes are leaves costing 0. The series converges to `O(n)`.</details>

<details><summary>Top 5 of a 10-million-item stream?</summary>
A min-heap of size 5. Push if under 5, else replace the root when the item beats it. `O(n log 5)` time, `O(5)` memory.</details>

---

## Binary search trees

<details><summary>State the BST invariant precisely.</summary>
For every node, **every** value in the left subtree is smaller and **every** value in the right subtree is larger — a claim about whole subtrees, which is what licenses discarding a branch unexamined.</details>

<details><summary>What does in-order traversal produce?</summary>
The values in sorted ascending order, always. It is also the cleanest way to verify a BST.</details>

<details><summary>How does a BST degenerate?</summary>
Sorted insertion order. Each value becomes the right child of the last, producing a linked list — height `n`, everything `O(n)`.</details>

<details><summary>Deleting a node with two children — what replaces it?</summary>
Its in-order successor (minimum of the right subtree), or symmetrically its predecessor. Only those preserve the invariant.</details>

<details><summary>Where are the min and max?</summary>
Leftmost and rightmost node respectively. Both `O(height)`.</details>

<details><summary>BST or hash table?</summary>
Hash table for exact-match only — `O(1)` beats `O(log n)`. BST the moment you need order: sorted iteration, min/max, ranges. Those are impossible in a hash table.</details>

---

## Balanced trees

<details><summary>What problem do balanced trees solve?</summary>
BST degeneracy. They make `O(log n)` a guarantee rather than a hope about insertion order.</details>

<details><summary>What is a balance factor?</summary>
`height(left) − height(right)`. AVL keeps it in {−1, 0, +1} and rotates the moment it reaches ±2.</details>

<details><summary>What does a rotation cost, and can it break the ordering?</summary>
`O(1)` — three pointer writes. It cannot break the invariant: the subtree that changes parents was already between the two rotated nodes in value.</details>

<details><summary>Why do LR and RL need two rotations?</summary>
A single rotation only fixes a straight lean. A zig-zag must first be rotated into a straight lean at the child.</details>

<details><summary>Why are new red-black nodes red?</summary>
A black node would break the equal-black-height rule on every path through it. A red one can only break "no red child of a red parent" — a local, cheaply repaired violation.</details>

<details><summary>Which do standard libraries use?</summary>
Red-black, almost universally. Its deletion rebalancing is capped at 3 rotations versus AVL's `O(log n)`, making write performance predictable.</details>

---

## Tries

<details><summary>Where are the characters stored?</summary>
On the **edges**. A node represents the prefix formed by the path to it, and carries only its children map and `isEndOfWord`.</details>

<details><summary>Why is lookup independent of the number of stored words?</summary>
You follow one edge per query character and look at nothing else. Ten words or ten million, "cat" is three hops.</details>

<details><summary>What does isEndOfWord distinguish?</summary>
A prefix from a complete word. After inserting "cat", the "ca" node exists but is not a word.</details>

<details><summary>Memory cost of inserting "car" when "cat" exists?</summary>
One node. The `c` and `a` are shared — prefix storage is paid for once.</details>

<details><summary>Why can deletion not just unlink nodes?</summary>
Those nodes may be on the path to other words. Unset the flag; prune only if the node has no children and is not itself a word end.</details>

<details><summary>What is a compressed trie (radix tree)?</summary>
Any chain of single-child nodes is collapsed into one edge labelled with the whole substring — far less memory and pointer-chasing, same prefix operations.</details>

---

## Graphs

<details><summary>What single change turns BFS into DFS?</summary>
Replacing the queue with a stack. FIFO explores by distance; LIFO explores by depth.</details>

<details><summary>Why does every traversal need a visited set?</summary>
Cycles. Without it the traversal never terminates, and it is also what caps total work at `O(V+E)`.</details>

<details><summary>Adjacency list or matrix?</summary>
List for sparse graphs (nearly all real ones): `O(V+E)` space. Matrix for dense graphs or constant single-edge tests, where `O(1)` adjacency beats `O(V²)` memory.</details>

<details><summary>Why does BFS only find shortest paths on unweighted graphs?</summary>
It expands by number of edges. With weights, fewest edges is not cheapest — a 2-edge path costing 100 loses to a 5-edge path costing 10.</details>

<details><summary>How does DFS detect a cycle in a directed graph?</summary>
Three states. Reaching a node still marked IN_PROGRESS means a back edge into your own active path. A DONE node is harmless.</details>

<details><summary>What is a DAG and why does it matter?</summary>
Directed, acyclic. It is the shape of dependencies, and it can be topologically sorted into a valid order. A cycle means no order exists — that *is* your circular-dependency error.</details>

---

## Searching

<details><summary>What is the one precondition for binary search?</summary>
Sorted data **with random access**. Sorted so a comparison tells you which half to drop; random access so reaching the middle is `O(1)`.</details>

<details><summary>Why lo + (hi − lo)/2 rather than (lo + hi)/2?</summary>
`lo + hi` can overflow a fixed-width integer, producing a negative index. The alternative is algebraically identical and never exceeds `hi`.</details>

<details><summary>Binary search on a linked list — why not?</summary>
Reaching the middle is `O(n)` instead of `O(1)`, making the total `O(n log n)` — worse than a single scan.</details>

<details><summary>When does linear search beat binary search?</summary>
On unsorted data (binary search does not apply), on very small arrays, when the target is usually near the front, and on any structure without random access.</details>

<details><summary>Hash lookup is O(1). Why ever binary search?</summary>
Because a hash table has no order. Binary search needs zero extra memory and generalises to `lowerBound` — range queries, nearest-neighbour, "first record after this date".</details>

<details><summary>What does lowerBound return when the target is absent?</summary>
The index where it would be inserted to keep the array sorted — the first position holding a value not less than the target.</details>

---

## Sorting

<details><summary>What does stable mean, with a consequence?</summary>
Equal elements keep their input order. Sort by name, then stably by department, and each department stays name-sorted. An unstable sort destroys the first pass.</details>

<details><summary>Why is quicksort usually faster than merge sort?</summary>
It sorts in place with excellent cache locality and a small constant. Merge sort copies through an `O(n)` buffer at every level.</details>

<details><summary>What triggers quicksort's O(n²)?</summary>
Consistently extreme pivots. A sorted array with a last-element pivot does it exactly. Randomising the pivot makes it negligible.</details>

<details><summary>Why is insertion sort still used in production?</summary>
`O(n)` on nearly-sorted data with tiny constants. Hybrids switch to it below ~16–32 elements.</details>

<details><summary>Why is O(n log n) the comparison-sort floor?</summary>
`n!` orderings, one bit per comparison, so at least `log₂(n!) = Θ(n log n)` comparisons are required.</details>

<details><summary>How can counting sort be O(n)?</summary>
It never compares. It counts occurrences and rebuilds the output — only possible for integer keys in a bounded range, at a cost of `O(n + k)`.</details>

<details><summary>Selection sort is always O(n²). Why use it?</summary>
It performs exactly `n−1` swaps — the fewest here. It matters when writes are far costlier than reads (wear-limited flash, very large records).</details>

---

## Recursion & backtracking

<details><summary>What three parts does every correct recursive function need?</summary>
Base case, recursive case, and progress. Missing the base case loops forever; missing progress loops forever despite having one.</details>

<details><summary>What causes a stack overflow?</summary>
Too many simultaneously pending frames — non-termination, or legitimate depth beyond the fixed call stack. Frames are real memory.</details>

<details><summary>What single line separates backtracking from brute force?</summary>
The **undo** after the recursive call. It lets you abandon a partial solution the instant it is illegal, discarding all its completions unexamined.</details>

<details><summary>Why is naive recursive fibonacci O(2ⁿ)?</summary>
It recomputes the same values independently in separate branches. The subproblems overlap — the signal to memoise.</details>

<details><summary>Is recursion always convertible to iteration?</summary>
Always. Tail recursion becomes a loop; general recursion becomes a loop plus an explicit stack.</details>

<details><summary>Why does DFS have a natural recursive form but BFS not?</summary>
DFS's order *is* the call stack's order. BFS needs a queue, and the call stack is not a queue.</details>

---

## Paradigms

<details><summary>Divide & conquer vs dynamic programming?</summary>
Whether subproblems overlap. D&C splits into independent pieces where caching gains nothing; DP applies when the same subproblem recurs.</details>

<details><summary>Memoisation vs tabulation?</summary>
Both DP. Memoisation is top-down — natural recursion plus a cache, computing only needed states. Tabulation is bottom-up — fill a table in dependency order, no recursion depth risk.</details>

<details><summary>What two conditions does DP require?</summary>
Overlapping subproblems and optimal substructure. Without overlap caching is pointless; without optimal substructure the cached sub-answers are unusable.</details>

<details><summary>Coins 1, 3, 4 and target 6 — what does greedy do?</summary>
Takes 4 + 1 + 1 = three coins. The optimum is 3 + 3 = two. Greedy correctness is a property of the problem, not the algorithm.</details>

<details><summary>Why is Dijkstra a correct greedy algorithm?</summary>
With non-negative weights, the cheapest unsettled distance is provably final — no later path can undercut it. Add a negative edge and the proof collapses.</details>

<details><summary>DP turned O(2ⁿ) into O(n). What did it cost?</summary>
Memory — `O(n)` for the table. DP is the canonical time-for-space trade, and the space is sometimes reducible afterwards.</details>

---

## Dijkstra

<details><summary>What is edge relaxation?</summary>
`if dist[u] + w(u,v) < dist[v]` then update `dist[v]` and `prev[v]`. Every step of Dijkstra is either a settle or a relaxation.</details>

<details><summary>Why always the cheapest unsettled node?</summary>
Its distance is provably final: any alternative route runs through another unsettled node that is already at least as expensive, and non-negative edges cannot reduce a total.</details>

<details><summary>What breaks with negative weights?</summary>
The finality argument. A settled node may later have a cheaper route found, and Dijkstra never revisits it — so it returns a wrong answer without erroring. Use Bellman-Ford.</details>

<details><summary>What is prev for?</summary>
Recording which node you arrived from, so the route can be reconstructed backwards from the target. Without it you get the distance but no path.</details>

<details><summary>Why is Dijkstra called greedy?</summary>
It takes the locally cheapest choice at every step and never reconsiders — but unlike most greedy algorithms that choice is provably globally safe, given non-negative weights.</details>

<details><summary>Dijkstra vs A*?</summary>
A\* adds a heuristic estimate of the remaining distance, so it explores toward the target rather than evenly outward. Dijkstra is A\* with a heuristic of zero.</details>

---

⬅️ [📋 Cheat sheet](cheatsheet-complexity.md) · [🏠 Index](../README.md) · [❓ Quiz](quiz.md) ➡️
