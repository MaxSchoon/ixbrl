# ESEF Mandatory Block-Tag List (RTS Annex II Table 2)

## Legal basis

The mandatory block-tagging regime for European listed-issuer annual
financial reports is established by **Commission Delegated Regulation
(EU) 2019/815** of 17 December 2018 — the Regulatory Technical
Standards on the European Single Electronic Format (the "RTS on
ESEF"), supplementing Directive 2004/109/EC (the Transparency
Directive). The Regulation requires that all issuers subject to the
Transparency Directive prepare their Annual Financial Reports (AFRs)
in XHTML, and that issuers preparing **IFRS consolidated financial
statements** mark up those statements using XBRL embedded as **Inline
XBRL** (iXBRL).

The architecture of the RTS distinguishes two tagging regimes:

- **Detailed (numeric) tagging** of the primary financial statements — Annex II Table 1 — applicable from financial years beginning on or after 1 January 2020.
- **Block (narrative) tagging** of the notes — Annex II Table 2 — applicable from financial years beginning on or after **1 January 2022**. Article 6 of the Regulation imposes the Table 2 obligation: issuers must mark up all disclosures made in the IFRS consolidated financial statements (or made by cross-reference therein to other parts of the AFR) that correspond to the elements listed in Table 2.

The Regulation has been amended several times to track updates to the
IFRS Taxonomy. The currently published consolidated versions on
EUR-Lex include `02019R0815-20210101`, `02019R0815-20230119`, and
`02019R0815-20250101`. ESMA's Reporting Manual notes that the 2025
ESEF taxonomy update incorporates the 2024 IFRS Taxonomy update and
that two separate entry points are being introduced ahead of the
mandatory IFRS 18 / IFRS 19 implementation effective 1 January 2027
(manual paragraphs 7–8). Mandatory Table 2 obligations are therefore
stable for FY 2022–FY 2026 reporting cycles, with prospective IFRS 18
changes ahead.

> **Honest gap note on the catalog.** When this reference was prepared,
> the consolidated EUR-Lex text of Regulation 2019/815 returned an
> asynchronous (HTTP 202) response that did not yield extractable
> Table 2 contents within the time budget, and the FCA Handbook mirror
> of Annex II Table 2 returned no extractable content via the
> available fetch tool. Accordingly, no QNames have been invented. The
> catalog section below lists only QNames literally verified in the
> fetched ESMA Reporting Manual figures plus the small additional set
> whose existence is unambiguously documented in the secondary sources
> successfully fetched (XBRL.org guidance article). **This is a
> deliberately partial-but-verified catalog** — preparers should
> consult the consolidated EUR-Lex text or the ESMA-published ESEF
> taxonomy package for the full ~250-element list.

## How block tagging works mechanically

The ESMA Reporting Manual glossary (ESMA32-60-254 Rev, 14 October
2025, p. 10) defines a block tag as: *"A single fact that contains the
content of an entire or a part of a section of a report. A block tag
may include text, numeric values, tables and other data. A block tag
is applicable to facts with datatype of dtr-types:textBlockItemType."*

In the iXBRL output:

- The element is declared in the IFRS Taxonomy as `xbrli:item` with type `dtr-types:textBlockItemType`.
- The disclosure is wrapped using `<ix:nonNumeric name="ifrs-full:DisclosureOf...Explanatory" contextRef="..." escape="true">…inner XHTML…</ix:nonNumeric>`.
- The `escape="true"` attribute instructs the iXBRL processor to preserve the inner XHTML markup as part of the fact's string value when extracting the target XBRL document.
- The same physical text in the rendered XHTML can be wrapped by **multiple** `ix:nonNumeric` tags of varying granularity (parent and child block tags can overlap). This is explicitly endorsed in Manual Guidance 1.9.1.
- When a single logical disclosure is split across multiple sections of the report, the iXBRL constructs `ix:continuation` and `ix:exclude` are used to assemble (or exclude) text fragments into a single fact value. This pattern is illustrated in Manual Figure 5 and governed by Guidance 2.5.5.

## Selection guidance (Reporting Manual §1.9)

