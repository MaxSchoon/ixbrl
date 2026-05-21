---
name: ixbrl
description: Use for preparing, reviewing, validating, or debugging Inline XBRL (iXBRL) and XBRL filings. Trigger on iXBRL, XBRL, ESEF, EDGAR/EFM, UK FRC/HMRC, Dutch SBR/KvK/AFM, EBA/EIOPA DPM, IFRS, US-GAAP, EDINET, MCA, Arelle, taxonomy packages, report packages, extension taxonomies, anchoring, block or narrative tagging, fact mapping, contexts, units, decimals, transformation formats, calculation/linkbase/dimension errors, and validator codes such as FR-NL-*, EFM.6.*, ESEF.*, xbrldie:*, xbrldte:*, and xbrl.5.2.5.2. Use it to route to primary-source references, templates, and validation scripts.
license: MIT
---

# iXBRL skill

Inline XBRL embeds XBRL facts inside an XHTML host document via `ix:*`
elements: one file, two audiences (human reader + machine consumer).

This skill provides reference material, scripts, and decision-rules
for iXBRL work across the major regulatory regimes. It does **not**
replace the regulator's filer manual; it routes you to the right page
of the right manual and encodes patterns experts recognise on sight.

## When you load this skill, do this first

1. **Identify the regulator and reporting basis.** The same iXBRL file
   passes or fails depending on which validator runs. Ask the user
   which jurisdiction and which taxonomy. Common combinations:
   - EU listed issuer, IFRS consolidated AFR → **ESEF**, see `references/esef.md`
   - US SEC registrant → **EDGAR / EFM**, see `references/sec-edgar.md`
   - Dutch entity (KvK deposit or AFM listed) → **NL Taxonomie / SBR**, see the NL section in `references/taxonomies.md`
   - UK statutory accounts or HMRC tax → **UK FRC Suite**, see `references/taxonomies.md`
   - Bank or insurer supervisory return → **EBA / EIOPA DPM**, see `references/taxonomies.md`
   - IFRS digital financial statements (no jurisdictional overlay) → **IFRS Accounting Taxonomy**, see `references/taxonomies.md`
2. **Pick the operative taxonomy version.** ESEF 2024 ≠ ESEF 2025;
   FASB 2024 GRT ≠ 2025 GRT; FRC 2025 Suite ≠ 2026 Suite. Confirm the
   financial-year boundary against `references/taxonomies.md` before
   tagging.
3. **Choose your validation profile.** Use `scripts/validate_with_arelle.sh
   <file> <profile>` (`esef`, `efm`, `ukfrc`, `hmrc`, `core`). Run
   `core` first to isolate XBRL 2.1 violations from jurisdictional ones.
4. **Use the live filing corpus for real examples.** For ESEF, UKSEF,
   and Ukraine filings, use <https://filings.xbrl.org/> before and
   after authoring:
   - Filter the index by **Country** (for example `NL` for the
     Netherlands, or another listed country) to inspect filings from the
     relevant market.
   - Open the Inline XBRL viewer to compare how facts, continuations,
     hidden facts, labels, dimensions, and note block tags appear in a
     real report.
   - Download or inspect the xBRL-JSON and XBRL Report Package when you
     need concrete examples of fact values, contexts, units, taxonomy
     package layout, and validation messages.
   - Treat the corpus as evidence, not as authority: the repository is
     not complete, and many included filings have validation errors or
     warnings. Use it to learn market practice, then validate against
     the operative regulator rules.

## How to use the references

Each reference is a focused dive. Load on demand — do **not** read all
of them up front.

