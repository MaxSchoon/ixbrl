# Germany (Deutschland) — E-Bilanz, HGB Offenlegung, and the German ESEF layer

Load this when the entity is German and the filing is one of three
structured-reporting regimes: **E-Bilanz** (tax XBRL under § 5b EStG),
**Offenlegung / Hinterlegung** (statutory publication of annual accounts
under §§ 325 ff. HGB to the Unternehmensregister), or **ESEF** (listed
Inlandsemittent under § 114 WpHG / § 328 Abs. 1 HGB, BaFin as NCA). The
most important fact for an iXBRL practitioner is in §1: **only the ESEF
regime is Inline XBRL** — the other two are plain XBRL 2.1 instances. For
generic ESEF mechanics (anchoring, block tagging, Reporting Manual,
report-package layout, `ESEF.*` codes) stay in `esef.md`; for bank/insurer
prudential DPM reporting use `dpm.md`. This file carries **only the German
jurisdiction layer**.

## Table of contents

1. Which regime? — the three-way split and the bi-temporal warning
2. Regime A — E-Bilanz (§ 5b EStG): scope, exemptions, transmission
3. Regime A — the HGB taxonomy family and its yearly cadence
4. Regime B — Offenlegung / Hinterlegung (§§ 325 ff. HGB)
5. Regime B — accepted formats, size classes, and enforcement
6. Regime C — the German ESEF layer (§ 114 WpHG / § 328 HGB, BaFin)
7. CSRD / ESRS — the German transposition state and the Omnibus effect
8. Stakeholders and governance (who does what)
9. Relation to EU reporting (how the national formats coexist with ESEF)
10. Validation how-to — and the honest Arelle gap
11. A pragmatic German review pass — in order
12. Honest gaps
13. Primary sources

---

## 1. Which regime? — the three-way split and the bi-temporal warning

Germany runs **three separate structured-reporting regimes** with
different legal bases, formats, taxonomies, recipients, and validators. A
converter product must serve them differently; conflating them is the
first and most expensive mistake.

| | **A — E-Bilanz** | **B — Offenlegung / Hinterlegung** | **C — ESEF** |
|---|---|---|---|
| Legal basis | § 5b EStG | §§ 325 ff. HGB | § 114 WpHG · § 328 Abs. 1 HGB |
| Purpose | Tax balance sheet + P&L to the Finanzverwaltung | Statutory publication of annual accounts | Listed-issuer annual financial report |
| Format | **plain XBRL 2.1** instance | **XML/XBRL default** (Word/PDF accepted with a fee) | **XHTML + iXBRL** |
| Taxonomy | HGB-Taxonomie (fiscal entry point) | HGB / IFRS / US-GAAP | ESEF core (Del. Reg. (EU) 2019/815) |
| Recipient | Länder-Finanzämter via ELSTER/ERiC | Unternehmensregister via Publikations-Plattform | Unternehmensregister; supervised by BaFin |
| Validator | ERiC (no Arelle plugin) | register-operator intake checks (no Arelle plugin) | Arelle ESEF plugin |

**The iXBRL point.** Only regime C is Inline XBRL. Regime A is
transmitted "in Form eines XBRL-Datensatzes" — a plain XBRL instance, not
iXBRL (BMF Grundlagen-Schreiben zu § 5b EStG). Regime B defaults to plain
XML/XBRL on the HGB taxonomy. Do not build an iXBRL pipeline for E-Bilanz
or ordinary HGB Offenlegung; build it for the listed-issuer ESEF path and
route its generic mechanics to `esef.md`.

**Bi-temporal warning.** As in every regime, the rules in force *when a
report was prepared* are not necessarily the rules in force today.
Germany makes this acute on several axes at once:

- **E-Bilanz taxonomy** is versioned yearly by a dated BMF-Schreiben
  (v6.9 for Wirtschaftsjahre beginning after 31 Dec 2025; v6.10 for those
  beginning after 31 Dec 2026). Pin the taxonomy version to the
  Wirtschaftsjahr, not to the calendar.
- **DiRUG (in force 1 Aug 2022)** moved the Offenlegung filing point from
  the Bundesanzeiger to the Unternehmensregister for Geschäftsjahre
  beginning after 31 Dec 2021 (Art. 88 Abs. 2 EGHGB). A FY2021 deposit
  and a FY2022 deposit go to nominally different destinations.
- **FISG (in force 1 Jul 2021; single-tier Bilanzkontrolle effective
  1 Jan 2022)** replaced the two-tier Bilanzkontrolle
  with single-tier BaFin enforcement.
- **CSRD-UG** (German CSRD transposition) was **still not enacted** as of
  the research window (early-mid 2026); do not assume a specific § 289b
  ff. HGB text. See §7.

State the regime, the reporting year, and the taxonomy/rule version
explicitly before you call anything a defect.

---

## 2. Regime A — E-Bilanz (§ 5b EStG): scope, exemptions, transmission

