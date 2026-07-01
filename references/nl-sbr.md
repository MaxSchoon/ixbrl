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
on **identical content** depending on which generation it was prepared
against — so before reviewing or validating, pin:

1. **The reporting period** (read from `<xbrli:period>`, not today's date).
2. **The filing channel.** KvK deposits flow through Digipoort or a
   commercial SBR Portal; AFM ESEF filings flow through the AFM loket.
   Re-read the operative `FilingRules-*.pdf` on sbr-nl.nl before
   declaring an iXBRL package "wrong" — many "errors" are the
   difference between the rules you remembered and the rules in force.
3. **The entry point** (= which schema is in `link:schemaRef`). Entry
   point choice is concept-bearing: it determines which concepts are
   in-DTS, what dimension defaults apply, and which presentation /
   calculation linkbases are active. A Microbedrijf entry point makes
   most of the bw2-titel9 disclosure concepts unbound; a Groot entry
   point makes them available.

### Two taxonomy trees, same prefix family

The Dutch SBR ecosystem ships **two parallel taxonomy stacks** that
both bind to a `bw2-titel9:` / `rj:` / `kvk:` family of prefixes. They
look alike but resolve to *different* schema URIs, and concepts that
exist in one may not exist in the other:

- **SBR-domein Handelsregister filer-facing taxonomy** — the one KvK
  iXBRL annual accounts actually use. Schema URIs of the form
  `https://www.nltaxonomie.nl/bw2-titel9/<release-date>/bw2-titel9-cor`,
  `https://www.nltaxonomie.nl/rj/<release-date>/rj-cor`,
  `https://www.nltaxonomie.nl/kvk/<release-date>/kvk-cor`. Distributed
  as separate ZIPs from sbr-nl.nl (e.g. `bw2-titel9-2025_taxonomie.zip`,
  `rj-2025_taxonomie.zip`, `kvk-2025_taxonomie.zip`). For FY2025 the
  release date is `2025-12-31`.
- **NT20 SBR-domein technical taxonomy** — the one that imports the
  filer-facing taxonomy and carries the SBR-domein technical
  infrastructure (jenv slice, BD slice, formula linkbases, validation
  artefacts). Schema URIs of the form
  `http://www.nltaxonomie.nl/nt20/jenv/<release-date>/dictionary/jenv-bw2-data`
  (prefix `jenv-bw2-i:`), etc. Distributed as the large NT20 ZIP from
  sbr-nl.nl.

Both are normative for different things. The **filer-facing** stack is
where preparers look up concept names for their facts; the **NT20
technical** stack carries the formula linkbases, generic-message
labels, and validation wiring that drive Arelle's validation behaviour.
A reviewer needs both downloaded locally for offline validation.

Verified namespace bindings used by a real FY2025 Groot NL-GAAP filing:

| Prefix | Schema URI (2025-12-31 release) | Carries |
|---|---|---|
| `bw2-titel9` | `https://www.nltaxonomie.nl/bw2-titel9/2025-12-31/bw2-titel9-cor` | Title 9 BW data concepts (line items, axes, members), abstracts (`BalanceSheetTitle`, `IncomeStatementTitle`, `StatementOfComprehensiveIncomeTitle`), `FinancialStatementsTypeAxis` and its `ConsolidatedMember`/`SeparateMember` |
| `rj` | `https://www.nltaxonomie.nl/rj/2025-12-31/rj-cor` | RJ application detail (`CashFlowStatementTitle`, `Creditors`, `Result`, RJ-specific disclosures) |
| `kvk` | `https://www.nltaxonomie.nl/kvk/2025-12-31/kvk-cor` | KvK metadata, `LegalEntitySize` extensible-enumeration fact and values (`LegalEntitySize{Micro,Small,Medium,Large}Member`), placeholders (`LineItemsIn{Consolidated,Separate}FinancialStatementsPlaceholder`), `AuditorsReportFinancialStatementsPresent` flag |
| `<filer>` | `https://www.<filer>.nl/xbrl/<release-date>` | The filer's own extension (custom concepts, custom members, calculation/presentation/definition linkbases) |

A pragmatic reviewer's first three commands:

```bash
unzip -p report.xbri 'reports/*/*.xhtml' | head -c 8000 | \
  grep -E 'schemaRef|xmlns:(bw2-titel9|rj|kvk|jenv-bw2-i)|xbrli:identifier' -c

unzip -p report.xbri 'META-INF/taxonomyPackage.xml' | \
  grep -E 'tp:identifier|tp:entryPoint|tp:version'

unzip -p report.xbri 'META-INF/reportPackage.json' 2>/dev/null
unzip -p report.xbri 'META-INF/reports.json' 2>/dev/null
```

The xBRI Report Package format (`https://xbrl.org/report-package/2023/xbri`)
publishes `META-INF/reportPackage.json`; older Report Packages 1.0
publish `META-INF/reports.json`. KvK FY2025 example packages use xBRI.

## 2. Bi-temporal cheatsheet (which rule applied when)

For each rule, ask: *was this in force when this report was prepared?*
Do not apply 2026 rules to a 2024 filing.

| Rule | Applies from | Notes |
|---|---|---|
| KvK Groot-class **must** deposit digitally (SBR Report Package) | FY2025 | Earlier years allowed paper for Groot. Don't insist on iXBRL for a FY2023 Groot deposit. |
| KvK Middelgroot must deposit digitally | FY2017 onward | Stable for years. |
| KvK Klein / Microbedrijf must deposit digitally | FY2016 / FY2017 | Stable for years. |
| Notes / management report / other-information block-tagging for KvK iXBRL | Delayed: one year after ESMA's amended block-tagging approach takes effect | The RTS 2025 expresses the date as `202X`, not a fixed year. For FY2025 and earlier, voluntary block-tagging is not permitted; check the current RTS / FAQ before requiring it. |
| ESEF block-tagging for AFM (listed) IFRS notes | FY2022 | Distinct from KvK above. AFM listed AFRs follow ESMA Annex II Table 2, not KvK. |
| Auditor's report (controleverklaring) required in package | Middelgroot + Groot, always (article 2:393 BW) | Klein/Micro: not required. art. 2:403 BW: group subsidiaries may be exempt — its absence on a Groot subsidiary is not automatically wrong. |
| Calculation basis for FY2025 KvK iXBRL Report Packages | **Calc 1.1** is listed in RTS 2025 Annex III | Calc 1.1 uses OIM rounding semantics — it handles iXBRL's routinely-duplicate facts correctly and surfaces the dual-statement cross-scope inconsistencies that Calc 1.0 silently hides. Run Calc 1.0 only as a legacy / compatibility pass if the operative validator profile still checks it (§4.2). |
| `validate/NL` disclosure system | Per NT release | Run `arelleCmdLine --plugins validate/NL --disclosureSystem` matching the NT generation in the report. |

When uncertain, **state the rule version you are applying** before
declaring a defect. "This violates the NT20 KvK Filing Rule X for
FY2025" is reviewable; "this is wrong" is not.

### 2.1 RTS 2025 essentials for SBR-domein Handelsregister

The **Regelgevende Technische Standaard (RTS) van het SBR-domein
Handelsregister** is the domain-level implementation of the Besluit
elektronische deponering handelsregister. Use the current Dutch RTS as
the authority; the English translation says the Dutch version prevails.
The 2025 RTS was finalised on 31 October 2025 for annual reports for
financial years beginning on or after 1 January 2025.

The RTS is not the same thing as the Reporting Manual (RM):

- **RTS** — the technical filing requirements: format, package,
  mandatory markup, valid taxonomy/specification set, and extension
  taxonomy constraints.
- **RM** — preparer guidance for applying those requirements in an
  actual iXBRL annual report.

RTS points that matter in review:

- It splits the regime into **iXBRL Report Packages** (chapter 2) and
  legacy **XBRL instance / document-set filings** (chapter 3). The
  iXBRL rules are aligned with the ESEF RTS where useful, but KvK uses
  KvK/BW2/RJ/IFRS core taxonomies and KvK-specific filing metadata.
- For iXBRL, the annual report is filed in **XHTML** as a **Report
  Package** through Digipoort or the KvK upload portal. The package may
  not exceed **100 MB**, must contain the Inline XBRL Document Set and
  any extension taxonomy files in one package, and only one adopted
  annual report may be filed per legal entity per financial year.
- The RTS treats iXBRL as the recommended standard where presentation
  matters. A legal entity that uses entity-specific line items, changes
  the standard format / presentation, reports sustainability
  information, or cannot use a predefined XBRL entry point should expect
  to use iXBRL rather than legacy XBRL.
- Annex II requires detailed tagging of all numbers in a declared
  currency in the primary statements (including dashes / empty cells
  that represent nil or zero) and the mandatory KvK filing metadata
  facts such as registration number, legal-entity name, legal form,
  registered office, entity size, period end, reporting period,
  consolidation flag, auditor's-report-present flag, and adoption
  status. Conditional facts include adoption date and 2:403 / 2:408
  foreign-group filing flags when applicable.
- Annex III lists the applicable XBRL specifications for iXBRL Report
  Packages: Inline XBRL 1.1, Transformation Registry 4 or 5, Units
  Registry 1.0, Data Type Registry 1.x, Link Role Registry 2.0, XBRL
  2.1, Dimensions 1.0, **Calculations 1.1**, Taxonomy Packages 1.0,
  and Report Package 1.0.
- Annex IV is the core markup rulebook: use the core-taxonomy element
  with the closest / narrowest accounting meaning; create an extension
  only when the core taxonomy would misrepresent the disclosure; give
  every used extension element proper datatype / period / balance
  attributes and report-language labels; include each used extension
  element in at least one presentation hierarchy and one definition
  hierarchy; document arithmetic relationships in the calculation
  linkbase; and anchor extension concepts to wider / narrower core
  concepts where required.

Do not cite an RTS rule from memory. The SBR project page also publishes
the current FAQ, practice guidance, conformance suite, taxonomy
packages, and example `.xbri` filings; use those alongside the RTS/RM
when diagnosing a deposit failure.

## 3. Entry point by entity-size class (Title 9 Book 2 BW)

The size class is a property of the entity, derived from balance-sheet
total, net turnover, and average headcount over the prior two
financial years. In the FY2025 KvK taxonomy, size class is reported as
the mandatory metadata fact `kvk:LegalEntitySize`, an
extensible-enumeration fact. Its value is one of the KvK size members
(`kvk:LegalEntitySize{Micro,Small,Medium,Large}Member`), reported as a
URI value such as
`https://www.nltaxonomie.nl/kvk/2025-12-31/kvk-cor#LegalEntitySizeLargeMember`.
It is **not** an XDT context axis and should not appear as an
`xbrldi:explicitMember`. The size class dictates:

- Which KvK entry point schema is in `link:schemaRef`.
- Which disclosures are mandatory (Klein omits many notes; Groot must
  include everything Title 9 requires plus the auditor's report).
- Whether the auditor's report (controleverklaring) is required at all.

| Size class | `kvk:LegalEntitySize` fact value | Auditor's report required | Typical entry point family (FY2025 KvK NL-GAAP) |
|---|---|---|---|
| Micro | `kvk:LegalEntitySizeMicroMember` | No | `kvk-rpt-jaarverantwoording-2025-nlgaap-micro` |
| Klein | `kvk:LegalEntitySizeSmallMember` | No | `kvk-rpt-jaarverantwoording-2025-nlgaap-klein` |
| Middelgroot | `kvk:LegalEntitySizeMediumMember` | Yes | `kvk-rpt-jaarverantwoording-2025-nlgaap-middelgroot` |
| Groot | `kvk:LegalEntitySizeLargeMember` | Yes | `kvk-rpt-jaarverantwoording-2025-nlgaap-groot` |

(Specialised entry points exist for banks, insurers, pension funds,
healthcare, housing, non-profit / fundraising organisations,
cooperatives, cv/vof, foundations, etc.; the suffix `-publicatiestukken`
selects publication-only accounts and `-verticaal` selects the
vertical balance-sheet layout.)

A common reviewer slip: applying Middelgroot disclosure expectations
to a Klein filing, or vice versa. Pin the size class first; it changes
which absences count as defects. Also verify it as a reported metadata
fact, not as a context dimension.

## 4. The dual-scope pattern (consolidated + separate)

A medium / large group routinely files both a **consolidated** statement
set and a **company-only (separate)** statement set in one report.
Both use the same base concepts (`bw2-titel9:Assets`,
`bw2-titel9:AssetsCurrent`, `bw2-titel9:Liabilities`,
`bw2-titel9:NetResultAfterTax`) and are distinguished only by an
explicit dimension member on **`bw2-titel9:FinancialStatementsTypeAxis`**
— `bw2-titel9:ConsolidatedMember` vs `bw2-titel9:SeparateMember`. This
is where SBR Dutch GAAP filings most often go wrong — not because of
one rule, but because three independent invariants must hold
simultaneously.

For IFRS-based statements, use the IFRS consolidated/separate axis
(`ifrs-full:ConsolidatedAndSeparateFinancialStatementsAxis`) and its
consolidated / separate members instead. In all KvK iXBRL contexts,
dimensions belong in `xbrli:scenario`, not `xbrli:segment`.

### 4.0 What the RTS requires when both scopes are present

RTS 2025 Article 4 sets the minimum tagging target by accounting basis:

- If the annual report contains **both consolidated and company
  financial statements** prepared under IFRS and/or NL-GAAP, the legal
  entity must mark up the **consolidated financial statements**.
- If the annual report contains **only company financial statements**
  under IFRS and/or NL-GAAP, it must mark up those **company financial
  statements**.
- If the report uses generally accepted standards of another country
  (**Other GAAP**), only the filing metadata / mandatory elements in
  Annex II point 3 are required.

That minimum rule is easy to misread. It does **not** mean separate
financial statements may be dimensionally ambiguous when they are
tagged. Once a report tags facts from both consolidated and company
statements, the two statement sets must be separated consistently by
the appropriate financial-statements-type dimension:

- Consolidated facts use the consolidated member on
  `bw2-titel9:FinancialStatementsTypeAxis` for NL-GAAP or
  `ifrs-full:ConsolidatedAndSeparateFinancialStatementsAxis` for IFRS.
- Company-only facts use the corresponding separate member on the same
  basis-specific axis.
- The mandatory metadata fact
  `rj:FinancialStatementsConsolidated` states whether the filed
  financial statements are consolidated; it is not a replacement for
  per-fact consolidated/separate dimensional context.

The 2025 KVK taxonomy documentation exposes four extension-taxonomy
placeholder roles for this purpose:

| Role URI | Scope / basis |
|---|---|
| `https://www.nltaxonomie.nl/kvk/role/lineitems-consolidated-financial-statements-nlgaap` (`[990010]`) | Consolidated + NL-GAAP |
| `https://www.nltaxonomie.nl/kvk/role/lineitems-consolidated-financial-statements-ifrs` (`[990015]`) | Consolidated + IFRS |
| `https://www.nltaxonomie.nl/kvk/role/lineitems-separate-financial-statements-nlgaap` (`[990020]`) | Separate + NL-GAAP |
| `https://www.nltaxonomie.nl/kvk/role/lineitems-separate-financial-statements-ifrs` (`[990025]`) | Separate + IFRS |

Use the entry point that matches the accounting-basis mix:

- **NL-GAAP consolidated + NL-GAAP company** — import the NL-GAAP
  extension entry point and wire line items into the consolidated and,
  if tagged, separate NL-GAAP placeholders.
- **IFRS consolidated + IFRS company** — import the IFRS extension entry
  point and wire the two scopes into the IFRS placeholders.
- **IFRS consolidated + NL-GAAP company** — import the IFRS extension
  entry point: it is designed to discover both IFRS and NL-GAAP concepts
  and to support IFRS consolidated statements with NL-GAAP company
  statements.

For equity, RTS Annex II has a special practical rule: if the equity
disclosure in the consolidated financial statements refers to the
company financial statements, only the statement of changes in equity
in the company financial statements needs to be marked up, using the
**Separate** member. Do not force a duplicate consolidated SoCE tag set
where the report itself points the reader to the separate equity
statement. Notes explaining differences between consolidated and
company equity are not currently subject to mandatory note markup while
block-tagging is deferred.

Typical NL-GAAP context families:

```xml
<!-- Filing metadata: no financial-statement-scope dimension -->
<xbrli:context id="meta-current">
  <xbrli:entity>
    <xbrli:identifier scheme="http://www.kvk.nl/kvk-id">12345678</xbrli:identifier>
  </xbrli:entity>
  <xbrli:period><xbrli:instant>2025-12-31</xbrli:instant></xbrli:period>
</xbrli:context>

<!-- Consolidated statement fact -->
<xbrli:context id="consolidated-current">
  <xbrli:entity>
    <xbrli:identifier scheme="http://www.kvk.nl/kvk-id">12345678</xbrli:identifier>
  </xbrli:entity>
  <xbrli:period><xbrli:instant>2025-12-31</xbrli:instant></xbrli:period>
  <xbrli:scenario>
    <xbrldi:explicitMember dimension="bw2-titel9:FinancialStatementsTypeAxis">
      bw2-titel9:ConsolidatedMember
    </xbrldi:explicitMember>
  </xbrli:scenario>
</xbrli:context>

<!-- Company-only statement fact -->
<xbrli:context id="separate-current">
  <xbrli:entity>
    <xbrli:identifier scheme="http://www.kvk.nl/kvk-id">12345678</xbrli:identifier>
  </xbrli:entity>
  <xbrli:period><xbrli:instant>2025-12-31</xbrli:instant></xbrli:period>
  <xbrli:scenario>
    <xbrldi:explicitMember dimension="bw2-titel9:FinancialStatementsTypeAxis">
      bw2-titel9:SeparateMember
    </xbrldi:explicitMember>
  </xbrli:scenario>
</xbrli:context>
```

### 4.1 Placeholder membership across both scopes

The KvK taxonomy declares scope/basis-specific placeholder roles that
anchor the extension's line-items into consolidated or separate
financial-statement hypercubes. In the FY2025 NL-GAAP release these
surface through placeholder concepts such as:

- `kvk:LineItemsInConsolidatedFinancialStatementsPlaceholder`
- `kvk:LineItemsInSeparateFinancialStatementsPlaceholder`

Both are confirmed members of `kvk-cor.xsd` in the FY2025 release. An
extension concept reported in both scopes must be wired into **both**
relevant placeholder domain-member trees via the extension's definition
linkbase. Forgetting one of them — typically because an extension
concept was added late without re-wiring the dual-scope arcs — fires a
KvK-specific filing-rule error of the form
`extensionTaxonomyLineItemNotLinkedToDesignatedPlaceholder` and
downstream `xbrldie:PrimaryItemDimensionallyInvalidError` against the
unwired scope's contexts.

The RM/taxonomy architecture also defines two gatekeeper roles:

- `[990080]` — line items to be reported as non-dimensional. These are
  not valid with dimensions.
- `[990090]` — line items that may be reported dimensionally only when
  the preparer's extension explicitly allows that use.

The consolidated/separate placeholders are for the single
financial-statements-type axis only. If a fact also uses another axis
— for example an equity-class axis in the statement of changes in
equity — build a proper extension definition role for that
multi-dimensional schedule rather than relying only on the KVK
placeholder.

Practitioner reports describe an additional extension-side compatibility
role (often called something like
`MixedScopeFinancialStatementsCompatibility`) used by some filer
extensions to declare which concepts are legitimately reportable across
both scopes. The KvK base taxonomy does not define this role — it
appears in filer-extension architectures. Whether you must wire it
depends on the extension framework your tooling uses; check the
extension's `*_def.xml` for the actual extended-link roles in use
before treating the absence of a specific role as a defect.

Fix pattern: treat dual-scope placeholder membership as derived from
one source predicate so the two arcs cannot drift apart, and document
the extension's compatibility-role convention (if any) alongside it.

### 4.2 Calculation linkbase scope-bleed — and why Calc 1.1 is the RTS basis

A `link:calculationLink` is grouped by extended-link role but is **not**
context-scoped — XBRL 2.1 binds every contributing item present in
**every** context where the summation concept also has a fact. So a
"BalanceSheetConsolidated" network binds against separate contexts too,
where the children may legitimately differ. Under Calc 1.1 round-to-
nearest semantics this surfaces as
`calc11e:inconsistentCalculationUsingRounding`; under Calc 1.0 the
binding is typically *skipped* (it requires *all* contributing items
present), so the same architectural fact stays invisible.

**For FY2025 KvK iXBRL Report Packages, Calc 1.1 (`--calc c11r`) is
the RTS Annex III calculation basis.**
The reasons:

- Calc 1.1 uses OIM rounding semantics rather than XBRL 2.1
  fact-level decimals, so iXBRL's routinely-duplicate facts (the same
  number tagged in a summary and a footnote) no longer produce false
  calc errors when their values agree within their declared precision.
- The cross-scope inconsistencies Calc 1.0 hides are real information
  about the dual-statement architecture. "Diagnostic" does not mean
  "noise" — it means the inconsistency does not need to be fixed *if*
  it is a cross-scope artefact, and it does need to be fixed if it
  isn't.
- The IFRS Accounting Taxonomy began publishing Calc 1.1 relationships
  from the 2024 release; SBR Dutch GAAP filings that import IFRS
  concepts (KvK IFRS entry points, AFM ESEF) are effectively already
  operating in a Calc 1.1 world for those concepts.

Run Calc 1.0 only as a legacy / compatibility pass if the operative
validator profile or filing channel still applies older FR-NL checks.
Do not treat an older Calc 1.0 assumption as overriding the FY2025
iXBRL RTS unless the current validator profile actually does so.

```bash
# FY2025 KvK iXBRL RTS pass
arelleCmdLine --plugins inlineXbrlDocumentSet|validate/NL \
              --calc c11r \
              --packages <NT package>.zip \
              -f report-package.zip --validate

# Legacy / compatibility pass only if the operative validator profile uses it
arelleCmdLine --plugins inlineXbrlDocumentSet|validate/NL \
              --calc c10 \
              --packages <NT package>.zip \
              -f report-package.zip --validate
```

Before concluding a calc network is broken, classify each
inconsistency by reading the `context …` and `link role …` fields:
*in-scope* (role-scope == context-scope) is a real arithmetic gap to
fix; *cross-scope* (role-scope ≠ context-scope) is the dual-statement
artefact — useful information that the dual-scope architecture is in
play, but not in itself a defect. See `validation.md` §4 for the full
binding-rule discussion.

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

## 5. Recurring KvK deposit-blocker patterns

The KvK Filing Rules / Business Rules (NT20 supplement) layer
KvK-specific validations on top of the SBR Filing Rules. The
authoritative code list lives in the operative
`KVK Business Rules NT20` PDF and the SBR-domein Handelsregister
**Reporting Manual** and **RTS**. Re-check those for the exact rule
numbers that apply to a given filing — they evolve per release and
this skill must not invent specific numbers it cannot cite.

The recurring deposit-blocker **patterns** (what gets caught, not the
exact rule code) are:

| Pattern | Typical root cause | Fix |
|---|---|---|
| `extensionTaxonomyLineItemNotLinkedToDesignatedPlaceholder` — an extension concept is missing from one of the `kvk:LineItemsIn{Consolidated,Separate}FinancialStatementsPlaceholder` domain-member trees | Concept added to one scope's placeholder but not the other (dual-scope drift) | Wire the concept into both placeholders via the extension `*_def.xml`; derive both arcs from one source predicate (§4.1) |
| `usableConceptsNotAppliedByTaggedFacts` — a concept exists in the extension presentation/definition linkbase but is never tagged in the instance | Over-inclusive linkbase (concept stayed after a tagging redesign) | Remove the unused concept from the linkbase **or** add the missing fact |
| `transformableElementIncludedInHiddenSection` — a numeric / transformable fact is emitted into `ix:hidden` | Convenience hiding of facts that don't fit visually | Render visibly; only non-transformable required-metadata facts belong in `ix:hidden` |
| `missingRelevantPlaceholder` — a primary statement roots on an extension abstract rather than the official Title 9 / RJ root (e.g. `bw2-titel9:BalanceSheetTitle`, `bw2-titel9:IncomeStatementTitle`, `rj:CashFlowStatementTitle`) | Generator emitted its own abstract root | Replace the root with the operative placeholder |
| `extensionTaxonomyWrongFilesStructure` — calculation linkbase file exists but contains no `link:calculationArc` | Empty calc linkbase emitted as a placeholder | Either populate the calc linkbase or remove the file from the package |

For the exact rule code that fired (the
`NL-KVK.<n>.<n>.<n>...` identifier), quote the validator log line
verbatim and look the code up in the operative Filing Rules /
Business Rules PDF — do not paraphrase from memory.

Two non-Filing-Rule signals routinely surface in NL reviews:

- `xbrl.4.8.2:sharesFactUnit-notSharesMeasure` — share-count concepts
  (`bw2-titel9:ShareCapital*`, `bw2-titel9:ShareCapitalNumberSharesIssue`)
  tagged with a currency unit instead of `xbrli:shares`. Audit every
  `xbrli:sharesItemType` concept's unit.
- `xbrldie:PrimaryItemDimensionallyInvalidError` — the concept is
  missing from one of the `kvk:LineItemsIn{Consolidated,Separate}FinancialStatementsPlaceholder`
  domain-member trees, so its fact's dimensional context is invalid.

## 6. FR-NL- / FG-NL- — SBR Filing Rules / Filing Guidelines

These rules are taxonomy-agnostic (they apply across NT generations
and across SBR channels — KvK, Belastingdienst, DNB). The high-frequency
**rule families** are:

| Family | Topic |
|---|---|
| Encoding | UTF-8, no BOM, correct XML declaration |
| Language | Non-numeric facts carry `xml:lang` for the report language |
| `link:schemaRef` | Placement and count |
| Period | `xbrli:forever` periods forbidden; times stripped from instant periods |
| Numeric attributes | `precision` forbidden — use `decimals`; `decimals="INF"` not allowed for rounded values |
| `xsi:nil` | `xsi:nil="true"` on a reported fact forbidden — omit the fact instead |
| Footnotes | Specific model and arcroles |

The exact code numbers (`FR-NL-x.xx`, `FG-NL-x.xx`) and the rule prose
live in the operative Filing Rules / Filing Guidelines PDF on
sbr-nl.nl. When a validator log cites a code, look the code up in the
PDF rather than paraphrasing from memory — the numbering has shifted
between releases, and a renumbered rule is no longer the rule you
remembered.

The KvK Business Rules (NL-KVK.* family in §5) layer
KvK-specific validations on top of these. Re-check both code families
when validating.

## 7. The auditor's report (controleverklaring) in the package

For Middelgroot and Groot entities subject to art. 2:393 BW, the
auditor's report is **part of the deposit**, not optional commentary.
The 2025 KvK taxonomy provides two related concepts:

- **`bw2-titel9:AuditorsReportFinancialStatements`** (`xsd:element`
  declared in `bw2-titel9-cor.xsd`) — the text-block concept carrying
  the auditor's report content. Tagged as `ix:nonNumeric escape="true"`
  in iXBRL with the controleverklaring's XHTML as the fact value.
- **`kvk:AuditorsReportFinancialStatementsPresent`** (declared in
  `kvk-cor.xsd`) — a boolean flag asserting whether the auditor's
  report is included in the deposit. In the operative FY2025 Groot
  example package this fact is tagged in the KvK-metadata iXBRL
  document with `format="ixt:fixed-true"` and value `"Ja"` when
  present.

The xBRI Report Package shape observed in the operative FY2025 Groot
NL-GAAP example:

```text
report-package.xbri
├── META-INF/
│   ├── catalog.xml
│   ├── reportPackage.json          # {"documentInfo":{"documentType":
│   │                                #   "https://xbrl.org/report-package/2023/xbri"}}
│   └── taxonomyPackage.xml
├── reports/
│   └── jaarrapportage-<period>/
│       ├── jaarrapportage-<period>-nl.xhtml   # primary statements (annual report)
│       └── kvk-<period>-nl.xhtml              # KvK filing metadata
│                                              # carries kvk:AuditorsReportFinancialStatementsPresent
└── <filer-domain>/xbrl/<period>/              # filer's extension taxonomy
    ├── <filer>-<period>.xsd
    ├── <filer>-<period>_cal.xml
    ├── <filer>-<period>_def.xml
    ├── <filer>-<period>_lab-nl.xml
    └── <filer>-<period>_pre.xml
```

### 7.1 NBA Alert 50: accountant consent and conversion scope

NBA Alert 50 (26 June 2025) is the accountant-facing source for SBR
Report Package situations where the originally audited annual accounts
were not themselves prepared as an SBR Report Package. Its practical
point for reviewers: a technical conversion to iXBRL can create a gap
between the original audited accounts, the visible XHTML, and the
machine-readable XBRL facts.

When the original controleverklaring is reproduced in the SBR Report
Package after that conversion, treat it as a **new publication** of the
auditor's report. Do not infer assurance over the technical conversion,
RTS compliance, extension taxonomy, or XBRL markings merely because the
controleverklaring is present in the package. NBA Alert 50 describes
the conditions and work needed before the external auditor can give
written consent, and distinguishes that from a voluntary assurance
engagement under Standard 3950N.

For review work, use the Alert as a prompt to separate three questions:

- Does the visible XHTML faithfully reproduce the audited annual
  accounts, allowing only legitimate filing exemptions?
- Does the SBR Report Package meet the minimum technical validation /
  RTS acceptance criteria for KvK filing?
- Is the machine-readable XBRL layer materially consistent with the
  visible XHTML after a consistent transformation of the tags?

An NBA Alert is transitional professional guidance: the PDF says alerts
normally expire after one year unless explicitly extended. Cite the
current NBA page before treating Alert 50 as live professional guidance
for an engagement.

Reviewer checks:

- The package uses `META-INF/reportPackage.json` (xBRI 2023) or
  `META-INF/reports.json` (Report Packages 1.0) — both are present in
  the wild. Single-file iXBRL deposits without a manifest are not
  acceptable for KvK Groot.
- The `kvk:AuditorsReportFinancialStatementsPresent` flag matches the
  filer's actual situation (`Ja` when the controleverklaring is in the
  deposit; `Nee` when it is legitimately absent — e.g. art. 2:403 BW
  group-subsidiary exemption, or a Klein/Micro entity).
