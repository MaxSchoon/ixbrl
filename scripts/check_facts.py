#!/usr/bin/env python3
"""Pre-flight sanity check for an iXBRL document.

Runs cheap, deterministic checks BEFORE invoking Arelle. Catches the
silent-failure category of mistakes preparers most often make.

Checks performed:
  - Every ix:nonFraction has contextRef, unitRef, and exactly one of
    decimals, precision, or xsi:nil="true".
  - Every ix:nonNumeric has contextRef. Where @escape is true, in either of
    its boolean spellings, the body is treated as XHTML and flagged if it
    does not parse.
  - Continuation chains (continuedAt → ix:continuation@id) resolve, are
    referenced at most once each, and contain no cycles.
  - A finite @decimals does not zero out non-zero digits of the reported
    value (EDGAR XBRL Guide 9.5, validation EFM 6.5.37).
  - All contextRef values resolve to a defined xbrli:context.
  - All unitRef values resolve to a defined xbrli:unit.
  - Currency unit measures match ISO 4217 alpha-3 patterns.

NOT checked here, on purpose: whether duplicate facts report consistent
values. Deciding that needs the semantics of contexts, units, targets, nil and
the normative duplicate-consistency rule, which is a model of the report
rather than a reading of the document. Arelle already has that model; a
cheaper imitation of it was wrong in both directions. Run Arelle for it.

Usage:
  python check_facts.py <ixbrl.xhtml>

A fact whose reported value cannot be decoded here, because @format names a
transformation this script does not implement, because the value comes from
descendant or continued content, or because the text is not a number, is
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
from pathlib import Path

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

# A currency measure is identified by this namespace and its local part, not by
# the prefix a document happens to bind to it. Matching the literal string
# "iso4217:" skipped a measure under any other prefix, and accepted one whose
# prefix was bound somewhere else entirely.
ISO_4217_NS = "http://www.xbrl.org/2003/iso4217"


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
# A transformation is named by an EXPANDED QName, so the namespace and the
# local part identify it together. Validating them separately would accept a
# pairing that no registry publishes, such as an early namespace combined with
# a name introduced years later.
# Only the two modern registries are decoded. TR1 to TR3 state materially
# different input grammars for the same conventions, including three-digit
# grouping and a different treatment of spaces around the decimal mark, so one
# shared decoder cannot honour all of them: the grammar that is right for TR4
# is too permissive for TR3. A legacy transformation is therefore declined and
# reported as a coverage gap, rather than decoded by a grammar that is not its
# own and given a confident EFM verdict it has not earned.
TR4 = "http://www.xbrl.org/inlineXBRL/transformation/2020-02-12"
TR5 = "http://www.xbrl.org/inlineXBRL/transformation/2022-02-16"

ASCII_DIGITS = frozenset("0123456789")

# An NCName, optionally prefixed by one. @format is checked against this before
# resolution, because `:num-dot-decimal` has an empty prefix that a bare
# rpartition reads as "no prefix", resolving it against the default namespace
# as though it were well formed.
#
# NCNames are not ASCII. `xmlns:é` is a legal binding, so an ASCII-only start
# character would decline a conformant document. `[^\W\d]` is the Unicode-aware
# spelling of "a word character that is not a digit", which is letters and the
# underscore; `\w` then admits digits and combining marks in later positions.
_NCNAME = r"[^\W\d][\w.\-\u00b7]*"
QNAME = re.compile(rf"(?:{_NCNAME}:)?{_NCNAME}")

# Exactly the characters the input patterns of `num-dot-decimal-apos` and
# `num-comma-decimal-apos` accept as the group separator. U+FF07 FULLWIDTH
# APOSTROPHE belongs only to `num-unit-decimal-apos`, which this module
# declines, so accepting it here would decode a document the registry does not.
APOSTROPHES = "'\u0060\u00b4\u2019\u2032"
SPACES = " \u00a0"

# (namespace, local name) -> (group separators, decimal mark). Only
# transformations whose sole effect is the separator convention appear here.
# `num-unit-decimal` and its apos variant are absent on purpose: their trailing
# group is the fraction rather than a thousands group, so reading one means
# implementing the transformation, not reading a separator.
#
# The apostrophe variants ADD the apostrophes to the base separator; they do
# not replace it, so `1,234.56` is valid under `num-dot-decimal-apos`.
_DOT = (",", ".")
_COMMA = (".", ",")
_DOT_APOS = ("," + APOSTROPHES, ".")
_COMMA_APOS = ("." + APOSTROPHES, ",")
# Each pairing below was confirmed against that registry's own specification.
SEPARATOR_FORMATS = {
    **{(ns, "num-dot-decimal"): _DOT for ns in (TR4, TR5)},
    **{(ns, "num-comma-decimal"): _COMMA for ns in (TR4, TR5)},
    (TR5, "num-dot-decimal-apos"): _DOT_APOS,
    (TR5, "num-comma-decimal-apos"): _COMMA_APOS,
}


def split_qname(el: etree._Element, value: str) -> tuple[str | None, str]:
    """Resolve a QName-valued element body to (namespace, local part).

    The namespace is what identifies the name; the prefix is only how this
    document spells it. Reading the prefix instead means a measure written
    `curr:USD` is missed and one written `iso4217:USD` under a prefix bound
    elsewhere is mistaken for a currency.
    """
    prefix, _, local = value.rpartition(":")
    return el.nsmap.get(prefix or None), local or value


def resolve_transformation(
    el: etree._Element, raw_format: str
) -> tuple[str, str] | None:
    """Resolve @format to a separator convention, or None to decline it.

    The name is a QName, so its prefix must resolve through the element's
    in-scope namespaces to a published registry namespace. Matching only the
    local part would decode `fake:num-dot-decimal` from an unrelated namespace
    as though it were the registry transformation of that name.
    """
    # xs:QName collapses whitespace, so a padded name is still that name.
    raw_format = collapse(raw_format)
    if not QNAME.fullmatch(raw_format):
        return None  # not a QName at all, so it names no transformation
    prefix, _, local = raw_format.rpartition(":")
    # An unprefixed name still resolves, through the default namespace.
    namespace = el.nsmap.get(prefix or None)
    if namespace is None:
        return None
    return SEPARATOR_FORMATS.get((namespace, local))


def collapse(text: str) -> str:
    """Apply XML `whiteSpace="collapse"`, which the registry patterns assume.

    Only the four XML whitespace characters take part. `str.strip()` also
    removes Unicode spaces such as U+2009 THIN SPACE, which collapsing does
    not, so a value surrounded by them would have been accepted as though the
    surrounding characters were not there.
    """
    for character in "\t\n\r":
        text = text.replace(character, " ")
    return re.sub(r" +", " ", text).strip(" ")


def decode_separators(text: str, groups: str, decimal_mark: str) -> str | None:
    """Strip the group separators, or None if the text does not fit the pattern.

    Follows the registry's own input pattern rather than a tidier one. The
    integer part is any run of digits and group separators, in any arrangement,
    and the fraction is digits and spaces after a single decimal mark. Runs of
    separators and a leading or trailing one are all permitted, so `1,,234.56`
    and `1. 5` are valid inputs and are decoded. An earlier version rejected
    them as malformed, which turned conformant documents into coverage gaps.

    Digits are ASCII only. `str.isdigit()` is true of Arabic-Indic and
    fullwidth digits, which these patterns do not admit and which `Decimal`
    would then parse into a number the document never stated.
    """
    if text.count(decimal_mark) > 1:
        return None
    whole, mark, fraction = text.partition(decimal_mark)
    if mark and not fraction:
        return None  # a decimal mark with nothing after it
    separators = groups + SPACES
    if any(c not in separators and c not in ASCII_DIGITS for c in whole):
        return None
    if any(c not in SPACES and c not in ASCII_DIGITS for c in fraction):
        return None
    whole = "".join(c for c in whole if c in ASCII_DIGITS)
    fraction = "".join(c for c in fraction if c in ASCII_DIGITS)
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
    text = collapse(el.text or "")
    if not text:
        return None

    # @format names a transformation from the registry, and the separator
    # convention is part of it: under `num-comma-decimal`, "1,5" is one and a
    # half. Stripping commas unconditionally turns that into fifteen.
    raw_format = el.get("format")
    if raw_format is None:
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
            places = int(collapse(scale))
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
    sign = collapse(el.get("sign") or "")
    if sign == "-":
        # copy_negate() flips the sign without consulting the decimal context.
        # Unary minus rounds to 28 significant digits, which silently dropped
        # the low-order digit of a long value before it could be tested.
        value = value.copy_negate()
    elif sign:
        # @sign is an enumeration whose only member is "-". Anything else is
        # not a value this script understands, and reading it as "not negative"
        # would report the wrong number with total confidence.
        return None
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
        # @escape is xs:boolean, so "1" is as true as "true".
        if (el.get("escape") or "").strip() in {"true", "1"}:
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
            txt = collapse(measure.text or "")
            namespace, code = split_qname(measure, txt)
            if namespace == ISO_4217_NS and not ISO_4217.match(code):
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