**Legal basis.** § 5b EStG requires taxpayers determining profit under
§ 4 Abs. 1, § 5 or § 5a EStG to transmit the *content* of the balance
sheet and P&L as an "amtlich vorgeschriebener Datensatz" by
Datenfernübertragung — including the un-condensed **Kontennachweise**
(account-level breakdown with balances), the **Anlagenspiegel**
(fixed-asset schedule) and its Anlagenverzeichnis. Where book values
deviate from tax rules, the filer either adjusts them through a structured
**Überleitungsrechnung** (Handelsbilanz → Steuerbilanz reconciliation) or
transmits a tax-compliant balance sheet directly (§ 5b Abs. 1 EStG). In
force since 1 Jan 2009, first mandatory for Wirtschaftsjahre beginning
after 31 Dec 2010 (§ 52 Abs. 15a EStG); the BMF blesses the dataset under
the § 51 Abs. 4 Nr. 1b EStG delegation.

**Scope of "balance sheet".** Every balance-sheet type transmittable to
the tax administration: Jahresabschluss, Umwandlungs-, Eröffnungs-,
Zwischen-, Liquidations- (Anfangs/Zwischen/Schluss)bilanz, Aufgabebilanz
(§ 16 EStG). For Personengesellschaften / Mitunternehmerschaften the
Kontennachweis must accompany the Gesamthandsbilanz and any Sonder- /
Ergänzungsbilanzen.

**FY2025 content change.** The **Jahressteuergesetz 2024** (BGBl. I 2024
Nr. 387, 2 Dec 2024) amended § 5b Abs. 1 EStG: for Wirtschaftsjahre
beginning after 31 Dec 2024 the **un-condensed Kontennachweise with
account balances become mandatory**, and the Anlagenspiegel remains a
Mussfeld (per BMF-Schreiben of 24 May 2016). Kontennachweis fields are
position name, account number, account description, and balance;
aggregation (Verdichtung) of individual accounts is generally not
permitted. A converter that condensed accounts to save space now produces
an incomplete FY2025 dataset.

**Exemption.** § 5b Abs. 2 EStG lets the tax authority, on application,
waive electronic transmission to avoid *unbillige Härte* (§ 150 Abs. 8 AO)
— typically for disproportionate cost or lack of technical capability.
Enforcement of the e-transmission duty is by Zwangsgeld (§§ 328 ff. AO).

**Transmission.** ELSTER is the authenticated channel; **ERiC** (ELSTER
Rich Client) is the interface for § 5b EStG submissions. No separate
signature or encryption is required, because transmission is authenticated
over ELSTER (eSteuer.de FAQ). There is no web upload and no Arelle gate on
this path — the authoritative validator is ERiC against the BMF-adopted
taxonomy version (§10).

---

## 3. Regime A — the HGB taxonomy family and its yearly cadence

**Author and blessing.** The E-Bilanz data schema is the **HGB-Taxonomie**,
authored by **XBRL Deutschland e.V.** and adopted by the BMF as the amtlich
vorgeschriebener Datensatz; published at `www.esteuer.de` and
`de.xbrl.org`.

**Two-module structure.** A **GCD module** (Global Common Document /
Stammdaten- und Berichtsprüfungsmodul — document, report, and
reporting-entity master data; standard-independent) plus a **GAAP module**
(Kerntaxonomie — the accounting content of Bilanz, GuV, Ergebnisverwendung,
Kapitalkontenentwicklung, Anhang). Around these sit **Branchentaxonomien**
(BRA module) and **Spezial-/Erweiterungstaxonomien** for regulated sectors
— FI (financial institutions / RechKredV), INS (insurers), PI, plus
KHBV/PBV forms.

**The fiscal entry point.** For an E-Bilanz submission use **only** the GCD
module plus the *"GAAP steuerlicher Einzelabschluss"* entry-point schema.
The fiscal module replaces position labels, deletes commercial-only
positions from the presentation view, and changes calculation rules
relative to the commercial GAAP module. Respect the position status flags:
**Mussfeld** (mandatory; omitting fails ERiC intake), **notPermittedFor=
steuerlich** (invalid in a Steuerbilanz — a Handelsbilanz must dissolve any
tax-impermissible position through the Überleitungsrechnung), and
**validThrough** (date-limits a position across versions).

**Versioning cadence** — one taxonomy version per year, each announced by a
dated BMF-Schreiben:

| Version | BMF-Schreiben | Applies to Wirtschaftsjahre beginning after | Echtfälle from |
|---|---|---|---|
| v6.9 | 10 Jun 2025 (GZ IV C 6 - S 2133-b/00064/002/006) | 31 Dec 2025 (WJ 2026) | ~May 2026 |
| v6.10 | 8 Jun 2026 | 31 Dec 2026 (WJ 2027) | ~May 2027 |

Each version's use for the immediately prior Wirtschaftsjahr is "nicht
beanstandet" (tolerated); v6.10 flags a data-model modernisation as a
"Previewfassung" for testing only. Do not cite a version from memory — read
the operative BMF-Schreiben (§13).

**DiFin overlay.** The same HGB taxonomy underpins the **DiFin** (Digitaler
Finanzbericht) programme; from v6.6 a `relevanceDiFin` attribute marks
positions relevant to the DiFin data set. DiFin reuses the taxonomy — it is
not a fourth filing regime.

---

## 4. Regime B — Offenlegung / Hinterlegung (§§ 325 ff. HGB)

**Legal basis.** § 325 HGB: the legal representatives of a
Kapitalgesellschaft must file the festgestellter Jahresabschluss,
Lagebericht, Bestätigungsvermerk, and the § 264 Abs. 2 S. 3 / § 289 Abs. 1
S. 5 declarations for publication, at latest **one year after the
Abschlussstichtag** (§ 325 Abs. 1a HGB).

