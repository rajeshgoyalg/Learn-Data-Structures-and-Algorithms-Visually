# Contributing

Corrections, clearer analogies and new modules are all welcome. The bar is: **does this make the concept land faster?**

---

## The rules that keep the repo coherent

### 1. No dependencies, ever

No build step, no package manager, no JavaScript, no CDN links, no external fonts. Every asset must render from a fresh `git clone` with nothing installed. This is not minimalism for its own sake — it is what lets the animations work identically on GitHub, offline and on Pages.

### 2. Animations are CSS inside the SVG

- Motion goes in a `<style>` block **inside the `.svg` file**, using `@keyframes` (or SMIL `<animate>`).
- **No `<script>`.** It will not run — GitHub renders SVGs in an `<img>` context, where scripts are inert.
- No external references of any kind: no webfonts, no linked images, no imported stylesheets.
- Give every file a `viewBox`, explicit `width`/`height`, a `<title>`, and an `aria-label`.
- Paint the panel background inside the file so it reads correctly in both GitHub themes.
- Keep files under ~30 KB.

### 3. The colour legend is a contract

Defined in [`docs/00-how-to-read-this.md`](docs/00-how-to-read-this.md) and used identically in all 62 assets:

| Colour | Meaning |
|:--|:--|
| `#38bdf8` cyan | the structure at rest |
| `#fbbf24` amber | active right now |
| `#34d399` green | settled / succeeded |
| `#fb7185` rose | rejected / removed |
| `#c084fc` violet | a secondary pointer |
| `#94a3b8` slate | labels and notes |

Do not introduce a new colour without also updating the legend and every asset that would now be inconsistent with it.

### 4. Frames must hard-cut, never cross-fade

Multi-step animations show one frame at a time. Two frames visible simultaneously produces unreadable double-exposed text. Keyframes should take a frame from opacity 1 straight to 0 at the exact percentage the next one appears.

Every loop also holds at its first and last frame so a reader can take in the start and end state.

### 5. Mermaid must be `flowchart`, not `mindmap`

**GitHub does not render Mermaid `mindmap` diagrams.** Mindmaps in this repo are written as `flowchart LR` with `classDef` styling, which renders everywhere. Do not "fix" them to `mindmap` syntax — it will silently produce a broken code block on GitHub.

### 6. Pseudocode explains; Python runs

Every operation is shown twice. The **pseudocode** is the explanation and stays language-neutral — the dialect is defined in [`docs/00-how-to-read-this.md`](docs/00-how-to-read-this.md): `←` for assignment, `function`/`end`, `for each … in`, 0-based indexing.

The **Python** is real code and lives in [`examples/`](examples/), never written directly into a module. `tools/sync_examples.py` extracts it into the doc between `<!-- python:... -->` markers:

```bash
python3 tools/sync_examples.py          # after changing an implementation
python3 tools/sync_examples.py --check  # report drift only
```

`tools/verify.py` fails if a doc block has drifted from its source, if a snippet is not valid Python, or if the test suite does not pass. So **edit `examples/`, then re-sync** — hand-editing a `python` block in a module will be caught and reverted.

Anything you add to `examples/` needs a test in `examples/test_examples.py`. Untested code in a teaching repo is worse than no code.

### 7. Every module has the same eleven blocks

Analogy → animation → mental model → blueprint → mindmap → operations → complexity → trade-offs → flashcards → quiz → navigation. A module missing a block will feel wrong next to the others. Copy the shape from [`docs/05-stacks.md`](docs/05-stacks.md) if you are starting a new one.

---

## Before you open a PR

```bash
python3 tools/verify.py
```

Twenty checks, stdlib only — no install, no build step. CI runs the identical
file on every push and pull request, so a green local run means a green PR.

It covers: SVG well-formedness, no `<script>` and no external references, the
`viewBox`/`<title>`/`aria-label` trio, text running past a canvas edge, legend
swatch alignment, blueprint title-block anchoring, body text running under a
title block, frame animations showing two
frames at once, internal links and anchors, the eleven-block module template,
unsupported Mermaid `mindmap` blocks, unclosed `<details>`, duplicate
flashcards, stated counts drifting from reality, orphaned assets, and gallery
links reverting to raw markdown. The last three cover the Python: every
snippet parses, no snippet has drifted from `examples/`, and the 76-test
suite passes.

The text-overflow check models the monospace advance at `0.60 × font-size` —
the same estimate the generator wraps with — so it catches text that never went
through the wrapper. It is not a rasterisation; exact metrics need a browser.

Then open `index.html` and confirm your animation actually plays and does not collide with any text at its edges. The validators check structure, not layout — only your eyes catch a caption overlapping a node.

---

## Writing style

- **Analogy first.** If you cannot state the concept as something physical in one sentence, the module is not ready.
- **Say why, not just what.** "Insert is `O(n)`" is a fact; "insert is `O(n)` *because the block has no gaps, so everything to the right must shift*" is an explanation.
- **Name the trap.** Every structure has one — the circular-list `null` check, the binary-search overflow, the greedy coin system. Those are the parts people actually get wrong.
- **Be honest about trade-offs.** Arrays often beat linked lists in practice despite worse Big-O. Say so.

---

## A note for forkers

`index.html` links to the module docs using absolute `github.com/.../blob/main/docs/...` URLs, not relative paths. That is deliberate: GitHub Pages serves a `.md` file as raw `text/markdown`, so a relative link from the gallery would show unrendered markdown — pipe tables, literal `**` and all. The blob URL renders properly.

The cost is that a fork's gallery still links to the upstream repo. If you fork this, run:

```bash
sed -i '' 's|github.com/rajeshgoyalg/Learn-Data-Structures-and-Algorithms-Visually|github.com/YOUR-USER/YOUR-REPO|g' index.html
```

The relative links inside `README.md` and `docs/*.md` are correct as they are — those are only ever read on github.com, where relative markdown links resolve and render.

---

## Adding a new module

1. Write `docs/NN-name.md` using the eleven-block template.
2. Add at least one animation to `assets/anim/` and one blueprint to `assets/blueprint/`.
3. Wire up the navigation footer in your module **and in its two neighbours**.
4. Add rows to the README module table and the animation gallery.
5. Add its cards to [`docs/flashcards.md`](docs/flashcards.md) and update the count in its index table.
6. Add its rows to [`docs/cheatsheet-complexity.md`](docs/cheatsheet-complexity.md).
7. Add the card to `index.html`.

Run the checks above, and thank you.
