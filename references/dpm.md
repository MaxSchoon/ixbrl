# Data Point Model (DPM) — Banking and Insurance Supervisory Reporting

The XBRL world has two architectures. Inline XBRL regimes (ESEF, EDGAR, KvK, FRC) start with a presentation tree of human-named concepts and embed facts in an HTML carrier. The **Data Point Model** (DPM) world starts with a relational metamodel of metrics × dimensions, rendering the same data as supervisory templates and an XBRL taxonomy. Banks file COREP/FINREP under DPM; insurers file Solvency II under DPM; pension funds file IORP under DPM. Different mental model, different tooling, same XBRL substrate.

## What DPM is and why it differs from financial-reporting taxonomies

The **Data Point Model (DPM)** is a multidimensional metamodel
maintained by the **European Banking Authority (EBA)** and the
**European Insurance and Occupational Pensions Authority (EIOPA)**. It
defines, in database form, every supervisory data point — its
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

> **Honest gap:** The "31 March 2026" cutover date for xBRL-CSV
> mandatory filing was not independently re-verified against an EBA
> primary source in this run. Treat the cutover as expected timing
> from EBA reporting-framework documentation, not verified here, and
> re-confirm against the live EBA Reporting Frameworks page at filing
> time.

## EBA Reporting Frameworks (COREP / FINREP / etc.)

The EBA Reporting Frameworks page lists every framework release back
to 2.3, with the highest currently published version being
**Reporting framework 4.4** (verified directly from the page menu).
Older versions such as 4.2 and 4.3 are also listed. The frameworks
bundle the modules a credit institution or investment firm must file:

- **COREP** — Common Reporting: own funds, capital requirements, large exposures, leverage ratio, NSFR/LCR liquidity.
- **FINREP** — Financial Reporting: IFRS-grounded supervisory financial statements at consolidated and solo level.
- **Resolution / MREL** — resolution planning data and minimum requirement for own funds and eligible liabilities.
- **Asset Encumbrance**, **Funding Plans**, **Remuneration**, **Pillar 3** (now flowing through the EBA Pillar 3 Data Hub), **MiCA** (crypto-asset issuers and CASPs), **DORA** (operational resilience register of ICT-third-party arrangements), **Instant Payments** reporting.

## EIOPA Solvency II and IORP DPM

EIOPA maintains a parallel DPM for insurers and occupational pension
funds, on its **"DPM and XBRL"** page. Confirmed directly:

- The current production **Solvency II Taxonomy** referenced is **2.9.1**, with **2.8.2** as a previous release. A **2.9.1 PWD** (Public Working Draft) is published with DPM Dictionary, Annotated Templates, and IRRD annotated templates at version 2.9.1.
- Pension fund (**IORP**) reporting is delivered through the same DPM release stream, with notes that the 2.7.1 release was applicable until Q4/2024 and 2.9.0 became applicable from Q1/2025 for IORP.
- A **PEPP** (Pan-European Personal Pension Product) prudential reporting flow shares the framework.

> **Honest gap:** A Solvency II 2.10.0 PWD was not visible on the
> EIOPA page when this reference was verified. The latest PWD
> confirmed in this run is 2.9.1. Re-check EIOPA before relying on a
> specific version.

## XBRL Table Linkbase 1.0

The **XBRL Table Linkbase 1.0** Recommendation, dated **2014-03-18**
with errata corrected **2024-12-17**, is published by XBRL International
at https://specifications.xbrl.org/work-product-index-table-linkbase-table-linkbase-1.0.html.
The opening sentence: "The Table Linkbase provides a mechanism for
taxonomy authors to define a tabular layout of facts. The resulting
tables can be used for both presentation and data entry."