**The DiRUG filing-point shift.** The Gesetz zur Umsetzung der
Digitalisierungsrichtlinie (**DiRUG**, in force 1 Aug 2022) moved where the
documents go. For Geschäftsjahre beginning **after 31 Dec 2021** they are
transmitted to "die das Unternehmensregister führende Stelle" for insertion
into the **Unternehmensregister** — no longer "eingereicht" at the
Bundesanzeiger; for those **before 1 Jan 2022** the old Bundesanzeiger route
still applies (Art. 88 Abs. 2 EGHGB). DiRUG re-worded §§ 325, 325a, 326,
327, 328, 329, 339 HGB accordingly.

**The operator fact that trips people up.** Both the Bundesanzeiger and the
Unternehmensregister are operated by the **same private entity —
Bundesanzeiger Verlag GmbH, Köln** — the "registerführende Stelle" (a
beliehene Stelle). All transmission goes through its **Publikations-Plattform**
(`www.publikations-plattform.de`) or a Webservice interface. Paper is
impossible; filing is **not** to the BMJ or the BfJ. The DiRUG "destination
change" is a legal re-labelling of the same operator and platform — do not
tell a filer to switch systems.

**Hinterlegung vs Offenlegung.** A **Kleinstkapitalgesellschaft** (§ 267a
HGB) may satisfy its duty by transmitting only the Bilanz for permanent
**deposit** (dauerhafte Hinterlegung) under § 326 Abs. 2 HGB rather than
public disclosure. The choice is one-way — once it opts for publication it
cannot convert back. The register body checks only *fristgemäß / vollzählig*
(timeliness/completeness), not content correctness (§ 329 HGB).

---

## 5. Regime B — accepted formats, size classes, and enforcement

**Accepted formats.** § 11 URV (Unternehmensregisterverordnung) designates
**XML** as the "maßgebliches Übermittlungsformat" for
Rechnungslegungsunterlagen. The register accepts XML/XBRL on a
Bundesanzeiger-Verlag XSD or web form, **and separately** Word (from Office
2000), RTF, Excel, and PDF — but any non-XML format incurs a conversion fee
(Konvertierungsentgelt, § 15 Abs. 1 S. 2 URV). So XBRL is **cost-privileged
and accepted, but not strictly mandatory**: a filer may submit Word/PDF and
pay for conversion, and small companies (§ 267 Abs. 1 HGB) may use
Eingabeformulare at the XML flat rate. (Whether XBRL is strictly compulsory
for any size class is an honest gap — §12.)

**HGB XBRL intake validation.** The register accepts HGB, IFRS, and US-GAAP
taxonomies. On intake it validates that every concept has a **label-linkbase
entry** (Terse or Standard) in the publication language (`*de` / `*en`)
**and** a **presentation-linkbase position**, and it **rejects extension
taxonomies** that reference concepts over the internet or create standalone
report parts. A "BA-Jahresabschluss-XHTML" add-on XSD lets filers embed
simple layout in XBRL footnotes; invalid fragments cause rejection. This is
the operator's own annahme check, not an Arelle plugin (§10).

**Size classes** (§§ 267, 267a HGB, by Bilanzsumme / Umsatzerlöse /
Arbeitnehmer over two years) drive scope:

| Size class | Filing extent | Auditor's report |
|---|---|---|
| Kleinst (§ 267a) | Bilanz only; Hinterlegung option (§ 326 Abs. 2) | No |
| klein (§ 267 Abs. 1) | Bilanz + Anhang, Anhang without P&L disclosures (§ 326 Abs. 1) | No |
| mittelgroß / groß | full extent per § 328 | Yes |

**Enforcement — two offences, one authority.** Enforcement is by the
**Bundesamt für Justiz (BfJ, Bonn)** — separate from the register operator
and from BaFin:

- **§ 335 HGB Ordnungsgeld** targets *not / late / incomplete filing*. The
  BfJ opens with an **Androhungsverfügung** giving a six-week Nachfrist; if
  the company files after it or not at all, the Ordnungsgeld is set. The
  minimum is **EUR 2.500** (§ 335 Abs. 4 S. 2 Nr. 3 HGB where a higher
  amount was threatened and a mittelgroße/große Gesellschaft files late);
  BfJ practice escalates toward EUR 5.000 on repetition. Filing within the
  Nachfrist does **not** waive the procedure fee (§ 335 Abs. 3 S. 2 HGB:
  the Verfahrenskosten are imposed with the Androhung and survive timely
  cure), and a later reduction may account only for circumstances arising
  before the Bundesamt's decision (§ 335 Abs. 4 S. 3 HGB). As an *echtes Unterlassungsdelikt* the
  two-year Verfolgungsverjährung (Art. 9 Abs. 1 EGStGB) starts only once
  the duty is properly fulfilled — a Jahresabschluss marked "vor
  Feststellung" does **not** satisfy § 325 (OLG Köln, 28 Wx 1/24, 3 Apr
  2024).
- **§ 334 HGB Bußgeld** targets *content* violating HGB form/content rules
  (inhaltlich unrichtiger Abschluss), also run by the BfJ.

§ 335 = wrong *timing/completeness*; § 334 = wrong *content*.

---

## 6. Regime C — the German ESEF layer (§ 114 WpHG / § 328 HGB, BaFin)

This is the only iXBRL regime. For anchoring, block tagging, the
Reporting Manual, report-package layout, and `ESEF.*` codes, use
`esef.md`. This section supplies **only** the German additions.

