---
reference_id: be-nbb
jurisdiction: BE
restructured_on: 2026-08-15
profiles:
  - id: nbb-cbso
    section: profile-nbb-cbso
  - id: fsma-esef
    section: profile-fsma-esef
  - id: biztax
    section: profile-biztax
---

# Belgium: NBB Central Balance Sheet Office, FSMA/ESEF, and Biztax

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*

Load this when the filer is a **Belgian** entity and the regulator is the
**National Bank of Belgium (NBB)** Central Balance Sheet Office (statutory annual
accounts, `be-gaap` / `nbb-cbso`), the **FSMA** (listed-issuer AFR under ESEF), or
**FPS Finance** (corporate income-tax return via **Biztax**, `be-tax`). For
generic ESEF taxonomy / tagging / RTS mechanics, prefer `references/esef.md`; for the
EBA/EIOPA supervisory DPM the NBB also runs as prudential supervisor, see
`references/dpm.md`. This file carries **only the Belgian jurisdiction
layer**. Its job is to stop a conversion product making the one mistake
that gets a Belgian filing rejected: emitting the wrong *format* for the
wrong regime.

## Start here: choose a filing profile

| Situation | Profile | Section |
|---|---|---|
| A Belgian company, association or foundation must file its statutory annual accounts | NBB Central Balance Sheet Office: `be-gaap` / `nbb-cbso`, classic XBRL 2.1 | [Profile: NBB Central Balance Sheet Office](#profile-nbb-cbso) |
| A listed issuer must publish an annual financial report as regulated information | FSMA / ESEF: Inline XBRL via eCorporate into STORI | [Profile: FSMA / ESEF](#profile-fsma-esef) |
| A company, non-resident or legal entity must file its income-tax return | Biztax: `be-tax`, classic XBRL 2.1, FPS Finance | [Profile: Biztax](#profile-biztax) |

Belgium runs one of Europe's oldest mandatory XBRL regimes; the NBB Central
Balance Sheet Office has accepted internet XBRL filings since **1 April 2007**.
Do not conflate the three legally and technically distinct pipelines a Belgian
entity may touch in the same financial year:

1. **NBB Central Balance Sheet Office (CBSO)**: NL *Balanscentrale*, FR
   *Centrale des bilans*. Mandatory structured filing of **statutory annual
   accounts** for ~**500,000** legal entities/year, in the `be-gaap`
   **`nbb-cbso`** taxonomy. The centrepiece a Belgian-market conversion product
   serves.
2. **FSMA / ESEF**: **listed-issuer** annual financial reports (AFRs), filed
   via **eCorporate** into the **STORI** storage mechanism.
3. **Biztax**: corporate / legal-entity / non-resident **income-tax returns**
   in FPS Finance's **`be-tax`** taxonomy.

Three institutions (NBB, FSMA, FPS Finance), three legal bases, three
taxonomies, and (decisively) **two different XBRL formats**. Establish which
one you are producing before writing a single tag.

### Legacy section index

1. Regime identification: three separate Belgian XBRL regimes
2. The critical split: iXBRL vs classic XBRL 2.1 (read before generating)
3. Bi-temporal warning: pin the version to the reporting date
4. NBB Central Balance Sheet Office: mandate and the Filing 2.0 application
5. NBB `be-gaap` taxonomy: versions, architecture, model / entry-point matrix
6. NBB accepted formats, controls, decimals, language, fees
7. FSMA / ESEF: the listed-issuer layer (eCorporate, STORI)
8. Biztax: the corporate income-tax return (`be-tax`, FPS Finance)
9. CSRD / ESRS in Belgium and the Omnibus I effect on digital tagging
10. Stakeholders and governance
11. Relation to EU reporting
12. Validation how-to: Arelle coverage and the honest gaps
13. Review checklist: a Belgian pass in order
14. Primary sources

## Vintage and applicability

The rules in force **when the accounts were prepared** are not necessarily
today's. Belgian taxonomies release **annually**, and the NBB Filing application
supports several versions in parallel, selecting by the **closing date of the
accounts**, not the upload date. Before you validate or review, pin:

- **The reference / closing date** selects the `be-gaap` framework version.
  `nbb-cbso-26.0.15` is the current final version (in use since **2 January
  2026**); the prior framework is `25.0`, final `nbb-cbso-25.0.11` (6 January
  2025). Do not validate a FY2024-closing set against the 26.0 framework.
- **The assessment year** for Biztax: `be-tax` is versioned
  `be-tax-YYYY-04-30` (`be-tax-2026-04-30` for AY2026), the return-form
  model fixed each year by Royal Decree.
- **The financial year for ESEF / ESRS** (see *CSRD / ESRS in Belgium and the
  Omnibus I effect on digital tagging*): the CSRD phase-in moved twice
  (stop-the-clock, then Omnibus I); applying a later wave's obligation to an
  earlier year is itself the defect.

State the version you assert a defect under. On a version-mismatch rejection,
re-read the live NBB **Taxonomy** page for the exact patch level in force on
the closing date; a search-index snapshot can lag the live page by a patch
(this session saw a `26.0.10` snapshot against a live `26.0.15`).

<a id="profile-nbb-cbso"></a>

## Profile: NBB Central Balance Sheet Office, statutory annual accounts

### Mandate and the Filing 2.0 application

The CBSO is an NBB department that collects, processes, publishes, and archives
the annual accounts of most Belgian legal entities (companies, associations,
foundations, health-insurance funds), free as PDF, XBRL, or CSV. Filing is
mandatory under the **Code of Companies and Associations (CCA / WVV / CSA)** and
its implementing **Royal Decree of 29 April 2019**. Paper filing was abolished
from **1 January 2020**. Electronic only.

The current portal is **Filing** (Filing 2.0). Since **4 April 2022** filing and
preparation are possible only in the rewritten integrated application; the old
**Sofista** application was deactivated the same day (**4 April 2022**), and the
legacy standalone **Filing** application on **1 May 2022**. Filing lets a filer
import XBRL/ZIP files, declare a single PDF, or draw up a new form from scratch
(the former Sofista functionality), auto-recovering company identification from
the **Crossroads Bank for Enterprises (KBO / BCE)**.

Legacy gotcha: **old XBRL files from Sofista or legacy commercial software are
not compatible with the new Filing structure**. Filing ships a "Convert an old
file" tool; convert a pre-2022 CBSO instance rather than assuming it loads.
Numeric-entry convention: **no thousands separator**; negative amounts preceded by
a **minus sign** rather than parentheses where possible.

### The `be-gaap` taxonomy: versions, architecture, model / entry-point matrix

**Name / owner:** "Belgian financial reporting taxonomy", NBB–CBSO,
`xbrl.be@nbb.be`. **Specification:** XBRL 2.1 (2003-12-31). The **DTS is
self-contained** (no external XBRL taxonomies), which matters for offline
validation (see *Validation*). Earlier generations declared FRTA 1.0
(2005-11-07) compliance.

**Version history to pin against:**

| Framework | Final version | Released / in use |
|---|---|---|
| 26.0 | `nbb-cbso-26.0.15` | since 2 January 2026 (`.15` is an in-year patch) |
| 25.0 | `nbb-cbso-25.0.11` | 6 January 2025 (technical guide 25.0.5) |
| 23.0 | — | 3 April 2023 |
| pre-2022 | `pfs` architecture (`pfs-full` / `pfs-abbr` / `pfs-mic` / `pfs-npo-*`) | legacy |

**Instance mechanics** (CBSO technical guide): `.xbrl` extension, UTF-8; **one
annual account per "annual accounts data" instance**; optional "software vendor"
and "contact data" instances may be ZIP-bundled alongside the mandatory
annual-accounts instance. `schemaRef` points to the per-model entry point.
Namespaces include `xbrli`, `link`, `xbrldi`, `iso4217`, `xlink`, plus the NBB
dictionary namespaces `met` (metrics), `dim` (dimensions), `dom` (domains),
`enum` (enumerations).

**Model / entry-point matrix** (26.0 recommended prefixes). Each `-f` entry point
splits into `-a` (annual accounts) and `-o` (other documents) variants (e.g.
`m02-a` / `m02-o`):

| Category | Full | Abbreviated | Micro |
|---|---|---|---|
| Company **with** capital | `m02-f` | `m01-f` | `m07-f` |
| Company **without** capital | `m82-f` | `m81-f` | `m87-f` |
| Associations & foundations | `m05-f` | `m04-f` | `m08-f` |

Plus **Contacts** `m100-r`, **Application producer** `m101-r`, and (**new in
26.0**) a **Country-by-Country report (CbCR)** entry point `m90-f`.

In WVV/CSA terms the standard models are **VOL** (full), **VKT** (abbreviated),
**MIC** (micro), suffixed **`-kap`** (with capital) or **`-inb`** (without).
Specific cover-sheet codes exist for credit institutions / investment firms
(`VOL-inst` / `VKT-inst`), insurers (`VOL-ver` / `VKT-ver`), copyright collecting
societies (`VOL-AUT`), and other exceptions (`VOL-A` / `VKT-A`).

Date limits that catch out early-year filings: **micro models cannot be used for
financial years beginning before 1 January 2016**, and without-capital and
association micro models cannot be used for years closed before 1 May 2019.

### Accepted formats, controls, decimals, language, fees

**Format choice.** Accounts may be filed as **XBRL** or **PDF**; XBRL is
preferred, cheaper, and ~**99%** of filings. XBRL is permitted **only** when the
accounts (a) use a **standard model**, (b) are in **euro** (or an FPS
Economy-authorised foreign currency disclosed in the notes), and (c) are **not**
a foreign company's. All other cases must be PDF.

**PDF is mandatory for the *specific* models:** credit institutions, investment
firms and UCI management companies; insurance companies; health-insurance funds
and their national federations (Act of 6 August 1990); copyright collecting
societies. Do not attempt a `be-gaap` XBRL instance for these. **Max file size
(XBRL or PDF): 50 MB.** For an XBRL filing that ceiling covers the instance
(or the ZIP of instance plus software-vendor and contact files) *including*
every PDF embedded in it.

**Encapsulated PDFs.** Each PDF embedded in a CBSO instance must additionally be
**≤ 10 MB** and meet the acceptance criteria of NBB Technical Guide 26.0.15 §5.1:
DIN-A4 pages (21 x 29.7 cm) only, and no OCG/layers, no comments or tags, no
attached files, no audio/video, no security or password protection, no JavaScript,
and no "fake" PDFs (a non-PDF renamed to `.pdf`). Colours and both handwritten and
electronic signatures are accepted in 26.0.15, having been refused in older
guides. These criteria are not all machine-checkable: the CBSO may refuse a filing
after manual visual inspection once it is uploaded.

**Decimals.** Reporting/publication unit is the **euro without decimals** for
full/abridged/micro. For XBRL a filer *may* optionally supply **two-decimal**
euro amounts to ease ledger carry-over; after acceptance and arithmetic
validation to euro-cent precision (10⁻²), the NBB rounds to the unit for PDF
publication.

**Validation.** Each instance must be valid XML, valid XBRL against the
applicable CBSO taxonomy, and satisfy the legal **arithmetic and logical
controls** published in the Belgian Bulletin, shipped as **Formula linkbase
assertions** (separate lists for companies vs associations/foundations) plus
technical constraints. NBB Technical Guide 26.0.15 §4.3.3.2 divides those linkbases
into `<model_id>-<model_part>-legal-formula` (the legal arithmetic and logic
controls), `-nbb-formula` (complementary arithmetic and logic controls) and
`-other-formula`, with the control list in its Appendix 2. Those shipped Formula
linkbases *are* the legal control set (see *Validation*).

**Language.** Filings are in **Dutch, French, or German** per the company's
region; NBB forms and labels come in four languages (`en`/`fr`/`nl`/`de`).

**Fees (2026, companies)**, by model, format, and corrected-or-not; indexed
annually on 1 January to the CPI (RD 29 April 2019, arts **3:70** / **3:118**):

| | Full | Abridged | Micro |
|---|---|---|---|
| XBRL | € 379.50 | € 89.40 | € 67.00 |
| PDF | € 449.70 | € 159.50 | € 137.30 |
| Corrected filing | € 86.00 | € 86.00 | € 54.70 |

Public **CbCR**: € 86.00. **Late-filing surcharge** (*tarieftoeslag*, CCA/WVV
art **3:13**), 2026, from the 1st day of the 9th month after year-end: € 151
(small company on abridged/micro) or € 504 (others); rising to € 227 / € 755 in
months 10–12 and € 453 / € 1,510 from month 13. Collected by the NBB, transferred
to FPS Finance.

### Sustainability information in the CBSO filing

**Scope: CSRD-regime companies only.** Everything in this section applies solely
to companies that must include sustainability information in the annual report
(*jaarverslag*). It does **not** reach the ordinary CBSO filer population, whose
annual accounts remain `be-gaap` XBRL 2.1 (see the regime table). The Belgian
basis is **art. 3:6/8 WVV**, inserted by art. 20 of the Law of 2 December 2024,
which by its own operative wording binds only "een vennootschap die
duurzaamheidsinformatie in het jaarverslag opneemt" (consolidated counterpart:
art. 3:32/6).

Per the NBB Balanscentrale notice *Rapportering van duurzaamheidsinformatie*
(22 October 2024), sustainability information is **not** a separate report: it is
an integral part of the (consolidated) management report. For companies in that
scope the NBB states: "Het volledige jaarverslag moet opgemaakt worden volgens de
ESEF-voorschriften (iXBRL, XHTML), zowel voor genoteerde als niet-genoteerde
vennootschappen." The listed/unlisted contrast is the load-bearing part. Unlike
the FSMA/Transparency-Directive ESEF regime, this one reaches **unlisted**
companies, but only those within CSRD scope. From **6 January 2025** the CBSO
**Filing** application accepts that management report, sustainability information
included, as a **ZIP** holding an XHTML file plus the files carrying the
XBRL/iXBRL taxonomy information; the NBB describes it as comparable to the ZIP
filed with the FSMA via STORI. NBB Technical Guide 26.0.15 §6 sets the container
mechanics for such encapsulated XHTML/iXBRL files: one XHTML document only, a
`.html` or `.xhtml` extension, no executable code, and no HTML `<base>` element.

**Caveat for current builds: the 2024 notice is stale.** It predates both
postponements, and the NBB has since restated the position (news item *Lijst van
ondernemingen onderhevig aan CSRD*, 12 May 2026).

- **Mark-up is off.** Article 29d of Directive 2013/34/EU, **as replaced by
  art. 2(9) of Directive (EU) 2026/470**, an operative provision rather than
  merely recital 24, now reads: "Until such rules on the marking-up are adopted
  by way of that Delegated Regulation, undertakings shall not be required to mark
  up their sustainability reporting." Belgium has **not yet transposed**
  2026/470, with a deadline of 19 March 2027, so art. 3:6/8 second lid WVV
  nominally still requires mark-up. It is inoperable regardless, because
  Delegated Regulation (EU) 2019/815 contains no ESRS mark-up rules to mark up
  against (see *CSRD / ESRS in Belgium and the Omnibus I effect on digital
  tagging*).
- **The format obligation survives on paper but is not yet an operational NBB
  requirement.** Art. 29d(1) and art. 3:6/8 first lid keep the XHTML/ESEF format
  requirement. The NBB's May 2026 statement nonetheless places the channel in the
  future: "Vanaf de publicatie van de aangepaste ESRS-standaarden is het
  verplicht om de duurzaamheidsinformatie in digitale vorm aan te leveren volgens
  het ESEF-formaat (...). In de Filing-toepassing dient het jaarverslag met
  duurzaamheidsinformatie vanaf dan via een zip-bestand (XHTML-bestand + de
  iXBRL-taxonomie) te worden opgeladen."
- **Population, after Omnibus.** NBB Group 1, large PIEs above 500 employees on
  the pre-Omnibus criteria, reported FY2024 in 2025. The next Belgian wave is
  **FY2027, published 2028**, on the revised scope.

**Net:** do not build ESRS tagging, and do not treat the ZIP/ESEF channel as a
live obligation for any CBSO filer today. Re-verify once the revised ESRS and the
ESEF-RTS mark-up rules are published.

<a id="profile-fsma-esef"></a>

## Profile: FSMA / ESEF, the listed-issuer layer (eCorporate, STORI)

The **FSMA** (Financial Services and Markets Authority; NL *Autoriteit voor
Financiële Diensten en Markten*) is Belgium's securities regulator / NCA.
**STORI** ("Storage of Regulated Information") is the Belgian **officially
appointed mechanism (OAM)** for regulated information under the Transparency
Directive; the FSMA was designated by **Royal Decree of 23 February 2010**,
effective **1 January 2011**. STORI holds regulated information for issuers on a
regulated market with Belgium as home Member State (and Euronext-operated
Alternext issuers), filed since 1 January 2011.

### Filing channel and mechanics

**Filing channel and mechanics** (per FSMA FAQ **FSMA_2021_19**):

- Issuers upload to **eCorporate**; regulated info there is automatically
  recorded in **STORI**. The ESEF AFR is filed with the FSMA via eCorporate,
  **not** with the NBB CBSO.
- ESEF is mandatory in Belgium for **financial years beginning on or after
  1 January 2021**; Belgium exercised the EU one-year optional postponement
  (RD of 6 September 2021, BS 17 September 2021, inserting art. 12/1 into the
  RD of 14 November 2007; the FSMA had announced forbearance for exercise
  2020).
- Reports with **consolidated IFRS statements** upload as a **ZIP reporting
  package** of exactly one XHTML report plus taxonomy info; reports **without**
  consolidated statements as a plain XHTML file; each language version in a
  **separate ZIP**. The FSMA FAQ *recommends* the lower-case **`.xbri`**
  extension for the inline-XBRL package rather than `.zip` (FSMA_2021_19
  §5.4: "It is recommended", not a hard requirement).
- The **ESEF version is official** and must be the "main document"; an optional
  PDF may be uploaded only as an **attachment**.
- **Deadline:** public by the earlier of **30 days before the AGM** or **4 months
  after year-end**.
- eCorporate's technical checks return a validation file that **does not guarantee
  full ESEF-Regulation compliance**; a temporary ESEF test environment previews
  validation without publishing to STORI.

For the ESEF taxonomy, tagging, anchoring, and RTS rules, defer to
`references/esef.md`; this is only the Belgian filing-mechanism overlay.

### CSRD / ESRS in Belgium and the Omnibus I effect on digital tagging

Belgium transposed **Directive (EU) 2022/2464 (CSRD)** by the **Law of 2 December
2024** (Belgian Official Gazette 20 December 2024, in force 30 December 2024),
amending the WVV/CSA, the Law of 2 August 2002 on financial-sector supervision,
the Law of 7 December 2016 on the audit profession, and the Code of Economic Law.
For listed issuers, the **RD of 16 March 2025** amended the RD of 14 November
2007 to require listed companies (except micro-issuers) to include ESRS-compliant
sustainability information in the management report, under FSMA supervision.

**Phase-in and the two postponements.** The original phase-in (WVV art 116) was
FY2024 for large NFRD/PIE entities > 500 employees, FY2025 for other large
companies, FY2026 for listed SMEs except micro. The **Law of 12 December 2025**
(transposing Directive (EU) 2025/794, "stop-the-clock") pushed **wave 2 from
FY2025 to FY2027** and **wave 3 from FY2026 to FY2028**. The **Omnibus I
"Content" Directive, Directive (EU) 2026/470 of 24 February 2026** (OJ
26 February 2026, in force 18 March 2026; CSRD-amending transposition deadline
19 March 2027) further reshaped the ESRS.

**Why this matters to a conversion product:** recital 24 of Directive (EU)
2026/470 states that **until the sustainability-reporting mark-up rules are
adopted** in Delegated Regulation (EU) 2019/815 (the ESEF RTS), undertakings are
**not** required to mark up sustainability reporting; the ESRS digital-tagging
delegated act is expected only in H2 2026, with revised (simplified) ESRS around
September 2026. **Net: ESRS mark-up in ESEF is effectively suspended pending the
updated ESEF RTS.** Belgian listed issuers still file the ESEF
financial-statements iXBRL but are **not yet obliged to tag the sustainability
statement**. Do not build that obligation into a Belgian ESEF pipeline as if
it were live; verify the current ESEF RTS first.

<a id="profile-biztax"></a>

## Profile: Biztax, the corporate income-tax return (`be-tax`, FPS Finance)

**Biztax** is the **FPS Finance** (FOD Financiën / SPF Finances) XBRL-based
e-service for filing legal-entity income-tax returns. The taxonomy is **`be-tax`**,
authored by FPS Finance.

- **Format:** classic **XBRL 2.1** (incl. errata) + **Dimensions 1.0** +
  **Formula 1.0**. **Not** Inline XBRL.
- **Instance:** the validatable unit is the instance document carrying the
  **`.xbrl`** extension. It must be **UTF-8**, must contain **exactly one return**,
  and must not exceed **15 MB** including its embedded PDF attachments, each of
  which may not exceed **5 MB**; attachments must be genuine PDFs, not files
  renamed to `.pdf`. File names may use only unaccented alphabetic characters,
  digits, spaces and the symbols `.`, `-` and `_`.
- **Package:** the **`.biztax`** file is only the transport envelope
  (*omslagbestand*) for online upload, holding **at most 25** such returns. The
  manual states no size cap for the envelope itself, so do not assert one. Both
  the instance and the `.biztax` file must be valid XML, and each return must
  satisfy the `be-tax` taxonomy including the content and technical validations in
  the Formula linkbases. On submission the return is stored as PDF; the XBRL file
  is also retained and consultable.
- **Two rejection gates, different scope.** **Technical failure is
  package-atomic:** if any one return in the uploaded `.biztax` envelope fails the
  technical checks (is the file technically correct, and may a return be filed for
  each enterprise in it), the whole upload is invalidated and every return in it is
  rejected. **Content failure is per-return:** a return with content
  (*inhoudelijke*) errors is stored but not submitted, while the other returns in
  the same package are automatically signed and filed; the failed ones are opened
  via *My returns* → *List of errors* and corrected. Validate each instance before
  bundling.
- **Cadence:** annual, tied to the **assessment year**. Architecture guides and
  user manuals are versioned `be-tax-YYYY-04-30`; **`be-tax-2026-04-30`** is
  live for AY2026; the return-form model is fixed each year by Royal Decree,
  e.g. the **RD of 13 April 2025** (AY2025), under **Income Tax Code 1992
  arts 307 §1 and 307bis** (mandatory electronic filing).
- **Entry points (three return types):** corporate income tax (`be-tax-inc-rcorp`;
  ISOC/VenB), non-resident (`be-tax-inc-nrcorp`; BNI/INR), legal-entities
  (`be-tax-inc-rle`; RPB/IPM). **Treat these identifiers as secondary** (gap
  below).
- **Reuse:** historically reused building blocks from the NBB annual-accounts and
  FPS Economy taxonomies; validation rules ship as a Formula linkbase (one XML per
  rule, `valueAssertion` pass/fail, no warnings).

### Honest gap

**Honest gap.** The entry-point identifiers come from a **republished FPS
Finance presentation, not the live schemas**. Confirm against the official
`be-tax` entry-point schemas before treating them as normative. The version,
format and size facts rest on the `be-tax-2026-04-30` Gebruikershandleiding
and the `be-tax-2025-04-30` Architecture Guide, the *Characteristics* /
*Functionaliteiten* page, and the RD of 13 April 2025; the FPS Finance Biztax
technical-docs index has been observed behind an anti-bot CAPTCHA, but the
`be-tax-2026-04-30` documents fetch directly from the FPS Finance downloads
path.

## Jurisdiction-specific invariants

### The critical split: iXBRL vs classic XBRL 2.1

This is the fact most likely to sink a Belgian conversion. **Only the FSMA/ESEF
layer uses Inline XBRL** (iXBRL facts embedded in XHTML). The other two regimes
use **classic XBRL 2.1 instance documents** (a separate `.xbrl` file, *not*
iXBRL, *not* XHTML):

- The NBB taxonomy page states plainly: *"XBRL Specification use: XBRL 2.1
  Specification - version (2003-12-31)."* CBSO instances carry the `.xbrl`
  extension.
- The `be-tax` architecture guide requires conformance to *"the XBRL 2.1
  specification, including errata, the Dimensions 1.0 and the Formula 1.0
  specification."* Biztax returns are `.xbrl` instances uploaded inside a
  `.biztax` envelope, not iXBRL.

Consequence for a product whose default output is iXBRL/XHTML (built for ESEF or
KvK): **iXBRL emitted for the NBB or Biztax will be rejected.** Those regimes want
plain XBRL 2.1 instances whose controls are checked by the taxonomy's shipped
Formula linkbases. Route the iXBRL/XHTML generator to the FSMA/ESEF path only;
route NBB and Biztax to a classic XBRL 2.1 instance writer.

| Regime | Institution | Taxonomy | Format | Container |
|---|---|---|---|---|
| Annual accounts | NBB CBSO | `be-gaap` (`nbb-cbso`) | **XBRL 2.1** | `.xbrl` instance (optionally in a ZIP) |
| Listed AFR | FSMA | ESEF core + issuer extension | **Inline XBRL 1.1** | `.xbri` report package (XHTML) |
| Income-tax return | FPS Finance | `be-tax` | **XBRL 2.1** + Dimensions 1.0 + Formula 1.0 | `.xbrl` instance, uploaded inside a `.biztax` envelope (max 25) |

### Relation to EU reporting

Belgium's three regimes sit on EU foundations but resolve to national formats and
channels:

- **Accounting Directive 2013/34/EU** underpins the `be-gaap` statutory models
  via the RD of 29 April 2019, but the `be-gaap` XBRL 2.1 filing is a purely
  national format; there is no EU-mandated iXBRL for unlisted entities' annual
  accounts.
- **Transparency Directive 2004/109/EC + ESEF RTS (Delegated Regulation (EU)
  2019/815)** land at **FSMA / eCorporate / STORI**, the only Belgian iXBRL
  regime. Generic ESEF mechanics → `references/esef.md`; Belgian overlay → the
  *FSMA / ESEF* profile.
- **CSRD (Directive (EU) 2022/2464)** flows through the WVV/CSA and FSMA
  supervision (Law of 2 December 2024, stop-the-clock Law of 12 December 2025,
  Omnibus I Directive (EU) 2026/470), with ESRS **mark-up suspended** pending the
  updated ESEF RTS (see *CSRD / ESRS in Belgium and the Omnibus I effect on
  digital tagging*).
- **The regimes never substitute for each other.** A listed issuer files ESEF with
  the **FSMA** (not the NBB); an unlisted entity files `be-gaap` XBRL with the
  **NBB**; **both** file `be-tax` with **FPS Finance**. One group may produce all
  three in a year, in two XBRL formats; one filing never discharges another.

## Validation

**There is no Belgium / BE Arelle plugin.** Verified against the installed
`arelle-release`: the shipped `validate` plugins are exactly **CIPC, DBA, EBA,
EDINET, ESEF, FERC, NL, ROS, UK**: no `be-gaap` (NBB CBSO) and no `be-tax`
(Biztax) disclosure-system plugin, and **no `FR-BE-*` equivalent to the Dutch
`FR-NL-*` family**. Do not invent Belgium-specific Arelle error codes.

Per regime:

1. **FSMA / ESEF (iXBRL): covered by the generic ESEF plugin.** The AFR package
   validates like any other member state's; the Belgian layer (eCorporate, STORI,
   `.xbri`, deadlines) is **filing-mechanism policy, not encoded in Arelle**. Use
   `--plugins 'inlineXbrlDocumentSet|validate/ESEF'` (see `references/esef.md`).
2. **NBB `be-gaap` and Biztax `be-tax`: no profile-aware plugin.** The
   statutory-model selection rules, fee/deadline logic, and specific-model
   PDF-only rule are **not encoded in Arelle**. Enforce them in your pipeline.
3. **But Arelle's *generic* processors do the heavy lifting.** Both are plain
   **XBRL 2.1 with self-contained DTSs** shipping their legal controls **as XBRL
   Formula 1.0 linkbases** (plus Dimensions 1.0): load the matching taxonomy
   package and `--validate` executes the taxonomy's own Formula assertions (the
   arithmetic/logical controls). No Belgium plugin required for that layer.

