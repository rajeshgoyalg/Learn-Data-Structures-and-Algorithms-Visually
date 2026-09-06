# 00 · How to read this repo

Every module in this repo is built from the same eleven blocks, in the same order. Learn the notation once here and the other seventeen modules read themselves.

---

## The visual legend

Colour means the same thing in all 62 diagrams. Nothing is decorative.

| Colour | Role | Where you see it |
|:--|:--|:--|
| 🟦 **Cyan** `#38bdf8` | the structure at rest | boxes, nodes, edges, pointers |
| 🟨 **Amber** `#fbbf24` | active right now | the cursor, the current comparison, the pivot, the item in flight |
| 🟩 **Green** `#34d399` | settled or succeeded | found, sorted, visited, final position, a new correct link |
| 🟥 **Rose** `#fb7185` | rejected or removed | failed comparison, deleted node, illegal state, the expensive case |
| 🟪 **Violet** `#c084fc` | a secondary pointer | `prev` in a doubly linked list, the hash function, the DFS stack |
| ⬜ **Slate** `#94a3b8` | labels, dimensions, notes | axis text, callouts, free slots |

Two shape conventions:

- **Dashed outline** = allocated but empty (spare array capacity, a free ring slot).
- **Double ring** = a terminal state (end of a word in a trie, a settled node).

---

## The three kinds of picture

| Kind | Folder | What it does |
|:--|:--|:--|
| 🎞️ **Animation** | `assets/anim/` | shows the operation *happening*, on a loop, with a caption per step |
| 📐 **Blueprint** | `assets/blueprint/` | a static engineering drawing: anatomy, labelled parts, costs, trade-offs |
| 📊 **Infographic** | `assets/infographic/` | cross-module comparison — the growth curves, the cost matrix, the chooser |

All three are plain SVG with the animation written in CSS inside the file. There is no JavaScript, no build step and no dependency: the pictures work on GitHub, in an offline clone, and in the Pages gallery identically.

> **Animations loop with a deliberate pause** at the first and last frame so you can read the start and end state before it restarts. If you catch one mid-cycle, wait a few seconds.

---

## The pseudocode dialect

This repo uses **no real programming language on purpose** — the video it follows teaches the idea, not the syntax. One dialect is used everywhere:

```text
function name(argument, argument)
    x ← 5                       assignment
    if condition then
        ...
    else
        ...
    end
    while condition do ... end
    for each item in collection do ... end
    for i ← 0 to n-1 do ... end
    return value

A ← B                           A now refers to what B refers to
A.next ← B                      write to a field
swap(a, b)                      exchange two values
null                            "points at nothing"
```

**Indexing is 0-based** throughout, matching every diagram: the first element of a 7-element array is at index `0`, the last at index `6`.

---

## The eleven blocks in every module

| # | Block | What to do with it |
|:--:|:--|:--|
| 1 | **The analogy** | read it first — it is the hook the rest hangs on |
| 2 | 🎞️ **Animation** | watch one full loop before reading anything else |
| 3 | 🧠 **Mental model** | the analogy mapped term-by-term onto the real structure |
| 4 | 📐 **Blueprint** | the same thing again, but static and fully labelled |
| 5 | 🗺️ **Mindmap** | the shape of the module, so you know what is coming |
| 6 | ⚙️ **Operations** | pseudocode, one block per operation |
| 7 | ⏱️ **Complexity** | best / average / worst / space, with the *reason* |
| 8 | ⚖️ **Trade-offs** | when to reach for it and when not to |
| 9 | 🃏 **Flashcards** | click to reveal — test yourself before moving on |
| 10 | ❓ **Quiz** | four or five questions, answers hidden with explanations |
| 11 | 🔗 **Navigation** | previous / index / next |

---

## Suggested route

1. **[01 · Foundations](01-foundations.md)** — non-negotiable. Everything later is priced in this notation.
2. Modules **02 → 13** in order. Each one leans on the one before it.
3. Modules **14 → 18**, the algorithms. These reuse the structures you just built.
4. **[Cheat sheet](cheatsheet-complexity.md)**, **[flashcards](flashcards.md)** and **[quiz](quiz.md)** for revision.

If you only have twenty minutes: read [01 · Foundations](01-foundations.md), then the **[cost matrix](../assets/infographic/operation-cost-matrix.svg)** and the **[structure chooser](../assets/infographic/structure-chooser.svg)**.

---

⬅️ *(start)* · [🏠 Index](../README.md) · [01 · Foundations](01-foundations.md) ➡️
