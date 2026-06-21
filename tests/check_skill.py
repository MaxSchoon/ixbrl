#!/usr/bin/env python3
"""Skill + asset guardrails for CI (standard library only).

Enforces the invariants documented in CONTRIBUTING.md so a PR can't silently
break the agent contract or the runnable scaffolds:

  1. SKILL.md exists, stays under 32 KiB, and has YAML frontmatter with a
     `name` and a `description` (description under 1024 chars).
  2. Every `references/*.md` linked from SKILL.md actually exists.
  3. Asset cross-references resolve: every `xlink:href="extension-schema.xsd#X"`
     in assets/ matches an `id="X"` declared in extension-schema.xsd.

Run: python3 tests/check_skill.py
Exits non-zero (and prints `::error::` annotations for GitHub Actions) on any
violation. No third-party dependencies; `xmllint`/Arelle cover XML validity
separately.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
SKILL = ROOT / "SKILL.md"

MAX_SKILL_BYTES = 32 * 1024  # 32 KiB — common harness ceiling for an auto-loaded SKILL.md
MAX_DESCRIPTION_CHARS = 1024

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)
    print(f"::error::{msg}")


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

    # Every references/*.md referenced from SKILL.md must exist.
    for rel in sorted(set(re.findall(r"references/([A-Za-z0-9._-]+\.md)", text))):
        if not (ROOT / "references" / rel).is_file():
            fail(f"SKILL.md references missing file: references/{rel}")


def check_asset_crossrefs() -> None:
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
    print(f"Asset cross-references OK ({referenced} checked against {len(declared_ids)} ids)")


def main() -> int:
    check_skill()
    check_asset_crossrefs()
    if errors:
        print(f"\n{len(errors)} guardrail failure(s).")
        return 1
    print("\nAll skill guardrails passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
