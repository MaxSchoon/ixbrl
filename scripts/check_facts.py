#!/usr/bin/env python3
"""Pre-flight sanity check for an iXBRL document.

Runs cheap, deterministic checks BEFORE invoking Arelle. Catches the
silent-failure category of mistakes preparers most often make.

Checks performed:
  - Every ix:nonFraction has contextRef, unitRef, and exactly one of
    decimals, precision, or xsi:nil="true".
  - Every ix:nonNumeric has contextRef. If escape="true" the body is
    treated as XHTML; flag if it does not parse.
  - Continuation chains (continuedAt → ix:continuation@id) form a tree
    with no cycles, no dangling references, and a single root per chain.
  - A finite @decimals does not zero out non-zero digits of the reported
    value (EDGAR XBRL Guide 9.5, validation EFM 6.5.37).
  - All contextRef values resolve to a defined xbrli:context.
  - All unitRef values resolve to a defined xbrli:unit.
  - Currency unit measures match ISO 4217 alpha-3 patterns.
  - Duplicate facts (same expanded concept name + contextRef + unitRef) report
    values whose decimals intervals overlap, so a figure tagged twice at
    different roundings is not reported as a disagreement.

Usage:
  python check_facts.py <ixbrl.xhtml>

A fact whose @format names a transformation this script does not decode is
reported as a NOTE rather than judged. The note does not fail the run; it says
plainly what was not evaluated, so "OK" never overstates the coverage.

Exit codes: 0 = clean (notes do not fail the run); 1 = issues found, including
a document that is not well-formed XML; 2 = usage error; 127 = lxml missing.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from pathlib import Path
from typing import NamedTuple

try:
    from lxml import etree
except ImportError:
    sys.stderr.write("This script requires lxml. Install: pip install lxml\n")
    sys.exit(127)

NS = {
    "ix": "http://www.xbrl.org/2013/inlineXBRL",
    "xbrli": "http://www.xbrl.org/2003/instance",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xhtml": "http://www.w3.org/1999/xhtml",
}

# lxml takes prefixes for XPath/findall but Clark notation for attribute
# access, so derive the one from the other rather than repeating the URI.
XSI_NIL = f"{{{NS['xsi']}}}nil"

ISO_4217 = re.compile(r"^[A-Z]{3}$")

# Beyond this the fixed-point spelling of a value stops being a comparison key
# and starts being a memory cost. Reported amounts do not approach it.
MAX_CANONICAL_EXPONENT = 1000

# Transformations from the Inline XBRL Transformation Registry whose only
# effect on a numeric fact is the separator convention. Everything else in the
# registry is declined by fact_value() rather than guessed at.
# Names are matched on the local part, so both the hyphenated spellings of
# Transformation Registry 4/5 and the camelCase of the earlier registries hit.
# `num-unit-decimal` is deliberately absent: its final group is the fraction,
# not a thousands group, so it is a transformation rather than a separator
# convention and is declined like any other.
# Registry 5 gives the apostrophe grouping its own transformations rather than
# folding it into the base ones, and accepts several apostrophe-like
# Every published namespace of the Inline XBRL Transformation Registry. A
# transformation name is a QName, so the local part alone does not identify it:
# `fake:num-dot-decimal` in an unrelated namespace is a different name and must
# not be decoded as though it were the registry's.
TRANSFORM_NAMESPACES = frozenset(
    {
        "http://www.xbrl.org/inlineXBRL/transformation/2010-04-20",
        "http://www.xbrl.org/inlineXBRL/transformation/2011-07-31",
        "http://www.xbrl.org/inlineXBRL/transformation/2015-02-26",
        "http://www.xbrl.org/inlineXBRL/transformation/2020-02-12",
        "http://www.xbrl.org/inlineXBRL/transformation/2022-02-16",
    }
)

# Exactly the characters the input patterns of `num-dot-decimal-apos` and
# `num-comma-decimal-apos` accept as the group separator. U+FF07 FULLWIDTH
# APOSTROPHE belongs only to `num-unit-decimal-apos`, which this module
# declines, so accepting it here would decode a document the registry does not.
APOSTROPHES = "'\u0060\u00b4\u2019\u2032"
SPACES = " \u00a0"

# Local name -> (group separators, decimal mark). Only transformations whose
# sole effect is the separator convention appear here. `num-unit-decimal` and
# its apos variant are absent on purpose: their trailing group is the fraction
# rather than a thousands group, so reading one means implementing the
# transformation, not reading a separator.
SEPARATOR_FORMATS = {
    "numdotdecimal": (",", "."),
    "num-dot-decimal": (",", "."),
    "numdotdecimalin": (",", "."),
    "num-dot-decimal-apos": (APOSTROPHES, "."),
    "numcommadecimal": (".", ","),
    "num-comma-decimal": (".", ","),
    "num-comma-decimal-apos": (APOSTROPHES, ","),
}


def resolve_transformation(
    el: etree._Element, raw_format: str
) -> tuple[str, str] | None:
    """Resolve @format to a separator convention, or None to decline it.

    The name is a QName, so its prefix must resolve through the element's
    in-scope namespaces to a published registry namespace. Matching only the
    local part would decode `fake:num-dot-decimal` from an unrelated namespace
    as though it were the registry transformation of that name.
    """
    prefix, _, local = raw_format.rpartition(":")
    if not prefix:
        return None  # an unprefixed name is in no namespace, so in no registry
    if el.nsmap.get(prefix) not in TRANSFORM_NAMESPACES:
        return None
    return SEPARATOR_FORMATS.get(local)


def decode_separators(text: str, groups: str, decimal_mark: str) -> str | None:
    """Strip the group separators, or None if the text does not fit the grammar.

    Deliberately stricter than the registry's own input pattern, which permits
    runs of separators. Being stricter can only decline a document the registry
    would accept, and a decline is reported as a coverage gap; being laxer
    would silently invent a value from malformed text. Group width is not
    checked, because `numdotdecimalin` groups Indian-style rather than in
    threes.
    """
    if text.count(decimal_mark) > 1:
        return None
    whole, _, fraction = text.partition(decimal_mark)
    separators = groups + SPACES
    for part, allowed in ((whole, separators), (fraction, SPACES)):
        if not part:
            continue
        if part[0] in allowed or part[-1] in allowed:
            return None  # a leading or trailing separator is not a grouping
        previous_was_separator = False
        for char in part:
            is_separator = char in allowed
            if is_separator and previous_was_separator:
                return None  # adjacent separators are not a grouping
            if not is_separator and not char.isdigit():
                return None
            previous_was_separator = is_separator
    whole = "".join(c for c in whole if c not in separators)
    fraction = "".join(c for c in fraction if c not in SPACES)
    if not whole and not fraction:
        return None
    return f"{whole or '0'}.{fraction}" if fraction else whole


def fact_value(el: etree._Element) -> Decimal | None:
    """The numeric value an ix:nonFraction reports, or None if undecidable.

    The reported value is the rendered text adjusted by @scale and @sign, so
    all three are needed before any arithmetic rule can be applied to it.
    Returns None whenever the text cannot be read as a number with confidence:
    @format may name a transformation from the registry that this script does
    not implement, and guessing at one would produce confident nonsense. A
    check that cannot see the value must decline to judge it.
    """
    if len(el) or el.get("continuedAt"):
        # A nested or continued fact takes its value from descendant content,
        # which this function does not assemble. Reading `.text` alone would
        # silently judge a fragment of the value.
        return None
    text = (el.text or "").strip()
    if not text:
        return None

    # @format names a transformation from the registry, and the separator
    # convention is part of it: under `num-comma-decimal`, "1,5" is one and a
    # half. Stripping commas unconditionally turns that into fifteen.
    raw_format = el.get("format")
    if not raw_format:
        cleaned = text  # no transformation: the text is already an XBRL numeric
    else:
        convention = resolve_transformation(el, raw_format)
        if convention is None:
            return None
        decoded = decode_separators(text, *convention)
        if decoded is None:
            return None
        cleaned = decoded
    try:
        value = Decimal(cleaned)
    except InvalidOperation:
        return None
    if not value.is_finite():
        # "NaN" and "Infinity" are legal Decimal literals but not legal XBRL
        # numeric values. Accepting them would put a nonsense figure into a
        # finding message and hand a non-finite value to the arithmetic below.
        return None
    scale = el.get("scale")
    if scale is not None:
        try:
            places = int(scale)
        except ValueError:
            return None
        # Shift the exponent rather than calling scaleb(), which rounds to the
        # active decimal context and would drop a digit from a value longer
        # than 28 significant figures before it could ever be tested.
        sign, digits, exponent = value.as_tuple()
        if not isinstance(exponent, int):
            return None
        try:
            value = Decimal((sign, digits, exponent + places))
        except (OverflowError, ValueError, InvalidOperation):
            # A @scale far outside any real reporting range: the exponent will
            # not fit. That is a malformed document, but this checker's job is
            # to report rather than to crash on one.
            return None
    if el.get("sign") == "-":
        # copy_negate() flips the sign without consulting the decimal context.
        # Unary minus rounds to 28 significant digits, which silently dropped
        # the low-order digit of a long value before it could be tested.
        value = value.copy_negate()
    return value


def truncates_nonzero_digits(value: Decimal, decimals: str) -> bool:
    """Does this @decimals interpret a non-zero digit of `value` as zero?

    EDGAR XBRL Guide section 9.5: "If the decimals attribute of a numeric fact
    is not INF, then the value is interpreted as if certain digits were zero.
    An instance must not contain usage that cause non-zero digits to be
    interpreted as zero." Validation EFM 6.5.37.

    `decimals="d"` zeroes every digit below the 10**-d place, so the rule holds
    exactly when value * 10**d is an integer. The guide stresses that the test
    is asymmetric: a decimals FINER than the value's own accuracy is fine --
    1,000,000 may carry any decimals greater than -6 -- because zeroing digits
    that are already zero loses nothing. Only coarsening is an error.

    This is the decidable half of the decimals rules. Whether a filer SHOULD
    have used INF (guide section 6.6.4: INF for an exactly reported amount)
    depends on the accuracy of the underlying figure, which is not present in
    the document, so it is deliberately not checked here.
    """
    if decimals == "INF":
        return False  # infinite precision zeroes nothing
    try:
        places = int(decimals)
    except ValueError:
        return False
    # Exact coefficient arithmetic, not scaleb(): scaleb rounds to the active
    # decimal context (28 significant digits by default), so a value longer
    # than that would silently lose the very digit being tested.
    digits, exponent = value.as_tuple()[1:]
    if not isinstance(exponent, int):
        return False  # NaN or Infinity carries a string exponent
    shift = exponent + places
    if shift >= 0:
        return False  # no digit falls below the retained place
    dropped = digits[shift:]
    return any(dropped)


def canonical_fact_text(value: str) -> str:
    """Return a stable comparison key for simple numeric duplicate checks.

    Trailing zeros are stripped so that "1.50" and "1.5" compare equal, but the
    stripping is done on the coefficient rather than through normalize().
    normalize() rounds to the active decimal context, so two values differing
    only beyond the 28th significant digit collapsed to one key and their
    inconsistency went unreported. Non-finite input is returned as written:
    it is not a number, and signalling NaN raises inside normalize().
    """
    text = value.strip()
    if not text:
        return text
    try:
        parsed = Decimal(text)
    except InvalidOperation:
        return text
    if not parsed.is_finite():
        return text
    key = canonical_decimal(parsed)
    return text if key is None else key


class Interval(NamedTuple):
    """A range of values, with each endpoint either included or excluded."""

    lower: Fraction
    upper: Fraction
    lower_closed: bool
    upper_closed: bool


def intervals_share_a_value(intervals: list[Interval]) -> bool:
    """Is there a single value satisfying every one of these ranges?"""
    lower = max(i.lower for i in intervals)
    upper = min(i.upper for i in intervals)
    if lower < upper:
        return True
    if lower > upper:
        return False
    # The ranges meet at exactly one point, which counts only if every range
    # that reaches it includes it.
    return all(i.lower_closed for i in intervals if i.lower == lower) and all(
        i.upper_closed for i in intervals if i.upper == upper
    )


def expand_qname(el: etree._Element, name: str | None) -> str | None:
    """Expand a QName attribute to `{namespace}local`, or None if unresolvable.

    Concept identity in XBRL is the expanded name. Two prefixes bound to one
    namespace name the same concept, and the same prefix in different scopes
    can name different concepts, so the lexical string is not an identity.
    """
    if not name:
        return None
    prefix, _, local = name.rpartition(":")
    if not local:
        return None
    namespace = el.nsmap.get(prefix or None)
    return f"{{{namespace}}}{local}" if namespace else None


def reported_interval(el: etree._Element) -> Interval | None:
    """Values this fact is consistent with, as a possibly half-open range.

    A numeric fact does not assert a point. `decimals` states the place to
    which the value is accurate, so a fact reported as 45,000 with
    `decimals="-3"` asserts only that the true amount lies within half a
    thousand of it. `INF` is the degenerate case that does assert a point.

    Whether the endpoints belong to the range depends on parity, because
    XBRL 2.1 section 4.6.7.2 defines "correct to n decimal places" by IEEE 754
    **roundTiesToEven**, not by rounding halves up. A tie goes to whichever
    neighbour is even, so the half-way points bound an ODD reported value from
    outside and an EVEN one from inside:

        5 at decimals="0"  ->  (4.5, 5.5)   4.5 ties down to 4, 5.5 up to 6
        6 at decimals="0"  ->  [5.5, 6.5]   both ties land on 6

    The two therefore share no value and are correctly reported as
    inconsistent, while two facts that agree to the accuracy each one claims
    overlap and are not. The spec's own worked example is 123450 correct to
    -2 decimal places, which is 123400 rather than 123500.
    """
    value = fact_value(el)
    if value is None:
        return None
    decimals = el.get("decimals")
    if decimals is None:
        return None  # @precision or a missing attribute: already reported above
    exact = Fraction(value)
    if decimals == "INF":
        return Interval(exact, exact, True, True)
    try:
        places = int(decimals)
    except ValueError:
        return None
    try:
        unit = Fraction(10) ** -places
    except (OverflowError, ValueError, ZeroDivisionError):
        return None
    half = unit / 2
    # A reported value whose last retained digit is even keeps both ties, so
    # its endpoints are included. An odd one loses both, so they are not. A
    # value that is not a whole multiple of its own unit is already reported
    # as an EFM 6.5.37 truncation, and is treated inclusively here so that
    # this check does not pile a second, derived complaint on top of it.
    multiple = exact / unit
    closed = multiple.denominator != 1 or multiple.numerator % 2 == 0
    return Interval(exact - half, exact + half, closed, closed)


def describe_reported(el: etree._Element) -> str:
    """How to name this fact's value in a finding, for a human reading it."""
    value = fact_value(el)
    if value is None:
        return (el.text or "").strip()
    canonical = canonical_decimal(value)
    return canonical if canonical is not None else str(value)


