---
reference_id: fi-prh
jurisdiction: FI
restructured_on: 2026-08-15
profiles:
  - id: fas-sbr
    section: profile-fas-sbr
  - id: ifrs-esef
    section: profile-ifrs-esef
  - id: sustainability-report
    section: profile-sustainability-report
---

# Finland: PRH digital financial statements (digitilinpäätös)

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*

**Last verified (UTC): 2026-10-15.** Every specific claim was re-read against the primary source cited for it; claims no primary source settles are marked as gaps.

**Load this when:** the filing goes to the Finnish PRH as digital financial statements, whether national FAS/SBR, IFRS, or an ESEF ZIP.

**Do not load this when:** the question is generic ESEF mechanics (`references/esef.md`); note that PRH's carrier is XHTML-in-ZIP, not a `.xbri` report package.

**Contents**

- [Start here: choose a filing profile](#start-here-choose-a-filing-profile)
- [Vintage and applicability](#vintage-and-applicability)
  - [The legal instruments: Accounting Act plus two named PRH decisions](#the-legal-instruments-accounting-act-plus-two-named-prh-decisions)
  - [The two-stage mandate: keep these distinct](#the-two-stage-mandate-keep-these-distinct)
  - [DTS and vintages](#dts-and-vintages)
  - [Bi-temporal cheatsheet: which vintage applies to which period](#bi-temporal-cheatsheet-which-vintage-applies-to-which-period)
- [Profile: Trade Register digital financial statement: Finnish FAS (national SBR taxonomy)](#profile-fas-sbr)
  - [Who files, to whom, under what law](#who-files-to-whom-under-what-law)
  - [The national SBR taxonomy: modules, distribution, cadence](#the-national-sbr-taxonomy-modules-distribution-cadence)
- [Profile: IFRS statements and listed-issuer ESEF re-use](#profile-ifrs-esef)
  - [Which taxonomy applies](#which-taxonomy-applies)
  - [Packaging: the ESEF ZIP re-used for the Trade Register](#packaging-the-esef-zip-re-used-for-the-trade-register)
  - [Relation to EU reporting: ESEF coexistence and the CSRD/ESRS trajectory](#relation-to-eu-reporting-esef-coexistence-and-the-csrdesrs-trajectory)
- [Profile: CSRD sustainability report: assured, filed with the digital statements, not XBRL-tagged](#profile-sustainability-report)
  - [The 2026 scope change: law 555/2026 (supersedes older ≥500-employee framing)](#the-2026-scope-change-law-5552026-supersedes-older-500-employee-framing)
- [Jurisdiction-specific invariants](#jurisdiction-specific-invariants)
  - [Packaging and artifact shape: XHTML-in-ZIP, NOT `.xbri`](#packaging-and-artifact-shape-xhtml-in-zip-not-xbri)
  - [Choosing the taxonomy family by accounting framework](#choosing-the-taxonomy-family-by-accounting-framework)
  - [Filing channels, signatures, deadline, tax forwarding, language](#filing-channels-signatures-deadline-tax-forwarding-language)
- [Validation](#validation)
  - [Arelle's FI-PRH plugin checks duplicates only (honest gap) + what PRH's interface checks](#arelles-fi-prh-plugin-checks-duplicates-only-honest-gap--what-prhs-interface-checks)
- [Review workflow](#review-workflow)
  - [A pragmatic PRH review pass, in order](#a-pragmatic-prh-review-pass-in-order)
- [Authorities and governance](#authorities-and-governance)
  - [Stakeholders: the institutional map](#stakeholders-the-institutional-map)
- [Coverage and known limitations](#coverage-and-known-limitations)
  - [When to escalate to primary sources](#when-to-escalate-to-primary-sources)
- [Sources](#sources)
  - [Primary sources: what each establishes](#primary-sources-what-each-establishes)

## Start here: choose a filing profile

Finland is **not** a report-package (`.xbri`) regime: a deposit is **XHTML
alone or a plain ZIP of XHTML** (PRH/1087 s. 2 permits either), and for a
listed issuer it is the **ESEF ZIP** re-used.
For the IFRS/ESEF path, most of the work is ESEF work. Use
`references/esef.md` and return here only for the Trade-Register overlays
(channel, metadata attachments, packaging, deadlines). For the national-GAAP
(Finnish FAS / SBR) path Arelle's `FI-PRH` disclosure system (from
Arelle 2.45.3) checks only for inconsistent duplicate facts; it does **not**
implement PRH's published SBR validation rules. See *Arelle's FI-PRH
plugin checks duplicates only (honest gap) + what PRH's interface checks*
before promising a validator can gate it. This file is a
working reference, not the legal source; the operative instruments are
named in *The legal instruments: Accounting Act plus two named PRH
decisions* and listed with URLs in *Primary sources: what each
establishes*.

| Situation | Profile | Section |
|---|---|---|
| A Finnish `osakeyhtiö` / `osuuskunta` (or foundation) filing statutory Finnish FAS statements to the Trade Register in digital form | Trade Register digital financial statement: Finnish FAS, national SBR taxonomy | [Profile: Trade Register digital financial statement: Finnish FAS (national SBR taxonomy)](#profile-fas-sbr) |
| An IFRS preparer, or a listed issuer re-filing its ESEF ZIP to the Trade Register alongside the Nasdaq Helsinki OAM | IFRS statements and listed-issuer ESEF re-use | [Profile: IFRS statements and listed-issuer ESEF re-use](#profile-ifrs-esef) |
| A company inside the CSRD/ESRS sustainability-reporting population (the trigger for mandatory digital filing, and a report that is **not** XBRL-tagged) | CSRD sustainability report | [Profile: CSRD sustainability report: assured, filed with the digital statements, not XBRL-tagged](#profile-sustainability-report) |

## Vintage and applicability

### The legal instruments: Accounting Act plus two named PRH decisions

The operative technical requirements live in two PRH decisions, both
**issued 24 June 2026** and published in Finlex under *Viranomaisten
määräyskokoelmat* (authority regulation collections), type = **Määräys**
(regulation/decision). PRH/1087/01/2026 entered into force on issue;
PRH/1088/01/2026 s. 2 states that it **enters into force on 1 July 2026**
(*"Tämä päätös tulee voimaan 1 päivänä heinäkuuta 2026"*), applicable to
sustainability-reporting companies' periods starting on or after
1.1.2026 [S6][S9]. Finlex's metadata field shows 24.6.2026 for both; for
PRH/1088 the decision text governs:

| Decision | Diaarinumero | What it sets |
|---|---|---|
| Päätös … digitaalisten tilinpäätösasiakirjojen ilmoittamisen teknisistä seikoista | **PRH/1087/01/2026** | Technical filing requirements for digital financial-statement documents [S6][S7] |
| Päätös … asiakirjojen ilmoittamisen teknisistä seikoista **(PRH-tunnisteet)** | **PRH/1088/01/2026** | PRH identifiers / taxonomy-adoption (which taxonomy + version to mark up against) [S7][S9] |

Finlex metadata for **PRH/1087/01/2026**: Antopäivä (issued) 24.6.2026;
Voimaantulo (in force) 24.6.2026; the operative text is a downloadable PDF
available in **Finnish and Swedish** [S6]. The legal basis is stated in the
decisions themselves (PRH/1087 s. 7 and PRH/1088 s. 3, *"Sovelletut
säännökset"*): *Kirjanpitolaki (1336/1993) 7 luku 23, 24 ja 25* +
*Kaupparekisterilaki (564/2023) 1 § 3 momentti* [S6][S9]. The *1336/1993*
is a misprint in the **Finnish decision texts** themselves (and in Finlex's
Finnish metadata); the Swedish texts and s. 1 of each Finnish text give the
Act's correct number, **1336/1997** [S6][S9][S19]. The Finlex detail page
carries this metadata in its server-rendered page payload, so a plain HTTP
fetch reads it; no JavaScript rendering is needed.

These decisions **replaced** PRH's decisions of **19.12.2025**:
**PRH/2287/01/2025** (technical filing, replaced by PRH/1087 s. 6) and
**PRH/2288/01/2025** (PRH identifiers, replaced by PRH/1088 s. 2) [S6][S9].
Neither 2025 decision is listed in Finlex's PRH collection for 2025. Earlier,
a PRH decision **entered into force on 31.5.2024** and applied to
financial-statement notifications for financial periods starting in 2024
[S21]; its diary number was not found in the sources read (Not verified
against Finlex; included pending citation).

> **Full extraction.** Both decision PDFs have been read in full
> (PRH/1087 ss. 1-8, PRH/1088 ss. 1-4) [S6][S9]. Where this file quotes a
> clause, the quote is verbatim from those PDFs.

### The two-stage mandate: keep these distinct

The single most important distinction in this regime, and the one most
easily conflated:

1. **Digital (XHTML) filing directly to the Trade Register** has been
   **mandatory** for **sustainability-reporting (CSRD-scope) companies
   for financial periods starting in 2024 onward** (first filed in 2025):
   PRH's 31.5.2024 decision applied to notifications for periods starting
   in 2024 [S21], and PRH states such companies "should submit their
   financial statements without the taxonomy in XHTML format for financial
   periods starting in 2024 and 2025" [S8]. PRH's 21 May 2025 notice states
   filing the digitilinpäätös "is mandatory for sustainability-reporting
   large companies from this year onwards and voluntary for other limited
   companies" [S3]; "this year" is the filing year 2025. These companies
   can **no longer file financial statements via the tax return**; they
   must file directly with the Trade Register [S1].
2. **Structured taxonomy markup** (PRH identifiers / iXBRL tagging against
   a taxonomy) is **mandatory only for financial periods starting on or
   after 1 January 2026** [S1][S4]. For periods that began in 2024 and
   2025, sustainability-reporting companies could still submit XHTML
   **without PRH identifiers**: digital format, but not yet
   taxonomy-tagged [S4][S8].

So: **FY2024 and FY2025** = digital XHTML filing mandatory, untagged
permitted; **FY2026+** = full structured iXBRL markup mandatory. Do not
declare an FY2024 or FY2025 XHTML deposit defective for lacking
PRH-identifier markup; that requirement had not yet cut in.

For **all other limited companies**, filing digital financial statements
is **voluntary** "for the time being" [S1], but a broader mandate has now
passed Parliament: **government bill HE 96/2026 vp** (*Hallituksen esitys
eduskunnalle laeiksi kirjanpitolain, kaupparekisterilain 11 §:n ja
tilintarkastuslain muuttamisesta*, given to Parliament 21 May 2026; Finlex
<https://www.finlex.fi/fi/hallituksen-esitykset/2026/96>; TEM project
TEM027:00/2025) proposes amending the Accounting Act, Trade Register Act
§ 11 and Auditing Act to make digital preparation and registration of the
financial statements and management report (XHTML, with the data PRH
designates tagged in iXBRL) **mandatory for a "digitaalisesti raportoiva
kirjanpitovelvollinen"**. Proposed **KPL 3:8 § 2 mom** defines that as an
entity registered as an `osakeyhtiö`, and an `avoin yhtiö` /
`kommandiittiyhtiö` whose partners (in a `kommandiittiyhtiö`, the general
partners) are such companies, including nested chains of them [S18].

Two carve-outs, and they are **not** the same kind:

- **Hard exclusion.** Proposed **KPL 3:8 § 4 mom** disapplies the
  digitally-reporting-entity provisions to **luottolaitokset** (credit
  institutions), **vakuutusyhtiöt** (insurance companies),
  **työeläkeyhtiöt** (employment-pension companies) **and their branches**,
  even though those are `osakeyhtiö`-form entities. "All limited companies"
  therefore overstates the bill [S18]. As amended by the Commerce
  Committee (TaVM 23/2026 vp) and adopted, the exclusion is wider: it also
  covers **sijoituspalveluyritykset** (investment firms),
  **rahastoyhtiöt** (fund management companies), **talletuspankkien
  yhteenliittymät** (deposit-bank amalgamations), entities controlled by
  companies belonging to them, companies consolidated into a credit
  institution's or insurance company's consolidated financial statements,
  and the branches of all of these [S22].
- **Not mandatory, but permitted.** `osuuskunnat`, `asunto-osakeyhtiöt`,
  `säätiöt`, `yhdistykset` and other private-law legal persons fall outside
  the mandate (*"ei koskisi pakottavana"*), but proposed **KPL 3:9 § 6 mom**
  lets them use the digital form for register filing once PRH issues a
  decision governing the procedure for that legal form [S18].

Sustainability-reporting companies stay governed exhaustively by Accounting
Act ch. 7, not by these proposed provisions. The bill implements Directives
(EU) 2017/1132, (EU) 2019/1151 and **(EU) 2025/25** (the second digital
directive, amending 2009/102/EC and (EU) 2017/1132) [S18]. Phasing runs from
financial years starting **1 Jul 2027** (**1 Jul 2028** for
digitally-reporting entities with no obligation to appoint an auditor),
unchanged by the committee [S18][S22]. Status: referred to the Commerce
Committee (talousvaliokunta) 27 May 2026; committee report **TaVM 23/2026
vp** of 2.10.2026 approved the bill **with amendments**; Parliament
completed the second reading on **13.10.2026** (*"Asian käsittely
päättyi"*), Parliament's reply **EV 140/2026 vp** [S22]. As of 2026-10-15
the act **awaits presidential confirmation** and Finlex publication, so
filing stays voluntary until it applies. The committee's amendments also
repeal Accounting Act **ch. 7 s. 24**, extend the Trade Register Act
amendment to **§ 31**, and require PRH to publish the taxonomy decision for
a reporting calendar year by the end of June of that year [S22].

### DTS and vintages

Which taxonomy release to load, where it lives, and what PRH accepts.
Vocabulary and column order are fixed in `references/dts.md`
§ Vocabulary. Verified 2026-08-21 and re-verified 2026-10-15 by
downloading the package [S23]. Two facts the rest of this file does not
make explicit: the national SBR taxonomy is a **Eurofiling DPM / Table
Linkbase** framework (coded metrics such as `fi_met:ei661` and dimensions
from the `suomi.fi` dictionary, one directory per table with `-rend.xml`
breakdowns, `find:filingIndicator` values that name the tables filed, as
PRH's own sample instances show), not a presentation-tree taxonomy; and
**no entry-point URI dereferences** (`http://www.valtiokonttori.fi/…`
returns 403), so resolution is by the package catalog only [S23].

| Release | Entry point(s) | Package | Valid time | Accepted at deposit | Status | Source |
|---|---|---|---|---|---|---|
| **`SBR-DPM-2025-12-31_fix_2026-02-19`** | `http://www.valtiokonttori.fi/fi/fr/xbrl/crr/fws/oytp/kpl-2016-12/2025-10-16/mod/oytp_gaap_{ind,con}.xsd` (note the entry-point date, 2025-10-16) (companies); `lstp_*` under `…/lstp/tiltoia_2018/2025-10-16/`; `vytp_*` under `…/vytp/stmtpa_2016/2025-10-16/`; foundations `stp/` and `stk/` still at `…/kpl-2016-12/2022-09-30/` ("ei päivitetty vuonna 2025") | `https://avoindata.suomi.fi/data/dataset/644a8ee5-1de5-4f9d-a7bf-ef5edfcb619a/resource/0f00c1d5-cc7b-4159-909d-05df806de1c6/download/sbr-dpm-2025-12-31_fix_2026-02-19.zip` (200; its manifest still says `tp:version` `SBR-DPM-2025-12-31`) | financial periods starting on or after **1 Jan 2026** | the version PRH names for markup | current | [S9][S20][S23] |
| `SBR-DPM-2025-12-31` | same modules | the unfixed zip on the same dataset page | superseded before use | labelled "VANHA VERSIO, ÄLÄ KÄYTÄ" (old version, do not use); "PRH ei tue tätä taksonomiaversiota vastaanottorajapinnassa" (not supported by PRH's interface) | withdrawn | [S23] |
| `SBR-DPM-2022-09-30` (`kpl-2016-12/2022-09-30`) | `…/oytp/kpl-2016-12/2022-09-30/mod/oytp_gaap_{ind,con}.xsd`, also shipped inside the current package | current package (and its own dataset resource) | periods starting in 2024 and 2025 | listed by PRH for those periods | legacy, supported | [S20][S23] |
| `kpl-2016-12/2019-11-06`, `2019-03-28` | `…/oytp/kpl-2016-12/<date>/mod/oytp_gaap_{ind,con}.xsd`, shipped inside the current package | current package | older periods | **not listed** on PRH's applicable-versions page; acceptance not verified against PRH's interface (honest gap) | legacy | [S20][S23] |
| IFRS Accounting Taxonomy 2025; ESEF 2024, ESEF 2025 | IFRS Foundation and ESMA entry points (`references/esef.md` § DTS and vintages); ESEF 2024 as listed by PRH: `https://www.esma.europa.eu/taxonomy/2022-03-24/esef_cor.xsd` / `esef_all.xsd`; ESEF 2025: `https://www.esma.europa.eu/taxonomy/2025-03-27/esef_cor.xsd` | | per period | IFRS 2025 (all entry points) for periods starting 2025 and 2026 (IFRS not in use for 2024 periods); ESEF 2024 for periods starting 2024 and 2025; ESEF 2025 for periods starting 2026 | current | [S20] |

PRH's cadence rule: it confirms the company-financial-reporting parts of
the SBR specification annually by year-end, and the confirmed
specification applies to periods beginning the following year. Note that
the entry-point date (`2025-10-16`), the package name (`2025-12-31`) and
the fix date (`2026-02-19`) are three different strings for one release;
select by the package, not by a date template.

### Bi-temporal cheatsheet: which vintage applies to which period

As with every iXBRL regime, ask for each rule: *was this in force when
this report was prepared?* Read the period from `<xbrli:period>`, not
today's date.

| Rule / obligation | Applies to periods | Notes |
|---|---|---|
| Digital (XHTML) filing **mandatory** for sustainability-reporting companies | periods starting in **2024** onward | Can no longer file FS via tax return; file directly to Trade Register [S1][S8][S21]. |
| Structured **taxonomy markup** (PRH identifiers) mandatory | periods starting **on/after 1 Jan 2026** | FY2024 and FY2025 permitted XHTML **without** PRH identifiers [S1][S4][S8]. |
| **SBR-DPM-2025-12-31_fix_2026-02-19** is the SBR version to mark up FAS statements against | periods starting **1 Jan 2026** at latest | PRH/1088/01/2026 s. 1 names this package by name; the unsuffixed `SBR-DPM-2025-12-31` is withdrawn on avoindata.fi as *"VANHA VERSIO, ÄLÄ KÄYTÄ"* [S2][S9]. |
| ESEF ZIP **also** filed to the Trade Register (not only to the OAM) | financial year starting **2024** onward | Listed issuers re-use their ESEF artifact [S2][S3]. |
| **Law 555/2026** narrows CSRD scope (turnover >€450M **and** >1,000 employees on average, **in both the last completed and the immediately preceding financial year**) | periods starting **on/after 1 Jul 2026** (opt-in from 1 Jan 2026) | In force 30 Jun 2026; PRH repealed & replaced both decisions [S7] (see *The 2026 scope change: law 555/2026 (supersedes older ≥500-employee framing)*). |
| FY2026 **entry-trigger**: a company that *becomes* sustainability-reporting-obligated on/after 1 Jul 2026 | its FS for periods starting **on/after 1 Jul 2026** | The decision applies from that entry point (PRH/1088/01/2026 s. 2) [S4][S9]. |

When uncertain, **state the vintage you are applying** before declaring a
defect. "This lacks PRH-identifier markup, which the PRH decision requires
for periods starting on/after 1 Jan 2026" is reviewable; "this is
untagged, therefore wrong" is not. For FY2024 and FY2025 it is permitted.

<a id="profile-fas-sbr"></a>

## Profile: Trade Register digital financial statement: Finnish FAS (national SBR taxonomy)

### Who files, to whom, under what law

Finnish limited companies and co-operatives may file their statutory
financial statements with the Trade Register in machine-readable digital
form. A digital financial statement has **two parts**, a human-readable
part (text and numbers as usual) and a machine-readable part, built from
a standardised structure (a **taxonomy**) using **Inline XBRL (iXBRL)**;
the file is **XHTML** web format [S1]. The document must be genuinely
structured against a taxonomy: PRH states that the XHTML format without
underlying structure does not yet allow effective use of the data
(*"XHTML-muoto ilman taustalla olevaa rakenteisuutta ei mahdollista vielä
tietojen tehokasta käyttöä"*), so the data must be standardised by a
taxonomy [S25]. An earlier PRH wording, "it is not enough to save Word
documents in XHTML file format", is no longer on PRH's pages as read on
2026-10-15 (Not verified against [S1]; replaced by the [S25] wording).

- **Filer:** `osakeyhtiö` (limited liability company) and `osuuskunta`
  (co-operative). The interface also accepts foundations'
  (`säätiö`) iXBRL annual reports [S5].
- **Recipient / register:** the **Finnish Trade Register**
  (kaupparekisteri), operated by PRH. Once registered, the data become
  public in PRH's **Virre** information service [S1].
- **Statutory basis:** PRH's power to require the digital format and the
  markup is in the **Accounting Act (Kirjanpitolaki 1336/1997)**: ch. 7 s.
  23 for the markup decision, and ch. 7 ss. 22–24 (and 24a) for the
  technical format of documents entered in the Trade Register [S4][S8]. The
  operative technical requirements are set in two **PRH decisions**
  (see *The legal instruments: Accounting Act plus two named PRH decisions*).
  Forward note: the HE 96/2026 act as adopted **repeals ch. 7 s. 24**
  (not yet in force as of 2026-10-15), one of the bases both PRH decisions
  cite; recheck their legal basis once it applies [S22].

### The national SBR taxonomy: modules, distribution, cadence

**(A) National SBR taxonomy, for Finnish FAS statements.** "SBR" =
Standard Business Reporting; expressed in XBRL as XML schema files plus
linkbases [S2]. **PRH maintains** the company-financial-reporting modules;
the **State Treasury (Valtiokonttori)** maintains the municipalities /
wellbeing-services-counties modules [S2]. Company-reporting modules in the
current SBR version [S2]:

| Module | Covers |
|---|---|
| **OYTP** | Limited companies' and co-operatives' financial-statement reporting (**the core module** for ordinary `osakeyhtiö` / `osuuskunta`) |
| STK | Foundations' report of operations (Säätiöiden toimintakertomus) |
| STP | Foundations' financial statements |
| VYTP | Insurance companies' financial-statement reporting |
| LSTP | Credit institutions' and investment firms' financial-statement reporting |

Distribution and cadence:

- Published on **`avoindata.fi`** as the *SBR-taksonomia* open-data dataset
  (with supporting guidance) [S2]; the interface page also directs
  software makers to the **Valtiokonttori** site for the LLC
  financial-statement taxonomy [S5].
- **Annual cadence:** PRH confirms the company-reporting SBR parts each
  year by year-end; the confirmed spec applies to periods **starting the
  following year** (e.g. the spec confirmed end-2025 must be used for
  periods starting 1.1.2026) [S2][S4]. A company must always use the
  **latest** spec approved for the period (it may re-use the prior year's
  template while preparing) [S2].
- **Currently supported SBR versions:** **SBR-DPM-2025-12-31_fix_2026-02-19**
  (apply at latest from periods starting 1.1.2026; PRH/1088/01/2026 s. 1
  names this package by name), plus legacy **SBR-DPM-2022-09-30**
  (`kpl-2016-12/2022-09-30`), which PRH's applicable-versions page lists
  for periods starting in 2024 and 2025 [S9][S20]. The older
  `kpl-2016-12/2019-11-06` and `2019-03-28` entry points still ship inside
  the package but are **not listed** by PRH; whether PRH's interface still
  accepts them is not verified (honest gap) [S20][S23]. The package
  published 31.12.2025 as `SBR-DPM-2025-12-31` is still on avoindata.fi,
  labelled *"VANHA VERSIO, ÄLÄ KÄYTÄ"* and not supported by PRH's
  interface. Selecting it by that shorter name picks the withdrawn package
  [S23].

<a id="profile-ifrs-esef"></a>

## Profile: IFRS statements and listed-issuer ESEF re-use

### Which taxonomy applies

**(B) IFRS taxonomy (IFRS Foundation), for IFRS statements.** Mark up
with the **IFRS Accounting Taxonomy version approved by the IFRS
Foundation for the reporting period** (PRH/1088/01/2026 s. 1 para 2);
PRH's applicable-versions page lists **IFRS Accounting Taxonomy 2025**
(all entry points) for periods starting in 2025 and 2026, and IFRS as not
in use for periods starting in 2024 [S4][S9][S20].

**(C) ESEF taxonomy (ESMA), for listed issuers' consolidated figures.**
Governed by the EU ESEF RTS (see `references/esef.md`); ESEF statements go to the
**Nasdaq Helsinki OAM** and, from the financial year starting 2024, **also
to the Trade Register** [S2]. PRH lists **ESEF 2024** (entry points
`…/taxonomy/2022-03-24/esef_cor.xsd` and `esef_all.xsd`) for periods
starting in 2024 and 2025, and **ESEF 2025** (`…/taxonomy/2025-03-27/esef_cor.xsd`)
for periods starting in 2026 [S20].

### Packaging: the ESEF ZIP re-used for the Trade Register

**ESEF listed companies re-use their ESEF artifact**: they file the
digitilinpäätös to the Trade Register **as an ESEF package in ZIP form**
(*ESEF-pakettina ZIP-muodossa*) [S3][S8]. PRH publishes an example of the
ESEF ZIP internal structure [S8]:

```text
<LEI>.zip
└── <report-package folder>/          # PRH example: acme-x42-submission-2022/
    ├── META-INF/
    │   ├── reportPackage.json
    │   ├── taxonomyPackage.xml
    │   └── catalog.xml
    ├── <taxonomy folder>/            # PRH example: xbrl.example.com/v1/
    │   ├── taxonomy.xsd
    │   └── taxonomy-linkbase.xml
    ├── reports/
    │   └── report-1.html
    ├── companyprofit.xhtml           # profit-use decision (free-form XHTML)
    ├── generalmeetingdecision.xhtml  # adoption-date decision (free-form XHTML)
    └── <auditreport>.xhtml           # if applicable; from PRH's prose, not
                                      # part of its published example tree
```

Note the level PRH's own example shows and that is easy to collapse: a
**single top-level report-package directory** sits between the ZIP and
`META-INF/`, and the free-form attachments sit **inside that directory**,
not at the ZIP root. That the XBRL Report Packages specification requires
exactly one such top-level directory is not verified against the
specification text in this file's sources (honest gap; check
`references/esef.md` or the specification before relying on it).

Packaging rules from the PRH example [S8]:

- The free-form adoption-date and profit-decision documents (and any audit
  report) are attached **in XHTML to the main file of the ZIP package**
  (PRH's wording), **not** to the `reports/` folder. Reading "main" as that
  single top-level report-package directory, **not** the ZIP root, follows
  PRH's example tree; PRH's prose does not say it.
- **If you add PDF files to the ZIP you cannot file it via ytj.fi** [S8].
- **Filenames must not contain `å`, `ä` or `ö`** [S8].
- **File naming:** "The PRH does not have any requirements concerning the
  naming of reporting packages." PRH points to ESMA's ESEF Reporting
  Manual, which **recommends** `{base}-{date}-{version}-{lang}.xhtml` (or
  `.html`): base = LEI or name (max 20 chars), date = period end
  `YYYY-MM-DD`, version starting at 1 and incremented on resubmission,
  lang = `fi` or `sv` [S8]. A different name is **not** a PRH defect.

### Relation to EU reporting: ESEF coexistence and the CSRD/ESRS trajectory

Delta-only: ESEF mechanics live in `references/esef.md`; the Finnish
overlays are in *Which taxonomy applies* and *Packaging: the ESEF ZIP
re-used for the Trade Register* above.

- **ESEF / Transparency-Directive transposition.** The ESEF RTS (**Reg (EU)
  2019/815**) is directly applicable; the Transparency Directive is transposed
  in the **Securities Markets Act**, with **FIN-FSA** as NCA and **Nasdaq
  Helsinki** as OAM (see *Stakeholders: the institutional map*) [S14].
  **Coexistence:** listed issuers file the ESEF
  ZIP to the Nasdaq OAM and re-file it to the Trade Register (from FY2024).
  The national FAS regime does **not** re-tag the ESEF markup; it re-receives
  the tagged report unchanged but the Trade-Register ZIP additionally carries
  the required free-form XHTML attachments (adoption date, profit/surplus-use
  decision, audit report; see *Packaging: the ESEF ZIP re-used for the
  Trade Register*) [S2][S3].
- **CSRD / ESRS trajectory.** Finland transposed the CSRD; scope was
  **narrowed by law 555/2026** (see *The 2026 scope change: law
  555/2026*). ESRS sustainability **mark-up is not yet required**: no ESRS
  XBRL taxonomy has been adopted (see *Filing channels, signatures,
  deadline, tax forwarding, language*) [S8].
- **Directive (EU) 2026/470 (Omnibus I).** Of **24 Feb 2026**, OJ L 2026/470
  publ. **26.2.2026**, **in force 18 March 2026** (20th day after publication);
  amends Dirs 2006/43/EC, **2013/34/EU**, (EU) 2022/2464, 2024/1760 [S13].
  **Art. 2 point (9) replaces Art. 29d of the Accounting Directive
  (2013/34/EU)**, the digital-format/mark-up article the CSRD inserted. Both
  paragraphs of the substituted Art. 29d provide that **until such rules on
  the marking-up are adopted by way of Delegated Regulation (EU) 2019/815,
  undertakings shall not be required to mark up their sustainability
  reporting** [S13]; recital 24 is the preambular explanation of that
  enacting text, not its source. This **expressly suspends the ESRS digital-tagging
  obligation at EU level**, matching PRH's national position (see *Filing
  channels, signatures, deadline, tax forwarding, language*). Art. 2
  point (11) also lets Member States provide that management-body members
  **do not have collective responsibility** for ensuring that the
  (consolidated) management report is prepared in accordance with
  Art. 29d [S13].

<a id="profile-sustainability-report"></a>

## Profile: CSRD sustainability report: assured, filed with the digital statements, not XBRL-tagged

### The 2026 scope change: law 555/2026 (supersedes older ≥500-employee framing)

Any description of Finnish CSRD scope as "large listed non-financial
companies; PIEs with ≥500 average employees; parents of such PIE groups"
is **pre-2026 and now superseded.** The Accounting Act amendment
**555/2026** (kirjanpitolain muutokset 555/2026), confirmed by the
President of the Republic and **in force 30 June 2026**, **reduced** the
population obliged to do sustainability reporting [S7]. It implements
Directive (EU) 2026/470 ("Omnibus I"), which law 555/2026 itself cites
[S13][S19]. Law 555/2026 was given on 16.6.2026 and published on
23.6.2026 [S19].

- **New threshold:** a sustainability report must be prepared and filed
  only if, **in both the last completed and the immediately preceding
  financial year** (*"viimeksi päättyneellä ja sitä edeltäneellä
  tilikaudella"*), the company or group parent had **on average more than
  1,000 employees AND turnover of more than €450 million** (Accounting Act
  **ch. 7 s. 1(1)** as amended by law 555/2026) [S7][S19]. The two-year
  condition governs **both** limbs: one qualifying year is not enough, and a
  company that fell below either limit in the preceding year is out of scope.
- **Group-level duty:** Accounting Act **ch. 7 s. 19(1)** applies the same
  two-limb, two-year test at group level: where the group met both limits in
  both years, the group management report must contain a **consolidated
  sustainability report as a separate section**
  (*konsernikestävyysraportti*) [S19].
- **Voluntary commitment:** a company may voluntarily commit to preparing
  an **ESRS-compliant** sustainability report, in which case it must also
  comply with the digital-financial-statement requirements [S7].
- **Timing:** applies to periods starting **on/after 1 July 2026**; a
  company **may** apply the new rules already to periods starting on/after
  1 January 2026 [S7].

As a consequence PRH **repealed** the two earlier digital-FS decisions and
**replaced** them with PRH/1087/01/2026 and PRH/1088/01/2026 (see *The legal
instruments: Accounting Act plus two named PRH decisions*). Under
the new decisions the digital-markup requirement applies to: (a) companies
already sustainability-reporting-obligated before the change and still
obligated; and (b) companies that become obligated from 1 July 2026. It
does **not** apply to companies that are no longer obligated and have not
voluntarily committed [S7].

**The markup requirements themselves are unchanged**: national SBR
taxonomy for FAS statements, IFRS taxonomy for IFRS statements, ESEF
taxonomy for listed companies' consolidated figures [S7] (see *Choosing the
taxonomy family by accounting framework*).

> **Honest gap.** The **post-555/2026 count** of in-scope Finnish
> sustainability-reporting companies (the mandatory digital-filing
> population) is not stated in any primary source read on 2026-10-15; any
> pre-Omnibus estimate is now stale. For context only, the Commerce
> Committee report on HE 96/2026 records about 13,000 digital financial
> statements filed with PRH in 2024 (all filers, voluntary included) and
> about 250,000 companies covered by that bill [S22].

## Jurisdiction-specific invariants

### Packaging and artifact shape: XHTML-in-ZIP, NOT `.xbri`

**All financial-statement documents must be filed in machine-readable web
format (XHTML). PDF is not accepted** [S1][S8]. PRH notes that a Word or PDF
document can be converted to XHTML, and its own pages mention free online
converters [S3][S8]. Do not act on that for a real filing: an unfiled financial
statement is confidential, and it commonly carries personal data of directors
and auditors, so uploading one to a third-party service is a disclosure the
filer has not agreed to. Convert locally, or with a tool the firm has
assessed. The notification maximum size is **200
MB** [S1][S6][S10]. On artifact shape the binding rule is
PRH/1087/01/2026 s. 2: *"Tämän määräyksen mukaan ilmoitettavat asiakirjat
on ilmoitettava XHTML-muodossa tai zip-pakettina"*, so **XHTML alone or a
ZIP package**, and that sentence follows the channel list in s. 2 rather
than attaching to one channel [S6]. PRH's web guidance states the
narrower "*tilinpäätös täytyy ilmoittaa XHTML-muodossa ZIP-pakettina*"
[S1][S10]; the ZIP is what PRH's pages expect and what a multi-document
notification needs in practice, but a single XHTML file is what the
closed interface and ytj.fi actually accept (see *Filing channels,
signatures, deadline, tax forwarding, language*) and is **not** a defect.

> **Divergence from the Dutch `.xbri` model.** "At the moment, the PRH
> cannot receive material filed as an XBRI package" (*PRH ei voi
> toistaiseksi vastaanottaa XBRI-pakettina ilmoitettuja aineistoja*)
> [S1][S10], so a converter output profile for Finland emits **XHTML, in a
> plain ZIP where the notification carries more than one document, and
> never a `.xbri`**. Whether or when PRH will accept `.xbri` is
> **unknown**: no roadmap was found.

**Closed-interface format rule: what may stay plain XHTML.** Under PRH's
**closed interface** (PRH/1087/01/2026 s. 2(a)), copies of the financial
statements and of the documents registrable with them go in **iXBRL (Inline
XBRL) in XHTML**. The **toimintakertomus** (management report), the
**tilintarkastuskertomus** (audit report) and the **kestävyysraportin
varmennuskertomus** (sustainability assurance report) may nonetheless be
included in the notification as **plain XHTML** *for as long as PRH has not
confirmed PRH identifiers (a taxonomy) applicable to those sections of the
financial-statement notification* (s. 3) [S6]. Where a document is XHTML
prepared in iXBRL, the data must be presented according to the applicable
taxonomy PRH has prescribed [S6]. The carve-out list is **exactly those
three documents**; it does **not** reach the auditor's statement under
Securities Markets Act ch. 7 s. 8(4) (item 4 of s. 1 of the decision) [S6].

> **Read the carve-out through the Swedish text.** The Finnish sentence
> carries a drafting double negative, "*jollei PRH **ei** ole vahvistanut
> näihin tilinpäätösilmoituksen osioihin soveltuvia PRH-tunnisteita
> (taksonomiaa)*", which, read literally, inverts the rule. The equally
> authentic Swedish text resolves it: "*om PRS **inte har fastställt**
> PRS-identifieringar (taxonomi) som lämpar sig för de här avsnitten i
> bokslutsanmälan*" [S6].

**Required attachments (free-form XHTML in the package).** The notification
must also state the **date the statements were adopted** and the
**decision on the use of the company's profits / co-operative surplus**;
the general-meeting minutes need **not** be attached [S1][S8].

**What must be filed (PRH/1087/01/2026 s. 1).** A sustainability-reporting
company, or one committed to sustainability reporting, files copies of
these documents where prepared: (1) the financial statements; (2) the
management report including the sustainability report; (3) the audit
report; (4) the auditor's statement under Securities Markets Act (746/2012)
ch. 7 s. 8(4); (5) the sustainability assurance report. The notification
also states: (6) the Business ID (Y-tunnus, EUID or LEI); (7) the date the
financial statements were adopted; (8) the general meeting's decision on
the company's profit, or the co-operative meeting's decision on the use of
surplus [S6].

### Choosing the taxonomy family by accounting framework

Three taxonomy families, chosen by **accounting framework** [S2][S4]:

**Mixed-basis rule.** If the **consolidated** statements are IFRS and the
**parent's own** statements are FAS, tag the consolidated with the **IFRS**
taxonomy and the parent with the **SBR** taxonomy [S2]. The decision's
markup rules do **not** reach information that must be reported under
**ESEF** requirements (PRH/1088/01/2026 s. 1 para 3: *"ei koske
ESEF-vaatimusten mukaan raportoitavia tietoja"*). In practice that is a
listed issuer's consolidated figures, which are marked up with the ESEF
taxonomy.
**IFRS preparers remain in scope**: s. 1 para 2 requires them to mark up
using the **IFRS Accounting Taxonomy confirmed by the IFRS Foundation for
each reporting period**. The parent company's own figures must always be
marked up with either the SBR (FAS) or the IFRS taxonomy [S4][S9].

### Filing channels, signatures, deadline, tax forwarding, language

**Three filing channels** [S1][S5][S3]:

1. **Financial-administration software via PRH's iXBRL REST interface.** A
   **free** REST API for software companies to send digital iXBRL
   statements plus metadata to the Trade Register; PRH provides no end-user
   client, so vendors build the send function. Accepts iXBRL FS from
   limited companies and iXBRL annual reports from foundations (may extend
   later). **Auth:** identify via a **separate authentication server** for
   an access token. **Metadata** (Business ID, period start/end) go in
   **URL parameters** + a **JSON body** (**multipart/form-data** with the
   iXBRL file attached). **Onboarding:** a **contract with PRH** and a PRH
   **test server**; reported at **10–15 person-workdays**; contact
   **digitilinpaatos@prh.fi** [S5]. Voluntary digital filing to the Trade
   Register has been possible **since 2019** [S22], and PRH has used
   automatic decision-making for digital financial-statement notifications
   since **24.4.2019** [S24].
2. **ytj.fi online filing service.** The digitilinpäätös (XHTML) option was
   **added to the renewed ytj.fi service on 21 May 2025** [S3]. In ytj.fi
   you first select that you are filing a digital financial statement
   (XHTML), give the requested data, and attach the required documents as
   **one file in XHTML** (ESEF filers attach the ESEF ZIP). ytj.fi requires
   a **Finnish personal identity code** plus a **Suomi.fi** e-identification
   method (bank credentials or mobile certificate) [S3]. That the service
   is available in Finnish and Swedish only is not verified against [S3]
   or ytj.fi (honest gap).
3. **Exception web form.** By way of exception, credit/insurance
   institutions not required to prepare ESEF statements, and companies that
   cannot sign in to ytj.fi (no Finnish personal identity code), may file
   via an online form (request a link from **digitilinpaatos@prh.fi**).
   This route is **only** for companies with a sustainability-reporting
   obligation [S1]. The decision adds a second ground: *"Jos PRH ei ole
   vahvistanut yrityksen tilinpäätökseen soveltuvia PRH-tunnisteita
   (taksonomiaa), ilmoitusvelvollinen saa tehdä ilmoituksen PRH:n tarjoamalla
   verkkolomakkeella"* (where PRH has confirmed no PRH identifiers that fit
   the company's financial statements, PRH/1087/01/2026 s. 2) [S6].

**Signatures.** Electronic signatures are **not mandatory**. iXBRL
financial statements are legally **copies**; the signed originals stay with
the company and need not be sent separately; signatory information may be
embedded in free-form manner [S1][S5].

**Deadline + tax forwarding.** File with the Trade Register within **eight
months** of the period end; **free** within that window, a **late fee**
applies to overdue filings [S1]. If you file by the **tax-return
deadline**, you do **not** send the statements separately to the Finnish
Tax Administration. **PRH forwards them automatically**; filing after that
deadline may require a separate Tax Administration filing [S1].

**Registration.** Digital statements can be **registered automatically**
(auto-decision); the data then become public in **Virre** [S1][S24]. A
timing of "as early as the next business day" is not verified against
[S1] or [S24] (honest gap).

**Language.** Statements to be registered must be in **Finnish or Swedish**;
they **may also include an English translation** (legal basis Accounting
Act **chapter 3, section 5**, and Finnish Accounting Board statement
2084/3.12.2024) [S8][S19]. The statement text itself was not readable on
2026-10-15 (the Board's site returned HTTP 403); it is cited as PRH cites
it. The report-language metadata value is **`fi`** or
**`sv`** [S8]. The **sustainability report** must be drafted in FI/SV and
**assured** (KRT / audit-firm assurance report attached) [S7][S8]. **XBRL
markup is not yet required** in the sustainability report or its assurance
report. Two independent grounds run in parallel and should not be collapsed
into one: at **EU level**, the Commission has not adopted an **ESRS XBRL
taxonomy** (EFRAG work), and the Art. 29d that Omnibus I Art. 2 point (9)
substitutes suspends the mark-up duty until marking-up rules are adopted
via Reg (EU) 2019/815 [S8][S13];
**nationally**, PRH/1087/01/2026 s. 3 lets the toimintakertomus and the
assurance report stay plain XHTML for as long as PRH has confirmed no
applicable PRH identifiers for those sections [S6]. Because item 2 of s. 1
of that decision places the **kestävyysraportti inside the
toimintakertomus**, it is the national PRH-identifier condition that
actually governs its markup at the Trade Register (see *Packaging and
artifact shape: XHTML-in-ZIP, NOT `.xbri`*).

**Corrections are whole-package resubmissions.** Under PRH/1087/01/2026
s. 5, if a filer reports corrections to the registrable data, **all
documents must be delivered to PRH again as one whole** (*"kaikki
asiakirjat on yhtenä kokonaisuutena toimitettava uudelleen"*), in the
manner set out earlier in the decision: that is, through the same channels
(the closed interface via software, ytj.fi, or the exception web form) and
in the same format (iXBRL in XHTML, or a ZIP package, max 200 MB; ESEF
consolidated statements per s. 4) [S6]. **There is no partial or delta
correction.** The
duty binds companies within Accounting Act ch. 7 s. 1 sustainability
reporting and companies that have committed to sustainability reporting
(s. 1), for documents filed for registration **on or after 1 Jan 2026**
(s. 6); the decision replaces PRH/2287/01/2025 [S6].

**Stale-document correction (PRH web-page guidance, subordinate to s. 5).**
A company that mistakenly filed a **PDF** must **also** file the digital
statement via ytj.fi or the interface; the digital one registers as the
latest version, but the PDF is **not** de-registered and remains in Virre
[S1][S10]. That describes what happens to a legacy PDF filing; it is not
the correction rule itself, which is s. 5 above.

## Validation

### Arelle's FI-PRH plugin checks duplicates only (honest gap) + what PRH's interface checks

**Implementation evidence.** Arelle added a Finland validation plugin,
`arelle/plugin/validate/PRH` ("Validate Finland-PRH", plugin version
0.0.1, disclosure system **`FI-PRH`** / `fi-prh`, validation type `PRH`),
in **2.45.3** (released 2026-09-24). Tag 2.45.2 and earlier, for example
2.39.11, whose `validate/` directory is exactly `CIPC, DBA, EBA, EDINET,
ESEF, FERC, NL, ROS, UK`, have no PRH plugin. As of 2.46.1 the plugin
holds **one rule**, code **`FINLAND-PRH.duplicateFact`**, which reports
inconsistent duplicate facts [S12]. Re-list `arelle/plugin/validate/PRH`
on the release you run before repeating the claim.

Consequences for review and for any converter:

- Arelle's `FI-PRH` disclosure system does **not** implement PRH's SBR
  validation rules, and there is **no** Arelle rule-code family analogous
  to the Dutch `FR-NL-*` (no `FR-FI-*`). **Do not claim Arelle "validates
  PRH SBR compliance"; it does not** [S12].
- **PRH publishes its own SBR validation rules with rule codes.** The
  taxonomy package carries `Validointisäännöt/SBR-DPM-2025-12-31_{OYTP,LSTP,VYTP}_validation rules.xlsx`:
  43 OYTP, 26 LSTP and 23 VYTP rule codes of the form `OYTP_2025_vN.N`
  (for example `OYTP_2025_v16.9`, profit or loss for the year against the
  income-statement items; `OYTP_2025_v19.1`, assets and liabilities
  non-negative), each with a severity (for example `WARNING`) and
  FI/SV/EN messages. Since 8.9.2026 avoindata.fi also carries an **SBR
  Conformance Suite** with per-rule valid and invalid iXBRL test reports
  (`OYTP_2026_vN.N`, `LSTP_2026_vN.N`, `VYTP_2026_vN.N`) [S23]. Which of
  these rules PRH's intake interface enforces, and at what severity, is not
  stated in [S5] (honest gap).
- For a **FAS / SBR** filing the deterministic gate is therefore core
  **XBRL 2.1** validity + **iXBRL 1.1** well-formedness/validity +
  **taxonomy-package resolution** (`taxonomyPackage.xml` / `catalog.xml`)
  against the national SBR taxonomy + calculation/dimension consistency,
  checked against PRH's published rule workbooks and conformance suite,
  **plus** whatever PRH's own intake interface enforces. Arelle's `FI-PRH`
  adds only the duplicate-fact check.
- For the **IFRS / ESEF re-use path**, the standard Arelle **ESEF plugin
  is present** [S12] and is the right profile, because Finnish listed
  issuers re-use their ESEF ZIP for the Trade Register filing. Validate
  that path **exactly as an ESEF filing** (`references/esef.md`, and
  `scripts/validate_with_arelle.sh <zip> esef`). Use the calculation
  behaviour consistent with the taxonomy in play (IFRS/ESEF for that
  path); the SBR path has no PRH-published Arelle calc profile, so rely on
  core-spec calc validation only.

```bash
# FAS / SBR path — Arelle's FI-PRH disclosure system (2.45.3+) adds only a
# duplicate-fact check; run CORE,
# with the SBR taxonomy package supplied for DTS resolution (the extra
# args pass through to arelleCmdLine — without --packages, offline
# schemaRef resolution fails and you get spurious xbrl.5.1.5 errors):
scripts/validate_with_arelle.sh statements.xhtml core --packages <SBR-taxonomy-package>.zip
#   or, directly:
arelleCmdLine --plugins inlineXbrlDocumentSet \
              --packages <SBR-taxonomy-package>.zip \
              -f statements.xhtml --validate
#   (SBR taxonomy published on avoindata.fi; also hosted by Valtiokonttori — see
#    "The national SBR taxonomy: modules, distribution, cadence")

# IFRS / ESEF re-use path — the deposited artifact IS the ESEF ZIP.
scripts/validate_with_arelle.sh <LEI>.zip esef
```

**What PRH's intake interface validates (published).** On submission the
interface checks that (a) the supplied **metadata are correct and match
the iXBRL file content**, and (b) the financial statements / annual report
have the **correct structure**. PRH states that "in the future, the
interface will also check the iXBRL file content more carefully"; i.e.
**deeper content validation is not yet in place** [S5]. On success the
interface returns a success response; otherwise an **error code plus a
description of the error reason**; the interface is generally open 24/7
[S5].

> **Honest gaps.** (1) PRH's interface error codes are not published in
> the sources read; PRH's published rule codes are the SBR validation-rule
> codes above [S23], and whether the interface returns those codes is not
> verified against [S5]. (2) Corroborating the early stage: PRH's
> open-data digital-FS API exposes only P&L and balance-sheet detail, only
> for iXBRL-format filings, which are "about 5 per cent of all financial
> statements" [S11].

## Review workflow

### A pragmatic PRH review pass, in order

When asked to review a Finnish digital financial statement, walk this in
order; each step depends on the prior being clean.

1. **Pin basis + vintage.** FAS/SBR vs IFRS vs ESEF (see *Choosing the
   taxonomy family by accounting framework*), and the period start date
   (see *Bi-temporal cheatsheet: which vintage applies to which period*).
   FY2024 and FY2025 permit **untagged** XHTML for
   sustainability reporters; the markup obligation is FY2026+ [S1][S4][S8].
2. **Pin the filing obligation.** Sustainability-reporting company under
   the **post-555/2026** threshold (turnover >€450M **and** >1,000
   employees on average, in **both** the last completed and the immediately
   preceding financial year, or a voluntary ESRS committer)? For everyone
   else digital filing is voluntary and its **absence is not a defect**
   [S1][S7][S19].
3. **Choose the validation profile, honestly.** IFRS/ESEF → validate as
   ESEF (`references/esef.md`, plugin present [S12]). FAS/SBR → **core XBRL 2.1 +
   iXBRL 1.1 + SBR taxonomy-package resolution**, checked against PRH's
   published SBR validation rules [S23]. Arelle's `FI-PRH` disclosure
   system (2.45.3+) checks only duplicate facts, so do not report an
   "FI profile" verdict as SBR compliance; see *Arelle's FI-PRH plugin
   checks duplicates only (honest gap) + what PRH's interface checks*.
4. **Check the package shape.** **XHTML, alone or in a plain ZIP**
   (PRH/1087 s. 2 permits either), ≤ **200 MB**, **not** a `.xbri`
   [S1][S6][S10]. ESEF re-use path: adoption-date + profit-decision
   XHTML (and audit report) in the **main folder**, the single top-level
   report-package directory, not the ZIP root and not `reports/`; no PDF
   if it will go via ytj.fi; no `å`, `ä` or `ö` anywhere in the filenames.
   PRH sets **no naming requirement**; ESMA's recommended
   `{base}-{date}-{version}-{lang}` is advisory, not a defect [S8].
5. **Check attachments + assurance.** Adoption date and profit-use /
   surplus decision present as free-form XHTML; minutes **not** required
   [S1][S8]. Sustainability reporters: report in FI/SV, KRT/audit-firm
   assurance report attached; **no** XBRL markup expected in it yet [S7][S8].
   Check the **national** condition, not only the missing ESRS taxonomy: the
   management report, audit report and assurance report may be plain XHTML
   for as long as PRH has confirmed no PRH identifiers applicable to those
   sections (PRH/1087/01/2026 s. 3) [S6].
6. **Content-level review.** No validator confirms fidelity to the source
   statements; read the rendered report as a financial professional
   (`references/conversion.md` §10).

## Authorities and governance

### Stakeholders: the institutional map

Who runs electronic business reporting in Finland, each named once; taxonomy
and ESEF detail stays in *Choosing the taxonomy family by accounting
framework* / *Relation to EU reporting: ESEF coexistence and the CSRD/ESRS
trajectory* (delta-only).

- **Business register / publication organ:** the **Finnish Trade Register
  (kaupparekisteri)**, operated by **PRH**; data become public via **Virre**
  (see *Who files, to whom, under what law*) [S1].
- **Digital-business-reporting programme (SBR-Nederland analogue).** No single
  government "SBR office"; the role is split: **PRH** "is responsible for
  developing structured financial statement reporting" and runs the taxonomy
  **working group** [S17]; the **State Treasury (Valtiokonttori)** maintains
  the municipality and wellbeing-services-county SBR modules [S2]. That it
  also maintains a national "Reporting Code List" from which the SBR
  taxonomy derives is not verified against [S2] or any other source read
  (honest gap). **XBRL Suomi / XBRL Finland** is the XBRL International
  jurisdiction consortium (**facilitated by TIEKE**) [S16].
- **Accounting standards setter:** the **Accounting Board (Kirjanpitolautakunta,
  KILA)**, appointed by the **Ministry of Economic Affairs and Employment
  (TEM)**, issues guidance and statements on applying the Accounting Act
  (Kirjanpitolaki ch. 8 s. 1: *"antaa ohjeita ja lausuntoja
  työ- ja elinkeinoministeriön asettama kirjanpitolautakunta"*) [S19] (e.g.
  statement 2084; see *Filing channels, signatures, deadline, tax
  forwarding, language*) [S8]. TEM's Board page [S15] returned HTTP 403 on
  2026-10-15, so it was not re-read. FAS = Accounting Act + KILA guidance,
  not a private standard-setter.
- **Taxonomy author / cadence:** PRH (company modules) + State Treasury (public
  sector); annual, on **avoindata.fi**; detail in
  *The national SBR taxonomy: modules, distribution, cadence* [S2].
- **Tax authority (structured-filing regime):** the **Finnish Tax
  Administration (Verohallinto)**, which **receives FS data automatically
  forwarded by PRH** when filed by the tax-return deadline; sustainability
  reporters can no longer route FS through the tax return (see *Filing
  channels, signatures, deadline, tax forwarding, language*) [S1].
- **Securities regulator (NCA):** **Finanssivalvonta (FIN-FSA)**, the
  Transparency-Directive competent authority (Securities Markets Act) and
  ESEF supervisor; **Nasdaq Helsinki** is the regulated-market operator
  whose storage is the
  **OAM** [S14] (see *Relation to EU reporting: ESEF coexistence and the
  CSRD/ESRS trajectory*). That FIN-FSA also runs the **EBA/EIOPA**
  prudential regimes (COREP/FINREP, Solvency II) as separate DPM filings,
  **not** part of the digital-FS regime, is not verified against [S14] or
  [S16] (honest gap; [S16] lists only an XBRL Suomi COREP/FINREP working
  group).

**How they interlock.** PRH owns the register *and* the FAS digital-FS pipeline;
the State Treasury maintains the public-sector SBR modules; KILA/TEM set the accounting
*content*; FIN-FSA + Nasdaq own the listed-issuer **ESEF** path PRH merely
**re-receives** (see *Which taxonomy applies* and *Packaging: the ESEF ZIP
re-used for the Trade Register*); Verohallinto is downstream via PRH
forwarding.

## Coverage and known limitations

### When to escalate to primary sources

This file is a reviewer's working reference, not the legal source. Defer
to and cite: the **two PRH decision PDFs** at Finlex [S6][S9] before
quoting any normative clause this file does not already quote verbatim
(both have been read in full, 2026-10-15); the
**PRH digital-FS pages** [S1][S2][S4][S5][S8][S10][S20] for
operative filing/taxonomy/interface/packaging guidance; the **Accounting
Act (Kirjanpitolaki 1336/1997)** ch. 3 s. 5 (language) and ch. 7 ss. 22–24 and 24a
(format + markup power) and **law 555/2026** [S7][S19] at `finlex.fi`; the
**HE 96/2026** act once confirmed and published [S18][S22]; and
**avoindata.fi** / **Valtiokonttori** for the SBR packages, validation
rules and conformance suite [S2][S5][S23] (IFRS/ESEF → `references/esef.md`).

If a question concerns a rule version newer than this file cites, a PRH
interface error code (not published in the sources read; PRH's SBR rule
codes are in [S23]; see *Arelle's FI-PRH plugin checks duplicates only
(honest gap) + what PRH's interface checks*), or whether PRH has begun
accepting `.xbri`, **say so and link the primary source**. Several
load-bearing facts here rest on PRH summary pages rather than the decision
PDFs; treat those as gaps to close, not settled normative text. The cost of
a wrong citation on a regulated filing is high.

## Sources

### Primary sources: what each establishes

All re-read 2026-10-15 unless an entry says otherwise. For any clause of
the two PRH decisions not quoted verbatim in this file, pull the PDFs from
the Finlex media endpoints given in [S6] and [S9].

- **[S1]** PRH, *Digital financial statements of limited liability
  companies to the Finnish Trade Register* (EN):
  <https://www.prh.fi/en/companiesandorganisations/financial_statements/limited_liability_companies_co-operatives_and_other_companies/digital.html>.
  Core regime: who files (sustainability reporters mandatory, others
  voluntary "for the time being"; thresholds >€450M and >1,000 staff);
  iXBRL saved as XHTML; 200 MB ZIP; **PRH cannot accept `.xbri`**;
  8-month free deadline; auto tax-forwarding; signatures optional / filings
  are copies; three channels; exception web form; PDF-then-digital
  correction. Page "Latest update 17.09.2026"; read 2026-10-15.
- **[S2]** PRH, *Tilinpäätöstaksonomiat* (FI):
  <https://www.prh.fi/fi/yrityksetjayhteisot/tilinpaatokset/digitaalinen-tilinpaatosraportointi/taksonomiat.html>.
  SBR governance (PRH company modules; Valtiokonttori municipal/wellbeing);
  modules STK/STP/VYTP/LSTP/**OYTP**; avoindata.fi; annual cadence (example:
  spec confirmed end-2025 used from 1.1.2026); ESEF to Nasdaq and, from
  FY starting 2024, the Trade Register; IFRS-vs-FAS mixed-consolidation
  rule. The per-period version list has moved to [S20]. Read 2026-10-15.
- **[S3]** PRH news 21.5.2025, ytj.fi renewed (FI):
  <https://www.prh.fi/fi/tietoa_prhsta/uutislistaus/tiedotteet/2025/ytj-palvelu-tilinpaatos_21.5.2025.html>.
  Digitilinpäätös option launched 21 May 2025; digital filing mandatory
  for sustainability-reporting large companies "from this year" (the filing
  year 2025), voluntary for others; attach documents as one XHTML file;
  free online converters; ytj.fi needs Finnish personal ID + Suomi.fi;
  listed ESEF filers submit the ESEF ZIP. Read 2026-10-15.
- **[S4]** PRH, *PRH's decision on digital financial statements* (EN):
  <https://www.prh.fi/en/companiesandorganisations/financial_statements/limited_liability_companies_co-operatives_and_other_companies/digital/sustainability-reporting/prh-decision.html>.
  PRH-identifiers markup mandatory for periods starting on/after
  1 Jan 2026; entry trigger for companies obligated from 1.7.2026;
  SBR-DPM-2025-12-31_fix_2026-02-19; FY2025 permitted without PRH
  identifiers; IFRS/ESEF carve-outs; annual taxonomy-approval decision;
  legal basis **Accounting Act ch. 7 s. 23**. Page "Latest update
  14.10.2026"; read 2026-10-15.
- **[S5]** PRH, *Interface for software companies* (iXBRL REST API) (EN):
  <https://www.prh.fi/en/companiesandorganisations/financial_statements/developing-digital-financial-reporting/interface.html>.
  REST iXBRL interface: free; LLC iXBRL FS + foundation iXBRL reports;
  token auth via separate auth server; metadata in URL params + JSON
  multipart/form-data; checks metadata↔content match + "correct structure"
  (deeper checks future); error-code responses; contract + test server;
  10–15 person-workdays; filings are copies. Read 2026-10-15.
- **[S6]** Finlex, technical-filing decision **PRH/1087/01/2026**:
  <https://www.finlex.fi/fi/viranomaiset/maarayskokoelmat/patentti-ja-rekisterihallitus/2026/2>.
  Type Määräys; issued & in force 24.6.2026; legal basis (s. 7) Accounting
  Act ch. 7 §§ 23, 24, 25 + kaupparekisterilaki 564/2023 § 1(3). The
  Finnish text of s. 7 (and Finlex's Finnish metadata) misprints the Act's
  number as *1336/1993*; the Swedish text and the Finnish s. 1 give
  **1336/1997** (see [S19]). FI PDF
  <https://www.finlex.fi/api/media/authority-regulation/1072570/mainPdf/main.pdf>,
  SV twin <https://www.finlex.fi/api/media/authority-regulation/1072569/mainPdf/main.pdf>;
  both read in full (ss. 1-8). **s. 1** (documents and data to file),
  **s. 2** (channels; web-form grounds; XHTML alone or a ZIP; 200 MB),
  **s. 3** (closed-interface format; the plain-XHTML carve-out for the
  toimintakertomus, tilintarkastuskertomus and kestävyysraportin
  varmennuskertomus, conditional on PRH having confirmed no applicable PRH
  identifiers), **s. 4** (ESEF consolidated statements; the text miscites
  the ESEF RTS as "(EU) 2018/815"), **s. 5** (corrections are
  whole-package resubmissions), **s. 6** (applies to documents filed for
  registration on/after 1 Jan 2026; replaces PRH/2287/01/2025 of
  19.12.2025). Read 2026-10-15.
- **[S7]** PRH news 2026, CSRD scope narrowed, law 555/2026 (FI):
  <https://www.prh.fi/fi/tietoa_prhsta/uutislistaus/tiedotteet/2026/kestavyysraportointi-laki-muuttuu.html>.
  Accounting Act amendment **555/2026** in force 30 Jun 2026 narrows
  scope to **turnover >€450M AND >1,000 employees** (the statutory
  two-year condition on both limbs is in the Act itself; see [S19]);
  periods starting on/after 1.7.2026 (opt-in from 1.1.2026); PRH repealed &
  replaced both decisions (**PRH/1088** + **PRH/1087**); markup rules
  unchanged; voluntary
  ESRS commitment triggers digital-FS duties; report assured by KRT. Page
  "Viimeksi päivitetty 25.06.2026"; read 2026-10-15.
- **[S8]** PRH, *How to file a sustainability report …* (EN):
  <https://www.prh.fi/en/companiesandorganisations/financial_statements/limited_liability_companies_co-operatives_and_other_companies/digital/sustainability-reporting/how-to-file.html>.
  Packaging: XHTML only, no PDF; free online converters; report assured,
  in FI/SV; untagged XHTML for periods starting in 2024 and 2025; ESEF ZIP
  internal structure; adoption-date + profit-decision as free-form XHTML in
  the "main file of the ZIP package"; PDF in ZIP blocks ytj.fi; "The PRH
  does not have any requirements concerning the naming of reporting
  packages" (ESMA's `{base}-{date}-{version}-{lang}` is a recommendation);
  language rule (**Accounting Act ch. 3 s. 5**; Board statement
  2084/3.12.2024); format basis ch. 7 ss. 22–24 & 24a; ESRS XBRL taxonomy
  not yet adopted. Page "Latest update 17.09.2026"; read 2026-10-15.
- **[S9]** Finlex, PRH-identifiers decision **PRH/1088/01/2026**:
  <https://www.finlex.fi/fi/viranomaiset/maarayskokoelmat/patentti-ja-rekisterihallitus/2026/3>.
  Title (*…teknisistä seikoista (PRH-tunnisteet)*), issued 24.6.2026;
  **s. 2: enters into force 1.7.2026** (Finlex metadata shows 24.6.2026),
  applicable to periods starting on/after 1.1.2026, and to periods starting
  on/after 1.7.2026 for companies that become sustainability-reporting
  from 1.7.2026; replaces PRH/2288/01/2025 (19.12.2025); legal basis (s. 3)
  Accounting Act ch. 7 §§ 23, 24, 25 + kaupparekisterilaki 564/2023 § 1(3).
  PDF <https://www.finlex.fi/api/media/authority-regulation/1072572/mainPdf/main.pdf>,
  read in full (ss. 1-4).
  **S. 1 paras 2–3** are quoted in this file: IFRS preparers mark up with
  the IFRS Accounting Taxonomy confirmed by the IFRS Foundation for each
  reporting period, and the markup rules "*ei koske ESEF-vaatimusten mukaan
  raportoitavia tietoja*". **S. 1 para 1** names the package
  `SBR-DPM-2025-12-31_fix_2026-02-19` on avoindata.fi for FAS preparers.
  Corroborated by [S4][S7]. Read 2026-10-15.
- **[S10]** PRH, *Osakeyhtiön digitaalinen tilinpäätös* (FI):
  <https://prh.fi/fi/yrityksetjayhteisot/tilinpaatokset/osakeyhtio_ja_osuuskunta_tilinpaatos_kaupparekisteriin/osakeyhtion_sahkoinen_tilinpaatos.html>.
  200 MB XHTML ZIP; **PRH cannot receive `.xbri`**; adoption-date +
  profit-decision required; auto-registration; Virre publicity;
  PDF-then-digital correction. Page "Viimeksi päivitetty 17.09.2026"; read
  2026-10-15. (The entry-trigger rule earlier cited here is no longer on
  this page; it is in [S4] and [S9].)
- **[S11]** PRH open data, *Digital financial statement information API*:
  <https://avoindata.prh.fi/en/info/swagger-ui>.
  Exposes P&L + balance-sheet detail only for iXBRL-format filings, which
  are "about 5 per cent of all financial statements". Read 2026-10-15.
- **[S12]** Arelle source, `arelle/plugin/validate/`
  (<https://github.com/Arelle/Arelle/tree/2.46.1/arelle/plugin/validate>):
  at tag 2.39.11 the directory holds **CIPC, DBA, EBA, EDINET, ESEF, FERC,
  NL, ROS, UK only** (no PRH plugin; tag 2.45.2 likewise). Commit
  `8543c579ee` (2026-09-23, "Add Finland PRH validation plugin") added
  `validate/PRH`, first released in **2.45.3** (2026-09-24): plugin
  "Validate Finland-PRH" v0.0.1, disclosure system `FI-PRH` / `fi-prh`
  (`resources/config.xml`), and in 2.46.1 a single rule,
  `FINLAND-PRH.duplicateFact` (`rules/prh_rules.py`). The ESEF plugin
  covers the IFRS/ESEF re-use path. Read 2026-10-15.
- **[S13]** **Directive (EU) 2026/470** (Omnibus I), OJ L 2026/470, publ.
  26.2.2026: <https://eur-lex.europa.eu/eli/dir/2026/470/oj/eng> (that
  address returned an empty HTTP 202 to automated fetches on 2026-10-15;
  the OJ text was read via the Publications Office at
  <http://publications.europa.eu/resource/celex/32026L0470>, XHTML).
  Of 24 Feb 2026; amends Dirs 2006/43/EC, 2013/34/EU, (EU) 2022/2464,
  2024/1760. **Art. 2 point (9)** replaces **Art. 29d of 2013/34/EU**: until
  mark-up rules are adopted via Reg 2019/815, undertakings **shall not be
  required to mark up** their sustainability reporting (recital 24 explains
  the same point in the preamble). **Art. 2 point (11)** replaces
  Art. 33(1): MS may provide that management-body members do not have
  collective responsibility for ensuring that the (consolidated) management
  report is prepared in accordance with Art. 29d. (18 Mar 2026 in-force =
  20th day after OJ publication, computed from the entry-into-force
  article; the EUR-Lex status field was not readable.) Read 2026-10-15.
- **[S14]** FIN-FSA, issuer disclosure obligation / ESEF:
  <https://www.finanssivalvonta.fi/en/financial-market-participants/capital-markets/issuers-and-investors/disclosure-obligation/>.
  Disclosure obligation under the Securities Markets Act; regulated
  information filed to the OAM, which "is serviced by the Helsinki Stock
  Exchange"; ESEF reporting for listed companies. Read 2026-10-15. It does
  not state that FIN-FSA runs EBA/EIOPA supervisory reporting.
- **[S15]** TEM (Min. of Economic Affairs and Employment), Accounting Board:
  <https://tem.fi/en/accounting-board>. Returned HTTP 403 on 2026-10-15
  (not re-read); the Board's statutory role is confirmed from Kirjanpitolaki
  ch. 8 s. 1 in [S19].
- **[S16]** XBRL Suomi / XBRL Finland: <https://fi.xbrl.org/>. The XBRL
  International jurisdiction consortium (~20 private + public members,
  **facilitated by TIEKE**; nine WGs incl. FAS/tax taxonomy, IFRS-XBRL,
  COREP/FINREP, sustainability). Read 2026-10-15.
- **[S17]** PRH, *Developing digital, structured financial reporting*:
  <https://www.prh.fi/en/companiesandorganisations/financial_statements/digital-financial-reporting.html>.
  "The PRH is responsible for developing structured financial statement
  reporting"; hosts the taxonomy **working group**. Page "Latest update
  09.10.2026"; read 2026-10-15.
- **[S18]** Finlex, government bill **HE 96/2026 vp** (*Hallituksen esitys
  eduskunnalle laeiksi kirjanpitolain, kaupparekisterilain 11 §:n ja
  tilintarkastuslain muuttamisesta*), given to Parliament 21.5.2026:
  <https://www.finlex.fi/fi/hallituksen-esitykset/2026/96>; FI PDF
  <https://www.finlex.fi/api/media/government-proposal/1070036/mainPdf/main.pdf>
  (SV twin RP 96/2026 rd at `…/1070037/…`, not re-read 2026-10-15).
  Proposed **KPL 3:8 § 2 mom** defines the *digitaalisesti raportoiva
  kirjanpitovelvollinen* (osakeyhtiö; avoin yhtiö / kommandiittiyhtiö whose
  partners, or general partners, are such companies); **§ 4 mom** disapplies
  the regime to credit institutions, insurance companies,
  employment-pension companies **and their branches** (widened in
  committee, see [S22]); proposed **KPL 3:8a** (XHTML, PRH decides which
  data carry iXBRL tags); proposed **KPL 3:9 § 6 mom** permits other legal
  forms to file digitally once PRH issues a decision for that form; the
  bill implements Dirs (EU) 2017/1132, (EU) 2019/1151 and **(EU) 2025/25**;
  entry into force 1.7.2027, applied to financial years starting on/after
  1.7.2027 (1.7.2028 where no auditor must be appointed); TEM project
  TEM027:00/2025. Status: see [S22] (eduskunta open data, VaskiData record
  341349). Read 2026-10-15.
- **[S19]** Finlex, **Laki 555/2026** amending the Accounting Act
  (given 16.6.2026, published 23.6.2026, in force 30.6.2026, applied to
  periods starting on/after 1.7.2026 with opt-in from 1.1.2026; implements
  Directive (EU) 2026/470):
  <https://www.finlex.fi/fi/laki/alkup/2026/20260555> (now redirects to
  `/fi/lainsaadanto/saadoskokoelma/2026/555`), and the consolidated
  **Kirjanpitolaki 1336/1997** carrying the amendment:
  <https://www.finlex.fi/fi/lainsaadanto/1997/1336>.
  **Ch. 7 s. 1(1)**: the chapter applies to an undertaking or group parent
  that, "*viimeksi päättyneellä ja sitä edeltäneellä tilikaudella*" (in the
  last completed **and** the immediately preceding financial year), had on
  average more than 1 000 employees **and** turnover of more than €450
  million; Swedish parallel text "*under den senast avslutade och den
  föregående räkenskapsperioden*". **ch. 7 s. 19(1)** applies the same
  two-limb, two-year test at group level and requires the
  *konsernikestävyysraportti* as a separate section of the group management
  report. **Ch. 3 s. 5**: financial statements and management report in
  Finnish or Swedish. **Ch. 8 s. 1**: the Accounting Board, appointed by
  TEM, gives guidance and statements on applying the Act. Note the Act's
  number is **1336/1997**, which 555/2026 itself cites, not the
  *1336/1993* misprinted in the Finnish texts of the PRH decisions
  ([S6][S9]). Read 2026-10-15.
- **[S20]** PRH, *Sovellettavat taksonomiaversiot raportointikausittain*
  (applicable taxonomy versions per reporting period) (FI):
  <https://www.prh.fi/fi/yrityksetjayhteisot/tilinpaatokset/digitaalinen-tilinpaatosraportointi/taksonomiat/sovellettavat-taksonomiaversiot.html>.
  Per-period tables by legal form: SBR-DPM-2022-09-30 for periods starting
  in 2024 and 2025, SBR-DPM-2025-12-31_fix_2026-02-19 for 2026 (OYTP, and
  VYTP/LSTP for insurers and banks); IFRS 2025 for 2025 and 2026 (not in use
  for 2024); ESEF 2024 (2022-03-24 entry points) for 2024 and 2025, ESEF
  2025 (2025-03-27) for 2026; full entry-point URLs. Page "Viimeksi
  päivitetty 17.09.2026"; read 2026-10-15.
- **[S21]** PRH newsletter 5/2024, *PRH:lta päätös kaupparekisteriin
  ilmoitettavien asiakirjojen teknisistä vaatimuksista* (FI):
  <https://www.prh.fi/fi/tietoa_prhsta/ajankohtaista/uutiskirjeet/prhn_uutiskirje/prhn-uutiskirje-52024/prhlta-paatos-kaupparekisteriin-ilmoitettavien-asiakirjojen-teknisista-vaatimuksista.html>.
  "*Päätös tuli voimaan 31.5.2024. Päätöstä sovelletaan vuonna 2024
  alkavia tilikausia koskeviin tilinpäätösilmoituksiin kaupparekisteriin.*"
  Read 2026-10-15.
- **[S22]** Eduskunta, processing record for HE 96/2026 vp:
  <https://www.eduskunta.fi/asiat-ja-aanestykset/valtiopaivaasiat/HE%2096%2F2026%20vp>,
  and Commerce Committee report **TaVM 23/2026 vp** (2.10.2026) via
  Eduskunta open data:
  <https://avoindata.eduskunta.fi/api/v1/tables/VaskiData/rows?columnName=Eduskuntatunnus&columnValue=TaVM%2023%2F2026%20vp>.
  Referred to talousvaliokunta 27.5.2026; committee approved the bill with
  amendments 2.10.2026; first reading 7.10.2026; second reading completed
  13.10.2026 (*"Asian käsittely päättyi"*); Parliament's reply EV 140/2026
  vp. The committee's amendments widen the KPL 3:8 § 4 mom financial-sector
  exclusion, repeal KPL ch. 7 s. 24, extend the Trade Register Act
  amendment to § 31, and set PRH's taxonomy-decision deadline at the end of
  June of the reporting calendar year. The report also records that
  voluntary digital filing has been possible since 2019, about 13,000
  digital financial statements in 2024, and about 250,000 companies in
  scope. Read 2026-10-15.
- **[S23]** avoindata.fi, *SBR-taksonomia (tilinpäätöskokonaisuuksien
  päivitykset)* dataset (PRH):
  <https://avoindata.suomi.fi/data/api/3/action/package_show?id=644a8ee5-1de5-4f9d-a7bf-ef5edfcb619a>
  (dataset metadata) and its resources: the
  `SBR-DPM-2025-12-31_fix_2026-02-19` package (manifest `tp:version`
  `SBR-DPM-2025-12-31`; entry points as tabled above; validation-rule
  workbooks `Validointisäännöt/SBR-DPM-2025-12-31_{OYTP,LSTP,VYTP}_validation rules.xlsx`
  with 43 / 26 / 23 rule codes such as `OYTP_2025_v16.9`; `LueMinut.txt`
  noting the foundation modules "ei päivitetty vuonna 2025"); the
  withdrawn `SBR-DPM-2025-12-31` ("VANHA VERSIO, ÄLÄ KÄYTÄ"; "PRH ei tue
  tätä taksonomiaversiota vastaanottorajapinnassa"); `SBR-DPM-2022-09-30`;
  the **SBR Conformance Suite** (`sbr-conformancesuite2026.zip`, added
  8.9.2026: per-rule valid and invalid iXBRL test reports); and
  `samplefiles.zip` (sample instances carrying `find:filingIndicator` and
  `fi_met:*` facts). Downloaded and read 2026-10-15.
- **[S24]** PRH, *Tilinpäätösilmoitus kaupparekisteriin* (automatic
  decision-making) (FI):
  <https://www.prh.fi/fi/tietoa_prhsta/automaattinen-paatoksenteko-prhssa/tilinpaatosilmoitus-kaupparekisteriin.html>.
  Automatic decision-making used for digital financial-statement
  notifications since 24.4.2019 and for ytj.fi notifications since
  21.5.2025; not every notification registers automatically. Read
  2026-10-15.
- **[S25]** PRH, *Mikä on digitaalinen eli rakenteinen tilinpäätös?* (FI):
  <https://www.prh.fi/fi/yrityksetjayhteisot/tilinpaatokset/digitaalinen-tilinpaatosraportointi/mika-digitilinpaatos.html>.
  "*XHTML-muoto ilman taustalla olevaa rakenteisuutta ei mahdollista vielä
  tietojen tehokasta käyttöä. Siksi tiedot on vakioitava taksonomian…*"
  Read 2026-10-15.