- When the controleverklaring text is included, the
  `bw2-titel9:AuditorsReportFinancialStatements` fact's escaped XHTML
  value preserves table structure, headings, signature block, date,
  and auditor identification. The escaped XHTML *is* the fact value;
  a screenshot is not.
- If the controleverklaring is reproduced after a technical conversion
  from paper / Word / PDF accounts into an SBR Report Package, apply
  NBA Alert 50 before assuming the auditor has consented to that new
  publication or provided assurance over the XBRL markings.
- The auditor's report concept appears in **some** presentation link in
  the extension — orphaned-tagged facts trip `validate/NL`
  equivalents of `ESEF.3.4.6.UsableConceptsNotIncludedInPresentationLink`.
- For art. 2:403 BW group-subsidiary exemption filings, the absence of
  the auditor's report on a Groot entity is not automatically wrong —
  cross-check the management report / 403-statement before flagging.
  The 403-exemption KvK example package on sbr-nl.nl
  (`403_voorbeeld-2025-12-31-nl.xbri`) shows the canonical pattern.

### 7.2 Foreign group head exemption (art. 2:403 / 2:408 BW) — a DIFFERENT package shape

When a **foreign parent's group annual report** is deposited to support
an NL entity's exemption (art. 2:403 group exemption, or art. 2:408
consolidation exemption), the package is **not** the shape in §7 / §1
above. Verified against the official FY2025 example
`403_voorbeeld-2025-12-31-nl.xbri` (downloaded and unzipped):

