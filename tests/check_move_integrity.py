#!/usr/bin/env python3
"""Prove a restructure moved content without changing it.

A reorganisation of regulated reference material has one failure mode that
review reliably misses: an agent "improves" a sentence while relocating it. In a
50 KB file describing filing obligations, a silently reworded claim is
indistinguishable from a faithful move by eye.

So verify it mechanically. Parse the file before and after with a CommonMark
parser, hash every non-heading block, and require the two multisets to match
exactly. A block that moved keeps its hash; a block that was reworded, split,
merged, dropped or duplicated does not.

Headings ARE expected to change -- that is the restructure -- so they are
counted and reported, not enforced.

Why a parser and not a regex: several of these files contain `#` shell comments
inside ```bash fences. A line-oriented heading matcher counts those as headings
(7 false positives in fi-prh.md alone) and produces confident nonsense.

Usage:
  python3 tests/check_move_integrity.py --baseline <git-ref> [paths...]

Exits non-zero on any content block added, dropped, or altered.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
from collections import Counter
from pathlib import Path

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent

# Headings are excluded deliberately: the restructure renames them, which is the
# entire point. Everything else must survive byte-identical.
HEADING_TYPES = {"heading_open"}


def blocks(source: str) -> tuple[list[tuple[str, str]], list[str]]:
    """Split markdown into (kind, text) top-level blocks plus heading texts.

    Nested content (list items, table rows) rides along inside its parent
    block's source span, so it is covered by the parent hash, not double-counted.
    """
    md = MarkdownIt("commonmark").enable("table")
    tokens = md.parse(source)
    lines = source.split("\n")

    found: list[tuple[str, str]] = []
    headings: list[str] = []
    consumed_to = -1

    for tok in tokens:
        if tok.level != 0 or tok.map is None:
            continue
        start, end = tok.map
        if start < consumed_to:
            continue  # already inside a captured block
        text = "\n".join(line.rstrip() for line in lines[start:end]).strip()
        if not text:
            continue
        if tok.type in HEADING_TYPES:
            headings.append(text)
        else:
            found.append((tok.type, text))
        consumed_to = end

    return found, headings


def digest(kind: str, text: str) -> str:
    return hashlib.sha256(f"{kind}\x00{text}".encode()).hexdigest()[:16]


def read_baseline(ref: str, path: Path) -> str | None:
    rel = path.relative_to(ROOT)
    proc = subprocess.run(
        ["git", "show", f"{ref}:{rel}"], cwd=ROOT, capture_output=True, text=True
    )
    return proc.stdout if proc.returncode == 0 else None


def compare(ref: str, path: Path, renames: dict[str, str]) -> list[str]:
    problems: list[str] = []
    source_path = Path(renames.get(str(path.relative_to(ROOT)), path))
    before = read_baseline(ref, ROOT / source_path)
    if before is None:
        return [f"{path.name}: not present at baseline {ref} (declare it as a rename)"]

    old_blocks, old_heads = blocks(before)
    new_blocks, new_heads = blocks(path.read_text(encoding="utf-8"))

    old_counts = Counter(digest(k, t) for k, t in old_blocks)
    new_counts = Counter(digest(k, t) for k, t in new_blocks)
    index = {digest(k, t): t for k, t in old_blocks + new_blocks}

    for h, n in (old_counts - new_counts).items():
        problems.append(
            f"{path.name}: {n} block(s) LOST or ALTERED -- first line: "
            f"{index[h].splitlines()[0][:90]!r}"
        )
    for h, n in (new_counts - old_counts).items():
        problems.append(
            f"{path.name}: {n} block(s) ADDED or ALTERED -- first line: "
            f"{index[h].splitlines()[0][:90]!r}"
        )

    if not problems:
        print(
            f"{path.name}: {len(new_blocks)} content blocks preserved exactly; "
            f"headings {len(old_heads)} -> {len(new_heads)}"
        )
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--baseline", required=True, help="git ref to compare against")
    ap.add_argument(
        "--rename",
        action="append",
        default=[],
        metavar="NEW=OLD",
        help="declare a moved file, e.g. references/jurisdictions/x.md=references/x.md",
    )
    ap.add_argument("paths", nargs="*", help="markdown files (default: references/)")
    args = ap.parse_args()

    # --rename NEW=OLD, keyed by the new path since that is what we walk.
    renames = {}
    for spec in args.rename:
        new_path, _, old_path = spec.partition("=")
        if not old_path:
            raise SystemExit(f"--rename expects NEW=OLD, got {spec!r}")
        renames[new_path] = old_path

    paths = (
        [Path(p).resolve() for p in args.paths]
        if args.paths
        else sorted((ROOT / "references").rglob("*.md"))
    )

    problems: list[str] = []
    for path in paths:
        problems.extend(compare(args.baseline, path, renames))

    if problems:
        for p in problems:
            print(f"::error::{p}")
        print(f"\n{len(problems)} move-integrity failure(s).")
        return 1
    print("\nMove integrity verified: no content block added, dropped, or altered.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
