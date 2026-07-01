# SEC EDGAR iXBRL Reference

Reference for Inline XBRL submissions to the U.S. Securities and Exchange Commission. Verify the operative version of every cited rule against the EDGAR Filer Manual at filing date.

## 1. Who must file in iXBRL

The mandate originates in **Release No. 33-10514, "Inline XBRL Filing of
Tagged Data"**, adopted 28 June 2018, which amended Regulation S-T
Rule 405 and the EDGAR Filer Manual.

**Operating-company phase-in** (10-K, 10-Q, transition reports, 8-Ks
containing revised financial statements, non-IPO Securities Act
registration statements, prospectuses, 20-F/40-F):

| Filer status / basis | Compliance date (fiscal periods ending on or after) |
|---|---|
| Large accelerated filers (U.S. GAAP) | 15 June 2019 |
| Accelerated filers (U.S. GAAP) | 15 June 2020 |
| All others (smaller reporting, non-accelerated, FPIs using IFRS or U.S. GAAP) | 15 June 2021 |

**Forms within scope:** 10-K, 10-Q, 8-K with revised financials, 20-F,
40-F, S-1/S-3/S-4/S-11 and other Securities Act registration statements,
proxy and information statements containing Pay-Versus-Performance
(Reg S-K Item 402(v)) disclosures, and Form 6-K when it contains
material cybersecurity-incident disclosures.

**Funds:** Open-end management investment companies on Form N-1A must
file tailored shareholder reports (Form N-CSR) in Inline XBRL for
transmittals on or after **24 July 2024** (Release No. 33-11125).
Risk/return summaries continue to be filed in Inline XBRL.

## 2. EDGAR Filer Manual (EFM)

The **EDGAR Filer Manual, Volume II: EDGAR Filing** is authoritative.
Filers must comply with whatever version is effective at submission
date. As of writing, chapter 6 ("Interactive Data") is reissued
effective **15 September 2025**.

Most-cited iXBRL rules:

- **EFM 6.4** — Submission of Interactive Data (which forms, attachment names, EX-101 vs. embedded iXBRL).
- **EFM 6.5** — *Syntax of Instances*. Master section for Inline XBRL syntax checks.
- **EFM 6.5.14** — Cover-page facts in `ix:hidden` must be referenced elsewhere via `-sec-ix-hidden` style.
- **EFM 6.5.16** — Numeric facts must carry `decimals` (not `precision`); `INF` is forbidden.
- **EFM 6.5.20 / 6.5.21** — Required DEI facts present for the document type.
- **EFM 6.5.34** — Inline XBRL submission-level validation (well-formedness of inline document and XHTML host).
- **EFM 6.5.40** — DEI completeness for the relevant taxonomy version (`EntitySmallBusiness`, `EntityEmergingGrowthCompany`, etc.).
- **EFM 6.5.42** — Use of deprecated concepts triggers a warning.
- **EFM 6.5.48** — Address-component DEI elements used to tag the registrant address block.
- **EFM 6.6.x** — Syntax of Inline Documents (`ix:nonNumeric`, `ix:nonFraction`, `ix:hidden`, `ix:references`, `ix:relationship`, transformation registries, XHTML wrapper).
- **EFM 6.11.x / 6.12.x** — Custom (extension) taxonomy structure: schema, presentation, calculation, definition, label linkbases.

Volume II PDF: https://www.sec.gov/files/edgar/filermanual/efmvol2.pdf
Chapter 6 split: https://www.sec.gov/files/edgar/filermanual/efmvol2-c6.pdf
EDGAR XBRL Guide (plain-language companion): https://www.sec.gov/files/edgar/filer-information/specifications/xbrl-guide.pdf

## 3. Required taxonomies

Canonical list: https://www.sec.gov/info/edgar/edgartaxonomies

A submission package combines exactly one US-GAAP (or IFRS for FPIs)
version plus DEI plus SRT plus any utility taxonomies it dimensionally
references.

- **US-GAAP Financial Reporting Taxonomy** (FASB) — core balance-sheet, income-statement, cash-flow, footnote elements. 2025 version mirrors FASB release of 16 December 2024.
- **DEI (Document and Entity Information)** — entity identity, document type, period, amendment flag, filer category. The 2026 DEI taxonomy adds `NYSETX` for NYSE Texas to the exchange data type.
- **SRT (SEC Reporting Taxonomy)** — schedules, ranges, disposal groups; cross-cutting across US GAAP and IFRS filers.
- **ECD (Executive Compensation Disclosure)** — Pay-Versus-Performance and clawback disclosures (Reg S-K Item 402(v) and 10D-1). 2022Q4 ECD is the operative PVP version.
- **COUNTRY, CURRENCY, EXCH, STPR, NAICS, SIC, SNJ** — utility code-list taxonomies.
- **RR, OEF, CEF, VIP, FND** — fund taxonomies.
- **RXP** — Resource Extraction Payments.

## 4. Custom (extension) elements

Extensions are declared in the filer's company schema
(`<ticker>-<date>.xsd`) when no base concept fits. Requirements:

- Declared in the filer's namespace, with a stable PascalCase name (no spaces).
- Standard Label and (where applicable) Terse, Verbose, Negated, or Period-Start/End labels in a label linkbase.
- Wired into a presentation linkbase under the appropriate parent and given a calculation-linkbase relationship if the value participates in an arithmetic roll-up.
- **Anchored** to the closest base-taxonomy element via a `widerNarrower` (or comparable) definition-linkbase relationship — the SEC equivalent of ESEF anchoring; enforced for IFRS filers under the IFRS-Taxonomy entry-point rules.

