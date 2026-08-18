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

import io
import sys
import tempfile
import unittest
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import check_facts
from check_facts import truncates_nonzero_digits

# `ixt` and the concept prefixes must be DECLARED, not merely written. A
# transformation name and a concept name are both QNames, and the checker
# resolves them through the in-scope namespaces. Fixtures that used an
# undeclared prefix were exercising unresolved names and proved nothing about
# the resolved path.
IXT_NS = "http://www.xbrl.org/inlineXBRL/transformation/2022-02-16"
ENTITY_NS = "http://example.com/entity"
NS_DECL = (
    'xmlns="http://www.w3.org/1999/xhtml" '
    'xmlns:ix="http://www.xbrl.org/2013/inlineXBRL" '
    'xmlns:xbrli="http://www.xbrl.org/2003/instance" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
    f'xmlns:ixt="{IXT_NS}" '
    'xmlns:ixt3="http://www.xbrl.org/inlineXBRL/transformation/2015-02-26" '
    f'xmlns:e="{ENTITY_NS}" '
    f'xmlns:f="{ENTITY_NS}" '
    'xmlns:fake="http://example.com/not-the-registry"'
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

    def defects(self, document):
        """Findings only, with coverage notes filtered out.

        A NOTE reports what the checker could not evaluate. It is not a defect
        in the document, so a test for "clean" must not trip over one.
        """
        return [i for i in self.run_on(document) if not i.startswith("NOTE")]

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
                flagged = any(
                    "6.5.37" in i and not i.startswith("NOTE") for i in issues
                )
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
                self.assertEqual(self.defects(self._fact("1000000", decimals)), [])

    def test_decimals_coarser_than_the_value_is_flagged(self):
        """-7 would zero the leading 1 of 1,000,000."""
        issues = self.run_on(self._fact("1000000", "-7"))
        self.assertTrue(
            any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
            f"got {issues}",
        )

    def test_exact_value_with_inf_is_never_flagged(self):
        """INF is prescribed for an exact amount (guide section 6.6.4)."""
        for value in ("1234.56", "45000", "0.0325", "1000000"):
            with self.subTest(value=value):
                self.assertEqual(self.defects(self._fact(value, "INF")), [])

    def test_scale_is_applied_before_the_check(self):
        """@scale changes the reported value, so it changes the verdict.

        Text 45 with scale=3 reports 45000. decimals=-3 zeroes nothing there
        and must pass; decimals=-6 would zero the 45 and must fail.
        """
        self.assertEqual(self.defects(self._fact("45", "-3", ' scale="3"')), [])
        issues = self.run_on(self._fact("45", "-6", ' scale="3"'))
        self.assertTrue(
            any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
            f"got {issues}",
        )

    def test_unreadable_value_is_not_judged(self):
        """A value this script cannot parse must produce no truncation verdict.

        @format may name a transformation from the registry that is not
        implemented here. Guessing would produce confident nonsense.
        """
        issues = self.run_on(self._fact("twelve thousand", "-3"))
        self.assertFalse(
            any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
            f"got {issues}",
        )

    def test_dot_decimal_transformation_is_read(self):
        """Commas are separators only when @format says so."""
        issues = self.run_on(
            self._fact("1,234.56", "-2", ' format="ixt:num-dot-decimal"')
        )
        self.assertTrue(
            any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
            f"got {issues}",
        )

    def test_comma_decimal_transformation_is_not_read_as_dot(self):
        """Under num-comma-decimal, "1,5" is one and a half, not fifteen.

        Stripping commas unconditionally read it as 15, which is exact at
        decimals="0" and so passed. The real value 1.5 must be flagged.
        """
        issues = self.run_on(self._fact("1,5", "0", ' format="ixt:num-comma-decimal"'))
        self.assertTrue(
            any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
            f"got {issues}",
        )
        # And its thousands separator is the dot.
        self.assertEqual(
            self.run_on(self._fact("1.234,56", "2", ' format="ixt:num-comma-decimal"')),
            [],
        )

    def test_apostrophe_separator_variants(self):
        """Registry 5 -apos forms use the apostrophe as the thousands mark."""
        self.assertEqual(
            self.defects(
                self._fact("1'234.56", "2", ' format="ixt:num-dot-decimal-apos"')
            ),
            [],
        )
        issues = self.run_on(
            self._fact("1'234,56", "0", ' format="ixt:num-comma-decimal-apos"')
        )
        self.assertTrue(
            any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
            f"got {issues}",
        )

    def test_unknown_transformation_is_declined(self):
        """A transformation this script does not decode yields no verdict."""
        issues = self.run_on(
            self._fact("1,234.56", "-2", ' format="ixt:num-unit-decimal"')
        )
        self.assertFalse(
            any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
            f"got {issues}",
        )

    def test_separators_without_a_format_are_not_assumed(self):
        """No @format means the text is already an XBRL numeric value.

        Commas are not valid there, so the value is undecodable rather than
        silently reinterpreted.
        """
        issues = self.run_on(self._fact("1,234.56", "-2"))
        self.assertFalse(
            any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
            f"got {issues}",
        )

    def test_value_longer_than_the_decimal_context_is_exact(self):
        """Regression: scaleb() rounded to 28 significant digits.

        The trailing .1 was rounded away before the integer test, so a value
        that plainly truncates at decimals="0" passed.
        """
        issues = self.run_on(self._fact("10000000000000000000000000000.1", "0"))
        self.assertTrue(
            any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
            f"got {issues}",
        )

    def test_nested_fact_is_declined(self):
        """A fact whose value comes from child content is not judged on .text."""
        body = (
            CONTEXT_AND_UNIT + '<ix:nonFraction name="e:A" contextRef="c1"'
            ' unitRef="u1" decimals="0"><span>2345.67</span></ix:nonFraction>'
        )
        issues = self.run_on(doc(body))
        self.assertFalse(
            any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
            f"got {issues}",
        )

    def test_sign_attribute_is_applied(self):
        """Conformant iXBRL puts the minus in @sign, not the text."""
        cases = [("INF", False), ("2", False), ("0", True), ("-3", True)]
        for decimals, should_flag in cases:
            with self.subTest(decimals=decimals):
                issues = self.run_on(self._fact("2345.67", decimals, ' sign="-"'))
                self.assertEqual(
                    any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
                    should_flag,
                    f"got {issues}",
                )

    def test_truncation_matches_exact_rational_arithmetic(self):
        """Differential test against an independent oracle.

        The rule is that value * 10**decimals must be an integer. Fraction
        computes that exactly and by a completely different route than the
        coefficient/exponent arithmetic under test, so the two agreeing across
        this grid is real evidence rather than a restatement of the
        implementation. The grid deliberately includes values longer than the
        default 28-digit decimal context, which is what the earlier scaleb()
        version got wrong.
        """
        values = [
            "-2345.67",
            "2345.67",
            "1000000",
            "1E+30",
            "1.000",
            "0",
            "0.0",
            "-0.5",
            "10000000000000000000000000000.1",
            "123456789012345678901234567890.5",
            "1.5",
            "0.0001",
            "-1234500",
            "9.99E-5",
            "1E-30",
        ]
        places = ["-9", "-7", "-6", "-3", "-2", "0", "2", "5", "9"]
        for literal in values:
            value = Decimal(literal)
            for decimals in places:
                with self.subTest(value=literal, decimals=decimals):
                    expected = (
                        Fraction(value) * Fraction(10) ** int(decimals)
                    ).denominator != 1
                    self.assertEqual(
                        truncates_nonzero_digits(value, decimals), expected
                    )
            with self.subTest(value=literal, decimals="INF"):
                self.assertFalse(truncates_nonzero_digits(value, "INF"))

    def test_scale_on_a_value_longer_than_the_decimal_context(self):
        """@scale must not round the value it is applied to.

        The exponent shift is exact; scaleb() would round to 28 significant
        digits and drop the trailing digit before it could be tested. Both a
        zero and a negative scale exercise the same path.
        """
        long_value = "10000000000000000000000000000.1"
        for scale in ("0", "-3"):
            with self.subTest(scale=scale):
                issues = self.run_on(self._fact(long_value, "0", f' scale="{scale}"'))
                self.assertTrue(
                    any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
                    f"scale={scale} got {issues}",
                )

    def test_note_names_the_uncovered_facts(self):
        """The coverage note must state the count and not fail the run."""
        body = (
            CONTEXT_AND_UNIT + '<ix:nonFraction name="e:A" contextRef="c1"'
            ' unitRef="u1" decimals="0" format="ixt:num-unit-decimal">12 34'
            "</ix:nonFraction>"
        )
        issues = self.run_on(doc(body))
        notes = [i for i in issues if i.startswith("NOTE")]
        self.assertEqual(len(notes), 1, f"got {issues}")
        self.assertIn("1 numeric fact", notes[0])
        self.assertEqual([i for i in issues if not i.startswith("NOTE")], [])

    def test_main_exit_code_ignores_notes(self):
        """A document whose only finding is a coverage note exits 0."""
        body = (
            CONTEXT_AND_UNIT + '<ix:nonFraction name="e:A" contextRef="c1"'
            ' unitRef="u1" decimals="0" format="ixt:num-unit-decimal">12 34'
            "</ix:nonFraction>"
        )
        with tempfile.NamedTemporaryFile(
            "w", suffix=".xhtml", delete=False, encoding="utf-8"
        ) as handle:
            handle.write(doc(body))
            temp = handle.name
        try:
            argv, stdout = sys.argv, sys.stdout
            sys.argv = ["check_facts.py", temp]
            sys.stdout = io.StringIO()
            try:
                code = check_facts.main()
                printed = sys.stdout.getvalue()
            finally:
                sys.argv, sys.stdout = argv, stdout
        finally:
            Path(temp).unlink()
        self.assertEqual(code, 0, printed)
        self.assertIn("NOTE", printed)
        self.assertIn("passes pre-flight checks", printed)

    def test_degenerate_values_are_declined_not_crashed(self):
        """Malformed input is a finding to report, never a traceback.

        "NaN" and "Infinity" parse as Decimal but are not legal XBRL numeric
        values, and an absurd @scale overflowed the exponent and raised.
        """
        cases = [
            ("NaN", ""),
            ("Infinity", ""),
            ("-Infinity", ""),
            ("45", ' scale="99999999999999999999"'),
            ("45", ' scale="-99999999999999999999"'),
            ("abc", ""),
            ("1.2.3", ""),
        ]
        for value, extra in cases:
            with self.subTest(value=value, extra=extra):
                issues = self.run_on(self._fact(value, "0", extra))
                self.assertFalse(
                    any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
                    f"got {issues}",
                )
                # Asserting only the absence of a verdict would also pass if
                # the fact were dropped entirely. The note is the evidence it
                # was seen and consciously declined.
                self.assertTrue(
                    any(i.startswith("NOTE") for i in issues),
                    f"declined without a coverage note: {issues}",
                )

    def test_sign_on_a_value_longer_than_the_decimal_context(self):
        """@sign must not round the value it negates.

        Unary minus consults the decimal context; copy_negate() does not. This
        combines @sign with @scale because that is the path that reintroduced
        the rounding after the parser itself had been fixed.
        """
        long_value = "10000000000000000000000000000.1"
        for extra in (' sign="-"', ' sign="-" scale="0"', ' sign="-" scale="-3"'):
            with self.subTest(extra=extra):
                issues = self.run_on(self._fact(long_value, "0", extra))
                self.assertTrue(
                    any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
                    f"{extra} got {issues}",
                )

    def test_apostrophe_set_matches_the_registry(self):
        """Only the separators the registry lists are decoded.

        The apos decimal transformations accept ASCII apostrophe, U+0060,
        U+00B4, U+2019 and U+2032. U+02BC is in no pattern at all, and U+FF07
        belongs only to num-unit-decimal-apos, which this module declines. A
        document using either is declined rather than reinterpreted.
        """
        for ch in "'\u0060\u00b4\u2019\u2032":
            with self.subTest(char=hex(ord(ch))):
                # Assert the value was DECODED, not merely that no defect was
                # reported: filtering notes out would let a decline pass here.
                # decimals="-2" truncates 1234.56, so a verdict proves the
                # separator was read and the value understood.
                issues = self.run_on(
                    self._fact(
                        f"1{ch}234.56", "-2", ' format="ixt:num-dot-decimal-apos"'
                    )
                )
                self.assertTrue(
                    any("1234.56" in i for i in issues), f"not decoded: {issues}"
                )
        for ch in "\u02bc\uff07":
            with self.subTest(declined=hex(ord(ch))):
                issues = self.run_on(
                    self._fact(
                        f"1{ch}234.56", "2", ' format="ixt:num-dot-decimal-apos"'
                    )
                )
                self.assertTrue(
                    any(i.startswith("NOTE") for i in issues), f"got {issues}"
                )

    def test_no_operation_consults_the_decimal_context(self):
        """Guard against the whole class of bug, not one more instance of it.

        Three separate rounding defects were fixed here in sequence: scaleb()
        in the predicate, scaleb() again in the parser, then unary minus and
        normalize(). Each was the same mistake in a new place. Running the
        decode-and-judge path under a deliberately tiny precision makes any
        context-sensitive operation change the answer, so a fourth instance
        fails here rather than reaching a filing.
        """
        long_value = "10000000000000000000000000000.1"
        for extra in ("", ' sign="-"', ' scale="0"', ' sign="-" scale="-3"'):
            with self.subTest(extra=extra):
                with localcontext() as ctx:
                    ctx.prec = 5
                    issues = self.run_on(self._fact(long_value, "0", extra))
                self.assertTrue(
                    any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
                    f"{extra} lost precision to the context: {issues}",
                )

    def test_transformation_namespace_must_be_the_registry(self):
        """@format is a QName; the local part alone does not identify it.

        `fake:num-dot-decimal` is a different name in a different namespace and
        must be declined, not decoded as the registry transformation.
        """
        issues = self.run_on(
            self._fact("1,234.56", "0", ' format="fake:num-dot-decimal"')
        )
        self.assertTrue(any(i.startswith("NOTE") for i in issues), f"got {issues}")
        self.assertFalse(
            any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
            f"got {issues}",
        )

    def test_malformed_transformation_input_is_declined(self):
        """Text that does not fit the grammar yields no value at all.

        Runs of separators, or one in a leading or trailing position, are not
        a grouping. Stripping them anyway would invent a number.
        """
        for text in ("1,,234.56", ",234", "1,234,", "1.2.3", "12a4"):
            with self.subTest(text=text):
                issues = self.run_on(
                    self._fact(text, "0", ' format="ixt:num-dot-decimal"')
                )
                self.assertTrue(
                    any(i.startswith("NOTE") for i in issues), f"{text}: {issues}"
                )

    def test_directory_argument_is_a_usage_error(self):
        """exists() is true for a directory, which then raised in the parser."""
        argv, stderr = sys.argv, sys.stderr
        sys.argv = ["check_facts.py", str(Path(__file__).parent)]
        sys.stderr = io.StringIO()
        try:
            code = check_facts.main()
        finally:
            sys.argv, sys.stderr = argv, stderr
        self.assertEqual(code, 2)

    def test_duplicate_consistency_is_deferred_to_arelle(self):
        """This checker must not judge whether duplicate facts agree.

        Deciding that needs semantic context and unit identity, target
        documents, nil handling and the normative duplicate-consistency rule.
        Four successive attempts at a cheaper version were each wrong in one
        direction or the other, so the rule is Arelle's. Two facts that plainly
        disagree must therefore produce no finding here, and this test exists
        to stop the rule creeping back in.
        """
        body = CONTEXT_AND_UNIT + "".join(
            '<ix:nonFraction name="e:A" contextRef="c1" unitRef="u1"'
            f' decimals="INF">{value}</ix:nonFraction>'
            for value in ("5", "6")
        )
        issues = self.run_on(doc(body))
        self.assertFalse(
            any("uplicate" in i or "inconsistent" in i for i in issues),
            f"the duplicate rule is back: {issues}",
        )

    def test_legacy_transformation_registries_are_declined(self):
        """TR1 to TR3 state different input grammars for the same conventions.

        One shared decoder cannot honour all of them, and the one that is right
        for TR4 is too permissive for TR3, which would put a confident EFM
        verdict on a value the registry never described that way.
        """
        issues = self.run_on(
            self._fact("1,234.56", "-2", ' format="ixt3:numdotdecimal"')
        )
        self.assertTrue(any(i.startswith("NOTE") for i in issues), f"got {issues}")

    def test_malformed_format_qnames_are_declined(self):
        """A name that is not a QName names no transformation.

        `:num-dot-decimal` has an empty prefix that a bare rpartition reads as
        "no prefix", which would resolve it against the default namespace as
        though it were well formed. An empty @format is present and invalid,
        not absent.
        """
        for bad in (":num-dot-decimal", "", "ixt:", "1bad:num-dot-decimal", "a:b:c"):
            with self.subTest(fmt=bad):
                issues = self.run_on(self._fact("1,234.56", "-2", f' format="{bad}"'))
                self.assertFalse(
                    any("6.5.37" in i and not i.startswith("NOTE") for i in issues),
                    f"{bad!r} was decoded: {issues}",
                )

    def test_escape_accepts_either_boolean_spelling(self):
        """@escape is xs:boolean, so "1" is as true as "true"."""
        for spelling in ("true", "1"):
            with self.subTest(escape=spelling):
                body = (
                    CONTEXT_AND_UNIT + '<ix:nonNumeric name="e:N" contextRef="c1"'
                    f' escape="{spelling}"><p>unclosed</ix:nonNumeric>'
                )
                issues = self.run_on(doc(body))
                self.assertTrue(
                    any("not well-formed" in i for i in issues), f"got {issues}"
                )

    def test_apostrophe_formats_also_accept_the_base_separator(self):
        """The apos transformations ADD apostrophes; they do not replace.

        Registry 5's input pattern for `num-dot-decimal-apos` admits the comma
        as well, so a conventionally grouped number is valid under it and must
        be decoded, not declined.
        """
        issues = self.run_on(
            self._fact("1,234.56", "-2", ' format="ixt:num-dot-decimal-apos"')
        )
        self.assertTrue(any("1234.56" in i for i in issues), f"not decoded: {issues}")

    def test_transformation_pairing_must_be_published(self):
        """A name is the namespace and the local part together.

        `num-dot-decimal-apos` exists only in Registry 5, so pairing it with
        Registry 3's namespace names nothing and must be declined. Each pairing
        in the table was confirmed against that registry's own specification.
        """
        issues = self.run_on(
            self._fact("1'234.56", "0", ' format="ixt3:num-dot-decimal-apos"')
        )
        self.assertTrue(any(i.startswith("NOTE") for i in issues), f"got {issues}")

    def test_non_ascii_digits_are_declined(self):
        """str.isdigit() is true of digits these patterns do not admit."""
        arabic_indic = "\u0661\u0662\u0663\u0664"
        fullwidth = "\uff11\uff12\uff13\uff14"
        for text in (arabic_indic, fullwidth):
            with self.subTest(text=text):
                issues = self.run_on(
                    self._fact(text, "0", ' format="ixt:num-dot-decimal"')
                )
                self.assertTrue(
                    any(i.startswith("NOTE") for i in issues), f"{text}: {issues}"
                )

    def test_trailing_decimal_mark_is_declined(self):
        """ "5." has no digits after the mark, which the grammar requires."""
        issues = self.run_on(self._fact("5.", "0", ' format="ixt:num-dot-decimal"'))
        self.assertTrue(any(i.startswith("NOTE") for i in issues), f"got {issues}")

    def test_default_namespace_resolves_a_transformation(self):
        """An unprefixed @format still resolves, through the default namespace."""
        body = (
            CONTEXT_AND_UNIT
            + '<ix:nonFraction xmlns="http://www.xbrl.org/inlineXBRL/transformation'
            '/2022-02-16" name="e:A" contextRef="c1" unitRef="u1" decimals="-2"'
            ' format="num-dot-decimal">1,234.56</ix:nonFraction>'
        )
        issues = self.run_on(doc(body))
        self.assertTrue(any("1234.56" in i for i in issues), f"not decoded: {issues}")

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


if __name__ == "__main__":
    unittest.main()
