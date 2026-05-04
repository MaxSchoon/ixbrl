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
  - decimals="INF" not used (rejected by SEC EFM and discouraged in ESEF).
  - All contextRef values resolve to a defined xbrli:context.
  - All unitRef values resolve to a defined xbrli:unit.
  - Currency unit measures match ISO 4217 alpha-3 patterns.
  - Duplicate facts (same concept + contextRef + unitRef) report consistent
    values modulo decimals.

Usage:
  python check_facts.py <ixbrl.xhtml>

Exit code: 0 = clean, 1 = issues found (issues printed to stdout).
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

ISO_4217 = re.compile(r"^[A-Z]{3}$")


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


def check(path: Path) -> list[str]:
    parser = etree.XMLParser(recover=False, ns_clean=True)
    tree = etree.parse(str(path), parser)
    root = tree.getroot()
    issues: list[str] = []

    nf_facts, nn_facts, continuations = find_facts(root)

    # --- ix:nonFraction required attributes ---
    for el in nf_facts:
        for attr in ("contextRef", "unitRef"):
            if not el.get(attr):
                issues.append(f"ix:nonFraction missing @{attr} at line {el.sourceline}")
        decimals_present = bool(el.get("decimals"))
        precision_present = bool(el.get("precision"))
        nil_value = (
            el.get("{http://www.w3.org/2001/XMLSchema-instance}nil") or ""
        ).lower()
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
        if el.get("decimals") == "INF":
            issues.append(
                f"ix:nonFraction uses decimals='INF' at line {el.sourceline} "
                f"(rejected by SEC EFM; discouraged elsewhere)"
            )

    # --- ix:nonNumeric required attributes ---
    for el in nn_facts:
        if not el.get("contextRef"):
            issues.append(f"ix:nonNumeric missing @contextRef at line {el.sourceline}")
        if el.get("escape") == "true":
            try:
                etree.fromstring(f"<wrap>{el.text or ''}</wrap>")
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
            issues.append(
                f"contextRef='{cref}' not defined (line {el.sourceline})"
            )
    for el in nf_facts:
        uref = el.get("unitRef")
        if uref and uref not in defined_units:
            issues.append(
                f"unitRef='{uref}' not defined (line {el.sourceline})"
            )

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
    cont_by_id = {c.get("id"): c for c in continuations if c.get("id")}
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
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit_continuation(cid: str) -> None:
        current_state = state.get(cid, 0)
        if current_state == 1:
            cycle = stack[stack.index(cid):] + [cid] if cid in stack else [cid]
            issues.append(f"continuation cycle detected: {' -> '.join(cycle)}")
            return
        if current_state == 2:
            return

        state[cid] = 1
        stack.append(cid)
        ref = next_ref.get(cid)
        if ref in cont_by_id:
            visit_continuation(ref)
        stack.pop()
        state[cid] = 2

    for cid in cont_by_id:
        visit_continuation(cid)

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

    return issues


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2
    issues = check(path)
    if not issues:
        print(f"OK — {path.name} passes pre-flight checks.")
        return 0
    print(f"{len(issues)} issue(s) in {path.name}:")
    for i, msg in enumerate(issues, 1):
        print(f"  {i}. {msg}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
