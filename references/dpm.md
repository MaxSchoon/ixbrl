# Data Point Model (DPM): Banking and Insurance Supervisory Reporting

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*

**Load this when:** the filing is supervisory: EBA COREP or FINREP, EIOPA Solvency II or IORP, or the question is Table Linkbase, filing indicators, or the xBRL-CSV migration.

**Do not load this when:** the report is a financial statement in Inline XBRL. DPM filings are not inline (see *DPM and Inline XBRL: what's connected, what's not*); use `references/esef.md` or the jurisdiction file.

The XBRL world has two architectures. Inline XBRL regimes (ESEF, EDGAR, KvK, FRC) start with a presentation tree of human-named concepts and embed facts in an HTML carrier. The **Data Point Model** (DPM) world starts with a relational metamodel of metrics × dimensions, rendering the same data as supervisory templates and an XBRL taxonomy. Banks file COREP/FINREP under DPM; insurers file Solvency II under DPM; pension funds file IORP under DPM. Different mental model, different tooling, same XBRL substrate.

## Contents

- [What DPM is and why it differs from financial-reporting taxonomies](#what-dpm-is-and-why-it-differs-from-financial-reporting-taxonomies)
- [DPM 2.0 architecture and the xBRL-CSV migration](#dpm-20-architecture-and-the-xbrl-csv-migration)
- [EBA Reporting Frameworks (COREP / FINREP / etc.)](#eba-reporting-frameworks-corep--finrep--etc)
- [EIOPA Solvency II and IORP DPM](#eiopa-solvency-ii-and-iorp-dpm)
- [DTS and vintages: EBA and EIOPA](#dts-and-vintages-eba-and-eiopa)
- [XBRL Table Linkbase 1.0](#xbrl-table-linkbase-10)
- [Filing indicators (find namespace)](#filing-indicators-find-namespace)
- [Open vs closed tables](#open-vs-closed-tables)
- [Metrics vs primary items](#metrics-vs-primary-items)
- [xBRL-CSV report packages](#xbrl-csv-report-packages)
- [Filing flow (filer → NCA → EBA/EIOPA)](#filing-flow-filer--nca--ebaeiopa)
- [Validation rules (V-rules)](#validation-rules-v-rules)
- [DPM and Inline XBRL: what's connected, what's not](#dpm-and-inline-xbrl-whats-connected-whats-not)
- [Sources](#sources)

## What DPM is and why it differs from financial-reporting taxonomies

The **Data Point Model (DPM)** is a multidimensional metamodel
maintained by the **European Banking Authority (EBA)** and the
**European Insurance and Occupational Pensions Authority (EIOPA)**. It
defines, in database form, every supervisory data point: its
business meaning, the metric it expresses, and the dimensions
(counterparty, currency, maturity, exposure class, accounting
portfolio, etc.) that qualify it. Both the human-readable supervisory
templates published in EU Implementing Technical Standards (ITS) **and**
the machine-readable XBRL taxonomy used to file them are derived from
the same underlying dictionary. The EBA describes the DPM as "the
standardised description of the metadata that defines and describes
regulatory data".

This differs fundamentally from presentation-tree-driven taxonomies (IFRS, US-GAAP), which start with a hierarchy of human-named concepts. In DPM the *table* is the assembly point: every cell of every supervisory template (e.g., F 01.01 row 010 column 010) is wired to a precise (metric × dimensional context) tuple. The taxonomy is a database schema rendered into XBRL.

## DPM 2.0 architecture and the xBRL-CSV migration

The EBA DPM Data Dictionary page describes the move from **DPM
Standard 1.0** to **DPM Standard 2.0** as a "DPM Refit" project run
jointly with EIOPA, intended to enhance the standard for evolving
supervisory needs. The motivating problem was scalability: granular
datasets (loan-level, transaction-level, AnaCredit-style) do not fit
cleanly into XBRL-XML, where each fact is a verbose XML element. DPM
2.0 re-architects the metamodel and pivots the file format from
**xBRL-XML** to **xBRL-CSV** for the heavy modules.

> **EBA level, verified:** the EBA Reporting framework 4.2 page states
> the CSV adoption policy in terms: "For the reports with reference
> dates >= 31/03/2026, all the submitted or resubmitted reports must be
> in xBRL-CSV format ... For the reports with reference dates <
> 31/03/2026, EBA accept both xBRL-XML and xBRL-CSV report for all the
> submission and resubmission." The obligation originally carried a
> 31/12/2025 reference date and the EBA moved it to 31/03/2026 with the
> Reporting framework 4.1 hotfix. Four report types sit outside the
> date entirely: MiCA, Pillar 3 and Instant Payments are xBRL-CSV
> regardless of reference date, and DORA is plain CSV.
>
> **France, verified:** the ACPR/Banque de France FAQ *Passage au
> format xBRL-CSV 03/2026* (v.2, February 2026) carries the same date
> into the national collection: "À compter de l'arrêté du 31/03/2026
> ... Les remises au format xBRL-XML ne seront plus acceptées". The
> French scoping is narrower than the EBA rule: earlier reference dates
> stay in xBRL-XML, corrections and late filings included whatever the
> deposit date, as do the national SUR-domain collections (RUBA) and
> the whole Solvency II insurance track.

## EBA Reporting Frameworks (COREP / FINREP / etc.)

The EBA Reporting Frameworks page lists every framework release back
to 2.3. The page menu runs up to **Reporting framework 4.4**, but on
2026-08-21 the latest release with a published technical package was
**4.2**; 4.3 and 4.4 are announced for later reference dates with no
artefacts yet (see *DTS and vintages* below). The frameworks bundle the
modules a credit institution or investment firm must file:

- **COREP** (Common Reporting): own funds, capital requirements, large exposures, leverage ratio, NSFR/LCR liquidity.
- **FINREP** (Financial Reporting): IFRS-grounded supervisory financial statements at consolidated and solo level.
- **Resolution / MREL**: resolution planning data and minimum requirement for own funds and eligible liabilities.
- **Asset Encumbrance**, **Funding Plans**, **Remuneration**, **Pillar 3** (now flowing through the EBA Pillar 3 Data Hub), **MiCA** (crypto-asset issuers and CASPs), **DORA** (operational resilience register of ICT-third-party arrangements), **Instant Payments** reporting.

## EIOPA Solvency II and IORP DPM

EIOPA maintains a parallel DPM for insurers and occupational pension
funds, on its **"DPM and XBRL"** page. Confirmed directly:

- The **Solvency II Taxonomy** in production is **2.8.2** (applicable from the Q4 / annual 2024 reference periods until Q4 / annual 2026 included); **2.10.0 Final** was published on 3 July 2026 for reference periods from Q1 2027. "2.9.1 PWD" survives on the page only as a change-log baseline.
- Pension fund (**IORP**) reporting is delivered through the same DPM release stream: 2.7.1 was applicable until Q4/2024 and 2.9.0 (with its NACE 2.1 hotfixes) from Q1/2025.
- A **PEPP** (Pan-European Personal Pension Product) prudential reporting flow shares the framework, and **IRRD 2.11.0 Final** (27 July 2026) joined it.

An earlier edition of this section named 2.9.1 as the production
version and recorded 2.10.0 as not visible; both were superseded by the
2026-08-21 check recorded in *DTS and vintages* below.

## DTS and vintages: EBA and EIOPA

Which framework release to load, where it lives, and for which reference
dates. Vocabulary and column order follow `references/dts.md`
§ Vocabulary. Verified 2026-08-21 by downloading the EBA 4.2 and EIOPA
Solvency II 2.10.0 packages. No entry-point URI dereferences at either
authority (`http://www.eba.europa.eu/eu/fr/xbrl/crr/fws/corep/4.2/mod/corep_of.xsd`
and `http://eiopa.europa.eu/eu/xbrl/s2md/fws/solvency/solvency2/2026-06-30/mod/qrs.xsd`
both return 403); load the package. Validity is machine-readable in two
places: Eurofiling `model:fromDate` / `model:modificationDate` on element
declarations, and (EBA only) `eba:documentation.FromReferenceDate` /
`toReferenceDate` in each module's JSON. EBA ships an xBRL-CSV table
template beside every module; EIOPA ships no JSON and remains xBRL-XML.

| Release | Entry point(s) | Package | Valid time | Accepted at deposit | Status | Source |
|---|---|---|---|---|---|---|
| **EBA 4.2** (Q4 2025; hotfix and FINREP9DP artefacts 27 Feb 2026) | 50 modules `…/crr/fws/<framework>/4.2/mod/<module>.xsd` | `https://www.eba.europa.eu/sites/default/files/2026-01/b54d2c74-877c-4195-a32a-6591253d8b0f/taxo_package_4.2_hotfix.zip` (200, 65 MB); 4.2.1 FINREP9DP `…/2026-02/5ecd43ca-893a-4b72-a6aa-08e19d125926/taxonomy%20package%204.2.1%20%28FINREP9DP%29.zip` | module-specific: most from reference date **31 Mar 2026** (`corep_of.json` `FromReferenceDate 2026-03-31`), Resolution and MREL 12/2025, COREP OF 06/2026 | **xBRL-CSV mandatory for reference dates on or after 31 Mar 2026**; XML and CSV both accepted below that; MiCA, Pillar 3, Instant Payments, DORA always CSV; from 1 Jul 2026 Euclid rejects CSV files with a negative filing indicator | current released framework | EBA 4.2 page; EBA Filing Rules v5.8 (25 Feb 2026) |
| EBA 4.3 (expected Q2 2026; "expected to apply from Q4 2026") | Third Country Branches, AMLA risk assessment | the 4.3 page carries "Taxonomy package 4.3", "Sample files 4.3" and "EBA filing rule V5.9" headings with **no downloadable artefact** behind them on 2026-08-21 | TCB 03/2027; AMLA 12/2026 | AMLA components "must not be used for data submissions" | announced; artefacts not yet published | EBA 4.3 page (fetched 2026-08-21) |
| EBA 4.4 (expected Q3 2026) | phase 1 FINREP (IFRS 18), DORA, Resolution, MREL, AMLA, Pillar 3; phase 2 ESG, COREP, AE, ALMM, LCR, … | not published | phase 1 from 12/2026, phase 2 from 09/2027 | | announced, no artefacts | EBA reporting-frameworks page |
| EBA 4.1 (Q2 2025), 4.0 (from 12/2024) | MiCAR, Pillar 3; CRR3/CRD6 COREP, DORA | own pages | module-specific from 06/2025 and 03/2025 | superseded; 4.0 and 4.1 were the last to ship DPM 1.0 beside 2.0 | historical | EBA pages |
| **EIOPA Solvency II 2.8.2** (15 Oct 2024; optional NACE 2.1 hotfix 30 Jun 2025, same entry points) | dated `mod/` set | `https://dev.eiopa.europa.eu/Taxonomy/Full/2.8.2/S2/EIOPA_SolvencyII_XBRL_Taxonomy_2.8.2_Final.zip` (200) | **Q4 / annual 2024 until Q4 / annual 2026 included** | in production | **the operative Solvency II version** | EIOPA DPM-and-XBRL page |
| **EIOPA Solvency II 2.10.0** (Final, 3 Jul 2026; `publicationDate` 2026-06-30) | 17 modules `…/s2md/fws/solvency/solvency2/2026-06-30/mod/{qrs,qes,ars,aes,…}.xsd` | `https://dev.eiopa.europa.eu/Taxonomy/Full/2.10.0/S2/EIOPA_SolvencyII_XBRL_Taxonomy_2.10.0.zip` (200, 50 MB) | from **Q1 2027** | not yet in production | published, future-dated | EIOPA page; package manifest |
| EIOPA IORP 2.9.0 hotfix (16 Jul 2024) and 2nd NACE hotfix (30 Jun 2025) | PF modules | `…/2.9.0_hotfix2/PF/EIOPA_PensionFunds_XBRL_Taxonomy_2.9.0_Hotfix2.zip` (200) | from 1 Jan 2025 until a new version is announced (2.7.1 closed after Q4 2024) | in production | current | EIOPA page |
| EIOPA IRRD 2.11.0 (Final, 27 Jul 2026); FICOD 2.8.1 hotfix 2; PEPP PR 2.7.0 hotfix 3; PEPP KID 2.6.1 | own modules | `…/2.11.0/irrd/EIOPA_IRRD_XBRL_Taxonomy_2.11.0.zip` (200); FICOD and PEPP zips under the same host | IRRD not stated; FICOD from 31 Dec 2023; PEPP from Q4 2022 | IRRD not yet; others in production | published / current | EIOPA page |

"2.9.1 PWD" survives on EIOPA's page only as the baseline of the 2.11.0
change log; it is not a release to validate against.

## XBRL Table Linkbase 1.0

The **XBRL Table Linkbase 1.0** Recommendation, dated **2014-03-18**
with errata corrected **2024-12-17**, is published by XBRL International
at https://specifications.xbrl.org/work-product-index-table-linkbase-table-linkbase-1.0.html.
The opening sentence: "The Table Linkbase provides a mechanism for
taxonomy authors to define a tabular layout of facts. The resulting
tables can be used for both presentation and data entry."

A Table Linkbase table is built from **breakdowns** along three
structural axes: typically rows ("y"), columns ("x"), and an
optional sheet axis ("z") used for repeating the same template across,
e.g., currency or country. Each axis tree contains nodes that pin
down primary items (concepts) and dimension members; rendering
software intersects the axes to produce the full table. **This is the
bridge between DPM's relational metamodel and XBRL**: the
human-readable F/C templates are rendering artefacts produced by
walking Table Linkbase definitions, not separate hand-authored
layouts.

By contrast, a presentation linkbase only orders concepts in a tree
for display; it has no concept of rows-times-columns cells.

## Filing indicators (find namespace)

DPM filings include a **filing indicators** block that tells the
receiver which templates the filer is actually submitting in this
report. This is essential because the taxonomy entry point covers
every template a given module could carry, but on any given reference
date a filer typically submits a subset. The mechanism originates
from the Eurofiling community.

The widely deployed convention referenced across EBA and EIOPA filing
manuals uses elements in a **`find:` (filing indicators) namespace**,
with a parent element (e.g., `find:fIndicators`) wrapping per-template
`find:filingIndicator` elements that carry the template code as
content (e.g., `S.02.01`, `C 01.00`, `F 01.01`) and a `filed`
attribute.

> **Honest gap:** The canonical Eurofiling specification URL and the
> exact `find:` namespace URI were not re-fetched in this run (the
> eurofiling.info paths returned 404 or non-spec content). Re-verify
> the URI against the current Eurofiling spec or EBA filing manual
> before relying on it.

## Open vs closed tables

DPM distinguishes **closed** from **open** tables.

- A **closed table** fixes both the row and column membership: F 01.01 (FINREP balance sheet) has a regulatorily defined set of rows (Cash balances, Financial assets held for trading, …) and columns (Carrying amount, Accumulated impairment, …).
- An **open table** lets the filer enumerate rows or columns at submission time: large exposures (C 28/C 29/C 30), AnaCredit-style loan-level templates, and many Solvency II asset-by-asset templates (S.06.02 list of assets) are open. Open tables rely heavily on **typed dimensions**: XBRL dimensions whose members are not enumerated in the taxonomy but supplied by the filer as data (a counterparty ID, an asset ID, a contract reference). The xBRL-CSV pivot in DPM 2.0 is largely motivated by the inefficiency of XML for these open, row-per-record tables.

## Metrics vs primary items

In DPM terminology a **metric** is the primary item: the "what is
measured" of a fact. Metrics are coded with stable identifiers
(commonly `mi`-prefixed in the DPM dictionary, e.g., `mi1`, `mi500`)
and carry properties such as data type (monetary, decimal, string,
percent, boolean), period type (instant/duration), and balance
(debit/credit, where applicable). **Members** populate dimensions;
e.g., an "Accounting portfolio" dimension takes members like "Held for
trading", "Amortised cost", "FVOCI". A table cell binds a single
metric to a vector of dimension members; the resulting tuple is the
data point. This is why a single FINREP fact carries far more
dimensional context than a typical IFRS-taxonomy fact: the dimensions
are doing the work that human-named concept hierarchies do in
IFRS/US-GAAP taxonomies.

## xBRL-CSV report packages

**xBRL-CSV 1.0** is a Recommendation of XBRL International published
**2021-10-13**, with errata dated **2023-04-19**. An xBRL-CSV report is
a ZIP report package containing:

- a **JSON report metadata** file (the "report" document) declaring the taxonomy entry point, parameters, and which CSV tables make up the report;
- one or more **CSV files**, each holding rows of facts whose columns match a `tableTemplate` defined in the taxonomy or report metadata;
- the customary taxonomy-package wrapping (catalog, manifest) so a processor can resolve the entry point.

CSV files scale to millions of rows where the equivalent XML would be
gigabytes, which is why DPM 2.0 selected this format for granular
modules.

## Filing flow (filer → NCA → EBA/EIOPA)

For banking modules, EU credit institutions and investment firms file
to their **National Competent Authority**: DNB in the Netherlands,
BaFin in Germany, ACPR in France, Bank of Italy, Bank of Spain, etc.
The NCA validates and onward-transmits the data to the EBA's
secondary-reporting infrastructure. The EBA "Secondary reporting"
page is the canonical description of NCA-to-EBA data transmission.

For Solvency II, insurers file to their NCA; EIOPA receives onward
data via its central infrastructure. The EIOPA "DPM and XBRL" page is
the operational reference for taxonomy versions, schedules, and known
issues.

> **Honest gap:** The specific names of the EBA "EUCLID" or EIOPA
> "CRTS"/"IRIS" transport systems were not re-verified in this run.
> Treat those acronyms as conventional rather than confirmed here.

## Validation rules (V-rules)

DPM frameworks ship a body of validation rules ("V-rules") that filers
must satisfy before submission. Mechanically these are **XBRL Formula
assertions** distributed as part of the taxonomy. They cover:

- **cardinal sanity** (a balance sheet must balance),
- **intra-template arithmetic** (sum of subcategories equals reported total),
- **cross-template consistency** (a value in COREP matches the corresponding value in FINREP).

Filers run validation locally (Arelle and commercial DPM-aware
processors load the formula linkbase and report violations), and NCAs
re-run the same rules at intake.

## DPM and Inline XBRL: what's connected, what's not

DPM reports are normally **xBRL-XML or xBRL-CSV**. They are not
Inline XBRL. The reason is purpose. Inline XBRL is a delivery format
that embeds machine-readable facts inside an HTML document a human
will actually read: the ESEF annual financial report, an SEC EDGAR
10-K, a Companies House micro-entity accounts deposit. DPM filings
are pure supervisory data exchanges between a regulated entity and a
regulator; there is no human reader of the artefact, no "annual
report" wrapping, and no requirement that the document render as a
presentable narrative. The DPM standard therefore optimises for
machine ingestion (XML for structured templates, CSV for granular
templates), not for dual human/machine consumption.

The architectural lesson for an iXBRL skill is that the Inline-XBRL
world (ESEF, EDGAR, KvK, FRC) and the DPM world share the same base
XBRL standard but **diverge sharply above it**: DPM is dimension-led
and template-driven, with table-linkbase rendering and filing
indicators; iXBRL regimes are concept-led, presentation-tree driven,
and embedded in an HTML carrier. A tool that handles both must keep
them as separate processing pipelines: they do not share
extension-taxonomy semantics, anchoring conventions, or output format.

## Sources

- https://www.eba.europa.eu/risk-and-data-analysis/reporting/reporting-frameworks (EBA Reporting Frameworks index: Reporting framework 4.4 down to 2.3; module list including COREP, FINREP, Resolution, MREL, Asset Encumbrance, Funding Plans, Remuneration, Pillar 3, MiCA, DORA, Instant Payments)
- https://www.eba.europa.eu/risk-and-data-analysis/reporting/dpm-data-dictionary (EBA DPM Data Dictionary; DPM Standard 1.0 → 2.0 Refit project; "Towards an enhanced DPM standard 2.0"; DPM Xplor and DPM table layout tools)
- https://www.eiopa.europa.eu/tools-and-data/supervisory-reporting-dpm-and-xbrl_en (EIOPA "DPM and XBRL"; Solvency II Taxonomy 2.9.1 PWD; 2.8.2 prior release; IORP and PEPP framework history)
- https://specifications.xbrl.org/work-product-index-table-linkbase-table-linkbase-1.0.html (Table Linkbase 1.0 Recommendation, 2014-03-18 with errata 2024-12-17)
- https://www.xbrl.org/Specification/xbrl-csv/ (xBRL-CSV 1.0 Recommendation directory; REC-2021-10-13 and REC-2021-10-13+errata-2023-04-19 confirmed)
- https://esurfi.banque-france.fr/system/files/2026-02/FAQ%20-%20xBRL-CSV%20VF2_fevrier%202026_0.pdf (ACPR/Banque de France FAQ, *Passage au format xBRL-CSV 03/2026*, v.2 February 2026: xBRL-XML no longer accepted from the 31/03/2026 reference date; prior reference dates, corrections and late filings stay xBRL-XML; SUR-domain national taxonomies including RUBA out of scope)
- https://www.eba.europa.eu/risk-and-data-analysis/reporting-frameworks/reporting-framework-42 (EBA Reporting framework 4.2, "CSV adoption policy": xBRL-CSV obligation moved from reference date 31/12/2025 to 31/03/2026; reference dates on or after 31/03/2026 must be xBRL-CSV for submission and resubmission; MICA, PILLAR3, INSTANT PAYMENT and DORA always CSV regardless of reference date)
- https://www.eba.europa.eu/sites/default/files/2025-11/f54ced05-870e-4dd0-a591-ecbcac2e32d4/faq_for_reporting_innovations_and_upcoming_releases_v2.pdf (EBA *FAQ for Reporting Innovations (release 4.0 and beyond)*, v2 November 2025, Q10: from reference date 03/2026 only xBRL-CSV is accepted on Euclid; DORA is plain CSV, Pillar 3 Data Hub always xBRL-CSV)

### Honest gaps

- Canonical Eurofiling filing-indicators specification URL and exact `find:` namespace URI not freshly confirmed (eurofiling.info paths returned 404).
- A Solvency II 2.10.0 PWD was not visible on the EIOPA page in this run; the latest PWD confirmed is 2.9.1.
- EUCLID / CRTS / IRIS transport-system names not independently confirmed.

Re-verify each of these against the live regulator page before relying
on it for a regulated filing.
