<div align="center">

# Learn Data Structures & Algorithms — Visually

**Eighteen modules. Thirty-eight animations. Zero dependencies.**

A GitHub-native course that teaches data structures the way the video does: one real-world analogy, one animation, then the costs — with the pictures doing the explaining.

Every operation is a small, real Python function — extracted from [`examples/`](examples/) and covered by a 156-test suite.

[![Modules](https://img.shields.io/badge/modules-18-38bdf8?style=flat-square)](docs/)
[![Animations](https://img.shields.io/badge/animated_SVGs-38-fbbf24?style=flat-square)](assets/anim/)
[![Blueprints](https://img.shields.io/badge/blueprints-18-c084fc?style=flat-square)](assets/blueprint/)
[![Flashcards](https://img.shields.io/badge/flashcards-108-34d399?style=flat-square)](docs/flashcards.md)
[![Tests](https://img.shields.io/badge/tested_Python-156_tests-38bdf8?style=flat-square)](examples/test_ops.py)
[![Quiz](https://img.shields.io/badge/quiz-45_questions-fb7185?style=flat-square)](docs/quiz.md)
[![Verify](https://github.com/rajeshgoyalg/Learn-Data-Structures-and-Algorithms-Visually/actions/workflows/verify.yml/badge.svg)](https://github.com/rajeshgoyalg/Learn-Data-Structures-and-Algorithms-Visually/actions/workflows/verify.yml)
[![Dependencies](https://img.shields.io/badge/dependencies-none-64748b?style=flat-square)](#no-dependencies)
[![License](https://img.shields.io/badge/license-MIT-94a3b8?style=flat-square)](LICENSE)

</div>

---

![The whole course on one sheet](assets/infographic/course-map.svg)

---

## Start here

| | |
|:--|:--|
| 🧭 **New?** | [00 · How to read this repo](docs/00-how-to-read-this.md) — the colour legend and the notation, in two minutes |
| 🎓 **Ready?** | [01 · Foundations](docs/01-foundations.md) — then work straight through |
| ⚡ **In a hurry?** | [📋 Complexity cheat sheet](docs/cheatsheet-complexity.md) and the [structure chooser](assets/infographic/structure-chooser.svg) |
| 🧪 **Revising?** | [🃏 108 flashcards](docs/flashcards.md) · [❓ 45-question quiz](docs/quiz.md) |

---

## The learning path

```mermaid
flowchart TD
  F["01 · Foundations — complexity"]

  subgraph LIN["Linear structures"]
    direction LR
    A["02 Arrays"] --> L["03 Linked lists"] --> V["04 Doubly & circular"]
  end

  subgraph RES["Restricted access"]
    direction LR
    S["05 Stacks"] --> Q["06 Queues"]
  end

  subgraph KEY["Keyed structures"]
    direction LR
    H["07 Hash tables"] --> E["08 Sets"]
  end

  subgraph HIER["Hierarchical structures"]
    direction LR
    P["09 Heaps"] --> B["10 BSTs"] --> T["11 Balanced trees"] --> R["12 Tries"] --> G["13 Graphs"]
  end

  subgraph ALGO["Searching & sorting"]
    direction LR
    SE["14 Searching"] --> SO["15 Sorting"]
  end

  subgraph TECH["Techniques & paradigms"]
    direction LR
    RE["16 Recursion"] --> PA["17 Paradigms"] --> DJ["18 Dijkstra"]
  end

  F --> LIN --> RES --> KEY --> HIER --> ALGO --> TECH

  classDef found fill:#0f2438,stroke:#e2e8f0,stroke-width:2px,color:#e2e8f0
  classDef lin fill:#0f2438,stroke:#38bdf8,color:#38bdf8
  classDef res fill:#0f2438,stroke:#fbbf24,color:#fbbf24
  classDef key fill:#0f2438,stroke:#34d399,color:#34d399
  classDef hier fill:#0f2438,stroke:#c084fc,color:#c084fc
  classDef algo fill:#0f2438,stroke:#fb7185,color:#fb7185
  class F found
  class A,L,V lin
  class S,Q res
  class H,E key
  class P,B,T,R,G hier
  class SE,SO,RE,PA,DJ algo
```

Each module leans on the one before it. Modules 14–18 reuse the structures you built in 02–13.

---

## The modules

### 🧱 Foundations

| # | Module | The analogy | Headline |
|:--:|:--|:--|:--|
| 00 | [How to read this repo](docs/00-how-to-read-this.md) | the legend on a map | colours, notation, structure |
| 01 | [Foundations](docs/01-foundations.md) | two people racing through a phone book | `O(1)` → `O(2ⁿ)` |

### 📏 Linear structures

| # | Module | The analogy | Headline |
|:--:|:--|:--|:--|
| 02 | [Arrays](docs/02-arrays.md) | a street of numbered houses | `O(1)` access, `O(n)` insert |
| 03 | [Linked lists](docs/03-linked-lists.md) | a treasure hunt of clues | `O(n)` access, `O(1)` insert |
| 04 | [Doubly & circular lists](docs/04-doubly-and-circular-lists.md) | a one-way street, then a roundabout | `O(1)` delete by reference |

### 🚦 Restricted access

| # | Module | The analogy | Headline |
|:--:|:--|:--|:--|
| 05 | [Stacks](docs/05-stacks.md) | a pile of plates | LIFO, everything `O(1)` |
| 06 | [Queues](docs/06-queues.md) | a checkout line, then a hospital triage | FIFO, everything `O(1)` |

### 🔑 Keyed structures

| # | Module | The analogy | Headline |
|:--:|:--|:--|:--|
| 07 | [Hash tables](docs/07-hash-tables.md) | a cloakroom ticket | `O(1)` average, no order |
| 08 | [Sets](docs/08-sets.md) | a guest list at the door | `O(1)` membership |

### 🌳 Hierarchical structures

| # | Module | The analogy | Headline |
|:--:|:--|:--|:--|
| 09 | [Heaps](docs/09-heaps.md) | a company where managers earn least | `O(1)` peek, `O(log n)` extract |
| 10 | [Binary search trees](docs/10-binary-search-trees.md) | twenty questions | `O(log n)` — if balanced |
| 11 | [Balanced trees](docs/11-balanced-trees.md) | a librarian who straightens the shelf | `O(log n)` **guaranteed** |
| 12 | [Tries](docs/12-tries.md) | a filing cabinet by letter | `O(L)`, prefix queries |
| 13 | [Graphs](docs/13-graphs.md) | a map of friendships | `O(V+E)` traversal |

### ⚙️ Algorithms & paradigms

| # | Module | The analogy | Headline |
|:--:|:--|:--|:--|
| 14 | [Searching](docs/14-searching.md) | a loose pile of pages vs a bound book | `O(n)` vs `O(log n)` |
| 15 | [Sorting](docs/15-sorting.md) | five people, one shuffled deck | `O(n²)` vs `O(n log n)` |
| 16 | [Recursion & backtracking](docs/16-recursion-and-backtracking.md) | Russian dolls | `O(depth)` space is real |
| 17 | [Paradigms](docs/17-paradigms.md) | three ways to cross a country | greedy / D&C / DP |
| 18 | [Dijkstra](docs/18-dijkstra.md) | a road atlas with distances | `O((V+E) log V)` |

### 📚 Revision

| Sheet | What it is |
|:--|:--|
| [📋 Complexity cheat sheet](docs/cheatsheet-complexity.md) | every structure and algorithm, one page |
| [🃏 Flashcards](docs/flashcards.md) | all 108 cards, grouped by module |
| [❓ Quiz bank](docs/quiz.md) | 45 questions across three difficulty levels |

---

## The animation gallery

Every operation in the course, animated. All 38 loop with a pause at the start and end so you can read the state.

<details open><summary><b>📏 Linear structures — 8 animations</b></summary>

| | |
|:--|:--|
| ![](assets/anim/array-index-lookup.svg) | ![](assets/anim/array-insert-shift.svg) |
| ![](assets/anim/array-dynamic-resize.svg) | ![](assets/anim/linked-list-traverse.svg) |
| ![](assets/anim/linked-list-insert.svg) | ![](assets/anim/linked-list-delete.svg) |
| ![](assets/anim/doubly-linked-list.svg) | ![](assets/anim/circular-linked-list.svg) |

</details>

<details><summary><b>🚦 Stacks & queues — 5 animations</b></summary>

| | |
|:--|:--|
| ![](assets/anim/stack-push-pop.svg) | ![](assets/anim/queue-enqueue-dequeue.svg) |
| ![](assets/anim/circular-queue-wrap.svg) | ![](assets/anim/deque-both-ends.svg) |
| ![](assets/anim/priority-queue.svg) | |

</details>

<details><summary><b>🔑 Hashing & sets — 3 animations</b></summary>

| | |
|:--|:--|
| ![](assets/anim/hash-function-bucket.svg) | ![](assets/anim/hash-collision-chaining.svg) |
| ![](assets/anim/set-dedupe.svg) | |

</details>

<details><summary><b>🌳 Trees & graphs — 9 animations</b></summary>

| | |
|:--|:--|
| ![](assets/anim/heap-sift-up.svg) | ![](assets/anim/heap-sift-down.svg) |
| ![](assets/anim/bst-search.svg) | ![](assets/anim/bst-insert.svg) |
| ![](assets/anim/avl-rotation.svg) | ![](assets/anim/red-black-recolor.svg) |
| ![](assets/anim/trie-prefix-walk.svg) | ![](assets/anim/graph-bfs.svg) |
| ![](assets/anim/graph-dfs.svg) | |

</details>

<details><summary><b>⚙️ Algorithms — 13 animations</b></summary>

| | |
|:--|:--|
| ![](assets/anim/linear-search.svg) | ![](assets/anim/binary-search.svg) |
| ![](assets/anim/bubble-sort.svg) | ![](assets/anim/selection-sort.svg) |
| ![](assets/anim/insertion-sort.svg) | ![](assets/anim/merge-sort.svg) |
| ![](assets/anim/quick-sort-partition.svg) | ![](assets/anim/recursion-call-stack.svg) |
| ![](assets/anim/backtracking-n-queens.svg) | ![](assets/anim/divide-and-conquer.svg) |
| ![](assets/anim/dp-table-fill.svg) | ![](assets/anim/greedy-coin-change.svg) |
| ![](assets/anim/dijkstra-relax.svg) | |

</details>

---

## Reference sheets

<details><summary><b>📊 The six infographics</b></summary>

| Sheet | What it answers |
|:--|:--|
| ![](assets/infographic/big-o-growth.svg) | how the growth curves actually diverge |
| ![](assets/infographic/operation-cost-matrix.svg) | every structure against every operation |
| ![](assets/infographic/structure-chooser.svg) | which structure for which question |
| ![](assets/infographic/memory-layouts.svg) | contiguous vs linked vs hierarchical |
| ![](assets/infographic/traversal-orders.svg) | four ways to read one tree |
| ![](assets/infographic/course-map.svg) | the whole course on one sheet |

</details>

Eighteen **blueprints** — one static engineering drawing per module — live in [`assets/blueprint/`](assets/blueprint/) and are embedded in their modules.

---

## No dependencies

This repo has no build step, no package manager, no JavaScript and no external assets.

- Every animation is a **plain `.svg` file** with CSS `@keyframes` written inside it.
- They render identically on GitHub, in an offline clone, and in the Pages gallery.
- Mermaid diagrams use `flowchart` syntax, which GitHub renders natively.
- Clone it and open `index.html` in any browser — or just read the markdown.

Twenty repository invariants are checked by `tools/verify.py` (stdlib only, no install) and run in CI on every push — see [CONTRIBUTING](CONTRIBUTING.md).

```bash
git clone <this-repo>
cd Learn-Data-Structures-and-Algorithms-Visually
open index.html          # the gallery; or start at docs/00-how-to-read-this.md
```

---

## Credit

This repo follows the curriculum of **[Learn Data Structures and Algorithms Visually – Crash Course](https://www.youtube.com/watch?v=RpLnQnurpLY)** by **Sumit Saha**, published on the [freeCodeCamp.org](https://www.freecodecamp.org/news/learn-data-structures-and-algorithms-visually/) YouTube channel. The analogy-first approach is theirs; the diagrams, prose, pseudocode and exercises here are original work built to match it.

Licensed [MIT](LICENSE). Corrections and additional modules welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