Practical harness shape:

```bash
# NBB CBSO annual-accounts instance (classic XBRL 2.1 — NOT iXBRL)
arelleCmdLine \
  --packages nbb-cbso-26.0.15.zip \
  -f annual-accounts.xbrl --validate

# Biztax return (classic XBRL 2.1 + Dimensions + Formula — NOT iXBRL).
# Validate the instance, not the envelope: unpack the .biztax file first and
# run each contained .xbrl instance through Arelle before bundling.
arelleCmdLine \
  --packages be-tax-2026-04-30.zip \
  -f return.xbrl --validate

# FSMA ESEF AFR (Inline XBRL) — the ONLY Belgian iXBRL path
arelleCmdLine \
  --plugins 'inlineXbrlDocumentSet|validate/ESEF' \
  -f afr-report-package.xbri --validate
```

Reserve `inlineXbrlDocumentSet` + `validate/ESEF` for the FSMA path only. The
`be-gaap` DTS is self-contained, so `--packages` with the matching `nbb-cbso`
version resolves everything locally: no remote fetch, which removes a class of
intermittent validation stalls.

## Review workflow

Walk this in order; each step depends on the prior being clean.

1. **Identify the regime.** NBB annual accounts, FSMA/ESEF AFR, or Biztax
   return (see *Start here: choose a filing profile*). State it back before
   opening the file.