Verified literally from ESMA32-60-254 Rev (14 October 2025), §1.9.1–1.9.3:

1. **Minimum requirement** — *"ESMA is of the opinion that issuers shall, as a minimum, mark up information contained in the IFRS consolidated financial statements (including headers/titles) with the elements of Annex II"* (§1.9.1).
2. **Multi-tagging at varying granularity** — *"In case of a disclosure corresponding to more than one element of different granularity (with narrower and wider elements), preparers should use each of them and multi tag the information to the extent that corresponds with the underlying accounting meaning of the information"* (§1.9.1). Figure 2 illustrates a parent `Disclosure of significant accounting policies [text block]` overlapping with narrower children `Disclosure of basis of preparation of financial statements [text block]` and `Disclosure of accounting judgements and estimates [text block]`.
3. **Annex II prevails over Annex VI** — Footnote 21 to §1.9.1 states that issuers may complement mark-up with Annex VI elements, *"Nevertheless, the use of these elements from Annex VI, even if with a closer accounting meaning, does not prevail over the use of the mandatory elements."*
4. **Granularity floor for tables** — *"The lowest level of granularity for block tagging the IFRS consolidated financial statements is individual tables contained within a single note. Therefore, issuers are not required to apply textBlockItemType elements from Annex II on selected rows or columns of such table"* (§1.9.2).
5. **No-disclosure, no-tag** — *"Whenever an issuer discloses information in an explanatory note or accounting policy that does not correspond to any of the elements in Annex II, such disclosure is not required to be block tagged. Consequently, there is also no obligation to create an extension element to block tag such notes"* (§1.9.3). Issuers are encouraged but not required to use Annex VI core elements or extension elements for such residual disclosures.
6. **Detailed tagging is permitted but does not displace block tagging** — Recital 10 of the RTS (cited in §1.9.3) preserves issuer discretion to apply higher granularity, but *"detailed tagging of the notes to the IFRS consolidated financial statements does not prevail over the requirement to block tag the notes."*
7. **Disclosures split across sections** — When the same logical disclosure (e.g., an accounting policy described in two notes) is physically split, issuers should use `ix:continuation` to assemble it into a single block-tag fact (§1.9.3 + Figure 5).

## The catalog — verified concepts grouped by topic

**Verification scope:** The QNames listed below are those literally
verified from primary or near-primary sources fetched when this
reference was prepared — principally the ESMA Reporting Manual
figures (Manual §1.9, Figures 2–5) and the XBRL.org guidance article.
Each is documented in the IFRS Foundation taxonomy at
`http://xbrl.ifrs.org/taxonomy/.../ifrs-full` with type
`dtr-types:textBlockItemType`. **This is a partial list.** The
complete Annex II Table 2 catalog contains roughly 250 IFRS-full
text-block elements covering every major IFRS standard (IAS 1, IAS 7,
IAS 12, IAS 16, IAS 19, IAS 24, IAS 36, IAS 38, IFRS 2, IFRS 3, IFRS
7, IFRS 8, IFRS 9, IFRS 13, IFRS 15, IFRS 16, IFRS 17, etc.). For the
authoritative full enumeration, fetch the consolidated text of
Regulation 2019/815 directly from EUR-Lex or load the ESMA-published
`esef_taxonomy.zip` package.

### Basis of preparation and accounting policies (verified in Manual §1.9)

- `ifrs-full:DisclosureOfNotesAndOtherExplanatoryInformationExplanatory` — top-level "Disclosure of notes and other explanatory information [text block]"
- `ifrs-full:DisclosureOfSignificantAccountingPoliciesExplanatory` — "Disclosure of significant accounting policies [text block]"
- `ifrs-full:DisclosureOfBasisOfPreparationOfFinancialStatementsExplanatory` — "Disclosure of basis of preparation of financial statements [text block]"
- `ifrs-full:DisclosureOfAccountingJudgementsAndEstimatesExplanatory` — "Disclosure of accounting judgements and estimates [text block]"
- `ifrs-full:DisclosureOfInitialApplicationOfStandardsOrInterpretationsExplanatory` — "Disclosure of initial application of standards or interpretations [text block]" (illustrated as a voluntary/Annex VI element in Figure 4)

