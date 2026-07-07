# Finland — PRH digital financial statements (digitilinpäätös)

Load this when the regulator is **PRH** (Patentti- ja rekisterihallitus /
Finnish Patent and Registration Office) and the filing is a **digital
financial statement** ("digitaalinen tilinpäätös", colloquially
*digitilinpäätös*) deposited with the **Finnish Trade Register**
(kaupparekisteri). Trigger conditions: a Finnish `osakeyhtiö` (limited
company) or `osuuskunta` (co-operative), the words *digitilinpäätös* /
*SBR-taksonomia* / *PRH-tunnisteet*, an `avoindata.fi` SBR taxonomy, the
PRH iXBRL REST interface, or an ESEF ZIP being re-filed to the Trade
Register.

Finland is **not** a report-package (`.xbri`) regime: a deposit is a plain
**ZIP of XHTML**, and for a listed issuer it is the **ESEF ZIP** re-used.
For the IFRS/ESEF path, most of the work is ESEF work — use `esef.md` and
return here only for the Trade-Register overlays (channel, metadata
attachments, packaging, deadlines). For the national-GAAP (Finnish FAS /
SBR) path there is **no jurisdictional Arelle disclosure system** — see §5
before promising a validator can gate it. This file is a working
reference, not the legal source; the operative instruments are named in §2
and listed with URLs in §12.

## 1. Regime overview — who files, to whom, under what law

Finnish limited companies and co-operatives may file their statutory
financial statements with the Trade Register in machine-readable digital
form. A digital financial statement has **two parts** — a human-readable
part (text and numbers as usual) and a machine-readable part — built from
a standardised structure (a **taxonomy**) using **Inline XBRL (iXBRL)**;
the file is **XHTML** web format. PRH states plainly that "it is not
enough to save Word documents in XHTML file format" — the document must be
genuinely structured against a taxonomy [S1].

- **Filer:** `osakeyhtiö` (limited liability company) and `osuuskunta`
  (co-operative). The interface also accepts foundations'
  (`säätiö`) iXBRL annual reports [S5].
- **Recipient / register:** the **Finnish Trade Register**
  (kaupparekisteri), operated by PRH. Once registered, the data become
  public in PRH's **Virre** information service [S1].
- **Statutory basis:** PRH's power to require the digital format and the
  markup is in the **Accounting Act (Kirjanpitolaki 1336/1993)** — ch. 7 s.
  23 for the markup decision, and ch. 7 ss. 22–24 (and 24a) for the
  technical format of documents entered in the Trade Register [S4][S8]. The
  operative technical requirements are set in two **PRH decisions** (§2).

### The two-stage mandate — keep these distinct

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
   PRH identifiers** — digital format, but not yet taxonomy-tagged
   [S4][S8].

So: **FY2025** = digital XHTML filing mandatory, untagged permitted;
**FY2026+** = full structured iXBRL markup mandatory. Do not declare an
FY2025 XHTML deposit defective for lacking PRH-identifier markup — that
requirement had not yet cut in.

For **all other limited companies**, filing digital financial statements
is **voluntary** "for the time being" [S1] — but a broader mandate is now
formally in train: **government bill HE 96/2026 vp**
("Tilinpäätösraportoinnin digitalisointi", given to Parliament
21 May 2026; Finlex
<https://www.finlex.fi/fi/hallituksen-esitykset/2026/96>; TEM project
TEM027:00/2025) proposes amending the Accounting Act, Trade Register Act
§ 11 and Auditing Act to make digital XHTML filing (with defined data
XBRL-tagged) **mandatory for all limited companies** and for open/limited
partnerships whose general partners are limited companies, phased from
financial years starting **1 Jul 2027** (1 Jul 2028 for companies without
an audit obligation). The bill is **pending in Parliament as of
2026-07-07** — filing stays voluntary until enacted.

## 2. The legal instruments — Accounting Act + two named PRH decisions

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
kaupparekisterilaki (564/2023) 1 § 3 momentti*; the operative text is a
downloadable PDF available in **Finnish and Swedish** [S6]. The Finlex detail
page is a **JavaScript shell** for plain fetchers, so these fields — including
the Säädösperusta legal-basis chain — were captured via a **JS-rendering
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