2. **Confirm format matches regime.** iXBRL/XHTML → FSMA only; `.xbrl` XBRL
   2.1 → NBB; `.xbrl` XBRL 2.1 inside a `.biztax` envelope → FPS Finance. An
   iXBRL file bound for the NBB or Biztax is wrong on its face (see *The
   critical split: iXBRL vs classic XBRL 2.1*).
3. **Pin the version to the reference date.** `nbb-cbso` framework by closing
   date; `be-tax-YYYY-04-30` by assessment year; ESEF/ESRS by financial year
   against the current phase-in (see *Vintage and applicability* and *CSRD /
   ESRS in Belgium and the Omnibus I effect on digital tagging*).
4. **NBB: format eligibility.** XBRL only if standard model + euro (or
   authorised foreign currency) + not a foreign company; specific-model
   entities (credit institutions, insurers, health funds, collecting societies)
   file **PDF**; 50 MB cap on the instance or ZIP including embedded PDFs, and
   ≤ 10 MB per encapsulated PDF, DIN-A4 and free of layers, comments,
   attachments, media, passwords and JavaScript (see *Accepted formats,
   controls, decimals, language, fees*).
5. **NBB: model / entry point.** With/without capital, size class,
   associations vs companies; `schemaRef` must point to the matching `m0x-f`
   entry point; respect micro-model date limits (see *The `be-gaap` taxonomy:
   versions, architecture, model / entry-point matrix*).