def canonical_decimal(parsed: Decimal) -> str | None:
    """Canonical string for a decoded value, or None if it has no exact form.

    Both duplicate-comparison paths go through here so that a decoded value and
    a raw text value are canonicalised the same way. They were not, and "5"
    against "5.0" was briefly reported as an inconsistency.
    """
    sign, digits, exponent = parsed.as_tuple()
    if not isinstance(exponent, int):
        return None
    if abs(exponent) > MAX_CANONICAL_EXPONENT:
        # format(..., "f") writes the value out in full, so an exponent like
        # 1E+100000 would build a hundred-thousand-character key. No real
        # reported amount needs one, and a crafted document should not be able
        # to spend memory here.
        return None
    digits = list(digits)
    while exponent < 0 and digits and digits[-1] == 0:
        digits.pop()
        exponent += 1
    if not digits:
        digits, exponent = [0], 0
    if not any(digits):
        # Negative zero is the same reported amount as zero. Keeping the sign
        # would make a fact pair of "0" and "-0" compare unequal and be
        # reported as an inconsistency that is not one.
        sign = 0
    return format(Decimal((sign, tuple(digits), exponent)), "f")


def find_facts(
    root: etree._Element,
) -> tuple[list[etree._Element], list[etree._Element], list[etree._Element]]:
    nf = root.findall(".//ix:nonFraction", NS)
    nn = root.findall(".//ix:nonNumeric", NS)
    cont = root.findall(".//ix:continuation", NS)
    return nf, nn, cont


