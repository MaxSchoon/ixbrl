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


# One content invariant, not a general one. The NL reference describes two
# filing systems that share a prefix family: the classic XBRL route (RTS
# Chapter 3), where the entry point is selected by entity size and sector, and
# the KvK Inline XBRL route (RTS Chapter 2), where it is selected by financial
# year and accounting basis. Merging their selectors is not a formatting slip:
# it tells a preparer to pick a schema that the taxonomy package the filing
# actually resolves against does not contain, and the deposit is rejected. It
# had merged once (upstream #28), so the two selectors are gated here.
#
# The rules are deliberately narrow, because the CONTRAST between the families
# is exactly what the prose must keep drawing. Only tables are checked, and a
# table row is a selection statement: this release or this situation takes this
# entry point. Prose may name both families in one sentence, and should.
# The classic family is recognised by either its `kvk-rpt-` prefix or the
# `jaarverantwoording-` stem (a row may quote the stem without the prefix);
# the Inline family by `kvk-annual-report-`. `kvk-cor.xsd` and `kvk-all.xsd`
# are element inventories, not entry points, so a bare `.xsd` is NOT a token:
# a row that names them beside a size class is a correct row.
NL_CLASSIC_ENTRY_POINT = re.compile(r"kvk-rpt-|jaarverantwoording-")
NL_INLINE_ENTRY_POINT = re.compile(r"kvk-annual-report-")
NL_ENTRY_POINT_TOKEN = re.compile(r"kvk-rpt-|jaarverantwoording-|kvk-annual-report-")
# Size classes as words in either case (Dutch writes them lowercase in
# running text), and the size-member QNames. The `-micro` / `-groot`
# suffixes inside a classic filename are not matched because they are not
# word-bounded by a space or pipe on both sides there.
NL_SIZE_CLASS = re.compile(
    r"(?<![\w-])(micro|klein|middelgroot|groot)(?![\w-])|LegalEntitySize",
    re.IGNORECASE,
)


def table_rows(text: str) -> list[tuple[int, str]]:
    """Return (line, joined cell text) per table row -- CommonMark, not regex.

    Shell fences in these files are full of `|` pipes, so a line-oriented row
    matcher reads `unzip -p x | grep y` as a table row.
    """
    md = MarkdownIt("commonmark").enable("table")
    tokens = md.parse(text)
    rows: list[tuple[int, str]] = []
    line = 0
    cells: list[str] = []
    inside = False
    for tok in tokens:
        if tok.map:
            line = tok.map[0]
        if tok.type == "tr_open":
            inside, cells = True, []
        elif tok.type == "tr_close":
            rows.append((line + 1, " ".join(cells)))
            inside = False
        elif inside and tok.type == "inline":
            cells.append(tok.content)
    return rows


def profile_span(text: str, anchor_id: str) -> tuple[int, int] | None:
    """Line span of the section introduced by `anchor_id`, up to the next H2.

    Keyed on the front-matter-declared anchor rather than on heading text, so
    rewording a heading does not silently switch the gate off.
    """
    match = re.search(rf'<a\s+id="{re.escape(anchor_id)}"', text)
    if match is None:
        return None
    start = text[: match.start()].count("\n") + 1
    md = MarkdownIt("commonmark").enable("table")
    h2_lines = [
        tok.map[0] + 1
        for tok in md.parse(text)
        if tok.type == "heading_open" and tok.tag == "h2" and tok.map
    ]
    # The first H2 at or after the anchor is the section's OWN heading; the
    # section ends at the one after that. Taking the first (an earlier bug)
    # collapsed the span to two lines and the gate checked nothing.
    after = [line for line in h2_lines if line >= start]
    if len(after) >= 2:
        return (start, after[1])
    return (start, text.count("\n") + 2)


def check_nl_entry_point_families(name: str, text: str) -> None:
    rows = table_rows(text)
    for line, row in rows:
        if NL_CLASSIC_ENTRY_POINT.search(row) and NL_INLINE_ENTRY_POINT.search(row):
            fail(
                f"{name}:{line}: one table row names both the classic "
                "(`kvk-rpt-` / `jaarverantwoording-`) and the Inline "
                "(`kvk-annual-report-`) entry-point family -- they are "
                "selected differently; give them separate rows or separate tables"
            )
    span = profile_span(text, "profile-kvk-ixbrl-annual-accounts")
    if span is None:
        return
    start, end = span
    for line, row in rows:
        if not start <= line < end:
            continue
        if NL_SIZE_CLASS.search(row) and NL_ENTRY_POINT_TOKEN.search(row):
            fail(
                f"{name}:{line}: a table row in the KvK Inline XBRL profile "
                "pairs an entity-size class with an entry-point schema. Size "
                "selects an entry point in the classic XBRL tree only (RM 2026 "
                "Guidance 4.1.2 selects the Inline entry point by financial "
                "year and accounting basis)"
            )


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

    if fm is not None and fm.get("reference_id") == "nl-sbr":
        check_nl_entry_point_families(name, text)

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
