# Major XBRL/iXBRL Taxonomies

The major XBRL/iXBRL taxonomies in active use globally for statutory and supervisory reporting. Each section: issuer, current version, entry points, filing scope, download URLs. Versions verified against issuer websites; re-check before relying on a specific version for a filing.

**Last verified (UTC): 2026-05-04.** Treat all "current version" references as point-in-time.

## 1. IFRS Accounting Taxonomy

**Issuer / Jurisdiction:** IFRS Foundation (IASB) — global standard-setter
for IFRS Accounting Standards.

**Purpose:** Digital expression of presentation and disclosure
requirements in IFRS Accounting Standards plus IFRS Practice Statement 1
(Management Commentary). Canonical concept set that other regulators
(ESMA, UK FRC, AFM, etc.) extend.

**Current version:** **IFRS Accounting Taxonomy 2025**, published
**27 March 2025**. Reflects IFRS Accounting Standards as issued by the
IASB at 1 January 2025 (including standards issued but not yet
effective). The IFRS Foundation announced in February 2026 that the 2025
taxonomy remains current for 2026 reporting.

**2025 content additions:** IFRS 18 *Presentation and Disclosure in
Financial Statements*; IFRS 19 *Subsidiaries without Public
Accountability: Disclosures*; amendments to IFRS 9/IFRS 7 (financial-
instrument classification, nature-dependent electricity contracts);
Annual Improvements Volume 11.

**Common entry points:**
- Full IFRS Accounting Standards entry point (IAS 1 application baseline)
- Early Application of IFRS 18
- Management Commentary (Practice Statement 1)
- "Essential" entry points (used as base for building extensions)
- IFRS 18 Management Performance Measure (MPM) reconciliation formula

**Filing scope:** The IFRS Foundation does not collect filings; the
taxonomy is reused by jurisdictions that mandate IFRS digital reporting
(most notably ESMA in the EU and the UK).

**Update cadence:** Annual main release in Q1, plus interim "Updates"
when standards change.

**Download:** https://www.ifrs.org/issued-standards/ifrs-taxonomy/ifrs-accounting-taxonomy-2025/

## 2. ESEF Taxonomy (European Single Electronic Format)

**Issuer / Jurisdiction:** European Securities and Markets Authority
(ESMA), EU-wide.

**Purpose:** Mandatory digital reporting format for Annual Financial
Reports (AFRs) of issuers with securities admitted to trading on EU
regulated markets (Transparency Directive). The ESEF taxonomy *extends*
the IFRS Accounting Taxonomy with EU-specific dimensions, entry points,
and architecture.

**Current version:** **ESEF Taxonomy 2024**, with the **2025 ESEF
taxonomy dated 2025-03-27** also published by ESMA. The 2025 taxonomy
reflects the IASB's 2025 IFRS taxonomy and IFRS 18 (mandatory tagging
effective 1 January 2027, early application allowed). The ESEF 2025
taxonomy becomes mandatory for AFRs covering financial years starting on
or after **1 January 2026**.

**Core architecture:** Filers reference the ESMA "core" entry point
`esef_cor.xsd`, which imports the IFRS Accounting Taxonomy. Issuers add
an entity-specific extension taxonomy with anchored extension concepts.
Labels and documentation ship in all 24 EU official languages.

**Mandatory tagging scope:**
- **Primary financial statements:** detailed element-by-element tagging
  (since financial year 2020).
- **Notes to consolidated IFRS financial statements:** **block tagging**
  of the notes mandatory for financial years starting on or after
  **1 January 2022**.

**Reporting Manual:** ESEF Reporting Manual (ESMA32-60-254) is the
canonical filer guidance, updated annually. It specifies anchoring, sign
conventions, scale, and the taxonomy elements applicable to block tags.

**Filing scope:** All issuers with securities listed on EU-regulated
markets that prepare consolidated IFRS financial statements. National
competent authorities (AFM, AMF, BaFin, CNMV, etc.) operate the actual
filing infrastructure.

**Download:**
- https://www.esma.europa.eu/electronic-reporting/esef-taxonomy
- https://www.esma.europa.eu/document/esef-taxonomy-2024
- https://www.esma.europa.eu/sites/default/files/library/esma32-60-254_esef_reporting_manual.pdf

