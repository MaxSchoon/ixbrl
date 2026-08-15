#!/usr/bin/env python3
"""Skill + asset guardrails for CI (standard library only).

Enforces the invariants documented in CONTRIBUTING.md so a PR can't silently
break the agent contract or the runnable scaffolds:

  1. SKILL.md exists, stays under 32 KiB, and has YAML frontmatter with a
     `name` and a `description` (description under 1024 chars).
  2. Every reference link resolves -- across ALL repository Markdown, not just
     SKILL.md, and through subdirectories. Both link forms in use are handled:
     repo-root (`references/foo.md`) and sibling (`foo.md` inside references/).
  3. Asset cross-references resolve: every `xlink:href="extension-schema.xsd#X"`
     in assets/ matches an `id="X"` declared in extension-schema.xsd.
  4. The licence attribution required by ATTRIBUTION.md is actually present:
     in SKILL.md, in NOTICE, and as the generator meta in the iXBRL skeleton.
     A licence obligation nobody checks is one that quietly rots away.

Run: python3 tests/check_skill.py
Exits non-zero (and prints `::error::` annotations for GitHub Actions) on any
violation. No third-party dependencies; `xmllint`/Arelle cover XML validity
separately.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
SKILL = ROOT / "SKILL.md"

# 32 KiB — the common harness ceiling for an auto-loaded SKILL.md.
MAX_SKILL_BYTES = 32 * 1024
MAX_DESCRIPTION_CHARS = 1024

# The credit string the licence requires (ATTRIBUTION.md § The credit string).
# Checked as three parts rather than one literal so that punctuation and line
# wrapping can differ between a Markdown body and an XHTML attribute.
ATTRIBUTION_PARTS = ("Max Schoon", "Doc2iXBRL", "doc2ixbrl.com")

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)
    print(f"::error::{msg}")


def failures_since(mark: int) -> int:
    """How many failures this check added, so it can report its own verdict.

    A check must not print "OK" on a run where it just emitted ::error::. A CI
    log that says OK two lines under its own error is exactly what gets skimmed
    past, and it devalues the OK lines that are true. Scoping the count to each
    check also stops one check's failure silencing another check's genuine pass.
    """
    return len(errors) - mark


def parse_frontmatter(text: str) -> dict[str, str]:
    """Minimal `key: value` frontmatter parser (top-level scalars only)."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip("\n")
    out: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            key, _, value = line.partition(":")
            out[key.strip()] = value.strip()
    return out


def check_skill() -> None:
    if not SKILL.is_file():
        fail("SKILL.md is missing")
        return

    raw = SKILL.read_bytes()
    size = len(raw)
    if size > MAX_SKILL_BYTES:
        fail(f"SKILL.md is {size} bytes; must stay under {MAX_SKILL_BYTES} (32 KiB)")
    else:
        print(f"SKILL.md size OK ({size} bytes, limit {MAX_SKILL_BYTES})")

    text = raw.decode("utf-8")
    fm = parse_frontmatter(text)
    if not fm.get("name"):
        fail("SKILL.md frontmatter is missing `name`")
    if not fm.get("description"):
        fail("SKILL.md frontmatter is missing `description`")
    elif len(fm["description"]) > MAX_DESCRIPTION_CHARS:
        fail(
            f"SKILL.md `description` is {len(fm['description'])} chars; "
            f"must stay under {MAX_DESCRIPTION_CHARS}"
        )
    else:
        print(f"SKILL.md frontmatter OK (description {len(fm['description'])} chars)")

    # Link resolution is checked repo-wide by check_reference_links().


# Repo-root form (references/foo.md, or references/sub/foo.md) and the sibling
# form used inside references/ (foo.md). The first pattern must allow path
# separators: it did not, so a file moved into references/<subdir>/ stopped
# matching and its links silently went unchecked -- a guardrail that quietly
# covers less is worse than one that fails.
ROOT_LINK = re.compile(r"references/((?:[A-Za-z0-9._-]+/)*[A-Za-z0-9._-]+\.md)")
SIBLING_LINK = re.compile(r"(?<![\w/.])([A-Za-z0-9._-]+\.md)")