6. **Validate in the operative profile.** NBB/Biztax: generic XBRL 2.1 +
   Dimensions + Formula with the matching taxonomy package; FSMA: `validate/ESEF`.
   Capture all messages (see *Validation*).
7. **Read Formula assertions as legal controls.** For NBB/Biztax the shipped
   Formula linkbase *is* the arithmetic/logical control set; a failed assertion
   is a legal control failure, not a style warning.
8. **Biztax: two rejection gates.** A technical failure in any one return
   invalidates the whole `.biztax` upload (≤25 returns) and rejects every
   return in it, while a content failure is confined to that return, which is
   stored but not filed; validate each `.xbrl` instance before bundling (see
   the *Biztax* profile).
9. **FSMA: apply the ESEF checklist** (`references/esef.md`), then the Belgian
   mechanics: `.xbri`, ESEF as main document, PDF only as attachment, one ZIP
   per language, deadline of the earlier of AGM − 30 days or year-end +
   4 months (see the *FSMA / ESEF* profile).
10. **CSRD/ESRS: do not require sustainability mark-up.** Mark-up is suspended
    pending the updated ESEF RTS; confirm the live RTS before flagging its
    absence (see *CSRD / ESRS in Belgium and the Omnibus I effect on digital
    tagging*).
11. **State every defect with its version and instrument.** No `FR-BE-*` code
    family exists; cite the RD, CCA/WVV article, technical guide, or FSMA FAQ by
    name, never a fabricated Belgian error code (see *Validation*).