### Income statement / finance items (verified in Manual §1.9, Figures 2–3, 5)

- `ifrs-full:DisclosureOfFinanceIncomeCostExplanatory` — "Disclosure of finance income (cost) [text block]"
- `ifrs-full:DisclosureOfFinanceIncomeExplanatory` — "Disclosure of finance income [text block]"
- `ifrs-full:DisclosureOfFinanceCostExplanatory` — "Disclosure of finance cost [text block]"

### Income taxes (verified — XBRL.org guidance)

- `ifrs-full:DisclosureOfIncomeTaxExplanatory` — covers IAS 12 disclosures including current/deferred tax reconciliation and tax receivables/payables tables.

### Other topical groups in Annex II Table 2 — coverage NOT verified literally in this run

The following topical groupings are documented as part of the
mandatory list in the secondary literature (XBRL.org guidance, ESMA
Manual structure, and the public IFRS Foundation taxonomy), but their
exact QNames were not literally extracted from a primary source when
this reference was prepared. Listed here by topic only — preparers
should validate exact local-names against the consolidated Regulation
2019/815 and the IFRS Taxonomy:

- **Revenue and customers** (IFRS 15) — disaggregation of revenue, performance obligations, contract balances, transaction price allocations.
- **Property, plant and equipment** (IAS 16) — PPE reconciliation, impairment, idle assets.
- **Intangible assets and goodwill** (IAS 38, IAS 36) — intangible assets reconciliation, goodwill, impairment testing assumptions.
- **Financial instruments** (IFRS 7, IFRS 9) — credit risk, liquidity risk, market risk (currency / interest-rate / other price), hedge accounting, fair value hierarchy of financial instruments, offsetting.
- **Leases** (IFRS 16) — lessee disclosures, lessor disclosures, right-of-use assets reconciliation.
- **Employee benefits** (IAS 19) — defined benefit plans (actuarial assumptions, sensitivity, plan asset categories), defined contribution plans, termination benefits, share-based payment (IFRS 2).
- **Provisions and contingencies** (IAS 37) — provisions reconciliation, contingent liabilities, contingent assets.
- **Equity and earnings per share** (IAS 33) — share capital, reserves, dividends, basic and diluted EPS reconciliations.
- **Business combinations** (IFRS 3) — consideration transferred, fair value of identifiable assets and liabilities, goodwill, NCI.
- **Consolidated and separate financial statements** (IFRS 10, IFRS 11, IFRS 12, IAS 27, IAS 28) — interests in subsidiaries, joint arrangements, associates, structured entities.
- **Fair value measurement** (IFRS 13) — Level 1/2/3 hierarchy, valuation techniques, unobservable inputs.
- **Government grants** (IAS 20), **Related parties** (IAS 24), **Events after the reporting period** (IAS 10).
- **Segment reporting** (IFRS 8) — `DisclosureOfOperatingSegmentsExplanatory` and related geographic / major customer disclosures.
- **Insurance contracts** (IFRS 17) — extensive set added in 2023+ amendments.

The naming pattern is uniform: each concept is
`ifrs-full:DisclosureOf<Topic>Explanatory` (or, for accounting
policies, `ifrs-full:DescriptionOfAccountingPolicyFor<Topic>Explanatory`),
all typed as `dtr-types:textBlockItemType`.

## Common pitfalls

