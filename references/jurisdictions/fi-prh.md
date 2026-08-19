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

## Start here: choose a filing profile

Load this when the regulator is **PRH** (Patentti- ja rekisterihallitus /
Finnish Patent and Registration Office) and the filing is a **digital
financial statement** ("digitaalinen tilinpäätös", colloquially
*digitilinpäätös*) deposited with the **Finnish Trade Register**
(kaupparekisteri). Trigger conditions: a Finnish `osakeyhtiö` (limited
company) or `osuuskunta` (co-operative), the words *digitilinpäätös* /
*SBR-taksonomia* / *PRH-tunnisteet*, an `avoindata.fi` SBR taxonomy, the
PRH iXBRL REST interface, or an ESEF ZIP being re-filed to the Trade
Register.

Finland is **not** a report-package (`.xbri`) regime: a deposit is **XHTML
alone or a plain ZIP of XHTML** (PRH/1087 s. 2 permits either), and for a
listed issuer it is the **ESEF ZIP** re-used.
For the IFRS/ESEF path, most of the work is ESEF work. Use
`references/esef.md` and return here only for the Trade-Register overlays
(channel, metadata attachments, packaging, deadlines). For the national-GAAP
(Finnish FAS / SBR) path there is **no jurisdictional Arelle disclosure
system**. See *No Arelle FI/PRH plugin exists (honest gap) + what PRH's
interface checks* before promising a validator can gate it. This file is a
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
issued and **entering into force 24 June 2026**, published in Finlex under
*Viranomaisten määräyskokoelmat* (authority regulation collections), type
= **Määräys** (regulation/decision):

| Decision | Diaarinumero | What it sets |
|---|---|---|
| Päätös … digitaalisten tilinpäätösasiakirjojen ilmoittamisen teknisistä seikoista | **PRH/1087/01/2026** | Technical filing requirements for digital financial-statement documents [S6][S7] |
| Päätös … asiakirjojen ilmoittamisen teknisistä seikoista **(PRH-tunnisteet)** | **PRH/1088/01/2026** | PRH identifiers / taxonomy-adoption (which taxonomy + version to mark up against) [S7][S9] |

Finlex metadata for **PRH/1087/01/2026**: Antopäivä (issued) 24.6.2026;
Voimaantulo (in force) 24.6.2026; Säädösperusta (legal basis) =
*Kirjanpitolaki (1336/1993) 7 luku 23, 24 ja 25 §* + *Laki
kaupparekisterilaki (564/2023) 1 § 3 momentti* (reproduced as Finlex renders
it; the Act's own number is **1336/1997**, see below); the operative text is a
downloadable PDF available in **Finnish and Swedish** [S6]. The Finlex detail
page is a **JavaScript shell** for plain fetchers, so these fields (including
the Säädösperusta legal-basis chain) were captured via a **JS-rendering
browser**, not a static response. Only **ch. 7 s. 23** is independently
confirmed by PRH's own decision page [S4]; the other bases (ss. 24, 25 and
kaupparekisterilaki 564/2023 § 1(3)) rest on the JS-rendered metadata alone,
un-cross-checked against the PDF body.

These 24.6.2026 decisions **replaced** prior versions dated 19.12.2025
(Finlex 2025/5) and, earlier, a decision in force from 31.5.2024 (which
applied to financial periods starting in 2024) [S6][S7].

> **Unverified identifiers.** The predecessor-decision identifiers *Finlex
> 2025/5* and the *31.5.2024* in-force date come from the Finlex "replaces /
> repeals" (Kumoaa/Korvaa) **relation metadata captured in-session**; they were
> **not** re-verified against the rendered body of either predecessor decision.
> Confirm against the superseded decision PDFs before relying on the exact
> vintage identifiers.
>
> **Partial extraction.** The Finlex detail pages render only a JavaScript
> shell, but the decision PDFs are downloadable from Finlex's media
> endpoint, and the sections quoted in this file (**PRH/1087 ss. 3 and 5**
> and **PRH/1088 s. 1**) were extracted from those PDFs and are quoted
> verbatim here [S6][S9]. The **remaining sections of both decisions have
> not been read**. **For any clause not quoted here, pull the downloadable
> PDFs from the Finlex pages in *Primary sources: what each establishes*
> below**. Do not paraphrase a clause you have not read.