**Legal basis in German law.**

- **§ 114 WpHG** requires an **Inlandsemittent** (§ 2 Abs. 14 WpHG) to
  prepare its Jahresfinanzbericht "nach Maßgabe der Delegierten Verordnung
  (EU) 2019/815" (the ESEF RTS), make it public at latest **four months**
  after year-end, notify BaFin of the Hinweisbekanntmachung, and transmit
  it to the register-keeping body for insertion into the
  Unternehmensregister.
- **§ 117 WpHG** extends this to the IFRS consolidated group report and
  Konzernlagebericht.
- **§ 328 Abs. 1 HGB** independently requires an Inlandsemittent (not a
  § 327a issuer) to disclose the § 328 Abs. 1 S. 1 documents in the
  einheitliches elektronisches Berichtsformat per Art. 3 of Del. Reg. (EU)
  2019/815.

  *(§ 117 WpHG and § 328 HGB were verified via mirrors, corroborated by the
  Bundestag materials below — §12.)*

**Transposition.** The requirement entered German law via the *Gesetz zur
weiteren Umsetzung der Transparenzrichtlinie-Änderungsrichtlinie …*
(12 Aug 2020, BGBl. I S. 1874), applying first to Jahresfinanzberichte for
**Geschäftsjahre beginning after 31 Dec 2019**. The Bundestag materials
(Drucksache 19/17343) confirm **XHTML + iXBRL mark-up of IFRS consolidated
statements** per Art. 4/6 ESEF-VO, and that §§ 316/317 HGB extend the
statutory audit to whether the offenlegung wiedergabe is "ESEF-konform".

