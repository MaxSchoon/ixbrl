# Validation Reference — Arelle, iXBRL, and the silent killers

If a code or behaviour is not cited here, treat it as folklore until verified in source.

## 1. Arelle — the de facto reference processor

**Arelle** is the open-source XBRL platform (desktop, REST, CLI, Python library) that ESMA, the SEC, HMRC, the UK FRC, the Dutch KvK ecosystem and most commercial XBRL tools either embed or benchmark against. When a regulator says "the file did not validate", in practice that means "Arelle (or a derivative) emitted an error code".

### Installation

```bash
pip install arelle-release                              # minimal
pip install arelle-release[Crypto,DB,EFM,WebServer]     # SEC/EBA work
arelleCmdLine --help
arelleGUI                                                # desktop app

# Docker
docker run arelleproject/arelle:latest python arelleCmdLine.py --help
docker run --name arelle-webserver -p 8080:8080 arelleproject/arelle:latest /opt/start.sh
```

Bundles for Windows/macOS/Linux are at https://arelle.org/arelle/pub/
and on the GitHub releases page.

### Canonical command-line invocation

```bash
arelleCmdLine \
  --plugins "validate/ESEF|inlineXbrlDocumentSet" \
  --disclosureSystem esef-2024 \
  --validate \
  --file report-package.zip \
  --logFile validation.xml \
  --logFormat "[%(messageCode)s] %(message)s - %(file)s %(sourceLine)s"
```

Key flags: `--plugins` selects validators (pipe-separated),
`--disclosureSystem` selects the regulator profile, `--validate`
triggers full validation, `--file` accepts a zip report package, an
XHTML, or an instance XBRL.

## 2. Plugins relevant to iXBRL

**`validate/ESEF`** — ESMA's European Single Electronic Format
validator. Implements the full numbered ruleset (`ESEF.2.x`,
`ESEF.3.x`, `ESEF.4.x`) plus UKSEF / UK FRC overlays (`UK.ESEF.*`,
`UKFRC.*`, `UKFRC22.*`). Mandatory for European listed-issuer work.

**`validate/EFM` (Arelle/EDGAR repo)** — The SEC's EDGAR Filer Manual
validator. As of mid-2025 the SEC consolidated validator, renderer,
transforms, and HTM validator into https://github.com/Arelle/EDGAR,
maintained by SEC staff (CC0-1.0). Newer rules (us-gaap/2025+) are
implemented in XULE / DQCRT; older rules remain in Python.

**`validate/UK` (HMRC + UK FRC)** — UK regulator validation including
UKSEF and UK FRC entry-point requirements.

**`validate/EBA`** — European Banking Authority validator for COREP /
FINREP / Resolution / Supervisory Benchmarking. Drives the
formula-linkbase-heavy DPM rules.

**`validate/NL`** — Netherlands-specific validations supporting SBR
(KvK iXBRL deposits, Nederlandse Taxonomie reporting rules).

**`inlineXbrlDocumentSet`** — Mandatory plumbing for iXBRL. Treats one
or more XHTML files as a single Inline XBRL Document Set (IXDS), reads
zip / manifest, lets you `--saveInstance` to extract the underlying
XBRL instance for downstream XBRL-only validators.

**`OimTaxonomy` / report-package handling** — Taxonomy package + report
package loading. Arelle understands `.zip` report packages with
`META-INF/taxonomyPackage.xml`, `META-INF/reports.json`, and the
`reports/` folder.

**`transforms/`** — Inline XBRL Transformation Registry implementations
(TR1–TR5).

## 3. Formula linkbase

**XBRL Formula 1.0** lets a taxonomy author ship machine-checkable
business rules far beyond what XBRL 2.1 calculation arcs can express:

- **Value assertions** — boolean expressions over fact sets ("revenue minus cost-of-sales equals gross profit, ±0.5 unit").
- **Existence assertions** — fact-presence rules ("if `IncomeTaxExpense` is reported, `EffectiveTaxRate` must exist for the same period").
- **Consistency assertions** — bind a calculated formula output to a reported fact and require they match within tolerance.
- **Variables, filters, generic-message linkbases** — composable building blocks.