### The two-stage mandate: keep these distinct

The single most important distinction in this regime, and the one most
easily conflated:

1. **Digital (XHTML) filing directly to the Trade Register** has been
   **mandatory** for **sustainability-reporting (CSRD-scope) companies
   since financial year 2025**. PRH's 21 May 2025 notice states filing the
   digitilinpäätös "is mandatory for sustainability-reporting large
   companies from this year onwards and voluntary for other limited
   companies" [S3]. These companies can **no longer file financial
   statements via the tax return**; they must file directly with the
   Trade Register [S1].
2. **Structured taxonomy markup** (PRH identifiers / iXBRL tagging against
   a taxonomy) is **mandatory only for financial periods starting on or
   after 1 January 2026** [S1][S4]. For periods that began in 2025,
   sustainability-reporting companies could still submit XHTML **without
   PRH identifiers**: digital format, but not yet taxonomy-tagged
   [S4][S8].

So: **FY2025** = digital XHTML filing mandatory, untagged permitted;
**FY2026+** = full structured iXBRL markup mandatory. Do not declare an
FY2025 XHTML deposit defective for lacking PRH-identifier markup; that
requirement had not yet cut in.

For **all other limited companies**, filing digital financial statements
is **voluntary** "for the time being" [S1], but a broader mandate is now
formally in train: **government bill HE 96/2026 vp**
("Tilinpäätösraportoinnin digitalisointi", given to Parliament
21 May 2026; Finlex
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
  therefore overstates the bill [S18].
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
digitally-reporting entities with no obligation to appoint an auditor). The
bill is **pending in Parliament as of 2026-08-18**, referred to the
Commerce Committee (talousvaliokunta) 27 May 2026 with no committee report
yet, so filing stays voluntary until enacted [S18].

### Bi-temporal cheatsheet: which vintage applies to which period

As with every iXBRL regime, ask for each rule: *was this in force when
this report was prepared?* Read the period from `<xbrli:period>`, not
today's date.

| Rule / obligation | Applies to periods | Notes |
|---|---|---|
| Digital (XHTML) filing **mandatory** for sustainability-reporting companies | FY **2025** onward | Can no longer file FS via tax return; file directly to Trade Register [S1][S3]. |
| Structured **taxonomy markup** (PRH identifiers) mandatory | periods starting **on/after 1 Jan 2026** | FY2025 permitted XHTML **without** PRH identifiers [S1][S4]. |
| **SBR-DPM-2025-12-31_fix_2026-02-19** is the SBR version to mark up FAS statements against | periods starting **1 Jan 2026** at latest | PRH/1088/01/2026 s. 1 names this package by name; the unsuffixed `SBR-DPM-2025-12-31` is withdrawn on avoindata.fi as *"VANHA VERSIO, ÄLÄ KÄYTÄ"* [S2][S9]. |
| ESEF ZIP **also** filed to the Trade Register (not only to the OAM) | financial year starting **2024** onward | Listed issuers re-use their ESEF artifact [S2][S3]. |
| **Law 555/2026** narrows CSRD scope (turnover >€450M **and** >1,000 employees on average, **in both the last completed and the immediately preceding financial year**) | periods starting **on/after 1 Jul 2026** (opt-in from 1 Jan 2026) | In force 30 Jun 2026; PRH repealed & replaced both decisions [S7] (see *The 2026 scope change: law 555/2026*). |
| FY2026 **entry-trigger**: a company that *becomes* sustainability-reporting-obligated on/after 1 Jul 2026 | its FS for periods starting **on/after 1 Jul 2026** | The decision applies from that entry point [S10]. |

When uncertain, **state the vintage you are applying** before declaring a
defect. "This lacks PRH-identifier markup, which the PRH decision requires
for periods starting on/after 1 Jan 2026" is reviewable; "this is
untagged, therefore wrong" is not. For FY2025 it is permitted.

<a id="profile-fas-sbr"></a>

## Profile: Trade Register digital financial statement: Finnish FAS (national SBR taxonomy)

### Who files, to whom, under what law

