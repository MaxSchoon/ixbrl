# First principles every preparer must internalise

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*

Eight things that decide whether tagged output is right, independent of
jurisdiction. `SKILL.md` points here; read it before a first review in an
unfamiliar regime, and when a validator passes but the numbers look wrong.

Truths that, when violated, produce silent failures no validator catches early.

## 1. The `decimals` ↔ rendering ↔ value relationship

`ix:nonFraction` carries three numbers in tension: **rendered text**
(what the reader sees), **canonical XBRL value** (what the consumer
parses), and **declared accuracy** (`decimals`).

- `format` (an `ixt:*` transformation, see `references/spec.md` §TRR) converts rendered text to a canonical numeric value.
- `scale` multiplies the parsed text by 10^scale. `scale="3"` on rendered "1,234" yields canonical 1,234,000.
- `decimals` declares accuracy. `decimals="-3"` ≡ "rounded to thousands"; `decimals="0"` ≡ "whole units". **Never use `decimals="INF"` for a rounded value**: it asserts the amount is exact. `INF` is legitimate, and is what the SEC prescribes for an exactly stated figure (EDGAR XBRL Guide section 6.6.4). The checkable violation is the converse, a finite `decimals` that zeroes a non-zero digit of the value (`EFM.6.05.37`, Guide section 9.5), plus the equivalent ESEF inconsistency check.
- `precision` is mutually exclusive with `decimals` on the same fact. **SEC and SBR forbid `precision`**. Use `decimals` only.

Audit rule: canonical value = `transform(rendered_text) × 10^scale × (sign == "-" ? -1 : 1)`. If that doesn't match the natural-language number the reader sees, it's a tagging defect.

## 2. Sign convention, balance type, and `preferredLabel` are three different things

The single most common substantive error in ESEF filings.

- The **canonical XBRL value** is signed per the as-reported mathematical fact; `sign="-"` appears on the inline tag only when parentheses-formatting is used in the host XHTML.
- The concept's **`balance` attribute** (`debit`/`credit` on monetary types) drives downstream arithmetic. Reporting a credit-balance concept with the same sign as a debit-balance concept inverts the result for any balance-respecting consumer.
- The **`preferredLabel` role** on a presentation arc (`terseLabel`, `negatedLabel`, `negatedTerseLabel`, `periodStartLabel`, `totalLabel`, etc.) is a *display* instruction. `negatedLabel` flips the visible sign; the underlying fact is unchanged.

Rule of thumb: never flip a fact's sign to fix visible parentheses. Tag the as-reported absolute value with `sign="-"` iff the value is negative; let preferred-label roles handle display.

## 3. Period type is concept-driven, not document-driven

Balance-sheet concepts (assets, liabilities, equity) are **instant**: `<xbrli:instant>YYYY-MM-DD</xbrli:instant>`. Income statement, OCI, cash-flow, and changes-in-equity flows are **duration**: `<xbrli:startDate>` + `<xbrli:endDate>`.

Mismatching period type to concept class causes `xbrldie:PrimaryItemDimensionallyInvalidError` or schema validation failures. Respect the concept's declared `periodType`.

## 4. Identifier scheme constancy

XBRL 2.1 requires only that each `<xbrli:identifier>` carry a non-empty
`scheme` URI (§4.7.3.1); it imposes no constancy across contexts. Every
filing profile in scope does impose it, and each fixes its own scheme.
ESEF: Reporting Manual Guidance 2.1.1 fixes the scheme at
`http://standards.iso.org/iso/17442`, and Guidance 2.1.4 requires all
entity identifiers and schemes in contexts to have identical content
(`ESEF.2.1.4.multipleIdentifiers`). SEC: EFM 6.5.1 fixes the scheme at
`http://www.sec.gov/CIK`, 6.5.2 requires the content to be the
registrant's CIK, and 6.5.3 requires every `xbrli:identifier` in the
instance to have identical content. SBR Handelsregister: Reporting
Manual G3-1-1_2 fixes the scheme at `http://www.kvk.nl/kvk-id`, and
G3-1-4_1 repeats the identical-content rule (`multipleIdentifiers`); a
Dutch deposit made by the direct-ESEF route carries the LEI scheme
instead. Mixing schemes does not create duplicate facts, it prevents
them: two facts are duplicates only when their contexts are c-equal,
and c-equality requires `xbrli:identifier` elements that are s-equal in
both scheme and value (XBRL 2.1 §4.10). A second scheme splits the
report across two entity identities, so a figure tagged twice is kept
as two facts about two entities and calculation, duplicate, and
comparison checks stop binding.