## 3. US-GAAP Financial Reporting Taxonomy

**Issuer / Jurisdiction:** Financial Accounting Standards Board (FASB),
United States. Accepted and operationalized by the SEC.

**Current version:** **2025 GAAP Financial Reporting Taxonomy (GRT)**,
accepted by the SEC on **18 March 2025**. The SEC concurrently accepted
the **2025 SEC Reporting Taxonomy (SRT)** and the **2025 GAAP Employee
Benefit Plan Taxonomy (EBPT)**.

**Publication path:** FASB authors and exposes the GRT for public review;
the SEC formally "accepts" each annual release for use in EDGAR filings.
Until acceptance, the prior year's taxonomy applies.

**Common namespaces:**
- `us-gaap` — FASB-authored core US GAAP concepts.
- `srt` — SEC Reporting Taxonomy: cross-cutting concepts (schedules,
  ranges, disposal groups) used across US GAAP and IFRS filers with the
  SEC.
- `dei` — Document and Entity Information (filer identity, period,
  document type, EntityCentralIndexKey, etc.). Authored under SEC
  oversight.
- `country`, `currency`, `exch`, `naics`, `sic`, `stpr` — code-list
  reference taxonomies.

**2025 content additions:** New elements for SEC Release Nos. 33-11070 /
34-95025 (Form 11-K employee benefit plans), disaggregation of income
statement expenses, profits-interest awards, induced conversions of
convertible debt instruments.

**Filing scope:** All registrants filing periodic and current reports
with the SEC under the Securities Exchange Act of 1934 (10-K, 10-Q, 8-K
with financial highlights, S-1/S-3 registrations, 6-K for foreign private
issuers, 11-K). Foreign private issuers using IFRS file under the IFRS
Taxonomy as accepted by the SEC, not the FASB GRT.

**Download:**
- https://www.fasb.org/page/detail?pageId=/projects/FASB-Taxonomies/2025-gaap-financial-reporting-taxonomy.html
- https://www.fasb.org/projects/fasb-taxonomies
- https://xbrl.fasb.org/resources/annualrelease/2025/GAAP_Financial_Reporting_Taxonomy_Release_Notes.pdf

## 4. UK FRC Taxonomy Suite

**Issuer / Jurisdiction:** Financial Reporting Council (FRC), UK,
operating the cross-regulator UK XBRL programme on behalf of Companies
House, HMRC, the Charity Commission, the FCA (UKSEF), and Irish Revenue
(Irish Extension).

**Current version:** **2026 FRC Taxonomy Suite v1.0.0**, released
**18 November 2025**. Prior **2025 FRC Taxonomy Suite v1.0.0** was
released 18 October 2024. FRC guidance: only the latest and penultimate
versions should be in active use simultaneously.

**Taxonomies in the Suite:**
- **UK IFRS** — UK companies preparing accounts under UK-adopted IFRS.
- **FRS 101** — Reduced Disclosure Framework (subsidiaries of IFRS
  groups).
- **FRS 102** — UK and Ireland GAAP (the dominant SME taxonomy).
- **UKSEF** — UK Single Electronic Format, the UK's post-Brexit successor
  extending ESEF for FCA listed-issuer filings.
- **Charities Taxonomy** — for charities reporting under the Charities
  FRS 102 SORP. Mandatory for large charities (income > £6.5m); refreshed
  for SORP 2026 in the 2026 suite.
- **Irish Extension** — Irish Revenue iXBRL filing of Corporation Tax
  accounts.

**Filing scope:**
- Companies House statutory accounts (most UK companies, in iXBRL).
- HMRC Corporation Tax computations and accounts attached to CT600
  (mandatory iXBRL).
- Charity Commission / HMRC for charities meeting the threshold.
- FCA for UKSEF AFR filings of premium- and standard-listed issuers.

**Download:**
- https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/frc-taxonomies/
- https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/frc-taxonomies/current-frc-taxonomy-suites/2026-frc-taxonomy-suite/
- https://www.gov.uk/file-your-company-annual-accounts

## 5. Dutch SBR / Nederlandse Taxonomie (NT)

**Issuer / Jurisdiction:** SBR Nederland — joint programme of Dutch
government, Belastingdienst, KvK, DNB, AFM, CBS, and the banks.