The EFM and EDGAR XBRL Guide explicitly require filers to use a base
element when one is "available and appropriate" before creating an
extension. The SEC's "Sample Letter to Companies Regarding Their XBRL
Disclosures" calls out misuse of extensions.

## 5. DEI and the entity context

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

## 6. Decimals, units, and signs

EFM 6.5.16 and the EDGAR XBRL Guide:

- Every numeric `ix:nonFraction` carries a `decimals` attribute. `precision` is not allowed.
- The literal `INF` is **forbidden** for `decimals`. Use a finite integer (e.g., `-3` thousands, `-6` millions, `0` whole units, `2` pennies).
- Monetary values use ISO 4217 currency codes as the unit (`iso4217:USD`).
- Per-share values use a divide unit such as `iso4217:USD / xbrli:shares`.
- A calculation linkbase is required for facts that roll up arithmetically. Calculation inconsistencies are reported as warnings.
- Negated/credit balances: tag the *as-reported* numeric value; never invert the sign manually. Use a negated label role for presentation only. The SEC's June 2024 Sample Letter specifically flagged misuse of negative values on concepts whose balance is credit/debit.

## 7. Common EFM error and warning codes

Codes verbatim, with the EFM section that drives them:

| Code | Meaning | EFM § |
|---|---|---|
| EFM.6.05.01 | CIK / identifier convention violation | 6.5.1 |
| EFM.6.05.11 | Duplicate or equivalent units must be deduplicated | 6.5.11 |
| EFM.6.05.14 | Hidden cover-page fact not referenced via `-sec-ix-hidden` | 6.5.14 |
| EFM.6.05.16 | `decimals` requirement; `INF` not permitted | 6.5.16 |
| EFM.6.05.20 | Required DEI element missing (e.g., `dei:AmendmentFlag`) | 6.5.20 |
| EFM.6.05.21 | Required DEI per document type (e.g., `EntityRegistrantName`) | 6.5.21 |
| EFM.6.05.34 | Inline XBRL submission / well-formedness violation | 6.5.34 |
| EFM.6.05.40 | DEI elements added in newer taxonomies | 6.5.40 |
| EFM.6.05.42 | Deprecated concept used (warning) | 6.5.42 |
| EFM.6.05.48 | Address element tagging via DEI address concepts | 6.5.48 |

Full lists:
- https://www.sec.gov/data-research/xbrl-validation-rendering/edgar-xbrl-validation-errors
- https://www.sec.gov/data-research/xbrl-validation-rendering/edgar-xbrl-validation-warnings

## 8. Submission and validation

- **Test submissions**: filers may submit non-public test filings via EDGAR Online Forms / EDGAR Filer System to exercise the EDGAR Renderer/Previewer before live filing.
- **Public Test Suite**: the SEC's **Interactive Data Public Test Suite** (https://www.sec.gov/structureddata/osdinteractivedatatestsuite) — categorized corpus of small XBRL instances exercising each validation check; used to certify preparation software.
- **Validator stack**: EDGAR uses **Arelle** (https://arelle.org) with the EDGAR plugin (the SEC's EDGAR Renderer is itself an Arelle distribution). The plugin combines the `EFM` validation profile with `FRTA` (Financial Reporting Taxonomy Architecture) checks. EDGAR plugin source on GitHub.
- **Financial Report Viewer**: renders embedded facts at https://www.sec.gov/cgi-bin/viewer and on EDGAR full-text search.
- **Dissemination**: accepted submissions are publicly disseminated within minutes via EDGAR full-text search and the bulk Public Dissemination Service.

### 8.1 Auditor assurance, certifications, liability, and consistency

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
  identical visual appearance is not the test — content consistency is.

## 9. Recent rule updates (last ~24 months)

- **Pay-Versus-Performance** — Release **34-95607**, adopted 25 August 2022, effective 11 October 2022. Compliance for proxy / information statements with fiscal years ending on or after **16 December 2022**. Each value in the PVP table is separately tagged; footnote, relationship, and Tabular List disclosures are block-text tagged. Smaller reporting companies provide Inline XBRL beginning the third PVP filing. Tagging uses the 2022Q4 ECD taxonomy.
- **Cybersecurity Risk Management, Strategy, Governance, and Incident Disclosure** — Release **33-11216 / 34-97989**, adopted 26 July 2023. New Form 8-K Item 1.05 (and 6-K equivalent) for material cybersecurity incidents, due four business days after materiality determination. New Reg S-K Item 106 for annual-report disclosures. **All registrants** (including SRCs) must Inline-XBRL-tag the disclosures by **18 December 2024**.
- **Tailored Shareholder Reports** — Release **33-11125**, adopted 26 October 2022. Open-end funds (Form N-1A) must transmit streamlined annual / semi-annual shareholder reports in Form N-CSR using Inline XBRL for transmittals on or after **24 July 2024**.
- **EDGAR 25.2 / 2026 Taxonomies Updates** — annual taxonomy refreshes (US-GAAP 2025, SRT 2025, DEI 2026) became loadable in EDGAR through 2025–2026. Filers transitioning concept usage should anchor any extensions to the new base elements.

Note: Release **33-11038** is the *proposed* cybersecurity rule
(March 2022). The final cybersecurity rule is **33-11216**. The
"33-11038" reference often seen in vendor documentation is incorrect
when used to mean Tailored Shareholder Reports or Cybersecurity; the
correct final-rule numbers are 33-11125 and 33-11216 respectively.

## Sources

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
