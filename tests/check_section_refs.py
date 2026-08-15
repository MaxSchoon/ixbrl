#!/usr/bin/env python3
"""Reject section cross-references that no longer resolve.

The jurisdiction references use semantic anchors, not numbered headings, because
numbers renumber and `see 4.2` then silently points at unrelated content. In
filing guidance that is a correctness bug, not a formatting one.

This gate enforces the consequence: no reference may cite a NUMBERED section of
a file that has no numbered sections. It exists because restructuring those
files orphaned 409 such references in one commit, and nothing caught it.

Two kinds of reference are deliberately excluded, because rewriting either
would be worse than the stale reference it was chasing.

Specification and manual citations -- `XDT section 2`, `XBRL 2.1 section 5`,
`Reporting Manual 2.1.3`, `EDGAR Filer Manual v68` -- point at external
documents, not at this repo. Only files that ACTUALLY LOST their numbering are
checked for self-references; a file that never had numbered sections cannot
have a stale self-reference, and treating its spec citations as one produced
166 false positives on the first run of this gate.

Statutory citations are the second, and are excluded the same way. German,
Danish and Dutch law is cited with the same symbol -- `§ 5b EStG`, `§§ 325 ff.
HGB`, `§ 114 WpHG`, `§ 13 stk. 3`, `§ 289 Abs. 2` -- and rewriting one of those
would be far worse than the stale reference it was trying to fix. A citation
naming a statute, a subsection word, or an article is left alone.

Run: python3 tests/check_section_refs.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFERENCES = ROOT / "references"

# Deciding whether a § is a document self-reference or a citation to something
# external is the whole difficulty here, and getting it wrong in the unsafe
# direction corrupts filing-critical text. So the test is not a list of statute
# names -- that under-matched and produced false positives on Belgian FSMA
# circulars, the Income Tax Code, and `§§ 325` forms -- but a structural one:
#
#   a citation NAMES ITS SOURCE, and the name sits just before the symbol.
#
# `§ 5b EStG`, `§§ 325 ff. HGB`, `FSMA_2021_19 §5.4`, `ITC 1992 arts 307 §1`,
# `XDT §2`, `Reporting Manual §2.1.3` all carry an acronym, a year, a proper
# noun, or a citation word within a short window. A genuine self-reference does
# not: `(§7.2)`, `see §4`, `§12)`.
CITATION_CUE = re.compile(
    r"(?:[A-Z]{2,}|\b(?:19|20)\d{2}\b|\b(?:art|arts|Art|Arts|artikel|Section|"
    r"section|Code|Manual|Guide|Recommendation|Circular|Regulation|Directive|"
    r"Annex|Abs|stk|lid|Nr|ff)\b|[A-Z][a-z]+_\d)"
)
# A statute number can also be FOLLOWED by its law, e.g. `§ 5b EStG`.
TRAILING_LAW = re.compile(r"^\s*[a-z]?\s*(?:ff\.?\s*)?[A-ZÅÄÖ][A-Za-zÅÄÖåäö]{1,8}\b")


# A § number immediately preceded by a .md filename cites that file.
TARGETED = re.compile(
    r"`(?:references/)?(?:jurisdictions/)?([a-z0-9-]+\.md)`[^§\n]{0,25}(§+\s?[\d.]+)"
)
BARE = re.compile(r"§+\s?\d+(?:\.\d+)*")

# Only files that lost their numbering can hold a stale SELF-reference.
RESTRUCTURED_DIR = REFERENCES / "jurisdictions"

# Jurisdictions whose legal system cites statutes with the section symbol, where
# a bare `§ 335` is overwhelmingly "HGB § 335" with the law implied by context.
# Classifying those by pattern is unwinnable -- every heuristic either misses
# real references or, far worse, invites an edit to a legal citation. So the
# bare self-reference scan is skipped for them and the targeted check below,
# which is unambiguous, carries the load. Recorded as a limitation rather than
# papered over: see the note in CONTRIBUTING.
SYMBOL_STATUTE_JURISDICTIONS = {"DE", "DK", "AT", "CH", "FI", "SE", "NO"}


def jurisdiction_of(path: Path) -> str:
    m = re.search(
        r"^jurisdiction:\s*([A-Z]{2})\s*$", path.read_text(encoding="utf-8"), re.M
    )
    return m.group(1) if m else ""


def is_citation(text: str, start: int, end: int) -> bool:
    """True if this § names an external source rather than a local section."""
    before = text[max(0, start - 32) : start]
    if CITATION_CUE.search(before):
        return True
    return bool(TRAILING_LAW.match(text[end : end + 14]))


errors: list[str] = []


def numbered_sections(path: Path) -> bool:
    """Does this file still have numbered H2 headings to cite?"""
    return bool(re.search(r"^## \d+\.", path.read_text(encoding="utf-8"), re.M))


def main() -> int:
    sources = [ROOT / "SKILL.md", *sorted(REFERENCES.rglob("*.md"))]
    has_numbers = {p.name: numbered_sections(p) for p in REFERENCES.rglob("*.md")}

    checked = 0
    for src in sources:
        if not src.is_file():
            continue
        label = src.relative_to(ROOT).as_posix()
        text = src.read_text(encoding="utf-8")

        targeted_spans = set()
        for m in TARGETED.finditer(text):
            targeted_spans.add(m.start(2))
            checked += 1
            target = m.group(1)
            if target in has_numbers and not has_numbers[target]:
                errors.append(
                    f"{label}: cites {target} {m.group(2).strip()}, but that file "
                    "has no numbered sections — name the section instead"
                )

        # Self-references only matter in a file that actually dropped its
        # numbering -- i.e. one this migration restructured. Everywhere else a
        # bare section number cites an external spec or manual.
        if (
            src.is_relative_to(RESTRUCTURED_DIR)
            and jurisdiction_of(src) not in SYMBOL_STATUTE_JURISDICTIONS
        ):
            for m in BARE.finditer(text):
                if m.start() in targeted_spans:
                    continue
                if is_citation(text, m.start(), m.end()):
                    continue
                checked += 1
                context = text[max(0, m.start() - 55) : m.end()].replace("\n", " ")
                errors.append(
                    f"{label}: self-reference {m.group().strip()} has no numbered "
                    f"section to resolve to — …{context[-70:]}"
                )

    if errors:
        for e in errors[:25]:
            print(f"::error::{e}")
        if len(errors) > 25:
            print(f"::error::… and {len(errors) - 25} more")
        print(f"\n{len(errors)} unresolvable section reference(s).")
        return 1
    print(f"Section references OK ({checked} checked; statutory citations exempt)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