Regulators ship formula linkbases as part of their taxonomy /
conformance suite. ESMA distributes them inside the ESEF Conformance
Suite zip; EBA bakes them into DPM; the SEC ships them via XULE /
DQCRT (different language, same role). Arelle reports formula
assertion failures through the standard logging pipeline; verify with
`--formulaParamExprResult` and `--formulaAsserResultCounts` flags.

## 4. Calculations 1.1 vs 1.0

**Calculation 1.0** — original `summation-item` mechanism baked into
XBRL 2.1. XML-syntactic parent-child arcs with `weight` attributes;
brittle in the face of dimensional facts, nil values, duplicates, and
rounding/`decimals` mismatches.

**Calculations 1.1** — XBRL Recommendation 14 February 2024. Provides
"improved handling of rounded and duplicate facts, particularly
relevant to Inline XBRL-based reporting" and updates calculation
functionality to leverage Open Information Model semantics rather than
the XML syntactic definitions of XBRL 2.1.

Practical implications:

- Reporting in OIM-semantic terms means duplicate facts (which iXBRL produces routinely — same concept tagged in multiple places) no longer trip false calc errors when their values agree within their declared precision.
- Rounding tolerance is computed from the strictest declared `decimals` across the operands.
- Calc 1.1 is opt-in: the taxonomy must declare a `calculation-1.1` arcrole.

**Adoption status (2026):** ESEF accepts both; SEC EFM is still
primarily on calc 1.0 with rounding consistency rules layered on top
via EFM checks; the IFRS Taxonomy began publishing 1.1 calc
relationships from the 2024 release.

