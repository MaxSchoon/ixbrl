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

# `name="generator"` is only one spelling. XHTML permits single quotes and
# whitespace around `=`, and attribute names are case-insensitive, so an
# exact-string search is trivially bypassed -- in either direction: it would
# miss a stamp that is present, and miss one that is absent.
GENERATOR_META = re.compile(
    r"""<meta\b[^>]*\bname\s*=\s*['\"]?generator['\"]?""", re.IGNORECASE
)

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
# Path files are linked as `paths/<name>.md` from SKILL.md and from each other.
PATH_LINK = re.compile(
    r"paths/([A-Za-z0-9._-]+\.md)"
)  # resolved only when paths/ exists
PATHS = ROOT / "paths"
PATH_HEADER_MARKS = ("**Load this when:**", "**Do not load this when:**")
# A path that grows past this is restating references (CONTRIBUTING.md
# section Paths and references); the composing path is held shorter still.
PATH_MAX_LINES = 120
COMPOSING_PATHS = {"improvement-cycle.md": 40}
SIBLING_LINK = re.compile(r"(?<![\w/.])([A-Za-z0-9._-]+\.md)")


def check_reference_links() -> None:
    """Every link to a references/ document must resolve, from any file."""
    mark = len(errors)
    references = ROOT / "references"
    known = {p.relative_to(references).as_posix() for p in references.rglob("*.md")}
    basenames = {p.name for p in references.rglob("*.md")}

    # Every Markdown file in the repo, not just SKILL.md and references/. The
    # docstring claimed repo-wide and the code did not deliver it, so a broken
    # references/... link in README.md, CONTRIBUTING.md or .github/*.md passed.
    sources = sorted(
        p
        for p in ROOT.rglob("*.md")
        if ".venv" not in p.parts and "node_modules" not in p.parts
    )
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

        # paths/ is local-only and gitignored, so a tracked file may not
        # link into it at all: the link would be dead for every reader of
        # the published tree. Where the directory is present locally the
        # link is additionally checked to resolve.
        for rel in sorted(set(PATH_LINK.findall(text))):
            checked += 1
            if not PATHS.is_dir():
                fail(
                    f"{label}: links to paths/{rel}, "
                    "which is not part of the published tree"
                )
            elif not (PATHS / rel).is_file():
                fail(f"{label}: link to paths/{rel} does not resolve")

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

    # The scaffold must CARRY the provenance stamp: it is the default under
    # ATTRIBUTION.md, and a scaffold that quietly loses it teaches the wrong
    # default to everyone who copies it. Matched by regex, because XHTML permits
    # single quotes, spaces around "=", and any case.
    for scaffold in sorted(ASSETS.glob("*.xhtml")):
        text = scaffold.read_text(encoding="utf-8")
        if not GENERATOR_META.search(text):
            fail(
                f"assets/{scaffold.name} is missing the provenance stamp "
                "(ATTRIBUTION.md — generated documents carry it by default)"
            )
        elif "doc2ixbrl.com" not in text:
            fail(f"assets/{scaffold.name} generator stamp lacks the source link")

    if not failures_since(mark):
        print("Attribution and licence surface OK")


# A source marker in prose, `[S7]`, and the entry that defines it, written as
# a bold marker at the head of a list item. Identifiers stay strings: `[S2]`
# and `[S02]` are different markers to a reader, and folding them to an int
# would hide one shadowing the other.
SOURCE_MARKER = re.compile(r"\[S(\d+)\]")
SOURCE_ENTRY = re.compile(r"^\s*-?\s*\*\*\[S(\d+)\]\*\*", re.M)
# A fenced block opens on a line of three or more backticks or tildes and
# closes on a line of at least as many of the SAME character. A regex
# backreference cannot express "at least as long", and trying made a longer
# closing fence either miss the block or swallow the rest of the file, so this
# is scanned a line at a time instead.
FENCE_OPEN = re.compile(r"^[ \t]*(`{3,}|~{3,})")
# An inline code span: a run of backticks closed by an equal run on the same
# line. `[S1]` inside one is an example, not a citation.
INLINE_CODE = re.compile(r"(`+)[^\n]*?\1")


def mask_fences(text: str) -> str:
    """Blank out fenced blocks and inline code, preserving every offset.

    Offsets matter here: the source-list boundary is a position in this text,
    so deleting rather than blanking would shift everything after the first
    fence. An unclosed fence runs to the end of the document, as CommonMark
    says it does.
    """
    out: list[str] = []
    marker = ""
    for line in text.split("\n"):
        if marker:
            closing = line.strip()
            out.append(" " * len(line))
            if (
                closing
                and closing[0] == marker[0]
                and closing == closing[0] * len(closing)
                and len(closing) >= len(marker)
            ):
                marker = ""
            continue
        opened = FENCE_OPEN.match(line)
        if opened:
            marker = opened.group(1)
            out.append(" " * len(line))
            continue
        out.append(INLINE_CODE.sub(lambda m: " " * len(m.group()), line))
    return "\n".join(out)


# The credit line every reference carries. It is not body prose, so a marker
# appearing in it is not a citation anyone made.
ATTRIBUTION = re.compile(r"^\*Part of the iXBRL Skill\b.*$", re.M)