def secure_parser() -> etree.XMLParser:
    """Return an lxml parser hardened against XXE and entity-expansion attacks.

    An iXBRL document handed to this script is untrusted input. lxml's
    default parser resolves entities, which opens the classic XML External
    Entity vectors: an external entity can disclose local files, and nested
    internal entities ("billion laughs") can exhaust memory. Conformant
    iXBRL is self-contained XHTML using numeric character references, so
    disabling entity resolution and external-DTD loading closes the attack
    surface at no cost to legitimate documents. See the lxml FAQ, "How do I
    use lxml safely as a web service endpoint?" (https://lxml.de/FAQ.html).
    """
    return etree.XMLParser(
        recover=False,
        ns_clean=True,
        resolve_entities=False,
        no_network=True,
        load_dtd=False,
        dtd_validation=False,
    )


def check(path: Path) -> list[str]:
    parser = secure_parser()
    try:
        tree = etree.parse(str(path), parser)
    except etree.XMLSyntaxError as exc:
        # The whole point of a pre-flight check is to be pointed at documents
        # that may be broken. Report the breakage as the finding it is; a
        # traceback tells the preparer nothing they can act on.
        return [f"{path.name} is not well-formed XML: {exc}"]
    root = tree.getroot()
    if root is None:
        return [f"{path.name} parsed but has no root element"]
    issues: list[str] = []

    nf_facts, nn_facts, continuations = find_facts(root)
    # Facts whose reported value this script could not decode, and which the
    # decimals check therefore did not evaluate, for any reason. Counted
    # rather than dropped: a
    # check that quietly covers less than it appears to is worse than one that
    # says so, and "no issues found" would otherwise overstate the coverage.
    undecodable = 0
    # Duplicate-fact groups in which at least one member could not be decoded,
    # so the group's consistency is unknown rather than confirmed.
    undecidable_groups = 0

    # --- ix:nonFraction required attributes ---
    for el in nf_facts:
        for attr in ("contextRef", "unitRef"):
            if not el.get(attr):
                issues.append(f"ix:nonFraction missing @{attr} at line {el.sourceline}")
        decimals_present = bool(el.get("decimals"))
        precision_present = bool(el.get("precision"))
        nil_value = (el.get(XSI_NIL) or "").lower()
        nil_present = nil_value in {"true", "1"}
        present_count = sum((decimals_present, precision_present, nil_present))
        if present_count == 0:
            issues.append(
                "ix:nonFraction missing @decimals, @precision or "
                f"xsi:nil='true' at line {el.sourceline}"
            )
        elif present_count > 1:
            issues.append(
                "ix:nonFraction has mutually exclusive attributes set "
                f"(decimals, precision, xsi:nil) at line {el.sourceline}"
            )
        decimals = el.get("decimals")
        if decimals and not nil_present:
            value = fact_value(el)
            if value is None:
                undecodable += 1
            elif truncates_nonzero_digits(value, decimals):
                issues.append(
                    f"ix:nonFraction at line {el.sourceline} has decimals="
                    f"'{decimals}', which interprets non-zero digits of "
                    f"{value} as zero (EFM 6.5.37)"
                )

    # --- ix:nonNumeric required attributes ---
    for el in nn_facts:
        if not el.get("contextRef"):
            issues.append(f"ix:nonNumeric missing @contextRef at line {el.sourceline}")
        if el.get("escape") == "true":
            try:
                etree.fromstring(f"<wrap>{el.text or ''}</wrap>", parser)
            except etree.XMLSyntaxError as exc:
                issues.append(
                    f"ix:nonNumeric escape='true' content not well-formed at "
                    f"line {el.sourceline}: {exc}"
                )

    # --- Context resolution ---
    defined_contexts = {
        c.get("id") for c in root.findall(".//xbrli:context", NS) if c.get("id")
    }
    defined_units = {
        u.get("id") for u in root.findall(".//xbrli:unit", NS) if u.get("id")
    }
    for el in nf_facts + nn_facts:
        cref = el.get("contextRef")
        if cref and cref not in defined_contexts:
            issues.append(f"contextRef='{cref}' not defined (line {el.sourceline})")
    for el in nf_facts:
        uref = el.get("unitRef")
        if uref and uref not in defined_units:
            issues.append(f"unitRef='{uref}' not defined (line {el.sourceline})")

    # --- Currency unit sanity ---
    for u in root.findall(".//xbrli:unit", NS):
        for measure in u.findall(".//xbrli:measure", NS):
            txt = (measure.text or "").strip()
            if txt.startswith("iso4217:"):
                code = txt.split(":", 1)[1]
                if not ISO_4217.match(code):
                    issues.append(
                        f"unit @id='{u.get('id')}' has non-ISO-4217 measure '{txt}'"
                    )

    # --- Continuation chains ---
    # Built with an explicit loop rather than a comprehension so the keys narrow
    # to str: `.get("id")` returns `str | None`, and a truthiness filter inside a
    # comprehension does not narrow the key type for a checker.
    cont_by_id: dict[str, etree._Element] = {}
    for continuation in continuations:
        continuation_id = continuation.get("id")
        if continuation_id:
            cont_by_id[continuation_id] = continuation
    starters = nf_facts + nn_facts + list(continuations)
    targets = defaultdict(int)
    for el in starters:
        ref = el.get("continuedAt")
        if ref:
            targets[ref] += 1
            if ref not in cont_by_id:
                issues.append(
                    f"continuedAt='{ref}' has no matching ix:continuation@id "
                    f"(line {el.sourceline})"
                )
    for ref, count in targets.items():
        if count > 1:
            issues.append(
                f"continuation id='{ref}' is the target of {count} continuedAt "
                f"attributes (must be unique)"
            )

    next_ref = {cid: c.get("continuedAt") for cid, c in cont_by_id.items()}

    # Walk iteratively, not recursively. @continuedAt is single-valued, so a
    # continuation chain is a linked list rather than a branching tree — the
    # recursion bought nothing and capped usable chain length at Python's
    # recursion limit (~1000). Long narrative disclosures exceed that routinely,
    # and the failure was a RecursionError traceback rather than a finding.
    UNVISITED, IN_PROGRESS, DONE = 0, 1, 2
    state: dict[str, int] = {}

    def walk_chain(start: str) -> None:
        path: list[str] = []
        cid = start
        while True:
            current = state.get(cid, UNVISITED)
            if current == IN_PROGRESS:
                # Re-entered a node on the path we are currently walking.
                cycle = [*path[path.index(cid) :], cid] if cid in path else [cid]
                issues.append(f"continuation cycle detected: {' -> '.join(cycle)}")
                break
            if current == DONE:
                break  # already resolved by an earlier chain
            state[cid] = IN_PROGRESS
            path.append(cid)
            nxt = next_ref.get(cid)
            if nxt is None or nxt not in cont_by_id:
                break  # end of chain, or a dangling ref already reported above
            cid = nxt
        for node in path:
            state[node] = DONE

    for cid in cont_by_id:
        walk_chain(cid)

    # --- Duplicate facts: same concept+context+unit, inconsistent values ---
    # The concept is identified by its EXPANDED name. @name is a QName, so two
    # prefixes bound to the same namespace name the same concept, and comparing
    # the lexical strings would treat `e:Assets` and `f:Assets` as unrelated.
    grouped: dict[tuple[str, str, str], list[etree._Element]] = defaultdict(list)
    for el in nf_facts:
        expanded = expand_qname(el, el.get("name"))
        context = el.get("contextRef")
        unit = el.get("unitRef")
        if expanded and context and unit:
            grouped[(expanded, context, unit)] = grouped[(expanded, context, unit)]
            grouped[(expanded, context, unit)].append(el)
    for group_key, els in grouped.items():
        if len(els) < 2:
            continue
        intervals = [reported_interval(e) for e in els]
        if any(interval is None for interval in intervals):
            # One member could not be decoded, so nothing can be concluded
            # about the group. Reporting an inconsistency here would compare a
            # decoded value against raw text, and staying silent would imply
            # the group was checked and agreed.
            undecidable_groups += 1
            continue
        bounded = [i for i in intervals if i is not None]
        if not intervals_share_a_value(bounded):
            lines = ", ".join(str(e.sourceline) for e in els)
            shown = sorted({describe_reported(e) for e in els})
            concept = group_key[0].rpartition("}")[2] or group_key[0]
            issues.append(
                f"Duplicate fact {concept} in context {group_key[1]} reports "
                f"inconsistent values {shown} (lines {lines})"
            )

    if undecidable_groups:
        issues.append(
            f"NOTE: {undecidable_groups} duplicate-fact group(s) contained a "
            "value this script could not decode, so their consistency was not "
            "determined either way."
        )

    if undecodable:
        issues.append(
            f"NOTE: {undecodable} numeric fact(s) had a reported value this "
            "script could not decode (an unsupported @format, a nested or "
            "continued fact, or text that is not a number), so EFM 6.5.37 was "
            "not evaluated for them. Arelle checks these; this is a coverage "
            "gap, not a defect."
        )

    return issues


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        # `exists()` is true for a directory, which then raised deep inside the
        # parser. The operator gets a usage error instead.
        problem = "Not a file" if path.exists() else "File not found"
        print(f"{problem}: {path}", file=sys.stderr)
        return 2
    findings = check(path)
    # A NOTE reports what could not be evaluated, so it is not a defect and
    # must not fail the run. It is still printed: a coverage gap the operator
    # cannot see is the same as no gap at all.
    notes = [f for f in findings if f.startswith("NOTE")]
    issues = [f for f in findings if not f.startswith("NOTE")]
    if issues:
        print(f"{len(issues)} issue(s) in {path.name}:")
        for i, msg in enumerate(issues, 1):
            print(f"  {i}. {msg}")
    else:
        print(f"OK: {path.name} passes pre-flight checks.")
    for note in notes:
        print(f"  {note}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
