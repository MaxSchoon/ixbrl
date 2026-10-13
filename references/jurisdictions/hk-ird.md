---
reference_id: hk-ird
jurisdiction: HK
restructured_on: 2026-10-13
profiles:
  - id: ird-profits-tax
    section: profile-ird-profits-tax
---

# Hong Kong: IRD Profits Tax e-filing with iXBRL supporting documents

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*

**Load this when:** the filing is a Hong Kong Profits Tax return (BIR51 or
BIR52) e-filed with the Inland Revenue Department (IRD), and the financial
statements or the tax computation must be prepared, tagged, validated or
reviewed as iXBRL data files against the IRD Taxonomy Package (IRD FS, IRD
FS-PE, IRD TC).

**Do not load this when:** the question is a Hong Kong listing or securities
disclosure (no source consulted here describes an HKEX Inline XBRL filing
regime); the question is generic Inline XBRL mechanics (`references/spec.md`,
`references/validation.md`); or it is ESEF (`references/esef.md`).

**Contents**

- [Start here: what the IRD regime is](#start-here-what-the-ird-regime-is)
- [Vintage and applicability](#vintage-and-applicability)
  - [DTS and vintages](#dts-and-vintages)
- [Profile: IRD Profits Tax return with iXBRL supporting documents](#profile-ird-profits-tax)
  - [Mandate: who must e-file, and from which year of assessment](#mandate-who-must-e-file-and-from-which-year-of-assessment)
  - [What is filed in iXBRL and what is not](#what-is-filed-in-ixbrl-and-what-is-not)
  - [Data file rules from the IRD iXBRL Style Guide](#data-file-rules-from-the-ird-ixbrl-style-guide)
  - [Minimum tagging and the List of Mandatory Items](#minimum-tagging-and-the-list-of-mandatory-items)
  - [IRD iXBRL Data Preparation Tools](#ird-ixbrl-data-preparation-tools)
- [Validation](#validation)
- [Filing channel](#filing-channel)
- [Relation to HKEX listing](#relation-to-hkex-listing)
- [Review workflow](#review-workflow)
- [Coverage and known limitations](#coverage-and-known-limitations)
- [Sources](#sources)

## Start here: what the IRD regime is

| Situation | Profile | Section |
|---|---|---|
| A corporation or business e-files a Profits Tax return (BIR51 corporations, BIR52 persons other than corporations) with its financial statements and tax computation | IRD Profits Tax, iXBRL supporting documents | [Profile: IRD Profits Tax return](#profile-ird-profits-tax) |

Hong Kong has one iXBRL regime, and it is a **tax** regime. The IRD launched
voluntary e-filing of Profits Tax returns with iXBRL supporting documents in
April 2023. The Inland Revenue (Amendment) (Minimum Tax for Multinational
Enterprise Groups) Ordinance 2025 (Ord. No. 21 of 2025, enacted 6 June 2025)
made e-filing **mandatory** for a first phase: entities of in-scope MNE groups,
for years of assessment beginning on or after 1 April 2025 (YA 2025/26
onwards). The IRD states that later phases will move from large businesses to
smaller entities, aiming at full-scale mandatory e-filing; it publishes no
dates or thresholds for those phases on the pages read here.

Three facts shape every IRD file and differ from ESEF or UK practice:

1. **Two data files, one entry point each.** The financial statements and the
   tax computation are separate iXBRL data files; each must reference
   **one and only one** IRD entry point (Style Guide para 9; error
   `553-E-0535` and siblings).
2. **No extension taxonomy.** "Extension Taxonomy is not allowed" (Style Guide
   para 12). If no tag with the same concept exists, the IRD lets the item stay
   untagged.
3. **Two edition clocks.** IRD FS and IRD FS-PE editions are per year of
   assessment; the IRD TC taxonomy applies to all years, and only its **latest**
   edition is accepted (Style Guide para 7; error `553-E-0468`).

## Vintage and applicability

Pin two things before tagging or reviewing:

- **The year of assessment (YA)** selects the IRD FS / FS-PE edition. The
  materials page maps edition to YA: 2022 edition to YA 2022/23, 2023 to
  2023/24, 2024 to 2024/25, 2025 to 2025/26.
- **The latest IRD TC edition** applies to the tax computation for every YA.
  On 2026-10-13 that is the TC in package `2026-04-01`.

**Naming trap.** The package's marketing name and its namespace date differ by
one: `tp:name` "IRD Taxonomy Package 2025" has identifier
`http://xbrl.ird.gov.hk/taxonomy/2026-04-01/fstc` and publication date
2026-04-01, and serves YA 2025/26. Cite the namespace date, not the name.

### DTS and vintages

Vocabulary and column order follow `references/dts.md` § Vocabulary. Verified
2026-10-13 by downloading all four English packages and reading
`META-INF/taxonomyPackage.xml` and `META-INF/catalog.xml` in each. All are
Taxonomy Packages 1.0 (`http://xbrl.org/2016/taxonomy-package`), `tp:version`
"Final", publisher IRD, one top-level folder named after the zip, and a
catalog rewriting `http://xbrl.ird.gov.hk/taxonomy/<date>/` to the package
root. The `xbrl.ird.gov.hk` host did not resolve from this machine on
2026-10-13, so load the package offline; do not expect entry points to
dereference.

| Release | Entry point(s) | Package | Valid time | Accepted at deposit | Status | Source |
|---|---|---|---|---|---|---|
| **`2026-04-01`** ("IRD Taxonomy Package 2025") | `http://xbrl.ird.gov.hk/taxonomy/2026-04-01/ird_fs_entry_point_2026-04-01.xsd`, `ird_fs_pe_entry_point_…`, `ird_tc_entry_point_…`, each also as `-zh-hk` (Traditional Chinese); plus two deprecated-element viewing entry points | `https://www.ird.gov.hk/eng/tax/ixbrl/IRD_Taxonomies_2026-04-01.zip` (200, 4.76 MB, 745 entries); the only English package that ships the `ird_tc` folder | FS / FS-PE: YA 2025/26. TC: all YAs (latest edition) | from 1 Apr 2026 (launch date on the main page); Tools 4.1.0.0 cover it | current | IRD materials page; package manifest |
| `2025-04-01` ("IRD Taxonomy Package 2024") | same eight entry points with `2025-04-01` | `…/IRD_Taxonomies_2025-04-01.zip` (200, 4.54 MB, 717 entries); FS and FS-PE files only, although the manifest still declares the TC entry points | FS / FS-PE: YA 2024/25 | FS / FS-PE for YA 2024/25; its TC is superseded by the latest edition | accepted (FS / FS-PE) | IRD materials page footnote; package manifest |
| `2024-04-01` ("IRD Taxonomy Package 2023") | same eight entry points with `2024-04-01`; the first release with Traditional Chinese entry points | `…/IRD_Taxonomies_2024-04-01.zip` (200, 3.45 MB, 714 entries); FS and FS-PE only | FS / FS-PE: YA 2023/24 | FS / FS-PE for YA 2023/24 | accepted (FS / FS-PE) | IRD materials page; package manifest |
| `2023-04-01` ("IRD Taxonomy Package 2022") | `ird_fs_entry_point_2023-04-01.xsd`, `ird_fs_pe_entry_point_…`, `ird_tc_entry_point_…`; English only | `…/IRD_Taxonomies_2023-04-01.zip` (200, 1.73 MB, 386 entries); FS and FS-PE only, so the declared TC entry point does not resolve inside this zip | FS / FS-PE: YA 2022/23 | FS / FS-PE for YA 2022/23 | accepted (FS / FS-PE) | IRD materials page; package manifest |

"Accepted at deposit" for the older rows is an inference: the IRD lists those
editions "For Year of Assessment" 2022/23 to 2024/25 and its current tools
(4.1.0.0) declare those packages and YAs. No IRD page states a deposit
window per release.

What the packages show (2026-04-01 unless stated):

- **Namespaces.** Full-HKFRS concepts in
  `http://xbrl.ird.gov.hk/taxonomy/2026-04-01/ird_fs` (schema
  `reference/full_hkfrs-cor_2026-04-01.xsd`, 4,970 element declarations), IRD
  additions in `…/ird_fs/new` (332); HKFRS for Private Entities in `…/ird_fs_pe`
  (1,213); tax computation in `…/ird_tc` (`ird_tc/tc_core_2026-04-01.xsd`, 448).
  Namespaces carry the release date, so a concept QName changes every release.
- **Linkbases.** Presentation, definition (dimensions), calculation, label (en
  and zh-hk) and reference linkbases; no Formula linkbase was found. The FS and
  FS-PE taxonomies ship calculation linkbases; the TC entry point references
  presentation, definition, label and reference linkbases only.
- **Sources of content.** The Taxonomy Package Guide (version 3.0, April 2025,
  para 11) says the elements are "obtained, customised and localised" from the
  IFRS Accounting Taxonomy, the HKFRSs including HKFRS for Private Entities, and
  the tax computation requirements. The schemas import no IFRS Foundation
  taxonomy file; the DTS is self-contained apart from XBRL International base
  schemas (instance, XBRL Dimensions, DTR types, LRR roles).
- **Same local name, different files.** `ProfitLossBeforeTax` is declared in
  the FS, FS-PE and TC schemas; the IRD cross-checks the FS and TC values
  (rule `NVAD-E-1390`).

<a id="profile-ird-profits-tax"></a>

## Profile: IRD Profits Tax return with iXBRL supporting documents

### Mandate: who must e-file, and from which year of assessment

The legal mechanism: section 21 of Ord. No. 21 of 2025 substitutes
**section 51AAB** of the Inland Revenue Ordinance (Cap. 112), and section 31
adds Schedules 61 to 65, among them **Schedule 65**. Section 51AAB(1) requires a "specified person" to file a
"specified return" for a "specified year of assessment" "in the form of an
electronic record"; Schedule 65 Part 1 fills those in:

- **Specified person:** a "phase 1 applicable entity".
- **Specified return:** the Profits Tax return for corporations (BIR51) or for
  persons other than corporations (BIR52).
- **Specified YA:** a year of assessment beginning on or after 1 April 2025.

An entity is a phase 1 applicable entity (Schedule 65 Part 2 s 2) when it is a
**Part 4AA entity** of an MNE group (Hong Kong constituent entity, Hong Kong
standalone JV, HK member of a JV group, or Part 4AA stateless constituent
entity) for the group's corresponding fiscal year, **and** the group is an
in-scope MNE group for that fiscal year, or was for an earlier fiscal year
beginning on or after 1 January 2025. In-scope follows the GloBE rules: annual
consolidated revenue of EUR 750 million or more in at least two of the four
preceding fiscal years (IRD BEPS page). **Once in, always in** (Schedule 65
Part 2 s 3): the entity stays mandated for every later YA even if the group
leaves scope.

**Where the iXBRL requirement sits.** The ordinance text mandates an
*electronic record* and does not contain the word iXBRL. The iXBRL format comes
from the IRD's e-filing requirements: the main iXBRL page states that in-scope
entities "are mandated to e-file their Profits Tax returns together with the
supporting documents in the iXBRL format" for YA 2025/26 onwards. Quote it that
way rather than attributing "iXBRL" to the ordinance.

**Paper exceptions** for a phase 1 applicable entity (IRD BEPS page): winding
up or amalgamation; no record in the Business Register; cessation notified;
financial statements covering more than 12 months; a YA 2025/26 return issued
on or before 31 March 2026, or a YA 2026/27 return issued on or before
31 March 2027; and re-filing of a return previously e-filed but found invalid.
Supplementary forms must still be filed electronically.

Entities outside phase 1 may e-file voluntarily with the same iXBRL files. FAQ
19: the IRD grants a further one-month extension on application for returns
filed electronically.

### What is filed in iXBRL and what is not

From *Supporting documents and information to be submitted electronically
together with profits tax returns* (last revised 3 June 2026):

| Entity type | Financial statements | Tax computation |
|---|---|---|
| Hong Kong-incorporated private company | audited financial statements, including the auditor's report, in iXBRL | tax computation with cover page in iXBRL |
| Dormant company (Companies Ordinance s 447 exemption) | not required (encouraged if prepared) | iXBRL TC if one was prepared |
| Non-Hong Kong incorporated company | iXBRL AFS (auditor's report substitutable by a statement where local law requires no audit) | iXBRL TC |
| Hong Kong branch / PE of a foreign company | branch- or PE-level financial statements in iXBRL | iXBRL TC |
| Company listed on the Hong Kong Stock Exchange | trimmed annual report plus company-level statement of financial position and statement of comprehensive income in iXBRL; group-level information not tagged | company-level iXBRL TC |
| Other company preparing consolidated statements | full consolidated AFS plus company-level primary statements in iXBRL; group-level information not tagged | iXBRL TC |
| Joint venture / partnership | financial statements in iXBRL | iXBRL TC |

FAQ 18 confirms: only **company-level** financial statements are tagged.

**PDF instead of iXBRL** (main page, "Exception"): financial statements not
prepared under full HKFRSs, HKFRS for Private Entities or SME-FRF & SME-FRS may
be submitted as PDF, "only ... under exceptional circumstances". IFRS preparers
may tag with the IRD taxonomy because HKFRS is "virtually identical" to IFRS
Accounting Standards; the IRD also welcomes iXBRL files for other non-HKFRS
statements. The **tax computation is always iXBRL**.

Which taxonomy for which document:

| Document | Taxonomy | Edition |
|---|---|---|
| Financial statements, full HKFRSs (and IFRS) | IRD FS (`ird_fs`) | the YA's edition |
| Financial statements, HKFRS for Private Entities or SME-FRF & SME-FRS | IRD FS-PE (`ird_fs_pe`) | the YA's edition |
| Tax computation, schedules and cover page | IRD TC (`ird_tc`) | the latest edition |

The TC data file carries a **cover page** with the BIR51 / BIR52 items not
otherwise in the computation (*A Guide to Cover Page for Tax Computation*,
version 4.0, April 2026).

### Data file rules from the IRD iXBRL Style Guide

The Style Guide (version 3.0, April 2025) names the specifications: Inline XBRL
1.1, Transformation Rules Registry 4 (namespace
`http://www.xbrl.org/inlineXBRL/transformation/2020-02-12`), XBRL 2.1, XBRL
Dimensions 1.0, Units Registry 1.0. Load-bearing rules:

- **schemaRef:** `link:schemaRef/@xlink:href` with the absolute entry-point
  URI, for example
  `http://xbrl.ird.gov.hk/taxonomy/2026-04-01/ird_tc_entry_point_2026-04-01.xsd`;
  exactly one per data file.
- **File:** valid XHTML, extension `.html` or `.xhtml`, UTF-8, no JavaScript,
  Java applets or other scripts; CSS embedded; images Base64 data URIs;
  should not exceed 20 MB.
- **Entity identifier:** scheme `http://www.ird.gov.hk`, value the IRD file
  number.
- **Numbers:** accuracy via `decimals` (not `precision`); at least one
  occurrence of each mandatory numeric item with `decimals="INF"`; negatives
  via `sign="-"` with the brackets outside the `ix:nonFraction`.
- **Hidden facts:** avoid `ix:hidden` for mandatory elements; rule
  `NVAD-E-1360` rejects some hidden tags and asks for the fact on the cover
  page.
- **Units:** monetary facts in HKD, or in the "Currency used" stated in the
  tax computation (`NVAD-E-1370`, `NVAD-E-1430`).
- **Duplicates:** an inconsistent duplicate fact is an error (`NVAD-E-0030`).
- **Software metadata:** the cover page may carry
  `ird_tc:VersionOfProductionSoftware`.

### Minimum tagging and the List of Mandatory Items

Two separate obligations (FAQ 13):

**Minimum tagging requirement**, applied only where the section exists in the
document:

- statement of comprehensive income, profit or loss;
- statement of financial position;
- notes: related party transactions;
- notes: property, plant and equipment;
- main tax computation schedules: items with tax adjustments, the Depreciation
  Allowance / Industrial Building Allowance / Commercial Building Allowance
  schedule, and the detailed profit and loss account.

Inside those sections, an item with no close tag may stay untagged.

**List of Mandatory Items** (version 4.0, April 2026), required even when the
item is absent from the document; absent monetary items are tagged as `0`. For
BIR51 financial statements: `Revenue`, `ProfitLossBeforeTax`, `Equity` (the
first two are not mandatory for consolidated statements trimmed to
entity-level information). For BIR52 financial statements: `Revenue`,
`ProfitLossBeforeTax`. The tax computation lists run to 102 items for BIR51,
starting with `CompanyName`, `IRDFileNumber`, `YearOfAssessment`,
`AccountingPeriodStartDate` and `AccountingPeriodEndDate`.

Tagging tips (IRD page): pick the closest tag across all groups; tagging
comparatives is encouraged but not required "at the initial stage"; when only
a breakdown exists without a total, tag the greatest breakdown value. FAQ 20:
the IRD takes a lenient approach to tag accuracy where the wrong tag does not
understate profits.

### IRD iXBRL Data Preparation Tools

Free, offline desktop tools with two components:

- **Tagging Tool:** imports financial statements in Word (Excel too in the
  English Windows version) and tax computations in Excel, auto-detects and
  auto-tags. It does not check arithmetic (FAQ 9) and does not import PDF
  (FAQ 7).
- **Template Tool:** pre-tagged templates for businesses with gross income not
  exceeding HK$5,000,000; enforced by rules `NVAD-E-1440` / `NVAD-E-1441`.

Current versions on 2026-10-13 (main page version table):

| Tool | Version | Released | Packages | YAs |
|---|---|---|---|---|
| English, Windows | 4.1.0.0 | 21 July 2026 | 2022 to 2025 English | 2022/23 to 2025/26 |
| English, Mac | 4.1.0.0 | 11 August 2026 | 2022 to 2025 English | 2022/23 to 2025/26 |
| Traditional Chinese, Windows and Mac | 3.1.0.0 | 11 August 2026 | 2023 to 2025 Traditional Chinese | 2023/24 to 2025/26 |

Version 4.0.0.0 (English) and 3.0.0.0 (Traditional Chinese), released 1 April
2026, are listed obsolete from 21 July 2026 (English Windows) or 11 August
2026 (the others). The FAQ warns that files made with an obsolete version may
be rejected. Using the tools is optional (FAQ 2).

## Validation

The IRD validates uploaded files "against the XBRL Specifications, the IRD
iXBRL Style Guide, the IRD Taxonomy schema and the List of Mandatory Items".
The *List of Validations and Error Messages* (version 3.0, April 2025) has two
code families:

- **`553-E-` technical:** `0467/0497/0534/0543` entry point invalid or not
  specified; `0468` TC not on the latest IRD TC edition; `0498` TC not on the
  IRD TC taxonomy; `0470/0486/0500` invalid taxonomy version;
  `0535/0536/0544/0552` more than one entry point in a data file. Schema and
  specification failures pass through as error-code patterns `xml.*:*`,
  `html:*`, `xmlSchema:*`, `ix1.1:*`, `xbrl.*:*`, `xbrldie:*`, `utre:*`.
- **`NVAD-E-` custom business rules:** for example `0010` mandatory numeric
  needs one `INF` occurrence; `0020` / `0021` period must match the basis
  period; `0030` inconsistent duplicates; `0040` IRD file number and YA must
  match the return; `0050` missing mandatory item; `0060` BIR52 elements tagged
  on a BIR51 return; `1290`-`1292` financial-statement mandatory items;
  `1300` total assets versus total equity and liabilities; `1340` empty string
  fact; `1360` hidden tag; `1390` profit before tax must agree between FS and
  TC files; `1440` / `1441` Template Tool eligibility.

Before going live, developers can register for the **Trial of iXBRL Test
File** service in the Business Tax Portal (no business account needed): the
same validation is run, results arrive within one working day, and test files
are not linked to any return or kept.

Arelle has no Hong Kong disclosure-system plugin that this file could confirm;
generic XBRL 2.1, Dimensions and Inline XBRL validation with the IRD package
loaded offline is the closest local check, and it does not run the `NVAD-E-`
rules. Not tested here; see `references/validation.md`.

## Filing channel

eTAX: the **Business Tax Portal (BTP)** or the **Tax Representative Portal
(TRP)**. The sequence on the main page: upload via "Uploading of Data Files for
Supplementary Forms and Supporting Documents to Profits Tax Return"; wait for
the validation e-mail; fix offline and re-upload on failure; then "Completion
of Profits Tax Return" and "Submission of Profits Tax Return". The FAQ says
audited paper financial statements must still be prepared as the law requires
(FAQ 1), and signed copies may be requested on review (FAQ 8).

## Relation to HKEX listing

No IRD page read here mentions an HKEX Inline XBRL requirement, and none was
found in a search of HKEX annual-report guidance. The only listing link in the
IRD material is the table in *What is filed in iXBRL and what is not*: a listed
company files a trimmed annual report with company-level primary statements in
iXBRL **to the IRD** for tax. Treat any claim of an HKEX iXBRL mandate as not
verified until an HKEX or SFC source says so.

## Review workflow

1. Confirm the return type (BIR51 / BIR52), the YA, and whether the entity is
   a phase 1 applicable entity or a voluntary filer.
2. Check the FS file references the YA's FS or FS-PE entry point and the TC
   file the latest TC entry point, one each, in the language of the document.
3. Check no extension schema, no script, UTF-8 XHTML, 20 MB or less, entity
   scheme `http://www.ird.gov.hk` with the IRD file number.
4. Walk the List of Mandatory Items, including zero-valued items and at least
   one `INF` occurrence each.
5. Walk the minimum-tagging sections present in the documents.
6. Cross-check profit before tax between the files, currency units, and basis
   period contexts.
7. Run the BTP upload validation (or the trial service) and clear every
   `553-E-` and `NVAD-E-` message.

## Coverage and known limitations

- **Later phases:** the IRD says phases will extend to smaller entities; no
  dates or thresholds were found. Not verified.
- **Deposit windows** for older FS / FS-PE editions are inferred from the
  tools' coverage, not from a stated rule.
- **Error list currency:** the validations list is version 3.0 (April 2025)
  and predates the April 2026 package; codes added since are not verified.
- **User Guide** (version 4.0) and the Traditional Chinese packages were not
  downloaded or read; Chinese-package facts come from the IRD pages only.
- **Element counts** are declaration counts in the schemas, not a statement of
  usable concepts (abstracts and dimension members are included).
- **HKEX:** absence of an HKEX iXBRL mandate rests on not finding one.
- **Arelle:** no Hong Kong plugin confirmed; nothing was run against Arelle.

If a rule version newer than the ones cited here is in force, re-read the IRD
materials page and cite it.

## Sources

All read 2026-10-13; HTTP status in brackets.

**IRD web pages:**

- iXBRL Filing (background, mandate statement, taxonomy summary, tools version
  table, tagging requirements, validation, exception) [200]:
  https://www.ird.gov.hk/eng/tax/bus_ixbrl.htm
- IRD iXBRL materials (package downloads, edition-to-YA map, guide versions)
  [200]: https://www.ird.gov.hk/eng/tax/bus_ixbrl_materials.htm
- FAQ on iXBRL filing [200]: https://www.ird.gov.hk/eng/faq/ixbrl.htm
- Tips for tagging [200]:
  https://www.ird.gov.hk/eng/tax/bus_ixbrl_tagging_tips.htm
- Trial of iXBRL Test File [200]:
  https://www.ird.gov.hk/eng/tax/bus_ixbrl_test_file.htm
- Global minimum tax and HKMTT, including "Mandatory electronic filing of
  profits tax returns" (phase 1 conditions, once-in always-in, paper
  exceptions) [200]: https://www.ird.gov.hk/eng/tax/bus_beps.htm
- Consultation on Profits Tax Filing (2021-2022 consultations, trial run
  19 December 2022 to 18 January 2023) [200]:
  https://www.ird.gov.hk/eng/tax/bus_ixbrl_consultation.htm
- Illustrative examples of mandatory e-filing [200, status only]:
  https://www.ird.gov.hk/eng/tax/beps_efiling_example.htm
- Videos on the tools [200, status only]:
  https://www.ird.gov.hk/eng/tax/bus_ixbrl_videos.htm

**Legislation:**

- Inland Revenue (Amendment) (Minimum Tax for Multinational Enterprise Groups)
  Ordinance 2025, Ord. No. 21 of 2025 (s 21 substituting s 51AAB; Schedule 65)
  [200]: https://www.ird.gov.hk/eng/pdf/es12025292321.pdf

**IRD technical documents:**

- Supporting documents and information to be submitted by e-filers (revised
  3 June 2026) [200]:
  https://www.ird.gov.hk/eng/pdf/supporting_documents_and_information_to_be_submitted_by_e_filers.pdf
- IRD Taxonomy Package Guide, version 3.0, April 2025 [200]:
  https://www.ird.gov.hk/eng/tax/ixbrl/ird_taxonomy_package_guide.pdf
- IRD iXBRL Style Guide, version 3.0, April 2025 [200]:
  https://www.ird.gov.hk/eng/tax/ixbrl/ird_ixbrl_style_guide.pdf
- List of Validations and Error Messages, version 3.0, April 2025 [200]:
  https://www.ird.gov.hk/eng/tax/ixbrl/list_of_validations_and_error_messages.pdf
- List of Mandatory Items, version 4.0, April 2026 [200]:
  https://www.ird.gov.hk/eng/tax/ixbrl/list_of_mandatory_items.pdf
- A Guide to Cover Page for Tax Computation, version 4.0, April 2026 [200]:
  https://www.ird.gov.hk/eng/tax/ixbrl/a_guide_to_cover_page_for_tax_computation.pdf

**Taxonomy packages** (manifests, catalogs and schemas read):

- 2026-04-01 [200]: https://www.ird.gov.hk/eng/tax/ixbrl/IRD_Taxonomies_2026-04-01.zip
- 2025-04-01 [200]: https://www.ird.gov.hk/eng/tax/ixbrl/IRD_Taxonomies_2025-04-01.zip
- 2024-04-01 [200]: https://www.ird.gov.hk/eng/tax/ixbrl/IRD_Taxonomies_2024-04-01.zip
- 2023-04-01 [200]: https://www.ird.gov.hk/eng/tax/ixbrl/IRD_Taxonomies_2023-04-01.zip
- Entry-point host `http://xbrl.ird.gov.hk/` [no response; DNS or connection
  failure from this machine]

**eTAX (status only):**

- Uploading Service [200]: https://www.gov.hk/en/apps/irdpfsuppform.htm
- eTAX Business Tax Portal [200]:
  https://www.gov.hk/en/business/taxes/etax/index.htm
