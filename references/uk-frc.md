# UK FRC Suite — Companies House, HMRC CT600, FCA/UKSEF (and Irish Revenue)

Load this when the regulator is **Companies House** (UK statutory
accounts), **HM Revenue & Customs** (Corporation Tax CT600 accounts +
computations), the **FCA National Storage Mechanism / UKSEF** (UK listed
issuer AFRs), or **Irish Revenue (ROS)** iXBRL Corporation Tax filing —
or when the file binds the FRC taxonomy family (FRS 101 / FRS 102 incl.
FRS 105 / UK IFRS / Charities / UKSEF / Irish Revenue Extension). For a
UK-listed issuer's ESEF-shaped obligation, read `esef.md` for the
tagging mechanics and return here for the UK-specific DTR / NSM /
UKSEF overlay.

Four receivers, **one taxonomy family**: Companies House, HMRC, the FCA
and Irish Revenue all consume the **same FRC taxonomy suites**, but each
layers its own filing rules, packaging, and validation gate on top. Pin
the receiver first — it changes which absences are defects and which
validator applies. The **Charity Commission** is part of the same
cross-regulator FRC programme (the FRC runs the Charities taxonomy on its
behalf), but charitable-company iXBRL accounts still flow through the
**CH and HMRC**
gates — there is no separate Charity Commission iXBRL channel — so it is a
fifth stakeholder, not a fifth iXBRL gate. [see `taxonomies.md` §4]

## 1. First: which receiver, and which FRC suite vintage?

The FRC publishes an **annual taxonomy suite** — the 2022, 2023, 2024,
2025 and 2026 suites. The same accounts content can pass or fail on
identical figures depending on which suite it was prepared against
(concepts are added, removed, and re-shaped every year — see §2.1). So
before reviewing or validating, pin four things:

1. **The receiver** — Companies House, HMRC (CT600 accounts +
   computations), FCA/NSM (listed-issuer AFR), or Irish Revenue (ROS CT).
   Each has a different gate (§8).
2. **The reporting period** — read from `<xbrli:period>`, not today. It
   selects the FRC suite and filing-rules edition.
3. **The accounting framework** — FRS 101 / 102 / 105 / UK-adopted IFRS /
   Charities SORP. Selects the FRC accounts entry point and the mandatory
   items (§5).