- The IXDS holds **two XHTML documents**: the foreign group report
  carried **UNTAGGED** (zero `ix:` tags), plus a separate **iXBRL
  filing-data document** that carries all the markup.
- META-INF contains **only `reportPackage.json`** (xBRI 2023). **No
  `catalog.xml`, no `taxonomyPackage.xml`, no filer extension
  taxonomy** — the §1/§7 layout above is the *Groot own-accounts* shape,
  wrong for this case.
- `link:schemaRef` → the KvK **"Other" entry point**, FY-dated: FY2025
  `https://www.nltaxonomie.nl/kvk/2025-12-31/kvk-annual-report-other.xsd`
  (FY2024 was `…/2024-12-31/kvk-annual-report-other-gaap.xsd`, note the
  `-gaap` suffix). **Same entry point for both 403 and 408.**
- The filing-data file describes the **NL entity** claiming the exemption
  (its KvK number / name / legal form / seat); the untagged report is the
  **foreign parent's** group accounts. One package per NL entity.

Mandatory facts in the filing-data document (RTS Annex II, Table 2 +
Table 3), against entity scheme `http://www.kvk.nl/kvk-id` and one
`duration` context: `bw2-titel9:ChamberOfCommerceRegistrationNumber`,
`:LegalEntityName`, `:LegalEntityLegalForm`, `:LegalEntityRegisteredOffice`,
`kvk:LegalEntitySize` (enum), `bw2-titel9:FinancialReportingPeriodEndDate`,
`:FinancialReportingPeriod`, `rj:FinancialStatementsConsolidated`,
`kvk:AuditorsReportFinancialStatementsPresent`,
`bw2-titel9:DocumentAdoptionStatus`, and (if adopted)
`bw2-titel9:DocumentAdoptionDate`.

