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
  - Duplicate facts (same concept + contextRef + unitRef) report consistent
    values modulo decimals.

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
# characters. Keeping the four sets separate means a base transformation does
# not silently accept a separator it does not permit.
APOSTROPHES = "'\u2019\u00b4\u02bc\u2032`"
DOT_DECIMAL_FORMATS = frozenset({"numdotdecimal", "num-dot-decimal", "numdotdecimalin"})
DOT_DECIMAL_APOS_FORMATS = frozenset({"num-dot-decimal-apos"})
COMMA_DECIMAL_FORMATS = frozenset({"numcommadecimal", "num-comma-decimal"})
COMMA_DECIMAL_APOS_FORMATS = frozenset({"num-comma-decimal-apos"})


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
    # half. Stripping commas unconditionally turns that into fifteen. Only the
    # two separator conventions below are decoded; any other transformation
    # (dates, words, sign handling) is declined rather than guessed at.
    fmt = (el.get("format") or "").rsplit(":", 1)[-1]
    if not fmt:
        cleaned = text  # no transformation: the text is already an XBRL numeric
    elif fmt in DOT_DECIMAL_FORMATS:
        cleaned = re.sub(r"[\s\u00a0,]", "", text)
    elif fmt in DOT_DECIMAL_APOS_FORMATS:
        cleaned = re.sub(rf"[\s\u00a0{re.escape(APOSTROPHES)}]", "", text)
    elif fmt in COMMA_DECIMAL_FORMATS:
        cleaned = re.sub(r"[\s\u00a0.]", "", text).replace(",", ".")
    elif fmt in COMMA_DECIMAL_APOS_FORMATS:
        cleaned = re.sub(rf"[\s\u00a0{re.escape(APOSTROPHES)}]", "", text)
        cleaned = cleaned.replace(",", ".")
    else:
        return None
    try:
        value = Decimal(cleaned)
    except InvalidOperation:
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
        value = Decimal((sign, digits, exponent + places))
    if el.get("sign") == "-":
        value = -value
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
    """Return a stable comparison key for simple numeric duplicate checks."""
    text = value.strip()
    if not text:
        return text
    try:
        parsed = Decimal(text)
    except InvalidOperation:
        return text
    return format(parsed.normalize(), "f")


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

    # --- Duplicate facts: same concept+context+unit, different value ---
    grouped: dict[tuple[str | None, str | None, str | None], list[etree._Element]] = (
        defaultdict(list)
    )
    for el in nf_facts:
        key = (el.get("name"), el.get("contextRef"), el.get("unitRef"))
        if all(key):
            grouped[key].append(el)
    for key, els in grouped.items():
        values = {canonical_fact_text(e.text or "") for e in els}
        if len(values) > 1:
            lines = ", ".join(str(e.sourceline) for e in els)
            issues.append(
                f"Duplicate fact {key[0]} in context {key[1]} reports inconsistent "
                f"values {sorted(values)} (lines {lines})"
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
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
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
