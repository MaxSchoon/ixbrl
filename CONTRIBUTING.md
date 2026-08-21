# Contributing to the iXBRL Skill

Thanks for considering a contribution. This skill is read by AI agents, so its accuracy directly affects the quality of iXBRL filings produced by people who rely on it. Contributions are welcome from anyone: filers, regulators, taxonomy authors, validation engineers, accountants, auditors.

## What this project is

An open, primary-source-grounded skill for any AI agent runtime that supports the standard skill convention. Maintained by [Doc2iXBRL](https://doc2ixbrl.com). It contains:

- `SKILL.md`: the agent entrypoint
- `references/`: primary-source-cited reference notes for XBRL 2.1, iXBRL 1.1, ESEF, EDGAR/EFM, dimensions, taxonomies, validation, registries, DPM, etc.
- `assets/`: runnable scaffolds (iXBRL skeleton, schema, linkbases, taxonomy package, catalog)
- `scripts/`: local validation helpers

There are no harness-specific assumptions in this repo. Do not introduce them.

## Discipline

Three rules govern every change:

### 1. Primary-source validation

Every technical claim must cite a spec section. Acceptable forms:

- `XBRL 2.1 §4.6.6`
- `iXBRL 1.1 §13.1.2`
- `EFM 6.5.21`
- `ESEF Reporting Manual G.4.1.3`
- `ESEF RTS Annex IV §1`
- `Dimensions 1.0 §1.4.3`
- `LRR §3.1` (Link Role Registry)
- A versioned URL to a regulator publication (PDF or HTML), pinned to a specific section anchor where possible

If you cannot find a citation, do not claim the rule. State the gap honestly (see rule 2).

### 2. Honest-gap discipline

If you could not verify a claim, say so. Use phrases like:

- "Not verified against [spec]; included pending citation."
- "Behavior observed in Arelle X.Y.Z; not stated explicitly in the spec."
- "Regulator guidance is silent on this; common practice is …"

Do not paper over uncertainty. A documented gap is a contribution; a confident-sounding fabrication is a regression.

### 3. Vendor-neutral language

The skill must be usable in any agent harness that supports the skill convention. Do not mention specific harnesses, vendors, IDEs, or assistants by name. Use "the agent", "an AI agent", "the agent runtime", "the harness".

## Size discipline (skill-runtime limits)

Skills are loaded into agent runtimes that enforce real size limits. A
bloated `SKILL.md` is silently truncated by some runtimes and crowds
out other skills from the loadable index. Keep:

- **YAML frontmatter `description`** ≤ **1024 characters** (the hard
  limit the skill convention sets for SKILL.md descriptions). The description is what the
  runtime reads to decide whether to load this skill at all, so the
  budget is precious.
- **`SKILL.md` file** ≤ **32 KiB (32,768 bytes)**, frontmatter
  included (that is what `wc -c` and `tests/check_skill.py` measure), and
  aim for **< 500 lines and < 5,000 tokens** of body. The line and token
  figures come from the Agent Skills specification and the published
  skill-authoring guidance of the harnesses that implement it (once a
  skill body is loaded, every token competes with the conversation); the
  32 KiB byte gate is this repository's conservative belt for them. An
  earlier edition of this file justified 32 KiB by a harness setting that
  governs project-instruction files, not `SKILL.md`; the number stands and
  that reason does not.
- **Aggregate skill-metadata budget.** Harnesses that list many skills
  bound the *list* (one documents roughly 2% of the context window, or
  8,000 characters when unknown) and shorten descriptions first, then read
  the full `SKILL.md` of the one they select. Front-load the trigger words
  in the description so a shortened one still matches.
- **Reference files over ~300 lines carry a table of contents** at the
  top, because an agent that previews a long file with `head` sees the
  contents list and can jump, where it would otherwise see one section
  and conclude that is all there is. `references/dts.md` is the model.
- **Dated facts are not "time-sensitive instructions".** Skill-authoring
  guidance warns against instructions that silently go stale ("before
  August 2025 use the old API"). The *DTS and vintages* tables and the
  bi-temporal cheatsheets are the opposite: dated facts with a valid-time
  column, an acceptance-window column, a status on a stated verification
  date, and a primary source per row. They are what bi-temporal filing
  work requires. Keep them in that table shape (`references/dts.md`
  § Vocabulary) and re-verify the status column rather than deleting it.

If you need to add substantive content, prefer extending a file in
`references/` over expanding `SKILL.md`. Reference files load only
when the skill body points the agent at them (progressive disclosure),
so they do not consume context until needed. Before merging an edit
that grows `SKILL.md`, run:

```bash
wc -c SKILL.md  # must stay under 32768
```

and trim or relocate content if you cross the limit. The intake and the reference index are the only sections that may grow; everything else moves to a reference or a path.

## Intake and references

The skill has two layers, and the rule that keeps them apart is the one
most worth defending in review.

- `SKILL.md` opens with an intake keyed on the artifacts in front of the
  agent (a package, a source document, a validator log with the code, a
  generator with a corpus, source code, a bare question) and routes each
  to an ordered list of references. Intake rows are artifacts, never
  topics and never named tasks; the table stays at six rows, and a row
  names references and their order, never a rule.
- `references/*.md` hold the knowledge. Each opens with `Load this when`
  and `Do not load this when`, one short paragraph each, decidable from the
  agent's situation; every file over 100 lines carries a contents list
  after the attribution line (jurisdiction files use a bold `Contents`
  line rather than a heading, because their landmarks are gated).
  `references/defect-causes.md` is the one reference shaped as a
  diagnostic table: symptom, what the package shows, candidate causes by
  pipeline stage, the check that confirms or refutes each, and where the
  rule lives; it seeds candidates and never concludes, and a row may say
  the cause is not known.

Every reference is linked directly from `SKILL.md`, so any file is one
read away from the entry point; `tests/check_skill.py` resolves those
links and the same-document anchors.

## Asset integrity

Every commit touching `assets/` must keep the scaffolds valid:

- `xmllint --noout` must pass on every file in `assets/`
- Cross-file references must resolve: every `xlink:href="extension-schema.xsd#X"` must match an `id="X"` in `extension-schema.xsd`; every custom `roleURI` referenced in a linkbase must be declared in the schema
- XML comments must not contain `--` runs (XML 1.0 §2.5)
- `taxonomyPackage.xml` must validate against `http://www.xbrl.org/2016/taxonomy-package.xsd`
- `catalog.xml` must validate against `http://www.xbrl.org/2016/taxonomy-package-catalog.xsd`

Run the local validation steps below before opening a PR and paste the output into the description.

## Local validation

```bash
# 0. Dev toolchain (only needed if you touch scripts/ or tests/).
#    Use a venv — many systems mark the system Python as externally managed.
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt

# 1. xmllint on all assets
xmllint --noout assets/*.xml assets/*.xsd assets/*.xhtml

# 2. Skill guardrails (size, frontmatter, references, asset cross-refs)
python3 tests/check_skill.py

# 3. Markdown lint — rules this repo does not follow are disabled, with
#    reasons, in .markdownlint-cli2.jsonc, so a hit here is a real defect
npx --yes markdownlint-cli2@0.18.1

# 4. Code gate — only if you changed scripts/ or tests/
.venv/bin/python -m ruff check scripts tests
.venv/bin/python -m ruff format --check scripts tests
shellcheck scripts/*.sh

# 5. Optional: full Arelle validation
./scripts/validate_with_arelle.sh assets/ixbrl-skeleton.xhtml

# 6. Optional: fact sanity check
python3 scripts/check_facts.py assets/ixbrl-skeleton.xhtml
```

Install `libxml2-utils` (Linux) or use the `xmllint` shipped with macOS. Arelle is optional.

## Code conventions

Most of this repo is prose and static assets. The small amount of code
(`scripts/` and `tests/`) follows one shared standard so it can be read as
one artifact rather than a file-by-file dialect.

**Mechanical (enforced by CI; do not work around it).** `ruff` is both the
linter and the formatter, configured in [`ruff.toml`](ruff.toml): ecosystem
defaults, 88-column lines, `target-version = "py310"`. Config lives in a
standalone file rather than `pyproject.toml` because this repo is a skill, not
a distributable package. This matches `pyrightconfig.json`. Run
`python3 -m ruff check scripts tests` and `python3 -m ruff format scripts tests`
before opening a PR. Shell scripts must be `shellcheck`-clean.

Do not silence a finding with `# noqa`, a per-file ignore, or a loosened rule to
make the gate pass. If a suppression is genuinely warranted, say why in the code
and in the PR; an unexplained suppression is a rule deleted quietly.

**Structural (convention, not tool-enforced).**

- Scripts are standard-library-only where they can be. `scripts/check_facts.py`
  depends on `lxml` and degrades with a clear message and exit `127` if it is
  missing; `tests/check_skill.py` has no third-party dependency at all, so CI can
  run it before installing anything.
- Entry points end with `if __name__ == "__main__": raise SystemExit(main())`,
  and `main()` returns the exit code rather than calling `exit` itself. Exit
  codes: `0` clean, `1` issues found, `2` usage error, `127` missing dependency.
- Checkers accumulate findings into a list and report them all at the end. They
  do not stop at the first problem; a preparer fixing a filing wants the whole
  list in one run.
- Parsing untrusted input goes through a hardened parser (see `secure_parser()`
  in `check_facts.py`); do not construct a bare `etree.XMLParser`.
- Module-level constants are `UPPER_SNAKE`. Namespace URIs are declared once in
  the module-level `NS` dict; `findall`/XPath take the prefix map, and the
  Clark-notation forms lxml needs for attribute access are derived from `NS`
  (e.g. `XSI_NIL`) rather than repeating the URI as a literal.

**Type gate.** `pyrightconfig.json` is enforced in CI and the tree passes it
clean. `lxml-stubs` supplies the types `lxml` does not ship inline; without them
the declared standard is unachievable rather than merely unmet. Run
`.venv/bin/python -m pyright` before opening a PR if you touched `scripts/` or
`tests/`.

**Section references.** The jurisdiction references under
`references/jurisdictions/` use named, anchored sections, not numbers. Numbers
renumber, and `see 4.2` then silently points at unrelated content. Cite a
section by name. `tests/check_section_refs.py` enforces it.

Its one honest limitation: German, Danish, Finnish and Nordic law is cited with
the same `§` symbol, so a bare `§ 335` in `de-hgb.md` is `HGB § 335` with the
statute implied by context. Classifying those by pattern is unwinnable, and
guessing wrong would edit a legal citation, much worse than the stale reference
it was chasing. So the bare-number scan is skipped for those jurisdictions and
the unambiguous check (a reference that names its target file) carries the load.

**Tests.** `tests/test_check_facts.py` covers `scripts/check_facts.py` with
stdlib `unittest`: no runner dependency, matching the dependency-light rule
above. Run `.venv/bin/python -m unittest discover -s tests -p 'test_*.py'`. A
bug fix lands with a test that fails without it; two crashes shipped in this
script precisely because it had no tests.

## How to contribute

1. **Fork** the repo on GitHub.
2. **Branch**, named for the change kind:
   - `fix/efm-6-5-21-citation`
   - `update/esef-2026-rts`
   - `regress/calc-linkbase-arc-order`
   - `trigger/false-fire-on-ledger`
   - `docs/contributing-clarification`
3. **Make focused changes.** One logical change per PR. Mixing a regulator update with a scaffold fix makes review harder and slows everyone down.
4. **Run local validation** (see above). Paste output into the PR.
5. **Open a PR.** Write a clear description. Cite specs for every technical claim added or changed.
6. **Respond to review.** Spec citations may be requested for claims that look right but are uncited.

## PR checklist

When opening a PR, confirm:

- Type of change identified
- Spec citations added or preserved for every technical claim
- `xmllint --noout` clean on `assets/`
- Cross-file refs resolve
- Vendor-neutral language preserved
- If `scripts/` or `tests/` changed: `ruff check`, `ruff format --check`, `pyright`, `shellcheck`, and the unit tests all clean
- No claim deleted without spec-citation justification
- Honest-gap notes preserved or added where applicable

## Multi-agent review (encouraged for substantive changes)

The initial release was built via independent multi-agent review: a creator drafted, an independent reviewer audited, a fixer applied corrections, and a fresh auditor re-verified. The discipline catches the kind of plausible-sounding-but-wrong text that single-pass review misses.

If your change touches normative content (spec interpretations, validation rules, scaffold semantics), running a similar review locally, even just two agents from different vendors, is encouraged. Note the review process in your PR description; it makes the reviewer's job easier and helps build trust in the change.

## Reporting bugs and gaps

Issues are most actionable when labeled by kind:

- **Spec-citation correction**: "file says X but the spec actually says Y"
- **Regulator update**: "ESEF 2026 changed Z, need to update files A and B"
- **Scaffold regression**: "asset no longer passes xmllint / Arelle"
- **Trigger misfire**: "skill triggers on X but shouldn't / doesn't trigger on Y but should"
- **Bug report**: anything else
- **Enhancement**: proposals for new content or structure

For security or filing-integrity concerns (a scaffold producing apparently-valid output that fails regulator validation), email contact@doc2ixbrl.com before filing publicly.

## License

**Attribution is a condition of use.** Anyone who uses this skill (to review
filings, generate report packages, or build software with it) must credit
Doc2iXBRL. See [`ATTRIBUTION.md`](ATTRIBUTION.md). Changes must not weaken that
obligation or reintroduce language describing credit as optional or requested.

By contributing you agree your contribution is licensed under this
repository's terms: **Apache-2.0** for code (`scripts/`, `tests/`) and
**CC BY 4.0** for content (`SKILL.md`, `references/`, `assets/`). See
[`NOTICE`](NOTICE).

Contributions merged before the relicensing commit were made under the MIT
License. They remain identified under MIT (see `NOTICE` § Relicensing history,
which names them) and are not represented as relicensed. Written consent will
be sought before doing so. The MIT text is preserved at `LICENSES/MIT.txt`.