4. **The document class** — accounts vs computation. HMRC returns carry
   *both*; the CT computational and DPL taxonomies are separate from the
   FRC accounts taxonomies and owned by HMRC, not the FRC. ["Taxonomies
   accepted by HMRC", GOV.UK]

### Taxonomy ownership split

| Family | Owner | Covers |
|---|---|---|
| FRS 101 / 102 (incl. 105) / UK IFRS / UKSEF / Charities / Irish Revenue Extension accounts taxonomies | **FRC** | Statutory-accounts markup for CH, HMRC accounts, FCA/UKSEF, ROS |
| CT Computational taxonomy (2021 / 2023 / 2024 / 2025 current) | **HMRC** | The tax computation attached to a CT600 |
| Detailed Profit & Loss (DPL) taxonomy | **HMRC** | The detailed P&L, tagged in the accounts **or** the computation, not both (§4) |

The only accepted **non-UK** accounts taxonomy for HMRC is **US GAAP**;
accounts prepared under a standard with no HMRC-supported taxonomy are
filed as PDF. ["Taxonomies accepted by HMRC", GOV.UK; COM60040, HMRC
COTAX Manual]

## 2. Bi-temporal cheatsheet (which rule applied when)

For each rule, ask: *was this in force when this report was prepared?*
Do not apply a 2028 mandate or a 2026-suite concept change to a 2024
filing.

| Rule | Applies from | Source |
|---|---|---|
| HMRC: Company Tax Return online, **accounts + computations both in iXBRL** | Periods ending on/after **1 April 2010** (mandatory since 1 April 2011) | COM60040; "Taxonomies accepted by HMRC" |
| HMRC: Detailed P&L **must** use the DPL taxonomy (in accounts **or** computation, not both — §4) | Periods ending on/after **1 April 2014** | "Guidance for the CT Online Service" |
| CH: `AverageNumberEmployeesDuringPeriod` a compulsory validated field | **13 Oct 2020** | "Using software to file…", GOV.UK |
| CH: **software/iXBRL filing voluntary** (alongside web + paper) until the 2028 mandate | Current regime | Same |
| FCA: onshored TD **ESEF RTS revoked**; requirements relocated into **DTR 4.1.15R–4.1.23G** (unchanged from ESEF; supplemented by **TN/507.2**, July 2025) | **29 July 2023** | FCA page; TN/507.2 |
| FCA/NSM: **ESEF-2024** (Reg (EU) 2025/19) is the generally-accepted taxonomy (ESEF-2022 before) | AFR deadlines **from 30 April 2026** (FY on/after 1 Jan 2025) | TN/507.2 |
| CH accepts **FRC suites 2026 / 2025 / 2024 / 2023 / 2022** (aligned with HMRC) | From **April 2026** | CH XML Gateway Forum, 22 Dec 2025 |
| HMRC's free **CATO** filing service closes | **31 March 2026** | COM60040 |
| CH: **software-only iXBRL accounts mandate** (ECCTA); web + paper accounts routes **close** (§3) | **April 2028** | GOV.UK news 9 June 2026; ICAEW |

The FRC's own version policy: **only two suite versions should be in
use at once — the latest and the penultimate** — to satisfy HMRC full
tagging. ["2026 FRC Taxonomy Suite", FRC]

### 2.1 The 2026 suite changed the audit-report tag set — a converter trap

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
converter hard-coding `NameIndividualAuditor` breaks. **Proposed** for April 2026 (not yet confirmed): for **audited**
charitable-company accounts the Boolean
`CharityAuditCarriedOutInAccordanceWithCharitiesAct2011Truefalse` would
become mandatory, with omission causing rejection — the 22 Dec 2025 CH
forum post states this as a proposal to be "confirmed ... next month";
re-verify against a later CH confirmation before treating omission as a
hard-reject defect. [CH XML Gateway Forum, 22 Dec 2025]

## 3. Companies House — voluntary today, software-only from April 2028

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

> **Honest gap.** The *scope* of mandatory tagging at April 2028 —
> whether it extends beyond the financial statements to
> directors'/strategic reports and (for charitable companies) trustees'
> reports — is **not restated** in the 9 June 2026 announcement or
> current gov.uk guidance. The pre-pause April-2027 plan trailed broader
> scope, but it is **not confirmed for 2028**. [GOV.UK news; "Using
> software to file your company's information"]

## 4. HMRC CT600 — iXBRL accounts + computations, full tagging, DPL, long periods

Since **1 April 2011** all Company Tax Returns for accounting periods
ending on/after 1 April 2010 must be filed online via CT Online Services,
with the **accounts and computations both in iXBRL**. The return
comprises form CT600, supplementary pages, accounts, computations, and
any elections. [COM60040; "Taxonomies accepted by HMRC"]

**Full tagging, not minimum tagging.** HMRC requires *full* tagging: "The
accounts and computations must be fully tagged because the taxonomy used
contains appropriate XBRL tags." The FRC taxonomies carry **no separate
minimum-tagging list** for HMRC. ["Taxonomies accepted by HMRC"]

**PDF fallbacks / exceptions** (COM60040): unincorporated charities /
clubs / societies may file **accounts** in iXBRL *or* PDF (return still
online, any computation iXBRL); smaller-charity accounts (combined income
≤ **£6.5m**) may be PDF; accounts under a standard with **no
HMRC-supported taxonomy** go as PDF; the **group accounts** of group
companies need not be iXBRL-tagged.

### 4.1 Long periods of account — separate computations, cross-document match

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

### 4.2 Detailed Profit & Loss (DPL)

For APs ending on/after 1 April 2014, any Detailed P&L — whether it
appears in the accounts or in the computation — **must** be tagged with
the **DPL taxonomy**. HMRC expects the DPL to be tagged in **either the
computations or the accounts, not both**; double-tagging is accepted at
the front end but invites compliance scrutiny. ["Guidance for the CT
Online Service"]

> **Honest gap.** The stronger DPL claims sometimes cited — "DPL is the
> *sole* source for Detailed P&L tags"; "no minimum-tagging subset, the
> whole DPL taxonomy is within the minimum requirement" — come from an
> unfetched search highlight of the DPL user guide. Fetched HMRC docs
> confirm only the DPL dates and the accounts-OR-computation rule. Fetch
> the DPL user guide before asserting the stronger wording.

### 4.3 CT technical mechanics and taxonomy-version enforcement

iXBRL instances are inserted into the CT600 XML package, an **IRmark** is
calculated over the package, and it is posted over HTTP; testing is via
the **Third Party Validation Service (TPVS)** and **External Test Service
(ETS)**. iXBRL 1.1 is supported. ["CT Online XBRL Technical Pack v2.0",
HMRC]

Taxonomy-version rejection codes at the HMRC gateway:

| Error | Trigger | Source |
|---|---|---|
| **3318 / 3320** | A **non-backward-compatible** taxonomy used for the wrong AP | "CT Online XBRL Technical Pack v2.0" |
| **3317** | Filing accounts with an **outdated FRC/US-GAAP taxonomy** (e.g. FRC 2022 for a 2025 period) — "appears to be an error in the Taxonomy reference" | "Taxonomies accepted by HMRC" |
| **1606 / 1607** | Accounts / computation content does not match the CT600 (§4.1) | "Guidance for the CT Online Service" |

> **Honest gap.** Error **3317**'s exact wording is corroborated via a
> search highlight of the gov.uk taxonomies-accepted page and secondary
> vendor pages, but was **not captured** in the fetched sub-page body —
> treat as corroborated-not-fully-fetched. **3318/3320** and **1606/1607**
> are directly supported by fetched Tier-1 evidence.

## 5. Filer classification — what changes which absences are defects

Two classifiers drive the mandatory-item and audit-concept logic: the
**accounting framework** and the **audit / regime status**. Both are
detected from the instance, not assumed.

| Framework | FRC entry point | Notes |
|---|---|---|
| FRS 105 (micro-entities) | FRS 102 suite (105 within) | Reduced disclosure; still fully tagged |
| FRS 102 (incl. Section 1A small) | FRS 102 | Common small/medium UK GAAP path |
| FRS 101 | FRS 101 | Reduced-disclosure IFRS-based |
| UK-adopted IFRS | UK IFRS | Listed + voluntary IFRS adopters |
| Charities (FRS 102 SORP) | Charities | Adds charity registration + audit Boolean (§2.1) |

Status classifiers the validator branches on: **audited vs audit-exempt**
(with/without accountants' report), **dormant**, **micro-entity**,
**abridged/abbreviated**, **small vs medium regime**, **group vs
single**, **LLP vs company**, plus a separate **charity** path. [Arelle
`validate/UK` — see §8]

Mandatory items (implementation evidence, Arelle `validate/UK`;
authoritative source is the Joint Filing Common Validation Checks — §8):

- **Common (all frameworks):** `AverageNumberEmployeesDuringPeriod`,
  `EntityCurrentLegalOrRegisteredName`,
  `StartDateForPeriodCoveredByReport`,
  `EndDateForPeriodCoveredByReport`, `BalanceSheetDate`.
- **FRS adds:** `DateAuthorisationFinancialStatementsForIssue`,
  `DirectorSigningFinancialStatements`, `EntityDormantTruefalse`,
  `EntityTradingStatus`, `AccountingStandardsApplied`,
  `AccountsStatusAuditedOrUnaudited`, `LegalFormEntity`,
  `DescriptionPrincipalActivities`, plus `AccountsType` (FRS-2022) /
  `AccountsTypeFullOrAbbreviated` (pre-2022).
- A `companieshouse.gov.uk` entity scheme makes
  `UKCompaniesHouseRegisteredNumber` mandatory; **charities** need at
  least one of
  `CharityRegistrationNumber{EnglandWales, Scotland, NorthernIreland}`.

Audited accounts require `DateAuditorsReport` + `OpinionAuditorsOnEntity`
+ (`NameIndividualAuditor` **OR**
`NameSeniorStatutoryAuditor`+`NameEntityAuditors`) — the disjunction is
what makes the 2026-suite change (§2.1) validator-safe. Charity audits
additionally key off the
`CharityAuditCarriedOutInAccordanceWithCharitiesAct2011Truefalse`
Boolean. [Arelle `validate/UK`]

## 6. FCA / UKSEF / National Storage Mechanism

Under the FCA Disclosure Guidance and Transparency Rules, issuers with
transferable securities on UK regulated markets must **prepare, publish
and file** annual financial reports (AFRs): the **whole AFR in XHTML**,
and where it contains **IFRS consolidated** statements, those tagged in
iXBRL using a "generally accepted taxonomy" — the primary statements
**and** the notes. ["Company annual financial reporting in electronic
format", FCA]

- **Legal home:** the onshored TD ESEF Regulation was **revoked 29 July
  2023**; requirements relocated into **DTR 4.1.15R–4.1.23G**,
  supplemented by Technical Note **TN/507.2** (July 2025); obligations
  **unchanged from ESEF**. [FCA page; TN/507.2]
- **Filing channel:** AFRs filed in the **National Storage Mechanism**
  (DTR 6.2.2R). A PDF alone does **not** satisfy DTR 4.1; the PIP route
  (DTR 6.2.3G) does **not** apply. [FCA page]
- **Exemptions:** public-sector issuers (DTR 4.4.1); debt ≥ **EUR
  100,000** denomination (DTR 4.4.2). **Notes block-tagging** since
  **FY2022** (PS20/14). [FCA page]
- **"Generally accepted taxonomy"** (DTR 4.1.18R / 4.1.8R(2)) = one based
  on an up-to-date IFRS Accounting Taxonomy. **ESEF-2024** (Reg (EU)
  2025/19) is required for AFR deadlines **from 30 April 2026** (FY on/after
  1 Jan 2025); ESEF-2022 before. Outdated/omitted taxonomies are
  **rejected by the NSM**. [TN/507.2]

### 6.1 UKSEF — the optional multi-target document

**UKSEF is optional.** The FRC reissues the latest ESEF taxonomy annually
**alongside** the FRC taxonomies, so a company can prepare a
**multi-target document** — one iXBRL file satisfying *both* the FCA
(ESEF-style IFRS tagging) and Companies House (FRC UK tags). UKSEF
(introduced 2022) lets one filing serve both regulators; NSM switchover
dates are announced each year in the FCA Filing Manual. For AFR tagging
mechanics (anchoring, block tagging, hidden facts, report-package layout)
read `esef.md` — UKSEF inherits the ESEF model. UK overlay: consolidated
**UKSEF** data may use **minimum tagging** where regulations permit;
otherwise accounts are fully tagged. ["2026 FRC Taxonomy Suite";
"Structured Digital Reporting: Insights 2025/26", FRC]

> **Honest gap.** Whether the FRC's promised **UKSEF 2026** guidance
> ("early 2026") is published, and whether it changes the joint FCA + CH
> mandatory-tag list, was **not verified**. The FRC documentation page
> still lists **UKSEF Tagging Guide 2025 v2.1** and **Conformance Suite
> v2.0** (both 12 Mar 2025) as current. [FRC documentation page]

## 7. FRC XBRL Tagging Guide 2026 (v13.0) — the numbered RULEs, and the closed-taxonomy inversion

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
| **4.2.1 / 4.3.1** | Choice of taxonomies; **scope of tagging** — full-tagging: all business data items MUST be tagged if a suitable tag exists |
| **4.4.1–4.10.1** | Choice of tags; significant numeric data; no-tag-available; alternative tags; unique application; multiple occurrences |
| **4.11.1 / 4.11.2** | **Generic** tags |
| **4.13.1** | Use of **analysis items** |
| **4.14.1 / 4.14.2** | Non-standard dimension tags |
| **4.15.1–4.18.1** | "Other…" data; grouping tags; text tagging; free-text comment tags |
| **4.20.1** | **Comparative (prior-period) data MUST be tagged**, including prior-period data with no current-period counterpart |
| **4.21.1 / 4.22.1 / 4.25.1** | **Compulsory tags**; unreported data; distinction of **company vs group** data |
| **5.3.1–5.11.1** | Positive/negative values; accuracy; period context; entity context |

Taxonomy **design** features (Section 3, for reading the DTS): 3.6.2
dimension **default** tags; 3.6.3 **generic** dimension tags (`Director1`,
`Director2`…); 3.6.4 "non-standard"/"further item" tags; 3.6.5 **typed**
dimensions; 3.7 groupings; 3.8 **analysis items** (repeatable line items
defined as components of a section total, on a typed "analysis"
dimension); 2.5 **Welsh** labels; Appendix A is the generic-dimension-tag
catalogue. [XBRL Tagging Guide 2026]

### 7.1 The structural inversion vs ESEF — extensions are discouraged

The most important architectural difference for anyone arriving from ESEF
or SEC work. **The FRC suite is effectively closed:** "The FRC taxonomies
are intended to cover all current tagging requirements for filing of
accounts information to public agencies." Entity-specific line items are
represented **inside the taxonomy** — via **analysis items on typed
dimensions** and **generic/"further-item" dimension tags** — **not** via
ESEF-style extension concepts plus anchoring. Extensions are
**discouraged** (RULE 3.16.1), the inverse of the ESEF norm where they are
expected and anchoring is mandatory. So: do not reach for an extension
when a generic dimension tag or analysis item expresses the line (check
Appendix A first), and there is **no wider/narrower anchoring
obligation** — almost nothing to anchor. [XBRL Tagging Guide 2026]

The 2026 suite (v1.0.0, 18 Nov 2025) contains UK IFRS, FRS 101/102, UKSEF,
Irish, and Charities taxonomies (changelog + Excel mapping files:
red=deletion, green=addition, yellow=change, orange=deprecated). 2026
content changes: UKEB-endorsed IFRS 7 amendments, FRED 85 amendments,
extra revenue-disaggregation dimensions, the audit-report overhaul (§2.1),
an updated SORPS dimension, Charities SORP 2026. Supporting docs (FRC
documentation page): Developer Guide 2026, Accounts Taxonomies Design
2026, UKSEF Tagging Guide 2025 v2.1, UKSEF Conformance Suite v2.0,
Consistency Checks, Yeti Viewer Guide. ["2026 FRC Taxonomy Suite"; FRC
documentation page]

## 8. Validation — how to run each gate

There are **three** UK gates plus the Irish one, and they emit different
codes. Keep straight which is which.

### 8.1 Companies House — the public XBRL Company Accounts Validator

CH runs a public three-stage validator (XBRL v2.1): [CH XBRL Validator
Help]

1. **XML well-formedness + DTS discovery + XML-Schema validation** —
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
rules", and complex (package) accounts must use the CH **zip**
functionality. ["Technical interface specifications for Companies House
software", GOV.UK]

> **Honest gap.** The CH TIS-for-accounts v5.9 rule content was **not
> read** (the file is an ODT, not fetched); only its version/metadata was
> verified. Download the ODT to enumerate the 2026 CH business rules.

### 8.2 HMRC / Companies House — the Joint Filing Common Validation Checks (Arelle `validate/UK`)

Run the bundled wrapper — its `hmrc`/`ukfrc` profiles load the
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

Codes the plugin emits — these establish "**Arelle implements** the
JFCVC / style-guide checks", **not** "the regulator returns this exact
number at the gateway":

| Code | What it flags |
|---|---|
| `JFCVC.3312` (+ `JFCVC.3312.atLeastOne`) | A mandatory concept is missing, or sits on a context whose dates don't align with `Start/EndDateForPeriodCoveredByReport`; the `atLeastOne` variant is the charity registration-number one-of |
| `JFCVC.3314` | Inconsistent **duplicate fact** values (precision-aware) |
| `JFCVC.3315` | A **generic-dimension member** used with no paired name/description item (or that item has no text) — see §9 |
| `JFCVC.3316` | The context entity identifier (scheme `companieshouse.gov.uk`) does not equal the `UKCompaniesHouseRegisteredNumber` fact |
| `HMRC.5.3` | A negative numeric value whose `en` label lacks a bracketed negative term |
| `HMRC.5.4` | `precision` attribute present on a numeric fact — HMRC requires `decimals`, not `precision` |
| `HMRC.SG.4.5` | Insignificant non-zero digits vs the declared `decimals` |
| `HMRC.SG.3.3` | iXBRL root MUST be `{xhtml}html`; no `<script>` elements, no `javascript:` hrefs |
| `HMRC.SG.3.8` | Images MUST be `data:` URIs — gif/jpeg/png only; no external image URLs in `<style>`/`style` |
| `FRC.TG.3.6.1` | A context carries an `xbrli:scenario` element — disallowed; **segment** is the dimensional container. This is the **inverse of ESEF** (Reporting Manual §2.1.3 forbids segment, requires scenario): do not carry an ESEF context shape into a UK FRC filing |

> **Honest gap.** The JFCVC numbering here was read from the **Arelle
> plugin**, not the primary JFCVC PDF (unfetched; the plugin advertises
> **JFCVC v4.0, 2020-06-09** and Style Guide v2.2). The authoritative
> gateway error numbers — **1606/1607/3312/3316/3317/3318/3320** — come
> from the HMRC/CH sources in §4 and §8.1, not the plugin. Obtain the
> current JFCVC PDF and CH TIS v5.9 before treating any emitted code as
> the exact code a live gateway returns.

### 8.3 Irish Revenue (ROS) — a separate disclosure system

Irish Revenue is modelled as a **distinct** disclosure system, not merely
the FRC accounts taxonomy: the installed Arelle release ships a separate
`plugin/validate/ROS` ("Validate ROS" v1.0), registering one disclosure
system whose names string is `ROS (Ireland)|ROS|ros`, validationType
`ROS`, defaultLanguage English, with a `rules/ros.py` module and a
`resources/config.xml`. [Arelle `validate/ROS`]

The FRC 2026 suite ships a separate **"Irish Revenue Taxonomies 2026"**
zip (2.9 MB, 18 Nov 2025). The Irish Revenue Extension "enables electronic
tagging of Irish accounts to support the Irish Revenue Commissioners'
requirement for iXBRL financial statements as part of the Corporation Tax
return", updated in line with the FRC suite; the Tagging Guide 2026 covers
the Republic of Ireland (FRS 101/102/105 and IFRS) in a dedicated Irish
Taxonomy section (2.3). ["2026 FRC Taxonomy Suite"; XBRL Tagging Guide
2026]

> **Honest gap.** Irish Revenue's own iXBRL CT filing rules and phase-in
> thresholds (Revenue eBrief / Tax and Duty Manual) were **not fetched**.
> ROS coverage here rests on the FRC Irish Revenue Extension description,
> the Tagging Guide's ROI scope, and the Arelle ROS plugin. Fetch
> Revenue.ie's iXBRL guidance for the ROI mandate scope and thresholds.

## 9. Generic-dimension pairing — the JFCVC.3315 pattern

A recurring UK-specific defect: a **generic dimension member** is used to
enumerate an officer, subsidiary, segment, or share class, but the
paired **name/description** fact is missing. `JFCVC.3315` flags it. The
machine form of the rule (Arelle `GENERIC_DIMENSION_VALIDATIONS`):

| Generic member(s) | Requires |
|---|---|
| `Director1..40`, `CompanySecretary1..2`, `Trustee1..20`, `PartnerLLP1..20`, `Chairman`, `ChiefExecutive` | `NameEntityOfficer` |
| `Subsidiary1..200` | `NameSubsidiary` |
| `Associate` / `JointVenture` | `NameAssociate` / `NameJointVenture` |
| `ReportableOperatingSegment` / `ProductService` / `MajorCustomer` | `NameIndividualSegment` |
| `OrdinaryShareClass` / `PreferenceShareClass` / `DeferredShareClass` / `OtherShareClass` | `DescriptionShareType` |
| `PensionPlan` | `NameDefinedContributionPlan` \| `NameDefinedBenefitPlan` |

[Arelle `validate/UK`]

**Welsh handling.** A bilingual text-validation table matches the required
Companies-Act statements (s.477/s.480 exemptions, directors'/members'
acknowledgements, small/micro-regime statements) in **English OR Welsh**,
selected by `ReportPrincipalLanguage=Welsh`. Do not flag a missing English
statement when the report is Welsh and the Welsh statement is present.
[Arelle `validate/UK`; Tagging Guide §2.5]

## 10. FRC "Structured Digital Reporting: Insights 2025/26" — design against these

Published 20 May 2026 (review of 30 UK listed companies' 2024/25 digital
annual reports plus market-wide CODEx analysis), the FRC's nine recurring
findings are the failure modes a converter should pre-empt:
["Structured Digital Reporting: Insights 2025/26", FRC]

1. **Inconsistent level of tagging** — one high-level tag where
   nested/multiple tags are required.
2. **Accounting meaning** — tags chosen by label wording not meaning;
   identical figures tagged inconsistently.
3. **Unnecessary custom extensions** where standard tags exist (APMs,
   equity movements, cash-flow) — the §7.1 point in the wild.
4. **Anchoring too broad / conceptually weak** (UKSEF/ESEF side).
5. **EPS scaling errors** (£45 vs 45 pence) — "one of the most common".
6. **Website availability / accessibility** of the SDR.
7. **Validation errors/warnings not investigated / resolved.**
8. **Filing timeliness / NSM publication failures.**
9. **UK-specific mandatory tags applied inconsistently** — omitted, or
   **group tags on parent-only disclosures** (some UKSEF mandatory tags
   are group-level, some parent-only). Counterpart to RULE 4.25.1
   (company vs group, §7): audit each such tag's scope.

## 11. Stakeholders and governance — the UK institutional map

The UK has **no single "SBR" agency** the way the Netherlands has
SBR-Nederland. The closest analogue is the **FRC-authored one-taxonomy-family
programme** run jointly with the two receivers: Companies House and HMRC
operate a **Joint Filing** arrangement (a shared FRC taxonomy plus the Joint
Filing Common Validation Checks, §8.2), so one markup serves both the
statutory-accounts and CT-accounts gates. Who does what:

| Institution | Role | Detail |
|---|---|---|
| **Companies House** (business register / publication organ) | Maintains the statutory register; receives and publishes company accounts | §1, §3, §8.1 |
| **HM Revenue & Customs** (tax authority) | Structured-filing regime: CT600 iXBRL accounts + computations; **owns** the CT computational and DPL taxonomies | §1, §4 |
| **Financial Reporting Council (FRC)** (standards setter + taxonomy author/governance) | Sets UK GAAP (FRS 100–105); authors and governs the **annual** FRC taxonomy suite (latest + penultimate in use at once), published at `frc.org.uk` | §1, §7 |
| **UK Endorsement Board (UKEB)** (IFRS adoption) | Established **26 Mar 2021**; delegated statutory IFRS-adoption functions from **21 May 2021** (SI 2021/609); endorses and adopts IFRS "for use in the UK" — the standards the UK-IFRS taxonomy tags | [SI 2021/609; UKEB] |
| **Financial Conduct Authority (FCA)** (securities regulator / NCA) | DTR + National Storage Mechanism for listed-issuer AFRs; UKSEF | §6 |
| **Bank of England / PRA** (financial-sector overlay) | Prudential returns from banks + insurers in **DPM-based XBRL** (EBA-taxonomy lineage) via the **BEEDS** portal — dimensional XBRL, **not iXBRL** and not the FRC accounts pipeline; the FCA collects its own via **RegData** | [BoE Regulatory reporting] |
| **Charity Commission** (fifth stakeholder) | Registers/regulates charities; charitable-company iXBRL accounts still flow through the CH/HMRC gates, not a separate channel | §1 |

**How they interlock.** FRC authors the taxonomies → CH and HMRC consume them
under Joint Filing → **UKEB** supplies the endorsed-IFRS content the UK-IFRS
taxonomy expresses → **FCA** overlays DTR/NSM (UKSEF reuses the FRC's annual
ESEF reissue, §6.1) → **PRA/Bank of England** runs a **parallel**
prudential-XBRL pipeline that never touches the accounts taxonomies.
Governance note: the planned replacement of the FRC by the **Audit, Reporting
and Governance Authority (ARGA)** was **shelved in January 2026**; the FRC
remains the regulator (to be put on a statutory footing when parliamentary
time allows), so treat "ARGA" in older material as not-yet-existing. [XBRL
International, Feb 2026]

## 12. Relation to EU/ESEF reporting — post-Brexit divergence

The UK is a **third country**; it keeps ESEF's *substance* without the EU
instrument. §6 has the DTR/NSM/UKSEF mechanics — this is the EU-relationship
summary only.

- **Transposition history.** Pre-Brexit the UK transposed the Transparency
  Directive and onshored the ESEF RTS. The **onshored TD ESEF Regulation was
  revoked 29 July 2023**; the obligation relocated *unchanged* into **DTR
  4.1.15R–4.1.23G** (§6). The substance of ESEF survives; the EU instrument
  does not.
- **Coexistence with the national format.** **UKSEF is the bridge** (§6.1): the
  FRC reissues the ESEF taxonomy annually **alongside** the FRC suite, so one
  multi-target iXBRL file satisfies both the FCA (ESEF-style IFRS tagging) and
  Companies House (FRC UK tags). The UK still **tracks EU ESEF taxonomy
  versions** — **ESEF-2024** (Reg (EU) 2025/19) is the FCA "generally accepted
  taxonomy" for AFR deadlines from 30 Apr 2026 (§6).
- **CSRD / ESRS trajectory — divergent.** The UK is **outside CSRD**. Its own
  path is **UK SRS S1/S2**, issued **25 Feb 2026** by DBT (based on the ISSB's
  IFRS S1/S2) for **voluntary** use; the FCA consulted (Jan 2026) on mandating
  UK SRS S2 for listed issuers, phased from 1 Jan 2027. There is **no UK digital
  mark-up mandate for sustainability reporting** — UK iXBRL under DTR 4.1 stays
  **financial-statements-only** (IFRS consolidated, §6). On the EU side,
  **Directive (EU) 2026/470** (Omnibus I, of 24 Feb 2026; in force 18 Mar 2026)
  amends Accounting Directive **Art. 29d** to expressly provide that, **until**
  the mark-up rules are adopted into Delegated Reg (EU) 2019/815, undertakings
  are **not required to mark up** their sustainability reporting — i.e. ESEF
  sustainability tagging is **suspended** EU-side (recital 24). **Net:** neither
  the UK nor the EU currently mandates sustainability-report mark-up — the UK
  has enacted no mandate; the EU has one but suspended it pending the RTS.
  [Directive (EU) 2026/470; UK SRS S1/S2, GOV.UK]

## 13. A pragmatic UK review pass — in order

Each step depends on the prior being clean.

1. **Pin** receiver, period, FRC suite vintage, framework, document class
   (§1). HMRC ⇒ expect *both* accounts and computation, plus DPL (§4).
2. **Classify the filer** (§5): micro/small/medium/large,
   audited/audit-exempt/dormant, company/LLP/charity, single/group —
   this changes which absences are defects.
3. **Run the right gate** (§8): CH accounts → CH validator + JFCVC
   (`validate/UK`, system `hmrc`); HMRC CT → JFCVC + CT technical-pack;
   FCA/UKSEF → `esef.md` NSM checks + the §6 DTR overlay; ROS →
   `validate/ROS`. Capture warnings.
4. **Classify by code prefix.** `JFCVC.*` / `HMRC.*` / `FRC.TG.*` are
   Arelle implementation evidence; `1606/1607/3312/3316/3317/3318/3320`
   are authoritative gateway numbers. Quote the log line verbatim.
5. **Mandatory-item + generic-dimension pass** (§5, §9): compulsory items
   on correctly-dated contexts; every generic member has its paired
   name/description fact.
6. **Audit-concept pass, vintage-aware** (§2.1): under the 2026 suite
   expect `NameSeniorStatutoryAuditor`+`NameEntityAuditors`, not
   `NameIndividualAuditor`; audited charity ⇒ the Charities-Act Boolean.
7. **Context-shape pass** (§8.2): UK FRC uses `xbrli:segment`
   (`FRC.TG.3.6.1` flags scenario) — opposite of ESEF; `precision`
   forbidden (`HMRC.5.4`).
8. **Extension discipline** (§7.1): could a generic dimension tag or
   analysis item carry it instead?
9. **Cross-document pass (HMRC)** (§4.1): long POA →
   `DescriptorEndOfPeriodForWhichReturnRequired` = CT600
   `PeriodCovered/To`; DPL in exactly one of accounts/computation.
10. **Content review**: rendered statements — EPS scaling (§10 finding 5),
    signs, company-vs-group scope (finding 9). See `conversion.md` §10.

## 14. Primary sources

Cite these, with version, before declaring a defect. Do not cite a rule
from memory; the FRC suites and filing rules evolve annually. Each line
notes what the source establishes; section refs point to the detail.

- **CH accounts changes from April 2028 — GOV.UK (9 June 2026)** —
  §2, §3. <https://www.gov.uk/government/news/companies-house-to-bring-in-changes-to-accounts-filing-from-april-2028>
- **Using software to file your company's information — GOV.UK (9 June
  2026)** — voluntary CH software filing; 2028 mandate; §2, §3.
  <https://www.gov.uk/guidance/using-software-to-file-your-companys-information>
- **2026 FRC Taxonomies Update — CH XML Gateway Forum (22 Dec 2025)** —
  accepted suites; 2026 audit-concept changes; charity Boolean; §2.1.
  <https://xmlforum.companieshouse.gov.uk/t/2026-frc-taxonomies-update/1903>
- **Taxonomies accepted by HMRC — GOV.UK** — mandate; full tagging;
  accepted taxonomies; error 3317; §1, §4.
  <https://www.gov.uk/government/publications/taxonomies-accepted-by-hm-revenue-and-customs/taxonomies-accepted-by-hmrc>
- **COM60040 — HMRC COTAX Manual** — online CT since 2011; long-POA; PDF
  exemptions; CATO close; §4. <https://www.gov.uk/hmrc-internal-manuals/cotax-manual/com60040>
- **Guidance for the CT Online Service (HMRC)** — long-POA cross-doc
  match; errors 1606/1607; computation items; DPL; §4.
  <https://assets.publishing.service.gov.uk/media/5a7ee17fe5274a2e87db27dc/additional-guidance.pdf>
- **CT Online XBRL Technical Pack v2.0 — HMRC** — CT600 XML + IRmark;
  TPVS/ETS; 3318/3320; §4.3.
  <https://assets.publishing.service.gov.uk/media/5d84bef7e5274a27c2c6d5aa/CT_Online_XBRL_Technical_Pack_2.0.pdf>
- **Company annual financial reporting in electronic format — FCA** —
  DTR 4.1; NSM; ESEF RTS revoked; exemptions; §6.
  <https://www.fca.org.uk/markets/company-annual-financial-reporting-electronic-format>
- **FCA Technical Note TN/507.2 (July 2025)** — DTR 4.1.15R–4.1.23G;
  ESEF-2024; UKSEF; §6. <https://www.fca.org.uk/publication/primary-market/tn-507-2.pdf>
- **XBRL Tagging Guide – FRC Taxonomies 2026 (v13.0, 18 Nov 2025)** —
  RULE numbering; closed-taxonomy design; §7.
  <https://media.frc.org.uk/documents/XBRL_Tagging_Guide_-_FRC_Taxonomies_2026.pdf>
- **2026 FRC Taxonomy Suite — FRC** — suite contents; version policy;
  Irish Revenue Extension; §1, §2, §7.
  <https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/frc-taxonomies/current-frc-taxonomy-suites/2026-frc-taxonomy-suite/>
- **FRC Taxonomies Documentation and Guidance — FRC** — 2026 doc set;
  UKSEF Guide/Conformance Suite; §6.1, §7.
  <https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/frc-taxonomies/frc-taxonomies-documentation-and-guidance/>
- **Structured Digital Reporting: Insights 2025/26 — FRC (20 May 2026)** —
  nine SDR findings; UKSEF; §10.
  <https://www.frc.org.uk/library/digital-reporting/structured-digital-reporting-insights-202526/>
- **Technical interface specifications for CH software — GOV.UK (1 Apr
  2026)** — TIS accounts v5.9 / general v5.3; §8.1.
  <https://www.gov.uk/government/publications/technical-interface-specifications-for-companies-house-software>
- **XBRL Validator Help — Companies House** — public validator; three-stage
  validation; §8.1. <https://ewf.companieshouse.gov.uk/help/en/stdwf/xbrl_validator.html>
- **CH accounts changes confirmed for April 2028 — ICAEW (9 June 2026)** —
  corroborates the 2028 package; §3.
  <https://www.icaew.com/insights/viewpoints-on-the-news/2026/jun-2026/companies-house-accounts-changes-confirmed-for-april-2028>
- **Arelle `validate/UK` and `validate/ROS` plugins (installed
  arelle-release)** — *implementation evidence* only (Arelle implements
  the JFCVC / style-guide checks; distinct ROS disclosure system). Not
  authoritative rule text: cross-check emitted codes against the JFCVC
  PDF, HMRC CT Style Guide, and CH TIS v5.9; §8.
- **UK Endorsement Board (UKEB) — GOV.UK / UKEB** — UKEB's statutory role
  endorsing/adopting IFRS for UK use; established 26 Mar 2021, statutory
  functions delegated 21 May 2021 (SI 2021/609);
  §11. <https://www.gov.uk/government/groups/uk-endorsement-board-ukeb>
- **Regulatory reporting: banking sector — Bank of England** — PRA prudential
  XBRL (DPM) returns via BEEDS; not iXBRL; §11.
  <https://www.bankofengland.co.uk/prudential-regulation/regulatory-reporting/regulatory-reporting-banking-sector/banks-building-societies-and-investment-firms>
- **UK drops audit reform legislation — XBRL International (Feb 2026)** — ARGA
  shelved Jan 2026; FRC remains the regulator; §11.
  <https://www.xbrl.org/news/uk-drops-audit-reform-legislation/>
- **UK Sustainability Reporting Standards: UK SRS S1 and UK SRS S2 — GOV.UK
  (25 Feb 2026)** — voluntary UK SRS based on ISSB IFRS S1/S2; FCA mandate
  consultation phased from 1 Jan 2027; no mark-up mandate; §12.
  <https://www.gov.uk/government/publications/uk-sustainability-reporting-standards-uk-srs-s1-and-uk-srs-s2>
- **Directive (EU) 2026/470 (Omnibus I, 24 Feb 2026) — EUR-Lex** — amends
  Accounting Directive Art. 29d to suspend sustainability mark-up until Reg
  (EU) 2019/815 is updated (recital 24); §12.
  <https://eur-lex.europa.eu/eli/dir/2026/470/oj/eng>

If the question concerns a receiver, rule version, or code not covered
here — or the April 2028 tagging scope, DPL "sole source" wording, the
JFCVC PDF numbering, UKSEF 2026 guidance, the CH TIS v5.9 rule content,
or Irish Revenue's own thresholds (all flagged as honest gaps above) —
say so and link the primary source. The cost of a wrong citation on a
regulated filing is high.