**Versioning:** Annual NT releases, currently in the **NT20** generation.
The Belastingdienst slice of NT20 (release `20251210.a`) was published
29 August 2025 and applies to corporate income tax 2025, VAT 2026, and
ICP 2026 filings. The definitive iXBRL annual-reporting taxonomies for
fiscal year 2025 were published **12 December 2025** for filing with the
KvK.

**Architecture:** The NT layers downward — BW2 (Civil Code Book 2) is the
core; RJ (Raad voor de Jaarverslaggeving) extends it for Dutch GAAP
application guidance; KvK applies BW2/RJ (and IFRS) for trade-register
deposits; AFM extends ESEF/IFRS for listed-issuer AFRs.

**Common entry points:**
- KvK Dutch GAAP entry points by company-size class: micro, small,
  medium, large (different disclosure depths under Title 9 Book 2 BW).
- KvK IFRS entry points where the entity reports under IFRS but files at
  the trade register.
- AFM ESEF / IFRS for Dutch listed-issuer AFRs (extends ESEF core).
- Belastingdienst entry points for corporate income tax (VPB), VAT (OB),
  payroll, and ICP returns.

**Namespaces (complementary, not interchangeable):**
- `bw2-titel9:` — Civil Code Title 9 core concepts.
- `rj:` — RJ extension concepts including cash-flow statement detail.
- `kvk:` — KvK metadata and entity-size dimensions.
- IFRS namespaces where applicable.

**Filing scope:** All Dutch legal entities required to file annual
accounts at the KvK; all VPB taxpayers; all AFR filers under ESEF for
Dutch listed issuers.

**Hosting:** Canonical schemas live at `nltaxonomie.nl`.

**Download:**
- https://www.sbr-nl.nl/werken-met-sbr/taxonomie/documentatie-nederlandse-taxonomie
- https://www.sbr-nl.nl/werken-met-sbr/taxonomie/architectuur-en-ontwikkelingen

## 6. EBA & EIOPA — Data Point Model (DPM) for Banking and Insurance

**Issuer / Jurisdiction:** European Banking Authority (EBA) for banking;
European Insurance and Occupational Pensions Authority (EIOPA) for
insurance and pensions. EU-wide, applied by national competent
authorities.

**Why structurally different from financial-reporting taxonomies:** The
DPM is **table-driven**. Concepts (metrics × dimensions) are organized
into supervisory reporting templates (rows × columns × sheets), not
presentation trees. The XBRL taxonomy is a derived rendering of the DPM
database. From 2025–2026 onward EBA is migrating to **DPM 2.0**, and
reports referencing periods ≥ 31 March 2026 must be filed in **xBRL-CSV**
(replacing xBRL-XML for these high-volume datasets).

### EBA — COREP / FINREP

**Current version:** The EBA Reporting Frameworks page currently
publishes **Reporting Framework 4.4** as the latest release, with 4.2
and 4.3 also listed for prior reference dates. Re-verify the operative
framework version against the EBA page at filing date.

**Modules:** COREP (own funds, large exposures, leverage, NSFR/LCR),
FINREP (IFRS-based supervisory financials), Resolution planning, MREL,
Asset Encumbrance, Funding Plans, Remuneration, Pillar 3 disclosures,
MiCA, DORA, Instant Payments.

**Filing scope:** EU credit institutions, investment firms, and certain
other regulated entities, reporting to national competent authorities
under CRR/CRD.

**Download:**
- https://www.eba.europa.eu/risk-and-data-analysis/reporting-frameworks
- https://www.eba.europa.eu/risk-and-data-analysis/reporting-frameworks/reporting-framework-42

### EIOPA — Solvency II and IORP

**Current version:** The EIOPA "DPM and XBRL" page currently references
**Solvency II Taxonomy 2.9.1 PWD** (with DPM Dictionary, Annotated
Templates, and IRRD annotated templates at 2.9.1) and **2.8.2** as a
prior release. Pension fund (IORP) reporting moved from 2.7.1
(applicable until Q4/2024) to 2.9.0 (applicable from Q1/2025).
Re-verify against the live EIOPA page before relying on a specific
version.

**Filing scope:** Insurance and reinsurance undertakings and groups
(Solvency II); occupational pension funds (IORP II).

