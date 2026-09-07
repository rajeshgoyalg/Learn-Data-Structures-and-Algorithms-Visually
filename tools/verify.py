#!/usr/bin/env python3
"""Repository invariant checks for the Visual DSA course.

Stdlib only, no install step: this is a checker, not a build step. The SVGs and
markdown stay hand-editable, and nothing here generates content.

Run locally:   python3 tools/verify.py
CI runs the same file, so a green local run means a green PR.
"""
import glob
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

FAILURES = []
CHECKS_RUN = 0


def check(name):
    """Decorator: register a check, collect its failure strings."""
    def wrap(fn):
        global CHECKS_RUN
        CHECKS_RUN += 1
        problems = fn() or []
        if problems:
            FAILURES.append((name, problems))
            print(f"  FAIL  {name}")
            for p in problems[:12]:
                print(f"          {p}")
            if len(problems) > 12:
                print(f"          ... and {len(problems) - 12} more")
        else:
            print(f"  ok    {name}")
        return fn
    return wrap


def svgs():
    return sorted(glob.glob("assets/*/*.svg"))


def md_files():
    return ["README.md", "CONTRIBUTING.md"] + sorted(glob.glob("docs/*.md"))


# --------------------------------------------------------------------- assets
@check("every SVG is well-formed XML")
def _():
    bad = []
    for f in svgs():
        try:
            ET.parse(f)
        except ET.ParseError as e:
            bad.append(f"{f}: {e}")
    return bad


@check("no <script> in any asset (inert in GitHub's <img> context)")
def _():
    return [f for f in svgs() if "<script" in open(f).read()]


@check("no external references (only the SVG namespace URI is allowed)")
def _():
    bad = []
    for f in svgs():
        urls = set(re.findall(r'https?://[^"\s]+', open(f).read()))
        urls.discard("http://www.w3.org/2000/svg")
        if urls:
            bad.append(f"{f}: {sorted(urls)[:2]}")
    return bad


@check("every SVG has viewBox, <title> and aria-label")
def _():
    bad = []
    for f in svgs():
        s = open(f).read()
        for attr in ("viewBox", "<title>", "aria-label"):
            if attr not in s:
                bad.append(f"{f}: missing {attr}")
    return bad


# The generator wraps text using this same advance estimate, so this check
# catches text that was never put through the wrapper. It is a model of the
# monospace stack, not a rasterisation - exact metrics need a browser.
CHAR_W = 0.60
CLASS_FS = {"title": 17, "sub": 12, "lbl": 11, "lbl-l": 11, "val": 16, "idx": 10, "step": 12}
CLASS_MID = {"lbl", "val", "idx"}
MARGIN = 4


@check("no text runs past the right edge of its canvas")
def _():
    bad = []
    for f in svgs():
        s = open(f).read()
        m = re.search(r'viewBox="0 0 (\d+) (\d+)"', s)
        if not m:
            continue
        W = int(m.group(1))
        for attrs, inner in re.findall(r"<text([^>]*)>(.*?)</text>", s, re.S):
            cls = (re.search(r'class="([^"]*)"', attrs) or [None, ""])[1]
            anchor = (re.search(r'text-anchor="([^"]*)"', attrs) or [None, None])[1]
            if anchor is None:
                anchor = "middle" if any(c in CLASS_MID for c in cls.split()) else "start"
            if anchor != "start":
                continue
            xm = re.search(r'\sx="([\d.-]+)"', attrs)
            if not xm:
                continue
            x = float(xm.group(1))
            fsm = re.search(r'font-size="?([\d.]+)', attrs) or re.search(r"font-size:([\d.]+)", attrs)
            fs = float(fsm.group(1)) if fsm else next(
                (v for k, v in CLASS_FS.items() if k in cls.split()), 12)
            lines = re.findall(r"<tspan[^>]*>(.*?)</tspan>", inner, re.S) or [inner]
            for ln in lines:
                text = re.sub(r"<[^>]+>", "", ln)
                if not text.strip():
                    continue
                right = x + len(text) * CHAR_W * fs
                if right > W - MARGIN:
                    bad.append(f'{f} +{right - W:.0f}px: "{text.strip()[:44]}"')
    return bad


@check("legend swatches stay aligned with their labels")
def _():
    bad = []
    for f in svgs():
        s = open(f).read()
        rects = [float(y) for y in re.findall(r'<rect class="swatch"[^>]*\sy="([\d.]+)"', s)]
        texts = [float(y) for y in re.findall(r'<text class="lbl-l"[^>]*\sy="([\d.]+)"', s)]
        for r in rects:
            if not any(abs((t - 6) - r) < 0.7 for t in texts):
                bad.append(f"{f}: swatch at y={r:g} has no label at y={r + 6:g}")
    return bad


@check("blueprint title blocks sit on the bottom edge")
def _():
    bad = []
    for f in sorted(glob.glob("assets/blueprint/*.svg")):
        s = open(f).read()
        H = int(re.search(r'viewBox="0 0 \d+ (\d+)"', s).group(1))
        m = re.search(r'<rect x="\d+" y="([\d.]+)" width="300" height="62"', s)
        if m:
            gap = H - (float(m.group(1)) + 62)
            if abs(gap - 20) > 1.5:
                bad.append(f"{f}: {gap:.0f}px from the bottom, expected 20")
    return bad