The article is distinguished **only** by one boolean (both
`xbrli:booleanItemType`, `periodType=duration`, tagged
`format="ixt:fixed-true"` value `Ja`, **must be True, never False**):

- art. 2:403 → `kvk:AnnualReportOfForeignGroupHeadForExemptionUnderArticle403` (rules G7-1-4_1 / G7-1-4_2)
- art. 2:408 → `kvk:AnnualReportOfForeignGroupHeadForExemptionUnderArticle408` (rules G7-2-1_1 / G7-2-1_2; note the manual's G7-2-1_2 has a typo naming the 403 QName)

**Timing (bi-temporal — see §2).** The 403 iXBRL route is operative for
FY2025. The 408 iXBRL route + 408 boolean are mandatory only for
**financial years starting on or after 2026-01-01**; FY2025 art. 2:408
filings may still be submitted **by PDF email**.

Note: in the FY2025 403 example, `kvk:AuditorsReportFinancialStatementsPresent`
is **`Ja`** — set it per the actual deposit, not by assuming the
exemption implies the auditor's report is absent.

Validate this package type with
`--disclosureSystem NL-INLINE-2025-GAAP-OTHER-PREVIEW` (§12).

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

Arelle accepts these because they exist somewhere in the operative DTS;
the auditor doesn't.

| Wrong | Right | Why it matters |
|---|---|---|
| `rj:Creditors` for trade payables | `bw2-titel9:TradePayablesCurrent` (or `TradePayablesNoncurrent`) | Both concepts exist. `rj:Creditors` is a broad RJ fallback covering all amounts owed; `bw2-titel9:TradePayables*` is the Title 9 line item. Using the broad concept loses the disclosure detail Title 9 requires. |
| `rj:Result` used as a generic profit/loss line | The specific Title 9 income-statement concept (e.g. `bw2-titel9:NetResultAfterTax` for total result; `bw2-titel9:ResultBeforeTax`; the appropriate `rj:*` for movements) | Both `bw2-titel9:Result` and `rj:Result` exist as concepts, but neither is "the" result line for a Title 9 income statement. Pick the specific concept the statement reports, not the broad fallback. |
| `rj:TreasurySharesMovement` on financing-activity rows in the cash flow | The specific bw2-titel9 / rj movement concept | `rj:TreasurySharesMovement` is the equity-side movement; cash spent on treasury shares is a separate financing-activity outflow. |
| `rj:PayablesBanksCurrent` | `bw2-titel9:PayablesBanksCurrent` | `rj:PayablesBanksCurrent` does not exist; the concept lives under `bw2-titel9:`. Right local name, wrong prefix → unbound fact. |
| `bw2-titel9:InvestmentsInParticipatingInterests` as a flat line item | The typed-dimension architecture: `bw2-titel9:InvestmentsInParticipatingInterestsTypedAxis` with member; the substantive concepts are typed-dimension members, not a single flat concept | Title 9 captures participating interests as a typed dimension, not as a single flat line. Tagging a flat concept that doesn't exist as a non-dimensional concept will be unbound. Verify the actual axis usage in the example annual reports on sbr-nl.nl. |

When reviewing a KvK iXBRL package, run a per-concept namespace check:
every fact's QName must resolve to a concept declared in (or imported
into) the operative DTS. The exact prefix-to-URI bindings used by FY2025
KvK NL-GAAP filings are catalogued in §1; verify each tagged fact's
prefix against that table. Use `arelleCmdLine ... --saveInstance` to
extract the underlying XBRL instance and grep for missing-reference
warnings (`ix11.12.1.2:missingReferences`, `xbrl.3.5.4:hrefIdNotFound`)
before any content review.

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
# FY2025 KvK iXBRL RTS pass — Calc 1.1 (see §4.2)
arelleCmdLine \
  --plugins inlineXbrlDocumentSet|validate/NL \
  --disclosureSystem NL-INLINE-2025 \
  --packages NT20-20251212.zip,kvk-nt20-fr-ifrs-2025.zip \
  --calc c11r \
  -f report-package.zip --validate \
  --internetConnectivity offline