| If the question is about… | Read |
|---|---|
| What `ix:nonFraction`, `decimals`, `contextRef`, transformation registry, calc weights mean | `references/spec.md` |
| QNames, SQNames, NCNames, substitution groups, item types (monetary / decimal / shares / pure / textBlock / date / boolean / QName), concept attributes (`periodType`, `balance`, `nillable`) | `references/types.md` |
| DTS, XLink primitives, all five standard linkbases, role / arcrole types, tuples, footnote model vs `ix:footnote`, OIM (xBRL-XML / -JSON / -CSV), versioning, nil-value policy, instance pointers (`schemaRef` / `linkbaseRef` / `roleRef` / `arcroleRef`) | `references/structure.md` |
| Hypercubes, axes, explicit vs typed dimensions, segment vs scenario, default members, `xbrldie:*` / `xbrldte:*` errors | `references/dimensions.md` |
| Generic Links (`gen:*`), Functions Registry (`xfi:*`, `xff:*`, `xfm:*`, `f:*`, `r:*`), Versioning (concept renames, deprecations, migrations) | `references/advanced-specs.md` |
| Label Role Registry (negated labels), Data Types Registry (`textBlockItemType`, `percentItemType`, ESRS quantity types), URI resolution conventions | `references/registries.md` |
| DPM (EBA/EIOPA), Table Linkbase, filing indicators, COREP/FINREP/Solvency II, xBRL-CSV migration | `references/dpm.md` |
| ESEF mandatory block-tag list (Annex II Table 2), block-tag selection guidance, `ix:continuation` for split disclosures | `references/esef-block-tags.md` |
| Converting a PDF / Word / accounts-production document to faithful iXBRL — preserving hierarchy, abstracts, dates, completeness; the content-level review pass | `references/conversion.md` |
| Real-world Inline XBRL examples by country, including Netherlands (`NL`) and other ESEF/UKSEF markets; viewer output, xBRL-JSON, report packages, and validation messages | <https://filings.xbrl.org/> and API docs at <https://filings.xbrl.org/docs/api> |
| Which taxonomies exist, current versions, who issues them, who must file | `references/taxonomies.md` |
| ESEF anchoring, block tagging, Reporting Manual rules, NCAs (AFM, BaFin, AMF, CONSOB, CNMV, FSMA), `ESEF.*` codes | `references/esef.md` |
| SEC iXBRL phase-in, EDGAR Filer Manual sections, DEI / SRT / US-GAAP, `EFM.6.05.*` codes, Pay-Versus-Performance, cybersecurity tagging | `references/sec-edgar.md` |
| Arelle CLI, plugins, formula linkbase, Calc 1.1, full anti-pattern list, ESEF + EFM + core XBRL error codes with fixes | `references/validation.md` |

## First principles every preparer must internalise

Truths that, when violated, produce silent failures no validator catches early.

### 1. The `decimals` ↔ rendering ↔ value relationship

`ix:nonFraction` carries three numbers in tension: **rendered text**
(what the reader sees), **canonical XBRL value** (what the consumer
parses), and **declared accuracy** (`decimals`).

- `format` (an `ixt:*` transformation, see `references/spec.md` §TRR) converts rendered text to a canonical numeric value.
- `scale` multiplies the parsed text by 10^scale. `scale="3"` on rendered "1,234" yields canonical 1,234,000.
- `decimals` declares accuracy. `decimals="-3"` ≡ "rounded to thousands"; `decimals="0"` ≡ "whole units". **Never use `decimals="INF"` for a rounded value** — SEC EFM 6.05.16 rejects it; ESEF discourages it; both reject when rendered text is shorter than INF claims.
- `precision` is mutually exclusive with `decimals` on the same fact. **SEC and SBR forbid `precision`** — use `decimals` only.

Audit rule: canonical value = `transform(rendered_text) × 10^scale × (sign == "-" ? -1 : 1)`. If that doesn't match the natural-language number the reader sees, it's a tagging defect.

### 2. Sign convention, balance type, and `preferredLabel` are three different things

The single most common substantive error in ESEF filings.

