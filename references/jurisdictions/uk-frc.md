---
reference_id: uk-frc
jurisdiction: GB
restructured_on: 2026-08-15
profiles:
  - id: companies-house
    section: profile-companies-house
  - id: hmrc-ct600
    section: profile-hmrc-ct600
  - id: fca-uksef
    section: profile-fca-uksef
  - id: irish-revenue-ros
    section: profile-irish-revenue-ros
---

# UK FRC Suite: Companies House, HMRC CT600, FCA/UKSEF (and Irish Revenue)

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*

Load this when the regulator is **Companies House** (UK statutory
accounts), **HM Revenue & Customs** (Corporation Tax CT600 accounts +
computations), the **FCA National Storage Mechanism / UKSEF** (UK listed
issuer AFRs), or **Irish Revenue (ROS)** iXBRL Corporation Tax filing,
or when the file binds the FRC taxonomy family (FRS 101 / FRS 102 incl.
FRS 105 / UK IFRS / Charities / UKSEF / Irish Revenue Extension). For a
UK-listed issuer's ESEF-shaped obligation, read `references/esef.md` for the
tagging mechanics and return here for the UK-specific DTR / NSM /
UKSEF overlay.

## Start here: choose a filing profile

Four receivers, **one taxonomy family**: Companies House, HMRC, the FCA
and Irish Revenue all consume the **same FRC taxonomy suites**, but each
layers its own filing rules, packaging, and validation gate on top. Pin
the receiver first; it changes which absences are defects and which
validator applies. The **Charity Commission** is part of the same
cross-regulator FRC programme (the FRC runs the Charities taxonomy on its
behalf), but charitable-company iXBRL accounts still flow through the
**CH and HMRC** gates (there is no separate Charity Commission iXBRL
channel), so it is a fifth stakeholder, not a fifth iXBRL gate.
[see `references/taxonomies.md` §4]