1. **Tagging at paragraph level instead of block level.** Multi-tagging of overlapping wider/narrower blocks is correct (Figure 2); fragmenting a coherent block into per-paragraph tags is excess tagging and does not satisfy the Annex II obligation at the wider level.
2. **Using a more general tag when a more specific Annex II tag is available.** §1.9.1 requires using each applicable element of different granularity — substituting a wider parent does not discharge the obligation to also use the narrower child where it applies.
3. **Substituting an Annex VI element for a closer-meaning Annex II element.** Footnote 21 is explicit: Annex VI does not prevail over Annex II. If both apply, the Annex II element is mandatory and the Annex VI element is supplementary.
4. **Forgetting `escape="true"`.** Without the escape attribute, inline markup in the disclosure (tables, lists, emphasis) is lost from the target XBRL fact value.
5. **Tagging selected rows/columns inside a note table.** §1.9.2 states the granularity floor is the entire individual table, not row- or column-level fragments.
6. **Creating an "umbrella" single block tag covering all notes.** §1.9.3's encouragement of detailed tagging implicitly disfavours a single sweep tag — it does not satisfy the requirement to apply each Annex II element where its specific accounting meaning is present.
7. **Creating extension block tags for residual disclosures.** §1.9.3 explicitly does not require this; encouraged use of Annex VI core elements is preferred.
8. **Failing to concatenate split disclosures with `ix:continuation`.** Where the same logical disclosure is physically split across notes, two separate facts will produce inconsistent duplicates (Guidance 2.2.4) and must instead be assembled into one fact (Figure 5, Guidance 2.5.5).
9. **Inconsistent block tagging across periods.** §1.9.3 requires consistency *"across reporting periods to the maximum possible extent"* when including additional voluntary tags.

## Recommended workflow for enumerating the full Table 2 list

When preparers need the definitive ~250-element catalog, the
authoritative path is:

1. Fetch the latest consolidated text of Regulation 2019/815 from EUR-Lex (e.g., `02019R0815-20250101`) and extract the Annex II Table 2 element list.
2. Alternatively, load the ESMA-published `esef_taxonomy.zip` and enumerate elements satisfying:
   - `xbrli:item` substitution group,
   - `dtr-types:textBlockItemType` (or `dtr:textBlockItemType`) type,
   - Member of the ESEF Annex II Table 2 entry-point.
3. Cross-check against the IFRS Taxonomy Illustrated package from the IFRS Foundation for the human-readable concept labels.

Both paths yield the same canonical list; both are mandatory inputs to
any preparation tool that purports to be ESEF-conformant.

## Sources

- Commission Delegated Regulation (EU) 2019/815 of 17 December 2018 — RTS on ESEF, Article 6 and Annex II Table 2. Consolidated versions: `02019R0815-20210101`, `02019R0815-20230119`, `02019R0815-20250101`. https://eur-lex.europa.eu/eli/reg_del/2019/815/oj/eng and https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02019R0815-20250101
- ESMA, *ESEF Reporting Manual — Preparation of Annual Financial Reports in ESEF format (Update October 2025)*, document reference **ESMA32-60-254 Rev**, dated 14 October 2025. Sections verified literally: Glossary (block tag definition, p. 10), §1.9.1 Marking up notes and accounting policies (p. 23), §1.9.2 Granularity of block tagging (p. 24), §1.9.3 Other considerations (p. 25–26), §2.2.4 Facts duplication (p. 30). https://www.esma.europa.eu/sites/default/files/library/esma32-60-254_esef_reporting_manual.pdf
- Directive 2004/109/EC (Transparency Directive), Article 4 and Article 20, as amended by Directive 2013/50/EU.
- XBRL International / XBRL.org, *Guidance on Block Tagging and Other ESEF Reporting Manual Updates from ESMA*. https://www.xbrl.org/guidance-on-block-tagging-and-other-esef-reporting-manual-updates-from-esma/
- IFRS Foundation, IFRS Taxonomy (namespace `http://xbrl.ifrs.org/taxonomy/.../ifrs-full`). https://www.ifrs.org/issued-standards/ifrs-taxonomy/

> **Verification gap acknowledged:** The full ~250-element list of
> Annex II Table 2 QNames was not literally extracted within the time
> budget when this reference was prepared (EUR-Lex consolidated text
> returned an asynchronous response; the FCA Handbook mirror returned
> no extractable text via the fetch tool; the XBRL France mapping PDF
> was binary-only). The catalog section above is therefore
> deliberately partial-verified rather than invented-comprehensive.
> Preparers requiring a definitive enumeration should fetch the
> consolidated EUR-Lex text directly or load the ESMA-published ESEF
> taxonomy package and enumerate elements with `xbrli:periodType` and
> `dtr-types:textBlockItemType` substitution group.