## Authorities and governance

The institutional map a Belgian filing product must hold in its head:

- **NBB Central Balance Sheet Office**: business register / publication organ /
  digital-reporting institution. Collects, validates, publishes, and archives
  statutory annual accounts (~500,000/year, free as PDF/XBRL/CSV), hosts **XBRL
  Belgium**, authors the `be-gaap` `nbb-cbso` taxonomy (`xbrl.be@nbb.be`).
- **Crossroads Bank for Enterprises (KBO / BCE)**: FPS Economy; the
  entity-identifier scheme in NBB instances, auto-recovered by Filing.
- **Accounting Standards Commission (CBN / CNC)**: autonomous body under Code
  of Economic Law **art III.93**; issues accounting opinions, co-develops the
  statutory account models with the NBB, approved the consolidated-accounts
  model (11 December 2019). The official Belgian accounting standard-setter.
- **FPS Finance**: authors `be-tax` and runs **Biztax** (ISOC/VenB corporate,
  BNI/INR non-resident, RPB/IPM legal-entities tax); XBRL 2.1 + Dimensions 1.0 +
  Formula 1.0, annual by assessment year.
- **FSMA**: securities regulator / NCA; supervises listed-issuer periodic
  information, operates eCorporate and the STORI OAM (RD 23 February 2010,
  effective 1 January 2011), and supervises listed-issuer ESRS disclosure (RD 16
  March 2025).
