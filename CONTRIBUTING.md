# Contributing to the iXBRL Skill

Thanks for considering a contribution. This skill is read by AI agents, so its accuracy directly affects the quality of iXBRL filings produced by people who rely on it. Contributions are welcome from anyone — filers, regulators, taxonomy authors, validation engineers, accountants, auditors.

## What this project is

A vendor-neutral skill for any AI agent runtime that supports the standard skill convention. It contains:

- `SKILL.md` — the agent entrypoint
- `references/` — primary-source-cited reference notes for XBRL 2.1, iXBRL 1.1, ESEF, EDGAR/EFM, dimensions, taxonomies, validation, registries, DPM, etc.
- `assets/` — runnable scaffolds (iXBRL skeleton, schema, linkbases, taxonomy package, catalog)
- `scripts/` — local validation helpers

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

## Asset integrity

Every commit touching `assets/` must keep the scaffolds valid:

- `xmllint --noout` must pass on every file in `assets/`
- Cross-file references must resolve: every `xlink:href="extension-schema.xsd#X"` must match an `id="X"` in `extension-schema.xsd`; every custom `roleURI` referenced in a linkbase must be declared in the schema
- XML comments must not contain `--` runs (XML 1.0 §2.5)
- `taxonomyPackage.xml` must validate against `http://www.xbrl.org/2016/taxonomy-package.xsd`
- `catalog.xml` must validate against `http://www.xbrl.org/2016/taxonomy-package-catalog.xsd`

CI runs all of these on every PR. They must be green before merge.

## Local validation

```bash
# 1. xmllint on all assets
xmllint --noout assets/*.xml assets/*.xsd assets/*.xhtml

# 2. Cross-file ID and role-reference check
python3 .github/scripts/validate_assets.py

# 3. Optional: full Arelle validation
./scripts/validate_with_arelle.sh assets/ixbrl-skeleton.xhtml

# 4. Optional: fact sanity check
python3 scripts/check_facts.py assets/ixbrl-skeleton.xhtml
```

Install `libxml2-utils` (Linux) or use the `xmllint` shipped with macOS. Arelle is optional for local work; CI does not run it by default.

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
5. **Open a PR.** Fill in the template. Cite specs for every technical claim added or changed.
6. **Respond to review.** Spec citations may be requested for claims that look right but are uncited.

## PR checklist

The PR template enforces these. Read them before opening:

- Type of change identified
- Spec citations added or preserved for every technical claim
- `xmllint --noout` clean on `assets/`
- Cross-file refs resolve
- Vendor-neutral language preserved
- No claim deleted without spec-citation justification
- Honest-gap notes preserved or added where applicable

## Multi-agent review (encouraged for substantive changes)

The initial release was built via independent multi-agent review: a creator drafted, an independent reviewer audited, a fixer applied corrections, and a fresh auditor re-verified. The discipline catches the kind of plausible-sounding-but-wrong text that single-pass review misses.

If your change touches normative content (spec interpretations, validation rules, scaffold semantics), running a similar review locally — even just two agents from different vendors — is encouraged. Note the review process in your PR description; it makes the reviewer's job easier and helps build trust in the change.

## Reporting bugs and gaps

Use the issue templates:

- **Spec-citation correction** — "file says X but the spec actually says Y"
- **Regulator update** — "ESEF 2026 changed Z, need to update files A and B"
- **Scaffold regression** — "asset no longer passes xmllint / Arelle"
- **Trigger misfire** — "skill triggers on X but shouldn't / doesn't trigger on Y but should"
- **Bug report** — anything else
- **Enhancement** — proposals for new content or structure

For security or filing-integrity concerns (a scaffold producing apparently-valid output that fails regulator validation), see [`SECURITY.md`](SECURITY.md) before filing publicly.

## Code of Conduct

Participation in this project is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). Report concerns to schonemax@gmail.com.

## License

By contributing you agree your contribution is licensed under the repository's MIT License.
