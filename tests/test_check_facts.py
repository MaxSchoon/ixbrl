#!/usr/bin/env python3
"""Tests for scripts/check_facts.py.

The script had 257 lines of validation logic and no tests, which is how two
crashes shipped: a malformed document raised an unhandled XMLSyntaxError
(issue #5) and a long continuation chain raised RecursionError (issue #6). Both
are inputs the tool exists to diagnose.

Uses stdlib unittest, so it runs with no runner dependency -- matching the
repo's dependency-light convention. The script itself needs lxml.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import check_facts

NS_DECL = (
    'xmlns="http://www.w3.org/1999/xhtml" '
    'xmlns:ix="http://www.xbrl.org/2013/inlineXBRL" '
    'xmlns:xbrli="http://www.xbrl.org/2003/instance" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
)


def doc(body: str) -> str:
    return f"<html {NS_DECL}><body>{body}</body></html>"


CONTEXT_AND_UNIT = '<xbrli:context id="c1"/><xbrli:unit id="u1"/>'


class CheckFactsTestCase(unittest.TestCase):
    def run_on(self, xml: str) -> list[str]:
        with tempfile.NamedTemporaryFile(
            "w", suffix=".xhtml", delete=False, encoding="utf-8"
        ) as fh:
            fh.write(xml)
            path = Path(fh.name)
        try:
            return check_facts.check(path)
        finally:
            path.unlink()

    # ── issue #5 ────────────────────────────────────────────────────────────
    def test_malformed_xml_is_reported_not_raised(self):
        """A document that will not parse is the finding, not a traceback.

        Asserts the whole diagnostic, not just that it was caught: a preparer
        needs the file, the line and the column to act on it, and a test that
        checks only the phrase would still pass if those were dropped.
        """
        issues = self.run_on('<html xmlns="http://www.w3.org/1999/xhtml"><p>oops')
        self.assertEqual(len(issues), 1)
        finding = issues[0]
        self.assertIn("not well-formed XML", finding)
        self.assertIn(".xhtml", finding, "diagnostic must name the file")
        self.assertRegex(finding, r"line \d+", "diagnostic must give a line")
        self.assertRegex(finding, r"column \d+", "diagnostic must give a column")

    def test_empty_file_is_reported_not_raised(self):
        issues = self.run_on("")
        self.assertEqual(len(issues), 1)
        self.assertIn("not well-formed XML", issues[0])

    # ── issue #6 ────────────────────────────────────────────────────────────
    def test_long_continuation_chain_does_not_recurse(self):
        """A 5000-link chain must be walked, not blow the recursion limit."""
        n = 5000
        parts = ['<ix:nonNumeric contextRef="c1" continuedAt="k0">x</ix:nonNumeric>']
        for i in range(n):
            nxt = f' continuedAt="k{i + 1}"' if i < n - 1 else ""
            parts.append(f'<ix:continuation id="k{i}"{nxt}>t</ix:continuation>')
        issues = self.run_on(doc(CONTEXT_AND_UNIT + "".join(parts)))
        self.assertEqual(issues, [], f"unexpected findings: {issues[:3]}")

    def test_cycle_still_detected_after_derecursing(self):
        body = (
            CONTEXT_AND_UNIT
            + '<ix:continuation id="a" continuedAt="b">x</ix:continuation>'
            + '<ix:continuation id="b" continuedAt="a">y</ix:continuation>'
        )
        issues = self.run_on(doc(body))
        self.assertTrue(any("cycle detected" in i for i in issues), f"got {issues}")

    def test_dangling_continued_at_still_detected(self):
        body = (
            CONTEXT_AND_UNIT
            + '<ix:nonNumeric contextRef="c1" continuedAt="nope">x</ix:nonNumeric>'
        )
        issues = self.run_on(doc(body))
        self.assertTrue(any("no matching" in i for i in issues), f"got {issues}")

    def test_duplicate_continuation_target_still_detected(self):
        body = (
            CONTEXT_AND_UNIT
            + '<ix:nonNumeric contextRef="c1" continuedAt="k">a</ix:nonNumeric>'
            + '<ix:nonNumeric contextRef="c1" continuedAt="k">b</ix:nonNumeric>'
            + '<ix:continuation id="k">t</ix:continuation>'
        )
        issues = self.run_on(doc(body))
        self.assertTrue(any("must be unique" in i for i in issues), f"got {issues}")

    # ── existing behaviour must survive the fixes ───────────────────────────
    def test_clean_document_has_no_issues(self):
        body = (
            CONTEXT_AND_UNIT + '<ix:nonFraction name="e:A" contextRef="c1" unitRef="u1"'
            ' decimals="0">5</ix:nonFraction>'
        )
        self.assertEqual(self.run_on(doc(body)), [])

    def test_nil_satisfies_the_decimals_requirement(self):
        body = (
            CONTEXT_AND_UNIT + '<ix:nonFraction name="e:A" contextRef="c1" unitRef="u1"'
            ' xsi:nil="true"/>'
        )
        self.assertEqual(self.run_on(doc(body)), [])

    def test_decimals_and_nil_together_are_mutually_exclusive(self):
        body = (
            CONTEXT_AND_UNIT + '<ix:nonFraction name="e:A" contextRef="c1" unitRef="u1"'
            ' decimals="0" xsi:nil="true"/>'
        )
        issues = self.run_on(doc(body))
        self.assertTrue(any("mutually exclusive" in i for i in issues))

    def test_missing_decimals_precision_and_nil_is_flagged(self):
        body = (
            CONTEXT_AND_UNIT
            + '<ix:nonFraction name="e:A" contextRef="c1" unitRef="u1">'
            "7</ix:nonFraction>"
        )
        issues = self.run_on(doc(body))
        self.assertTrue(any("missing @decimals" in i for i in issues))

    def _fact(self, value, decimals, extra=""):
        return doc(
            CONTEXT_AND_UNIT + '<ix:nonFraction name="e:A" contextRef="c1"'
            f' unitRef="u1" decimals="{decimals}"{extra}>{value}</ix:nonFraction>'
        )

    def test_edgar_guide_truncation_examples(self):
        """The worked table from EDGAR XBRL Guide section 9.5, verbatim.

        Fact text -2345.67 against each decimals value, with the Result column
        the guide itself gives. These are the authority for EFM 6.5.37, so if
        the checker disagrees with any row, the checker is wrong.
        """
        cases = [
            ("INF", False),
            ("2", False),
            ("0", True),
            ("-2", True),
            ("-3", True),
            ("-6", True),
        ]
        for decimals, should_flag in cases:
            with self.subTest(decimals=decimals):
                issues = self.run_on(self._fact("-2345.67", decimals))
                flagged = any("6.5.37" in i for i in issues)
                self.assertEqual(flagged, should_flag, f"got {issues}")

    def test_decimals_finer_than_the_value_is_allowed(self):
        """The guide states the check is asymmetric.

        "a value such as 1,000,000 may have a decimals attribute with any value
        greater than -6". Zeroing digits that are already zero loses nothing,
        so only coarsening is an error. The previous version of this checker
        flagged exactly these conformant values.
        """
        for decimals in ("INF", "0", "-3", "-5", "-6"):
            with self.subTest(decimals=decimals):
                self.assertEqual(self.run_on(self._fact("1000000", decimals)), [])

    def test_decimals_coarser_than_the_value_is_flagged(self):
        """-7 would zero the leading 1 of 1,000,000."""
        issues = self.run_on(self._fact("1000000", "-7"))
        self.assertTrue(any("6.5.37" in i for i in issues), f"got {issues}")

    def test_exact_value_with_inf_is_never_flagged(self):
        """INF is prescribed for an exact amount (guide section 6.6.4)."""
        for value in ("1234.56", "45000", "0.0325", "1000000"):
            with self.subTest(value=value):
                self.assertEqual(self.run_on(self._fact(value, "INF")), [])

    def test_scale_is_applied_before_the_check(self):
        """@scale changes the reported value, so it changes the verdict.

        Text 45 with scale=3 reports 45000. decimals=-3 zeroes nothing there
        and must pass; decimals=-6 would zero the 45 and must fail.
        """
        self.assertEqual(self.run_on(self._fact("45", "-3", ' scale="3"')), [])
        issues = self.run_on(self._fact("45", "-6", ' scale="3"'))
        self.assertTrue(any("6.5.37" in i for i in issues), f"got {issues}")

    def test_unreadable_value_is_not_judged(self):
        """A value this script cannot parse must produce no truncation verdict.

        @format may name a transformation from the registry that is not
        implemented here. Guessing would produce confident nonsense.
        """
        issues = self.run_on(self._fact("twelve thousand", "-3"))
        self.assertFalse(any("6.5.37" in i for i in issues), f"got {issues}")

    def test_thousands_separators_are_read(self):
        issues = self.run_on(self._fact("1,234.56", "-2"))
        self.assertTrue(any("6.5.37" in i for i in issues), f"got {issues}")

    def test_unresolved_context_is_flagged(self):
        body = (
            CONTEXT_AND_UNIT
            + '<ix:nonFraction name="e:A" contextRef="nope" unitRef="u1"'
            ' decimals="0">5</ix:nonFraction>'
        )
        issues = self.run_on(doc(body))
        self.assertTrue(any("not defined" in i for i in issues))

    def test_non_iso4217_measure_is_flagged(self):
        body = (
            '<xbrli:context id="c1"/>'
            '<xbrli:unit id="u1">'
            "<xbrli:measure>iso4217:EUROS</xbrli:measure></xbrli:unit>"
        )
        issues = self.run_on(doc(body))
        self.assertTrue(any("non-ISO-4217" in i for i in issues))

    def test_inconsistent_duplicate_facts_are_flagged(self):
        body = (
            CONTEXT_AND_UNIT + '<ix:nonFraction name="e:A" contextRef="c1" unitRef="u1"'
            ' decimals="0">5</ix:nonFraction>'
            + '<ix:nonFraction name="e:A" contextRef="c1" unitRef="u1"'
            ' decimals="0">6</ix:nonFraction>'
        )
        issues = self.run_on(doc(body))
        self.assertTrue(any("inconsistent" in i for i in issues))

    def test_consistent_duplicate_facts_are_not_flagged(self):
        """iXBRL routinely tags the same number twice; that is not an error."""
        body = (
            CONTEXT_AND_UNIT + '<ix:nonFraction name="e:A" contextRef="c1" unitRef="u1"'
            ' decimals="0">5.0</ix:nonFraction>'
            + '<ix:nonFraction name="e:A" contextRef="c1" unitRef="u1"'
            ' decimals="0">5</ix:nonFraction>'
        )
        self.assertEqual(self.run_on(doc(body)), [])


if __name__ == "__main__":
    unittest.main()