A Table Linkbase table is built from **breakdowns** along three
structural axes — typically rows ("y"), columns ("x"), and an
optional sheet axis ("z") used for repeating the same template across,
e.g., currency or country. Each axis tree contains nodes that pin
down primary items (concepts) and dimension members; rendering
software intersects the axes to produce the full table. **This is the
bridge between DPM's relational metamodel and XBRL**: the
human-readable F/C templates are rendering artefacts produced by
walking Table Linkbase definitions, not separate hand-authored
layouts.

By contrast, a presentation linkbase only orders concepts in a tree
for display — it has no concept of rows-times-columns cells.

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

- A **closed table** fixes both the row and column membership — F 01.01 (FINREP balance sheet) has a regulatorily defined set of rows (Cash balances, Financial assets held for trading, …) and columns (Carrying amount, Accumulated impairment, …).
- An **open table** lets the filer enumerate rows or columns at submission time: large exposures (C 28/C 29/C 30), AnaCredit-style loan-level templates, and many Solvency II asset-by-asset templates (S.06.02 list of assets) are open. Open tables rely heavily on **typed dimensions** — XBRL dimensions whose members are not enumerated in the taxonomy but supplied by the filer as data (a counterparty ID, an asset ID, a contract reference). The xBRL-CSV pivot in DPM 2.0 is largely motivated by the inefficiency of XML for these open, row-per-record tables.

## Metrics vs primary items

In DPM terminology a **metric** is the primary item — the "what is
measured" of a fact. Metrics are coded with stable identifiers
(commonly `mi`-prefixed in the DPM dictionary, e.g., `mi1`, `mi500`)
and carry properties such as data type (monetary, decimal, string,
percent, boolean), period type (instant/duration), and balance
(debit/credit, where applicable). **Members** populate dimensions —
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
to their **National Competent Authority** — DNB in the Netherlands,
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

Filers run validation locally — Arelle and commercial DPM-aware
processors load the formula linkbase and report violations — and NCAs
re-run the same rules at intake.

## DPM and Inline XBRL — what's connected, what's not

DPM reports are normally **xBRL-XML or xBRL-CSV** — they are not
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
them as separate processing pipelines — they do not share
extension-taxonomy semantics, anchoring conventions, or output format.

## Sources

- https://www.eba.europa.eu/risk-and-data-analysis/reporting/reporting-frameworks (EBA Reporting Frameworks index — Reporting framework 4.4 down to 2.3; module list including COREP, FINREP, Resolution, MREL, Asset Encumbrance, Funding Plans, Remuneration, Pillar 3, MiCA, DORA, Instant Payments)
- https://www.eba.europa.eu/risk-and-data-analysis/reporting/dpm-data-dictionary (EBA DPM Data Dictionary; DPM Standard 1.0 → 2.0 Refit project; "Towards an enhanced DPM standard 2.0"; DPM Xplor and DPM table layout tools)
- https://www.eiopa.europa.eu/tools-and-data/supervisory-reporting-dpm-and-xbrl_en (EIOPA "DPM and XBRL"; Solvency II Taxonomy 2.9.1 PWD; 2.8.2 prior release; IORP and PEPP framework history)
- https://specifications.xbrl.org/work-product-index-table-linkbase-table-linkbase-1.0.html (Table Linkbase 1.0 Recommendation, 2014-03-18 with errata 2024-12-17)
- https://www.xbrl.org/Specification/xbrl-csv/ (xBRL-CSV 1.0 Recommendation directory; REC-2021-10-13 and REC-2021-10-13+errata-2023-04-19 confirmed)

### Honest gaps

- "31 March 2026" DPM 2.0 cutover date not independently re-verified from a primary EBA source in this run.
- Canonical Eurofiling filing-indicators specification URL and exact `find:` namespace URI not freshly confirmed (eurofiling.info paths returned 404).
- A Solvency II 2.10.0 PWD was not visible on the EIOPA page in this run; the latest PWD confirmed is 2.9.1.
- EUCLID / CRTS / IRIS transport-system names not independently confirmed.

Re-verify each of these against the live regulator page before relying
on it for a regulated filing.
