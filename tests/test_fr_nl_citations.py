#!/usr/bin/env python3
"""The FR-NL numbers this skill states are the NT20 v1.1 rules.

SBR Filing Rules NT20 v1.1 (19 November 2025), read 2026-11-09:
FR-NL-3.02 forbids xbrli:forever, FR-NL-3.04 forbids duplicate contexts,
FR-NL-2.07 forbids xsi:nil, FR-NL-5.06 forbids precision, FR-NL-5.07
requires percentages as decimals, and FR-NL-6.01 forbids footnotes.

A swapped number sends a reviewer to the wrong rule.
"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODED = (
    "references/defect-causes.md",
    "references/validation.md",
    "references/structure.md",
)


def lines_of(rel: str) -> list[str]:
    return (ROOT / rel).read_text(encoding="utf-8").splitlines()


class FrNlCitations(unittest.TestCase):
    def test_forever_is_fr_nl_3_02(self) -> None:
        hits = [
            (rel, n, line)
            for rel in CODED
            for n, line in enumerate(lines_of(rel), 1)
            if "forever" in line and "FR-NL-" in line
        ]
        self.assertTrue(hits)
        for rel, n, line in hits:
            self.assertIn("FR-NL-3.02", line, f"{rel}:{n}")
            self.assertNotIn("FR-NL-3.04", line, f"{rel}:{n}")

    def test_duplicate_contexts_are_fr_nl_3_04(self) -> None:
        text = (ROOT / "references/validation.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"FR-NL-3\.04` \| [^|]*[Dd]uplicate")

    def test_nil_is_fr_nl_2_07(self) -> None:
        hits = [
            (rel, n, line)
            for rel in CODED
            for n, line in enumerate(lines_of(rel), 1)
            if "xsi:nil" in line and "FR-NL-" in line
        ]
        self.assertTrue(hits)
        for rel, n, line in hits:
            self.assertIn("FR-NL-2.07", line, f"{rel}:{n}")
            self.assertNotIn("FR-NL-5.07", line, f"{rel}:{n}")

    def test_percentages_are_fr_nl_5_07(self) -> None:
        hits = [
            (rel, n, line)
            for rel in ("references/defect-causes.md", "references/validation.md")
            for n, line in enumerate(lines_of(rel), 1)
            if "FR-NL-5.07" in line
        ]
        self.assertTrue(hits)
        for rel, n, line in hits:
            self.assertRegex(line, r"percent|decimal", f"{rel}:{n}")
            self.assertNotIn("xsi:nil", line, f"{rel}:{n}")

    def test_precision_stays_fr_nl_5_06(self) -> None:
        hits = [
            line
            for rel in ("references/defect-causes.md", "references/validation.md")
            for line in lines_of(rel)
            if "FR-NL-5.06" in line
        ]
        self.assertTrue(hits)
        for line in hits:
            self.assertIn("precision", line)

    def test_footnotes_are_forbidden_by_fr_nl_6_01(self) -> None:
        for line in lines_of("references/validation.md"):
            if "FR-NL-6.01" not in line:
                continue
            self.assertNotIn("footnote model", line)
            self.assertRegex(line, r"[Ff]orbid|[Oo]mit")

    def test_inline_xbrl_errata_edition_is_2026_07_14(self) -> None:
        text = (ROOT / "references/conversion.md").read_text(encoding="utf-8")
        self.assertIn("2026-07-14", text)
        self.assertNotIn("errata 2024-12-17", text)

    def test_ifrs_filers_are_deemed_large(self) -> None:
        text = (ROOT / "references/jurisdictions/nl-sbr.md").read_text(encoding="utf-8")
        start = text.index("### Size class:")
        section = text[start : text.index("\n### ", start + 5)]
        self.assertIn("IFRS", section)
        self.assertIn("regardless", section)

    def test_lei_is_not_listed_as_an_fy2026_delta(self) -> None:
        text = (ROOT / "references/jurisdictions/nl-sbr.md").read_text(encoding="utf-8")
        self.assertNotIn(
            "The substantive deltas sit\nin the Annexes: the LEI identifier",
            text,
        )


if __name__ == "__main__":
    unittest.main()