- The **canonical XBRL value** is signed per the as-reported mathematical fact; `sign="-"` appears on the inline tag only when parentheses-formatting is used in the host XHTML.
- The concept's **`balance` attribute** (`debit`/`credit` on monetary types) drives downstream arithmetic. Reporting a credit-balance concept with the same sign as a debit-balance concept inverts the result for any balance-respecting consumer.
- The **`preferredLabel` role** on a presentation arc (`terseLabel`, `negatedLabel`, `negatedTerseLabel`, `periodStartLabel`, `totalLabel`, etc.) is a *display* instruction. `negatedLabel` flips the visible sign; the underlying fact is unchanged.

Rule of thumb: never flip a fact's sign to fix visible parentheses. Tag the as-reported absolute value with `sign="-"` iff the value is negative; let preferred-label roles handle display.

### 3. Period type is concept-driven, not document-driven

Balance-sheet concepts (assets, liabilities, equity) are **instant** — `<xbrli:instant>YYYY-MM-DD</xbrli:instant>`. Income statement, OCI, cash-flow, and changes-in-equity flows are **duration** — `<xbrli:startDate>` + `<xbrli:endDate>`.

Mismatching period type to concept class causes `xbrldie:PrimaryItemDimensionallyInvalidError` or schema validation failures. Respect the concept's declared `periodType`.

### 4. Identifier scheme constancy

Every `<xbrli:identifier scheme="...">` in an instance must use the **same scheme URI**: ESEF → LEI scheme (`http://standard.iso.org/iso/17442`); SEC → CIK scheme (`http://www.sec.gov/CIK`); SBR → KvK scheme. Mixing schemes silently produces "duplicate fact" errors because consumers treat differently-scheme'd entities as different.

### 5. Dimensions and axes — XDT is the substrate of every regime

XBRL Dimensions 1.0 ("XDT") makes a fact say more than "this amount, this period". Hypercubes attached to primary items declare which dimensions (taxonomy practice calls them **axes**) apply; the fact's dimensional context lives in `xbrli:segment` or `xbrli:scenario` carrying `xbrldi:explicitMember` (taxonomy-defined members) or `xbrldi:typedMember` (open-ended typed values).

Minimum rules:

- **Default members are implicit.** Never emit a dimension's default member explicitly. Triggers `xbrldie:DefaultValueUsedInInstanceError`.
- **`xbrldt:contextElement` lives on the `all`/`notAll` has-hypercube arc**, not on `hypercube-dimension`. It picks `segment` or `scenario`.
- **ESEF is scenario-only.** Reporting Manual §2.1.3 forbids `xbrli:segment`; `xbrli:scenario` may contain only `xbrldi:explicitMember` / `xbrldi:typedMember`.
- **"Axis" ≠ XDT vocabulary.** XDT uses *dimensions*. "Axis" is FASB/IFRS taxonomy convention (SEC EDGAR XBRL Filing Guide §3.5) — a label suffix marking explicit dimensions.
- **Closed hypercubes are exclusive.** `@xbrldt:closed="true"` means the container must contain *only* and *exactly* the declared dimensions.
- **Error namespaces split:** `xbrldie:*` is instance-level (e.g., `PrimaryItemDimensionallyInvalidError`); `xbrldte:*` is taxonomy/DTS-level (e.g., `HasHypercubeMissingContextElementAttributeError`, `TooManyDefaultMembersError`).

See `references/dimensions.md` for the full arcrole table, error codes, explicit-vs-typed contrast, and per-regime axis examples (IFRS, US-GAAP / SRT / DEI, SBR, EBA DPM).

### 6. Anchoring is mandatory only in some regimes — but always good practice

