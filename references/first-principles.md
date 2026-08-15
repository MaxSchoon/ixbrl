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
- `decimals` declares accuracy. `decimals="-3"` ≡ "rounded to thousands"; `decimals="0"` ≡ "whole units". **Never use `decimals="INF"` for a rounded value** — SEC EFM 6.05.16 rejects it; ESEF discourages it; both reject when rendered text is shorter than INF claims.
- `precision` is mutually exclusive with `decimals` on the same fact. **SEC and SBR forbid `precision`** — use `decimals` only.

Audit rule: canonical value = `transform(rendered_text) × 10^scale × (sign == "-" ? -1 : 1)`. If that doesn't match the natural-language number the reader sees, it's a tagging defect.

## 2. Sign convention, balance type, and `preferredLabel` are three different things

The single most common substantive error in ESEF filings.

- The **canonical XBRL value** is signed per the as-reported mathematical fact; `sign="-"` appears on the inline tag only when parentheses-formatting is used in the host XHTML.
- The concept's **`balance` attribute** (`debit`/`credit` on monetary types) drives downstream arithmetic. Reporting a credit-balance concept with the same sign as a debit-balance concept inverts the result for any balance-respecting consumer.
- The **`preferredLabel` role** on a presentation arc (`terseLabel`, `negatedLabel`, `negatedTerseLabel`, `periodStartLabel`, `totalLabel`, etc.) is a *display* instruction. `negatedLabel` flips the visible sign; the underlying fact is unchanged.

Rule of thumb: never flip a fact's sign to fix visible parentheses. Tag the as-reported absolute value with `sign="-"` iff the value is negative; let preferred-label roles handle display.

## 3. Period type is concept-driven, not document-driven

Balance-sheet concepts (assets, liabilities, equity) are **instant** — `<xbrli:instant>YYYY-MM-DD</xbrli:instant>`. Income statement, OCI, cash-flow, and changes-in-equity flows are **duration** — `<xbrli:startDate>` + `<xbrli:endDate>`.

Mismatching period type to concept class causes `xbrldie:PrimaryItemDimensionallyInvalidError` or schema validation failures. Respect the concept's declared `periodType`.

## 4. Identifier scheme constancy

Every `<xbrli:identifier scheme="...">` in an instance must use the **same scheme URI**: ESEF → LEI scheme (`http://standards.iso.org/iso/17442`); SEC → CIK scheme (`http://www.sec.gov/CIK`); SBR → KvK scheme. Mixing schemes silently produces "duplicate fact" errors because consumers treat differently-scheme'd entities as different.

## 5. Dimensions and axes — XDT is the substrate of every regime

XBRL Dimensions 1.0 ("XDT") makes a fact say more than "this amount, this period". Hypercubes attached to primary items declare which dimensions (taxonomy practice calls them **axes**) apply; the fact's dimensional context lives in `xbrli:segment` or `xbrli:scenario` carrying `xbrldi:explicitMember` (taxonomy-defined members) or `xbrldi:typedMember` (open-ended typed values).

Minimum rules:

- **Default members are implicit.** Never emit a dimension's default member explicitly. Triggers `xbrldie:DefaultValueUsedInInstanceError`.
- **`xbrldt:contextElement` lives on the `all`/`notAll` has-hypercube arc**, not on `hypercube-dimension`. It picks `segment` or `scenario`.
- **ESEF is scenario-only.** Reporting Manual §2.1.3 forbids `xbrli:segment`; `xbrli:scenario` may contain only `xbrldi:explicitMember` / `xbrldi:typedMember`.
- **"Axis" ≠ XDT vocabulary.** XDT uses *dimensions*. "Axis" is FASB/IFRS taxonomy convention (SEC EDGAR XBRL Filing Guide §3.5) — a label suffix marking explicit dimensions.
- **Closed hypercubes are exclusive, not exhaustive.** `@xbrldt:closed="true"` restricts the `segment`/`scenario` chosen by `@xbrldt:contextElement` to dimensions *declared by that hypercube* — no others may appear. It does **not** require every declared dimension to be stated: a dimension with a default member may be omitted and is treated as present at its default (XDT 1.0 §3.1.4.3.2). Reading it as "exactly" contradicts the default-member rule above — the default may not be emitted, so a hypercube with a defaulted dimension could never be satisfied.
- **Error namespaces split:** `xbrldie:*` is instance-level (e.g., `PrimaryItemDimensionallyInvalidError`); `xbrldte:*` is taxonomy/DTS-level (e.g., `HasHypercubeMissingContextElementAttributeError`, `TooManyDefaultMembersError`).

See `references/dimensions.md` for the full arcrole table, error codes, explicit-vs-typed contrast, and per-regime axis examples (IFRS, US-GAAP / SRT / DEI, SBR, EBA DPM).

## 6. Anchoring is mandatory only in some regimes — but always good practice

- **ESEF:** anchor every primary-statement extension to the **closest wider** IFRS/ESEF base concept (Reporting Manual 1.4.1), plus to **each** narrower base concept when the extension combines two or more (RTS Annex IV §9(b)). Pure subtotals are exempt from wider anchoring (§10) but must still participate in the calculation linkbase. **Never anchor to an abstract concept** (`ESEF.3.3.1.ExtensionConceptAnchoredToAbstractConcept`).
- **SEC EDGAR:** strongly recommended; EFM and SEC Sample Letter require using base concepts before extensions; IFRS foreign private issuers must anchor under the SEC's IFRS entry-point rules.
- **Dutch SBR / KvK:** fixed entry points by entity-size class; extensions are generally not authored for KvK deposits.

When in doubt, anchor wider.

## 7. Block tagging is structured narrative, not a screenshot

Where note-block tagging is required (ESEF Article 6, mandatory from FY2022; analogous regimes elsewhere), an `ix:nonNumeric escape="true"` element wraps the entire note's XHTML. The escaped XHTML *is* the fact value — preserve tables, lists, headings, and ensure machine-readability after extraction (Reporting Manual 2.2.6). Empty or whitespace-only block tags are valid syntactically but useless and often trip downstream formula assertions.

## 8. The hidden section is for facts that exist, not for facts you're embarrassed by

`ix:hidden` carries facts required in XBRL but with no natural visible rendering (notably SEC `dei:` cover-page facts). ESEF and EFM both require any hidden fact whose value also appears as visible text to be linked via the `-esef-ix-hidden` (ESEF) or `-sec-ix-hidden` (SEC) CSS style. Do not put numeric/transformable facts in `ix:hidden` to suppress them — ESEF forbids it (`ESEF.2.4.1.transformableElementIncludedInHiddenSection`).

The mistake runs both ways. `ix:hidden` is *under*-used as often as it is abused: taxonomy-mandated entity metadata (registered name, registration number, legal form, document/report type, period-end date) and non-numeric classification facts that steer interpretation but are not a line in any statement (an entity-size class member, a reporting-framework choice, a consolidated-vs-company-only indicator) are real required facts with no row to sit on — they belong in `ix:hidden`, not omitted. See `references/conversion.md` §8 for the positive case.