## 5. Dimensions and axes: XDT is the substrate of every regime

XBRL Dimensions 1.0 ("XDT") makes a fact say more than "this amount, this period". Hypercubes attached to primary items declare which dimensions (taxonomy practice calls them **axes**) apply; the fact's dimensional context lives in `xbrli:segment` or `xbrli:scenario` carrying `xbrldi:explicitMember` (taxonomy-defined members) or `xbrldi:typedMember` (open-ended typed values).

Minimum rules:

- **Default members are implicit.** Never emit a dimension's default member explicitly. Triggers `xbrldie:DefaultValueUsedInInstanceError`.
- **`xbrldt:contextElement` lives on the `all`/`notAll` has-hypercube arc**, not on `hypercube-dimension`. It picks `segment` or `scenario`.
- **ESEF is scenario-only.** Reporting Manual §2.1.3 forbids `xbrli:segment`; `xbrli:scenario` may contain only `xbrldi:explicitMember` / `xbrldi:typedMember`.
- **"Axis" ≠ XDT vocabulary.** XDT uses *dimensions*. "Axis" is FASB/IFRS taxonomy convention (SEC EDGAR XBRL Filing Guide §3.5): a label suffix marking explicit dimensions.
- **Closed hypercubes are exclusive, not exhaustive.** `@xbrldt:closed="true"` restricts the `segment`/`scenario` chosen by `@xbrldt:contextElement` to dimensions *declared by that hypercube*; no others may appear. It does **not** require every declared dimension to be stated: a dimension with a default member may be omitted and is treated as present at its default (XDT 1.0 §3.1.4.3.2). Reading it as "exactly" contradicts the default-member rule above: the default may not be emitted, so a hypercube with a defaulted dimension could never be satisfied.
- **Error namespaces split:** `xbrldie:*` is instance-level (e.g., `PrimaryItemDimensionallyInvalidError`); `xbrldte:*` is taxonomy/DTS-level (e.g., `HasHypercubeMissingContextElementAttributeError`, `TooManyDefaultMembersError`).

See `references/dimensions.md` for the full arcrole table, error codes, explicit-vs-typed contrast, and per-regime axis examples (IFRS, US-GAAP / SRT / DEI, SBR, EBA DPM).

## 6. Anchoring is mandatory only in some regimes, but always good practice

- **ESEF:** anchor every primary-statement extension to the **closest wider** IFRS/ESEF base concept (Reporting Manual 1.4.1), plus to **each** narrower base concept when the extension combines two or more (RTS Annex IV §9(b)). Pure subtotals are exempt from wider anchoring (§10) but must still participate in the calculation linkbase. **Never anchor to an abstract concept** (`ESEF.3.3.1.ExtensionConceptAnchoredToAbstractConcept`).
- **SEC EDGAR:** strongly recommended; EFM and SEC Sample Letter require using base concepts before extensions; IFRS foreign private issuers must anchor under the SEC's IFRS entry-point rules.
- **Dutch SBR / KvK:** fixed entry points by entity-size class; extensions are generally not authored for KvK deposits.

When in doubt, anchor wider.

## 7. Block tagging is structured narrative, not a screenshot

Where note-block tagging is required (ESEF Article 4(2) with Annex II, mandatory from FY2022; analogous regimes elsewhere), an `ix:nonNumeric escape="true"` element wraps the entire note's XHTML. The escaped XHTML *is* the fact value. Preserve tables, lists, headings, and ensure machine-readability after extraction (Reporting Manual 2.2.6). Empty or whitespace-only block tags are valid syntactically but useless and often trip downstream formula assertions.

## 8. The hidden section is for facts that exist, not for facts you're embarrassed by

`ix:hidden` carries facts required in XBRL but with no natural visible rendering (notably SEC `dei:` cover-page facts). ESEF and EFM both require any hidden fact whose value also appears as visible text to be linked via the `-esef-ix-hidden` (ESEF) or `-sec-ix-hidden` (SEC) CSS style. Do not put numeric/transformable facts in `ix:hidden` to suppress them: ESEF forbids it (`ESEF.2.4.1.transformableElementIncludedInHiddenSection`).

The mistake runs both ways. `ix:hidden` is *under*-used as often as it is abused: taxonomy-mandated entity metadata (registered name, registration number, legal form, document/report type, period-end date) and non-numeric classification facts that steer interpretation but are not a line in any statement (an entity-size class member, a reporting-framework choice, a consolidated-vs-company-only indicator) are real required facts with no row to sit on. They belong in `ix:hidden`, not omitted. See `references/conversion.md` §8 for the positive case.