- **ESEF:** anchor every primary-statement extension to the **closest wider** IFRS/ESEF base concept (Reporting Manual 1.4.1), plus to **each** narrower base concept when the extension combines two or more (RTS Annex IV §9(b)). Pure subtotals are exempt from wider anchoring (§10) but must still participate in the calculation linkbase. **Never anchor to an abstract concept** (`ESEF.3.3.1.ExtensionConceptAnchoredToAbstractConcept`).
- **SEC EDGAR:** strongly recommended; EFM and SEC Sample Letter require using base concepts before extensions; IFRS foreign private issuers must anchor under the SEC's IFRS entry-point rules.
- **Dutch SBR / KvK:** fixed entry points by entity-size class; extensions are generally not authored for KvK deposits.

When in doubt, anchor wider.

### 7. Block tagging is structured narrative, not a screenshot

Where note-block tagging is required (ESEF Article 6, mandatory from FY2022; analogous regimes elsewhere), an `ix:nonNumeric escape="true"` element wraps the entire note's XHTML. The escaped XHTML *is* the fact value — preserve tables, lists, headings, and ensure machine-readability after extraction (Reporting Manual 2.2.6). Empty or whitespace-only block tags are valid syntactically but useless and often trip downstream formula assertions.

### 8. The hidden section is for facts that exist, not for facts you're embarrassed by

`ix:hidden` carries facts required in XBRL but with no natural visible rendering (notably SEC `dei:` cover-page facts). ESEF and EFM both require any hidden fact whose value also appears as visible text to be linked via the `-esef-ix-hidden` (ESEF) or `-sec-ix-hidden` (SEC) CSS style. Do not put numeric/transformable facts in `ix:hidden` to suppress them — ESEF forbids it (`ESEF.2.4.1.transformableElementIncludedInHiddenSection`).

The mistake runs both ways. `ix:hidden` is *under*-used as often as it is abused: taxonomy-mandated entity metadata (registered name, registration number, legal form, document/report type, period-end date) and non-numeric classification facts that steer interpretation but are not a line in any statement (an entity-size class member, a reporting-framework choice, a consolidated-vs-company-only indicator) are real required facts with no row to sit on — they belong in `ix:hidden`, not omitted. See `references/conversion.md` §8 for the positive case.

## Converting a source document to iXBRL

Most iXBRL is not authored from scratch — it is *converted* from a
finished PDF, Word file, or accounts-production output. Conversion is
where filings quietly go wrong, because a converted file can pass every
validator and still misrepresent the financial statements: validators
check syntax and DTS wiring, not whether the iXBRL is *faithful* to the
document a human prepared.

If the task involves a conversion (or building a pipeline that does
one), read `references/conversion.md`. The failures it guards against
are the ones that look fine from a distance and fall apart up close:

- **Flattened hierarchy.** Headings, groupings, and indentation are
  information. Every visible heading maps to an **abstract concept**;
  the presentation linkbase tree must mirror the statement's visual
  structure. A flattened presentation linkbase is the structural
  equivalent of deleting every heading from the printed accounts.
- **Lost dates and columns.** Each column header is a context. The
  balance-sheet date is a disclosure, not decoration — never let it
  disappear because the converter only kept the numbers.
- **Half-tagged statements.** A primary statement is fully tagged or
  defective; a consumer cannot tell an omitted line from a missed one.
  Walk every row *and* every column. The most-skipped facts are the
  totals that feel "derived" — total equity / shareholders' equity,
  result before tax. The statement of changes in equity is a *matrix*
  (components × movements); tag every cell.
- **Incomplete or sign-wrong calc trees.** Every subtotal needs a
  summation network covering all its children. A calc `weight` is not a
  free choice: XBRL 2.1 §5.1.1.2 ties its sign to the `balance`
  attributes — same balance → `weight="1"`, opposite → `weight="-1"`.
- **Reinvented labels.** Do not re-author labels for base-taxonomy
  concepts; they already carry official labels. Author labels only for
  extension concepts, and make each label the line-item wording *as it
  reads in the source document* — a paraphrase breaks the audit trail.