**Dual statement sets — a Calc 1.1 trap that Calc 1.0 hides.** A
calculation network lives in an extended-link role, but the link role
only *groups* the arcs; it does **not** restrict which contexts they
apply to. A summation-item network is evaluated for **every** context in
which its summation concept has a fact. So when an entity files both a
consolidated and a separate (company-only) statement set that share base
concepts — `bw2-titel9:Assets`, `AssetsCurrent`, `Liabilities`,
`NetResultAfterTax`, distinguished only by a member such as
`FinancialStatementsTypeAxis` Consolidated/Separate — the
"BalanceSheetConsolidated" network is *also* bound against the separate
contexts (and vice versa), where its children follow a different
structure. Calc 1.1 round-to-nearest reports these as
`calc11e:inconsistentCalculationUsingRounding` (it binds whenever *some*
contributing items are present and the present items don't sum), whereas
Calc 1.0 typically **skips** the binding (it requires *all* contributing
items present). The result: a filing can be clean under `--calc c10`
and show a dozen+ cross-scope inconsistencies under `--calc c11r`.

This is **inherent to dual full-tagging** and is not removable without
mis-tagging (you cannot invent a separate-scope subtotal that does not
exist). Resolve it by validating with the **regulator's actual calc
profile**: the SBR Filing Rules (NT20) list **XBRL 2.1** — i.e. Calc 1.0 —
as the normative calculation basis (Calculations 1.1 is *not* referenced,
and Calculations 2.0 has only a 2019 requirements note, no specification),
so run `arelleCmdLine ... --calc c10` for the authoritative KvK verdict and
treat the `c11r` cross-scope warnings as diagnostic, not blocking. Before
concluding a calc is "broken," classify each inconsistency: *in-scope*
(role-scope == context-scope) is a real arithmetic gap to fix; *cross-
scope* (role-scope != context-scope) is this artifact. Distinguish them
by reading the `context …` and `link role …` fields of each message.

## 5. Common error categories with concrete codes

### 5.1 ESEF (European Single Electronic Format)

| Code | Meaning | Typical root cause | Fix |
|---|---|---|---|
| `ESEF.2.1.1.nonLEIContextScheme` | Context identifier scheme is not the LEI scheme | Filer used CIK / KvK number, not LEI URI | Set `<xbrli:identifier scheme="http://standard.iso.org/iso/17442">` |
| `ESEF.2.1.1.invalidIdentifierFormat` | LEI not a valid 20-char ISO-17442 string | Typo or trimmed LEI | Re-key the LEI |
| `ESEF.2.1.2.periodWithTimeContent` | xbrli:period contains a time component | Generated `2024-12-31T00:00:00` | Strip the time portion |
| `ESEF.2.1.3.segmentUsed` | xbrli:segment used (forbidden in ESEF) | Legacy template emitting segment | Replace with xbrli:scenario + dimensions |
| `ESEF.2.1.3.scenarioContainsNonDimensionalContent` | Scenario carries non-dimensional XML | Custom typed-dimension built without xbrldi | Move to `xbrldi:explicitMember` / `xbrldi:typedMember` only |
| `ESEF.2.1.4.multipleIdentifiers` | Different `<xbrli:identifier>` values across contexts | Mixed parent + subsidiary LEI | Keep one identifier per report |
| `ESEF.2.2.1.precisionAttributeUsed` | `precision` attribute on a numeric fact | Hand-edited XBRL | Use `decimals` exclusively |
| `ESEF.2.2.2.percentGreaterThan100` | Percentage fact > 1 (or > 100 depending on scale) | Filer wrote `25` for 25% on a `pure`-typed concept that requires `0.25` | Apply `xbrli:pure` scaling correctly |
| `ESEF.2.2.3.incorrectTransformationRuleApplied` | `format` does not transform the displayed text to the declared datatype | Wrong TR registry version, comma-vs-dot locale mismatch | Pick the correct `ixt:numdotdecimal` / `ixt:numcomadot` etc. |
| `ESEF.2.2.4.inconsistentDuplicateNumericFactInInlineXbrlDocument` | Same concept+context+unit reported with different numeric values | Tagging the same number twice with rounding drift | Make values equal at their declared `decimals` |
| `ESEF.2.2.4.inconsistentDuplicateNonnumericFactInInlineXbrlDocument` | Two non-numeric facts with same context but different text | Translation block tagged twice | Use a single tag and a continuation chain |
| `ESEF.2.2.5.roundedValueBelowScaleNotNull` | Scaled fact rounds to zero but underlying value non-zero | Aggressive `scale="6"` on an immaterial line | Tag at finer scale, or omit |
| `ESEF.2.2.7.improperApplicationOfEscapeAttribute` | `escape="true"` on a non-`textBlockItemType` fact | Block-tagging a single string concept | Only escape on text-block types |
| `ESEF.2.2.8.missingFactID` | iXBRL fact has no `id` attribute | Generator not emitting `id` | Add stable, unique `id` to every ix:nonFraction / ix:nonNumeric |
| `ESEF.2.3.1.unusedFootnote` | ix:footnote not pointed to by any fact | Orphaned footnote element | Delete or wire up via fact-footnote arc |
| `ESEF.2.3.1.footnoteOnlyInLanguagesOtherThanLanguageOfAReport` | Footnotes in non-primary language | English-only footnotes on a Dutch report | Add a footnote in the report language |
| `ESEF.2.4.1.instanceShallBeInlineXBRL` | Non-iXBRL XBRL instance found inside a report package | Mis-zipped extension | Remove the .xbrl, use only .xhtml |
| `ESEF.2.4.1.tupleElementUsed` | XBRL tuples used (forbidden in ESEF) | Legacy tuple-based construct | Replace with dimensional facts |
| `ESEF.2.4.1.transformableElementIncludedInHiddenSection` | Numeric / transformable fact in `ix:hidden` instead of visible | Convenience hiding | Render the fact visibly |
| `ESEF.2.4.1.factInHiddenSectionNotInReport` | Hidden fact has no on-page rendering anywhere | Hide-and-forget | Put the fact in the visible XHTML |
| `ESEF.2.4.1.IxHiddenStyleDisallowed` | `style="-esef-ix-hidden:..."` with no link to a hidden fact | Broken hidden-style mechanism | Either remove the style or wire it to a hidden fact |
| `ESEF.2.4.2.htmlOrXmlBaseUsed` | `xml:base` / HTML `<base>` in the report | Generator side-effect | Strip the base element |
| `ESEF.2.5.1.executableCodePresent` | `<script>`, embedded JS, or executable element | Templating tooling injected JS | Remove all executable content |
| `ESEF.2.5.2.undefinedLanguageForTextFact` | Non-numeric fact missing `xml:lang` | Translation block without lang | Add `xml:lang="nl"` |
| `ESEF.2.5.3.targetAttributeUsedForESEFContents` | `target` attribute on iXBRL elements within the ESEF report target | Multi-target manifest leakage | Remove `target` for primary report content |
| `ESEF.2.5.4.displayNoneUsedToHideTaggedFacts` | `display:none` on a tagged element | Hiding numbers behind CSS | Render visibly or move to `ix:hidden` correctly |
| `ESEF.2.5.4.externalCssReportPackage` | External CSS file referenced from a report package | URL-linked stylesheet | Inline the CSS or include it in the package |
| `ESEF.2.6.1.incorrectFileExtension` | XHTML report with the wrong extension | `.html` instead of `.xhtml` | Rename to `.xhtml` |
| `ESEF.2.6.3.incorrectNamingConventionReportPackageReportFile` | Report file inside the package does not follow the prescribed naming pattern | Wrong folder or mis-named file | Place under `reports/<lei>-<period>.xhtml` |
| `ESEF.3.3.1.ExtensionConceptAnchoredToAbstractConcept` | Extension element anchored to an abstract base-taxonomy element | Filer anchored to a heading concept | Anchor to a non-abstract base concept |
| `ESEF.3.4.4.missingPreferredLabelRole` | Presentation arc to a subtotal child is missing `preferredLabel="totalLabel"` | Generator did not emit preferred labels for subtotals | Add the preferred label role on the arc |
| `ESEF.3.4.5.taxonomyElementDuplicateLabels` | Same concept has two labels with the same role and language | Re-import collision | Deduplicate labels |
| `ESEF.3.4.6.UsableConceptsNotIncludedInPresentationLink` | Tagged fact's concept missing from any presentation link | Concept tagged but never placed in the report's structure | Add a presentation arc, or remove the tag |
| `ESEF.3.5.1.inlineXbrlDocumentContainsExternalReferences` | iXBRL imports a schema or linkbase from a non-package URL | External `schemaRef` | Bundle the taxonomy in the report package |

### 5.2 SEC EFM (US filings)

| Code | Meaning | Typical root cause | Fix |
|---|---|---|---|
| `EFM.6.05.16` | Default member must not be used in `xbrli:scenario` (must omit the member to assert the default) | Generator emits the default member explicitly | Remove the explicit default member |
| `EFM.6.05.19` | A custom segment / scenario element is not a dimensional construct | Free-form XML in scenario | Replace with `xbrldi:explicitMember` / `xbrldi:typedMember` |
| `EFM.6.05.20.missingAmendmentFlag` | `dei:AmendmentFlag` not reported | Required DEI tag missing | Tag `dei:AmendmentFlag` in the cover page |
| `EFM.6.05.27` | Two contexts have equal period+entity+segment but different IDs | Duplicate contexts with different `id`s | Collapse to one context, repoint contextRef |
| `EFM.6.05.34` | Numeric fact missing `decimals` attribute | `decimals` omitted on a non-nil numeric fact | Add `decimals` (use `INF` only for exact values) |
| `EFM.6.05.36` | Calculation-link inconsistency at the declared decimals | Sum of children does not match parent within tolerance | Fix the data, or revisit `decimals` |
| `EFM.6.05.42` | `xbrli:unit` for a monetary fact does not match the reporting currency declared in DEI | USD-typed unit on a EUR filing | Use the matching ISO-4217 unit |
| `EFM.6.05.45` | Required DEI cover-page tag missing or invalid | `EntityRegistrantName` / `DocumentPeriodEndDate` etc. missing | Tag the missing DEI element |
| `EFM.6.05.48` | Fact with `decimals="INF"` and a non-exact textual representation | Filer rounded but kept INF | Lower `decimals` to match the rendered scale |
| `EFM.6.08.x` | Linkbase validations for industry taxonomies (`cef`, `ecd`, `oef`, `rxp`, `vip`, `sro`, `spac`) | Wrong relationships for the relevant SEC industry overlay | Repair presentation/calculation/definition arcs against the industry config |

### 5.3 SBR Dutch GAAP / KvK (NL-KVK.* and FR-NL- / FG-NL-)

The Dutch filing path layers KvK-specific Filing Rules supplements
(NL-KVK.*) on top of taxonomy-agnostic SBR Filing Rules (FR-NL-).
The KvK supplement is normative for trade-register deposits; FR-NL-
applies across SBR channels (KvK, Belastingdienst, DNB).

| Code | Meaning | Typical root cause | Fix |
|---|---|---|---|
| `NL-KVK.4.4.2.5.extensionTaxonomyLineItemNotLinkedToDesignatedPlaceholder` | Dual-scope extension concept missing from the `MixedScopeFinancialStatementsCompatibility` ELR | Concept added to consolidated **and** separate placeholders without updating the compatibility ELR | Add the missing domain-member arc; treat all three memberships as derived from one source predicate |
| `NL-KVK.4.4.6.1.usableConceptsNotAppliedByTaggedFacts` | Concept present in the extension presentation/definition linkbase but never tagged in the instance | Over-inclusive linkbase (often a concept left behind after a tagging redesign) | Either tag the missing fact or remove the unused concept from the linkbase |
| `NL.NL-KVK.3.4.1.3.transformableElementIncludedInHiddenSection` | Numeric / transformable fact emitted into `ix:hidden` instead of visible | Convenience hiding of facts that don't fit visually | Render the fact visibly; only non-transformable required-metadata facts belong in `ix:hidden` |
| `NL-KVK.*.missingRelevantPlaceholder` | Primary-statement root is an extension abstract, not an official Title 9 / RJ placeholder | Generator emitted its own abstract root | Replace the root with `bw2-titel9:*Title` or `rj:CashFlowStatementTitle` etc. |
| `NL-KVK.*.extensionTaxonomyWrongFilesStructure` | Calculation linkbase exists but is empty (no `link:calculationArc`) | Empty calc linkbase shipped as a placeholder | Populate the calc linkbase or remove the file from the package |
| `FR-NL-1.01` / `1.05` | Encoding violation | Non-UTF-8 source, BOM, or wrong XML declaration | Re-serialise as UTF-8 without BOM |
| `FR-NL-2.03` | Non-numeric fact missing `xml:lang` | Translation block emitted without lang | Add `xml:lang="nl"` (or the report language) |
| `FR-NL-2.04` | `link:schemaRef` placement / count violation | Multiple or mis-placed `schemaRef` elements | Single `schemaRef` in the operative location |
| `FR-NL-3.04` | `xbrli:forever` period used | Forever periods are forbidden in SBR | Use bounded `xbrli:duration` or `xbrli:instant` |
| `FR-NL-5.06` | `precision` attribute on a numeric fact | Carried over from non-SBR templates | Replace with `decimals` |
| `FR-NL-5.07` | `xsi:nil="true"` on a reported fact | Generator nilled a fact instead of omitting it | Omit the fact entirely |
| `FR-NL-6.01` | Footnote model / arcrole violation | Visual footnote not wired as `ix:footnote` | Use the iXBRL footnote model with fact-footnote arc |

The KvK normative calculation basis is **Calc 1.0** — run `arelleCmdLine
... --calc c10`. Calc 1.1 cross-scope warnings are diagnostic, not
deposit blockers (see §4 above). For the dual-scope pattern, the
auditor's report as a separate iXBRL document in the package, the
per-fiscal-year cheatsheet, the size-class entry points, and the
recurring deprecated-concept choices, see `references/nl-sbr.md`.

### 5.4 Core XBRL 2.1 and Inline XBRL

| Code | Meaning | Typical root cause | Fix |
|---|---|---|---|
| `xbrl.5.2.5.2` | Calculation arc inconsistency in summation-item | Sum of weighted children ≠ parent at declared decimals | Either correct the values or, if you've adopted Calc 1.1, declare the 1.1 arcrole |
| `xbrl.5.1.1.4` | Schema-level constraint on item declarations (e.g. `substitutionGroup` not derived from `xbrli:item`) | Custom concept declared with the wrong substitution group | Set `substitutionGroup="xbrli:item"` (or `xbrli:tuple`) |
| `xbrl.4.6` | Type derivation rule violated for an item declaration | Custom item not derived from a base XBRL item type | Derive from `xbrli:monetaryItemType` etc. |
| `xbrldie:PrimaryItemDimensionallyInvalidError` | Primary item used in a hypercube context that isn't valid for it | Wrong dimension combination | Fix the dimensional context, or extend the hypercube |
| `xbrldie:DefaultValueUsedInInstanceError` | Default member of a dimension used explicitly | Tooling emitted the default member | Drop the explicit default |

## 6. Anti-patterns and pitfalls

The silent killers — Arelle either flags them only at the very end,
weakly, or not at all (and you learn from the regulator's downstream
tooling).

1. **Sign-convention errors via "negated terse" labels.** Preparers see `(1,234)` on the page and tag the underlying fact as `-1234`. Result: the reported XBRL value is `-1234` while the calc tree expects `+1234`. Review every `negatedLabel`/`negatedTerseLabel` arc against the underlying numeric sign.
2. **Calc inconsistencies from `decimals` mismatches.** Parent at `decimals="-3"` and child at `decimals="0"`: the calc engine takes the looser `-3` and rounds. Drift accumulates. Reconcile decimals across calc tree levels.
3. **Missing `decimals` on scaled facts.** Scaling `1,234` thousand to "1.234" with no `decimals` is an EFM violation (`EFM.6.05.34`) and an ESEF nonconformance.
4. **Same fact value reported with conflicting `decimals` across documents.** Multi-XHTML iXBRL document sets often tag the same revenue concept twice with different `decimals`. Triggers `ESEF.2.2.4` if values disagree once rounded.
5. **Continuation chain ordering and forking.** `ix:continuation` is a strict singly-linked chain — every continuation referenced exactly once, no loops. Two facts pointing to the same continuation, or a continuation pointing back into the chain, breaks iXBRL 1.1.
6. **`ix:hidden` facts with no transformable rendering elsewhere.** ESEF requires every `ix:hidden` fact to be surfaced visibly somewhere — for transformable types via a normal ix tag, for non-transformable types via the `-esef-ix-hidden` style mechanism.
7. **Extension elements with no anchoring (or anchored to abstract).** Every ESEF extension concept must be anchored to a base-taxonomy concept that is *not* abstract. This is the single most common ESEF.3.x error category.
8. **Duplicate facts (same concept + context + unit, different value).** XBRL 2.1 forbids this; iXBRL inherits the rule. Often comes from tagging both a summary table and a footnote disclosing the same number.
9. **Wrong period type (instant vs duration).** Tagging "Cash at year-end" as a duration fact, or "Revenue" as an instant fact. Match the concept's declared `periodType`.
10. **Identifier scheme drift across contexts.** Mixing LEI and CIK schemes in different contexts of the same instance. ESEF requires a single LEI scheme; SEC requires a single CIK scheme.
11. **Footnotes vs `ix:footnote` element confusion.** Visual footnotes in the rendered XHTML are not XBRL footnotes. The XBRL footnote model is `ix:footnote` plus a fact-footnote arc. Visual footnotes carry zero validation weight.
12. **Empty / whitespace-only `ix:nonNumeric` blocks.** Tagged paragraph with only whitespace is technically valid but useless and frequently trips formula assertions.
13. **Format mismatches (TR transformation against value).** `format="ixt:numcomadot"` on a number rendered with thousands-dot and decimal-comma. Triggers `ESEF.2.2.3`.
14. **Currency mismatch between `unitRef` and reported currency.** EUR-presenting filing tagging revenue with a USD `xbrli:unit`. SEC catches via `EFM.6.05.42`.
15. **Wrong namespace for shared concepts.** A concept exists in exactly one namespace. Using a jurisdiction-extension version when the core concept exists makes the calc tree fail.
16. **`decimals="INF"` on a rounded value.** Asserts the value is exact. If the underlying ledger has more digits, INF is a lie. Triggers `EFM.6.05.48` and equivalent ESEF inconsistency checks.
17. **Tuples used in ESEF reports.** Forbidden (`ESEF.2.4.1.tupleElementUsed`). Migrate to dimensional facts.
18. **External CSS / JS / `<script>` references.** Forbidden in both ESEF (`ESEF.2.5.1`, `ESEF.2.5.4`) and SEC EFM. Inline everything; sanitise the HTML at generation time.
19. **`xml:base` / HTML `<base>` smuggled into the report.** Trips `ESEF.2.4.2.htmlOrXmlBaseUsed`. Most commonly introduced by frontend rendering frameworks. Strip in the iXBRL serialiser.
20. **Default-member explicit emission.** A dimension's default member should be implicit (omitted). Triggers `EFM.6.05.16` / `xbrldie:DefaultValueUsedInInstanceError`.
21. **Concepts tagged but absent from any presentation link.** Triggers `ESEF.3.4.6.UsableConceptsNotIncludedInPresentationLink`.
22. **Subtotal arcs without `preferredLabel="totalLabel"`.** Triggers `ESEF.3.4.4.missingPreferredLabelRole`.
23. **Mismatched `id` references across the iXBRL document set.** Each fact `id` must be unique across the IXDS, not only within a single XHTML file.
24. **Negative values on credit-balance concepts ignored.** Tagging a credit-balance concept with the same sign as a debit-balance concept inverts arithmetic in any downstream consumer. Look up `balance` on the concept declaration and align the sign.
25. **Linkbase arc `from`/`to` pointing at a QName instead of the loc label.** An XLink extended-link arc references the `xlink:label` of a `link:loc`, *not* the concept's QName or href. Authoring a `definitionArc`/`presentationArc`/`calculationArc` with `xlink:from="kvk_LineItemsInConsolidatedFinancialStatementsPlaceholder"` (the resolved concept name) instead of the locator's actual label (e.g. `placeholder_consolidated_loc`, `statement_root_loc`) yields `xbrl.3.5.3.9.2:arcResource` ("attribute 'from' has no matching loc or resource label") and, downstream, `xbrldie:PrimaryItemDimensionallyInvalidError` because the intended domain-member relationship never forms. Beware: audit/dump scripts often *resolve* loc labels to their href localnames for readability, which hides the real label — read the raw `xlink:label` before reusing it as an arc endpoint.
26. **Tagging a concept that does not exist in the operative DTS.** A fact whose `name` is a plausible-but-nonexistent QName — a concept invented from memory (`bw2-titel9:Result` when only `rj:Result` exists), or the right local name under the wrong prefix (`rj:PayablesBanksCurrent` vs `bw2-titel9:PayablesBanksCurrent`) — is **unbound**: Arelle reports `ix11.12.1.2:missingReferences` ("Instance fact missing schema definition") and any locator referencing it fails with `xbrl.3.5.4:hrefIdNotFound` + `xbrl.5.2.6.1:definitionLinkLocTarget`. This is worse than a warning — the fact carries no concept semantics at all. Never guess a QName: confirm the exact prefix *and* local name against the operative taxonomy schema (e.g. grep the `*-cor.xsd` in Arelle's cache, or check the namespace a sibling/twin fact already uses) before tagging. The cheapest catch is to validate early — `missingReferences` surfaces immediately.
27. **Forgetting `META-INF/taxonomyPackage.xml` in the report package.** Without it Arelle cannot locate the taxonomy and validation aborts immediately.

## 7. Conformance suites and test material

- **ESEF Conformance Suite (latest)** — https://www.esma.europa.eu/document/esef-conformance-suite-2024
- **ESEF Reporting Manual** — https://www.esma.europa.eu/document/esef-reporting-manual
- **Inline XBRL 1.1 conformance suite** — https://www.xbrl.org/2020/inlineXBRL-1.1-conformanceSuite-2020-04-08.zip
- **XBRL 2.1 base conformance suite** — https://specifications.xbrl.org/work-product-index-group-base-spec-base-spec.html
- **Calculations 1.1 spec + tests** — https://specifications.xbrl.org/work-product-index-calculations-2-calculations-1-1.html
- **SEC EDGAR XBRL Guide** — https://www.sec.gov/files/edgar/filer-information/specifications/xbrl-guide.pdf
- **Arelle/EDGAR repository** — https://github.com/Arelle/EDGAR
- **SBR Netherlands** — https://www.sbr-nl.nl/
- **EBA reporting framework** — https://www.eba.europa.eu/risk-and-data-analysis/reporting-frameworks/dpm-data-dictionary

## 8. Validation workflow recommendation

A defensible validation pipeline always runs the same steps in the same
order. Skipping a step is how filings reach the regulator broken.

1. **Validate against the base XBRL spec.** Run Arelle with no jurisdiction plugin, just `--validate`. Catches XBRL 2.1 schema, linkbase, dimension and units violations (`xbrl.*`, `xbrldie:*`).
2. **Validate against the jurisdiction's filer-manual rules.** Add `--plugins validate/ESEF` (with `--disclosureSystem esef-2024`), `validate/EFM`, `validate/UK`, `validate/EBA`, `validate/NL` as appropriate. This is where `ESEF.*`, `EFM.*`, `UKFRC.*` codes appear.
3. **Run formula assertions.** Many regulators ship Formula 1.0 linkbases. Verify with `--formulaAsserResultCounts` that the count of unsatisfied assertions is zero.
4. **Verify report-package structure.** Confirm `META-INF/taxonomyPackage.xml` (and `META-INF/reports.json` for newer packages), correct file extensions (`.xhtml`, not `.html`), correct naming, and that the report file lives under the expected `reports/` path.
5. **Hash and seal.** For regulators that require cryptographic sealing (KvK Digipoort/SBR; some EBA flows), produce the digest after step 4 and sign. Do not seal before the prior steps are clean.

## Sources

- https://arelle.readthedocs.io/en/latest/install.html
- https://github.com/Arelle/Arelle
- https://github.com/Arelle/Arelle/tree/master/arelle/plugin
- https://github.com/Arelle/Arelle/blob/master/arelle/plugin/validate/ESEF/ESEF_Current/ValidateXbrlFinally.py
- https://github.com/Arelle/EDGAR
- https://specifications.xbrl.org/work-product-index-calculations-2-calculations-1-1.html
- https://specifications.xbrl.org/work-product-index-formula-formula-1.0.html
- https://specifications.xbrl.org/spec-group-index-formula.html
- https://specifications.xbrl.org/work-product-index-inline-xbrl-inline-xbrl-1.1.html
- https://specifications.xbrl.org/work-product-index-group-base-spec-base-spec.html
- https://www.esma.europa.eu/document/esef-conformance-suite-2024
- https://www.esma.europa.eu/document/esef-reporting-manual
- https://www.sec.gov/files/edgar/filer-information/specifications/xbrl-guide.pdf
- https://www.sbr-nl.nl/
- https://www.eba.europa.eu/risk-and-data-analysis/reporting-frameworks/dpm-data-dictionary
