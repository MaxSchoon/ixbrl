#!/usr/bin/env python3
"""Reject section cross-references that no longer resolve.

The jurisdiction references use semantic anchors, not numbered headings, because
numbers renumber and `see 4.2` then silently points at unrelated content. In
filing guidance that is a correctness bug, not a formatting one.

This gate enforces the consequence: no reference may cite a NUMBERED section of
a file that has no numbered sections. It exists because restructuring those
files orphaned 409 such references in one commit, and nothing caught it.

Statutory citations are the hazard here and are deliberately excluded. German,
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

# Tokens that mark a § as a legal citation rather than a document section.
# Derived from what actually follows § in this corpus, not guessed.
STATUTE = (
    r"(?:HGB|WpHG|EStG|AO|BW|AktG|PublG|GmbHG|Wft|URV|"
    r"ÅRL|ARL|SEL|KVL|stk|Abs|Nr|lid|ff)"
)
STATUTORY = re.compile(r"§+\s?\d+[a-z]?(?:\s*ff\.?)?[\s.,]*" + STATUTE, re.IGNORECASE)

# A § number immediately preceded by a .md filename cites that file.
TARGETED = re.compile(
    r"`(?:references/)?(?:jurisdictions/)?([a-z0-9-]+\.md)`[^§\n]{0,25}(§+\s?[\d.]+)"
)
BARE = re.compile(r"§+\s?\d+(?:\.\d+)*")

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
        text = STATUTORY.sub("", src.read_text(encoding="utf-8"))

        targeted_spans = set()
        for m in TARGETED.finditer(text):
            targeted_spans.add(m.span(2))
            checked += 1
            target = m.group(1)
            if target in has_numbers and not has_numbers[target]:
                errors.append(
                    f"{label}: cites {target} {m.group(2).strip()}, but that file "
                    "has no numbered sections — name the section instead"
                )

        # Self-references only matter in a file that dropped its numbering.
        if src.is_relative_to(REFERENCES) and not has_numbers.get(src.name, True):
            for m in BARE.finditer(text):
                if m.span() in targeted_spans:
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