@check("frame animations never show two frames at once")
def _():
    bad = []
    for f in sorted(glob.glob("assets/anim/*.svg")):
        s = open(f).read()
        spans = []
        for name, body in re.findall(r"@keyframes (fk\d+)\{(.*?)\}\n", s, re.S):
            on = [float(p) for p, d in re.findall(r"([\d.]+)%\{([^}]*)\}", body) if "opacity:1" in d]
            if on:
                spans.append((min(on), max(on), name))
        spans.sort()
        for i in range(len(spans) - 1):
            if spans[i][1] > spans[i + 1][0] + 0.001:
                bad.append(f"{f}: {spans[i][2]} overlaps {spans[i + 1][2]}")
    return bad


# ------------------------------------------------------------------- markdown
@check("all internal links and anchors resolve")
def _():
    bad = []
    for f in md_files():
        base = os.path.dirname(f)
        text = open(f).read()
        heads = [re.sub(r"[^a-z0-9\s-]", "", h.lower()).strip().replace(" ", "-")
                 for h in re.findall(r"^#{1,6}\s+(.*)$", text, re.M)]
        for target in re.findall(r"\]\(([^)\s]+)\)", text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            path, _, frag = target.partition("#")
            if not path:
                if frag not in heads:
                    bad.append(f"{f} -> #{frag} (no such heading)")
            elif not os.path.exists(os.path.normpath(os.path.join(base, path))):
                bad.append(f"{f} -> {target} (missing file)")
    return bad


@check("every module keeps the eleven-block template")
def _():
    blocks = [("analogy", r"^> \*\*The analogy"), ("animation", r"!\[.*\]\(\.\./assets/anim/"),
              ("mental model", r"## 🧠 Mental model"), ("blueprint", r"!\[.*\]\(\.\./assets/blueprint/"),
              ("mindmap", r"```mermaid"), ("operations", r"## ⚙️"), ("complexity", r"## ⏱️"),
              ("trade-offs", r"## ⚖️"), ("flashcards", r"## 🃏"), ("quiz", r"## ❓"),
              ("nav", r"⬅️ .*🏠 Index")]
    bad = []
    for f in sorted(glob.glob("docs/[0-9][0-9]-*.md")):
        if f.endswith("00-how-to-read-this.md"):
            continue          # the legend, deliberately not a module
        s = open(f).read()
        missing = [n for n, p in blocks if not re.search(p, s, re.M)]
        if f.endswith("01-foundations.md"):
            missing = [m for m in missing if m != "animation"]   # theory module, no animation
        if missing:
            bad.append(f"{f}: missing {missing}")
    return bad


@check("no Mermaid mindmap blocks (GitHub cannot render them)")
def _():
    bad = []
    for f in md_files():
        for block in re.findall(r"```mermaid\n(.*?)```", open(f).read(), re.S):
            first = block.strip().split("\n")[0].strip()
            if first.startswith("mindmap"):
                bad.append(f"{f}: uses `mindmap`; use `flowchart` instead")
    return bad


@check("every <details> is closed")
def _():
    bad = []
    for f in md_files():
        if f == "CONTRIBUTING.md":
            continue          # documents the tags inside fenced code blocks
        s = open(f).read()
        if s.count("<details") != s.count("</details>"):
            bad.append(f"{f}: {s.count('<details')} open, {s.count('</details>')} closed")
    return bad


@check("no duplicate flashcards")
def _():
    import collections
    qs = [q.strip().lower() for q in
          re.findall(r"<summary>(.*?)</summary>", open("docs/flashcards.md").read())]
    return [f"asked {c}x: {q[:60]}" for q, c in collections.Counter(qs).items() if c > 1]


@check("stated counts match reality")
def _():
    bad = []
    fc = open("docs/flashcards.md").read()
    n_cards = fc.count("<details>")
    m = re.search(r"\*\*Total\*\* \| \*\*(\d+)\*\*", fc)
    if m and int(m.group(1)) != n_cards:
        bad.append(f"flashcards index says {m.group(1)}, deck has {n_cards}")
    readme = open("README.md").read()
    for label, actual in [("animated_SVGs", len(glob.glob("assets/anim/*.svg"))),
                          ("blueprints", len(glob.glob("assets/blueprint/*.svg"))),
                          ("flashcards", n_cards),
                          ("quiz", open("docs/quiz.md").read().count("<details>"))]:
        m = re.search(rf"badge/{label}-(\d+)", readme)
        if m and int(m.group(1)) != actual:
            bad.append(f"README badge {label}={m.group(1)}, actual {actual}")
    return bad


@check("no orphaned assets")
def _():
    refs = "".join(open(f).read() for f in md_files() + ["index.html"])
    return [a for a in svgs() if os.path.basename(a) not in refs]


@check("gallery links point at rendered pages, not raw markdown")
def _():
    # GitHub Pages serves .md as text/markdown, so a relative link from the
    # gallery shows unrendered source. See CONTRIBUTING, "A note for forkers".
    return [f"index.html: relative link to {t}"
            for t in re.findall(r'href="(docs/[^"]+\.md)"', open("index.html").read())]



@check("no blueprint text runs under the title block")
def _():
    bad = []
    for f in sorted(glob.glob("assets/blueprint/*.svg")):
        s = open(f).read()
        m = re.search(r'viewBox="0 0 (\d+) (\d+)"', s)
        if not m:
            continue
        W, H = int(m.group(1)), int(m.group(2))
        box = (W - 322, H - 82, W - 22, H - 20)
        for attrs, inner in re.findall(r"<text([^>]*)>(.*?)</text>", s, re.S):
            cls = (re.search(r'class="([^"]*)"', attrs) or [None, ""])[1]
            if "tb" in cls.split():
                continue                      # the block's own labels belong there
            anchor = (re.search(r'text-anchor="([^"]*)"', attrs) or [None, None])[1]
            if anchor is None:
                anchor = "middle" if any(c in CLASS_MID for c in cls.split()) else "start"
            if anchor != "start":
                continue
            xm = re.search(r'\sx="([\d.-]+)"', attrs)
            ym = re.search(r'\sy="([\d.-]+)"', attrs)
            if not (xm and ym):
                continue
            x, y = float(xm.group(1)), float(ym.group(1))
            fsm = re.search(r'font-size="?([\d.]+)', attrs)
            fs = float(fsm.group(1)) if fsm else next(
                (v for k, v in CLASS_FS.items() if k in cls.split()), 12)
            lines = re.findall(r"<tspan[^>]*>(.*?)</tspan>", inner, re.S) or [inner]
            for i, ln in enumerate(lines):
                t = re.sub(r"<[^>]+>", "", ln)
                if not t.strip():
                    continue
                yy = y + i * (fs + 6)
                if (x + len(t) * CHAR_W * fs > box[0] and x < box[2]
                        and yy + fs * 0.4 > box[1] and yy - fs * 0.8 < box[3]):
                    bad.append(f'{f}: "{t.strip()[:42]}"')
    return bad


@check("every operation shows pseudocode before its Python")
def _():
    """The idea first, then the code. A python fence with no preceding text
    fence in the same Operations section means an operation lost its
    pseudocode -- except node/type definitions, which are data, not algorithms."""
    DATA_ONLY = {"Node", "DNode", "TreeNode", "TrieNode"}
    bad = []
    for f in sorted(glob.glob("docs/[0-9][0-9]-*.md")):
        s = open(f).read()
        m = re.search(r"^## ⚙️ .*$", s, re.M)
        if not m or "## ⏱️ Complexity" not in s:
            continue
        ops = s[m.start():s.index("## ⏱️ Complexity")]
        n_text = len(re.findall(r"```text", ops))
        markers = re.findall(r"<!-- py:([\w./]+):(\w+) -->", ops)
        n_code = len([sym for _, sym in markers if sym not in DATA_ONLY])
        if n_text == 0 and n_code > 0:
            bad.append(f"{f}: {n_code} Python snippet(s) but no pseudocode at all")
        elif n_code and n_text < 1:
            bad.append(f"{f}: pseudocode missing")
    return bad


# --------------------------------------------------------------------- python
@check("every ```python block in docs/ parses as valid Python")
def _():
    import ast as _ast
    bad = []
    for f in sorted(glob.glob("docs/*.md")):
        for i, code in enumerate(re.findall(r"```python\n(.*?)```", open(f).read(), re.S), 1):
            try:
                _ast.parse(code)
            except SyntaxError as e:
                bad.append(f"{f} block {i}: line {e.lineno}: {e.msg}")
    return bad


@check("embedded Python still matches examples/ (no drift)")
def _():
    import subprocess
    r = subprocess.run([sys.executable, "tools/sync_examples.py", "--check"],
                       capture_output=True, text=True)
    if r.returncode == 0:
        return []
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]


@check("the examples test suite passes")
def _():
    import subprocess
    # -B and a cleared cache: bytecode is invalidated on mtime+size, so an edit
    # that keeps the file the same size (swapping < for >, say) can otherwise be
    # masked by a stale .pyc. Cost is a few milliseconds.
    import shutil
    shutil.rmtree("examples/__pycache__", ignore_errors=True)
    r = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover",
                        "-s", "examples", "-t", "."],
                       capture_output=True, text=True,
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    if r.returncode == 0:
        tail = [ln for ln in r.stderr.splitlines() if ln.startswith("Ran ")]
        print(f"          {tail[0] if tail else 'passed'}")
        return []
    return [ln for ln in r.stderr.splitlines()
            if ln.startswith(("FAIL", "ERROR", "AssertionError"))][:10]


# ----------------------------------------------------------------------- exit
print()
if FAILURES:
    print(f"FAILED: {len(FAILURES)} of {CHECKS_RUN} checks\n")
    sys.exit(1)
print(f"All {CHECKS_RUN} checks passed.\n")