Finnish limited companies and co-operatives may file their statutory
financial statements with the Trade Register in machine-readable digital
form. A digital financial statement has **two parts**, a human-readable
part (text and numbers as usual) and a machine-readable part, built from
a standardised structure (a **taxonomy**) using **Inline XBRL (iXBRL)**;
the file is **XHTML** web format. PRH states plainly that "it is not
enough to save Word documents in XHTML file format"; the document must be
genuinely structured against a taxonomy [S1].

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
  names this package by name), plus legacy `kpl-2016-12/2022-09-30`,
  `kpl-2016-12/2019-11-06`, `kpl-2016-12/2019-03-28` [S2][S4][S9]. The
  package published 31.12.2025 as `SBR-DPM-2025-12-31` is still on
  avoindata.fi, labelled *"VANHA VERSIO, ÄLÄ KÄYTÄ"*. Selecting it by
  that shorter name picks the withdrawn package [S2].

<a id="profile-ifrs-esef"></a>

## Profile: IFRS statements and listed-issuer ESEF re-use

### Which taxonomy applies

**(B) IFRS taxonomy (IFRS Foundation), for IFRS statements.** Mark up
with the **IFRS Accounting Taxonomy version approved by the IFRS
Foundation for the reporting period**; supported at PRH intake: **IFRS
Accounting Taxonomy 2025 and 2024** [S2][S4].

**(C) ESEF taxonomy (ESMA), for listed issuers' consolidated figures.**
Governed by the EU ESEF RTS (see `references/esef.md`); ESEF statements go to the
**Nasdaq Helsinki OAM** and, from the financial year starting 2024, **also
to the Trade Register**; supported at PRH intake: **ESEF 2024 and 2022** [S2].

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
not at the ZIP root. The XBRL Report Packages specification requires exactly
one such top-level directory.

Packaging rules from the PRH example [S8]:

- The free-form adoption-date and profit-decision documents (and any audit
  report) are attached **in XHTML to the MAIN folder** of the ZIP,
  **not** to the `reports/` folder. "MAIN folder" here means that single
  top-level report-package directory, **not** the ZIP root.
- **If you add PDF files to the ZIP you cannot file it via ytj.fi** [S8].
- **Filenames must not contain `å`, `ä` or `ö`** [S8].
- **File naming** follows ESMA's ESEF Reporting Manual: name = **LEI code
  (or name, max 20 chars) + financial-period end date `YYYY-MM-DD` +
  report language (`fi` or `sv`)**; both the main folder and the
  `reports/` folder/report must be named this way [S8].

### Relation to EU reporting: ESEF coexistence and the CSRD/ESRS trajectory

Delta-only; ESEF mechanics live in `references/esef.md`, *Which taxonomy applies*
and *Packaging: the ESEF ZIP re-used for the Trade Register*.

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
  channels, signatures, deadline, tax forwarding, language*); it also lets
  Member States **limit** management-body collective responsibility to
  publication in the electronic format [S13].

<a id="profile-sustainability-report"></a>

## Profile: CSRD sustainability report: assured, filed with the digital statements, not XBRL-tagged

### The 2026 scope change: law 555/2026 (supersedes older ≥500-employee framing)

Any description of Finnish CSRD scope as "large listed non-financial
companies; PIEs with ≥500 average employees; parents of such PIE groups"
is **pre-2026 and now superseded.** The Accounting Act amendment
**555/2026** (kirjanpitolain muutokset 555/2026), confirmed by the
President of the Republic and **in force 30 June 2026**, **reduced** the
population obliged to do sustainability reporting. This is Finland's
transposition of the EU CSRD "Omnibus" simplification [S7].

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
> population) was not quantified this session; any pre-Omnibus estimate is
> now stale.

## Jurisdiction-specific invariants

### Packaging and artifact shape: XHTML-in-ZIP, NOT `.xbri`

**All financial-statement documents must be filed in machine-readable web
format (XHTML). PDF is not accepted** [S1][S8]. PRH notes that a Word or PDF
document can be converted to XHTML, and its own pages mention free online
converters. Do not act on that for a real filing: an unfiled financial
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