| Situation | Profile | Section |
|---|---|---|
| Filing UK statutory accounts to the company register in iXBRL | Companies House | [Profile: Companies House](#profile-companies-house) |
| Filing a Company Tax Return: accounts **and** computations | HMRC CT600 | [Profile: HMRC CT600](#profile-hmrc-ct600) |
| Publishing a listed issuer's annual financial report on a UK regulated market | FCA / NSM / UKSEF | [Profile: FCA / UKSEF / NSM](#profile-fca-uksef) |
| Filing an Irish Corporation Tax return with iXBRL financial statements | Irish Revenue (ROS) | [Profile: Irish Revenue (ROS)](#profile-irish-revenue-ros) |

## Vintage and applicability

The FRC publishes an **annual taxonomy suite**: the 2022, 2023, 2024,
2025 and 2026 suites. The same accounts content can pass or fail on
identical figures depending on which suite it was prepared against
(concepts are added, removed, and re-shaped every year; see *The 2026 suite
changed the audit-report tag set*). So before reviewing or validating, pin
four things:

1. **The receiver**: Companies House, HMRC (CT600 accounts +
   computations), FCA/NSM (listed-issuer AFR), or Irish Revenue (ROS CT).
   Each has a different gate (see *Validation*).
2. **The reporting period**: read from `<xbrli:period>`, not today. It
   selects the FRC suite and filing-rules edition.
3. **The accounting framework**: FRS 101 / 102 / 105 / UK-adopted IFRS /
   Charities SORP. Selects the FRC accounts entry point and the mandatory
   items (see *Filer classification*).
4. **The document class**: accounts vs computation. HMRC returns carry
   *both*. The CT computational taxonomy is separate from the FRC
   accounts taxonomies and owned by HMRC, not the FRC. The DPL is an
   HMRC extension, but from the **FRC 2022 suite** it ships inside the
   FRC package under an FRC namespace, as a section of each accounts
   entry point rather than an entry point of its own (see *Detailed
   Profit & Loss (DPL)*). ["Taxonomies accepted by HMRC", GOV.UK; "2022
   FRC Taxonomy Suite" release notes, FRC §4]

### Taxonomy ownership split

| Family | Owner | Covers |
|---|---|---|
| FRS 101 / 102 (incl. 105) / UK IFRS / UKSEF / Charities / Irish Revenue Extension accounts taxonomies | **FRC** | Statutory-accounts markup for CH, HMRC accounts, FCA/UKSEF, ROS |
| CT Computational taxonomy (2021 / 2023 / 2024 / 2025 current) | **HMRC** | The tax computation attached to a CT600 |
| Detailed Profit & Loss (DPL) | **HMRC** extension, published inside the FRC suite (namespace `http://xbrl.frc.org.uk/dpl/…`; standalone through FRC 2021 DPL, a section of each accounts entry point from FRC 2022) | The detailed P&L, tagged in the accounts **or** the computation, not both (see the *HMRC CT600* profile) |

### DTS and vintages

Which suite to load, where it lives, and which receiver accepts it when.
Vocabulary and column order are fixed in `references/dts.md`
§ Vocabulary. Verified 2026-08-21; every entry point below returned 200
that day. The architecture behind the table: each accounts entry point is
a thin shell (two imports, six `linkbaseRef`s) over one shared core,
`https://xbrl.frc.org.uk/fr/<YYYY>-01-01/core/frc-core-<YYYY>-01-01.xsd`,
so an entry point is a **presentation view over one concept set**, not a
distinct concept set. Entry-point URLs are fully regular for every suite
2022 to 2026:

```text
FRS 102        https://xbrl.frc.org.uk/FRS-102/<YYYY>-01-01/FRS-102-<YYYY>-01-01.xsd
FRS 101        https://xbrl.frc.org.uk/FRS-101/<YYYY>-01-01/FRS-101-<YYYY>-01-01.xsd
UK IFRS        https://xbrl.frc.org.uk/IFRS/<YYYY>-01-01/IFRS-<YYYY>-01-01.xsd
FRS 102 UKSEF  https://xbrl.frc.org.uk/FRS-102/<YYYY>-01-01/UKSEF/FRS-102-<YYYY>-01-01.xsd
IFRS UKSEF     https://xbrl.frc.org.uk/IFRS/<YYYY>-01-01/UKSEF/IFRS-<YYYY>-01-01.xsd
DPL standalone https://xbrl.frc.org.uk/dpl/<YYYY>-01-01/dpl-<YYYY>-01-01.xsd   (2023 onward)
```

| Release | Entry point(s) | Package | Valid time | Accepted at deposit | Status | Source |
|---|---|---|---|---|---|---|
| **2026 suite** (`2026-01-01`, v1.0.0, released 18 Nov 2025) | pattern above with `2026` | `https://www.frc.org.uk/documents/8907/FRC-2026-Taxonomy-v1.0.0.zip`; Charities `…/8898/Charities-2026-Taxonomy-v1.0.0.zip`; Irish Revenue `…/8899/Irish-Revenue-2026-Taxonomy-v1.0.0.zip` | FRC Tagging Guide v13.0 section 6.6: "the latest version"; "All reporters may elect to use this 2026 taxonomy suite" | Companies House from ~1 Apr 2026 (XML Gateway Forum, 22 Dec 2025); HMRC: acceptance end "to be advised" | current | FRC 2026 suite page; Tagging Guide v13.0 § 6.6; CH forum; "Taxonomies accepted by HMRC" (updated 17 Apr 2026) |
| **2025 suite** (`2025-01-01`, v1.0.0, released 18 Oct 2024) | pattern with `2025` | 2025 suite ZIP on the FRC 2025 page (7.8 MB) | Tagging Guide section 6.6: "the penultimate version" | CH accepted; HMRC end "to be advised" | accepted | same |
| **2024 suite** (`2024-01-01`, v1.0.0, released 3 Nov 2023) | pattern with `2024` | `https://www.frc.org.uk/documents/6566/FRC-2024-Taxonomy-v1.0.0_GJp67Do.zip`; Charities `…/6567/Charities-2024-Taxonomy-v1.0.0_l5PHCwA.zip` | Tagging Guide section 6.6: "should only be used prior to 1 January 2025" | CH accepted; HMRC: accounting periods ending on or before **31 Mar 2027** | accepted (contrary to the FRC's own use policy) | same |
| **2023 suite** (`2023-01-01`, v1.0.1 hotfix 17 Feb 2023; v1.0.0 21 Oct 2022) | pattern with `2023` | 2023 suite v1.0.1 ZIP on the FRC historical page | Tagging Guide section 6.6: prior to 1 Jan 2025 only | CH accepted; HMRC: periods ending on or before **31 Mar 2026** | accepted at CH; closed at HMRC for later periods | same |
| **2022 suite** (`2022-01-01`, v1.0.0, released 8 Oct 2021) | pattern with `2022` (no standalone DPL: `dpl/2022-01-01/…` returns 403) | 2022 suite ZIP on the FRC historical page | Tagging Guide section 6.6: prior to 1 Jan 2025 only | CH accepted; HMRC: periods ending on or before **31 Mar 2025** | accepted at CH; closed at HMRC | same |
| UKSEF 2021 / 2022 (standalone taxonomies) | `https://xbrl.frc.org.uk/uksef/<YYYY>-01-01/…` for 2021 and 2022 only; 2023 onward return 403 | FRC historical pages | the FCA NSM's generally accepted taxonomies for the AFR deadlines they covered, both windows now expired | FCA NSM table; no longer accepted | retired; from the 2023 suite UKSEF is a multi-target-document *approach* whose FRC entry points import only `frc-core`, not a taxonomy | FCA NSM; FRC design document |

Read the two clocks apart. The Tagging Guide's section 6.6 is a preparation-quality
position (an old suite cannot express new disclosures); the receivers'
tables are the acceptance rule, and they are more permissive. Never turn
that section into a gate prediction. The FRC's own page says it: "The specific
taxonomy versions that preparers can use, including dates for adoption,
are governed by the requirements and guidance of the relevant data
collectors".

Three measured facts about the DTS itself that change how binding works
here (`references/dts.md` § Six DTSs compared): the suite ships **no
calculation linkbase** and states that the label, not the `balance`
attribute, decides sign; the label roles are standard, documentation,
verbose and terse plus the two deprecation roles (no negated, total or
period roles), in English and **Welsh at near-parity**; and three proprietary definition arcroles (`inflow`,
`outflow`, `crossref`) plus 2 356 `targetRole` arcs carry structure a
standard processor ignores.

### Bi-temporal cheatsheet: which rule applied when

For each rule, ask: *was this in force when this report was prepared?*
Do not apply a 2028 mandate or a 2026-suite concept change to a 2024
filing.

| Rule | Applies from | Source |
|---|---|---|
| HMRC: Company Tax Return online, **accounts + computations both in iXBRL** | Periods ending on/after **1 April 2010** (mandatory since 1 April 2011) | COM60040; "Taxonomies accepted by HMRC" |
| HMRC: Detailed P&L **must** use the DPL taxonomy (in accounts **or** computation, not both; see the *HMRC CT600* profile) | Periods ending on/after **1 April 2014** | "Guidance for the CT Online Service" |
| CH: `AverageNumberEmployeesDuringPeriod` a compulsory validated field | **13 Oct 2020** | "Using software to file…", GOV.UK |
| CH: **software/iXBRL filing voluntary** (alongside web + paper) until the 2028 mandate | Current regime | Same |
| FCA: onshored TD **ESEF RTS revoked**; requirements relocated into **DTR 4.1.15R–4.1.23G** (unchanged from ESEF; supplemented by **TN/507.2**, July 2025) | **29 July 2023** | FCA page; TN/507.2 |
| FCA/NSM: **ESEF-2024** (Reg (EU) 2025/19) is the generally-accepted taxonomy (ESEF-2022 before) | AFR deadlines **from 30 April 2026**: the earliest deadline in the DTR 4.1.3R four-month range (FY on/after 1 Jan 2025) | TN/507.2 |
| CH accepts **FRC suites 2026 / 2025 / 2024 / 2023 / 2022** (aligned with HMRC) | From **April 2026** | CH XML Gateway Forum, 22 Dec 2025 |
| HMRC's free **CATO** filing service closes | **31 March 2026** | COM60040 |
| CH: **software-only iXBRL accounts mandate** (ECCTA); web + paper accounts routes **close** (see the *Companies House* profile) | **April 2028** | GOV.UK news 9 June 2026; ICAEW |

The FRC's own version policy: **only two suite versions should be in
use at once (the latest and the penultimate)**, to satisfy HMRC full
tagging. The 2026 suite was released 18 November 2025 and the 2025 suite
on 18 October 2024, and "all reporters may elect to use this 2026
taxonomy suite". This is the FRC's *use* policy, which is a different
question from what Companies House accepts (see the acceptance row
above). ["XBRL Tagging Guide – FRC Taxonomies 2026" v13.0, §6.6
"Taxonomy versioning"]

### The 2026 suite changed the audit-report tag set: a converter trap

The 2026 FRC suite (v1.0.0, 18 Nov 2025), effective at Companies House
with the April 2026 release, **removed** audit concepts including
`NameIndividualAuditor`, "Statement on respective responsibilities of
directors and auditors", "Emphasis of matter statement", and "Name or
location of office performing audit" (the last replaced by granular
address concepts on a countries dimension), and **added** granular ones
(auditors' responsibilities; opinions on other legal/regulatory and
Companies Act matters; going-concern conclusions; emphasis/other-matter
paragraphs). **Consequence:** the auditor's identity can now only be
expressed with `NameSeniorStatutoryAuditor` + `NameEntityAuditors`; a
converter hard-coding `NameIndividualAuditor` breaks. **Proposed** for
April 2026 (not yet confirmed): for **audited** charitable-company
accounts the Boolean
`CharityAuditCarriedOutInAccordanceWithCharitiesAct2011Truefalse` would
become mandatory, with omission causing rejection. The 22 Dec 2025 CH
forum post states this as a proposal to be "confirmed ... next month";
re-verify against a later CH confirmation before treating omission as a
hard-reject defect. [CH XML Gateway Forum, 22 Dec 2025]

### What the 2026 suite ships

The 2026 suite (v1.0.0, 18 Nov 2025) contains UK IFRS, FRS 101/102, UKSEF,
Irish, and Charities taxonomies (changelog + Excel mapping files:
red=deletion, green=addition, yellow=change, orange=deprecated). 2026
content changes: UKEB-endorsed IFRS 7 amendments, FRED 85 amendments,
extra revenue-disaggregation dimensions, the audit-report overhaul (see *The
2026 suite changed the audit-report tag set*), an updated SORPS dimension,
Charities SORP 2026. Supporting docs (FRC
documentation page): Developer Guide 2026, Accounts Taxonomies Design
2026, UKSEF Tagging Guide 2025 v2.1, UKSEF Conformance Suite v2.0,
Consistency Checks, Yeti Viewer Guide. ["2026 FRC Taxonomy Suite"; FRC
documentation page]

<a id="profile-companies-house"></a>

## Profile: Companies House (voluntary today, software-only from April 2028)

Today CH accepts accounts through **web filing, paper, and software
(iXBRL via the CH XML gateway)** in parallel; software filing is
**voluntary**. On **9 June 2026** the government confirmed the ECCTA
accounts-reform package effective **April 2028** (moved from the paused
April-2027 date; 21 months' notice). From April 2028: ["Using software to
file your company's information", GOV.UK; GOV.UK news 9 June 2026; ICAEW]

- **All** UK-registered companies file accounts in **iXBRL via commercial
  software**; CH **web and paper accounts routes close** (web filing
  survives for non-accounts filings).
- Small companies and micro-entities must file a **profit-and-loss
  account**, with an **opt-out from publication** (CH, HMRC, law
  enforcement retain access).
- **Abridged accounts abolished**; **strengthened audit-exemption
  eligibility statement**; **all component parts** filed together;
  **fewer** accounting-reference-period shortenings.
- Per ICAEW: public-register **annotation** for non-compliance with a
  Companies Act 2006 notice; small-company directors'-report requirement
  dropped under Modernising Corporate Reporting.

> **Honest gap.** The *scope* of mandatory tagging at April 2028 is
> **not restated** in the 9 June 2026 announcement or current gov.uk
> guidance: whether it extends beyond the financial statements to
> directors'/strategic reports and (for charitable companies) trustees'
> reports. The pre-pause April-2027 plan trailed broader
> scope, but it is **not confirmed for 2028**. [GOV.UK news; "Using
> software to file your company's information"]

<a id="profile-hmrc-ct600"></a>

## Profile: HMRC CT600 (iXBRL accounts + computations, full tagging, DPL, long periods)

Since **1 April 2011** all Company Tax Returns for accounting periods
ending on/after 1 April 2010 must be filed online via CT Online Services,
with the **accounts and computations both in iXBRL**. The return
comprises form CT600, supplementary pages, accounts, computations, and
any elections. [COM60040; "Taxonomies accepted by HMRC"]

**Full tagging, not minimum tagging.** HMRC requires *full* tagging: "The
accounts and computations must be fully tagged because the taxonomy used
contains appropriate XBRL tags." The FRC taxonomies carry **no separate
minimum-tagging list** for HMRC. ["Taxonomies accepted by HMRC"]

The only accepted **non-UK** accounts taxonomy for HMRC is **US GAAP**;
accounts prepared under a standard with no HMRC-supported taxonomy are
filed as PDF. ["Taxonomies accepted by HMRC", GOV.UK; COM60040, HMRC
COTAX Manual]

**PDF fallbacks / exceptions** (COM60040): unincorporated charities /
clubs / societies may file **accounts** in iXBRL *or* PDF (return still
online, any computation iXBRL); smaller-charity accounts (combined income
≤ **£6.5m**) may be PDF; accounts under a standard with **no
HMRC-supported taxonomy** go as PDF; the **group accounts** of group
companies need not be iXBRL-tagged.

### Long periods of account: separate computations, cross-document match

For a **long period of account**, separate computations must be provided
for **each accounting period** within it. A tax computation is **not
standalone**: `DescriptorEndOfPeriodForWhichReturnRequired` **must match**
the CT600 `PeriodCovered/To`, so the *same* computation cannot be attached
to both returns. A mismatch raises **error 1607** ("Information within the
computations does not match that on the CT600"); the accounts analogue is
**error 1606**. ["Guidance for the CT Online Service"; COM60040]

Mandatory computation items (2013 dimensional computations taxonomy
onward): `CompanyName`, `TaxDistrict`, `TaxReference`,
`PeriodOfAccountStartDate`, `PeriodOfAccountEndDate`,
`StartOfPeriodCoveredByReturn`, `EndOfPeriodCoveredByReturn`. [Same]

### Detailed Profit & Loss (DPL)

For APs ending on/after 1 April 2014, any Detailed P&L, whether it
appears in the accounts or in the computation, **must** be tagged with
the **DPL taxonomy**. HMRC expects the DPL to be tagged in **either the
computations or the accounts, not both**; double-tagging is accepted at
the front end but invites compliance scrutiny. ["Guidance for the CT
Online Service"]

The DPL user guide is explicit on both scope and completeness. **Scope**
(User Guide §2.1): the DPL taxonomies "are only intended for tagging
data in Detailed P&L statements. They should not be used for tagging data in ordinary
statutory accounts or in computations"; "tags applied to statutory
accounts must be sourced from the accounts taxonomies, while tags applied
to Detailed P&L data must be sourced from the DPL taxonomies". That
prohibition governs which *data* a DPL tag may carry, not which document
it sits in: ordinary statutory-accounts facts take accounts-taxonomy
tags and ordinary computation facts take CT computational-taxonomy tags,
while a Detailed P&L attached to the computation still takes DPL tags.
["CT Online XBRL Technical Pack v2.0" §3.3.3] **Sole source** (User
Guide §2.2): the DPL taxonomies "are intended as the sole source of
tags for Detailed P&L accounts", and Detailed P&L data "must not be tagged
using tags in the statutory accounts taxonomies if these tags are not also
available in the DPL taxonomy presentation views"; the "Detailed Profit
and Loss" section in the UK GAAP statutory-accounts taxonomy "must not be
used for tagging Detailed P&L statements". **No minimum-tagging subset**
(User Guide §2.3): Detailed P&L information "must be tagged
comprehensively using the available tags in the DPL taxonomies… There is
no 'minimum tagging' subset of the DPL taxonomies: the whole of the taxonomies should be regarded as
falling within the HMRC minimum tagging requirement." ["Detailed Profit
and Loss XBRL Taxonomies – User Guide", HMRC]

**Vintage caveat.** That guide is dated **18 May 2013** and is written for
the two standalone taxonomies of that era (GAAP DPL and IFRS DPL).
"Taxonomies accepted by HMRC" §1.3 lists standalone DPL section taxonomies
only through **FRC 2021 DPL** (AP end 31 March 2024); from the **FRC 2022
suite** the DPL "has been incorporated as a section within each of the
current entry points, not separately as its own entry point". The guide
itself remains operative: still published on GOV.UK's CT
technical-specifications page (last updated 15 May 2026) and still called
"essential reading for anyone tagging a DPL statement" by CT Online XBRL
Technical Pack v2.0 §2.2. ["2022 FRC Taxonomy Suite" release notes,
FRC §4; "Taxonomies accepted by HMRC"; "CT Online XBRL Technical Pack
v2.0"]

### CT technical mechanics and taxonomy-version enforcement

iXBRL instances are inserted into the CT600 XML package, an **IRmark** is
calculated over the package, and it is posted over HTTP; testing is via
the **Third Party Validation Service (TPVS)** and **External Test Service
(ETS)**. iXBRL 1.1 is supported. ["CT Online XBRL Technical Pack v2.0",
HMRC]

Taxonomy-version rejection codes at the HMRC gateway:

| Error | Trigger | Source |
|---|---|---|
| **3318 / 3320** | A **non-backward-compatible** taxonomy used for the wrong AP | "CT Online XBRL Technical Pack v2.0" |
| **3317** | Filing accounts with an **outdated FRC/US-GAAP taxonomy** (e.g. FRC 2022 for a 2025 period): "appears to be an error in the Taxonomy reference" | "Taxonomies accepted by HMRC" |
| **1606 / 1607** | Accounts / computation content does not match the CT600 (see *Long periods of account*) | "Guidance for the CT Online Service" |

> **Honest gap.** Error **3317**'s exact wording is corroborated via a
> search highlight of the gov.uk taxonomies-accepted page and secondary
> vendor pages, but was **not captured** in the fetched sub-page body.
> Treat as corroborated-not-fully-fetched. **3318/3320** and **1606/1607**
> are directly supported by fetched Tier-1 evidence.

<a id="profile-fca-uksef"></a>

## Profile: FCA / UKSEF / National Storage Mechanism

Under the FCA Disclosure Guidance and Transparency Rules, issuers with
transferable securities on UK regulated markets must **prepare, publish
and file** annual financial reports (AFRs): the **whole AFR in XHTML**,
and where it contains **IFRS consolidated** statements, those tagged in
iXBRL using a "generally accepted taxonomy": the primary statements
**and** the notes. ["Company annual financial reporting in electronic
format", FCA]

- **Legal home:** the onshored TD ESEF Regulation was **revoked 29 July
  2023**; requirements relocated into **DTR 4.1.15R–4.1.23G**,
  supplemented by Technical Note **TN/507.2** (July 2025); obligations
  **unchanged from ESEF**. [FCA page; TN/507.2]
- **Filing channel:** AFRs filed in the **National Storage Mechanism**
  (DTR 6.2.2R). A PDF alone does **not** satisfy DTR 4.1; the PIP route
  (DTR 6.2.3G) does **not** apply. [FCA page]
- **Deadline (the rule behind the dates):** **DTR 4.1.3R** requires an
  issuer to make its annual financial report public "at the latest four
  months after the end of each financial year", with a copy filed in the
  NSM (DTR 6.2.2R). TN/507.2 states the two together: the AFR is to be
  "prepared and made public (with a copy filed in the NSM) within 4 months
  of the financial year end (DTR 4.1.3R)". Its taxonomy table therefore
  shows a **range of possible deadlines**, not a fixed cutover date: the
  "from 30 April 2026" below is the *earliest* deadline in the range for
  financial years starting on or after 1 January 2025, matching the common
  1 January–31 December year; for a financial year starting after
  1 January the deadline falls correspondingly later. [TN/507.2; FCA
  Handbook DTR 4.1.3R]
- **Exemptions:** public-sector issuers (DTR 4.4.1); debt ≥ **EUR
  100,000** denomination (DTR 4.4.2). **Notes block-tagging** since
  **FY2022** (PS20/14). [FCA page]
- **"Generally accepted taxonomy"** (DTR 4.1.18R / 4.1.8R(2)) = one based
  on an up-to-date IFRS Accounting Taxonomy. **ESEF-2024** (Reg (EU)
  2025/19) is required for AFR deadlines **from 30 April 2026** (FY on/after
  1 Jan 2025); ESEF-2022 before. Outdated/omitted taxonomies are
  **rejected by the NSM**. [TN/507.2]

### UKSEF: the optional multi-target document

**UKSEF is optional.** The FRC reissues the latest ESEF taxonomy annually
**alongside** the FRC taxonomies, so a company can prepare a
**multi-target document**: one iXBRL file satisfying *both* the FCA
(ESEF-style IFRS tagging) and Companies House (FRC UK tags). UKSEF
(introduced 2022) lets one filing serve both regulators; NSM switchover
dates are announced each year in the FCA Filing Manual. For AFR tagging
mechanics (anchoring, block tagging, hidden facts, report-package layout)
read `references/esef.md`. UKSEF inherits the ESEF model. UK overlay:
consolidated **UKSEF** data may use **minimum tagging** where regulations
permit; otherwise accounts are fully tagged. ["2026 FRC Taxonomy Suite";
"Structured Digital Reporting: Insights 2025/26", FRC]

> **Honest gap.** Whether the FRC's promised **UKSEF 2026** guidance
> ("early 2026") is published, and whether it changes the joint FCA + CH
> mandatory-tag list, was **not verified**. The FRC documentation page
> still lists **UKSEF Tagging Guide 2025 v2.1** and **Conformance Suite
> v2.0** (both 12 Mar 2025) as current. [FRC documentation page]

<a id="profile-irish-revenue-ros"></a>

## Profile: Irish Revenue (ROS), a separate disclosure system

Irish Revenue is modelled as a **distinct** disclosure system, not merely
the FRC accounts taxonomy: the installed Arelle release ships a separate
`plugin/validate/ROS` ("Validate ROS" v1.0), registering one disclosure
system whose names string is `ROS (Ireland)|ROS|ros`, validationType
`ROS`, defaultLanguage English, with a `rules/ros.py` module and a
`resources/config.xml`. [Arelle `validate/ROS`]

The FRC 2026 suite ships a separate **"Irish Revenue Taxonomy 2026"**
zip (2.9 MB, 18 Nov 2025). The Irish Revenue Extension "enables electronic
tagging of Irish accounts to support the Irish Revenue Commissioners'
requirement for iXBRL financial statements as part of the Corporation Tax
return", updated in line with the FRC suite; the Tagging Guide 2026 covers
the Republic of Ireland (FRS 101/102/105 and IFRS) in a dedicated Irish
Taxonomy section (2.3). ["2026 FRC Taxonomy Suite"; XBRL Tagging Guide
2026]

### The ROI mandate: phases, deferral thresholds, CT1 options, filing window

**Statutory basis.** Section 884 TCA 1997 extends the definition of a
Corporation Tax return to encompass the financial statements; combined
with the existing e-filing legislation, that makes electronic financial
statements part of the return. [Revenue TDM Part 41A-03-01 §1.1]

**Mandate phase-in.** Each phase is gated on **both** a return-filing date
and an accounting-period-end date. Pin both before deciding whether a
given filing was in scope. [Revenue TDM Part 41A-03-01 §2.1]

| From | Phase | Who, and on what accounting periods |
|---|---|---|
| 23 Nov 2012 / 1 Jan 2013 | Voluntary | All CT payers (23 Nov 2012); all income-tax payers (1 Jan 2013) |
| 1 Oct 2013 | **Phase I** | Customers of Large Corporates Division and High Wealth and Financial Services Division (formerly Large Cases Division), **excluding** Section 110 securitisation SPVs; CT returns filed on/after 1 Oct 2013 for APs ending on/after 31 Dec 2012 |
| 1 May 2014 | — | The same LCD/HWFSD population's **Section 110 securitisation SPVs**; returns filed on/after 1 May 2014 for APs ending on/after 31 Jul 2013 |
| 1 Oct 2014 | **Phase II** | All remaining Revenue customers **except** those meeting the deferral criteria; returns filed on/after 1 Oct 2014 for APs ending on/after 31 Dec 2013 |
| "Later phases to be confirmed" | **Phase III** | All CT payers not covered by Phases I and II: **not implemented**; date and scope still undetermined |

So there is **no universal ROI iXBRL mandate** today: Phase III remains
unimplemented, and the manual only notes that the mandate may later extend
to some income-tax filers.

**Phase II deferral criteria: cumulative, not any-of.** A company is
excluded only if it meets **all three**: balance-sheet total (the
aggregate of assets *without* deduction of liabilities) not exceeding
**€4.4m**; turnover not exceeding **€8.8m**; and an average number of
persons employed, per s.317 Companies Act 2014, not exceeding **50**.
These thresholds are **not pro-rated** for a long accounting period.
[Revenue TDM Part 41A-03-01 §2.1]

**CT1 self-classification.** The filer picks one of five options on the
Form CT1: (1) not mandated but electing to file iXBRL; (2) mandated and
not excluded by options 3–5; (3) claiming the three-criteria deferral
exclusion; (4) inactive: no P&L income or expenses and balance-sheet
movement under €500; (5) in liquidation (other than a voluntary
liquidation with net assets). **Options 1 and 2 must file iXBRL**; the
rest complete "Extracts from Accounts" on the CT1 in full. [Revenue TDM
Part 41A-03-01 §3]

**Filing window.** Revenue's current administrative practice permits the
iXBRL financial statements to be filed before, at the same time as, or
**within 3 months after** the CT1 due date. Outside that window the CT1 is
**deemed incomplete**, which can block refunds and repayments and
tax-clearance applications. [Revenue TDM Part 41A-03-01 §2.1.1]

## Jurisdiction-specific invariants

### Filer classification: what changes which absences are defects

Two classifiers drive the mandatory-item and audit-concept logic: the
**accounting framework** and the **audit / regime status**. Both are
detected from the instance, not assumed.

| Framework | FRC entry point | Notes |
|---|---|---|
| FRS 105 (micro-entities) | FRS 102 suite (105 within) | Reduced disclosure; still fully tagged |
| FRS 102 (incl. Section 1A small) | FRS 102 | Common small/medium UK GAAP path |
| FRS 101 | FRS 101 | Reduced-disclosure IFRS-based |
| UK-adopted IFRS | UK IFRS | Listed + voluntary IFRS adopters |
| Charities (FRS 102 SORP) | Charities | Adds charity registration (except Academy Trusts) + audit Boolean (see *The 2026 suite changed the audit-report tag set*) |

Status classifiers the validator branches on: **audited vs audit-exempt**
(with/without accountants' report), **dormant**, **micro-entity**,
**abridged/abbreviated**, **small vs medium regime**, **group vs
single**, **LLP vs company**, plus a separate **charity** path. [Arelle
`validate/UK`; see *Validation*]

Mandatory items are **receiver-specific**, and the two published
instruments do not carry the same list. Split them before declaring an
absence a defect:

- **HMRC (Government Gateway boundary validation): JFCVC v4.4a, error
  3312**, tabulated per taxonomy vintage. For the FRS 2022 / 2023 / 2024 /
  2025 / 2026 taxonomies: `EntityCurrentLegalOrRegisteredName`,
  `StartDateForPeriodCoveredByReport`, `EndDateForPeriodCoveredByReport`,
  `BalanceSheetDate`, `DateAuthorisationFinancialStatementsForIssue`,
  `DirectorSigningFinancialStatements`, `EntityDormantTruefalse`,
  `EntityTradingStatus`, `AccountingStandardsApplied`,
  `AccountsStatusAuditedOrUnaudited`, `AccountsType`, `LegalFormEntity`,
  `DescriptionPrincipalActivities`. The **2021** vintage is identical
  except that the accounts-type concept is
  `AccountsTypeFullOrAbbreviated`, so the `AccountsType` (2022+) /
  `AccountsTypeFullOrAbbreviated` (pre-2022) split holds **for HMRC**. For
  the +2018 … +2026 FRS **Charities** taxonomies the JFCVC marks legal
  form of entity, accounts type and description of principal activities
  "Not Applicable", and for a detected charity submission the rules look
  **only** for the Trustee variants of the three director-related items.
  [JFCVC v4.4a]
- **Companies House (eFiling gateway), TIS for accounts v5.9 (1 April
  2026), "FRS – Mandatory elements":** `UKCompaniesHouseRegisteredNumber`
  (unconditional here), `EntityCurrentLegalOrRegisteredName`,
  `BalanceSheetDate`, `DateAuthorisationFinancialStatementsForIssue`,
  `DirectorSigningFinancialStatements`, `EntityDormantTruefalse`,
  `StartDateForPeriodCoveredByReport`, `EndDateForPeriodCoveredByReport`,
  `EntityTradingStatus` (via `EntityTradingStatusDimension`),
  `AccountsStatusAuditedOrUnaudited` (via `AccountsStatusDimension`),
  `AccountsTypeFullOrAbbreviated` (via `AccountsTypeDimension`),
  `AccountingStandardsApplied` (via `AccountingStandardsDimension`).
  `LegalFormEntity` (via `LegalFormEntityDimension`) is **mandatory only
  for LLP accounts** and must then carry the value
  `LimitedLiabilityPartnershipLLP`; that qualifier attaches to
  `LegalFormEntity` alone, not to `AccountsTypeFullOrAbbreviated`.
  `DescriptionPrincipalActivities` is **not** a CH FRS mandatory element;
  it is mandatory only in the **CIC34** component of a CIC package. TIS
  v5.9 also warns that **dimension defaults must not be reported**: a
  trading entity reports `EntityTradingStatus` *without* the
  `EntityTradingStatusDimension`. [CH TIS for accounts v5.9]
- **Charities at Companies House**: the "Charities – Mandatory elements"
  table is the same core list minus accounts type, legal form and
  principal activities, plus at least one of
  `CharityRegistrationNumber{EnglandWales, Scotland, NorthernIreland}`;
  `AccountsTypeFullOrAbbreviated` is **not** mandatory there, but if
  present must equal `FullAccounts`. **Academy Trusts are the exception
  to the charity number.** They are charitable companies exempt from
  registration with the Charity Commission, with the Department for
  Education as principal regulator, and they report under the Charities
  SORP (FRS 102) using the `AcademyTrust` member of the Legal Form of
  Entity dimension, added to the Charities taxonomy for that purpose.
  With the 2024 suite, TIS v5.9 records that "Companies House filing
  rules have also been amended to allow Academy Trusts to file
  electronically by removing the mandatory Charity number requirement".
  `UKCompaniesHouseRegisteredNumber` still applies. [CH TIS for accounts
  v5.9]
- **Divergences to hold in mind**, since they are the reason the split
  matters. `LegalFormEntity`: always mandatory at HMRC, LLP-only at CH.
  `DescriptionPrincipalActivities`: always mandatory at HMRC, CIC34-only
  at CH. Accounts type: CH TIS v5.9's 2026 table still names
  `AccountsTypeFullOrAbbreviated` where JFCVC v4.4a's 2022–2026 table
  names `AccountsType`. And `AverageNumberEmployeesDuringPeriod` appears
  in **neither** instrument's mandatory-element tables: it is enforced by
  the Arelle `validate/UK` plugin's `COMMON_MANDATORY_ITEMS`, so it fires
  `JFCVC.3312` locally without a matching published gateway rule (GOV.UK's
  "Using software to file…" separately describes it as a compulsory
  validated field from 13 October 2020; see *Vintage and applicability*).
  Treat the plugin list as an implementation **superset**, not a receiver
  requirement. [Arelle `validate/UK`; see *Validation*]
- **The context entity identifier scheme is a conditional trigger, and the
  direction matters.** If **at least one context entity uses the scheme**
  `http://www.companieshouse.gov.uk/`, then
  `UKCompaniesHouseRegisteredNumber` (Company Reference Number) is
  mandatory. JFCVC v4.4a separates this from the rest of the 3312
  mandatory items precisely because it is *conditional*, not universal
  (§ "Validation on identifier scheme"), and its companion **3316** then
  requires that **every** context entity carrying that scheme have an
  identifier value equal to the `UKCompaniesHouseRegisteredNumber` fact.
  The JFCVC does not oblige anyone to *use* the Companies House scheme; it
  conditions on the scheme being used. In practice a company or LLP filing
  to Companies House will use it (and an HMRC CT filing must carry a
  matching CRN; gateway error 1606), so for those filers the fact is
  effectively always required; but an entity that has a CRN yet identifies
  its contexts under another scheme does not trip 3312. [JFCVC v4.4a]

  `http://www.companieshouse.gov.uk/` is the exact value: lowercase
  `http`, `www.`, and the **trailing slash**. The slash
  is part of the attribute value, so a bare domain is a *different
  identifier*, not a lenient spelling of the same one (HMRC, *XBRL
  tagging: context entity identifiers*). The same value serves Companies
  House accounts and HMRC CT600 accounts and computations.

  It is **not the only valid scheme**, and this section should not be read
  as if it were. Unincorporated charities may use
  `http://www.charitycommission.gov.uk/`; mutual societies
  `http://mutuals.fsa.gov.uk/`; certain regulated insurers historically
  `http://www.fsa.gov.uk/`; foreign entities their home-jurisdiction
  scheme; and HMRC's residual scheme is `http://www.hmrc.gov.uk/` with
  the UTR. A charitable *company* still normally uses its CRN as the
  context entity identifier; charity registration is tagged separately.

**When the disclosure itself is absent.** A mandatory tag stays mandatory
even where the underlying disclosure is not in the accounts: "In some
circumstances a Directors' Report, for example, may not be included with
the accounts but the mandatory XBRL tags relating to the Directors' Report
must still be present. In most cases software will prompt this and attach
the tag either against data elsewhere in the accounts, or within a
'hidden' area within the iXBRL file." For
`DescriptionPrincipalActivities` specifically, JFCVC v4.4a directs
preparers to the hidden section and either a preparer-sourced description
or the literal value **"No description of principal activity"** (singular
"activity"); that note is attached to the 2022 / 2023 / 2024 / 2025 / 2026
FRS mandatory-item tables, so scope it to those vintages. For a UK branch
of a non-UK-incorporated company with no director, "in place of a director
you should include the name of the person approving the balance sheet or
the CT600". This is a preparation instruction, not a rule with its own
error code; the failure mode is the ordinary 3312 rejection. ["XBRL guide
for businesses" §4.6, HMRC; JFCVC v4.4a]

Audited accounts require `DateAuditorsReport` plus
`OpinionAuditorsOnEntity` plus (`NameIndividualAuditor` **OR**
`NameSeniorStatutoryAuditor` + `NameEntityAuditors`); the disjunction is
what makes the 2026-suite change (see *The 2026 suite changed the audit-report
tag set*) validator-safe. The disjunction is the validator's, not a choice
offered to the preparer: `NameIndividualAuditor` is absent from the 2026
taxonomies, so a 2026 filing has only the pair, and passing this rule with the
removed concept means the filing is on an earlier suite. Charity audits
additionally key off the
`CharityAuditCarriedOutInAccordanceWithCharitiesAct2011Truefalse`
Boolean. [Arelle `validate/UK`]

### FRC XBRL Tagging Guide 2026 (v13.0): the numbered RULEs, and the closed-taxonomy inversion

The authority for markup is the **"XBRL Tagging Guide – FRC Taxonomies
2026" v13.0**, dated 18 November 2025. It covers FRS 101/102/105,
Charities FRS 102 SORP, and IFRS in the UK and the Republic of Ireland,
and uses RFC 2119 keywords (MUST / MUST NOT / SHOULD / MAY) for its
numbered RULEs. [XBRL Tagging Guide 2026]

Numbered RULEs a converter must implement (section anchors verified from
the guide's contents):

| RULE | Requirement |
|---|---|
| **3.16.1** | **Extensions**: preparers "are not expected to create their own taxonomy extensions"; permitted **only** for data that is material AND not covered by the FRC taxonomies, MUST NOT duplicate/alter FRC tags or be presentational, MUST follow FRC design conventions |
| **4.2.1 / 4.3.1** | Choice of taxonomies; **scope of tagging** (full-tagging): all business data items MUST be tagged if a suitable tag exists |
| **4.4.1–4.10.1** | Choice of tags; significant numeric data; no-tag-available; alternative tags; unique application; multiple occurrences |
| **4.11.1 / 4.11.2** | **Generic** tags |
| **4.13.1** | Use of **analysis items** |
| **4.14.1 / 4.14.2** | Non-standard dimension tags |
| **4.15.1–4.18.1** | "Other…" data; grouping tags; text tagging; free-text comment tags |
| **4.20.1** | **Comparative (prior-period) data MUST be tagged**, including prior-period data with no current-period counterpart |
| **4.21.1 / 4.22.1 / 4.25.1** | **Compulsory tags**; unreported data; distinction of **company vs group** data |
| **5.3.1–5.11.1** | Positive/negative values; accuracy; period context; entity context |

Taxonomy **design** features (Section 3, for reading the DTS): 3.6.1
dimensions, **general description** (not, despite Arelle's code label,
the segment/scenario rule; see *Validation*); 3.6.2
dimension **default** tags; 3.6.3 **generic** dimension tags (`Director1`,
`Director2`…); 3.6.4 "non-standard"/"further item" tags; 3.6.5 **typed**
dimensions; 3.7 groupings; 3.8 **analysis items** (repeatable line items
defined as components of a section total, on a typed "analysis"
dimension); 2.5 **Welsh** labels; Appendix A is the generic-dimension-tag
catalogue. [XBRL Tagging Guide 2026]

### The structural inversion vs ESEF: extensions are discouraged

The most important architectural difference for anyone arriving from ESEF
or SEC work. **The FRC suite is effectively closed:** "The FRC taxonomies
are intended to cover all current tagging requirements for filing of
accounts information to public agencies." Entity-specific line items are
represented **inside the taxonomy**, via **analysis items on typed
dimensions** and **generic/"further-item" dimension tags**, **not** via
ESEF-style extension concepts plus anchoring. Extensions are
**discouraged** (RULE 3.16.1), the inverse of the ESEF norm where they are
expected and anchoring is mandatory. So: do not reach for an extension
when a generic dimension tag or analysis item expresses the line (check
Appendix A first), and there is **no wider/narrower anchoring
obligation**, since there is almost nothing to anchor. [XBRL Tagging
Guide 2026]

### Generic-dimension pairing: the JFCVC.3315 pattern

A recurring UK-specific defect: a **generic dimension member** is used to
enumerate an officer, subsidiary, segment, or share class, but the
paired **name/description** fact is missing. `JFCVC.3315` flags it. The
rule itself is HMRC's, not the plugin's: whenever a listed Generic Domain
Member element name appears in an instance, the corresponding related
name/description tag must also be present, on the same dimension. The
member lists below are the **FRS 2022–2026 (+ FRS Charities)** tables of
HMRC's *Generic dimension validations 4.91a*; those five vintages are
substantively identical, differing only in the `{fr, cd, char}` namespace
year. ["Generic dimension validations 4.91a", HMRC]

| Generic member(s) | Requires |
|---|---|
| `SpecificDiscontinuedOperation1..8`, `SpecificNon-currentAssetsDisposalGroupHeldForSale1..8` | `DescriptionDiscontinuedOperationOrNon-currentAssetsOrDisposalGroupHeldForSale` |
| `Chairman`, `ChiefExecutive`, `ChairmanChiefExecutive`, `SeniorPartnerLimitedLiabilityPartnership`, `CompanySecretary1..2`, `CompanySecretaryDirector1..2`, `Director1..40`, `PartnerLLP1..20` (`EntityOfficersDimension`) | `NameEntityOfficer` |
| `CorporateTrustee1..3`, `DirectorOfCorporateTrustee`, `CustodianTrustee`, `Trustee1..20` (`char` namespace, `EntityOfficersDimension`) | `NameEntityOfficer` |
| `ReportableOperatingSegment1..20`, `ProductService1..12`, `MajorCustomer1..12` | `NameIndividualSegment` |
| `OtherContractType1..2` | `DescriptionOtherContractType` |
| `OtherDurationType1..2` | `DescriptionOtherContractDurationType` |
| `OtherChannelType1..2` | `DescriptionOtherSalesChannelType` |
| `SpecificBusinessCombination1..10` | `NameAcquiredEntity` |
| `ConsumableBiologicalAssetClass1..5`, `BearerBiologicalAssetClass1..5` | `NameOrDescriptionBiologicalAssetClass` |
| `Subsidiary1..200` | `NameSubsidiary` |
| `Associate1..50` | `NameAssociate` |
| `JointVenture1..50` | `NameJointVenture` |
| `UnconsolidatedStructuredEntity1..5` | `NameUnconsolidatedStructuredEntity` |
| `IntermediateParent1..5`, `EntityWithJointControlOrSignificantInfluence1..5`, `OtherGroupMember1..8`, `KeyManagementIndividualGroup1..5`, `CloseFamilyMember1..5`, `EntityControlledByKeyManagementPersonnel1..5`, `OtherRelatedPartyRelationshipType1..2`, `ComponentTotalRelatedParties` | `NameOrDescriptionRelatedPartyIfNotDefinedByAnotherTag` |
| `OrdinaryShareClass1..5`, `PreferenceShareClass1..5`, `DeferredShareClass1..5`, `OtherShareClass1..4` (`EntityShareClassesDimension`) | `DescriptionShareType` |
| `Share-basedArrangement1..8` | `NameShare-basedPaymentArrangement` |
| `Grant1..10` | `NameOrDescriptionGrantUnderShare-basedPaymentArrangement` |
| `PensionPlan1..6`, `Post-employmentMedicalPlan1..2`, `OtherPost-employmentBenefitPlan1..2` | `NameDefinedContributionPlan` \| `NameDefinedBenefitPlan` |

The machine form is Arelle's `GENERIC_DIMENSION_VALIDATIONS`, which agrees
with the instrument bar one range: Arelle allows `OtherShareClass` to 5
where *Generic dimension validations 4.91a* stops at 4. [Arelle
`validate/UK`]

**Welsh handling.** A bilingual text-validation table matches the required
Companies-Act statements (s.477/s.480 exemptions, directors'/members'
acknowledgements, small/micro-regime statements) in **English OR Welsh**,
selected by `ReportPrincipalLanguage=Welsh`. Do not flag a missing English
statement when the report is Welsh and the Welsh statement is present.
[Arelle `validate/UK`; Tagging Guide section 2.5]

## Validation

There are **three** UK gates plus the Irish one, and they emit different
codes. Keep straight which is which.

### Companies House: the public XBRL Company Accounts Validator

CH runs a public three-stage validator (XBRL v2.1): [CH XBRL Validator
Help]

1. **XML well-formedness + DTS discovery + XML-Schema validation**;
   else `MalformedXMLError`, `SchemaValidationError`, `IllegalReference`,
   `UnresolvableReferenceError`.
2. **XBRL v2.1 validation + consistency** against the referenced
   taxonomy.
3. For inline XBRL, a **business-rules** stage confirming the required
   **Companies Act 2006 statements** are present.

The error report gives a code, location, message, and optional spec
excerpt. Public test endpoint
`test-validator.companieshouse.gov.uk/xbrl_validate`; open source at
`github.com/companieshouse/account-validator-web`. [CH XBRL Validator Help]

The **Technical Interface Specification (TIS)** governs the software
gateway: general TIS **v5.3**, **TIS for accounts v5.9** (1 April 2026).
Developers "must read and understand the file structure and the validation
rules". v5.9 is the "2026 taxonomy implementation highlighting changes to
Audit Report requirements and new Charity functionality"; FRS 105
submissions use the **FRS 102 entry point**, and 2026-01-01 entry points
exist for FRS 101, FRS 102, IFRS and Charities. ["Technical interface
specifications for Companies House software", GOV.UK; CH TIS for accounts
v5.9]

**Extensions are not merely discouraged at the CH gateway; they are
unsupported.** TIS v5.9: "Extension taxonomies will only be supported for
the filing of UKSEF accounts." For FRS 101/102/105, full IFRS and
Charities filings to Companies House an extension taxonomy is not accepted
at all, which is stronger than the Tagging Guide's RULE 3.16.1 posture
(see *The structural inversion vs ESEF*). [CH TIS for accounts v5.9]

**Package submissions.** On the XML gateway, for UKSEF and Welsh
submissions the self-contained file (the "Blob") "is no longer a single
iXBRL instance but must be a Base64-encoded zip package"; the file
structures are in TIS Appendix A. The separate browser-route **ZIP Upload
Service** (live January 2025 for UKSEF, April 2025 for the rest) is
**optional** ("Until CH mandates digital filing, using this upload
service is optional"), so package accounts are not obliged to travel that
route. A **100 MB** limit applies on the initial service release. Nine
package types are defined: [CH TIS for accounts v5.9]

- **UKSEF**; **Welsh** (`reports/english/` + `reports/welsh/`).
- **Limited Partnership (LP)**: `general-partner-accounts`,
  `partnership-accounts`.
- **Community Interest Company (CIC)**: `accounts`, `CIC34`.
- **Audit Exempt Subsidiary**: `parent-accounts`, `subsidiary-accounts`,
  `agreement`, `guarantee`.
- **Filing Exempt Subsidiary**: `parent-accounts`, `agreement`,
  `guarantee`.
- **Group Package Accounts s400** (UK-consolidated):
  `consolidated-accounts`, `exempt-parent-accounts`.
- **Group Package Accounts s401** (non-UK-consolidated): the same two
  directories; the consolidated side is checked only for valid iXBRL.
- **Overseas Accounts**: `english-accounts`, optional
  `untranslated-accounts`, optional OSAA01 PDF; not validated against UK
  law.

`parent-accounts` may itself be an FRC iXBRL file **or** a nested UKSEF
zip package. Audit Exempt and Filing Exempt Subsidiary packages replace
the s477 statement with **s479a**
(`StatementThatCompanyEntitledToExemptionFromAuditUnderSection479aCompaniesAct2006RelatingToSmallCompanies`);
AA06 in the taxonomy suite may be tailored for LLAA06. [CH TIS for
accounts v5.9]

**Welsh packages.** `META-INF` carries a `taxonomyPackage.xml` with
minimal information: no entry-point descriptions, since there is no
extension taxonomy to describe; `catalog.xml` may be omitted; there is no
extension-taxonomy directory alongside `META-INF`; and `reports.json`
declares `documentType`
`http://xbrl.org/PWD/2020-12-09/report-package`. The two reports sit in
`reports/english/` and `reports/welsh/` (identical filenames permitted).
Each iXBRL document is validated **independently** under its
language-specific statement rules and either failure rejects the whole
package; if both pass they are cross-compared for the same entity, the
same period, and matching numeric and date content, and a mismatch
rejects the package. Welsh is signalled by `ReportPrincipalLanguage` on
the **Welsh** member of the Languages dimension (typically in the hidden
section); English by omission or by an undimensioned occurrence, English
being the dimension default (which sources the Welsh-handling note under
*Generic-dimension pairing*). [CH TIS for accounts v5.9]

### HMRC / Companies House: the Joint Filing Common Validation Checks (Arelle `validate/UK`)

Run the bundled wrapper: its `hmrc`/`ukfrc` profiles load the
`validate/UK` plugin **and select the `hmrc` disclosure system** (the
plugin gates every JFCVC/HMRC/FRC.TG check behind
`validateDisclosureSystem`, so a run without it validates nothing
UK-specific). Add `--calc c11r` for the round-to-nearest calculation
pass (the wrapper passes extra args through):

```bash
# Bundled wrapper (disclosure system selected by the profile)
scripts/validate_with_arelle.sh <accounts.xhtml-or-zip> hmrc --calc c11r   # or: ukfrc
# Raw Arelle equivalent
arelleCmdLine --plugins validate/UK --disclosureSystem hmrc --calc c11r -f accounts.xhtml --validate
```

**Implementation evidence (not the regulator's rule text).** The installed
Arelle release ships `plugin/validate/UK` ("Validate UK" v4.0, alias
`validate/hmrc`), registering one disclosure system: `UK HMRC (Joint
Filing Validation Checks)|hmrc`, validationType `HMRC`,
`defaultXmlLang="en-UK"`. It cites `xbrl.frc.org.uk`, the JFCVC PDF, and
the HMRC CT Inline XBRL Style Guide; auto-detects the taxonomy family
(charities / ukGAAP / ukIFRS / FRS / FRS-2022) by namespace and
accounts-vs-computation from the computations namespace
`govtalk.gov.uk/uk/fr/tax/uk-hmrc-ct`. [Arelle `validate/UK`]

Codes the plugin emits (these establish "**Arelle implements** the
JFCVC / style-guide checks", **not** "the regulator returns this exact
number at the gateway"):

| Code | What it flags |
|---|---|
| `JFCVC.3312` (+ `JFCVC.3312.atLeastOne`) | A mandatory concept is missing, or sits on a context whose dates don't align with `Start/EndDateForPeriodCoveredByReport`; the `atLeastOne` variant is the charity registration-number one-of |
| `JFCVC.3314` | Inconsistent **duplicate fact** values (precision-aware) |
| `JFCVC.3315` | A **generic-dimension member** used with no paired name/description item (or that item has no text); see *Generic-dimension pairing* |
| `JFCVC.3316` | The context entity identifier (scheme `http://www.companieshouse.gov.uk/`) does not equal the `UKCompaniesHouseRegisteredNumber` fact |
| `HMRC.5.3` | A negative numeric value whose `en` label lacks a bracketed negative term |
| `HMRC.5.4` | `precision` attribute present on a numeric fact; HMRC requires `decimals`, not `precision` |
| `HMRC.SG.4.5` | Insignificant non-zero digits vs the declared `decimals` |
| `HMRC.SG.3.3` | iXBRL root MUST be `{xhtml}html`; no `<script>` elements, no `javascript:` hrefs |
| `HMRC.SG.3.8` | Images MUST be `data:` URIs (gif/jpeg/png only); no external image URLs in `<style>`/`style` |
| `FRC.TG.3.6.1` | A context carries an `xbrli:scenario` element. The rule text is in the **FRC Developer Guide 2026 §4.2.5** ("Primary items and hypercubes"), not the Tagging Guide: "By convention, the 'all' arc is defined using the 'segment' element of context. The scenario element of context is not used. This is purely a matter of technical convention and does not alter the functionality of dimensions." `FRC.TG.3.6.1` is **Arelle's own code label** and its number does not point at the text of the rule: Tagging Guide 2026 §3.6.1 exists but is headed "Dimensions – general description" and the word "scenario" appears nowhere in that guide. The consequence for a filer is concrete rather than declaratory: the FRC hypercubes bind through **segment**, so a scenario-shaped context yields dimensionally invalid facts. This is the **inverse of ESEF** (Reporting Manual section 2.1.3 forbids segment, requires scenario): do not carry an ESEF context shape into a UK FRC filing |

> **Honest gap, narrowed.** The code numbering in this table was read
> from the **Arelle plugin**, which advertises **JFCVC v4.0 (2020-06-09)**
> and Style Guide v2.2. The current instrument is **JFCVC v4.4a** (ODT on
> the GOV.UK CT technical-specifications page; change history "V4.3a to
> V4.4a: FRS 2026 / 2026 FRS Charities taxonomies added"), and it has now
> been read for the 3312 mandatory-item tables, the conditional
> identifier-scheme check and 3316 (see *Filer classification*). What
> remains unverified is whether every code the plugin emits is the exact
> number a live gateway returns: the authoritative gateway numbers
> (**1606/1607/3312/3316/3317/3318/3320**) come from the HMRC/CH sources
> in the *HMRC CT600* profile and *Companies House: the public XBRL
> Company Accounts Validator*, not the plugin. The HMRC CT Inline XBRL
> Style Guide is still unfetched.

## Review workflow

### A pragmatic UK review pass, in order

Each step depends on the prior being clean.

1. **Pin** receiver, period, FRC suite vintage, framework, document class
   (see *Vintage and applicability*). HMRC ⇒ expect *both* accounts and
   computation, plus DPL (see the *HMRC CT600* profile).
2. **Classify the filer** (see *Filer classification*):
   micro/small/medium/large, audited/audit-exempt/dormant,
   company/LLP/charity, single/group. This changes which absences are
   defects.
3. **Run the right gate** (see *Validation*): CH accounts → CH validator +
   JFCVC (`validate/UK`, system `hmrc`); HMRC CT → JFCVC + CT technical-pack;
   FCA/UKSEF → `references/esef.md` NSM checks + the DTR overlay in the
   *FCA / UKSEF / NSM* profile; ROS → `validate/ROS`. Capture warnings.
4. **Classify by code prefix.** `JFCVC.*` / `HMRC.*` / `FRC.TG.*` are
   Arelle implementation evidence; `1606/1607/3312/3316/3317/3318/3320`
   are authoritative gateway numbers. Quote the log line verbatim.
5. **Mandatory-item + generic-dimension pass** (see *Filer classification* and
   *Generic-dimension pairing*): compulsory items on correctly-dated
   contexts; every generic member has its paired name/description fact.
6. **Audit-concept pass, vintage-aware** (see *The 2026 suite changed the
   audit-report tag set*): under the 2026 suite expect
   `NameSeniorStatutoryAuditor`+`NameEntityAuditors`, not
   `NameIndividualAuditor`; audited charity ⇒ the Charities-Act Boolean.
7. **Context-shape pass** (see *HMRC / Companies House: the Joint Filing
   Common Validation Checks*): UK FRC binds dimensions through
   `xbrli:segment` (FRC Developer Guide 2026 §4.2.5; Arelle flags a
   scenario context as `FRC.TG.3.6.1`), opposite of ESEF; `precision`
   forbidden (`HMRC.5.4`).
8. **Extension discipline** (see *The structural inversion vs ESEF*): could a
   generic dimension tag or analysis item carry it instead?
9. **Cross-document pass (HMRC)** (see *Long periods of account*): long POA →
   `DescriptorEndOfPeriodForWhichReturnRequired` = CT600
   `PeriodCovered/To`; DPL in exactly one of accounts/computation.
10. **Content review** of the rendered statements: EPS scaling
    (*FRC "Structured Digital Reporting: Insights 2025/26"*, finding 5),
    signs, company-vs-group scope (finding 9). See
    `references/conversion.md` §10 for the content-level review pass.

### FRC "Structured Digital Reporting: Insights 2025/26" (design against these)

Published 20 May 2026 (review of 30 UK listed companies' 2024/25 digital
annual reports plus market-wide CODEx analysis), the FRC's nine recurring
findings are the failure modes a converter should pre-empt:
["Structured Digital Reporting: Insights 2025/26", FRC]

1. **Inconsistent level of tagging**: one high-level tag where
   nested/multiple tags are required.
2. **Accounting meaning**: tags chosen by label wording not meaning;
   identical figures tagged inconsistently.
3. **Unnecessary custom extensions** where standard tags exist (APMs,
   equity movements, cash-flow): the *structural inversion vs ESEF* point
   in the wild.
4. **Anchoring too broad / conceptually weak** (UKSEF/ESEF side).
5. **EPS scaling errors** (£45 vs 45 pence): "one of the most common".
6. **Website availability / accessibility** of the SDR.
7. **Validation errors/warnings not investigated / resolved.**
8. **Filing timeliness / NSM publication failures.**
9. **UK-specific mandatory tags applied inconsistently**: omitted, or
   **group tags on parent-only disclosures** (some UKSEF mandatory tags
   are group-level, some parent-only). Counterpart to RULE 4.25.1
   (company vs group; see *FRC XBRL Tagging Guide 2026 (v13.0)*): audit each
   such tag's scope.

## Authorities and governance

The UK has **no single "SBR" agency** the way the Netherlands has
SBR-Nederland. The closest analogue is the **FRC-authored one-taxonomy-family
programme** run jointly with the two receivers: Companies House and HMRC
operate a **Joint Filing** arrangement (a shared FRC taxonomy plus the Joint
Filing Common Validation Checks; see *Validation*), so one markup serves both
the statutory-accounts and CT-accounts gates. Who does what:

| Institution | Role | Detail |
|---|---|---|
| **Companies House** (business register / publication organ) | Maintains the statutory register; receives and publishes company accounts | *Start here: choose a filing profile*; the *Companies House* profile; *Companies House: the public XBRL Company Accounts Validator* |
| **HM Revenue & Customs** (tax authority) | Structured-filing regime: CT600 iXBRL accounts + computations; **owns** the CT computational taxonomy and the DPL extension, the latter published inside the FRC suite from FRC 2022 | *Start here: choose a filing profile*; the *HMRC CT600* profile |
| **Financial Reporting Council (FRC)** (standards setter + taxonomy author/governance) | Sets UK GAAP (FRS 100–105); authors and governs the **annual** FRC taxonomy suite (latest + penultimate in use at once), published at `frc.org.uk` | *Start here: choose a filing profile*; *FRC XBRL Tagging Guide 2026 (v13.0)* |
| **UK Endorsement Board (UKEB)** (IFRS adoption) | Established **26 Mar 2021**; delegated statutory IFRS-adoption functions from **21 May 2021** (SI 2021/609); endorses and adopts IFRS "for use in the UK": the standards the UK-IFRS taxonomy tags | [SI 2021/609; UKEB] |
| **Financial Conduct Authority (FCA)** (securities regulator / NCA) | DTR + National Storage Mechanism for listed-issuer AFRs; UKSEF | the *FCA / UKSEF / NSM* profile |
| **Bank of England / PRA** (financial-sector overlay) | Prudential returns from banks + insurers in **DPM-based XBRL** (EBA-taxonomy lineage) via the **BEEDS** portal: dimensional XBRL, **not iXBRL** and not the FRC accounts pipeline; the FCA collects its own via **RegData** | [BoE Regulatory reporting] |
| **Charity Commission** (fifth stakeholder) | Registers/regulates charities; charitable-company iXBRL accounts still flow through the CH/HMRC gates, not a separate channel | *Start here: choose a filing profile* |

**How they interlock.** FRC authors the taxonomies → CH and HMRC consume them
under Joint Filing → **UKEB** supplies the endorsed-IFRS content the UK-IFRS
taxonomy expresses → **FCA** overlays DTR/NSM (UKSEF reuses the FRC's annual
ESEF reissue; see *UKSEF: the optional multi-target document*) →
**PRA/Bank of England** runs a **parallel**
prudential-XBRL pipeline that never touches the accounts taxonomies.
Governance note: the planned replacement of the FRC by the **Audit, Reporting
and Governance Authority (ARGA)** was **shelved in January 2026**; the FRC
remains the regulator (to be put on a statutory footing when parliamentary
time allows), so treat "ARGA" in older material as not-yet-existing. [XBRL
International, Feb 2026]

### Relation to EU/ESEF reporting: post-Brexit divergence

The UK is a **third country**; it keeps ESEF's *substance* without the EU
instrument. The *FCA / UKSEF / NSM* profile has the DTR/NSM/UKSEF
mechanics; this is the EU-relationship summary only.

- **Transposition history.** Pre-Brexit the UK transposed the Transparency
  Directive and onshored the ESEF RTS. The **onshored TD ESEF Regulation was
  revoked 29 July 2023**; the obligation relocated *unchanged* into **DTR
  4.1.15R–4.1.23G** (see the *FCA / UKSEF / NSM* profile). The substance of
  ESEF survives; the EU instrument does not.
- **Coexistence with the national format.** **UKSEF is the bridge** (see
  *UKSEF: the optional multi-target document*): the FRC reissues the ESEF
  taxonomy annually **alongside** the FRC suite, so one
  multi-target iXBRL file satisfies both the FCA (ESEF-style IFRS tagging) and
  Companies House (FRC UK tags). The UK still **tracks EU ESEF taxonomy
  versions**: **ESEF-2024** (Reg (EU) 2025/19) is the FCA "generally accepted
  taxonomy" for AFR deadlines from 30 Apr 2026, the earliest deadline in
  the DTR 4.1.3R four-month range (see the *FCA / UKSEF / NSM* profile).
- **CSRD / ESRS trajectory: divergent.** The UK is **outside CSRD**. Its own
  path is **UK SRS S1/S2**, issued **25 Feb 2026** by DBT (based on the ISSB's
  IFRS S1/S2) for **voluntary** use; the FCA consulted (Jan 2026) on mandating
  UK SRS S2 for listed issuers, phased from 1 Jan 2027. There is **no UK digital
  mark-up mandate for sustainability reporting**; UK iXBRL under DTR 4.1 stays
  **financial-statements-only** (IFRS consolidated; see the
  *FCA / UKSEF / NSM* profile). On the EU side,
  **Directive (EU) 2026/470** (Omnibus I, of 24 Feb 2026; in force 18 Mar 2026)
  amends Accounting Directive **Art. 29d** to expressly provide that, **until**
  the mark-up rules are adopted into Delegated Reg (EU) 2019/815, undertakings
  are **not required to mark up** their sustainability reporting; i.e. ESEF
  sustainability tagging is **suspended** EU-side (recital 24). **Net:** neither
  the UK nor the EU currently mandates sustainability-report mark-up: the UK
  has enacted no mandate; the EU has one but suspended it pending the RTS.
  [Directive (EU) 2026/470; UK SRS S1/S2, GOV.UK]

## Coverage and known limitations

If the question concerns a receiver, rule version, or code not covered
here, say so and link the primary source. The same holds for the April
2028 tagging scope, the UKSEF 2026 guidance, and whether an
Arelle-emitted code is the exact number a live gateway returns (the
honest gaps that remain above). The cost of a wrong citation on a
regulated filing is high.

## Sources

- **HMRC, *XBRL tagging: context entity identifiers***: the identifier
  scheme URL table. Companies Act 2006 entities use
  `http://www.companieshouse.gov.uk/` with the company registration
  number; the protocol, `www.` and trailing slash are part of the value.
  <https://www.gov.uk/government/publications/xbrl-tagging-context-entity-identifiers/xbrl-tagging-context-entity-identifiers>.

Cite these, with version, before declaring a defect. Do not cite a rule
from memory; the FRC suites and filing rules evolve annually. Each line
notes what the source establishes; section refs point to the detail.

- **CH accounts changes from April 2028 (GOV.UK, 9 June 2026)**:
  *Vintage and applicability*; the *Companies House* profile.
  <https://www.gov.uk/government/news/companies-house-to-bring-in-changes-to-accounts-filing-from-april-2028>
- **Using software to file your company's information (GOV.UK, 9 June
  2026)**: voluntary CH software filing; 2028 mandate;
  *Vintage and applicability*; the *Companies House* profile.
  <https://www.gov.uk/guidance/using-software-to-file-your-companys-information>
- **2026 FRC Taxonomies Update (CH XML Gateway Forum, 22 Dec 2025)**:
  accepted suites; 2026 audit-concept changes; charity Boolean;
  *The 2026 suite changed the audit-report tag set*.
  <https://xmlforum.companieshouse.gov.uk/t/2026-frc-taxonomies-update/1903>
- **Taxonomies accepted by HMRC (GOV.UK)**: mandate; full tagging;
  accepted taxonomies; error 3317; *Vintage and applicability*;
  the *HMRC CT600* profile.
  <https://www.gov.uk/government/publications/taxonomies-accepted-by-hm-revenue-and-customs/taxonomies-accepted-by-hmrc>
- **COM60040 (HMRC COTAX Manual)**: online CT since 2011; long-POA; PDF
  exemptions; CATO close; the *HMRC CT600* profile.
  <https://www.gov.uk/hmrc-internal-manuals/cotax-manual/com60040>
- **Guidance for the CT Online Service (HMRC)**: long-POA cross-doc
  match; errors 1606/1607; computation items; DPL; the *HMRC CT600* profile.
  <https://assets.publishing.service.gov.uk/media/5a7ee17fe5274a2e87db27dc/additional-guidance.pdf>
- **CT Online XBRL Technical Pack v2.0 (HMRC)**: CT600 XML + IRmark;
  TPVS/ETS; 3318/3320; *CT technical mechanics and taxonomy-version enforcement*.
  <https://assets.publishing.service.gov.uk/media/5d84bef7e5274a27c2c6d5aa/CT_Online_XBRL_Technical_Pack_2.0.pdf>
- **Company annual financial reporting in electronic format (FCA)**:
  DTR 4.1; NSM; ESEF RTS revoked; exemptions; the *FCA / UKSEF / NSM* profile.
  <https://www.fca.org.uk/markets/company-annual-financial-reporting-electronic-format>
- **FCA Technical Note TN/507.2 (July 2025)**: DTR 4.1.15R–4.1.23G;
  ESEF-2024; UKSEF; the *FCA / UKSEF / NSM* profile.
  <https://www.fca.org.uk/publication/primary-market/tn-507-2.pdf>
- **XBRL Tagging Guide – FRC Taxonomies 2026 (v13.0, 18 Nov 2025)**:
  RULE numbering; closed-taxonomy design; the **version policy** at
  Tagging Guide §6.6 "Taxonomy versioning"; *Vintage and applicability*;
  *FRC XBRL Tagging Guide 2026 (v13.0)*.
  <https://media.frc.org.uk/documents/XBRL_Tagging_Guide_-_FRC_Taxonomies_2026.pdf>
- **2026 UK and Irish digital reporting taxonomies, FRC** (the page
  formerly titled "2026 FRC Taxonomy Suite"; the suite artefact is still
  named "2026 FRC Taxonomy Suite v1.0.0" on its download table, and the
  old URL 301-redirects): suite contents; Irish Revenue Taxonomy 2026;
  *Start here: choose a filing profile*; *Vintage and applicability*;
  *FRC XBRL Tagging Guide 2026 (v13.0)*.
  <https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/frc-taxonomies/current-uk-and-irish-digital-reporting-taxonomies/2026-uk-and-irish-digital-reporting-taxonomies/>
- **UK and Irish digital reporting taxonomies Guide, FRC** (the page
  formerly titled "FRC Taxonomies Documentation and Guidance"; the old URL
  301-redirects): 2026 doc set; UKSEF Guide/Conformance Suite;
  *UKSEF: the optional multi-target document*;
  *FRC XBRL Tagging Guide 2026 (v13.0)*.
  <https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/frc-taxonomies/uk-and-irish-digital-reporting-taxonomies-guide/>
- **Structured Digital Reporting: Insights 2025/26 (FRC, 20 May 2026)**:
  nine SDR findings; UKSEF;
  *FRC "Structured Digital Reporting: Insights 2025/26"*.
  <https://www.frc.org.uk/library/digital-reporting/structured-digital-reporting-insights-202526/>
- **Technical interface specifications for CH software (GOV.UK, 1 Apr
  2026)**, and the attached **TIS for accounts v5.9** ODT (issued
  01/04/2026, status Final): CH mandatory-element tables; UKSEF-only
  extension support; the nine package types and Welsh `META-INF` rules;
  *Filer classification*; *Companies House: the public XBRL Company
  Accounts Validator*.
  <https://www.gov.uk/government/publications/technical-interface-specifications-for-companies-house-software>
- **Joint Filing Common Validation Checks v4.4a (GOV.UK, ODT)**: the
  3312 mandatory-item tables per taxonomy vintage; the conditional
  identifier-scheme check and 3316; the hidden-section note for
  `DescriptionPrincipalActivities`; *Filer classification*; *Validation*.
  <https://assets.publishing.service.gov.uk/media/6a06d6545f39105e0848a2f6/Joint-Filing-Common-Validation-Checks-v4.4a.odt>
- **Generic dimension validations 4.91a (HMRC, ODT)**: the regulator's
  own generic-member / paired-tag tables per taxonomy vintage;
  *Generic-dimension pairing*.
  <https://assets.publishing.service.gov.uk/media/6a06d61ac0cc74b4523e4e71/Generic-Dimension-Validations-4.91a.odt>
- **XBRL guide for businesses (HMRC / GOV.UK, updated 1 April 2026)**:
  §4.6 on mandatory tags for boundary validation, the `ix:hidden` route
  when the disclosure is absent, and the UK-branch no-director case;
  *Filer classification*.
  <https://www.gov.uk/government/publications/xbrl-guide-for-uk-businesses/xbrl-guide-for-uk-businesses>
- **Detailed Profit and Loss XBRL Taxonomies – User Guide (HMRC, 18 May
  2013)**: DPL scope (Guide §2.1), sole source of tags (Guide §2.2), no
  minimum-tagging subset (Guide §2.3); *Detailed Profit & Loss (DPL)*.
  <https://assets.publishing.service.gov.uk/media/5a7f9dc6ed915d74e33f7845/dpl-guide.pdf>
- **Developer Guide 2026 (FRC, v13.0, 18 Nov 2025)**: §4.2.5 "Primary
  items and hypercubes": closed hypercubes, and the segment-not-scenario
  convention that `FRC.TG.3.6.1` actually enforces; *Validation*.
  <https://www.frc.org.uk/documents/8911/Developer_Guide_2026.pdf>
- **2022 FRC Taxonomy Suite release notes §4 (FRC)**: the DPL
  "incorporated as a section within each of the current entry points, not
  separately as its own entry point" from the 2022 suite;
  *Detailed Profit & Loss (DPL)*.
- **Tax and Duty Manual Part 41A-03-01, "Submission of iXBRL Financial
  Statements as part of Corporation Tax Returns" (Irish Revenue, last
  updated July 2026)**: s.884 TCA 1997 basis; the phase table; the three
  cumulative deferral thresholds; CT1 Options 1–5; the 3-month filing
  window; the *Irish Revenue (ROS)* profile.
  <https://www.revenue.ie/en/tax-professionals/tdm/income-tax-capital-gains-tax-corporation-tax/part-41a/41a-03-01.pdf>
- **FCA Handbook DTR 4.1 (FCA)**: DTR 4.1.3R, the four-month AFR
  deadline behind the TN/507.2 dates; the *FCA / UKSEF / NSM* profile.
  <https://www.handbook.fca.org.uk/handbook/DTR/4/1.html>
- **XBRL Validator Help (Companies House)**: public validator; three-stage
  validation; *Companies House: the public XBRL Company Accounts
  Validator*.
  <https://ewf.companieshouse.gov.uk/help/en/stdwf/xbrl_validator.html>
- **CH accounts changes confirmed for April 2028 (ICAEW, 9 June 2026)**:
  corroborates the 2028 package; the *Companies House* profile.
  <https://www.icaew.com/insights/viewpoints-on-the-news/2026/jun-2026/companies-house-accounts-changes-confirmed-for-april-2028>
- **Arelle `validate/UK` and `validate/ROS` plugins (installed
  arelle-release)**: *implementation evidence* only (Arelle implements
  the JFCVC / style-guide checks; distinct ROS disclosure system). Not
  authoritative rule text: cross-check emitted codes against the JFCVC
  PDF, HMRC CT Style Guide, and CH TIS v5.9; *Validation*.
- **UK Endorsement Board (UKEB), GOV.UK / UKEB**: UKEB's statutory role
  endorsing/adopting IFRS for UK use; established 26 Mar 2021, statutory
  functions delegated 21 May 2021 (SI 2021/609);
  *Authorities and governance*.
  <https://www.gov.uk/government/groups/uk-endorsement-board-ukeb>
- **Regulatory reporting: banking sector (Bank of England)**: PRA prudential
  XBRL (DPM) returns via BEEDS; not iXBRL; *Authorities and governance*.
  <https://www.bankofengland.co.uk/prudential-regulation/regulatory-reporting/regulatory-reporting-banking-sector/banks-building-societies-and-investment-firms>
- **UK drops audit reform legislation (XBRL International, Feb 2026)**: ARGA
  shelved Jan 2026; FRC remains the regulator; *Authorities and governance*.
  <https://www.xbrl.org/news/uk-drops-audit-reform-legislation/>
- **UK Sustainability Reporting Standards: UK SRS S1 and UK SRS S2 (GOV.UK,
  25 Feb 2026)**: voluntary UK SRS based on ISSB IFRS S1/S2; FCA mandate
  consultation phased from 1 Jan 2027; no mark-up mandate;
  *Relation to EU/ESEF reporting*.
  <https://www.gov.uk/government/publications/uk-sustainability-reporting-standards-uk-srs-s1-and-uk-srs-s2>
- **Directive (EU) 2026/470 (Omnibus I, 24 Feb 2026), EUR-Lex**: amends
  Accounting Directive Art. 29d to suspend sustainability mark-up until Reg
  (EU) 2019/815 is updated (recital 24); *Relation to EU/ESEF reporting*.
  <https://eur-lex.europa.eu/eli/dir/2026/470/oj/eng>