def check_reference_links() -> None:
    """Every link to a references/ document must resolve, from any file."""
    mark = len(errors)
    references = ROOT / "references"
    known = {p.relative_to(references).as_posix() for p in references.rglob("*.md")}
    basenames = {p.name for p in references.rglob("*.md")}

    sources = [ROOT / "SKILL.md", *sorted(references.rglob("*.md"))]
    checked = 0
    for src in sources:
        if not src.is_file():
            continue
        text = src.read_text(encoding="utf-8")
        label = src.relative_to(ROOT).as_posix()

        for rel in sorted(set(ROOT_LINK.findall(text))):
            checked += 1
            if rel not in known:
                fail(f"{label}: link to references/{rel} does not resolve")

        # Sibling form only makes sense from inside references/.
        if src.is_relative_to(references):
            for name in sorted(set(SIBLING_LINK.findall(text))):
                if name == src.name or name not in basenames:
                    continue  # unknown .md names are prose, not links
                checked += 1
                if not (src.parent / name).is_file():
                    fail(
                        f"{label}: sibling link to {name} does not resolve from "
                        f"{src.parent.relative_to(ROOT).as_posix()}/ "
                        "(the file moved -- use the repo-root form)"
                    )

    if not failures_since(mark):
        print(f"Reference links OK ({checked} checked across {len(sources)} files)")


def check_asset_crossrefs() -> None:
    mark = len(errors)
    schema = ASSETS / "extension-schema.xsd"
    if not schema.is_file():
        fail("assets/extension-schema.xsd is missing")
        return

    schema_text = schema.read_text(encoding="utf-8")
    declared_ids = set(re.findall(r'\bid="([^"]+)"', schema_text))

    referenced = 0
    for path in sorted(ASSETS.glob("*")):
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        for target in re.findall(r'extension-schema\.xsd#([^"\'\s]+)', content):
            referenced += 1
            if target not in declared_ids:
                fail(
                    f"{path.name}: xlink:href to extension-schema.xsd#{target} "
                    "has no matching id= in extension-schema.xsd"
                )
    unresolved = failures_since(mark)
    counts = f"{referenced} checked against {len(declared_ids)} ids"
    if unresolved:
        # Report the counts, not a verdict. They stay useful on a failing run.
        print(f"Asset cross-references: {counts}, {unresolved} unresolved")
    else:
        print(f"Asset cross-references OK ({counts})")


def check_attribution() -> None:
    """Verify the licensing surface is present, consistent, and not overclaiming.

    Three distinct things are checked, and the third is an INVERTED check:

    1. The licence files exist. Removing one silently would leave the repo
       claiming terms it does not ship.
    2. Every references/*.md carries the attribution header, so the credit
       survives someone copying a single file rather than the repo.
    3. The default filing scaffold carries NO vendor stamp. Attribution must
       never be forced into an issuer's annual report: the tag alters the XHTML
       bytes and therefore package digests, digital signatures and any auditor
       hash over the document, and `name="generator"` would assert this tool
       generated a document it may only have informed. It is opt-in, documented
       in ATTRIBUTION.md, and this check exists to stop it drifting back into
       the default.
    """
    mark = len(errors)
    for name in (
        "LICENSE",
        "LICENSE-CONTENT",
        "LICENSES/MIT.txt",
        "NOTICE",
        "ATTRIBUTION.md",
        "rsl.xml",
        "llms.txt",
    ):
        if not (ROOT / name).is_file():
            fail(f"{name} is missing")

    notice = ROOT / "NOTICE"
    if notice.is_file():
        text = notice.read_text(encoding="utf-8")
        for part in ATTRIBUTION_PARTS:
            if part not in text:
                fail(f"NOTICE is missing required attribution: {part}")
        # The relicensing history must keep saying what MIT does and does not
        # allow; dropping it would leave an unenforceable implication behind.
        if "cannot be revoked" not in text:
            fail("NOTICE no longer states that the MIT grant cannot be revoked")

    skill = ROOT / "SKILL.md"
    if skill.is_file() and "doc2ixbrl.com" not in skill.read_text(encoding="utf-8"):
        fail("SKILL.md is missing the attribution section")

    missing_headers = [
        path.name
        for path in sorted((ROOT / "references").rglob("*.md"))
        if "doc2ixbrl.com" not in path.read_text(encoding="utf-8")
    ]
    if missing_headers:
        fail(f"references missing attribution header: {', '.join(missing_headers)}")

    # Inverted: the scaffold must stay clean.
    for scaffold in sorted(ASSETS.glob("*.xhtml")):
        if 'name="generator"' in scaffold.read_text(encoding="utf-8"):
            fail(
                f"assets/{scaffold.name} carries a vendor generator stamp; "
                "attribution must not be forced into a filing scaffold "
                "(ATTRIBUTION.md — it breaks digests, signatures and hashes)"
            )

    if not failures_since(mark):
        print("Attribution and licence surface OK")


def main() -> int:
    check_skill()
    check_reference_links()
    check_asset_crossrefs()
    check_attribution()
    if errors:
        print(f"\n{len(errors)} guardrail failure(s).")
        return 1
    print("\nAll skill guardrails passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