- **NBB, prudential hat**: also the banks/insurers prudential supervisor
  running separate **EBA/EIOPA DPM supervisory reporting (OneGate)**, distinct
  from the CBSO regime (see `references/dpm.md`). Consequence: specific-model
  financial entities file their **CBSO annual accounts as PDF**, not `be-gaap`
  XBRL (see *Accepted formats, controls, decimals, language, fees*).
- **XBRL Belgium**: XBRL International jurisdiction since 15 July 2006, hosted
  by the NBB.

## Coverage and known limitations

**Honest gaps to carry:**

- The `be-tax` **entry-point identifiers** rest on a republished FPS Finance
  presentation rather than the live schemas; confirm against the official `be-tax`
  entry-point schemas before treating them as normative.
- The `.biztax` envelope schema itself was not fetched; the envelope facts come
  from the `be-tax-2026-04-30` Gebruikershandleiding and the FPS Finance
  *Functionaliteiten* page.
- Belgium-specific ESEF guidance beyond the FSMA FAQ was not separately fetched;
  defer generic ESEF/RTS mechanics to `references/esef.md`.

If the question concerns a rule version newer than this file cites, or a Belgian
error code (there is no Arelle `FR-BE-*` family), say so and link the primary
source. The cost of a wrong citation on a regulated filing is high.