- **A toy test filing.** A single-page micro-entity statement with no
  cash flow, no changes-in-equity matrix, and no extensions exercises
  almost none of the hard parts. Validate pipelines against a
  representative filing (full primary statements, comparatives,
  extensions, anchoring, dimensions).

After the validators are clean, do the **content-level review pass** in
`references/conversion.md` §10 — read the rendered statements as a
financial professional. That pass catches what no validator does.

## Standard validation pipeline

Run these in order. Each step depends on the prior being clean.

```bash
# 1. Base XBRL spec — catches xbrl.* and xbrldie:* violations
scripts/validate_with_arelle.sh report.zip core

# 2. Jurisdictional rules — catches ESEF.*, EFM.6.*, UKFRC.*, FR-NL-*
scripts/validate_with_arelle.sh report.zip esef        # or efm, ukfrc, hmrc

# 3. Pre-flight pure-XML sanity (cheap, no Arelle dependency)
python scripts/check_facts.py path/to/document.xhtml

# 4. (If applicable) cryptographic seal/sign of the validated package
```

Step 1 first because a base XBRL error makes step 2 noisy. Step 3 catches issues validators don't always surface clearly: dangling continuation chains, undefined contexts/units, inconsistent duplicate facts, `decimals="INF"` abuse, non-ISO currency unit measures.

## Common-error decision tree

When the user shows you a validator error, route by code prefix:

- `ESEF.2.x.*` → iXBRL/instance-construction issue. See the table in `references/esef.md` §8 and the duplicated/expanded table in `references/validation.md` §5.1.
- `ESEF.3.x.*` → extension-taxonomy issue (anchoring, labels, link roles). Same references.
- `EFM.6.05.*` → SEC iXBRL syntax/DEI/decimals issue. See `references/sec-edgar.md` §7 and `references/validation.md` §5.2.
- `EFM.6.08.*` → SEC industry-overlay (ECD, RXP, OEF, CEF) linkbase issue.
- `FR-NL-*` / `FG-NL-*` → Dutch SBR rule. The most common are encoding (1.01–1.05), missing `xml:lang` (2.03), `link:schemaRef` placement (2.04), `xbrli:forever` use (3.04), `precision` usage (5.06), `xsi:nil` on facts (5.07), footnotes (6.01).
- `xbrl.5.2.5.2` → calculation inconsistency. Either fix the data or move to Calc 1.1 if the regulator accepts it. See `references/validation.md` §4.
- `xbrldie:*` (instance-level) → dimensional context error. See `references/dimensions.md` §"Dimensional validity errors".
- `xbrldte:*` (taxonomy/DTS-level) → hypercube/dimension/domain wiring error in the linkbases. See `references/dimensions.md` §"Dimensional validity errors".

## Anti-patterns that pass syntax but fail review

No validator error in step 1 or 2, but flagged by auditors or NCA post-filing reviews. Full list in `references/validation.md` §6 — highlights:

- **Negated-label sign confusion.** Tagging `(1,234)` as `-1234` when the calc tree expects `+1234` (let the negated-label role handle display).
- **Decimals drift across calc tree levels.** Parent at thousands, child at units; rounding tolerance computed from the looser side; cumulative drift fires `xbrl.5.2.5.2`.
- **Same fact, two values.** Same concept tagged in summary and footnote with different rounding.
- **Wrong namespace for shared concepts.** Concepts exist in *exactly one* namespace per taxonomy. Picking a jurisdiction-extension prefix when the core concept exists makes the calc tree silently fail.
- **Tagged but not in any presentation linkbase.** ESEF requires every tagged fact's concept to appear in at least one presentation link.
- **Default-member explicit emission.** Drop default members — they are implicit.
- **External CSS / `<script>` / `xml:base`.** All forbidden in ESEF and EFM. Inline everything; sanitise the HTML at generation time.

## Authoring an extension taxonomy (high level)

When base taxonomy lacks a needed concept, build a small extension. Typical ESEF / EFM-style layout:

