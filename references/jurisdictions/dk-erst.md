---
reference_id: dk-erst
jurisdiction: DK
restructured_on: 2026-08-15
profiles:
  - id: arl-arsrapport
    section: profile-arl-arsrapport
  - id: ifrs-esef
    section: profile-ifrs-esef
  - id: dkfin
    section: profile-dkfin
  - id: foreign-branch
    section: profile-foreign-branch
---

# Denmark: Erhvervsstyrelsen (DCCA) årsrapport iXBRL reference

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*

**Last verified (UTC): 2026-10-15.** Every specific claim was re-read against the primary source cited for it; claims no primary source settles are marked as gaps.

**Load this when:** the filing is a Danish årsrapport to Erhvervsstyrelsen, or the codes carry the Fejl / Advis, TH / TR / TM or FR prefixes.

**Do not load this when:** the Danish entity is a listed issuer whose question is the ESEF layer itself (`references/esef.md`).

**Contents**

- [Start here: choose a filing profile](#start-here-choose-a-filing-profile)
- [Vintage and applicability](#vintage-and-applicability)
  - [DTS and vintages](#dts-and-vintages)
- [Profile: ÅRL årsrapport deposited with Erhvervsstyrelsen](#profile-arl-arsrapport)
  - [Who files, to whom, under what law](#who-files-to-whom-under-what-law)
  - [Deadlines](#deadlines)
  - [Channels: Regnskab Basis / Regnskab Special / system-til-system](#channels-regnskab-basis--regnskab-special--system-til-system)
  - [Reporting classes and channel mapping](#reporting-classes-and-channel-mapping)
  - [ÅRL taxonomy architecture, versions, and entry points](#årl-taxonomy-architecture-versions-and-entry-points)
  - [iXBRL format rules: one self-contained XHTML](#ixbrl-format-rules-one-self-contained-xhtml)
  - [Block (clob) tagging vs mandatory detail tagging](#block-clob-tagging-vs-mandatory-detail-tagging)
  - [No filer extensions under ÅRL: widen and disclose](#no-filer-extensions-under-årl-widen-and-disclose)
- [Profile: IFRS filers, dual ÅRL + ESEF tagging](#profile-ifrs-esef)
  - [The stand-alone DK-IFRS taxonomy is phased out](#the-stand-alone-dk-ifrs-taxonomy-is-phased-out)
  - [The reducible structured set](#the-reducible-structured-set)
  - [Extensions are available, and they bar system-til-system](#extensions-are-available-and-they-bar-system-til-system)
  - [Relation to EU / ESEF reporting](#relation-to-eu--esef-reporting)
- [Profile: DKFIN, the Finanstilsynet financial-sector sub-regime](#profile-dkfin)
- [Profile: Foreign-company branch (PDF, not iXBRL)](#profile-foreign-branch)
- [Jurisdiction-specific invariants](#jurisdiction-specific-invariants)
  - [Mandatory structured fields, CVR contexts, and periods](#mandatory-structured-fields-cvr-contexts-and-periods)
  - [Broken / floating fiscal years: the RegisteredReportingPeriod dimension](#broken--floating-fiscal-years-the-registeredreportingperiod-dimension)
  - [Packaging / artifact shape](#packaging--artifact-shape)
- [Validation](#validation)
  - [The ERST Kontroller corpus: the filing-rules authority](#the-erst-kontroller-corpus-the-filing-rules-authority)
  - [How to run it: the Arelle DBA plugin](#how-to-run-it-the-arelle-dba-plugin)
  - [Rule-code reference: FR business rules](#rule-code-reference-fr-business-rules)
- [Review workflow](#review-workflow)
- [Authorities and governance](#authorities-and-governance)
- [Coverage and known limitations](#coverage-and-known-limitations)
- [Sources](#sources)

## Start here: choose a filing profile

| Situation | Profile | Section |
|---|---|---|
| A Danish entity in reporting class A/B/C/D deposits an årsrapport prepared under ÅRL (Danish GAAP), through Regnskab Basis, Regnskab Special, or system-til-system | ÅRL årsrapport | [Profile: ÅRL årsrapport](#profile-arl-arsrapport) |
| The accounts are prepared under EU-endorsed IFRS: one Inline XBRL file carrying both the ÅRL taxonomy and ESMA's ESEF taxonomy | IFRS + ESEF dual tagging | [Profile: IFRS filers](#profile-ifrs-esef) |
| The entity is a bank, mortgage-credit institution, insurer, pension fund, UCITS, or fund manager supervised by Finanstilsynet | DKFIN financial-sector taxonomy | [Profile: DKFIN](#profile-dkfin) |
| A branch of a foreign company deposits the foreign company's report in Denmark | Foreign-company branch (PDF, no XBRL) | [Profile: Foreign-company branch](#profile-foreign-branch) |

This is a jurisdiction working reference, not the legal source. Danish
filing rules are Danish-language regulator publications; every rule id,
version, and threshold below is tied to a source in *Sources*. Where a fact
could not be verified this pass it is marked as an honest gap (*Coverage and known limitations*).
Do not paper over it.

## Vintage and applicability

Danish årsrapport filing has **two independent version axes**, and the
same iXBRL file passes or fails depending on both. Pin them before
reviewing:

1. **The balance date (balancedato).** Read it from the reporting
   period, not from today. The iXBRL mandate itself is triggered by
   balance date, not filing date (see the table below).
2. **The taxonomy generation.** Annual: `20241001`, `20251001`, …
   Selecting the wrong generation changes which concepts, enumerations,
   and controls apply.

| Rule / obligation | Applies from | Notes |
|---|---|---|
| iXBRL (Inline XBRL) mandatory for the årsrapport | Balance date **on/after 2025-01-01** | ERST: "kravet om indberetning i Inline XBRL for årsrapporter med en balancedato fra den 1. januar 2025" [S3]. Do not demand iXBRL of a 2024 balance-date filing. The threshold comes from BEK 1003/2023 § 2 stk. 2 [S13] and [S3]. ERST control `FR83` "Der skal indberettes inlineXBRL" (Fejl) blocks plain-XBRL filing, but names no balance date, and the Kontroller corpus states "Kontrollen er pt. inaktiv" [S2]. |
| ÅRL taxonomy `20251001` | Published Nov 2025; live in ERST PreProd + Prod (announced 2026-01-16) | ERST recommends filing with the 2025 or the previous **2024** taxonomy [S3][S6]. |
| DKFIN (financial-sector) mandatory for entities required to file in Inline XBRL | Financial year **2025** onward | Scope: BEK nr. 917 af 27/06/2025 § 3 stk. 2-6 (listed issuers, sustainability reporters, Taxonomy-Regulation Art. 8 reporters); every other financial-sector entity files a searchable PDF via Regnskab Special (§ 3 stk. 1) [S14]. § 18: applies to financial years beginning 1 January 2025 or later, with §§ 6-9 usable voluntarily already for FY2024 [S14][S5]. |
| Dual ÅRL + ESEF tagging for IFRS filers | Balance date **on/after 2025-01-01** | Introduced by BEK nr. 1003 af 26/06/2023 § 1 nr. 4, which rewrote § 17 of BEK 1054/2021; its § 2 stk. 2 gives nr. 4-6 effect for balance dates on/after 2025-01-01 [S13]. Re-enacted **verbatim** as BEK 859/2025 § 17 stk. 3 [S1]. Note BEK 859/2025 § 35 stk. 2-3 repealed BEK 1054/2021 and gives the current order effect for documents **filed** on/after 2025-07-01, so § 17 stk. 3 as now in force carries no balance-date carve-out of its own. The stand-alone DK-IFRS taxonomy is **phased out** [S3] (see the *IFRS filers* profile). |
| Raised ÅRL § 7 size thresholds | Financial years beginning on/after **2023-01-01** | Raised by lov nr. 480 af 22. maj 2024 § 1 nr. 2-3, with effect under its § 14 stk. 2 [S16]. New DKK limits in *Reporting classes and channel mapping*; measured two-of-three over two consecutive years [S7]. |

State the balance date and taxonomy generation back to the user before
declaring any defect. "This violates ÅRL taxonomy 20251001 control X for
a 2025 balance date" is reviewable; "this is wrong" is not.

### DTS and vintages

Which release to load, where it lives, and what is accepted when.
Vocabulary and column order are fixed in `references/dts.md`
§ Vocabulary. Re-verified 2026-10-15 by downloading and unpacking the
packages; publication dates are read from each package's
`tp:publicationDate`.

**The namespace host is not a download location.** Every `schemaRef`
must begin with `http://archprod.service.eogs.dk/taxonomy/` (control
`TH01`, Fejl), and that host returns 404 for every path. The package's
`META-INF/catalog.xml` rewrites
`http://archprod.service.eogs.dk/taxonomy/20251001/` to the files inside
the zip; load the package, never the URL.

| Release | Entry point(s) | Package | Valid time | Accepted at deposit | Status | Source |
|---|---|---|---|---|---|---|
| **20251001** (`tp:identifier` `http://www.erst.dk/XBRL20251001`, `tp:publicationDate` 2025-11-15) | 24 declared: six DKGAAP filing entry points plus `entryAll.xsd`: `http://archprod.service.eogs.dk/taxonomy/20251001/entryDanishGAAP{BalanceSheetAccountForm,BalanceSheetAccountByCurrentAndLongTermForm}IncomeStatementBy{Nature,Function}IncludingManagementsReviewStatisticsAndTax20251001.xsd`, `…/entryDanishGAAPExcludingBalanceSheetIncomeStatementIncludingManagementsReview20251001.xsd` (the IFRS/ESEF companion), `…/entryDKGAAPRequiredInformation20251001.xsd`, `…/entryAll.xsd` (accession only); eight DFSA / DKFIN `entryDFSA*.xsd`; UVM entry points | `https://erhvervsstyrelsen.dk/sites/default/files/2025-11/XBRL20251001-20251120.zip` | årsrapporter with balance date on or after 2025-01-01 must be Inline XBRL ([S3]; BEK 1003/2023 § 2 stk. 2 [S13]); ERST "anbefaler" (recommends) the 2025 or the 2024 taxonomy | no published acceptance matrix; the package's `frm_injection/` carries ERST's current formula controls for vintages **20201001 to 20251001**, the strongest machine-readable evidence of the window | current, recommended | package manifest; Kontroller corpus; ERST "Taksonomier, aktuelle" |
| **20241001** (`tp:publicationDate` 2024-10-01) | 23 declared; DFSA / DKFIN entry points first appear here | `https://erhvervsstyrelsen.dk/sites/default/files/2024-11/AARL%20taksonomi%E2%80%93version-20241001%20%28zip-fil%29.zip` | FY2024 onward; DKFIN mandatory from FY2025 | recommended alternative to 20251001; in `frm_injection` | accepted, recommended | same |
| **20231001** (2023-10-01) | 14 declared | `https://erhvervsstyrelsen.dk/sites/default/files/2023-11/XBRL20231001_20231108.zip` | FY2023 onward | carried in `frm_injection`; not verified against any ERST statement that receipt validation applies the current controls to this vintage | accepted (inferred from the package; not verified against a published ERST acceptance rule) | "historiske" page, updated 2025-11-25 [S18] |
| **20221001** (2022-10-01) | 13 declared | `https://erhvervsstyrelsen.dk/sites/default/files/2022-11/XBRL20221001-20221117.zip` | FY2022 onward | in `frm_injection` | accepted (inferred) | same |
| **20211001** (2021-10-01) | 11 declared | `https://erhvervsstyrelsen.dk/sites/default/files/2021-11/XBRL20211001_20211105_0459.zip` | FY2021 onward | in `frm_injection` | accepted (inferred) | same |
| 20201001 | not unpacked | `https://erhvervsstyrelsen.dk/sites/default/files/2021-11/XBRL20201001_20210115_1135%20%284%29.zip` | FY2020 onward | oldest vintage in `frm_injection` | accepted (inferred) | same |
| 20191001 and older (20171001, 20161001, 20151001, 20140701, 20130401, 20121001, 20110701, 20101108; no 20181001 exists) | | listed on the "historiske" page | | **not** in `frm_injection` | likely not accepted; not confirmed | same |
| DK-IFRS stand-alone (20211220 last; 20191220, 20171220, …) | | "historiske" page | | phased out; IFRS filers use the ÅRL companion entry point plus ESEF | retired | same |

> **Honest gap (acceptance window).** "Accepted (inferred)" in the table
> above is not verified against any published ERST acceptance matrix: the
> Taksonomier-aktuelle [S3], historiske [S18] and Kontroller [S2] pages
> publish none.

No final 2026 release existed on 2026-10-15; the cadence is one `YYYY1001`
release published each November. On 2 October 2026 ERST sent a draft 2026
DKGAAP taxonomy out for consultation (comments by 23 October 2026; final
version "i løbet af november 2026"); the draft adds EBITDA in the key
figures, changes the data type `StringItemType` to `TextBlockItemType`, and
implements ESAP metadata [S19]. Per release ERST publishes a machine diff
(`compare-DKGAAP-2025-vs-2024_0.zip`) and a human change summary [S3].

The package's `frm_injection/` holds ERST formula controls for vintages
20201001 to 20251001, which suggests that ERST validates older-vintage
filings against its current control set. That is an inference from the
package: it is **not verified against** any ERST statement that receipt
validation applies the injected controls to a 2022-vintage filing. If it
holds, validating against the pristine 2022 package reproduces the wrong
rule set; inject the current formula package first
(`HowToDoInjectionOfFormulaIntoDkgaapYYYY.txt` in the package says how).

<a id="profile-arl-arsrapport"></a>

## Profile: ÅRL årsrapport deposited with Erhvervsstyrelsen

### Who files, to whom, under what law

- **Regulator / receiver:** Erhvervsstyrelsen (DCCA), which runs the
  Regnskab Indberet platform and publishes the filed data on
  `www.data.virk.dk` [S1].
- **Primary statute:** *Årsregnskabsloven* (ÅRL, the Danish Financial
  Statements Act), consolidated as **LBK nr. 402 af 23/03/2026**, which
  re-promulgates lovbekendtgørelse nr. 1057 af 23. september 2024 with the
  later amendments [S7]. ÅRL § 155 empowers ERST to lay down rules on
  submission (indsendelse); § 153 a stk. 2 empowers it to prescribe IT
  systems, digital formats and signatures; § 138 fixes the filing deadlines
  (*Deadlines*) [S7].
- **Operative filing rules:** the *indsendelsesbekendtgørelse* (submission
  executive order), currently **BEK nr. 859 af 18/06/2025** (j.nr.
  2025-4279, Lovtidende A 28 June 2025), issued "i medfør af" ÅRL §§ 99 d,
  137 j, 137 n, 138, 138 a, 148 a, 153 a-153 c, 155, 155 b, 157, and 164
  [S1].
- **Who files:** entities subject to ÅRL, reporting classes B, C, D, plus
  voluntary filers: a company that may omit preparing and filing an
  årsrapport under the ÅRL §§ 4-6 exemptions but does not use that option
  must follow ÅRL and this executive order's rules on filing an årsrapport
  (BEK 859/2025 § 1 stk. 3) [S1]. Reporting class A itself is ÅRL § 7
  stk. 1 nr. 1: entities without a § 3 stk. 1 duty that report
  voluntarily [S7]. BEK 859/2025 § 1 stk. 1 defines scope by **document
  type** rather than by reporting class, so the B/C/D framing is an
  inference from ÅRL. That scope also covers exemption declarations
  (undtagelseserklæringer) filed in lieu, half-year reports for state
  joint-stock companies, interim reports for listed class-D companies,
  third-country sustainability reports, and country-by-country income-tax
  information reports (CbCR) [S1].
- **Exclusive channels:** § 3 makes the digital channels mandatory;
  reports "kan ikke indberettes på andre måder" (cannot be filed any other
  way) [S1].
- **Responsibility:** management stays responsible even when a rådgiver
  (auditor/lawyer) submits, and for up to 5 years ERST may demand
  documentation of preparation, approval, and signature (§ 2; ÅRL § 160)
  [S1].

### Deadlines

The deadline runs on **receipt at Erhvervsstyrelsen**, not on dispatch, and
the reporting class fixes its length [S7][S1]:

| Filer | Deadline |
|---|---|
| Reporting classes B and C | Årsrapport **received** by ERST no later than **6 months** after the end of the financial year (ÅRL § 138 stk. 1, 2. pkt.): calendar-year 2025 ⇒ 30 June 2026 |
| Reporting class D | **4 months** (same sentence): calendar-year 2025 ⇒ 30 April 2026 |
| Branch of a foreign undertaking | The foreign undertaking's audited annual report received within **6 months** of financial-year end; no dispensation; the branch's own accounts cannot be filed instead (ÅRL § 143 stk. 1) |

- **Filing must also be prompt after approval.** ÅRL § 138 stk. 1, 1. pkt.
  requires filing "uden ugrundet ophold" once the årsrapport is approved, so
  an unexplained approval-to-filing delay is itself a breach even inside the
  6-month window [S7].
- **No dispensation from the § 138 deadline outside ÅRL §§ 140-141; BEK
  859/2025 § 26 can only extend a påkrav deadline.** ÅRL § 138 stk. 1,
  3. pkt. bars dispensation "jf. dog §§ 140 og 141": ERST may allow an undertaking in *rekonstruktionsbehandling* to file
  within 1 month of the reconstruction ending (§ 140 stk. 1), and an
  undertaking in *konkurs* files no årsrapport at all, back-years falling
  due within 1 month of the bankruptcy ending if the undertaking resumes
  (§ 141) [S7]. BEK 859/2025 § 26 extends the **påkrav** deadline, not the
  § 138 deadline: where the undertaking has received a påkrav (ÅRL § 150
  stk. 2) and a digital reporting solution was unavailable for 2
  consecutive hours between 08:00 and 24:00 on the påkrav deadline day, the
  påkrav deadline moves to 8 working days after the solution works again;
  announced maintenance and the undertaking's or its adviser's own IT
  problems do not qualify (§ 26 stk. 1-4) [S1].
- **Receipt governs.** The deadline is met if the årsrapport is received by
  **24:00 on the deadline day** (BEK 859/2025 § 25 stk. 2) [S1].
- **Miss it** (or file late, not in proper form, or not through the
  prescribed channel) and ÅRL §§ 150-152 and § 162 stk. 1 nr. 1 apply
  (BEK 859/2025 § 25 stk. 3) [S1]: a *påkrav* with an 8-working-day
  deadline (ÅRL § 150 stk. 2), then, only if the report arrives after that
  deadline, an *afgift* (late fee) per management member of DKK 500 / 2,000
  / 3,000 for the 1st / 2nd / 3rd month begun (maximum DKK 3,000), computed
  from expiry of the § 138 stk. 1, 2. pkt. deadline (ÅRL § 151 stk. 1-3);
  § 152 allows a waiver in quite special circumstances [S7].
- **Half-year reports for state joint-stock companies:** within **3 months**
  of the end of the half-year period, via Regnskab Special (BEK 859/2025
  § 30 stk. 1) [S1].

### Channels: Regnskab Basis / Regnskab Special / system-til-system

BEK 859/2025 Kapitel 3 defines three digital solutions. Regnskab Basis and
Regnskab Special must be accessed via `www.indberet.virk.dk` (§ 13 stk. 2).
Instead of Basis or Special a company may use ERST's system-til-system
solution (§ 13 stk. 3, subject to stk. 4); `www.erst.dk` publishes **how**
companies access it, and the provisions laid down for Regnskab Special
apply correspondingly to system-til-system [S1]:

- **Regnskab Basis:** ERST's guided web-keying UI; the filer keys the
  data and the platform generates both the human-readable iXBRL and the
  machine-readable XBRL (§ 17 stk. 1) [S1].
- **Regnskab Special:** a file-upload channel for filers with XBRL
  software; the filer submits **one Inline XBRL file**, which Special
  converts into one or more XBRL files filed alongside it (§ 17 stk. 2)
  [S1].
- **system-til-system:** the machine API; the channel for an automated
  filing platform. It may substitute for Regnskab Special, with the
  Special provisions applying equally (§ 13 stk. 3) [S1].

`§ 13 stk. 4` lists cases where **system-til-system cannot be used** and
the filer must fall back to Basis/Special [S1]: (1) a resubmitted /
corrected report (omgørelse, § 11, which itself must use Basis/Special,
§ 11 stk. 2); (2) a fond (foundation) parent filing a subsidiary's group
accounts (ÅRL § 111 stk. 3); (3) a parent filing a higher parent's group
accounts (§ 112); (4) an IFRS parent using the IFRS 10 consolidation
exemption; (5) a medium subsidiary using the § 78 a class-B option;
(6) an IFRS filer that needs to **extend** the taxonomy (§ 23 stk. 2, the
one case where an extension is permitted; see *Extensions are available,
and they bar system-til-system*); (7) where the general
meeting changed the profit appropriation documented by minutes.

**system-til-system upload contract.** ERST's REST guide (Version 6) [S17]
documents it: base URL `https://erst-api.virk.dk/ri/api`, endpoints
`/ixbrl/indberet` and `/ixbrl/test` (GET and POST; `/xbrl/…` for plain
XBRL), and a JSON body whose required fields are `destinationErst` (value
`true`) and `iXbrl`, which "Indeholder inline XBRL. Værdien er Base64
kodet". Optional fields: `supplerendeInstans`, `token` (sent to file despite
an Advis), `returnDocuments`, `dirigent`, `godkendelsesdato`,
`legatarfortegnelse`. Status code 76: "Entrypointet {0} er ikke understøttet
i indberetning via System til System". Omgørelse and berigtigelse are not
possible through system-til-system (Bilag B) [S17].

### Reporting classes and channel mapping

ÅRL § 7 assigns every entity a reporting class [S7]: **Class A** =
voluntary filers; **Class B** = small; **Class C** = medium (C
mellemstor) and large (C stor); **Class D** = state joint-stock companies
and entities with securities on an EU/EEA regulated market, regardless of
size.

Size thresholds (ÅRL § 7 stk. 2, as raised by lov nr. 480 af 22. maj 2024
§ 1 nr. 2-3 for financial years beginning on or after 1 January 2023
[S16]). An entity crosses a class when it exceeds two of the three limits
in two consecutive years, measured at the balance date [S7]:

| Class | Balance sum | Net revenue | Average FTE |
|---|---|---|---|
| Small (class B) | ≤ DKK 55m | ≤ DKK 111m | ≤ 50 |
| Medium | ≤ DKK 195m | ≤ DKK 391m | ≤ 250 |
| Large (class C stor) | exceeds the medium limits | | |

**Income-mix adjustment (§ 7 stk. 4).** An entity whose financial income or
investment income at least equals its net revenue must, when testing the
stk. 2 thresholds, use net revenue **plus** financial income and investment
income; investment income includes positive value adjustments under ÅRL
§ 38 stk. 1 and realised gains on the sale of investment properties [S7].

The reporting class is itself a tagged fact; `fsa:ClassOfReportingEntity`
carries the enumerated value ("Regnskabsklasse A", "Regnskabsklasse B",
"Regnskabsklasse B, mikrovirksomhed", "Regnskabsklasse C, mellemstor
virksomhed", "Regnskabsklasse C, stor virksomhed", "Regnskabsklasse D",
read from the `20251001` package) [S3][S8]. Embedded control `v801.0100`
(Advis) states that "Regnskabsklasse A" / "Reporting class A" cannot be
used [S2].

**Channel by class** (BEK 859/2025 §§ 13-16) [S1]:

| Class | Channel |
|---|---|
| B | Regnskab Basis **or** Special (or system-til-system, § 13 stk. 3), but **must** use Special if it applies one or more class-C rules (unless Basis offers those C-elements), if the report is IFRS, if it is multilingual (one language Danish/English), or if it splits accounting-policy disclosure per ÅRL § 16 stk. 1, 2. pkt. (§ 14) |
| C | Regnskab Special or system-til-system (§ 15; § 13 stk. 3) |
| D | Regnskab Special or system-til-system, ÅRL or IFRS alike (§ 16; § 13 stk. 3) |

### ÅRL taxonomy architecture, versions, and entry points

**Official root URI:** `http://archprod.service.eogs.dk/taxonomy/`,
controlled by the DCCA. File locations (`schemaRef` values) take the form
`{root}/{yyyymmdd publication date}/{optional 3-letter component}/{file}`,
with the official location embedded per-file as an `officialURI`
processing instruction; namespaces are `http://xbrl.dcca.dk/{prefix}`
(e.g. `http://xbrl.dcca.dk/fsa`, the `targetNamespace` in the `20251001`
package's `fsa.xsd`) [S4]. **The host serves nothing under that path
(404 on every probe, 2026-08-21 and again 2026-10-15)**: it is an identifier, and the files are
distributed only in the taxonomy package whose catalog rewrites the prefix
(see *DTS and vintages*).

**Modular components** (three-letter namespace prefixes) [S4]:

| Prefix | Component |
|---|---|
| `gsd` | General + submission data (submission, entity, period, auditors, board members) |
| `arr` | Approved auditor's reports |
| `mrv` | Management's review (ledelsesberetning) |
| `sob` | Statement of boards (ledelsespåtegning etc.) |
| `fsa` | Financial statements: balance sheet (account + report form), income statement (by nature + by function), result distribution, cash-flow, SoCE, disclosures |
| `dst` / `tax` / `eogs` | Statistics Denmark / tax authority / other Business Authority concepts |
| `tch.xsd`, `cmn.xsd` | Common/technical schemas + bilingual label linkbases `cmn_lab-da` / `cmn_lab-en` |

**Entry points** are schema files that combine reporting requirements
[S4]. The 2015 framework paper framed selection along balance-sheet form
(account vs report) × income-statement form (by nature vs by function),
plus the disclosure set; the shipped `20251001` set uses a different
first axis, set out below.

**Current generation = `20251001`** (published Nov 2025) [S3][S6].
Changes in `20251001` [S3]: updated auditor's-statement enumerations
(audit, extended review, review); new sustainability-assurance fields
(Emphasis of matter, Other matter, Inherent limitations, Management's
responsibilities, Summary of performed work); a new "egenkapital før
korrektioner, primo" (opening equity before corrections) tag in the
`[700.00]` Statement of changes in equity; and case-insensitive
"Regnskabsklasse"/"regnskabsklasse" in the `[801.00]` accounting-policies
section.

**Single-DTS identification.** The instance carries exactly one
`schemaRef` pointing at an archprod entry point. `TH01`: the first
schemaRef must contain `http://archprod.service.eogs.dk/taxonomy/`
(regulator control, **Fejl**, Entrypoints: Alle [S2]; in Arelle DBA [S8]);
`TH10`: no `linkbaseRef`, no `roleRef` (the corpus adds `arcroleRef`),
exactly one `schemaRef` (Fejl) [S2][S8]; `TH02`: the first schemaRef must
be recognisable as a valid entrypoint (Fejl) [S2], not implemented in
Arelle. The absolute-URI requirement belongs to `TH01`.

The `20251001` entry-point filenames are enumerated in *DTS and vintages*
above, read from the package manifest. The selection axis is
balance-sheet form (account form, or account form split by current and
long term) × income-statement form (by nature, by function), plus the
"excluding balance sheet and income statement" companion for IFRS/ESEF
filers and the required-information entry point; the older "account vs
report form" framing of [S4] no longer matches the shipped set.
`entryTotal.xsd` is on disk but not declared as an entry point; do not
file against it.

### iXBRL format rules: one self-contained XHTML

ERST adopted a single format that is both human- and machine-readable
[S3]. Format rules (BEK 859/2025 § 17) [S1]:

- **Specifications:** XBRL 2.1 + Inline XBRL 1.1, against an
  ERST-prescribed taxonomy accessed via `www.erst.dk` (§ 17 stk. 2).
- **One file in, XBRL derived server-side:** "Inline XBRL-format består
  af én fil, som Regnskab Special omdanner til en eller flere
  XBRL-filer". The filer submits **one iXBRL file** and the platform
  derives the XBRL instance(s) (§ 17 stk. 2) [S1].
- **Readable layer may be richer:** more specific labels, logos, images,
  and graphs are allowed, provided the readable figures correspond to the
  tagged structured data (§ 17 stk. 4) [S1]. ERST uses both the iXBRL and
  the derived XBRL in regnskabskontrol (ÅRL §§ 159-159 b and § 161 a;
  § 17 stk. 5).
- **Signatures** need not be reproduced in the filed report (§ 28
  stk. 8), but a signed copy must be retained (§ 28 stk. 5) [S1].

**Self-containment controls** (regulator Kontroller corpus, implemented
in Arelle DBA) [S2][S8]. The corpus states a Fejl/Advis severity for every
rule:

| Code | Requirement | Severity |
|---|---|---|
| `TR11` | No references to external images: only Base64-encoded content is accepted | Fejl [S2] |
| `FR87` | No links to external CSS: all CSS must be inline | Fejl [S2] |
| `FR88` | XBRL elements must have the same CSS media type: "Reglen omfatter forbud mod XBRL-elementer i print-only afsnit" (not implemented in Arelle DBA) | Fejl [S2] |
| `TR12` | No executable code | Fejl [S2] |
| `TR17` | No HTML `<base>` element and no `xml:base` attribute | Fejl [S2] |
| `TR16` | `xml:lang` must be present on the root of the inline XBRL document | Fejl [S2] |

**Hidden elements: the Acceptliste.** Kapitel 3 of the Taksonomier-aktuelle
page, "Acceptliste for hidden elements i Inline XBRL" (formerly the
"Whitelist for hidden elements"), restricts `ix:hidden`: "Indberetninger
fra den 1. januar 2027 må kun benytte nedenstående felter som hidden
elements" [S3]. Version 4 of that page (25 November 2025) moved the start
of the check from 1 January 2026 to 1 January 2027 [S3]. Permitted fields:

- `gsd:IdentificationNumberCvrOfSubmittingEnterprise`,
  `gsd:LegalEntityIdentifierOfSubmittingEnterprise`,
  `gsd:NameOfSubmittingEnterprise`,
  `gsd:AddressOfSubmittingEnterpriseStreetAndNumber`,
  `gsd:AddressOfSubmittingEnterprisePostcodeAndTown`;
- `gsd:DateOfGeneralMeeting`, `gsd:NameAndSurnameOfChairmanOfGeneralMeeting`,
  `gsd:ToolForPreparingTheXBRLInstanceDocument`;
- `gsd:ReportingPeriodStartDate` and `gsd:ReportingPeriodEndDate` with the
  member `RegisteredReportingPeriodDeviatingFromReportedReportingPeriodDueArbitraryDatesMember`;
- `gsd:PrecedingReportingPeriodStartDate` and the preceding-period end date
  (printed on the page as `gsd:PredingReportingPeriodEndDate`);
- `cmn:TypeOfAuditorAssistance` and `fsa:ClassOfReportingEntity`, the
  latter only when the report follows reporting class B, Mikro;
- `arr:TypeOfOpinionSustainabilityReport`,
  `arr:TypeOfOpinionAuditSustainabilityReport`,
  `sob:TheReportingEntityAppliesTheExceptionConcerningOptingOutOfTheStatementByManagementEtc`;
- the 31 ESAP metadata `gsd:` fields listed on the page, including
  `gsd:SizeOfReportingEntityBySectorDBA`, the
  `gsd:Is…DisclosedInTheDocument` / `gsd:Is…SubmittedMandatory` pairs and
  `gsd:InformationOnDisclosureOfPersonalData` [S3].

ERST says the list "vil løbende blive evalueret"; read the page before
gating on it [S3].

### Block (clob) tagging vs mandatory detail tagging

BEK 859/2025 § 19 governs block tagging (clob-opmærkning). In Regnskab
Basis (and optionally Regnskab Special, § 19 stk. 11) certain narrative
areas are keyed as a **block**: management endorsement (ledelsespåtegning),
management review (ledelsesberetning), and note disclosures including
accounting policies [S1].

But specific items must still be **separately detail-tagged**, even
inside a block (§ 19 stk. 2-10) [S1]: responsible managers' signatures
incl. any disagreement (ÅRL §§ 9-10); the § 10 a "next year not audited"
statement; CSR / § 99 a incl. sustainability reporting; corporate
governance §§ 107 b/107 c; fond-governance § 77 a; distribution policy
§ 77 b; payments to governments § 99 c; diversity § 107 d; data-ethics
§ 99 d; and, at note level (§ 19 stk. 10), the reporting class, whether
class-C/D elements were opted in, changes in accounting policy, whether
the cash-flow statement was omitted, the average number of employees, and
the proposed result appropriation.

### No filer extensions under ÅRL: widen and disclose

**No filer-extension mechanism exists under ÅRL.** If the taxonomy lacks
a specific line item, the filer tags under a broader item ("en
regnskabspost med en bredere benævnelse") and specifies it in the notes
(§ 22 stk. 1, *widen-and-disclose*) [S1]. Only if no broader item covers
it and a special need exists under ÅRL § 23 stk. 4 can ERST, on
application, exempt the filer from Basis/Special for that year → a PDF
filing (§ 22 stk. 2-3) [S1].

<a id="profile-ifrs-esef"></a>

## Profile: IFRS filers, dual ÅRL + ESEF tagging

**Which ESEF taxonomy.** Erhvervsstyrelsen implemented ESEF taxonomy
2025 in its systems on 26 August 2026, with the two filer entry points
(IAS 1 or IFRS 18). It may be used only for periods starting on or
after 1 January 2026; earlier periods stay on ESEF 2024, the vintage
`references/esef.md` § DTS and vintages gives for those years [S15].

### The stand-alone DK-IFRS taxonomy is phased out

The stand-alone DK-IFRS taxonomy has been **phased out**: BEK 859/2025
requires IFRS accounts to be filed with the ÅRL taxonomy **plus** the
ESEF taxonomy (§ 17 stk. 3) [S3][S1]. So an IFRS preparer files **one
Inline XBRL file** tagged with both the Danish ÅRL taxonomy **and**
ESMA's ESEF taxonomy [S1]. The ÅRL entry point used for the
non-financial-statement parts is
`entryDanishGAAPExcludingBalanceSheetIncomeStatementIncludingManagementsReview`
[S3].

### The reducible structured set

IFRS filers may reduce the **structured** part to a minimum set (§ 20):
the auditor/verifier statement, the statement of comprehensive income
incl. income statement, the balance sheet, the cash-flow statement, and
any CSR/governance/diversity/data-ethics statements or URL references,
plus mandatory separate tagging of the **reporting class** and the
**average number of employees** (§ 20 stk. 2); the full report must still
appear in the readable part (§ 20 stk. 4) [S1].

### Extensions are available, and they bar system-til-system

By contrast, **IFRS filers can and must** add a genuine taxonomy
extension when no covering item exists (§ 23 stk. 2), which is precisely
why an extension forces Regnskab Special and bars system-til-system
(§ 13 stk. 4 nr. 6) [S1].

### Relation to EU / ESEF reporting

Denmark is an EU member state: the årsrapport regime **coexists** with ESEF
rather than replacing it. Delta-only: the dual-tagging mechanics live in the *IFRS filers* and
*DKFIN* profiles; this section frames them in the EU context.

- **ESEF / Transparency-Directive transposition.** ESEF (Commission Delegated
  Regulation (EU) 2019/815) applies to issuers caught by **kapitel 5 of the
  Danish Capital Markets Act** (*lov om kapitalmarkeder*), in practice every
  entity with securities on an EU/EEA regulated market. **Finanstilsynet**
  directs issuers to ESMA's ESEF taxonomy [S9]; that it is the national
  competent authority under the Transparency Directive is **not verified
  against** a primary source here ([S9] does not state it; the designation
  sits in *lov om kapitalmarkeder*, not fetched). Denmark **took the
  one-year deferral**: ESEF is mandatory for financial years starting **on/after
  2021-01-01** (first reports published 2022), with iXBRL **block tagging of the
  notes** phased in from FY2022 [S9].
- **Coexistence with the national format.** An IFRS issuer does not choose
  between ÅRL and ESEF; it files **one Inline XBRL document tagged with both**
  the ÅRL taxonomy and ESMA's ESEF taxonomy (see *The stand-alone DK-IFRS taxonomy is phased out*), because BEK 859/2025 § 17
  stk. 3 phased out the stand-alone DK-IFRS taxonomy (*Vintage and applicability*) [S1][S3]. Listed
  financial groups add DKFIN on top (ESEF + DKFIN, the *DKFIN* profile) [S5].
- **CSRD / ESRS trajectory.** Sustainability-reporting markup was slated to
  follow ESEF: CSRD (Directive (EU) 2022/2464) amended Art. 29d of the Accounting
  Directive to require the management report in ESEF format and the sustainability
  statement marked up per Reg. 2019/815 [S10]. That obligation is now
  **suspended**: **Directive (EU) 2026/470 (Omnibus I)** (adopted 24 Feb 2026,
  in force **18 March 2026**) amends Art. 29d so that, *until* mark-up rules are
  actually adopted through an update to Reg. 2019/815, undertakings **are not
  required to mark up their sustainability reporting** [S10]. So as of this
  reference there is **no live ESRS/CSRD iXBRL tagging obligation**; treat any
  tool that emits ESRS block-tags today as running ahead of the mandate.

<a id="profile-dkfin"></a>

## Profile: DKFIN, the Finanstilsynet financial-sector sub-regime

From financial year 2025, financial-sector entities covered by the
iXBRL-filing requirement must use Finanstilsynet's taxonomy (**DKFIN**),
which is an **embedded part** of ERST's ÅRL taxonomy [S5]. Legal basis:
indberetningsbekendtgørelsen **BEK nr. 917 af 27/06/2025**, in force
1 July 2025, except § 4 stk. 4 nr. 2-4 and § 14, which enter into force
10 January 2028, and § 4 stk. 4 nr. 1, which enters into force 10 January
2030 (§ 17 stk. 1-3). It applies to financial years beginning 1 January
2025 or later; §§ 6-9 may be applied voluntarily, wholly or partly, for the
first time in annual and interim reports for financial year 2024 (§ 18)
[S14][S5].

- Listed financial groups reporting IFRS **consolidated** accounts tag
  with **ESEF + DKFIN**, using the IFRS entry points in DKFIN [S5].
- Financial entities preparing a CSRD sustainability report or Taxonomy-
  Regulation Art. 8 reporting will tag with **DKFIN plus** the EU
  sustainability taxonomies (ESRS / Art. 8), which Finanstilsynet itself
  calls *"de kommende EU-taksonomier"*, the **forthcoming** ones, with the
  duty grounded in the ESEF regulation [S5]. Neither taxonomy has been
  adopted, and the substituted Art. 29d suspends mark-up until they are
  (*Relation to EU / ESEF reporting*), so do **not** require ESRS or Art. 8 mark-up
  of a filing today [S5][S10].

DKFIN has **eight top-level entry points** by entity type [S5]: (1)
alternative investment fund managers and investment management companies;
(2) banks, mortgage-credit institutions, financial holding companies
(primarily credit), investment firms, investment holding companies, the
ship-finance institute, and KommuneKredit; (3) company pension funds
(firmapensionskasser); (4) Danish UCITS (excluding værdipapirfonde);
(5) IFRS excluding financial statements; (6) insurance companies,
transversal pension funds, insurance holding and financial holding
(primarily insurance); (7) life insurance companies; (8) non-life
insurance companies.

Tagging depth mirrors ÅRL: detail vs block tagging per section, keyed to
`[020.00]`/`[120.00]`/`[121.00]`/`[122.00]`/`[220.00]` (management review
block-tagged except the CSR/governance/payments/diversity/data-ethics
sub-statements) [S5]. Hard controls: an unknown entrypoint, multiple CVR
numbers in one filing, and invalid formatting all **block** submission
[S5]. Implementation: the Arelle DBA plugin ships a
`dkfin-2024-multi-target-preview` disclosure system [S8].

<a id="profile-foreign-branch"></a>

## Profile: Foreign-company branch (PDF, not iXBRL)

Foreign-company branches file the foreign report as a **PDF** via a
dedicated self-service solution (§ 24) [S1]. The foreign undertaking's
audited annual report must be **received** by ERST within 6 months of the
end of the financial year; no dispensation is available, and the branch's
own accounts cannot be filed instead (ÅRL § 143 stk. 1; *Deadlines*) [S7].

## Jurisdiction-specific invariants

### Mandatory structured fields, CVR contexts, and periods

**Readable-part header** (§ 27 stk. 1): the top of the readable part
must clearly show (1) the designation "Årsrapport"; (2) the entity's full
name, CVR number, and registered address (hjemstedsadresse); (3) the
reporting period [S1]. The approval date and the name of the dirigent
(chair of the approving body) must be reported to ERST as part of the
report, or supplied at filing time when filed in Inline XBRL
(§ 27 stk. 2) [S1].

**CVR and context controls** (Arelle DBA; pair with BEK 859/2025 § 27 and
the Kontroller corpus) [S8]. `TR01`, `TR02`, `TR03`, `TR05`, `TR06`,
`TR09`, `TR15`, `TH06`, `TH14` and `TC02` are regulator rules too, all
**Fejl** [S2]. `TM12`, `TM16`, `TM22` and `TM24` survive in the corpus only
in Bilag 2, as business rules replaced by embedded controls (`e000.0001`,
`v000.0104`, `v000.0105`, `v000.0107`, all Advis); `TM13`, `TM25`, `TM27`
and `TM29` are Arelle-only [S2][S8]:

| Code | Requirement |
|---|---|
| `TM12` / `TM13` | `gsd:IdentificationNumberCvrOfReportingEntity` present, and only once |
| `TR02` | CVR context entity-identifier scheme = the absolute URI `http://www.dcca.dk/cvr` |
| `TR03` | Identifier value = the CVR number in that fact |
| `TR09` | All contexts share the same identifier scheme + value |
| `TH06` | CVR context period cannot be "forever" |
| `TR15` | LEI-scheme value match (`http://standards.iso.org/iso/17442`) |
| `TR01` | All `gsd` facts share the CVR context's entity + period |
| `TR05` / `TR06` | `gsd:ReportingPeriodStartDate` / `EndDate` tie to the CVR context period |
| `TM16` | `gsd:InformationOnTypeOfSubmittedReport` tagged once |
| `TH14` | Arelle: report-type fact must not use certain enumerations (Selskabsselvangivelse; the exemption-declaration value; ESG-rapport) [S8]. The regulator's `TH14` (Fejl) is instead a whitelist that includes Selskabsselvangivelse and "Erklæring om undtagelse fra aflæggelse årsrapport" [S2]; the two differ |
| `TM22` / `TM24` | Entity-name / submitter-name capped to one tag each |
| `TM25` / `TM27` | Submitter street+number and postcode+town mandatory |
| `TM29` | Either `gsd:DateOfGeneralMeeting` or `gsd:DateOfApprovalOfAnnualReport` present |
| `FR91` | If both meeting date and approval date are given, they must match (not in the regulator corpus; Arelle-only) [S8] |
| `FR1` | Dirigent name (`gsd:NameAndSurnameOfChairmanOfGeneralMeeting`) required when a meeting date is given |
| `TC02` | CPR (personal-ID) numbers must not appear as typed-dimension values |

`TH03` is a regulator rule: "Der skal oplyses et gyldigt CVR-nr. for
regnskabsaflæggende virksomhed" (Fejl, Entrypoints: Alle): the CVR number
must be filled in and registered in the CVR register [S2]. The Arelle DBA
plugin does not implement it (no `rule_th03`) [S8].

### Broken / floating fiscal years: the RegisteredReportingPeriod dimension

Denmark distinguishes two date sets (Taksonomier-aktuelle Kapitel 2.3)
[S3]:

1. **The accounting reporting period (regnskabsperioden).** The
   accounting dates underlying the figures. For an entity with a floating
   year these form an unbroken date sequence across the company's life.
   It is marked with the `AllReportingPeriodsMember`.
2. **The registered reporting period (registrerede regnskabsperiode).**
   The period registered in CVR, which ERST's systems know in advance.

When a report uses a period **differing** from the CVR-registered period
(a *flydende regnskabsperiode*, e.g. a group whose parent and subsidiary
have unequal periods, or after a demerger/merger), the CVR-registered
period must be marked in XBRL via an extra dimension member:
`RegisteredReportingPeriodDeviatingFromReportedReportingPeriodDueArbitraryDatesMember`.
Its dates have **no accounting meaning**: they exist only so ERST can
place and publish the filing against the registered obligation, and they
**never** form the basis for the context dates [S3].

Controls (Arelle DBA) [S8]: `TM18`/`TM20` constrain
`ReportingPeriodStartDate`/`EndDate` (no dimension, or the default
`AllReportingPeriodsMember`) to a single tagging (in the regulator corpus
these survive only in Bilag 2, replaced by the embedded Advis controls
`v000.0103`/`v000.0102` [S2]); `TM32`/`TM33` do the same for the
`RegisteredReportingPeriodDeviating…ArbitraryDatesMember` dimension, and
are regulator rules too (Fejl) [S2].

`FR107`/`FR108`/`FR109`/`FR115` are **not** fiscal-period checks: they
check the dates of the **bookkeeping system** (bogføringssystem, ÅRL
§ 138 a) reported in the supplementary instance. In the corpus: `FR107` a
date in the accounting period with no bookkeeping system (Fejl), `FR108`
overlapping systems (Fejl), `FR109` a system period outside the accounting
period (Fejl), `FR115` end date before start date (Advis); all
"Entrypoints: Supplerende instans" [S2]. Arelle's `FR109` resolves the
accounting period via `AllReportingPeriodsMember` for consolidated reports
and via the deviating member for floating-period reports [S8].

### Packaging / artifact shape

The filer submits a **single Inline XBRL file** in XHTML; Regnskab
Special (or system-til-system) derives the XBRL instance(s) server-side
(§ 17) [S1]. This differs from the ESEF/KvK Report-Package model: no
filer-assembled `META-INF/taxonomyPackage.xml` container is described in
the fetched sources; the derivation is ERST's, not the filer's. The
single XHTML must satisfy the self-containment controls in *iXBRL format rules: one self-contained XHTML* (no external
images/CSS, no executable code, no `<base>`/`xml:base`, `xml:lang` on the
root); Base64-embed any images.

For an automated filer the system-til-system REST service takes the same
single Inline XBRL document, Base64-encoded in the JSON field `iXbrl` of a
POST to `/ixbrl/indberet`, not a filer-assembled zip (*Channels: Regnskab
Basis / Regnskab Special / system-til-system*) [S17].

## Validation

### The ERST Kontroller corpus: the filing-rules authority

The Danish analogue of the KVK Filing Rules is ERST's *Teknisk vejledning
og dokumentation for Regnskab Indberet: Kontroller*, structured to follow
the taxonomy section by section and explicitly a living document [S2].

**Two outcome classes** (Kapitel 1.1) [S2]: **Fejl** = blocking (the
filing cannot proceed) and **Advis** = advisory (the filer may proceed
but should check for an error). This maps cleanly onto an
errors-gate / warnings-inform validator split: gate on `Fejl`, surface
`Advis`.

**Rule naming** (Kapitel 1.2-1.3) [S2]: business rules
(*Forretningsregler*) carry **2-3 letters + a number** (e.g. `FR1`,
`TH01`), sometimes with a trailing letter (`FR74a`/`FR74b`,
`FR84a`/`FR84b`/`FR84c`); a separate `FRU` series (`FRU01`-`FRU11`) covers
undtagelses- and fritagelseserklæringer, with the CVR-period trio
`FRU09`/`FRU10`/`FRU11` ("FRU010"/"FRU011" appear only as
cross-references inside `FR43`/`FR44`).
Embedded taxonomy rules carry an **assertion letter + 3 section-digits + an
ID**, where the assertion letter is **E** = Existence (selected fields
present) or **V** = Value (reported values valid); a section digit may be
an `x` wildcard (`e50x.0001`, `v40x.0101`) as well as a literal
(`v806.0100`, `v808.0100`).

**The whole corpus is retrievable, and every rule carries its severity.**
All 16 chapters render as static HTML, and each rule is followed by an
explicit `FEJL` or `ADVIS` token plus an **Anvendelse** block naming the
entry points (Entrypoints), the taxonomies (Taksonomier), and where
relevant the reporting class (Regnskabsklasse) the rule applies to [S2].
Read severity and scope off the corpus rather than inferring them from a
validator's message level.

Codes verified on the fetched regulator page [S2]: `FR1` (missing dirigent
name), `FR6` (general-meeting date not after filing date), `FR8` (approval
date not after filing date), `FR42` (accounting period not found in CVR;
Fejl), `FR43` (start date differs from CVR; Fejl), `FR44` (end-date
mismatch = Advis), `FR47` (changed attachment set on omgørelse = Advis);
`TH01` (first schemaRef begins with the archprod URI; Fejl, Entrypoints:
Alle), `TH02` (first schemaRef must be a valid entrypoint; Fejl), `TH03`
(valid, registered CVR number; Fejl), `TH06` (context period cannot be
"forever"; Fejl), `TR02` (entity-identifier scheme = the absolute URI
`http://www.dcca.dk/cvr`; Fejl, Entrypoints: DKGAAPRequiredInformation),
and `TC02` (CPR number as context id for a typedMember; Fejl). The
embedded assertions render with severities too: `v40x.0100` (assets must
equal liabilities and equity; Fejl), `v40x.0101` (all asset fields must be
positive; Fejl), `e50x.0001` (`ProfitLoss` must be stated; Advis),
`v806.0100` and `v808.0100` (both Advis) [S2].

`FR34`, `FR41`, `FR82`, and `FR91` appear **nowhere** in the corpus. They
are Arelle-only, and a finding resting on one of them establishes "Arelle
implements X", not "the regulation requires X" [S8].

### How to run it: the Arelle DBA plugin

Arelle ships a dedicated Danish plugin at `plugin/validate/DBA`
(validationType `DBA`, PLUGIN_NAME "Validate DBA"). It is the best
machine-readable enumeration of real Danish rule codes and their exact
predicates [S8]. It registers **six disclosure systems** [S8]:

| Disclosure system | Use |
|---|---|
| `arl-2022-preview` | Stand-alone ÅRL, 2022 |
| `arl-2024-preview` | Stand-alone ÅRL, 2024 |
| `arl-2025-preview` | Stand-alone ÅRL, 2025 |
| `arl-2024-multi-target-preview` | Multi-target (dual/derived-target iXBRL era), 2024 |
| `arl-2025-multi-target-preview` | Multi-target iXBRL era, 2025 |
| `dkfin-2024-multi-target-preview` | Finanstilsynet financial-sector sub-profile |

Rule logic is split into five modules (`validationRuleModules=[fr, tc,
th, tm, tr]`): `fr.py` (business rules), `th.py` (schemaRef/DTS/context
shape), `tr.py` (technical/inline-document), `tm.py`
(mandatory/uniqueness tagging), `tc.py` (content/privacy) [S8].

Run a standard ÅRL 2025 iXBRL validation (swap the disclosure system to
`dkfin-2024-multi-target-preview` for a financial-sector filing):

```bash
python3 -m arelle.CntlrCmdLine \
  --plugins validate/DBA \
  --disclosureSystem arl-2025-multi-target-preview \
  --file <report>.xhtml --validate
```

> **Caveat: the `-preview` suffix matters.** Every DBA disclosure-system
> name carries `-preview`, signalling **pre-release** rule sets. Verify
> code coverage against the live ERST Kontroller corpus [S2] before
> relying on any single code, and remember the plugin proves *Arelle
> implements X*, not *the regulation requires X* [S8]. Pair every finding
> with a BEK 859/2025 [S1], Kontroller [S2], Taksonomier-aktuelle [S3],
> or Finanstilsynet [S5] citation.

### Rule-code reference: FR business rules

The technical TH / TR / TM / TC codes are tabulated in the functional
sections where they bite: self-containment (*iXBRL format rules: one self-contained XHTML*), CVR + context (*Mandatory structured fields, CVR contexts, and periods*), and
period coverage (*Broken / floating fiscal years: the RegisteredReportingPeriod dimension*). Additional codes: `TH05` (no segments in
contexts; Fejl) and `TC02` (no CPR in typed dimensions; Fejl) are in both
the corpus and the plugin [S2][S8]; `TR19` (duplicate facts must not
differ in content) and `TM30`/`TM31` (meeting/approval dates tagged once)
are Arelle-only [S8]. The **FR business rules** carry the substantive
accounting/formal checks. Severity and Anvendelse are the regulator's own
[S2], and `n/a` marks a code the corpus does not carry at all. Predicates without an [S2] marker come from the plugin
docstrings [S8]:

| Code | Predicate | Severity | Anvendelse / source |
|---|---|---|---|
| `FR1` | Dirigent name required when a general-meeting date is given | Fejl | Entrypoints: Alle; Taksonomier: Alle [S2] |
| `FR33` | SoCE/equity-disclosure minimums for class C/D groups | Advis | Entrypoints: Alle; Taksonomier: Alle; Regnskabsklasse C og D [S2] |
| `FR34` | If `Equity` is non-zero, at least one other balance-sheet field (Assets / NoncurrentAssets / CurrentAssets / liabilities lines / LiabilitiesAndEquity) must also be tagged | n/a | Not in the corpus, Arelle-only [S8] |
| `FR63` | Balance-sheet item must not exceed the balance-sheet total | Fejl | Entrypoints: Balance i kontoform [S2] |
| `FR74a` / `FR74b` / `FR77a` / `FR77b` | Each line group ≤ balance-sheet total minus equity: `FR74a` provisions, `FR74b` liabilities other than provisions, `FR77a` long-term liabilities, `FR77b` short-term liabilities (four line groups, not variants of one rule) | Fejl | Entrypoints: Alle; Taksonomier: Alle [S2] |
| `FR41` | Tax expense required when `ProfitLoss` > DKK 1000 | n/a | Not in the corpus, Arelle-only [S8] |
| `FR56` | Result appropriation (resultatdisponering) required when \|`ProfitLoss`\| > DKK 1000 (ÅRL §§ 31, 95 a) | Fejl | Entrypoints: Alle; Taksonomier: Alle [S2] |
| `FR75` | Employee count (`fsa:AverageNumberOfEmployees`) required when `fsa:EmployeeBenefitsExpense` or `fsa:WagesAndSalaries` exceeds DKK 200,000 (ÅRL § 68) | Advis | [S2] |
| `FR81` | At least one fact carries `xml:lang` of `da` or `en` | Advis | Entrypoints: Alle; Taksonomier: ESEF [S2][S8] |
| `FR82` | Blocks plain XBRL for DK ESEF | n/a | Not in the corpus, Arelle-only [S8] |
| `FR83` | Blocks plain XBRL; allows only Inline XBRL. The rule text names no balance date, and the corpus states "Kontrollen er pt. inaktiv" | Fejl (inactive per the corpus) | Entrypoints: Alle; Taksonomier: Alle [S2] |
| `FR87` | No external CSS: all CSS inline | Fejl | [S2] |
| `FR88` | XBRL elements must have the same CSS media type; no XBRL elements in print-only sections (not implemented in Arelle) | Fejl | Entrypoints: Alle; Taksonomier: Alle [S2] |
| `FR89` | Audit cannot be opted out of when the årsrapport is prepared under reporting class C or D | Fejl | [S2] |
| `FR91` | General-meeting date = approval date when both present | n/a | Not in the corpus, Arelle-only [S8] |
| `FR107` / `FR108` / `FR109` / `FR115` | Bookkeeping-system (bogføringssystem) dates: a date with no system / overlapping systems / system period outside the accounting period / end before start | Fejl / Fejl / Fejl / Advis | Entrypoints: Supplerende instans [S2][S8] |
| `FR116` / `FR117` | Single value per numeric field per period; rendering dimension numeric-only | Advis | Entrypoints: ERST entrypoints; all report types from 2024 onward [S2][S8] |

The corpus is finer-grained than the plugin in places: besides the
`FR74a`/`FR74b` and `FR77a`/`FR77b` splits it carries `FR84a`/`FR84b`/
`FR84c` and `FR85b`/`FR85c` on the audit requirement (all Advis), and an
`FRU` series (`FRU01`-`FRU11`) for undtagelses- and fritagelseserklæringer
[S2]. Check a code against the corpus before reporting it as absent.

## Review workflow

1. **Pin balance date + taxonomy generation** (*Vintage and applicability*). iXBRL is required
   only for balance dates ≥ 2025-01-01; use `20251001` (or `20241001`).
2. **Check the deadline** (*Deadlines*). Classes B and C: received by ERST
   within 6 months of financial-year end; class D: 4 months; a foreign
   branch: 6 months for the foreign undertaking's own audited report.
   Receipt by 24:00 on the deadline day governs, not dispatch, and filing
   must follow approval "uden ugrundet ophold". The § 138 deadline admits
   no dispensation outside ÅRL §§ 140-141; BEK 859/2025 § 26 extends only a
   påkrav deadline after a system outage.
3. **Pin the class, channel, and basis** (*Reporting classes and channel mapping*; the *IFRS filers* profile). Class B/C/D changes
   the legal channel and mandatory detail-tags (read
   `fsa:ClassOfReportingEntity`); IFRS ⇒ dual ÅRL+ESEF tagging and
   possibly an extension (which bars system-til-system).
4. **Run the DBA validator** in the matching disclosure system (*How to run it: the Arelle DBA plugin*):
   `arl-2025-multi-target-preview`, or `dkfin-2024-multi-target-preview`
   for a financial-sector filing. Capture all messages.
5. **Classify each finding as Fejl vs Advis** (*The ERST Kontroller corpus: the filing-rules authority*). Gate on Fejl; treat
   Advis as informational. When a code is unclear, quote the log line
   verbatim and route on its leading letters (TH/TR/TM/TC/FR).
6. **CVR + context pass** (*Mandatory structured fields, CVR contexts, and periods*). One CVR (`TM12`/`TM13`), scheme
   `http://www.dcca.dk/cvr` (`TR02`), value match (`TR03`), uniform
   scheme (`TR09`), no "forever" CVR period (`TH06`), no CPR in typed
   dimensions (`TC02`).
7. **Period pass** (*Broken / floating fiscal years: the RegisteredReportingPeriod dimension*). For a period differing from the CVR-registered
   period, confirm `RegisteredReportingPeriodDeviating…ArbitraryDatesMember`
   marks the registered dates and `AllReportingPeriodsMember` the
   accounting period. Registered dates must never drive context dates.
8. **Tagging + hygiene pass** (*iXBRL format rules: one self-contained XHTML*; *Block (clob) tagging vs mandatory detail tagging*). The § 19 stk. 2-10 items are
   separately detail-tagged even inside block-tagged narrative; the XHTML
   is self-contained (no external images/CSS, no executable code, no
   `<base>`/`xml:base`, `xml:lang` on the root); the readable part carries
   the "Årsrapport"/name/CVR/address/period header plus approval date and
   dirigent name (`TM29`, `FR1`; `FR91` is an Arelle-only cross-check).
9. **Content-level review.** Read the rendered statements as a finance
   professional. No validator confirms the iXBRL faithfully represents
   the source årsrapport, or that the readable figures match the tagged
   data (§ 17 stk. 4).

When a finding is unclear, quote the validator log line verbatim and
route by its code prefix, the cheapest way to distinguish a real Fejl
from an Advis or a preview-plugin artefact.

## Authorities and governance

The Danish map is unusually concentrated: **Erhvervsstyrelsen** (the Danish
Business Authority / DCCA) is at once the business register, the publication
organ, the digital-reporting operator, and the årsrapport taxonomy author.

- **Business register + publication organ: Erhvervsstyrelsen.** Runs the
  Central Business Register (*Det Centrale Virksomhedsregister*, CVR), the
  authoritative register of basic data for all registered enterprises
  since 1999 (Danish entities; CVR.dk also shows Greenlandic companies
  registered under other legislation), and publishes every deposited årsrapport openly via `CVR.dk` / `data.virk.dk`
  [S11][S1]. The CVR number is the entity key threaded through every context
  (*Mandatory structured fields, CVR contexts, and periods*).
- **Digital-business-reporting programme: Erhvervsstyrelsen (Regnskab
  Indberet on `virk.dk`).** Denmark has **no separately branded SBR-style
  consortium** (the SBR-Nederland analogue); that function, a single digital
  channel over a shared, multi-agency taxonomy (*Channels: Regnskab Basis / Regnskab Special / system-til-system*), is operated directly by
  Erhvervsstyrelsen. The DCCA XBRL framework is explicitly built to serve the
  Business Authority **plus** Statistics Denmark (`dst`) and the tax authority
  (`tax`) from one taxonomy [S4]. This is the "collect once, share across
  agencies" design SBR embodies.
- **Accounting standard-setter: the legislature via ÅRL, administered by
  Erhvervsstyrelsen.** Danish GAAP is codified in the *Årsregnskabsloven* itself
  rather than issued by an independent private board; Erhvervsstyrelsen
  administers, interprets, and enforces it through *regnskabskontrol* (ÅRL
  §§ 159-159 b and § 161 a) [S1]. Listed groups apply EU-endorsed IFRS (see the *IFRS filers* profile).
- **Taxonomy author + governance: Erhvervsstyrelsen (DCCA), annual cadence.**
  Authors and versions the ÅRL taxonomy on a yearly `YYYY1001` generation
  (`20241001`, `20251001`, …), published under
  `http://archprod.service.eogs.dk/taxonomy/` (*ÅRL taxonomy architecture, versions, and entry points*) [S3][S4]. **Finanstilsynet**
  authors the financial-sector DKFIN taxonomy, embedded inside the ÅRL taxonomy
  (see the *DKFIN* profile) [S5].
- **Tax authority: Skattestyrelsen (the Danish Tax Agency).** Runs its own
  structured corporate-filing regime (the *selskabsselvangivelse* via **TastSelv
  Erhverv**), separate from the årsrapport deposit [S12]; the DCCA taxonomy's
  `tax` component carries concepts submittable *with* the annual accounts for tax
  settlement [S4].
- **Securities regulator: Finanstilsynet (the Danish FSA).** Its status as
  National Competent Authority under the Transparency Directive is **not
  verified against** a primary source here ([S9] does not state it). It
  publishes the ESEF guidance for issuers on EU-regulated markets (*Relation to EU / ESEF reporting*) and overlays DKFIN for financial-sector
  entities (the *DKFIN* profile) [S9][S5]. Erhvervsstyrelsen stays the *receiver/publisher* even
  for these issuers: listed class-D filers deposit via Regnskab Special
  (BEK 859/2025 § 16) [S1], financial-sector filers likewise (BEK 917/2025
  § 3 stk. 8), and ERST forwards the receipt to Finanstilsynet (§ 4) [S14].

They interlock at the CVR number and the archprod taxonomy: Erhvervsstyrelsen
collects and publishes; Finanstilsynet supervises the capital-market and
financial-sector overlays; DST / Skattestyrelsen consume adjacent components of
the same framework.

## Coverage and known limitations

Danish filing rules evolve per release. The Kontroller corpus itself
renders in full and states a Fejl/Advis severity and an Anvendelse scope
for every rule, so route a severity or scope question to it rather than
inferring one (*The ERST Kontroller corpus: the filing-rules authority*).
If the question concerns an un-enumerated entry-point filename or matrix (*ÅRL taxonomy architecture, versions, and entry points*), the
acceptance window for older taxonomy vintages (*DTS and vintages*), CSRD/sustainability applicability by class/year, or any
code carrying the plugin's `-preview` caveat (*How to run it: the Arelle DBA plugin*), say so and route to
the primary source: Kontroller [S2], Taksonomier-aktuelle [S3], BEK
859/2025 [S1], or Finanstilsynet [S5]. Do not invent a rule id,
enumeration, or version. The cost of a wrong citation on a regulated
årsrapport is high.

## Sources

Each source was live-fetched for this reference; the id in brackets is
what each establishes.

- **[S1]** BEK nr. 859 af 18/06/2025 (indsendelsesbekendtgørelsen),
  Tier 1: <https://www.retsinformation.dk/eli/lta/2025/859/pdf>. The
  current submission executive order and the source for nearly every § in
  this file: legal basis (§ 3, ÅRL § 155), channels + class mapping
  (§§ 13-16), single-file iXBRL with server-side derivation (§ 17), dual
  ÅRL+ESEF (§ 17 stk. 3), clob block tagging (§ 19), IFRS minimum set +
  extension rules (§§ 20-23), foreign-branch PDF (§ 24), readable-part
  header + approval + dirigent (§ 27), signatures (§ 28), language
  (§§ 6-7), deadline receipt + late-fee routing (§§ 25-26), state
  joint-stock half-year reports (§ 30), and the repeal of BEK 1054/2021
  with effect for documents filed on/after 2025-07-01 (§ 35).
- **[S2]** Teknisk vejledning for Regnskab Indberet: Kontroller, Tier 1:
  <https://erhvervsstyrelsen.dk/vejledning-teknisk-vejledning-og-dokumentation-regnskab-20-kontroller>.
  Version 3, last updated 1 October 2025. The filing-rules authority:
  Fejl vs Advis semantics; rule naming; the FR and FRU business rules and
  the embedded `e###.####` / `v###.####` assertions, each followed by an
  explicit FEJL/ADVIS token and an Anvendelse block (Entrypoints /
  Taksonomier / Regnskabsklasse); the TH/TR/TC technical chapters. All 16
  chapters render as plain static HTML.
- **[S3]** Dokumentation for Regnskab Indberet: Taksonomier, aktuelle,
  Tier 1:
  <https://erhvervsstyrelsen.dk/vejledning-teknisk-vejledning-og-dokumentation-regnskab-20-taksonomier-aktuelle>.
  ÅRL taxonomy `20251001` and its changes; iXBRL mandate from balance
  date 2025-01-01; DK-IFRS phased out ⇒ ÅRL(Excluding…) + ESEF; the
  floating-year dimension members; the Kapitel 3 "Acceptliste for hidden
  elements i Inline XBRL" (Version 5, updated 2 October 2026; read
  2026-10-15).
- **[S4]** DCCA XBRL Taxonomy Framework Architecture, v1.0 (2015-10-01),
  Tier 1:
  <https://danishbusinessauthority.dk/sites/default/files/2023-10/xbrl-taxonomy-framework-architecture-01102015_wa.pdf>.
  Root URL, `{yyyymmdd}/{component}` layout and per-file `officialURI`;
  modular namespaces; entry-point schemas. Architectural reference only
  (predates the iXBRL era).
- **[S5]** Finanstilsynets taksonomi (DKFIN), Tier 1:
  <https://www.finanstilsynet.dk/ansoeg-og-indberet/indberetning-til-erhvervsstyrelsen/finanstilsynets-taksonomi>.
  DKFIN embedded in the ÅRL taxonomy, mandatory FY2025; BEK nr. 917 af
  27/06/2025 (commencement and application detail in [S14]); ESEF+DKFIN for listed IFRS groups; the eight entry points;
  detail-vs-block tagging; hard controls.
- **[S6]** Årsregnskabslov-taksonomi 2025 er implementeret (ERST),
  Tier 1:
  <https://erhvervsstyrelsen.dk/aarsregnskabslov-taksonomi-2025-er-implementeret-og-klar-til-brug>.
  `20251001` published November 2025, live in ERST PreProd + Prod;
  2025 or 2024 taxonomy recommended.
- **[S7]** Årsregnskabsloven, **LBK nr. 402 af 23/03/2026**
  (Bekendtgørelse af årsregnskabsloven), Tier 1:
  <https://www.retsinformation.dk/eli/lta/2026/402> (PDF at
  <https://www.retsinformation.dk/eli/lta/2026/402/pdf>; the page itself is
  JS-rendered, the `/pdf` path serves plain text). Re-promulgates
  lovbekendtgørelse nr. 1057 af 23/09/2024 with later amendments. Reporting classes
  A/B/C/D and the size thresholds (§ 7 stk. 2 and stk. 4); filing deadlines
  and their carve-outs (§§ 138, 140, 141, 143); late-filing consequences
  (§§ 150-152, § 162 stk. 1 nr. 1); regnskabskontrol (§§ 159-159 b,
  § 161 a).
- **[S8]** Arelle `validate/DBA` plugin source, Tier 1 implementation
  evidence:
  <https://github.com/Arelle/Arelle/tree/master/arelle/plugin/validate/DBA>.
  Real Danish rule codes and predicates; the six disclosure systems;
  rule modules fr/th/tr/tm/tc. Establishes *Arelle implements X*, **not**
  *the regulation requires X*; pair every code with S1/S2/S3/S5. The
  `-preview` suffix marks pre-release rule sets.
- **[S9]** Finanstilsynet: European Single Electronic Format
  (Transparensdirektivet), Tier 1:
  <https://www.finanstilsynet.dk/lovgivning/eu-lovsamling/transparensdirektivet/european-single-electronic-format>.
  ESEF applies to kapitel-5 *lov om kapitalmarkeder* issuers; Denmark's
  one-year deferral (mandatory FY2021, published 2022); notes block tagging
  from FY2022; ESMA-authored ESEF taxonomy. The page (updated 27-02-2023)
  does not state that Finanstilsynet is the NCA and does not address
  sustainability mark-up; neither point is verified against it.
- **[S10]** Directive (EU) 2026/470 (Omnibus I), Tier 1:
  <https://eur-lex.europa.eu/eli/dir/2026/470/oj/eng>. Adopted 24 Feb 2026, in
  force 18 Mar 2026; recital 24 + the amendment to Accounting-Directive Art. 29d:
  until markup rules are adopted via an update to Reg. (EU) 2019/815,
  undertakings are not required to mark up sustainability reporting.
- **[S11]** Erhvervsstyrelsen: Det Centrale Virksomhedsregister (CVR), Tier 1:
  <https://erhvervsstyrelsen.dk/det-centrale-virksomhedsregister-cvr>. CVR = the
  authoritative register of basic data for all registered enterprises
  since 1999; grunddata published via CVR.dk.
- **[S12]** Skattestyrelsen: Tax return for companies and foundations (TastSelv
  Erhverv), Tier 1:
  <https://skat.dk/en-us/businesses/companies-and-foundations/companies-and-foundations/tax-return-for-companies-and-foundations>.
  Danish corporate tax-return regime via TastSelv Erhverv, separate from the
  årsrapport deposit; deadline usually ~6 months after period end.
- **[S13]** BEK nr. 1003 af 26/06/2023 (amending BEK nr. 1054 af
  31/05/2021), Tier 1:
  <https://www.retsinformation.dk/eli/lta/2023/1003/pdf>. § 1 nr. 4 rewrote
  § 17 of BEK 1054/2021 (single-file iXBRL, the Regnskab Special format
  specification, dual ÅRL + ESEF tagging for IFRS filers); § 2 stk. 2 gives
  nr. 4-6 effect for balance dates on/after 1 January 2025. Establishes
  that the dual-tagging obligation dates from 2023, not from BEK 859/2025.
- **[S14]** BEK nr. 917 af 27/06/2025 (indberetningsbekendtgørelsen,
  financial sector), Tier 1:
  <https://www.retsinformation.dk/eli/lta/2025/917/pdf>. § 17: in force
  1 July 2025, with § 4 stk. 4 nr. 2-4 and § 14 deferred to 10 January 2028
  and § 4 stk. 4 nr. 1 to 10 January 2030; § 18: applies to financial years
  beginning 1 January 2025 or later, §§ 6-9 usable voluntarily, wholly or
  partly, first for financial year 2024.
- **[S15]** Erhvervsstyrelsen: "ESEF-taksonomi 2025 er implementeret og
  klar til brug" (news, 26 August 2026), Tier 1:
  <https://erhvervsstyrelsen.dk/esef-taksonomi-2025-er-implementeret-og-klar-til-brug>,
  read 2026-10-13.
- **[S16]** Lov nr. 480 af 22. maj 2024 (amending årsregnskabsloven, incl.
  the EU directive raising the size criteria), Tier 1:
  <https://www.retsinformation.dk/eli/lta/2024/480/pdf>, read 2026-10-15.
  § 1 nr. 2-3 raise the ÅRL § 7 stk. 2 limits (44 → 55, 89 → 111, 156 →
  195, 313 → 391 mio. kr.); § 14 stk. 2 gives them effect for financial
  years beginning on or after 1 January 2023.
- **[S17]** Erhvervsstyrelsen: "XBRL og Inline XBRL REST Klient Eksempel i
  Java" (system-til-system guide, Version 6, updated 11 February 2026),
  Tier 1:
  <https://erhvervsstyrelsen.dk/vejledning-xbrl-og-inline-xbrl-rest-klient-eksempel-i-java>,
  read 2026-10-15. Base URL, endpoints, JSON fields (Base64 `iXbrl`),
  status codes, and the bar on omgørelse via system-til-system.
- **[S18]** Dokumentation for Regnskab Indberet: Taksonomier, historiske,
  Tier 1:
  <https://erhvervsstyrelsen.dk/vejledning-teknisk-vejledning-og-dokumentation-regnskab-20-taksonomier-historiske>,
  read 2026-10-15 (updated 25 November 2025). Older ÅRL and DK-IFRS
  taxonomy packages and compare files.
- **[S19]** Erhvervsstyrelsen: "Udkast til ny version af taksonomi til
  årsrapporter sendt i høring" (news, 2 October 2026), Tier 1:
  <https://erhvervsstyrelsen.dk/udkast-til-ny-version-af-taksonomi-til-aarsrapporter-sendt-i-hoering>,
  read 2026-10-15. Draft 2026 DKGAAP taxonomy, consultation to 23 October
  2026, final version due November 2026.
