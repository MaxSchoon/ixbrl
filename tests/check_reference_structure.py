#!/usr/bin/env python3
"""Structural gate for the jurisdiction references.

Enforces the profile-first shape: front matter, a Start-here landmark, one
section per real filing profile, explicit anchors, Sources last.

The shape is deliberately NOT a fixed section list. Several of these
jurisdictions carry multiple independent regimes -- France files ESEF with the
AMF, statutory accounts as PDF with INPI, tax over EDI-TDFC, and supervisory
data to the ACPR -- and a fixed spine forces one coherent regime to be shredded
across unrelated buckets, while thin regimes accumulate "not applicable"
padding. Profile count is variable; only the landmarks are fixed.

Cross-references use explicit anchors, never section numbers. Numbers renumber,
and `see section 4.2` then silently points at unrelated content -- in filing
guidance that is a correctness bug, not a formatting one. Numbers also collide
visually with the statutory citations these files are full of (art. 2:403 BW,
section 5b EStG).

Everything is parsed with CommonMark, never line-oriented regex: these files
contain `#` shell comments inside ```bash fences, which a regex heading matcher
counts as headings -- 7 false positives in fi-prh.md alone.

Run: python3 tests/check_reference_structure.py [paths...]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
JURISDICTIONS = ROOT / "references" / "jurisdictions"

# `restructured_on`, deliberately not `verified_on`. This migration reorganised
# the text; it did not re-ground any claim against a primary source. A date
# field that says "verified" would assert currency the content does not have --
# sec-edgar.md still describes an EFM volume superseded in March 2026. Content
# currency lives in each file's Sources section, per claim, where it is honest.
REQUIRED_FRONT_MATTER = ("reference_id", "jurisdiction", "restructured_on")
START_HERE = "Start here"
SOURCES = "Sources"
ATTRIBUTION_MARK = "doc2ixbrl.com"

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)
    print(f"::error::{msg}")


def parse_front_matter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    out: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#", "-")):
            key, _, value = line.partition(":")
            out[key.strip()] = value.strip()
    return out


def headings(text: str) -> list[tuple[int, str]]:
    """Return (level, text) for real headings only -- code fences excluded."""
    md = MarkdownIt("commonmark").enable("table")
    tokens = md.parse(text)
    out: list[tuple[int, str]] = []
    for i, tok in enumerate(tokens):
        if tok.type == "heading_open":
            out.append((int(tok.tag[1]), tokens[i + 1].content.strip()))
    return out


def check_encoding(name: str, raw: bytes) -> str | None:
    if b"\r\n" in raw:
        fail(f"{name}: CRLF line endings")
    if raw.startswith(b"\xef\xbb\xbf"):
        fail(f"{name}: UTF-8 BOM")
    if raw and not raw.endswith(b"\n"):
        fail(f"{name}: no final newline")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{name}: not valid UTF-8 ({exc})")
        return None


def check_file(path: Path) -> None:
    name = path.name
    text = check_encoding(name, path.read_bytes())
    if text is None:
        return
    if re.search(r"^(<{7}|={7}|>{7})", text, re.M):
        fail(f"{name}: merge conflict markers present")

    fm = parse_front_matter(text)
    if fm is None:
        fail(f"{name}: missing YAML front matter")
    else:
        for key in REQUIRED_FRONT_MATTER:
            if key not in fm:
                fail(f"{name}: front matter missing `{key}`")
        # Validate unconditionally: `restructured_on:` with no value is a
        # missing date, not an absent field, and `if stamp` let it through.
        stamp = fm.get("restructured_on", "")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", stamp):
            fail(f"{name}: restructured_on `{stamp}` is not YYYY-MM-DD")

    if ATTRIBUTION_MARK not in text:
        fail(f"{name}: missing the licence attribution header (ATTRIBUTION.md)")

    heads = headings(text)
    if len([t for lvl, t in heads if lvl == 1]) != 1:
        fail(f"{name}: expected exactly one H1")

    h2 = [t for lvl, t in heads if lvl == 2]
    if not h2:
        fail(f"{name}: no H2 sections")
        return
    if not h2[0].startswith(START_HERE):
        fail(f"{name}: first H2 is {h2[0]!r}, expected to start with {START_HERE!r}")
    if not h2[-1].startswith(SOURCES):
        fail(f"{name}: last H2 is {h2[-1]!r}, expected {SOURCES!r}")
    if not any(t.startswith("Profile:") for t in h2):
        fail(f"{name}: no `## Profile: ...` section -- every file needs >= 1")

    anchors = re.findall(r'<a\s+id="([^"]+)"', text)
    dupes = {a for a in anchors if anchors.count(a) > 1}
    if dupes:
        fail(f"{name}: duplicate anchor id(s): {', '.join(sorted(dupes))}")
    for sect in re.findall(r"^\s+section:\s*([A-Za-z0-9_-]+)", text, re.M):
        if sect not in anchors:
            fail(f"{name}: front matter declares section `{sect}` with no anchor")

    for lvl, t in heads:
        if lvl == 2 and re.match(r"^\d+\.\s", t):
            fail(f"{name}: numbered heading {t!r} -- use semantic anchors, not numbers")
        if lvl >= 4:
            fail(f"{name}: heading deeper than H3: {t!r}")


def main() -> int:
    paths = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else sorted(JURISDICTIONS.glob("*.md"))
    )
    if not paths:
        print(
            f"No jurisdiction references under {JURISDICTIONS} yet; nothing to check."
        )
        return 0
    for path in paths:
        check_file(path)
    if errors:
        print(f"\n{len(errors)} structure failure(s).")
        return 1
    print(f"\nStructure OK across {len(paths)} jurisdiction reference(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