> **Honest gap.** The full **operative paragraph text** of both decision
> PDFs was **not extracted** this session — only the Finlex metadata /
> legal basis for PRH/1087 and PRH's own summary pages were fetched. The
> PRH/1088 Finlex page body rendered only its JavaScript shell; its
> existence, title, and 24.6.2026 date are confirmed via [S7], but the
> body was not read. **For verbatim normative wording, pull the
> downloadable PDFs from the Finlex pages in §12** — do not paraphrase a
> clause you have not read.

## 3. Bi-temporal cheatsheet — which vintage applies to which period

As with every iXBRL regime, ask for each rule: *was this in force when
this report was prepared?* Read the period from `<xbrli:period>`, not
today's date.

| Rule / obligation | Applies to periods | Notes |
|---|---|---|
| Digital (XHTML) filing **mandatory** for sustainability-reporting companies | FY **2025** onward | Can no longer file FS via tax return; file directly to Trade Register [S1][S3]. |
| Structured **taxonomy markup** (PRH identifiers) mandatory | periods starting **on/after 1 Jan 2026** | FY2025 permitted XHTML **without** PRH identifiers [S1][S4]. |
| **SBR-DPM-2025-12-31** is the SBR version to mark up FAS statements against | periods starting **1 Jan 2026** at latest | PRH confirms the company-reporting SBR parts each year-end; the confirmed spec applies to periods starting the following year [S2][S4]. |
| ESEF ZIP **also** filed to the Trade Register (not only to the OAM) | financial year starting **2024** onward | Listed issuers re-use their ESEF artifact [S2][S3]. |
| **Law 555/2026** narrows CSRD scope (turnover >€450M **and** >1,000 employees) | periods starting **on/after 1 Jul 2026** (opt-in from 1 Jan 2026) | In force 30 Jun 2026; PRH repealed & replaced both decisions [S7] (see §4). |
| FY2026 **entry-trigger**: a company that *becomes* sustainability-reporting-obligated on/after 1 Jul 2026 | its FS for periods starting **on/after 1 Jul 2026** | The decision applies from that entry point [S10]. |

When uncertain, **state the vintage you are applying** before declaring a
defect. "This lacks PRH-identifier markup, which the PRH decision requires
for periods starting on/after 1 Jan 2026" is reviewable; "this is
untagged, therefore wrong" is not — for FY2025 it is permitted.

## 4. The 2026 scope change — law 555/2026 (supersedes older ≥500-employee framing)

Any description of Finnish CSRD scope as "large listed non-financial
companies; PIEs with ≥500 average employees; parents of such PIE groups"
is **pre-2026 and now superseded.** The Accounting Act amendment
**555/2026** (kirjanpitolain muutokset 555/2026), confirmed by the
President of the Republic and **in force 30 June 2026**, **reduced** the
population obliged to do sustainability reporting — Finland's transposition
of the EU CSRD "Omnibus" simplification [S7].

- **New threshold:** a sustainability report must be prepared and filed
  only if the company or group has **turnover over €450 million AND more
  than 1,000 employees** [S7].
- **Voluntary commitment:** a company may voluntarily commit to preparing
  an **ESRS-compliant** sustainability report, in which case it must also
  comply with the digital-financial-statement requirements [S7].
- **Timing:** applies to periods starting **on/after 1 July 2026**; a
  company **may** apply the new rules already to periods starting on/after
  1 January 2026 [S7].

As a consequence PRH **repealed** the two earlier digital-FS decisions and
**replaced** them with PRH/1087/01/2026 and PRH/1088/01/2026 (§2). Under
the new decisions the digital-markup requirement applies to: (a) companies
already sustainability-reporting-obligated before the change and still
obligated; and (b) companies that become obligated from 1 July 2026. It
does **not** apply to companies that are no longer obligated and have not
voluntarily committed [S7].

**The markup requirements themselves are unchanged**: national SBR
taxonomy for FAS statements, IFRS taxonomy for IFRS statements, ESEF
taxonomy for listed companies' consolidated figures [S7] (see §6).

> **Honest gap.** The **post-555/2026 count** of in-scope Finnish
> sustainability-reporting companies (the mandatory digital-filing
> population) was not quantified this session; any pre-Omnibus estimate is
> now stale.

## 5. Validation — no Arelle FI/PRH plugin exists (honest gap) + what PRH's interface checks