**Download:** https://www.eiopa.europa.eu/tools-and-data/supervisory-reporting-dpm-and-xbrl_en

## 7. Other Notable Taxonomies

**Japan — EDINET (FSA).** The Financial Services Agency of Japan operates
EDINET for electronic disclosure of statutory filings (annual securities
reports, quarterly reports, prospectuses) by listed Japanese issuers, in
XBRL since 2008. https://disclosure2.edinet-fsa.go.jp/

**Spain — CNMV IPP.** Comisión Nacional del Mercado de Valores receives
Periodic Public Information in XBRL from listed issuers, originating with
Circular 1/2005 and updated through Circular 5/2015 and Circular 3/2018.
CNMV also acts as the national ESEF officer for Spanish issuers.
https://www.cnmv.es/Portal/xbrl/xbrl

**Australia — SBR (cross-agency).** SBR AU Taxonomy (XBRL-based) reused
across the ATO and other agencies for tax, super (SuperStream), and
business reporting.
https://www.sbr.gov.au/digital-service-providers/sbr-implementation-support-products/sbr-au-taxonomy

**India — MCA.** Ministry of Corporate Affairs maintains the C&I
Taxonomy (Indian GAAP / IND-AS) and Costing Taxonomy used for filing
financial statements via e-form AOC-4 XBRL. Mandatory for listed
companies, their Indian subsidiaries, companies with paid-up capital
≥ INR 5 crore, companies with turnover ≥ INR 100 crore, and all companies
preparing accounts under IND-AS Rules 2015.
https://www.mca.gov.in/MinistryV2/xbrl.html

## Sources

- https://www.ifrs.org/issued-standards/ifrs-taxonomy/
- https://www.ifrs.org/issued-standards/ifrs-taxonomy/ifrs-accounting-taxonomy-2025/
- https://www.ifrs.org/news-and-events/news/2025/03/ifrs-accounting-taxonomy-2025-is-now-available/
- https://www.esma.europa.eu/electronic-reporting/esef-taxonomy
- https://www.esma.europa.eu/document/esef-taxonomy-2024
- https://www.esma.europa.eu/sites/default/files/library/esma32-60-254_esef_reporting_manual.pdf
- https://www.esma.europa.eu/press-news/esma-news/esma-publishes-2024-esef-reporting-manual
- https://www.esma.europa.eu/press-news/esma-news/updated-2025-ifrs-taxonomy-introduced-european-single-electronic-format
- https://www.fasb.org/page/detail?pageId=/projects/FASB-Taxonomies/2025-gaap-financial-reporting-taxonomy.html
- https://www.fasb.org/projects/fasb-taxonomies
- https://www.fasb.org/news-and-meetings/in-the-news/sec-accepts-2025-fasb-taxonomies-421244
- https://xbrl.fasb.org/resources/annualrelease/2025/GAAP_Financial_Reporting_Taxonomy_Release_Notes.pdf
- https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/frc-taxonomies/
- https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/frc-taxonomies/current-frc-taxonomy-suites/2026-frc-taxonomy-suite/
- https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/frc-taxonomies/current-frc-taxonomy-suites/2025-frc-taxonomy-suite/
- https://www.gov.uk/file-your-company-annual-accounts
- https://www.sbr-nl.nl/werken-met-sbr/taxonomie/documentatie-nederlandse-taxonomie
- https://www.sbr-nl.nl/werken-met-sbr/taxonomie/architectuur-en-ontwikkelingen
- https://www.sbr-nl.nl/sites/default/files/bestanden/taxonomie/NT20_BD_20251210.a%20Releasenotes.pdf
- https://www.eba.europa.eu/risk-and-data-analysis/reporting-frameworks
- https://www.eba.europa.eu/risk-and-data-analysis/reporting-frameworks/reporting-framework-42
- https://www.eiopa.europa.eu/tools-and-data/supervisory-reporting-dpm-and-xbrl_en
- https://disclosure2.edinet-fsa.go.jp/
- https://www.cnmv.es/Portal/xbrl/xbrl
- https://www.sbr.gov.au/digital-service-providers/sbr-implementation-support-products/sbr-au-taxonomy
- https://www.mca.gov.in/MinistryV2/xbrl.html
