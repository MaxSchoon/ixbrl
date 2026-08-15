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
        """A document that will not parse is the finding, not a traceback."""
        issues = self.run_on('<html xmlns="http://www.w3.org/1999/xhtml"><p>oops')
        self.assertEqual(len(issues), 1)
        self.assertIn("not well-formed XML", issues[0])

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

    def test_decimals_inf_is_flagged(self):
        body = (
            CONTEXT_AND_UNIT + '<ix:nonFraction name="e:A" contextRef="c1" unitRef="u1"'
            ' decimals="INF">5</ix:nonFraction>'
        )
        issues = self.run_on(doc(body))
        self.assertTrue(any("INF" in i for i in issues))

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