## Sources

Cite the live source at filing date; versions and fees change annually. Each
entry notes what it establishes.

**NBB, Central Balance Sheet Office (`be-gaap`):**

- Taxonomy (`nbb-cbso-26.0.15`; XBRL 2.1, self-contained DTS, model matrix incl.
  CbCR `m90-f`):
  <https://www.nbb.be/en/central-balance-sheet-office/preparation-and-filing/technical-information-and-taxonomy-9>
- Chronological taxonomy overview (`25.0.11`, `23.0`, pre-2022 `pfs`):
  <https://www.nbb.be/en/central-balance-sheet-office/preparation-and-filing/technical-information-and-taxonomy-10>
- Filing format (XBRL-vs-PDF eligibility, specific-model PDF rule, 50 MB, RD 29
  April 2019 + Dir 2013/34/EU, paper abolished 1 Jan 2020):
  <https://www.nbb.be/en/central-balance-sheet-office/preparation-and-filing/when-and-how-file/filing-format>
- CBSO technical guide, Version 2026 - 3.0 (18/06/2026), taxonomy version 26.0.15
  (XBRL since 1 April 2007, `.xbrl` mechanics, 50 MB instance/ZIP cap and the
  encapsulated-PDF acceptance criteria, encapsulated XHTML/iXBRL rules, controls as
  Formula linkbase assertions, four-language EN/FR/NL/DE labels, micro-model date
  limits):
  <https://www.nbb.be/doc/ba/xbrl/taxo2026/Taxonomy_technical%20guide_26.0.15.pdf>
  (the superseded 22.9.1 guide, historical reference for the 2022 framework only, is
  still reachable at
  <https://www.nbb.be/doc/ba/xbrl/Taxo2022/Technische%20handleiding/taxonomy_technical_guide_22.9.1.pdf>)
- About the CBSO (mandate, ~500,000/year, free access, history):
  <https://www.nbb.be/en/central-balance-sheet-office/about-central-balance-sheet-office>
- New integrated Filing (2.0 live 4 April 2022; legacy Filing off 1 May 2022):
  <https://www.nbb.be/en/news-events/news/old-filing-application-was-deactivated-1-may-2022-new-integrated-filing>
- Sofista deactivated 4 April 2022:
  <https://www.nbb.be/en/news-events/news/sofista-application-was-deactivated-4-april-2022>
- ESEF start in Belgium: RD of 6 September 2021 (BS 17 Sept 2021), art. 12/1
  inserted into the RD of 14 November 2007 (one-year ESEF postponement to FYs
  beginning on/after 1 Jan 2021)
- 2026 fees + CPI indexing (RD 29 April 2019 arts 3:70/3:118):
  <https://www.nbb.be/en/central-balance-sheet-office/preparation-and-filing/how-and-how-much-pay/filing-fees-0>
- Late-filing surcharge tiers (CCA/WVV art 3:13):
  <https://www.nbb.be/nl/balanscentrale/opmaken-en-neerleggen/hoeveel-betalen/tarieftoeslag-en-beroepsprocedure>
- In welk formaat? (~99% XBRL; euro unit rules):
  <https://www.nbb.be/nl/balanscentrale/opmaken-en-neerleggen/wanneer-en-hoe-neerleggen/welk-formaat>
- Rapportering van duurzaamheidsinformatie (CSRD phase-in; 6 Jan 2025 ZIP
  upload): <https://www.nbb.be/nl/nieuws-en-evenementen/nieuws/rapportering-van-duurzaamheidsinformatie>

**FSMA, ESEF / STORI:**

- ESEF & eCorporate FAQ FSMA_2021_19 (ESEF as official AFR, filed via eCorporate
  not NBB, `.xbri`, PDF as attachment, test env, deadlines):
  <https://www.fsma.be/sites/default/files/media/files/2021-12/fsma_2021_19_en.pdf>
- STORI OAM (designated RD 23 Feb 2010, effective 1 Jan 2011):
  <https://www.fsma.be/en/stori-belgian-official-mechanism-storage-regulated-information>
  (NL: <https://www.fsma.be/nl/informatie-van-genoteerde-vennootschappen-stori>)
- Periodic information (eCorporate→STORI auto-record; AFR deadline):
  <https://www.fsma.be/en/faq/periodic-information>

**FPS Finance, Biztax (`be-tax`):**

- Biztax Characteristics / Functionaliteiten (`.biztax` envelope, max 25 returns,
  technical failure invalidating the whole upload vs content failure confined to
  one return, PDF stored + XBRL retained):
  <https://finance.belgium.be/en/E-services/biztax/how-to-use-biztax/characteristics>
  (NL: <https://financien.belgium.be/nl/E-services/biztax/hoe-biztax-gebruiken/functionaliteiten>)
- `be-tax` 2026-04-30 Gebruikershandleiding XBRL Taxonomie, v1.0 of 2026-04-30
  (`.xbrl` instance = exactly one return, UTF-8, ≤ 15 MB incl. embedded PDFs of
  ≤ 5 MB each, file-name character set; `.biztax` *omslagbestand* of at most 25
  returns):
  <https://financien.belgium.be/sites/default/files/downloads/be-tax-2026-04-30-Gebruikershandleiding.pdf>
- `be-tax` 2025-04-30 Architecture Guide (XBRL 2.1 + Dimensions 1.0 + Formula
  1.0, not iXBRL; annual `be-tax-YYYY-04-30`; fetched in-session, but the
  URL has since been observed CAPTCHA-gated; re-request via the Biztax
  technical-documentation index below if it 403s):
  <https://financien.belgium.be/sites/default/files/downloads/be-tax-2025-04-30-ArchitectureGuide.pdf>
- Biztax technical-documentation index (official; body CAPTCHA-gated this
  session; existence/ownership confirmed, contents not fetched):
  <https://financien.belgium.be/nl/E-services/biztax/technische-documentatie>
- RD 13 April 2025 (return-form model AY2025; mandatory e-filing ITC 1992
  arts 307 §1 / 307bis):
  <https://etaamb.openjustice.be/nl/koninklijk-besluit-van-13-april-2025_n2025003189.html>

**CSRD / ESRS and governance:**

- Law of 2 December 2024, CSRD transposition (amends WVV/CSA, 2002/2016 laws,
  CEL; art 116): <https://www.ejustice.just.fgov.be/eli/wet/2024/12/02/2024011683/justel>
- Law of 12 December 2025, stop-the-clock (Dir (EU) 2025/794; wave 2 → FY2027,
  wave 3 → FY2028): <https://www.ejustice.just.fgov.be/eli/wet/2025/12/12/2025009725/justel>
- RD 16 March 2025, CSRD for listed issuers (ESRS in management report; FSMA
  supervises): <https://etaamb.openjustice.be/nl/koninklijk-besluit-van-16-maart-2025_n2025002457>
- Directive (EU) 2026/470, Omnibus I (**art. 2(9) replaces art. 29d of Directive
  2013/34/EU**: no mark-up until ESEF-RTS rules adopted; recital 24 explains it;
  art. 5 transposition 19 Mar 2027):
  <https://eur-lex.europa.eu/eli/dir/2026/470/oj/eng>
- NBB, *Lijst van ondernemingen onderhevig aan CSRD* (12 May 2026: art. 3:6/8
  WVV; ESEF/ZIP from publication of the revised ESRS; 2026/470 not yet
  transposed; Group 1 FY2024, Group 2 FY2027):
  <https://www.nbb.be/nl/nieuws-en-evenementen/nieuws/lijst-van-ondernemingen-onderhevig-aan-csrd>
- CNC/CBN art III.93, legal basis of the Accounting Standards Commission:
  <https://www.cbn-cnc.be/nl/node/756>

**Secondary / corroborating (Tier 2: informs with caveat, not normative):**
`be-tax` entry points (`be-tax-inc-rcorp` / `-nrcorp` / `-rle`) from a republished
FPS Finance presentation, not the live schemas (confirm before treating as
normative); XBRL International progress report (Nov 2007): XBRL Belgium a
jurisdiction since 15 July 2006; IFRS Foundation Belgium profile: CNC-CBN as
official standard-setter; Loyens & Loeff / EY notes: CSRD Act in force 30 Dec
2024, Directive (EU) 2026/470 in force 18 Mar 2026 (transposition deadline 19 Mar
2027, digital-tagging delegated act expected H2 2026).
