# SBR Dutch GAAP / KvK — the pragmatic reference

Load this when the regulator is **KvK (Kamer van Koophandel)**, **AFM**
(Dutch listed issuer, where ESEF rules dominate but SBR overlays apply),
**Belastingdienst** (corporate income tax, VAT, ICP, payroll), or
**DNB**, or when the file uses `bw2-titel9:`, `rj:`, or `kvk:`
namespaces. For ESEF-only listed-issuer questions, prefer
`esef.md` and only return here for SBR-specific overlays.

This file concentrates the parts of Dutch SBR practice that catch out
preparers and reviewers in the field — not the canonical Filing Rules
prose (which is at <https://www.sbr-nl.nl/>). Treat it as the
"experienced KvK reviewer's checklist", not as a substitute for the
official Filing Rules.

## 1. First: which Nederlandse Taxonomie applies?

Dutch SBR is an annual taxonomy generation: **NT19**, **NT20**, **NT21**
etc. Filing Rules also evolve. The same iXBRL package can pass or fail
on **identical content** depending on which NT generation it was
prepared against — so before reviewing or validating, pin both:

1. **The reporting period.** A Dutch annual account for fiscal year
   ending 31 December 2024 is prepared against the **NT20 KvK Dutch
   GAAP / Dutch IFRS entry points** published 12 December 2024 for FY2024
   filings. FY2025 filings use the NT20 publication issued late 2025.
   The Belastingdienst slice has its own cadence (`20251210.a` for VPB
   2025, OB 2026, ICP 2026).
2. **The filing channel.** KvK deposits flow through Digipoort or a
   commercial SBR Portal; AFM ESEF filings flow through the AFM
   loket. Each channel may pin a slightly different Filing Rules
   version. Re-read the operative `FilingRules-*.pdf` on sbr-nl.nl
   before declaring an iXBRL package "wrong" — many "errors" are merely
   the difference between the rules you remembered and the rules in
   force.
3. **The entry point** (= which schema is in `link:schemaRef`). Entry
   point choice is concept-bearing: it determines which concepts are
   in-DTS, what dimension defaults apply, and which presentation /
   calculation linkbases are active. A Microbedrijf entry point makes
   most of the bw2-titel9 disclosure concepts unbound; a Groot entry
   point makes them available.

A pragmatic reviewer's first three commands:

```bash
unzip -p report.zip 'reports/*.xhtml' | head -c 8000 | \
  grep -E 'schemaRef|xmlns:(bw2-titel9|rj|kvk|jenv-bw2-i)|xbrli:identifier' -c

unzip -p report.zip 'META-INF/taxonomyPackage.xml' | \
  grep -E 'tp:identifier|tp:entryPoint|tp:version'

unzip -p report.zip 'META-INF/reports.json' 2>/dev/null  # Report Packages 1.0+
```

These tell you (a) which NT entry point was selected, (b) which
filer-side extension is wired in, and (c) whether the package uses
Report Packages 1.0 (`reports.json`) or the older `META-INF/` layout.

## 2. Bi-temporal cheatsheet (which rule applied when)

For each rule, ask: *was this in force when this report was prepared?*
Do not apply 2026 rules to a 2024 filing.

| Rule | Applies from | Notes |
|---|---|---|
| KvK Groot-class **must** deposit digitally (SBR Report Package) | FY2025 | Earlier years allowed paper for Groot. Don't insist on iXBRL for a FY2023 Groot deposit. |
| KvK Middelgroot must deposit digitally | FY2017 onward | Stable for years. |
| KvK Klein / Microbedrijf must deposit digitally | FY2016 / FY2017 | Stable for years. |
| Notes block-tagging required for KvK Dutch GAAP | **FY2026** (preview taxonomies live earlier) | For FY2025 and earlier KvK Dutch GAAP filings, notes block-tagging is **not** required and emitting it can break presentation parity. Watch for `kvk-inline-2025-preview` vs the operative entry point. |
| ESEF block-tagging for AFM (listed) IFRS notes | FY2022 | Distinct from KvK above. AFM listed AFRs follow ESMA Annex II Table 2, not KvK. |
| Auditor's report (controleverklaring) required in package | Middelgroot + Groot, always (article 2:393 BW) | Klein/Micro: not required. art. 2:403 BW: group subsidiaries may be exempt — its absence on a Groot subsidiary is not automatically wrong. |
| SBR Filing Rules calculation basis | XBRL 2.1 / Calc 1.0 throughout | NT20 Filing Rules still list XBRL 2.1 as normative; Calc 1.1 is diagnostic, not blocking. Calc 2.0 had a 2019 requirements note only, no specification. |
| `validate/NL` disclosure system | Per NT release | Run `arelleCmdLine --plugins validate/NL --disclosureSystem` matching the NT generation in the report. |

When uncertain, **state the rule version you are applying** before
declaring a defect. "This violates the NT20 KvK Filing Rule X for
FY2025" is reviewable; "this is wrong" is not.

## 3. Entry point by entity-size class (Title 9 Book 2 BW)

The size class is a property of the entity, derived from balance-sheet
total, net turnover, and average headcount over the prior two
financial years (`bw2-titel9:LegalEntitySize` axis members). It
dictates:

- Which KvK entry point schema is in `link:schemaRef`.
- Which disclosures are mandatory (Klein omits many notes; Groot must
  include everything Title 9 requires plus the auditor's report).
- Whether the auditor's report (controleverklaring) is required at all.

| Size class | bw2-titel9 axis member | Auditor's report required | Typical entry point family |
|---|---|---|---|
| Micro | `MicroEntity` | No | `bd-rpt-ihz-micro-*` (Bedrijfsdrijver), `kvk-rpt-jr-micro-*` |
| Klein | `SmallEntity` | No | `kvk-rpt-jr-klein-*` |
| Middelgroot | `MediumSizedEntity` | Yes | `kvk-rpt-jr-middelgroot-*` |
| Groot | `LargeEntity` | Yes | `kvk-rpt-jr-groot-*` |

A common reviewer slip: applying Middelgroot disclosure expectations
to a Klein filing, or vice versa. Pin the size class first; it changes
which absences count as defects.

## 4. The dual-scope pattern (consolidated + separate)

A medium / large group routinely files both a **consolidated** statement
set and a **company-only (separate)** statement set in one report.
Both use the same base concepts (`bw2-titel9:Assets`,
`AssetsCurrent`, `Liabilities`, `NetResultAfterTax`) and are
distinguished only by an explicit dimension member, typically on
`FinancialStatementsTypeAxis` (Consolidated / Separate). This is where
SBR Dutch GAAP filings most often go wrong — not because of one rule,
but because three independent invariants must hold simultaneously.

### 4.1 The mixed-scope ELR

Any extension concept reported in **both** scopes must additionally be
declared as a member of the extension's
`MixedScopeFinancialStatementsCompatibility` extended-link role.
Forgetting this — typically because an extension concept was added late
without re-wiring the compatibility ELR — fires:

> `NL-KVK.4.4.2.5.extensionTaxonomyLineItemNotLinkedToDesignatedPlaceholder`

This is a deposit-blocking error. Diagnosis: the extension's
`*_def.xml` shows the concept in
`kvk_LineItemsInConsolidatedFinancialStatementsPlaceholder` **and**
`kvk_LineItemsInSeparateFinancialStatementsPlaceholder`, but **not** in
`MixedScopeFinancialStatementsCompatibility`. Fix: add the missing
domain-member arc. Treat dual-scope placeholder membership and the
mixed-scope ELR as derived from one source of truth; never patch one
without updating the other.

### 4.2 Calculation linkbase scope-bleed

A `link:calculationLink` is grouped by extended-link role but is **not**
context-scoped — XBRL 2.1 binds every contributing item present in
**every** context where the summation concept also has a fact. So a
"BalanceSheetConsolidated" network binds against separate contexts too,
where the children may legitimately differ. Under Calc 1.1 round-to-
nearest semantics, this produces
`calc11e:inconsistentCalculationUsingRounding` warnings that look like
arithmetic errors but are role-vs-context artefacts.

The KvK normative basis is **Calc 1.0** (XBRL 2.1). Run:

```bash
arelleCmdLine --plugins inlineXbrlDocumentSet|validate/NL \
              --calc c10 \
              --packages <NT package>.zip \
              -f report-package.zip --validate
```

Treat Calc 1.1 cross-scope inconsistencies as diagnostic only, not as
deposit blockers. Before concluding a calc network is broken, classify
each inconsistency by reading the `context …` and `link role …` fields:
*in-scope* (role-scope == context-scope) is a real arithmetic gap to
fix; *cross-scope* is the dual-statement artefact. See
`validation.md` §4 for the full discussion.

### 4.3 Per-scope value-correctness — what Arelle won't catch

Arelle validates linkbase wiring, not whether the values map to the
correct scope. A converter can put consolidated values into the
separate context and pass every NL-KVK rule. Reviewers must perform a
content pass; the cheapest signals:

- Identical grand-totals across consolidated and separate scopes
  (`Equity`, `Assets`, `Revenue`). Possible, but rare. Flag for review.
- `Equity == Assets` in either scope — usually means liabilities were
  not tagged into that scope, or were tagged into the wrong scope.
- Subsidiaries-only concepts (`InvestmentsInParticipatingInterestsInGroupCompanies`)
  populated in the consolidated scope but not the separate scope.
- `NetResultAfterTax` consolidated ≠ separate when the separate scope
  reflects only the parent's standalone result.

## 5. NL-KVK validator codes — the ones that actually fire

These are the recurring KvK iXBRL deposit blockers as of NT20 Filing
Rules. Full code list lives in the operative Filing Rules PDF — these
are the high-frequency ones.

| Code | Meaning | Typical root cause | Fix |
|---|---|---|---|
| `NL-KVK.4.4.2.5.extensionTaxonomyLineItemNotLinkedToDesignatedPlaceholder` | Dual-scope extension concept missing from the `MixedScopeFinancialStatementsCompatibility` ELR | Concept added to consolidated + separate placeholders without updating compatibility ELR | Add the missing domain-member arc to the compatibility ELR; derive all three memberships from one predicate (see §4.1) |
| `NL-KVK.4.4.6.1.usableConceptsNotAppliedByTaggedFacts` | Concept present in extension presentation/definition linkbase but never tagged in the instance | Over-inclusive linkbase — e.g. concept stayed after a tagging redesign | Remove the unused concept from the linkbase, **or** add the missing fact |
| `NL.NL-KVK.3.4.1.3.transformableElementIncludedInHiddenSection` | Numeric / transformable fact emitted into `ix:hidden` | Convenience hiding of facts that don't fit visually | Render visibly; only non-transformable required-metadata facts belong in `ix:hidden` |
| `NL-KVK.*.missingRelevantPlaceholder` | Primary statement root is an extension abstract rather than the official `bw2-titel9:*Title` (or `rj:CashFlowStatementTitle`) placeholder | Generator emitted its own abstract root | Replace the root with the operative placeholder |
| `NL-KVK.*.extensionTaxonomyWrongFilesStructure` | Calculation linkbase file exists but contains no `link:calculationArc` | Empty calc linkbase emitted as a placeholder | Either populate the calc linkbase or remove it from the package |

In addition, two non-Filing-Rule signals routinely surface in NL
reviews:

- `xbrl.4.8.2:sharesFactUnit-notSharesMeasure` — share-count concepts
  (`bw2-titel9:ShareCapital*`, `ShareCapitalNumberSharesIssue`) tagged
  with a currency unit instead of `xbrli:shares`. Audit every
  `xbrli:sharesItemType` concept's unit.
- `xbrldie:PrimaryItemDimensionallyInvalidError` — the concept is
  missing from one of the `kvk_LineItemsIn{Consolidated,Separate}FinancialStatementsPlaceholder`
  domain-member trees, so its fact's dimensional context is invalid.

## 6. FR-NL- / FG-NL- — Filing Rules / Filing Guidelines recap

These rules are taxonomy-agnostic (they apply across NT generations
unless deprecated). The most common ones:

| Code | Rule |
|---|---|
| FR-NL-1.01 / 1.05 | Encoding: UTF-8, no BOM, correct XML declaration |
| FR-NL-2.03 | Non-numeric facts carry `xml:lang` |
| FR-NL-2.04 | `link:schemaRef` placement and count |
| FR-NL-3.04 | `xbrli:forever` periods forbidden |
| FR-NL-5.06 | `precision` attribute forbidden — use `decimals` |
| FR-NL-5.07 | `xsi:nil="true"` on a reported fact forbidden — omit the fact instead |
| FR-NL-6.01 | Footnotes — model and arcroles |

The newer NL-KVK.* code family in §5 layers KvK-specific Filing Rules
on top of these. Re-check both code families when validating.

## 7. The auditor's report (controleverklaring) in the package

For Middelgroot and Groot entities subject to art. 2:393 BW, the
auditor's report is **part of the deposit**, not optional commentary.
SBR Dutch GAAP 2025 treats it as a **separate tagged iXBRL document**
inside the report package, not as a section of the main
financial-statements XHTML:

```text
report-package.zip
├── META-INF/
│   ├── taxonomyPackage.xml
│   └── reports.json                              # may list both reports
└── reports/
    ├── <kvk>-<period>-annual-accounts.xhtml      # primary statements
    └── <kvk>-<period>-auditor-report.xhtml       # controleverklaring
```

The auditor's report XHTML carries an escaped text-block fact, typically
`bw2-titel9:AuditorsReportFinancialStatements` (`ix:nonNumeric
escape="true"`), and a boolean presence flag
`kvk:AuditorsReportFinancialStatementsPresent` in the primary
document. Reviewer checks:

- The presence flag is `true` when the auditor's report XHTML is
  included in the package, and `false` (or omitted, if the rule
  allows) when it is not.
- The auditor's report concept appears in **some** presentation link in
  the extension — orphaned-tagged facts trip `ESEF.3.4.6` equivalents
  in `validate/NL`.
- The escaped XHTML preserves table structure, headings, signature
  block, date, and auditor identification. The escaped XHTML *is* the
  fact value; a screenshot is not.
- For art. 2:403 BW group-subsidiary exemption filings, the absence of
  the auditor's report on a Groot entity is not automatically wrong —
  cross-check the management report / 403-statement before flagging.

## 8. Presentation linkbase — what KvK reviewers actually look at

This is the area where converters drift fastest from review expectation.

- **Roots on official placeholders.** Each primary statement roots on
  `bw2-titel9:BalanceSheetTitle`, `bw2-titel9:IncomeStatementTitle`,
  `rj:CashFlowStatementTitle`, etc. Rooting on an `ext:*Abstract`
  ("My Balance Sheet") triggers `missingRelevantPlaceholder`.
- **IS and Cash Flow are flat running totals in presentation.** The
  calculation linkbase carries the subtotal ladder
  (`ResultAfterTax ← ResultBeforeTax ← OperatingResult ← …`); the
  presentation linkbase shows the income statement as the reader sees
  it: a flat sequence of line items in reading order. Mirroring the
  calc ladder in presentation
  (`xbrl_model.presentation.structural_parity_mismatch`) makes the
  rendered viewer unusable.
- **Balance Sheet nests through the operative groupings.** Typically
  `AssetsNoncurrent` / `AssetsCurrent` and `Equity`, `ProvisionsAndLiabilitiesNoncurrent`,
  `LiabilitiesCurrent`. A flat balance sheet (one Title abstract with
  every line as direct child) loses the reader's information and
  fails review even when Arelle is silent.
- **Every tagged fact must appear in some presentation link.** The
  ten entity-metadata facts (registered name, legal form, registration
  number, registered office, etc.) and `kvk:AuditorsReportFinancialStatementsPresent`
  are the most frequently orphaned. Wire them into a metadata
  presentation role.

## 9. Recurring Dutch concept choices that are syntactically valid but wrong

Arelle accepts these because they exist in NT20; the auditor doesn't.

| Wrong | Right | Why it matters |
|---|---|---|
| `rj:Creditors` for trade payables | `bw2-titel9:TradePayablesCurrent` | `Creditors` is a broad RJ fallback covering all amounts owed; trade payables is a Title 9 line item. Using the broad concept loses the disclosure detail Title 9 requires. |
| `bw2-titel9:InvestmentsInParticipatingInterests` on a separate-scope statement | `bw2-titel9:InvestmentsInParticipatingInterestsInGroupCompanies` | The general concept includes minority interests; the in-group-companies concept is the parent's holdings in its consolidated subsidiaries — a different financial fact. |
| `rj:TreasurySharesMovement` on financing-activity rows in the cash flow | The specific bw2-titel9 / rj movement concept | `TreasurySharesMovement` is the equity-side change; cash spent on treasury shares is a separate financing-activity outflow. |
| `bw2-titel9:Result` (does not exist) | `rj:Result` | Plausible-from-memory QName that is unbound. See `validation.md` §6 item 26: `ix11.12.1.2:missingReferences` follows. |
| `rj:PayablesBanksCurrent` | `bw2-titel9:PayablesBanksCurrent` | Right local name, wrong prefix. Unbound concept. |

When reviewing a KvK iXBRL package, run a per-concept namespace check:
every fact's QName must resolve to a concept declared in (or imported
into) the operative DTS. Use `arelleCmdLine ... --saveInstance` to
extract the underlying XBRL instance and grep for missing-reference
warnings before any content review.

## 10. Sign and balance — the Dutch flavour

Two SBR-specific traps on top of the universal rules in
`SKILL.md` §"First principles":

- **Loss-labelled subtotals tagged positive.** `NetResultAfterTax` on
  a loss-making Dutch GAAP P&L must be **negative** in the canonical
  XBRL value; the `negatedLabel` role flips the rendered sign for the
  reader. A positive canonical value with a loss-labelled total is
  the single most common substantive defect in NL filings.
- **Cash-flow outflows.** Calculation weight `-1` on a child means
  "subtract from the parent". The fact itself should still be tagged
  as the as-reported magnitude (positive when the line items it
  aggregates are positive cash movements), and the `negatedLabel` role
  on the presentation arc renders parentheses. Do not negate the fact
  to compensate for the calc weight; one of the two will be wrong on
  the other side.

## 11. Concept-period class — the silent mis-map

`bw2-titel9:CashAndCashEquivalents` is declared `periodType="instant"`.
A converter that tags the opening cash balance as a fact in the
**cash flow statement** with the duration context of the year produces
an instant-on-duration mis-map. The XBRL primary item is dimensionally
invalid only when a hypercube is wired against the alternate period
type — otherwise the validator may stay silent and the fact looks
right in the viewer.

Reviewer rule: walk every fact in the cash flow statement and the
statement of changes in equity. Instant-period concepts there are
suspect unless the SoCE convention explicitly permits them (opening
and closing equity positions are instants by design).

## 12. Offline DTS resolution and `nltaxonomie.nl`

The canonical NT schemas live at `nltaxonomie.nl`. Arelle validating
KvK packages against an online cache can stall, intermittently fail,
or pick up the wrong NT generation. For deposit-quality validation:

1. Download the operative NT package(s) from sbr-nl.nl before
   validating: KvK Dutch GAAP, RJ, BW2, jenv (Belastingdienst), and any
   IFRS overlay used by the filer.
2. Pass them all to Arelle via `--packages` so the DTS resolves from
   local files only:

```bash
arelleCmdLine \
  --plugins inlineXbrlDocumentSet|validate/NL \
  --disclosureSystem nl-fr-nt20-kvk-ifrs-2025 \
  --packages NT20-20251212.zip,kvk-nt20-fr-ifrs-2025.zip \
  --calc c10 \
  -f report-package.zip --validate \
  --internetConnectivity offline
```

Adapt the disclosure system name to the operative one in your Arelle
build (it changes per NT generation; `arelleCmdLine
--showEnvironment` lists what's registered). When validation is
slow or intermittent, suspect remote-taxonomy resolution before
suspecting the package.

## 13. A pragmatic NL review pass — in order

When a user says "please review my SBR Dutch GAAP report package",
walk this in order. Each step depends on the prior being clean.

1. **Pin the regime, period, NT generation, and entry point.** §1 and
   §2. State them back to the user before opening the file. If any
   are ambiguous, ask.
2. **Pin the entity-size class.** §3. The size class changes which
   absences count as defects (auditor's report, certain disclosures).
3. **Run validation in the operative profile, offline.** §12. Capture
   the full log, including warnings. Use `--calc c10` for the
   normative KvK calc verdict; treat any `calc11r` cross-scope
   warning as diagnostic, not blocking.
4. **Classify each finding.** Route by code prefix using `SKILL.md`'s
   common-error decision tree. Distinguish dual-scope artefacts (§4.2)
   from real arithmetic defects, and rule violations from style
   warnings.
5. **Concept-binding pass.** §9. Confirm every fact's QName resolves
   in the operative DTS. `missingReferences` is harder to fix than
   surface validation errors and changes the meaning of every
   downstream check.
6. **Per-scope value pass.** §4.3. For consolidated + separate filings,
   sample a dozen line items and confirm the value belongs in the
   scope it appears in. No validator catches this for you.
7. **Sign and period class.** §10, §11. Walk the IS, CF, and SoCE.
8. **Presentation pass.** §8. Roots on official placeholders, IS/CF
   flat, BS nested, every tagged fact placed somewhere.
9. **Package shape.** §7. Auditor's report present if size class
   requires; metadata facts present and tagged; no MacOS artefacts
   (`.DS_Store`, `__MACOSX/`) at package root.
10. **Content-level review (read the rendered statements).** See
    `conversion.md` §10. The validators cannot tell whether the iXBRL
    is faithful to the source document; you can.

When a finding is unclear, **quote the validator log line verbatim**
and route by the code prefix in step 4 — that is the cheapest way to
distinguish a real defect from a known artefact.

## 14. When to escalate to primary sources

This file is a reviewer's working reference, not the legal source.
Defer to and cite:

- **SBR Nederland Filing Rules (FR-NL- / FG-NL-)** — <https://www.sbr-nl.nl/>
- **KvK Filing Rules supplements (NL-KVK.*)** — published with each
  NT generation; the PDF lives in the same documentation tree.
- **Title 9 Book 2 BW** for legal disclosure obligations
  (`wetten.overheid.nl`).
- **Richtlijnen voor de Jaarverslaggeving (RJ)** for Dutch GAAP
  application detail.
- **AFM ESEF guidance** for listed-issuer filings (then return to
  `esef.md`).

If the question concerns a rule version newer than what this file
cites, or a code not listed in §5 / §6, say so and link the primary
source. The cost of a wrong citation on a regulated filing is high.