```

The operative `validate/NL` disclosure systems for FY2025 are
**`NL-INLINE-2025`** (an entity's own NL-GAAP / NL-IFRS accounts) and
**`NL-INLINE-2025-GAAP-OTHER-PREVIEW`** (the KvK "Other" entry point —
used for the foreign-group-head 403/408 filings in §7.2). Earlier
editions of this file cited `nl-fr-nt20-kvk-ifrs-2025`; that name is
**not** registered in Arelle — the `validate/NL` `config.xml` declares
the `NL-INLINE-2025*` names above (and their lowercase aliases), so the
old name silently falls back to no disclosure system. Confirm the
operative name in your build with `arelleCmdLine --plugins validate/NL
--showEnvironment`. Run a second pass with `--calc c10` only if the
operative validator profile or filing channel still applies older
Calc 1.0 checks. When validation is slow or intermittent, suspect
remote-taxonomy resolution before suspecting the package.

## 13. A pragmatic NL review pass — in order

When a user says "please review my SBR Dutch GAAP report package",
walk this in order. Each step depends on the prior being clean.

1. **Pin the regime, period, NT generation, and entry point.** §1 and
   §2. State them back to the user before opening the file. If any
   are ambiguous, ask.
2. **Pin the entity-size class.** §3. The size class changes which
   absences count as defects (auditor's report, certain disclosures).
3. **Pin the RTS Article 4 statement scope.** §4.0. If both
   consolidated and company financial statements are present under IFRS
   and/or NL-GAAP, detailed statement tagging applies at least to the
   consolidated statements. If only company statements are present, tag
   those. If both scopes are tagged, verify the basis-specific
   consolidated/separate dimensions and placeholder roles before
   interpreting validation errors.
4. **Run validation in the operative profile, offline.** §12. Capture
   the full log, including warnings. Run **Calc 1.1** (`--calc c11r`)
   as the FY2025 KvK iXBRL RTS calculation basis (it handles iXBRL
   duplicate facts and surfaces the dual-statement cross-scope
   inconsistencies Calc 1.0 hides). Run **Calc 1.0** (`--calc c10`)
   only as a legacy / compatibility pass if the operative validator
   profile still applies it (§4.2).
   Classify any cross-scope inconsistency by role-vs-context before
   treating it as a defect.
5. **Classify each finding.** Route by code prefix using `SKILL.md`'s
   common-error decision tree. Distinguish dual-scope artefacts (§4.2)
   from real arithmetic defects, and rule violations from style
   warnings.
6. **Concept-binding pass.** §9. Confirm every fact's QName resolves
   in the operative DTS. `missingReferences` is harder to fix than
   surface validation errors and changes the meaning of every
   downstream check.
7. **Per-scope value pass.** §4.3. For consolidated + separate filings,
   sample a dozen line items and confirm the value belongs in the
   scope it appears in. No validator catches this for you.
8. **Sign and period class.** §10, §11. Walk the IS, CF, and SoCE.
9. **Presentation pass.** §8. Roots on official placeholders, IS/CF
   flat, BS nested, every tagged fact placed somewhere.
10. **Package shape.** §7. Auditor's report present if size class
   requires; metadata facts present and tagged; no MacOS artefacts
   (`.DS_Store`, `__MACOSX/`) at package root. If the package contains
   a reproduced controleverklaring after technical conversion, separate
   the statutory audit opinion from any consent / assurance question
   under NBA Alert 50.
11. **Content-level review (read the rendered statements).** See
    `conversion.md` §10. The validators cannot tell whether the iXBRL
    is faithful to the source document; you can.

When a finding is unclear, **quote the validator log line verbatim**
and route by the code prefix in step 4 — that is the cheapest way to
distinguish a real defect from a known artefact.

## 14. When to escalate to primary sources

This file is a reviewer's working reference, not the legal source.
Defer to and cite:

- **SBR-domein Handelsregister project page** for the current RTS, RM,
  FAQ, conformance suite, taxonomy packages, and example `.xbri`
  filings — <https://www.sbr-nl.nl/sbr-domeinen/handelsregister/uitbreiding-elektronische-deponering-handelsregister>
- **RTS SBR-domein Handelsregister** for FY2025 iXBRL / XBRL filing
  requirements, Annex II mandatory markups, Annex III specifications,
  and Annex IV markup / extension rules.
- **Reporting Manual SBR-domein Handelsregister** and **KVK taxonomy
  documentation** for practical iXBRL construction, consolidated /
  separate placeholders, contexts, extension DRS, and examples.
- **SBR Nederland Filing Rules (FR-NL- / FG-NL-)** — <https://www.sbr-nl.nl/>
- **KvK Filing Rules supplements (NL-KVK.*)** — published with each
  NT generation; the PDF lives in the same documentation tree.
- **Title 9 Book 2 BW** for legal disclosure obligations
  (`wetten.overheid.nl`).
- **Richtlijnen voor de Jaarverslaggeving (RJ)** for Dutch GAAP
  application detail.
- **NBA Alert 50** for external-accountant consent, scope, and
  controleverklaring wording in SBR Report Package situations —
  <https://www.nba.nl/wet--en-regelgeving/alerts/nba-alert-50/>.
- **AFM ESEF guidance** for listed-issuer filings (then return to
  `esef.md`).
- **Arelle `validate/NL` plugin `config.xml`** for the registered
  disclosure-system names (`NL-INLINE-2025`,
  `NL-INLINE-2025-GAAP-OTHER-PREVIEW`, and their aliases) — the operative
  reference when a `--disclosureSystem` name silently fails to bind —
  <https://github.com/Arelle/Arelle/tree/master/arelle/plugin/validate/NL>.

If the question concerns a rule version newer than what this file
cites, or a code not listed in §5 / §6, say so and link the primary
source. The cost of a wrong citation on a regulated filing is high.