def check_citation_markers() -> None:
    """Every `[S7]` marker resolves to an entry, and every entry is cited.

        Only some references use this convention; a file that uses none is skipped
        rather than required to adopt it.

    Citations are counted from the body ABOVE the source list, and the list
        begins at its first entry. An entry carries its own marker, so counting
        the whole file would make every entry look cited. Excluding only each
        entry's first line is not enough either: entries wrap, and a continuation
        line can cite a different source, which would keep that source looking
        cited after its last real citation was deleted. Nor is a heading a safe
        boundary: one reference has a section called "When to escalate to primary
        sources" well above its actual list, and cutting there would drop real
        citations. The first entry is the list. A list grouped under its own
        subheadings is fine: its citations sit above it either way.

        This is the invariant that lets `.markdownlint-cli2.jsonc` switch MD052
        off. markdownlint reads `[S7]` as a shortcut reference link and wants a
        link definition, which this repository deliberately does not write. That
        rule is only safe to disable while something else checks what a reader
        depends on: that a marker points at a real source, and that no source goes
        uncited. Before this existed, the rationale for disabling MD052 named a
        check that did not exist.
    """
    mark = len(errors)
    checked = 0
    for path in sorted((ROOT / "references").rglob("*.md")):
        text = mask_fences(path.read_text(encoding="utf-8"))
        label = path.relative_to(ROOT).as_posix()

        entries = list(SOURCE_ENTRY.finditer(text))
        body = text[: entries[0].start()] if entries else text
        used = set(SOURCE_MARKER.findall(ATTRIBUTION.sub("", body)))
        defined: set[str] = set()
        for match in entries:
            if match.group(1) in defined:
                fail(f"{label}: source entry [S{match.group(1)}] is defined twice")
            defined.add(match.group(1))
        if not used and not defined:
            continue

        checked += 1
        for orphan in sorted(used - defined, key=int):
            fail(f"{label}: [S{orphan}] is cited but has no source entry")
        for unused in sorted(defined - used, key=int):
            fail(f"{label}: source entry [S{unused}] is never cited in the body")
    if not failures_since(mark):
        print(f"Citation markers OK ({checked} file(s) using the convention)")


# Same-document links: `[text](#slug)`. Headings slug the GitHub way (lower
# case, punctuation dropped, spaces to hyphens); explicit `<a id="…">` and
# `id="…"` attributes are targets too, which is how the gated `#profile-*`
# landmarks resolve.
SAME_DOC_LINK = re.compile(r"\]\(#([^)\s]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.M)
EXPLICIT_ID = re.compile(r"""\bid=["']([^"']+)["']""")
SLUG_DROP = re.compile(r"[^\w\- ]", re.U)


def slugify(heading: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", heading)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.strip().lower()
    text = SLUG_DROP.sub("", text)
    return text.replace(" ", "-")


def check_anchors() -> None:
    """Every same-document link in the tree resolves to a heading or an id.

    A contents list is the first thing a long reference hands a reader, so a
    dead entry in it costs a read and teaches distrust of the rest. Slugs
    are regenerated here rather than trusted; a heading edit that silently
    breaks its contents entry is exactly what this catches.
    """
    mark = len(errors)
    files = (
        sorted(ROOT.glob("*.md"))
        + sorted(ROOT.rglob("references/**/*.md"))
        + sorted(PATHS.glob("*.md"))
    )
    checked = 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        masked = mask_fences(text)
        # Headings come from the raw text: inline code in a heading is part
        # of its slug, and masking would blank it.
        targets = {slugify(h) for h in HEADING.findall(text)}
        targets |= set(EXPLICIT_ID.findall(text))
        # Duplicate headings get `-1`, `-2`, ... on the first free suffix,
        # reserving every slug already taken by any heading, the way the
        # rendered page allocates them.
        taken: set[str] = set()
        for h in HEADING.findall(text):
            base = slugify(h)
            slug = base
            n = 1
            while slug in taken:
                slug = f"{base}-{n}"
                n += 1
            taken.add(slug)
            targets.add(slug)
        label = path.relative_to(ROOT).as_posix()
        for anchor in SAME_DOC_LINK.findall(masked):
            checked += 1
            if anchor not in targets:
                fail(
                    f"{label}: link to `#{anchor}` matches no heading or id in the file"
                )
    if not failures_since(mark):
        print(f"Anchors OK ({checked} same-document links resolve)")


def check_paths() -> None:
    """Every path file carries its load-condition header and stays short.

    A path holds ordering only; the header is what tells an agent whether
    to read it at all, and the line cap is the tripwire for a path that has
    started restating the references it should only name.
    """
    mark = len(errors)
    if not PATHS.is_dir():
        print("Paths: none present (local-only working files), skipped")
        return
    files = sorted(PATHS.glob("*.md"))
    if not files:
        fail("paths/ holds no path files")
    for path in files:
        text = path.read_text(encoding="utf-8")
        label = path.relative_to(ROOT).as_posix()
        masked = mask_fences(text)
        for mark_text in PATH_HEADER_MARKS:
            if not re.search(rf"(?m)^{re.escape(mark_text)}", masked):
                fail(f"{label}: missing the `{mark_text}` header line")
        attribution = ATTRIBUTION.search(text)
        if attribution is None or not all(
            part in attribution.group(0) for part in ATTRIBUTION_PARTS
        ):
            fail(f"{label}: attribution line missing")
        cap = COMPOSING_PATHS.get(path.name, PATH_MAX_LINES)
        lines = len(text.splitlines())
        if lines > cap:
            fail(f"{label}: {lines} lines exceeds the {cap}-line cap for a path")
    if not failures_since(mark):
        print(f"Paths OK ({len(files)} path file(s), headers present, within caps)")


def main() -> int:
    check_skill()
    check_reference_links()
    check_paths()
    check_anchors()
    check_asset_crossrefs()
    check_attribution()
    check_citation_markers()
    if errors:
        print(f"\n{len(errors)} guardrail failure(s).")
        return 1
    print("\nAll skill guardrails passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