> **Divergence from the Dutch `.xbri` model (reviewer-critical).** "At the
> moment, the PRH cannot receive material filed as an XBRI package"
> (*PRH ei voi toistaiseksi vastaanottaa XBRI-pakettina ilmoitettuja
> aineistoja*) [S1][S10]. Finland wants **XHTML, in a plain ZIP where the
> notification carries more than one document**. **Any converter output
> profile for Finland must emit XHTML, in a plain ZIP where the
> notification carries more than one document, and must NOT emit a
> `.xbri`.** Whether/when PRH will accept `.xbri` is **unknown**:
> no roadmap was found.

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

> **Honest gap.** The full enumerated list of "financial statement
> documents to be filed" was not fully fetched; only the adoption-date and
> profit-distribution-decision attachments and the not-required minutes are
> confirmed here.

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
   **digitilinpaatos@prh.fi** [S5].
   > **Honest gap.** A claim that this interface has been "live since 2019"
   > was **not verified** this session; treat the 2019 date as unverified.
2. **ytj.fi online filing service.** The digitilinpäätös (XHTML) option was
   **added to the renewed ytj.fi service on 21 May 2025** [S3]. In ytj.fi
   you first select that you are filing a digital financial statement
   (XHTML), give the requested data, and attach the required documents as
   **one file in XHTML** (ESEF filers attach the ESEF ZIP). ytj.fi requires
   a **Finnish personal identity code** plus a **Suomi.fi** e-identification
   method (bank credentials or mobile certificate); the service is
   available in **Finnish and Swedish only** [S3].
3. **Exception web form.** By way of exception, credit/insurance
   institutions not required to prepare ESEF statements, and companies that
   cannot sign in to ytj.fi (no Finnish personal identity code), may file
   via an online form (request a link from **digitilinpaatos@prh.fi**).
   This route is **only** for companies with a sustainability-reporting
   obligation [S1].

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
(auto-decision), as early as the next business day; the data then become
public in **Virre** [S1].

**Language.** Statements to be registered must be in **Finnish or Swedish**;
they **may also include an English translation** (legal basis Accounting
Act **chapter 3, section 5**, and Finnish Accounting Board statement
2084/3.12.2024) [S8]. The report-language metadata value is **`fi`** or
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

### No Arelle FI/PRH plugin exists (honest gap) + what PRH's interface checks

**Verified absence (implementation evidence).** The Arelle release
installed in this repo has **no Finland/PRH validation plugin**. Listing
`arelle/plugin/validate/` shows exactly: `CIPC, DBA, EBA, EDINET, ESEF,
FERC, NL, ROS, UK`; there is **no FI, PRH, or SBR** disclosure-system
module [S12].

Consequences for review and for any converter:

- There is **no** published Arelle disclosure system and **no rule-code
  family** (e.g. no `FR-FI-*` analogous to the Dutch `FR-NL-*`) for PRH
  SBR filings. **Do not claim Arelle "validates PRH SBR compliance"; it
  does not.** State this as an honest gap.
- For a **FAS / SBR** filing the deterministic gate is therefore
  **generic**: core **XBRL 2.1** validity + **iXBRL 1.1**
  well-formedness/validity + **taxonomy-package resolution**
  (`taxonomyPackage.xml` / `catalog.xml`) against the national SBR
  taxonomy + calculation/dimension consistency, **plus** whatever PRH's
  own intake interface enforces. It is not an Arelle profile.
- For the **IFRS / ESEF re-use path**, the standard Arelle **ESEF plugin
  is present** [S12] and is the right profile, because Finnish listed
  issuers re-use their ESEF ZIP for the Trade Register filing. Validate
  that path **exactly as an ESEF filing** (`references/esef.md`, and
  `scripts/validate_with_arelle.sh <zip> esef`). Use the calculation
  behaviour consistent with the taxonomy in play (IFRS/ESEF for that
  path); the SBR path has no PRH-published Arelle calc profile, so rely on
  core-spec calc validation only.

