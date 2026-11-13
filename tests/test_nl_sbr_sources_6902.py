#!/usr/bin/env python3
"""Claims in the NL-SBR and taxonomy references that primary sources settle.

Each assertion names the source read on 2026-11-13:

- RTS 2026 NL, Chapter 3 Annex I Table 1, prints the NT21 namespace as
  ``http://www.nltaxonomie.nl/nt20/kvk/20261209/`` (404); the English
  edition prints ``nt21`` (200). The file must flag the Dutch misprint.
- Reporting Manual 2026 EN Guidance 3.6.3: the separate filing-information
  document references only the Annex II point 3 elements, holds at most one
  non-dimensional context and no units. Arelle checks these as
  NL-KVK.3.6.3.5, .6 and .7 (``validate/NL/rules/nl_kvk.py``).
- Reporting Manual 2026 EN Guidance 8.2.2: the Digipoort supply request,
  Base64-encoded package included, must not exceed 150 MB.
- Arelle ``validate/NL/resources/config.xml`` registers NL-INLINE-2025,
  NL-INLINE-2025-GAAP-OTHER-PREVIEW, NL-INLINE-2024, NL-INLINE-2024-GAAP-OTHER,
  NL-INLINE-MULTI-TARGET and NT16 to NT20.
- Calculations 1.1 section 4.1: "XBRL v2.1 prescribes no behaviour for
  Calculations v1.1 relationships and XBRL v2.1 calculation consistency
  checking MUST NOT be applied to them." It does not extend section 3.1.
- SBR Filing Rules NT20 v1.1 has no rule on ``decimals="INF"``; the KvK
  Filing Rules NT20 v1.0 carry FR-KVK-5.01 and 5.02.
- The FRC's "latest and penultimate" policy is XBRL Tagging Guide 2026
  section 6.6, a use policy; Companies House accepts the 2022 to 2026
  suites (XML Gateway forum, 22 December 2025). The two must not be read
  as one window.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NL = ROOT / "references/jurisdictions/nl-sbr.md"
TAX = ROOT / "references/taxonomies.md"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def flat(path: Path) -> str:
    return re.sub(r"\s+", " ", text(path))


class Claims(unittest.TestCase):
    def has(self, needle: str, body: str) -> None:
        self.assertTrue(needle in body, f"missing: {needle!r}")

    def lacks(self, needle: str, body: str) -> None:
        self.assertFalse(needle in body, f"still present: {needle!r}")

    def matches(self, pattern: str, body: str) -> None:
        self.assertTrue(re.search(pattern, body), f"no match: {pattern!r}")


class NlSbrSources(Claims):
    def test_dutch_rts_nt21_namespace_misprint_is_flagged(self) -> None:
        body = flat(NL)
        self.has("nt20/kvk/20261209/", body)
        idx = body.index("nt20/kvk/20261209/")
        window = body[max(0, idx - 600) : idx + 600]
        self.has("nt21/kvk/20261209/", window)
        self.has("404", window)

    def test_filing_information_document_constraints(self) -> None:
        body = flat(NL)
        for code in ("NL-KVK.3.6.3.5", "NL-KVK.3.6.3.6", "NL-KVK.3.6.3.7"):
            self.has(code, body)
        self.has("single non-dimensional context", body)
        self.matches(r"no units|must not contain any units", body)

    def test_digipoort_supply_request_limit(self) -> None:
        body = flat(NL)
        self.matches(r"150 MB[^.]*Guidance 8\.2\.2|Guidance 8\.2\.2[^.]*150 MB", body)

    def test_arelle_disclosure_systems_are_complete(self) -> None:
        body = flat(NL)
        for name in (
            "NL-INLINE-2024",
            "NL-INLINE-2024-GAAP-OTHER",
            "NL-INLINE-MULTI-TARGET",
            "NT16",
            "NT20",
        ):
            self.has(f"`{name}`", body)

    def test_calc_11_section_4_1_is_stated_exactly(self) -> None:
        body = flat(NL)
        self.lacks("§4.1 extends that to XBRL 2.1", body)
        self.has("MUST NOT be applied to them", body)

    def test_inf_rule_is_sourced_to_kvk_filing_rules(self) -> None:
        rows = [
            line
            for line in text(NL).splitlines()
            if line.startswith("| Numeric attributes |")
        ]
        self.assertEqual(len(rows), 1)
        self.assertNotIn("INF", rows[0])
        body = flat(NL)
        self.matches(r"FR-KVK-5\.01[^.]*INF", body)

    def test_rts_2026_delta_census_is_complete(self) -> None:
        body = flat(NL)
        self.lacks("small Annex IV wording changes may be missing", body)
        self.matches(
            r"Chapter 3 Annex I[^.]*NT21[^.]*NT18|Chapter 3 Annex I[^.]*NT18[^.]*NT21",
            body,
        )


class TaxonomiesSources(Claims):
    def test_frc_use_policy_is_cited_apart_from_acceptance(self) -> None:
        body = flat(TAX)
        idx = body.index("penultimate")
        window = body[idx - 400 : idx + 900]
        self.has("§6.6", window)
        self.has("Companies House", window)
        self.matches(r"2026, 2025, 2024, 2023 and 2022", window)


if __name__ == "__main__":
    unittest.main()