```text
{prefix}-{date}/
├── {prefix}-{date}.xsd          # schema with new concepts
├── {prefix}-{date}_pre.xml      # presentation linkbase
├── {prefix}-{date}_cal.xml      # calculation linkbase
├── {prefix}-{date}_def.xml      # definition linkbase (anchoring lives here)
├── {prefix}-{date}_lab-en.xml   # English labels
├── {prefix}-{date}_lab-{lang}.xml  # report-language labels
└── META-INF/
    ├── taxonomyPackage.xml      # manifest with <tp:identifier>, <tp:entryPoint>
    └── catalog.xml              # URI rewrite for offline resolution
```

Rules:

- Concept names: PascalCase, no spaces, derived from `xbrli:item` or `xbrli:tuple` substitution group.
- Each concept has a Standard Label in the report language. Add English labels.
- For monetary concepts, set `balance="debit"` or `balance="credit"` correctly — this drives sign convention everywhere downstream.
- For ESEF: anchor each non-subtotal extension to the closest wider IFRS concept (and to each narrower component concept if the extension is an aggregation). Never anchor to abstract concepts.
- Add an abstract concept for every section header and grouping so the presentation linkbase tree mirrors the statement's visible hierarchy (see `references/conversion.md` §2).
- Wire concepts into a presentation link with appropriate `preferredLabel` roles on subtotal arcs.
- Wire calculation links with `weight="1"` when parent and child share the same `balance`, `weight="-1"` when they are opposite (XBRL 2.1 §5.1.1.2). Give every subtotal a summation network covering *all* of its children.

See `references/esef.md` §5 for ESEF specifics and `references/sec-edgar.md` §4 for EFM specifics.

## Generating a Report Package

Both ESEF and report-package-aware regulators expect a `.zip` (or `.xbri`) with:

```text
report-package.zip
├── META-INF/
│   ├── taxonomyPackage.xml      # manifest (mandatory)
│   ├── catalog.xml              # standard remap (optional but expected)
│   └── reports.json             # for newer Report Packages 1.0
├── reports/
│   └── {LEI}-{YYYY-MM-DD}.xhtml # single-file iXBRL
│   └── {set}/                    # OR a folder with multiple .xhtml files
│       ├── statements.xhtml
│       └── notes.xhtml
└── {prefix}-{date}/             # extension taxonomy (if any)
    ├── *.xsd
    └── *.xml
```

Common rejection grounds: macOS `.DS_Store` / `__MACOSX` artifacts at package root; PDFs at root; `.html` instead of `.xhtml`; filename pattern violations (Arelle enforces via regex); missing `taxonomyPackage.xml`. See `references/esef.md` §6.

## When this skill can't answer with confidence

Be honest. iXBRL has many regimes and they evolve. If a question concerns:

- a regulator not covered in `references/taxonomies.md`,
- a rule version newer than what the references cite,
- an Arelle error code not listed in `references/validation.md`,

— say so and point to the primary source on the regulator's website. Do not invent error codes, rule numbers, or taxonomy versions. The cost of a wrong citation in a regulated filing is high.

## Bundled scripts

- **`scripts/validate_with_arelle.sh <file> [profile]`** — wraps `arelleCmdLine` with the right plugins per profile (`esef`, `efm`, `ukfrc`, `hmrc`, `core`). Auto-detects single file, iXBRL document set, or `.zip` / `.xbri` report package.
- **`scripts/check_facts.py <ixbrl.xhtml>`** — pure-Python pre-flight sanity check. Catches: required attributes (`contextRef`, `unitRef`, `decimals`/`precision`), unresolved context/unit references, non-ISO-4217 currency measures, `decimals="INF"` abuse, broken continuation chains, inconsistent duplicate facts. Run before Arelle to surface cheap-to-detect errors fast.

Both scripts are dependency-light (`arelle-release`, `lxml`) and CI-safe.