```bash
# FAS / SBR path — no PRH disclosure system exists; run CORE only,
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

> **Honest gaps.** (1) There is **no published FI rule-code catalogue**:
> the interface's "future deeper iXBRL content checks" match no error-code
> set found this session, so this file lists **no** `FR-FI`/`NL-KVK`-style
> codes; none are verifiable. (2) Corroborating the early stage: PRH's
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
   FY2025 permits **untagged** XHTML for
   sustainability reporters; the markup obligation is FY2026+ [S1][S4].
2. **Pin the filing obligation.** Sustainability-reporting company under
   the **post-555/2026** threshold (turnover >€450M **and** >1,000
   employees on average, in **both** the last completed and the immediately
   preceding financial year, or a voluntary ESRS committer)? For everyone
   else digital filing is voluntary and its **absence is not a defect**
   [S1][S7][S19].
3. **Choose the validation profile, honestly.** IFRS/ESEF → validate as
   ESEF (`references/esef.md`, plugin present [S12]). FAS/SBR → **core XBRL 2.1 +
   iXBRL 1.1 + SBR taxonomy-package resolution only**; **no** PRH Arelle
   disclosure system, so do not report an "FI profile" verdict; see *No
   Arelle FI/PRH plugin exists (honest gap) + what PRH's interface checks*.
4. **Check the package shape.** **XHTML, alone or in a plain ZIP**
   (PRH/1087 s. 2 permits either), ≤ **200 MB**, **not** a `.xbri`
   [S1][S6][S10]. ESEF re-use path: adoption-date + profit-decision
   XHTML (and audit report) in the **main folder**, the single top-level
   report-package directory, not the ZIP root and not `reports/`; no PDF
   if it will go via ytj.fi; no `å`, `ä` or `ö` anywhere in the filenames;
   ESMA naming `<LEI>-YYYY-MM-DD-fi|sv` [S8].
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
  government "SBR office"; the role is split: **PRH** is "responsible for the
  development of digital financial statement reporting" and runs the taxonomy
  **working group** [S17]; the **State Treasury (Valtiokonttori)** maintains the
  national **Reporting Code List** the SBR taxonomy derives from, plus the
  public-sector modules [S2]; and **XBRL Suomi / XBRL Finland** is the XBRL
  International jurisdiction consortium (**facilitated by TIEKE**) [S16].
- **Accounting standards setter:** the **Accounting Board (Kirjanpitolautakunta,
  KILA)**, under the **Ministry of Economic Affairs and Employment (TEM)**;
  issues general guidance and statements interpreting the Accounting Act (e.g.
  statement 2084; see *Filing channels, signatures, deadline, tax
  forwarding, language*) [S15][S8]. FAS = Accounting Act + KILA guidance,
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
  CSRD/ESRS trajectory*). FIN-FSA also runs the **EBA/EIOPA** prudential regimes
  (COREP/FINREP, Solvency II) as separate DPM filings, **not** part of the
  digital-FS regime [S16].

**How they interlock.** PRH owns the register *and* the FAS digital-FS pipeline;
the State Treasury supplies the code-list backbone; KILA/TEM set the accounting
*content*; FIN-FSA + Nasdaq own the listed-issuer **ESEF** path PRH merely
**re-receives** (see *Which taxonomy applies* and *Packaging: the ESEF ZIP
re-used for the Trade Register*); Verohallinto is downstream via PRH
forwarding.

## Coverage and known limitations

### When to escalate to primary sources

This file is a reviewer's working reference, not the legal source. Defer
to and cite: the **two PRH decision PDFs** at Finlex [S6][S9] before
quoting any normative clause this file does not already quote verbatim
(only PRH/1087 ss. 3 and 5 and PRH/1088 s. 1 have been read); the
**PRH digital-FS pages** [S1][S2][S4][S5][S8][S10] for
operative filing/taxonomy/interface/packaging guidance; the **Accounting
Act (Kirjanpitolaki 1336/1997)** ch. 3 s. 5 (language) and ch. 7 ss. 22–24 and 24a
(format + markup power) and **law 555/2026** [S7] at `finlex.fi`; and
**avoindata.fi** / **Valtiokonttori** for the SBR packages [S2][S5]
(IFRS/ESEF → `references/esef.md`).

If a question concerns a rule version newer than this file cites, an FI
error code (none are catalogued here; see *No Arelle FI/PRH plugin exists
(honest gap) + what PRH's interface checks*), or whether PRH has begun
accepting `.xbri`, **say so and link the primary source**. Several
load-bearing facts here rest on PRH summary pages rather than the decision
PDFs; treat those as gaps to close, not settled normative text. The cost of
a wrong citation on a regulated filing is high.

## Sources

### Primary sources: what each establishes

All fetched live this session. For any clause of the two PRH decisions not
quoted verbatim in this file, pull the PDFs from the Finlex media endpoints
given in [S6] and [S9].

- **[S1]** PRH, *Digital financial statements of limited liability
  companies to the Finnish Trade Register* (EN):
  <https://www.prh.fi/en/companiesandorganisations/financial_statements/limited_liability_companies_co-operatives_and_other_companies/digital.html>.
  Core regime: who files (sustainability reporters mandatory, others
  voluntary "for the time being"); structured XHTML required
  (Word-as-XHTML insufficient); 200 MB ZIP; **PRH cannot accept `.xbri`**;
  8-month free deadline; auto tax-forwarding; signatures optional / filings
  are copies; three channels; PDF-then-digital correction.
- **[S2]** PRH, *Tilinpäätöstaksonomiat* (FI):
  <https://www.prh.fi/fi/yrityksetjayhteisot/tilinpaatokset/digitaalinen-tilinpaatosraportointi/taksonomiat.html>.
  SBR governance (PRH company modules; Valtiokonttori municipal/wellbeing);
  modules STK/STP/VYTP/LSTP/**OYTP**; avoindata.fi; annual cadence;
  **SBR-DPM-2025-12-31_fix_2026-02-19** + legacy `kpl-2016-12/*`; IFRS
  2025/2024; ESEF 2024/2022; IFRS-vs-FAS mixed-consolidation rule.
- **[S3]** PRH news 21.5.2025, ytj.fi renewed (FI):
  <https://www.prh.fi/fi/tietoa_prhsta/uutislistaus/tiedotteet/2025/ytj-palvelu-tilinpaatos_21.5.2025.html>.
  Digitilinpäätös option launched 21 May 2025; digital filing mandatory
  for sustainability-reporting large companies "from this year" (2025),
  voluntary for others; ytj.fi needs Finnish personal ID + Suomi.fi; listed
  ESEF filers submit the ESEF ZIP.
- **[S4]** PRH, *PRH's decision on digital financial statements* (EN):
  <https://www.prh.fi/en/companiesandorganisations/financial_statements/limited_liability_companies_co-operatives_and_other_companies/digital/sustainability-reporting/prh-decision.html>.
  PRH-identifiers markup mandatory for periods starting on/after
  1 Jan 2026; SBR-DPM-2025-12-31_fix_2026-02-19; FY2025 permitted without
  PRH identifiers; IFRS/ESEF carve-outs; annual taxonomy-approval decision;
  legal basis **Accounting Act ch. 7 s. 23**.
- **[S5]** PRH, *Interface for software companies* (iXBRL REST API) (EN):
  <https://www.prh.fi/en/companiesandorganisations/financial_statements/developing-digital-financial-reporting/interface.html>.
  REST iXBRL interface: free; LLC iXBRL FS + foundation iXBRL reports;
  token auth via separate auth server; metadata in URL params + JSON
  multipart/form-data; checks metadata↔content match + "correct structure"
  (deeper checks future); error-code responses; contract + test server;
  filings are copies.
- **[S6]** Finlex, technical-filing decision **PRH/1087/01/2026**:
  <https://www.finlex.fi/fi/viranomaiset/maarayskokoelmat/patentti-ja-rekisterihallitus/2026/2>.
  Type Määräys; issued & in force 24.6.2026; legal basis Accounting Act
  ch. 7 §§ 23, 24, 25 + kaupparekisterilaki 564/2023 § 1(3) (the Finlex
  metadata field renders the Act's number as *1336/1993*; the Act's own
  number is **1336/1997**; see [S19]). The operative text **is**
  extractable: FI PDF
  <https://www.finlex.fi/api/media/authority-regulation/1072570/mainPdf/main.pdf>,
  SV twin at `…/1072569/…`. **s. 3** (closed-interface format; the
  plain-XHTML carve-out for the toimintakertomus, tilintarkastuskertomus and
  kestävyysraportin varmennuskertomus, conditional on PRH having confirmed
  no applicable PRH identifiers) and **s. 5** (corrections are whole-package
  resubmissions) are quoted in this file; **s. 6** applies the decision to
  documents filed for registration on/after 1 Jan 2026 and it replaces
  PRH/2287/01/2025 (19.12.2025). Other sections not read.
- **[S7]** PRH news 2026, CSRD scope narrowed, law 555/2026 (FI):
  <https://www.prh.fi/fi/tietoa_prhsta/uutislistaus/tiedotteet/2026/kestavyysraportointi-laki-muuttuu.html>.
  Accounting Act amendment **555/2026** in force 30 Jun 2026 narrows
  scope to **turnover >€450M AND >1,000 employees** (the statutory
  two-year condition on both limbs is in the Act itself; see [S19]);
  periods starting on/after 1.7.2026 (opt-in from 1.1.2026); PRH repealed &
  replaced both decisions (**PRH/1088** + **PRH/1087**); markup rules
  unchanged; voluntary
  ESRS commitment triggers digital-FS duties; report assured by KRT.
- **[S8]** PRH, *How to file a sustainability report …* (EN):
  <https://www.prh.fi/en/companiesandorganisations/financial_statements/limited_liability_companies_co-operatives_and_other_companies/digital/sustainability-reporting/how-to-file.html>.
  Packaging: XHTML only, no PDF; report assured, in FI/SV; ESEF ZIP
  internal structure; adoption-date + profit-decision as free-form XHTML in
  **main folder**; PDF in ZIP blocks ytj.fi; ESMA naming (LEI + `YYYY-MM-DD`
  + `fi`/`sv`); language rule (**Accounting Act ch. 3 s. 5**; Board
  statement 2084/3.12.2024); format basis ch. 7 ss. 22–24 & 24a; ESRS XBRL
  taxonomy not yet adopted.
- **[S9]** Finlex, PRH-identifiers decision **PRH/1088/01/2026**:
  <https://www.finlex.fi/fi/viranomaiset/maarayskokoelmat/patentti-ja-rekisterihallitus/2026/3>.
  Title (*…teknisistä seikoista (PRH-tunnisteet)*), issued 24.6.2026,
  replaces PRH/2288/01/2025; legal basis Accounting Act ch. 7 §§ 23, 24, 25.
  The Finlex page body is a JS shell, but the PDF is at
  <https://www.finlex.fi/api/media/authority-regulation/1072572/mainPdf/main.pdf>.
  **S. 1 paras 2–3** are quoted in this file: IFRS preparers mark up with
  the IFRS Accounting Taxonomy confirmed by the IFRS Foundation for each
  reporting period, and the markup rules "*ei koske ESEF-vaatimusten mukaan
  raportoitavia tietoja*". **S. 1 para 1** names the package
  `SBR-DPM-2025-12-31_fix_2026-02-19` on avoindata.fi for FAS preparers.
  Other sections not read; corroborated by [S4][S7].
- **[S10]** PRH, *Osakeyhtiön digitaalinen tilinpäätös* (FI):
  <https://prh.fi/fi/yrityksetjayhteisot/tilinpaatokset/osakeyhtio_ja_osuuskunta_tilinpaatos_kaupparekisteriin/osakeyhtion_sahkoinen_tilinpaatos.html>.
  FY2026 **entry-trigger** rule; 200 MB XHTML ZIP; **PRH cannot receive
  `.xbri`**; adoption-date + profit-decision required; SBR-vs-IFRS choice;
  auto-registration; Virre publicity; PDF-then-digital correction.
- **[S11]** PRH open data, *Digital financial statement information API*:
  <https://avoindata.prh.fi/en/info/swagger-ui>.
  Exposes P&L + balance-sheet detail only for iXBRL-format filings, which
  are "about 5 per cent of all financial statements".
- **[S12]** Installed Arelle `validate/` plugin directory (this repo):
  `arelle/plugin/validate/` contains **CIPC, DBA, EBA, EDINET, ESEF, FERC,
  NL, ROS, UK only**: implementation evidence that **no Finland/PRH/SBR
  disclosure-system plugin exists**; the ESEF plugin covers the IFRS/ESEF
  re-use path.
- **[S13]** EUR-Lex, **Directive (EU) 2026/470** (Omnibus I), OJ L 2026/470,
  publ. 26.2.2026, "In force": <https://eur-lex.europa.eu/eli/dir/2026/470/oj/eng>.
  Of 24 Feb 2026; amends Dirs 2006/43/EC, 2013/34/EU, (EU) 2022/2464,
  2024/1760. **Art. 2 point (9)** replaces **Art. 29d of 2013/34/EU**: until
  mark-up rules are adopted via Reg 2019/815, undertakings **shall not be
  required to mark up** their sustainability reporting (recital 24 explains
  the same point in the preamble). **Art. 2 point (11)** amends Art. 33(1):
  MS may limit collective responsibility to
  publication in the electronic format. (18 Mar 2026 in-force = 20th day after
  OJ publication.)
- **[S14]** FIN-FSA, issuer disclosure obligation / ESEF:
  <https://www.finanssivalvonta.fi/en/financial-market-participants/capital-markets/issuers-and-investors/disclosure-obligation/>.
  FIN-FSA is the Transparency-Directive NCA (Securities Markets Act) and ESEF
  supervisor; Nasdaq Helsinki is the regulated-market operator whose storage is
  the **OAM**; FIN-FSA also runs EBA/EIOPA supervisory reporting.
- **[S15]** TEM (Min. of Economic Affairs and Employment), Accounting Board:
  <https://tem.fi/en/accounting-board>. The **Accounting Board (KILA)**
  operates under TEM and interprets the Accounting Act via general
  guidance/statements.
- **[S16]** XBRL Suomi / XBRL Finland: <https://fi.xbrl.org/>. The XBRL
  International jurisdiction consortium (~20 private + public members,
  **facilitated by TIEKE**; WGs incl. FAS/tax taxonomy, IFRS-XBRL, COREP/FINREP,
  sustainability).
- **[S17]** PRH, *Developing digital financial reporting*:
  <https://www.prh.fi/en/companiesandorganisations/financial_statements/digital-financial-reporting.html>.
  PRH "is responsible for the development of digital financial statement
  reporting"; hosts the taxonomy **working group**.
- **[S18]** Finlex, government bill **HE 96/2026 vp** (*Hallituksen esitys
  eduskunnalle laeiksi kirjanpitolain, kaupparekisterilain 11 §:n ja
  tilintarkastuslain muuttamisesta*), given to Parliament 21.5.2026:
  <https://www.finlex.fi/fi/hallituksen-esitykset/2026/96>; FI PDF
  <https://www.finlex.fi/api/media/government-proposal/1070036/mainPdf/main.pdf>
  (SV twin RP 96/2026 rd at `…/1070037/…`).
  Proposed **KPL 3:8 § 2 mom** defines the *digitaalisesti raportoiva
  kirjanpitovelvollinen* (osakeyhtiö; avoin yhtiö / kommandiittiyhtiö whose
  partners, or general partners, are such companies); **§ 4 mom** disapplies
  the regime to credit institutions, insurance companies,
  employment-pension companies **and their branches**; proposed **KPL 3:9
  § 6 mom** permits other legal forms to file digitally once PRH issues a
  decision for that form; the bill implements Dirs (EU) 2017/1132,
  (EU) 2019/1151 and **(EU) 2025/25**; entry into force 1.7.2027, applied to
  financial years starting on/after 1.7.2027 (1.7.2028 where no auditor must
  be appointed). Status: referred to talousvaliokunta 27.5.2026, **no
  committee report as of 2026-08-18** (eduskunta open data, VaskiData
  record 341349).
- **[S19]** Finlex, **Laki 555/2026** amending the Accounting Act
  (published 23.6.2026, in force 30.6.2026):
  <https://www.finlex.fi/fi/laki/alkup/2026/20260555>, and the consolidated
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
  report. Note the Act's number is **1336/1997**, which 555/2026 itself
  cites, not the *1336/1993* reproduced elsewhere in this file from Finlex's
  PRH-decision metadata field.