**Filing point.** The ESEF report is transmitted through the
Bundesanzeiger-Verlag Publikations-Plattform to the Unternehmensregister;
the intake offers three uploads (native ESEF report, further ESEF files,
further components) accepting XHTML, ZIP, PDF, or Bundesanzeiger-XML,
conditioned on Geschäftsjahresbeginn ≥ 1 Jan 2020 and issuer status under
§ 2 Abs. 14 WpHG. German-language extension labels are the norm (the
register's XBRL intake requires a publication-language label). The NCA and
enforcer is **BaFin**, not the register operator.

**BaFin — two functions.** BaFin (Bundesanstalt für
Finanzdienstleistungsaufsicht) is Germany's securities NCA under the WpHG:

1. **Finanzberichterstattung oversight** (§§ 114 ff. WpHG):
   Inlandsemittenten publish Jahres-/Halbjahresfinanzberichte, announce
   them via Hinweisbekanntmachung (to BaFin through the MVP-Portal), and
   transmit them to the Unternehmensregister. BaFin can order compliance
   and impose Zwangsgelder / Geldbußen — e.g. EUR 190.000 against ETC
   Issuance GmbH (24 Mar 2023), EUR 220.000 threatened against Singulus
   (7 Feb 2022), EUR 690.000 against Marudai Food (2 Feb 2022).
2. **Bilanzkontrolle** (Abschnitt 16 Unterabschnitt 1 WpHG, § 106 ff.):
   BaFin checks the legality of accounts and management reports of
   capital-market-oriented Herkunftsstaat-Germany issuers, on a sample and
   cause basis. **Post-Wirecard**, the **Gesetz zur Stärkung der
   Finanzmarktintegrität (FISG)** replaced, from 1 Jan 2022, the two-tier
   system (private *Deutsche Prüfstelle für Rechnungslegung e.V.*, DPR, on
   tier 1; BaFin on tier 2) with a **single-tier procedure, BaFin as sole
   authority** (DPR abolished). FISG gave BaFin sovereign powers
   (information rights against "jedermann" on concrete grounds, summons,
   search/seizure), let Anlassprüfungen reach the two preceding financial
   years, and let BaFin publish error findings and require Neuaufstellung /
   Fehlerkorrektur.

`esef.md` §7 already lists BaFin/Bundesanzeiger among the NCAs; treat this
as the deeper German cut, not a duplicate.

---

## 7. CSRD / ESRS — the German transposition state and the Omnibus effect

**Germany was and remains late.** The CSRD (Directive (EU) 2022/2464)
should have been transposed by **6 Jul 2024**; missing it triggered an EU
infringement procedure. A 2024 draft died with the Ampel coalition; a
Referentenentwurf (10 Jul 2025) and a Regierungsentwurf of a
**CSRD-Umsetzungsgesetz (CSRD-UG)** followed on 3 Sep 2025, incorporating
the Omnibus "stop-the-clock" two-year deferral (Art. 96 Abs. 3/4 EGHGB-E).
As of the research window (early-mid 2026) the CSRD-UG was **still not
enacted**: Rechtsausschuss Änderungsanträge on 31 Mar 2026, public hearing
13 Apr 2026, a SPD/CDU-CSU amendment folding in Omnibus I (Directive (EU)
2026/470). The final enactment date and § 289b ff. HGB text are not yet
fixed — an honest gap (§12). Because no HGB amendment passed, the
pre-existing (NFRD-based) regime remains in force for FY2025; large German
PIEs largely applied ESRS 1.0 voluntarily (advisory/chamber analysis, §12).

**Omnibus I — Directive (EU) 2026/470** (24 Feb 2026, in force 18 Mar
2026; CSRD-amending provisions to be transposed by 19 Mar 2027, CSDDD by 26
Jul 2028) removes the Commission's power to adopt sector-specific ESRS
(only the cross-cutting ESRS under Del. Reg. (EU) 2023/2772 remain),
reduces scope, and defers first application by two years.

**The ESEF-relevant suspension — read before tagging ESRS.** Recital 24 of
Directive (EU) 2026/470 addresses Art. 29d of Directive 2013/34/EU (which
requires sustainability reporting to be marked up in the ESEF format of
Del. Reg. (EU) 2019/815): **until** those mark-up rules are adopted via an
update to Del. Reg. (EU) 2019/815, undertakings should **not** be required
to mark up their sustainability reporting; Recital 25 lets Member States
limit management-body digitalisation responsibility to publication in the
single electronic format including mark-up. Consequence: **ESRS digital
tagging is effectively suspended pending the ESEF RTS update — do not
attempt mandatory ESRS iXBRL mark-up for German filers in 2026.**

---

## 8. Stakeholders and governance (who does what)

The three regimes are run by different bodies; a filer who sends the right
file to the wrong body gets nowhere.

- **Bundesanzeiger Verlag GmbH, Köln** — a single private operator that is
  **both** the Betreiber des Bundesanzeigers **and** "die das
  Unternehmensregister führende Stelle" (beliehene Stelle). Runs the
  Publikations-Plattform that ingests **all** Offenlegung / Hinterlegung
  and ESEF filings and performs the HGB-XBRL intake validation.
- **Unternehmensregister** — statutory filing point since DiRUG (1 Aug
  2022) for Geschäftsjahre beginning after 31 Dec 2021; the Bundesanzeiger
  remains the point for earlier years.
- **Finanzverwaltung (Länder-Finanzämter) under the BMF** — receives
  E-Bilanz via ELSTER/ERiC. The **BMF** issues the annual
  taxonomy-adopting BMF-Schreiben (§ 51 Abs. 4 Nr. 1b EStG).
- **XBRL Deutschland e.V.** (`de.xbrl.org`, `info@xbrl.de`) — authors the
  **HGB-Taxonomie** (GCD + GAAP + BRA + special modules) used for **both**
  E-Bilanz and Offenlegung; versions at `www.esteuer.de` and `de.xbrl.org`.
- **DiFin (Digitaler Finanzbericht)** — joint XBRL Deutschland / banks /
  Finanzverwaltung programme for structured annual-account exchange; drives
  the `relevanceDiFin` attribute from v6.6.
- **DRSC (Deutsches Rechnungslegungs Standards Committee e.V.)** —
  national accounting standards body; active in the CSRD-UG consultation.
  It does **not** author the XBRL taxonomies.
- **BaFin** — securities NCA: WpHG oversight of Inlandsemittenten,
  ESEF/financial-reporting enforcement, and the **sole Bilanzkontrolle
  authority** since FISG.
- **Bundesamt für Justiz (BfJ, Bonn)** — runs the § 335 HGB Ordnungsgeld
  and § 334 HGB Bußgeld procedures; distinct from the register operator and
  from BaFin.
- **Financial-sector overlays** — special taxonomies (FI for credit
  institutions under RechKredV, INS for insurers, KHBV/PBV forms) attach to
  both E-Bilanz and Offenlegung. Bank **prudential** reporting runs on the
  **EBA DPM**, a separate regime — see `dpm.md`.

---

## 9. Relation to EU reporting (how the national formats coexist with ESEF)

- **Transparency Directive (2004/109/EC) → ESEF.** § 114 WpHG and § 328 HGB
  transpose the ESEF format (Del. Reg. (EU) 2019/815) for Inlandsemittenten,
  first applicable for Geschäftsjahre beginning after 31 Dec 2019.
- **Accounting Directive (2013/34/EU).** The HGB size classes (§§ 267, 267a)
  and disclosure regime (§§ 325 ff.) implement it. CSRD (Directive (EU)
  2022/2464) amends 2013/34/EU and is the still-pending German CSRD-UG (§7).
- **ESRS trajectory.** ESRS are a directly-applicable delegated regulation
  (Del. Reg. (EU) 2023/2772) needing no national transposition, so they
  bind in-scope German undertakings even while the CSRD-UG lags. Omnibus I
  (Directive (EU) 2026/470) reforms ESRS and **suspends the digital mark-up
  requirement** until the ESEF RTS is updated (§7).

**The coexistence rule (practitioner takeaway).** A **non-listed HGB
entity** files **E-Bilanz** (plain XBRL 2.1 → Finanzverwaltung) **and**
**Offenlegung** (XML/XBRL default → Unternehmensregister) — **neither is
iXBRL**. A **listed Inlandsemittent** files its Jahresfinanzbericht in
**ESEF** (XHTML/iXBRL) to the Unternehmensregister, supervised by BaFin; its
HGB Offenlegung duty is satisfied through that ESEF report per § 328 Abs. 1
HGB — the plain-XBRL Offenlegung route is **replaced by ESEF**. Do not
expect a separate HGB-XBRL deposit alongside the ESEF filing.

---

## 10. Validation how-to — and the honest Arelle gap

The installed **arelle-release is version 2.41.6**; its `plugin/validate`
directory ships exactly **CIPC, DBA, EBA, EDINET, ESEF, FERC, NL, ROS, UK**
— **no Germany-specific national plugin.** Map the regimes to what can and
cannot be gated deterministically:

1. **E-Bilanz (§ 5b EStG) — NO deterministic Arelle validator here.**
   Authoritative validation is **ERiC** against the BMF-adopted taxonomy
   version, plus the taxonomy's own **Mussfeld / notPermittedFor=steuerlich
   / validThrough** flags and calc rules. A converter **cannot gate an
   E-Bilanz with Arelle.** Do not imply otherwise.
2. **HGB Offenlegung XBRL — validated at intake by the Bundesanzeiger-Verlag
   / Unternehmensregister annahme checks** (label + presentation completeness
   in the publication language; extension-reference restrictions), **not** an
   Arelle national plugin.
3. **ESEF (§ 114 WpHG / § 328 HGB) — IS covered.** Because ESEF is the
   harmonised EU format (Del. Reg. (EU) 2019/815), the Arelle **ESEF plugin**
   validates the German listed-issuer filing like any other ESEF report.
   Route to `esef.md` §8 for the `ESEF.*` codes and use the standard
   pipeline:

   ```bash
   scripts/validate_with_arelle.sh report.zip core   # base XBRL 2.1
   scripts/validate_with_arelle.sh report.zip esef   # ESEF.* rules
   ```
4. **Bank prudential (supervisory DPM) — covered by the EBA plugin**, a
   **separate regime** from all three above. See `dpm.md`.

**Net.** Only the ESEF (listed-issuer) side is deterministically validatable
with the shipped Arelle plugins; E-Bilanz and HGB Offenlegung require ERiC
and the register operator's intake validation respectively. Do not present
an Arelle "clean" result as evidence that an E-Bilanz or an ordinary HGB
Offenlegung will be accepted. (The "no DE plugin" finding is scoped to
arelle-release 2.41.6 — §12.)

---

## 11. A pragmatic German review pass — in order

Walk this in order; each step depends on the prior being clean.

1. **Identify the regime.** A plain XBRL instance bound for ELSTER/ERiC is
   E-Bilanz; a plain XML/XBRL (or Word/PDF) deposit to the
   Publikations-Plattform is Offenlegung; an XHTML/iXBRL report package is
   ESEF. Only ESEF is iXBRL. State it back before opening the file.
2. **Pin year and version.** E-Bilanz taxonomy by Wirtschaftsjahr (v6.9 /
   v6.10, §3); DiRUG filing-point split by Geschäftsjahr (§4); ESEF
   taxonomy year (`esef.md`).
3. **Pin the size class** (Kleinst / klein / mittelgroß / groß, §5) — it
   changes which absences are defects (Bestätigungsvermerk requirement;
   Hinterlegung availability).
4. **E-Bilanz:** confirm the fiscal entry point (GCD + "GAAP steuerlicher
   Einzelabschluss"), Mussfelder populated, no surviving
   `notPermittedFor=steuerlich` position, and — for WJ after 31 Dec 2024 —
   un-condensed Kontennachweise (§2). No Arelle gate; validation is
   ERiC-side (§10).
5. **HGB Offenlegung:** confirm each concept has a publication-language
   label and a presentation position, and no extension references concepts
   over the internet (register intake rejects these, §5). A non-XML format
   means a conversion fee, not an error.
6. **ESEF:** run the full ESEF review in `esef.md`, then add the German
   layer — German extension labels, the four-month deadline and
   Hinweisbekanntmachung to BaFin (§ 114 WpHG), and that the § 328 HGB
   Offenlegung duty is satisfied by this ESEF report (§9). **Do not require
   ESRS iXBRL mark-up for 2026 filings** — suspended pending the ESEF RTS
   update (§7).
7. **Route enforcement to the right body:** § 335 / § 334 HGB → BfJ;
   ESEF/Bilanzkontrolle → BaFin; E-Bilanz Zwangsgeld → Finanzamt (§§ 328
   ff. AO). § 335 Ordnungsgeld (late/incomplete filing) ≠ § 334 Bußgeld
   (wrong content).

---

## 12. Honest gaps

Per the skill's honest-gap discipline, what could not be pinned to a
current primary source:

- **Offenlegung taxonomy version.** The exact HGB/German-GAAP taxonomy
  version used for **Offenlegung** (vs E-Bilanz) was not pinned: a
  Publikations-Plattform FAQ still references "German GAAP Version 2.0" for
  the XML/XBRL route, which looks dated relative to the E-Bilanz v6.9/v6.10
  line. Whether Offenlegung uses the same version as E-Bilanz is unconfirmed
  — re-check before asserting one.
- **Is XBRL mandatory for Offenlegung?** § 11 URV names XML the maßgebliches
  Format and non-XML incurs a fee, but the sources do **not** state XBRL is
  compulsory for all size classes. Treated here as **"default, not strictly
  mandatory."** A full-text § 11 URV / § 328 HGB reading was not obtained.
- **CSRD-UG enactment.** Still a draft in the research window (RegE 3 Sep
  2025; hearing 13 Apr 2026; Omnibus I folded in). The eventual adoption
  date and final § 289b ff. HGB text must be re-verified.
- **Operator ESEF acceptance criteria.** The detailed "ESEF-Berichte
  Einreichungskriterien Standards" document (viewer, ZIP structure,
  extension handling) was not fetched in full; German-layer ESEF intake
  specifics beyond the format list are not exhaustively cited.
- **Arelle plugin scope.** The "no DE plugin" finding is scoped to the
  installed **arelle-release 2.41.6**; newer/third-party distributions were
  not inspected.
- **Statutory-mirror citations.** § 328 HGB, § 117 WpHG, and § 106 WpHG were
  verified via commercial/legal-database mirrors
  (handelsgesetzbuch-hgb.com, dejure.org), corroborated by BaFin/legislative
  sources; re-confirm the pinpoint wording against gesetze-im-internet for a
  normative citation.

---

## 13. Primary sources

Regulator and gesetze-im-internet sources are primary; legal-database
mirrors and advisory/professional analyses are marked *(tier 2)* / *(tier
3)* where a claim rests on them (honest-gap discipline). Each line notes
what the source establishes.

**Regime A — E-Bilanz**

- § 5b EStG — <https://www.gesetze-im-internet.de/estg/__5b.html> — the
  E-Bilanz duty: content, Kontennachweise/Anlagenspiegel,
  Überleitungsrechnung, Härtefall waiver (Abs. 2).
- BMF-Schreiben 8 Jun 2026 (Taxonomien 6.10) —
  <https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Einkommensteuer/2026-06-08-ebilanz-taxonomien-6-10.pdf?__blob=publicationFile&v=4>
  — v6.10 for WJ after 31 Dec 2026; Previewfassung; yearly cadence.
- BMF-Schreiben 10 Jun 2025 (Taxonomien 6.9) —
  <https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Einkommensteuer/2025-06-10-ebilanz-taxonomien-6-9.pdf?__blob=publicationFile&v=7>
  — v6.9 (WJ 2026); JStG 2024 mandatory un-condensed Kontennachweise for WJ
  after 31 Dec 2024; balance-sheet types; Kontennachweis field spec.
- BMF Grundlagen-Schreiben zu § 5b EStG —
  <https://www.esteuer.de/download/bmf-schreiben_grundlagen_e-bilanz_2009-0865962.pdf>
  — E-Bilanz transmitted "in Form eines XBRL-Datensatzes" (plain XBRL, not
  iXBRL); first WJ after 31 Dec 2010; Zwangsgeld; § 51 Abs. 4 Nr. 1b.
- eSteuer.de E-Bilanz FAQ 2026-01 —
  <https://www.esteuer.de/download/taxonomie/FAQ_Version_2026-01.pdf> —
  ELSTER/ERiC-authenticated transmission; no separate signature/encryption.
- XBRL Deutschland — Technischer Leitfaden HGB-Taxonomie —
  <http://de.xbrl.org/technischer_leitfaden_hgb-taxonomie_2010-09-27.pdf> —
  GCD + GAAP architecture; fiscal entry point; status flags;
  Überleitungsrechnung; sector modules.
- XBRL Deutschland — HGB-Taxonomie v6.6 —
  <https://de.xbrl.org/taxonomien/e-bilanz-hgb-taxonomie-version-6-6/> —
  taxonomy underpins E-Bilanz and DiFin; `relevanceDiFin` from v6.6.
  *(Haufe corroborates ERiC as the § 5b EStG interface — tier 3.)*

**Regime B — Offenlegung / Hinterlegung**

- § 325 HGB — <https://www.gesetze-im-internet.de/hgb/__325.html> —
  disclosure duty; 12-month deadline; transmission to the register body.
- § 335 HGB — <https://www.gesetze-im-internet.de/hgb/__335.html> — the
  Ordnungsgeld regime for non/late/incomplete Offenlegung.
- DiRUG (BGBl.) —
  <https://www.bmjv.de/SharedDocs/Downloads/DE/Gesetzgebung/BGBl/Bgbl_DiRUG.pdf?__blob=publicationFile&v=3>
  — re-wording of §§ 325–329, 339 HGB; Art. 88 → GJ after 31 Dec 2021.
- Unternehmensregister — Nutzungsbedingungen —
  <https://unternehmensregister.de/i18n-doc/D061_UReg_nutz_0118_de.pdf> —
  DiRUG split; accepted formats (XML/XBRL, ESEF); Kleinst Hinterlegung
  § 326 Abs. 2; irreversible publication choice.
- Publikations-Plattform — Startseite — <https://publikations-plattform.de/>
  — § 11 URV XML as maßgebliches Format; Konvertierungsentgelt; ESEF
  exception for Jahresfinanzberichte/Inlandsemittenten.
- Bundesanzeiger Verlag — Arbeitshilfe Rechnungslegung (D004) —
  <https://publikations-plattform.de/sp/i18n/doc/D004_Arbeitshilfe_Rechnungslegung.pdf?document=D153&language=de>
  — accepted formats; small-company input forms; ESEF three-upload intake.
- Publikations-Plattform — XBRL-Taxonomie für Jahresabschlüsse —
  <https://publikations-plattform.de/sp/service?global_data.designmode=pp&page.navid=to_tech_std_annual_xbrl_taxonomie&dest=service&global_data.language=de&start=new>
  — HGB taxonomy by XBRL Deutschland; intake requires label + presentation
  per concept; extension-reference restrictions; BA-XHTML add-on.
- BfJ — Merkblatt Offenlegungspflicht —
  <https://www.bundesjustizamt.de/SharedDocs/Downloads/DE/EHUG/Merkblatt_Offenlegungspflicht_Rechnungslegungsunterlagen.pdf?__blob=publicationFile&v=1>
  — size-class scope; filing to Bundesanzeiger Verlag Köln; Art. 88 Abs. 2.
- BfJ — Ordnungsgeldverfahren —
  <https://www.bundesjustizamt.de/DE/Themen/OrdnungsgeldVollstreckung/Jahresabschluesse/Offenlegung/Verfahren/Verfahren_node.html>
  — Androhungsverfügung → 6-week Nachfrist; EUR 2.500 minimum; escalation.
- BfJ — FAQ (§ 335 vs § 334) —
  <https://www.bundesjustizamt.de/DE/Themen/OrdnungsgeldVollstreckung/Jahresabschluesse/Verstoesse/Fragen/Fragen_node.html>
  — § 335 (filing) vs § 334 (content); OLG Köln 28 Wx 1/24.
- *(tier 2 — private HGB mirror; corroborated by Drucksache 19/17343)*
  § 328 HGB — <https://www.handelsgesetzbuch-hgb.com/hgb/328.html> —
  Inlandsemittent discloses in ESEF per Art. 3 Del. Reg. (EU) 2019/815.

**Regime C — ESEF (German layer) and BaFin**

- § 114 WpHG — <https://www.gesetze-im-internet.de/wphg/__114.html> —
  Jahresfinanzbericht per Del. Reg. (EU) 2019/815; 4-month publication;
  Hinweisbekanntmachung to BaFin; transmission to Unternehmensregister.
- *(tier 2 — dejure)* § 117 WpHG —
  <https://dejure.org/gesetze/WpHG/117.html> — extends §§ 114/115 to the
  IFRS consolidated group report.
- Bundestag Drucksache 19/17343 —
  <https://dserver.bundestag.de/btd/19/173/1917343.pdf> — § 114 WpHG →
  ESEF-VO; XHTML + iXBRL of IFRS consolidated statements per Art. 4/6;
  first GJ after 31 Dec 2019; §§ 316/317 HGB audit → ESEF-Konformität.
- BaFin — Finanzberichterstattung —
  <https://www.bafin.de/DE/Aufsicht/BoersenMaerkte/Transparenz/InformationspflichtenEmittenten/Finanzberichterstattung/finanzberichterstattung_artikel.html>
  — NCA role; enforcement examples (ETC Issuance, Singulus, Marudai).
- BaFin — Bilanzkontrolle —
  <https://www.bafin.de/DE/unternehmen-maerkte/aufsicht/emittenten/bilanzkontrolle/bilanzkontrolle_node.html>
  — post-Wirecard FISG single-tier Bilanzkontrolle (DPR abolished);
  sovereign powers; two-prior-year reach. (BaFin restructured its site
  in 2026; the former `.../Transparenz/Bilanzkontrolle/...` article URL
  is dead.)
- *(tier 2 — dejure; corroborated by BaFin)* § 106 WpHG —
  <https://dejure.org/gesetze/WpHG/106.html> — BaFin's mandate over
  Herkunftsstaat-Germany issuers' accounts.

**CSRD / ESRS / Omnibus**

- Directive (EU) 2026/470 (Omnibus I), OJ —
  <https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ%3AL_202600470>
  — Recital 24 suspends ESRS mark-up until Del. Reg. (EU) 2019/815 is
  updated; Recital 25 management-body limitation; ESRS reform mandate.
- *(tier 2 — law firm)* King & Spalding — Omnibus I —
  <https://www.kslaw.com/news-and-insights/simplification-of-eu-sustainability-legislation-omnibus-package-set-to-enter-into-force>
  — adopted 24 Feb 2026, in force 18 Mar 2026; transposition 19 Mar 2027.
- DRSC — CSRD-UG Anhörung & Änderungsantrag —
  <https://www.drsc.de/news/csrd-umsetzungsgesetz-oeffentliche-anhoerung-aenderungsantrag/>
  — CSRD-UG status; Änderungsanträge 31 Mar 2026; hearing 13 Apr 2026;
  CSRD deadline was 6 Jul 2024; ESRS directly applicable.
- *(tier 2 — professional chamber)* WPK — Q&A CSRD-UG (7 Jan 2026) —
  <https://www.wpk.de/fileadmin/documents/Wissen/Nachhaltigkeit/WPK_Nachhaltigkeit_CSRD_Fragen_Antworten_Anwendung_Umsetzung_07-01-2026.pdf>
  — RegE 3 Sep 2025; Omnibus deferral in Art. 96 Abs. 3/4 EGHGB-E.
- *(tier 2 — advisory firm)* PKF — Nachhaltigkeit 2026 Status quo —
  <https://www.pkf.de/pkf-magazin/ausgaben/2026/ausgabe-1-26/nachhaltigkeitsberichterstattung-status-quo>
  — FY2025: NFRD regime stays; voluntary ESRS 1.0.

**Environment evidence**

- Installed arelle-release 2.41.6 `plugin/validate` listing — ships CIPC,
  DBA, EBA, EDINET, ESEF, FERC, NL, ROS, UK; **no German (DE) plugin**.
  Establishes the deterministic-validation gap for E-Bilanz and HGB
  Offenlegung (§10). Scoped to this installed version.

For anything newer than these sources — a passed CSRD-UG, an updated
E-Bilanz taxonomy version, an ESEF RTS update that re-enables ESRS
mark-up — re-verify against the live regulator page before acting. The
cost of a wrong citation on a regulated filing is high.