**Verified absence (implementation evidence).** The Arelle release
installed in this repo has **no Finland/PRH validation plugin**. Listing
`arelle/plugin/validate/` shows exactly: `CIPC, DBA, EBA, EDINET, ESEF,
FERC, NL, ROS, UK` — there is **no FI, PRH, or SBR** disclosure-system
module [S12].

Consequences for review and for any converter:

- There is **no** published Arelle disclosure system and **no rule-code
  family** (e.g. no `FR-FI-*` analogous to the Dutch `FR-NL-*`) for PRH
  SBR filings. **Do not claim Arelle "validates PRH SBR compliance" — it
  does not.** State this as an honest gap.
- For a **FAS / SBR** filing the deterministic gate is therefore
  **generic**: core **XBRL 2.1** validity + **iXBRL 1.1**
  well-formedness/validity + **taxonomy-package resolution**
  (`taxonomyPackage.xml` / `catalog.xml`) against the national SBR
  taxonomy + calculation/dimension consistency — **plus** whatever PRH's
  own intake interface enforces. It is not an Arelle profile.
- For the **IFRS / ESEF re-use path**, the standard Arelle **ESEF plugin
  is present** [S12] and is the right profile, because Finnish listed
  issuers re-use their ESEF ZIP for the Trade Register filing — validate
  that path **exactly as an ESEF filing** (`esef.md`, and
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
#   (SBR taxonomy published on avoindata.fi; also hosted by Valtiokonttori — §6)

# IFRS / ESEF re-use path — the deposited artifact IS the ESEF ZIP.
scripts/validate_with_arelle.sh <LEI>.zip esef
```

**What PRH's intake interface validates (published).** On submission the
interface checks that (a) the supplied **metadata are correct and match
the iXBRL file content**, and (b) the financial statements / annual report
have the **correct structure**. PRH states that "in the future, the
interface will also check the iXBRL file content more carefully" — i.e.
**deeper content validation is not yet in place** [S5]. On success the
interface returns a success response; otherwise an **error code plus a
description of the error reason**; the interface is generally open 24/7
[S5].

> **Honest gaps.** (1) There is **no published FI rule-code catalogue** —
> the interface's "future deeper iXBRL content checks" match no error-code
> set found this session, so this file lists **no** `FR-FI`/`NL-KVK`-style
> codes; none are verifiable. (2) Corroborating the early stage: PRH's
> open-data digital-FS API exposes only P&L and balance-sheet detail, only
> for iXBRL-format filings, which are "about 5 per cent of all financial
> statements" [S11].

## 6. Taxonomies — national SBR (FAS), IFRS, ESEF

Three taxonomy families, chosen by **accounting framework** [S2][S4]:

**(A) National SBR taxonomy — for Finnish FAS statements.** "SBR" =
Standard Business Reporting; expressed in XBRL as XML schema files plus
linkbases [S2]. **PRH maintains** the company-financial-reporting modules;
the **State Treasury (Valtiokonttori)** maintains the municipalities /
wellbeing-services-counties modules [S2]. Company-reporting modules in the
current SBR version [S2]:

| Module | Covers |
|---|---|
| **OYTP** | Limited companies' and co-operatives' financial-statement reporting — **the core module** for ordinary `osakeyhtiö` / `osuuskunta` |
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
  following year** — e.g. the spec confirmed end-2025 must be used for
  periods starting 1.1.2026 [S2][S4]. A company must always use the
  **latest** spec approved for the period (it may re-use the prior year's
  template while preparing) [S2].
- **Currently supported SBR versions:** **SBR-DPM-2025-12-31** (apply at
  latest from periods starting 1.1.2026 — this is the version the
  PRH-identifiers decision directs sustainability reporters to), plus
  legacy `kpl-2016-12/2022-09-30`, `kpl-2016-12/2019-11-06`,
  `kpl-2016-12/2019-03-28` [S2][S4].

**(B) IFRS taxonomy (IFRS Foundation) — for IFRS statements.** Mark up
with the **IFRS Accounting Taxonomy version approved by the IFRS
Foundation for the reporting period**; supported at PRH intake: **IFRS
Accounting Taxonomy 2025 and 2024** [S2][S4].

**(C) ESEF taxonomy (ESMA) — for listed issuers' consolidated figures.**
Governed by the EU ESEF RTS (see `esef.md`); ESEF statements go to the
**Nasdaq Helsinki OAM** and, from the financial year starting 2024, **also
to the Trade Register**; supported at PRH intake: **ESEF 2024 and 2022** [S2].

**Mixed-basis rule.** If the **consolidated** statements are IFRS and the
**parent's own** statements are FAS, tag the consolidated with the **IFRS**
taxonomy and the parent with the **SBR** taxonomy [S2]. The PRH-identifiers
markup obligation does **not** apply to the consolidated figures of ESEF
reporters or to IFRS preparers — those follow ESEF/IFRS [S4].

## 7. Packaging and artifact shape — XHTML-in-ZIP, NOT `.xbri`

**All financial-statement documents must be filed in machine-readable web
format (XHTML). PDF is not accepted** (Word/PDF may be converted to XHTML
with free online tools) [S1][S8]. The notification maximum size is **200
MB**, and the statements must be filed **as a ZIP package** [S1][S10].

> **Divergence from the Dutch `.xbri` model — reviewer-critical.** "At the
> moment, the PRH cannot receive material filed as an XBRI package"
> (*PRH ei voi toistaiseksi vastaanottaa XBRI-pakettina ilmoitettuja
> aineistoja*) [S1][S10]. Finland wants a **plain ZIP of XHTML**. **Any
> converter output profile for Finland must emit XHTML-in-ZIP and must NOT
> emit a `.xbri`.** Whether/when PRH will accept `.xbri` is **unknown** —
> no roadmap was found.

**Required attachments (free-form XHTML in the package).** The notification
must also state the **date the statements were adopted** and the
**decision on the use of the company's profits / co-operative surplus**;
the general-meeting minutes need **not** be attached [S1][S8].

> **Honest gap.** The full enumerated list of "financial statement
> documents to be filed" was not fully fetched; only the adoption-date and
> profit-distribution-decision attachments and the not-required minutes are
> confirmed here.

**ESEF listed companies re-use their ESEF artifact** — they file the
digitilinpäätös to the Trade Register **as an ESEF package in ZIP form**
(*ESEF-pakettina ZIP-muodossa*) [S3][S8]. PRH publishes an example of the
ESEF ZIP internal structure [S8]:

```text
<LEI>.zip
├── META-INF/
│   ├── reportPackage.json
│   ├── taxonomyPackage.xml
│   └── catalog.xml
├── <taxonomy folder>/
│   ├── taxonomy.xsd
│   └── taxonomy-linkbase.xml
├── reports/
│   └── report-1.html
├── companyprofit.xhtml            # profit-use decision (free-form XHTML)
├── generalmeetingdecision.xhtml   # adoption-date decision (free-form XHTML)
└── <auditreport>.xhtml            # if applicable
```

Packaging rules from the PRH example [S8]:

- The free-form adoption-date and profit-decision documents (and any audit
  report) are attached **in XHTML to the MAIN folder** of the ZIP —
  **not** to the `reports/` folder.
- **If you add PDF files to the ZIP you cannot file it via ytj.fi** [S8].
- **File naming** follows ESMA's ESEF Reporting Manual: name = **LEI code
  (or name, max 20 chars) + financial-period end date `YYYY-MM-DD` +
  report language (`fi` or `sv`)**; both the main folder and the
  `reports/` folder/report must be named this way [S8].

## 8. Filing channels, signatures, deadline, tax forwarding, language

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
   > was **not verified** this session — treat the 2019 date as unverified.
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
   via an online form (request a link from **digitilinpaatos@prh.fi**) —
   **only** for companies with a sustainability-reporting obligation [S1].

**Signatures.** Electronic signatures are **not mandatory**. iXBRL
financial statements are legally **copies**; the signed originals stay with
the company and need not be sent separately; signatory information may be
embedded in free-form manner [S1][S5].

**Deadline + tax forwarding.** File with the Trade Register within **eight
months** of the period end; **free** within that window, a **late fee**
applies to overdue filings [S1]. If you file by the **tax-return
deadline**, you do **not** send the statements separately to the Finnish
Tax Administration — **PRH forwards them automatically**; filing after that
deadline may require a separate Tax Administration filing [S1].

**Registration.** Digital statements can be **registered automatically**
(auto-decision), as early as the next business day; the data then become
public in **Virre** [S1].

**Language.** Statements to be registered must be in **Finnish or Swedish**;
they **may also include an English translation** — legal basis Accounting
Act **chapter 3, section 5** (and Finnish Accounting Board statement
2084/3.12.2024) [S8]. The report-language metadata value is **`fi`** or
**`sv`** [S8]. The **sustainability report** must be drafted in FI/SV and
**assured** (KRT / audit-firm assurance report attached) [S7][S8]. **XBRL
markup is not yet required** in the sustainability report or its assurance
report, because the Commission has not yet adopted the **ESRS XBRL
taxonomy** (EFRAG work) [S8].

**Stale-document correction.** A company that mistakenly filed a **PDF**
must **also** file the digital statement via ytj.fi or the interface; the
digital one registers as the latest version, but the PDF is **not**
de-registered and remains in Virre [S1].

## 9. A pragmatic PRH review pass — in order

When asked to review a Finnish digital financial statement, walk this in
order; each step depends on the prior being clean.

1. **Pin basis + vintage.** FAS/SBR vs IFRS vs ESEF (§6), and the
   period start date (§3). FY2025 permits **untagged** XHTML for
   sustainability reporters; the markup obligation is FY2026+ [S1][S4].
2. **Pin the filing obligation.** Sustainability-reporting company under
   the **post-555/2026** threshold (turnover >€450M **and** >1,000
   employees, or a voluntary ESRS committer)? For everyone else digital
   filing is voluntary and its **absence is not a defect** [S1][S7].
3. **Choose the validation profile — honestly.** IFRS/ESEF → validate as
   ESEF (`esef.md`, plugin present [S12]). FAS/SBR → **core XBRL 2.1 +
   iXBRL 1.1 + SBR taxonomy-package resolution only**; **no** PRH Arelle
   disclosure system, so do not report an "FI profile" verdict (§5).
4. **Check the package shape.** **XHTML-in-ZIP**, ≤ **200 MB**, **not** a
   `.xbri` [S1][S10]. ESEF re-use path: adoption-date + profit-decision
   XHTML (and audit report) in the **main folder**, not `reports/`; no PDF
   if it will go via ytj.fi; ESMA naming `<LEI>-YYYY-MM-DD-fi|sv` [S8].
5. **Check attachments + assurance.** Adoption date and profit-use /
   surplus decision present as free-form XHTML; minutes **not** required
   [S1][S8]. Sustainability reporters: report in FI/SV, KRT/audit-firm
   assurance report attached; **no** XBRL markup expected in it yet [S7][S8].
6. **Content-level review.** No validator confirms fidelity to the source
   statements — read the rendered report as a financial professional
   (`references/conversion.md` §10).

## 10. Stakeholders and governance — the institutional map

Who runs electronic business reporting in Finland, each named once; taxonomy
and ESEF detail stays in §6 / §11 (delta-only).

- **Business register / publication organ:** the **Finnish Trade Register
  (kaupparekisteri)**, operated by **PRH**; data become public via **Virre**
  (§1) [S1].
- **Digital-business-reporting programme (SBR-Nederland analogue).** No single
  government "SBR office" — the role is split: **PRH** is "responsible for the
  development of digital financial statement reporting" and runs the taxonomy
  **working group** [S17]; the **State Treasury (Valtiokonttori)** maintains the
  national **Reporting Code List** the SBR taxonomy derives from, plus the
  public-sector modules [S2]; and **XBRL Suomi / XBRL Finland** is the XBRL
  International jurisdiction consortium (**facilitated by TIEKE**) [S16].
- **Accounting standards setter:** the **Accounting Board (Kirjanpitolautakunta,
  KILA)**, under the **Ministry of Economic Affairs and Employment (TEM)**;
  issues general guidance and statements interpreting the Accounting Act (e.g.
  statement 2084, §8) [S15][S8]. FAS = Accounting Act + KILA guidance, not a
  private standard-setter.
- **Taxonomy author / cadence:** PRH (company modules) + State Treasury (public
  sector); annual, on **avoindata.fi** — detail in §6 [S2].
- **Tax authority (structured-filing regime):** the **Finnish Tax
  Administration (Verohallinto)** — **receives FS data automatically forwarded
  by PRH** when filed by the tax-return deadline; sustainability reporters can
  no longer route FS through the tax return (§8) [S1].
- **Securities regulator (NCA):** **Finanssivalvonta (FIN-FSA)** — Transparency-
  Directive competent authority (Securities Markets Act) and ESEF supervisor;
  **Nasdaq Helsinki** is the regulated-market operator whose storage is the
  **OAM** [S14] (§11). FIN-FSA also runs the **EBA/EIOPA** prudential regimes
  (COREP/FINREP, Solvency II) as separate DPM filings, **not** part of the
  digital-FS regime [S16].

**How they interlock.** PRH owns the register *and* the FAS digital-FS pipeline;
the State Treasury supplies the code-list backbone; KILA/TEM set the accounting
*content*; FIN-FSA + Nasdaq own the listed-issuer **ESEF** path PRH merely
**re-receives** (§6–§7); Verohallinto is downstream via PRH forwarding.

## 11. Relation to EU reporting — ESEF coexistence and the CSRD/ESRS trajectory

Delta-only; ESEF mechanics live in `esef.md` and §6–§7.

- **ESEF / Transparency-Directive transposition.** The ESEF RTS (**Reg (EU)
  2019/815**) is directly applicable; the Transparency Directive is transposed
  in the **Securities Markets Act**, with **FIN-FSA** as NCA and **Nasdaq
  Helsinki** as OAM (§10) [S14]. **Coexistence:** listed issuers file the ESEF
  ZIP to the Nasdaq OAM and re-file it to the Trade Register (from FY2024) —
  the national FAS regime does **not** re-tag the ESEF markup; it re-receives
  the tagged report unchanged but the Trade-Register ZIP additionally carries
  the required free-form XHTML attachments (adoption date, profit/surplus-use
  decision, audit report — §7) [S2][S3].
- **CSRD / ESRS trajectory.** Finland transposed the CSRD; scope was
  **narrowed by law 555/2026** (§4). ESRS sustainability **mark-up is not yet
  required** — no ESRS XBRL taxonomy has been adopted (§8) [S8].
- **Directive (EU) 2026/470 (Omnibus I).** Of **24 Feb 2026**, OJ L 2026/470
  publ. **26.2.2026**, **in force 18 March 2026** (20th day after publication);
  amends Dirs 2006/43/EC, **2013/34/EU**, (EU) 2022/2464, 2024/1760 [S13].
  The directive amends **Art. 29d of the Accounting Directive (2013/34/EU)** —
  the digital-format/mark-up article the CSRD inserted — and recital 24
  (preambular, explaining the enacting article) specifies that **until
  marking-up rules are adopted via Delegated Regulation (EU) 2019/815,
  undertakings are not required to mark up their sustainability reporting**
  [S13]. This **expressly suspends the ESRS digital-tagging obligation at EU
  level**, matching PRH's national position (§8); it also lets Member States
  **limit** management-body collective responsibility to publication in the
  electronic format [S13].

## 12. Primary sources — what each establishes

All fetched live this session. For verbatim normative wording of the two
PRH decisions, pull the PDFs from the Finlex pages ([S6], [S9]).

- **[S1]** PRH — *Digital financial statements of limited liability
  companies to the Finnish Trade Register* (EN):
  <https://www.prh.fi/en/companiesandorganisations/financial_statements/limited_liability_companies_co-operatives_and_other_companies/digital.html>
  — core regime: who files (sustainability reporters mandatory, others
  voluntary "for the time being"); structured XHTML required
  (Word-as-XHTML insufficient); 200 MB ZIP; **PRH cannot accept `.xbri`**;
  8-month free deadline; auto tax-forwarding; signatures optional / filings
  are copies; three channels; PDF-then-digital correction.
- **[S2]** PRH — *Tilinpäätöstaksonomiat* (FI):
  <https://www.prh.fi/fi/yrityksetjayhteisot/tilinpaatokset/digitaalinen-tilinpaatosraportointi/taksonomiat.html>
  — SBR governance (PRH company modules; Valtiokonttori municipal/wellbeing);
  modules STK/STP/VYTP/LSTP/**OYTP**; avoindata.fi; annual cadence;
  **SBR-DPM-2025-12-31** + legacy `kpl-2016-12/*`; IFRS 2025/2024; ESEF
  2024/2022; IFRS-vs-FAS mixed-consolidation rule.
- **[S3]** PRH news 21.5.2025 — ytj.fi renewed (FI):
  <https://www.prh.fi/fi/tietoa_prhsta/uutislistaus/tiedotteet/2025/ytj-palvelu-tilinpaatos_21.5.2025.html>
  — digitilinpäätös option launched 21 May 2025; digital filing mandatory
  for sustainability-reporting large companies "from this year" (2025),
  voluntary for others; ytj.fi needs Finnish personal ID + Suomi.fi; listed
  ESEF filers submit the ESEF ZIP.
- **[S4]** PRH — *PRH's decision on digital financial statements* (EN):
  <https://www.prh.fi/en/companiesandorganisations/financial_statements/limited_liability_companies_co-operatives_and_other_companies/digital/sustainability-reporting/prh-decision.html>
  — PRH-identifiers markup mandatory for periods starting on/after
  1 Jan 2026; SBR-DPM-2025-12-31; FY2025 permitted without PRH identifiers;
  IFRS/ESEF carve-outs; annual taxonomy-approval decision; legal basis
  **Accounting Act ch. 7 s. 23**.
- **[S5]** PRH — *Interface for software companies* (iXBRL REST API) (EN):
  <https://www.prh.fi/en/companiesandorganisations/financial_statements/developing-digital-financial-reporting/interface.html>
  — REST iXBRL interface: free; LLC iXBRL FS + foundation iXBRL reports;
  token auth via separate auth server; metadata in URL params + JSON
  multipart/form-data; checks metadata↔content match + "correct structure"
  (deeper checks future); error-code responses; contract + test server;
  filings are copies.
- **[S6]** Finlex — technical-filing decision **PRH/1087/01/2026**:
  <https://www.finlex.fi/fi/viranomaiset/maarayskokoelmat/patentti-ja-rekisterihallitus/2026/2>
  — type Määräys; issued & in force 24.6.2026; legal basis Kirjanpitolaki
  1336/1993 ch. 7 §§ 23, 24, 25 + kaupparekisterilaki 564/2023 § 1(3);
  downloadable PDF (FI/SV). Metadata captured; **PDF body not extracted**.
- **[S7]** PRH news 2026 — CSRD scope narrowed, law 555/2026 (FI):
  <https://www.prh.fi/fi/tietoa_prhsta/uutislistaus/tiedotteet/2026/kestavyysraportointi-laki-muuttuu.html>
  — Accounting Act amendment **555/2026** in force 30 Jun 2026 narrows
  scope to **turnover >€450M AND >1,000 employees**; periods starting
  on/after 1.7.2026 (opt-in from 1.1.2026); PRH repealed & replaced both
  decisions (**PRH/1088** + **PRH/1087**); markup rules unchanged; voluntary
  ESRS commitment triggers digital-FS duties; report assured by KRT.
- **[S8]** PRH — *How to file a sustainability report …* (EN):
  <https://www.prh.fi/en/companiesandorganisations/financial_statements/limited_liability_companies_co-operatives_and_other_companies/digital/sustainability-reporting/how-to-file.html>
  — packaging: XHTML only, no PDF; report assured, in FI/SV; ESEF ZIP
  internal structure; adoption-date + profit-decision as free-form XHTML in
  **main folder**; PDF in ZIP blocks ytj.fi; ESMA naming (LEI + `YYYY-MM-DD`
  + `fi`/`sv`); language rule (**Accounting Act ch. 3 s. 5**; Board
  statement 2084/3.12.2024); format basis ch. 7 ss. 22–24 & 24a; ESRS XBRL
  taxonomy not yet adopted.
- **[S9]** Finlex — PRH-identifiers decision **PRH/1088/01/2026**:
  <https://www.finlex.fi/fi/viranomaiset/maarayskokoelmat/patentti-ja-rekisterihallitus/2026/3>
  — confirms title (*…teknisistä seikoista (PRH-tunnisteet)*) and date
  (24.6.2026). **Page body not captured** (JS shell only); corroborated by
  [S7].
- **[S10]** PRH — *Osakeyhtiön digitaalinen tilinpäätös* (FI):
  <https://prh.fi/fi/yrityksetjayhteisot/tilinpaatokset/osakeyhtio_ja_osuuskunta_tilinpaatos_kaupparekisteriin/osakeyhtion_sahkoinen_tilinpaatos.html>
  — FY2026 **entry-trigger** rule; 200 MB XHTML ZIP; **PRH cannot receive
  `.xbri`**; adoption-date + profit-decision required; SBR-vs-IFRS choice;
  auto-registration; Virre publicity; PDF-then-digital correction.
- **[S11]** PRH open data — *Digital financial statement information API*:
  <https://avoindata.prh.fi/en/info/swagger-ui>
  — exposes P&L + balance-sheet detail only for iXBRL-format filings, which
  are "about 5 per cent of all financial statements".
- **[S12]** Installed Arelle `validate/` plugin directory (this repo):
  `arelle/plugin/validate/` contains **CIPC, DBA, EBA, EDINET, ESEF, FERC,
  NL, ROS, UK only** — implementation evidence that **no Finland/PRH/SBR
  disclosure-system plugin exists**; the ESEF plugin covers the IFRS/ESEF
  re-use path.
- **[S13]** EUR-Lex — **Directive (EU) 2026/470** (Omnibus I), OJ L 2026/470,
  publ. 26.2.2026, "In force": <https://eur-lex.europa.eu/eli/dir/2026/470/oj/eng>
  — of 24 Feb 2026; amends Dirs 2006/43/EC, 2013/34/EU, (EU) 2022/2464,
  2024/1760; amends **Art. 29d of 2013/34/EU** (recital 24) so that until mark-up
  rules are adopted via Reg 2019/815, undertakings are **not required to mark
  up sustainability reporting**; MS may limit collective responsibility to
  publication in the electronic format. (18 Mar 2026 in-force = 20th day after
  OJ publication.)
- **[S14]** FIN-FSA — issuer disclosure obligation / ESEF:
  <https://www.finanssivalvonta.fi/en/financial-market-participants/capital-markets/issuers-and-investors/disclosure-obligation/>
  — FIN-FSA is the Transparency-Directive NCA (Securities Markets Act) and ESEF
  supervisor; Nasdaq Helsinki is the regulated-market operator whose storage is
  the **OAM**; FIN-FSA also runs EBA/EIOPA supervisory reporting.
- **[S15]** TEM (Min. of Economic Affairs and Employment) — Accounting Board:
  <https://tem.fi/en/accounting-board> — the **Accounting Board (KILA)** operates
  under TEM and interprets the Accounting Act via general guidance/statements.
- **[S16]** XBRL Suomi / XBRL Finland: <https://fi.xbrl.org/> — the XBRL
  International jurisdiction consortium (~20 private + public members,
  **facilitated by TIEKE**; WGs incl. FAS/tax taxonomy, IFRS-XBRL, COREP/FINREP,
  sustainability).
- **[S17]** PRH — *Developing digital financial reporting*:
  <https://www.prh.fi/en/companiesandorganisations/financial_statements/digital-financial-reporting.html>
  — PRH "is responsible for the development of digital financial statement
  reporting"; hosts the taxonomy **working group**.

## 13. When to escalate to primary sources

This file is a reviewer's working reference, not the legal source. Defer
to and cite: the **two PRH decision PDFs** at Finlex [S6][S9] before
quoting any normative clause (this file cites only their metadata and PRH's
summary pages); the **PRH digital-FS pages** [S1][S2][S4][S5][S8][S10] for
operative filing/taxonomy/interface/packaging guidance; the **Accounting
Act (Kirjanpitolaki 1336/1993)** ch. 3 s. 5 (language) and ch. 7 ss. 22–25
(format + markup power) and **law 555/2026** [S7] at `finlex.fi`; and
**avoindata.fi** / **Valtiokonttori** for the SBR packages [S2][S5]
(IFRS/ESEF → `esef.md`).

If a question concerns a rule version newer than this file cites, an FI
error code (none are catalogued here — see §5), or whether PRH has begun
accepting `.xbri`, **say so and link the primary source**. Several
load-bearing facts here rest on PRH summary pages rather than the decision
PDFs — treat those as gaps to close, not settled normative text. The cost of
a wrong citation on a regulated filing is high.
