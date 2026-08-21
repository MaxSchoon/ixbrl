---
reference_id: sec-edgar
jurisdiction: US
restructured_on: 2026-08-15
profiles:
  - id: operating-company
    section: profile-operating-company
  - id: investment-company
    section: profile-investment-company
---

# SEC EDGAR iXBRL Reference

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*

**Load this when:** the receiver is the SEC: an EDGAR Inline XBRL submission, an EDGAR Filer Manual chapter, a DEI / SRT / US-GAAP question, or an `EFM.6.05.*` code.

**Do not load this when:** the filing is European (`references/esef.md` or the file under `references/jurisdictions/`); EDGAR neither anchors nor uses the ESEF package shape.

**Contents**

- [Start here: choose a filing profile](#start-here-choose-a-filing-profile)
- [Vintage and applicability](#vintage-and-applicability)
- [Profile: Operating companies (periodic and registration filings)](#profile-operating-company)
- [Profile: Registered investment companies (funds)](#profile-investment-company)
- [Jurisdiction-specific invariants](#jurisdiction-specific-invariants)
- [Validation](#validation)
- [Review workflow](#review-workflow)
- [Authorities and governance](#authorities-and-governance)
- [Sources](#sources)

Reference for Inline XBRL submissions to the U.S. Securities and Exchange Commission. Verify the operative version of every cited rule against the EDGAR Filer Manual at filing date.

## Start here: choose a filing profile

| Situation | Profile | Section |
|---|---|---|
| You file 10-K, 10-Q, 8-K, 20-F, 40-F, Securities Act registration statements, or proxy and information statements (including Pay-Versus-Performance) as an operating company | Operating companies | [Profile: Operating companies](#profile-operating-company) |
| You file shareholder reports or risk/return summaries for a registered fund on Form N-1A or Form N-CSR | Registered investment companies | [Profile: Registered investment companies](#profile-investment-company) |

## Vintage and applicability

The **EDGAR Filer Manual, Volume II: EDGAR Filing** is authoritative,
and filers must comply with whichever version is effective at
**submission** date, not at period end, and not the one current when a
report was drafted. The manual is reissued on EDGAR release cadence, so
this is a live check, never a remembered fact.

**Version 77**, deployed **16 March 2026** with EDGAR Release 26.1
(adopting release 33-11411), is current as of 2026-08-15. Confirm the
operative version at <https://www.sec.gov/submit-filings/edgar-filer-manual>
before citing a chapter or section number: chapter 6 ("Interactive
Data") is the Inline XBRL chapter, and its numbering moves between
versions. Version 69 (March 2024) removed the Inline XBRL technical
detail from chapter 6 into the EDGAR XBRL Guide, and the Release 26.3
draft, deploying 14 September 2026, removes what remains.

### DTS and vintages

Which GRT vintage to load, where it lives, and when EDGAR accepts it.
Vocabulary and column order are fixed in `references/dts.md`
§ Vocabulary. Verified 2026-08-21; every URL marked 200 was fetched that
day (`sec.gov` answers only a descriptive `User-Agent`; `xbrl.fasb.org`
serves every path below its root). The architecture: `us-gaap` core plus
`srt` plus `dei` plus the SEC code lists; there are **no per-industry
entry points** in any vintage back to 2016, the industry dimension lives in
the statement modules (`stm/…`); `entire/us-gaap-entryPoint-std-YYYY.xsd`
omits documentation labels, references and deprecated elements, which
`…-all-YYYY.xsd` carries. The GRT uses **Calculations 1.1**
(`https://xbrl.org/2023/arcrole/summation-item`) from the 2024 vintage;
2022 and 2023 used the XBRL 2.1 arcrole.

| Release | Entry point(s) | Package | Valid time | Accepted at deposit | Status | Source |
|---|---|---|---|---|---|---|
| **2026** GRT + SRT (FASB 15 Dec 2025) | `https://xbrl.fasb.org/us-gaap/2026/elts/us-gaap-2026.xsd`; `https://xbrl.fasb.org/srt/2026/elts/srt-2026.xsd`; entry points under `https://xbrl.fasb.org/us-gaap/2026/entire/` | `us-gaap-2026.zip`, `srt-2026.zip` in the same directories | SEC: "for the earliest reporting period that ends on or after **March 16, 2026**, but not for reporting periods that end before" | EDGAR Release 26.1, **16 Mar 2026**, onward; removal not announced | current | SEC 2026 taxonomies announcement; `https://www.sec.gov/files/edgartaxonomies.xml` (v77; the `/info/edgar/` path redirects here) |
| **2025** GRT + SRT (FASB 16 Dec 2024) | `…/us-gaap/2025/elts/us-gaap-2025.xsd`; `…/srt/2025/elts/srt-2025.xsd` (200) | `us-gaap-2025.zip`, `srt-2025.zip` | periods ending on or after **17 Mar 2025** | EDGAR Release 25.1, **17 Mar 2025**, onward; removal not announced | accepted | SEC 2025 announcement |
| **2024** GRT + SRT (FASB 14 Dec 2023) | `…/us-gaap/2024/elts/us-gaap-2024.xsd`; `…/srt/2024/elts/srt-2024.xsd` (200) | `us-gaap-2024.zip`, `srt-2024.zip` | periods ending on or after **18 Mar 2024** | EDGAR Release 24.1, **18 Mar 2024**; removal was due at Release 26.2 (June 2026), which the SEC **cancelled on 1 Jun 2026**; now planned for Release 26.3, **14 Sep 2026**, "may approve or disapprove" | **still accepted** on 2026-08-21; three vintages live at once | SEC Release 26.3 preview (14 Aug 2026); cancellation notice |
| 2023 GRT + SRT (FASB 16 Dec 2022) | `…/us-gaap/2023/elts/us-gaap-2023.xsd` (200, still fetchable) | | periods ending on or after 20 Mar 2023 | EDGAR 23.1 (20 Mar 2023) to Release 25.2, **16 Jun 2025** | removed | SEC 25.2 announcement |
| 2022 GRT + SRT (FASB 17 Dec 2021) | `…/us-gaap/2022/elts/us-gaap-2022.xsd` (200, still fetchable) | | periods ending on or after 21 Mar 2022 | EDGAR 22.1 (21 Mar 2022) to Release 24.2, **1 Jul 2024** | removed | SEC 24.2 announcement |
| DEI, ECD, CYD, SBS, SRO, COUNTRY, CURRENCY, EXCH, NAICS, SIC, SNJ, STPR | `https://xbrl.sec.gov/<name>/2026/<name>-2026.xsd` (2026 core) | | same year as the GRT in the submission | 2024, 2025, 2026 accepted (`edgartaxonomies.xml` v77) | current | `edgartaxonomies.xml` |
| IFRS (for FPIs) | `https://xbrl.ifrs.org/taxonomy/2025-03-27/full_ifrs/full_ifrs-cor_2025-03-27.xsd` | | the standing exception to version synchronisation | 2021, 2022, 2024, 2025 accepted; no IFRS 2026 row, because the IFRS Foundation issued no 2026 taxonomy and the 2025 taxonomy remains current for 2026 reporting | current | `edgartaxonomies.xml` |

The rule, from the EDGAR XBRL Guide (August 2026) § 1: taxonomies are
"updated at least annually … and removed from use after two years". In
practice a vintage is added at the `NN.1` release in March and removed at
the `NN.2` release in June or July two years later, a window of about two
years and three months, stretched this year by the cancelled 26.2. **A
fetchable URL is not an accepted vintage**: 2022 and 2023 still resolve
and are refused. The machine-readable authority is
`https://www.sec.gov/files/edgartaxonomies.xml`; the human pages no
longer carry a table.

### Recent rule updates (last ~24 months)

- **Pay-Versus-Performance**: Release **34-95607**, adopted 25 August 2022, effective 11 October 2022. Compliance for proxy / information statements with fiscal years ending on or after **16 December 2022**. Each value in the PVP table is separately tagged; footnote, relationship, and Tabular List disclosures are block-text tagged. Smaller reporting companies provide Inline XBRL beginning the third PVP filing. Tagging uses the 2022Q4 ECD taxonomy.
- **Cybersecurity Risk Management, Strategy, Governance, and Incident Disclosure**: Release **33-11216 / 34-97989**, adopted 26 July 2023. New Form 8-K Item 1.05 (and 6-K equivalent) for material cybersecurity incidents, due four business days after materiality determination. Annual-report disclosures sit at **Reg S-K Item 106 on Form 10-K** and at **Item 16K on Form 20-F**, not Item 106 on both. The Inline XBRL tagging obligation runs **one year after** each disclosure's own compliance date, so the two dates differ and must not be conflated: **Form 10-K Item 106 / Form 20-F Item 16K** are tagged for **fiscal years ending on or after 15 December 2024**, while **Form 8-K Item 1.05 / 6-K** (material-incident disclosures) are tagged from **18 December 2024**. Both apply to **all registrants subject to these rules, including SRCs**. The SRC extension applied to the incident *disclosure*, not to tagging. The rules do **not** reach every filer: eligible Form 40-F filers, asset-backed issuers, and registered investment companies are outside them.
- **Tailored Shareholder Reports**: Release **33-11125**, adopted 26 October 2022. Open-end funds (Form N-1A) must transmit streamlined annual / semi-annual shareholder reports in Form N-CSR using Inline XBRL for transmittals on or after **24 July 2024**.
- **EDGAR 25.1 and 26.1 taxonomy updates**: annual taxonomy refreshes became loadable in EDGAR through 2025 and 2026 (US-GAAP and SRT 2025 at Release 25.1; US-GAAP, SRT and DEI 2026 at Release 26.1; a submission uses one year's set throughout for these synchronised families, while IFRS remains the standing exception noted above). Filers transitioning concept usage should re-map extensions onto the new base elements where one is available and appropriate; anchoring arcs remain optional (see *Custom (extension) elements*).

Note: Release **33-11038** is the *proposed* cybersecurity rule
(March 2022). The final cybersecurity rule is **33-11216**. The
"33-11038" reference often seen in vendor documentation is incorrect
when used to mean Tailored Shareholder Reports or Cybersecurity; the
correct final-rule numbers are 33-11125 and 33-11216 respectively.

<a id="profile-operating-company"></a>

## Profile: Operating companies (periodic and registration filings)

The mandate originates in **Release No. 33-10514, "Inline XBRL Filing of
Tagged Data"**, adopted 28 June 2018, which amended Regulation S-T
Rule 405 and the EDGAR Filer Manual.

### Phase-in by filer status

**Operating-company phase-in** (10-K, 10-Q, transition reports, 8-Ks
containing revised financial statements, non-IPO Securities Act
registration statements, prospectuses, 20-F/40-F):

| Filer status / basis | Compliance date (fiscal periods ending on or after) |
|---|---|
| Large accelerated filers (U.S. GAAP) | 15 June 2019 |
| Accelerated filers (U.S. GAAP) | 15 June 2020 |
| All others (smaller reporting, non-accelerated, FPIs using IFRS or U.S. GAAP) | 15 June 2021 |

### Forms in scope

**Forms within scope:** 10-K, 10-Q, 8-K with revised financials, 20-F,
40-F, S-1/S-3/S-4/S-11 and other Securities Act registration statements,
proxy and information statements containing Pay-Versus-Performance
(Reg S-K Item 402(v)) disclosures, and Form 6-K when it contains
material cybersecurity-incident disclosures.

<a id="profile-investment-company"></a>

## Profile: Registered investment companies (funds)

**Funds:** Open-end management investment companies on Form N-1A must
file tailored shareholder reports (Form N-CSR) in Inline XBRL for
transmittals on or after **24 July 2024** (Release No. 33-11125).
Risk/return summaries continue to be filed in Inline XBRL.

## Jurisdiction-specific invariants

### Required taxonomies

Canonical list: https://www.sec.gov/info/edgar/edgartaxonomies

A submission package combines exactly one US-GAAP (or IFRS for FPIs)
version plus DEI plus SRT plus any utility taxonomies it dimensionally
references.

- **US-GAAP Financial Reporting Taxonomy** (FASB): core balance-sheet, income-statement, cash-flow, footnote elements. 2025 version mirrors FASB release of 16 December 2024.
- **DEI (Document and Entity Information)**: entity identity, document type, period, amendment flag, filer category. The 2026 DEI taxonomy adds `NYSETX` for NYSE Texas to the exchange data type.
- **SRT (SEC Reporting Taxonomy)**: schedules, ranges, disposal groups; cross-cutting across US GAAP and IFRS filers.
- **ECD (Executive Compensation Disclosure)**: Pay-Versus-Performance and clawback disclosures (Reg S-K Item 402(v) and 10D-1). 2022Q4 ECD is the operative PVP version.
- **COUNTRY, CURRENCY, EXCH, STPR, NAICS, SIC, SNJ**: utility code-list taxonomies.
- **RR, OEF, CEF, VIP, FND**: fund taxonomies.
- **RXP**: Resource Extraction Payments.

### Custom (extension) elements

Extensions are declared in the filer's company schema
(`<ticker>-<date>.xsd`) when no base concept fits. Requirements:

- Declared in the filer's namespace, with a stable PascalCase name (no spaces).
- Standard Label and (where applicable) Terse, Verbose, Negated, or Period-Start/End labels in a label linkbase.
- Wired into a presentation linkbase under the appropriate parent and given a calculation-linkbase relationship if the value participates in an arithmetic roll-up.
- **Not anchored.** Neither the EDGAR XBRL Guide (August 2026) nor EFM Volume II chapter 6 requires an extension to be anchored; the words "anchor" and "wider" do not occur in either. The ESMA `wider-narrower` arcrole is on EDGAR's list of supported base files, so an anchoring arc is *permitted*, never required. An earlier edition of this file stated the opposite.

The EFM and EDGAR XBRL Guide explicitly require filers to use a base
element when one is "available and appropriate" before creating an
extension. The SEC's "Sample Letter to Companies Regarding Their XBRL
Disclosures" calls out misuse of extensions.

### DEI and the entity context

Every iXBRL instance must tag cover-page DEI facts. Mandatory concepts
(EFM 6.5.20 / 6.5.21 / 6.5.40):

- `dei:DocumentType`
- `dei:DocumentPeriodEndDate`
- `dei:AmendmentFlag` (and `dei:AmendmentDescription` if true)
- `dei:EntityRegistrantName`
- `dei:EntityCentralIndexKey` (10-digit CIK in the *required context*)
- `dei:CurrentFiscalYearEndDate`
- `dei:EntityFilerCategory`
- `dei:EntitySmallBusiness`, `dei:EntityEmergingGrowthCompany`
- `dei:EntityCommonStockSharesOutstanding` (10-K / 10-Q)
- Address: `dei:EntityAddressAddressLine1`, `…CityOrTown`, `…StateOrProvince`, `…PostalZipCode`, `dei:CityAreaCode`, `dei:LocalPhoneNumber`
- Trading-symbol set: `dei:TradingSymbol`, `dei:Security12bTitle`, `dei:SecurityExchangeName`

Identifier facts with no display equivalent (CIK, AmendmentFlag) are
placed in `<ix:hidden>`. EFM 6.5.14 requires that any `ix:hidden` fact
whose value also appears as visible text be referenced via the
`-sec-ix-hidden` CSS style on the visible element. A duplicate fact must
have at least one occurrence outside `ix:hidden`.

### Decimals, units, and signs

EDGAR XBRL Guide sections 6.6.4, 8.6 and 9.5. EFM Volume II version 69
(March 2024) moved this detail out of chapter 6, so the section numbers
6.5.17 and 6.5.37 are EFM v68 numbering, which the Guide keeps in its
"EFM v68 Ref" column and EDGAR keeps in its error codes:

- Every numeric `ix:nonFraction` carries a `decimals` attribute. `precision` is
  not allowed (Guide section 8.6, `EFM.6.05.17`).
- The literal `INF` is permitted for `decimals`. Guide section 6.6.4 gives `INF`
  as the correct value for an exactly reported monetary amount, percentage or
  basis-point figure; a rounded amount takes a finite integer instead (`-3`
  thousands, `-6` millions, `0` whole units, `2` pennies).
- A finite `decimals` must not zero out a non-zero digit of the reported value
  (`EFM.6.05.37`). Guide section 9.5: "If the decimals attribute of a numeric
  fact is not INF, then the value is interpreted as if certain digits were zero.
  An instance must not contain usage that cause non-zero digits to be interpreted
  as zero." So `-2345.67` may carry `decimals="2"` or `"INF"`, but `"0"`, `"-2"`,
  `"-3"` and `"-6"` are each an error.
- The test is **asymmetric**, and this is the part most often got wrong: a
  `decimals` finer than the value's own accuracy is fine, because zeroing digits
  that are already zero loses nothing. The guide's own example is that 1,000,000
  "may have a decimals attribute with any value greater than -6". Do not flag
  `INF` merely because a figure ends in zeros.
- Monetary values use ISO 4217 currency codes as the unit (`iso4217:USD`).
- Per-share values use a divide unit such as `iso4217:USD / xbrli:shares`.
- A calculation linkbase is required for facts that roll up arithmetically. Calculation inconsistencies are reported as warnings.
- Negated/credit balances: tag the *as-reported* numeric value; never invert the sign manually. Use a negated label role for presentation only. The SEC's June 2024 Sample Letter specifically flagged misuse of negative values on concepts whose balance is credit/debit.

## Validation

### Submission, test filing, and the validator stack

- **Test submissions**: filers may submit non-public test filings via EDGAR Online Forms / EDGAR Filer System to exercise the EDGAR Renderer/Previewer before live filing.
- **Public Test Suite**: the SEC's **Interactive Data Public Test Suite** (https://www.sec.gov/structureddata/osdinteractivedatatestsuite), a categorized corpus of small XBRL instances exercising each validation check; used to certify preparation software.
- **Validator stack**: EDGAR uses **Arelle** (https://arelle.org) with the EDGAR plugin (the SEC's EDGAR Renderer is itself an Arelle distribution). The plugin combines the `EFM` validation profile with `FRTA` (Financial Reporting Taxonomy Architecture) checks. EDGAR plugin source on GitHub.
- **Financial Report Viewer**: renders embedded facts at https://www.sec.gov/cgi-bin/viewer and on EDGAR full-text search.
- **Dissemination**: accepted submissions are publicly disseminated within minutes via EDGAR full-text search and the bulk Public Dissemination Service.

### Common EFM error and warning codes

Codes verbatim, with the EFM v68 section each one cites. The current
chapter 6 no longer contains these sections; the EDGAR XBRL Guide
reproduces the numbers in its "EFM v68 Ref" column:

| Code | Meaning | EFM v68 § |
|---|---|---|
| EFM.6.05.01 | CIK / identifier convention violation | 6.5.1 |
| EFM.6.05.11 | Duplicate or equivalent units must be deduplicated | 6.5.11 |
| EFM.6.05.14 | Hidden cover-page fact not referenced via `-sec-ix-hidden` | 6.5.14 |
| EFM.6.05.16 | `href`/`src` attribute scheme restrictions on embedded content | 6.5.16 |
| EFM.6.05.17 | Numeric fact carries `precision` instead of `decimals` | 6.5.17 |
| EFM.6.05.37 | A finite `decimals` truncates non-zero digits of the value | 6.5.37 |
| EFM.6.05.20 | Required DEI element missing (e.g., `dei:AmendmentFlag`) | 6.5.20 |
| EFM.6.05.21 | Required DEI per document type (e.g., `EntityRegistrantName`) | 6.5.21 |
| EFM.6.05.34 | Inline XBRL submission / well-formedness violation | 6.5.34 |
| EFM.6.05.40 | DEI elements added in newer taxonomies | 6.5.40 |
| EFM.6.05.42 | Deprecated concept used (warning) | 6.5.42 |
| EFM.6.05.48 | Address element tagging via DEI address concepts | 6.5.48 |

Full lists:

- https://www.sec.gov/data-research/xbrl-validation-rendering/edgar-xbrl-validation-errors
- https://www.sec.gov/data-research/xbrl-validation-rendering/edgar-xbrl-validation-warnings

## Review workflow

### Auditor assurance, certifications, liability, and consistency

SEC EDGAR does not have a single NBA Alert 50-style auditor guidance
document for Inline XBRL. The relevant authority is distributed across
Regulation S-T Rule 405, SEC adopting releases, the EDGAR Filer Manual /
EDGAR XBRL Guide, staff interpretations, and PCAOB standards.

The practical rule: Inline XBRL changes the filing format, not the
default audit scope. Release 33-10514 reaffirmed that the move from
exhibit XBRL to Inline XBRL did **not** change the SEC's existing
positions on officer certifications or auditor assurance.

- **No mandatory auditor assurance.** Auditors are not required to
  apply PCAOB AS 2710, AS 4101, or AS 4105 to the Interactive Data File.
  Filers are not required to obtain assurance or involve auditors,
  consultants, or other third parties in preparing it.
- **Audit-report scope.** The financial statement audit report does not
  by itself extend to XBRL tagging. The SEC declined to require audit
  report changes or auditor-responsibility legends for Inline XBRL,
  though issuers may disclose the degree or absence of auditor
  involvement, for example in a financial-statement footnote.
- **Voluntary assurance and consent.** Issuers may voluntarily obtain
  third-party assurance on XBRL tagging. If a filing refers to that
  assurance or names the auditor as an expert, evaluate the Securities
  Act consent implications separately; PCAOB AS 4101 remains relevant
  in that expert/consent context.
- **Officer certifications.** Exchange Act Rules 13a-14(f) and
  15d-14(f) exclude Interactive Data Files from CEO/CFO certification
  requirements. That exclusion does not remove interactive data from
  disclosure controls and procedures: SEC staff says filers still must
  consider controls over interactive data when evaluating disclosure
  controls under Rules 13a-15 / 15d-15 and Regulation S-K Item 307.
- **Liability.** Do not rely on the old phase-in safe-harbor framing:
  temporary modified liability under Regulation S-T Rule 406T expired
  on 31 October 2014, and Release 33-10514 noted that expiration. Treat
  accepted Inline XBRL as part of the live SEC filing risk surface.
- **Consistency with the human-readable filing.** Rule 405 requires
  each data element in the Interactive Data File to reflect the same
  information in the corresponding data in the Related Official Filing.
  Do not change, delete, or summarize data elements merely because the
  tag layer is machine-readable; choose the appropriate standard tag
  unless an extension is required. SEC staff guidance clarifies that
  identical visual appearance is not the test; content consistency is.

## Authorities and governance

Most-cited iXBRL rules, in EFM v68 numbering. Version 69 (March 2024)
moved this material to the EDGAR XBRL Guide, and the operative chapter 6
now runs only to 6.6; the Guide and the EDGAR error codes still cite
these numbers:

- **EFM 6.4**: Submission of Interactive Data (which forms, attachment names, EX-101 vs. embedded iXBRL).
- **EFM 6.5**: *Syntax of Instances*. Master section for Inline XBRL syntax checks.
- **EFM 6.5.14**: Cover-page facts in `ix:hidden` must be referenced elsewhere via `-sec-ix-hidden` style.
- **EFM 6.5.16**: Scheme restrictions on `href` and `src` attributes.
- **EFM 6.5.17**: Numeric facts must carry `decimals`, not `precision`.
- **EFM 6.5.37**: A non-nil numeric fact value must not be truncated by its
  `decimals` attribute. There is no separate rule prohibiting `INF`; guidance on
  choosing `decimals` is Guide section 6.6.4, formerly EFM v68 section 6.6.32.
- **EFM 6.5.20 / 6.5.21**: Required DEI facts present for the document type.
- **EFM 6.5.34**: Inline XBRL submission-level validation (well-formedness of inline document and XHTML host).
- **EFM 6.5.40**: DEI completeness for the relevant taxonomy version (`EntitySmallBusiness`, `EntityEmergingGrowthCompany`, etc.).
- **EFM 6.5.42**: Use of deprecated concepts triggers a warning.
- **EFM 6.5.48**: Address-component DEI elements used to tag the registrant address block.
- **EFM 6.6.x**: Syntax of Inline Documents (`ix:nonNumeric`, `ix:nonFraction`, `ix:hidden`, `ix:references`, `ix:relationship`, transformation registries, XHTML wrapper).
- **EFM 6.11.x / 6.12.x**: Custom (extension) taxonomy structure: schema, presentation, calculation, definition, label linkbases.

Volume II PDF: https://www.sec.gov/files/edgar/filermanual/efmvol2.pdf
Chapter 6 split: https://www.sec.gov/files/edgar/filermanual/efmvol2-c6.pdf
EDGAR XBRL Guide (SEC staff; carries the Inline XBRL technical detail
removed from chapter 6): https://www.sec.gov/files/edgar/filer-information/specifications/xbrl-guide.pdf

## Sources

- **SEC, *EDGAR Filer Manual***: the version index. Volume II Version 77
  deployed 16 March 2026 (EDGAR Release 26.1, adopting release 33-11411);
  always check this page for the version effective at submission date.
  <https://www.sec.gov/submit-filings/edgar-filer-manual>.

- **SEC, *Cybersecurity Risk Management … Small Entity Compliance Guide***:
  establishes the two distinct Inline XBRL tagging dates: Form 10-K / 20-F for
  fiscal years ending on or after 15 December 2024, Form 8-K / 6-K from
  18 December 2024, both for all registrants including SRCs.
  <https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/cybersecurity-risk-management-strategy-governance-incident-disclosure>.

- https://www.sec.gov/files/rules/final/2018/33-10514.pdf
- https://www.sec.gov/newsroom/press-releases/2018-117
- https://www.sec.gov/rules-regulations/2018/06/inline-xbrl-filing-tagged-data
- https://www.sec.gov/data-research/structured-data/inline-xbrl
- https://www.sec.gov/newsroom/whats-new/osd-announcement-061121-inline-xbrl-be-required
- https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/operating-company-inline-xbrl-filing-tagged-data
- https://www.sec.gov/files/rules/final/2009/33-9002fr.pdf
- https://www.sec.gov/files/edgar/filermanual/efmvol2.pdf
- https://www.sec.gov/files/edgar/filermanual/efmvol2-c6.pdf
- https://www.sec.gov/submit-filings/edgar-filer-manual
- https://www.sec.gov/files/edgar/filer-information/specifications/xbrl-guide.pdf
- https://www.sec.gov/info/edgar/edgartaxonomies
- https://www.sec.gov/newsroom/whats-new/2603-2026-xbrl-taxonomies-update
- https://www.sec.gov/newsroom/whats-new/2506-edgar-252-release-xbrl-taxonomies-update
- https://www.sec.gov/newsroom/whats-new/2503-2025-xbrl-taxonomies-update
- https://xbrl.sec.gov/ecd/2022q4/ecd-taxonomy-guide-2022-12-19.pdf
- https://www.sec.gov/structureddata/FAQs
- https://www.sec.gov/rules-regulations/staff-guidance/corporation-finance-interpretations-cfis/interactive-data
- https://www.sec.gov/data-research/xbrl-validation-rendering/edgar-xbrl-validation-errors
- https://www.sec.gov/data-research/xbrl-validation-rendering/edgar-xbrl-validation-warnings
- https://www.sec.gov/structureddata/osdinteractivedatatestsuite
- https://www.sec.gov/rules-regulations/staff-guidance/disclosure-guidance/sample-letter-companies-regarding-their-xbrl
- https://pcaobus.org/oversight/standards/auditing-standards/details/AS2710
- https://pcaobus.org/oversight/standards/auditing-standards/details/AS4101
- https://pcaobus.org/oversight/standards/auditing-standards/details/AS4105
- https://www.sec.gov/files/rules/final/2022/34-95607.pdf
- https://www.sec.gov/files/rules/final/2023/33-11216.pdf
- https://www.sec.gov/files/rules/final/2022/33-11125.pdf
