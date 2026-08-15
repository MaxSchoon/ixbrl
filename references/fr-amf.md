# France — ESEF via the AMF, and the honest map of what is *not* iXBRL

Load this when the jurisdiction is **France**: a listed-issuer annual
financial report filed with the **AMF** (Autorité des marchés
financiers), the French statutory annual-accounts deposit, the *liasse
fiscale*, or French banking/insurance supervisory reporting. For ESEF
mechanics common to every EU Member State (legal basis, anchoring, block
tagging, extension taxonomies, the `ESEF.*` codes) stay in `esef.md` —
this file adds only the **France layer** on top of it and must not
duplicate or contradict it.

The single most useful thing here is to **stop an agent from treating a
non-XBRL French obligation as an iXBRL job**. France has exactly one
in-force *inline* XBRL mandate (ESEF, listed issuers with IFRS
consolidated accounts) plus a separate non-inline DPM/xBRL path at the
prudential regulator. Statutory accounts and tax are not XBRL at all.

## 1. Regime map — pin this first

| Filing | Regulator / channel | Format | iXBRL job? |
|---|---|---|---|
| Listed-issuer RFA / DEU-valant-RFA with **IFRS consolidated** accounts | AMF — **ONDE**, archived on **info-financiere.fr** | XHTML **+ Inline XBRL** (ESEF) | **Yes — the core French iXBRL market** |
| Listed-issuer RFA **not** IFRS-consolidated | AMF — ONDE | Plain **XHTML, no XBRL** | No — XHTML formatting, not tagging |
| Statutory annual accounts (*dépôt des comptes annuels*) | **INPI Guichet unique** | **PDF** (or paper deposit) | **No mandate** (honest negative, §3) |
| Corporate tax + accounting schedules (*liasse fiscale*) | **DGFiP** via **EDI-TDFC** | **UN/EDIFACT** (INFENT) | **No — EDIFACT, not XBRL** (§4) |
| Banking / insurance supervisory reporting | **ACPR** via **OneGate** | plain **xBRL** on EBA/EIOPA **DPM** | Not *inline* → `references/dpm.md` (§5) |
| Sustainability statement (CSRD / ESRS) tagging | AMF (future, *rapport de gestion*) | XHTML + iXBRL — **not yet mandatory** | Prepare-ahead only (§6) |

If the task is a row that is not an iXBRL job, say so and route to the
right non-XBRL channel rather than attempting Inline XBRL validation.

## 2. Listed issuers — ESEF filed via the AMF

The AMF is France's NCA for the Transparency Directive (2004/109/CE as
revised by 2013/50/UE), so ESEF Reg. **(UE) 2019/815** applies to every
issuer of shares or bonds admitted to trading on a French regulated
market and subject to that Directive [S5]. Since **1 January 2022**
(financial years opened from 1 January 2021) the *rapport financier
annuel* (RFA) — or the *document d'enregistrement universel valant RFA*
(URD acting as the AFR) — must be filed with the AMF **exclusively in
ESEF** [S1].

**Format split** (identical to `esef.md` §1 Article 4, restated with the
French document names):

- RFA / DEU with **IFRS consolidated** accounts → XHTML with primary
  statements in Inline XBRL, plus block-tagged notes (full-notes block
  tagging has applied to French issuers from FY2022) [S2][S6][S7].
- RFA / DEU with accounts **other than IFRS-consolidated** → plain
  XHTML, **no XBRL markup required** [S2][S7].

**Filing mechanics.**

- The RFA is deposited on the AMF extranet **ONDE**
  (`onde.amf-france.org/RemiseInformationEmetteur/...`), directly by the
  issuer or by a **diffuseur professionnel**; if a diffuseur is used the
  issuer is exempted from filing directly and the diffuseur deposits
  electronically [S2][S4].
- **Instruction AMF DOC-2007-03** (in-force version **02/2025**) is the
  reference text for electronic deposit of regulated information:
  **Annexe 1** specifies the `.zip` / `.xbri` report-package structure,
  **Annexe 2** the accepted formats and languages [S2].
- To open an ONDE deposit account the issuer emails
  `ONDE_Administrateur_Deposant@amf-France.org`; the technical mailbox
  `esefxbrl@amf-france.org` handles ESEF/XBRL questions and pre-filing
  tests [S2][S5][S6].
- Officially filed regulated information is published on
  **info-financiere.fr**, France's Transparency-Directive **OAM**
  (Officially Appointed Mechanism), operated by **DILA**. The AMF ESEF
  FAQ states it verbatim: the AMF transmits RFAs to "la DILA, l'OAM
  français (Officially Appointed Mechanism, mécanisme de stockage
  centralisé des informations réglementées des sociétés cotées)"
  [S5][S1][S6].
- Deadline: the RFA is filed / published / disseminated within **four
  months** of period close [S7].

**Document-typology quirk (a real rejection cause).** On ONDE the filer
must pick the exact typology — *Rapport financier annuel*, or *Document
d'enregistrement universel* with *Vaut RFA = OUI / NON*. A typology
error means the document is **not considered officially filed** and is
not published on the archive [S1][S6]. An otherwise-valid ESEF package
filed under the wrong typology has, in the AMF's terms, not been filed.

**First-year enforcement signal.** At 30 September 2022 (FY2021, first
mandatory year) **98%** of obligated issuers filed successfully; **87%**
prepared IFRS consolidated accounts and so XBRL-tagged their primary
statements; **85%** were conformant on first deposit (~15% filed a
corrective); the AMF ran **300+** pre-filing tests and urges quality
XHTML with proper heading / section tags for machine exploitation [S6].
Use the `esefxbrl@` pre-filing test route before a first deposit.

**Taxonomy version to pin.** The applicable text now cites Reg.
2019/815 **as amended by Reg. (UE) 2025/19** (taxonomy update) [S5] —
the same amendment as `esef.md` §1. The 2025-taxonomy amendment is now
**adopted and in force**: **Commission Delegated Regulation (EU)
2026/283** of 12 Dec 2025 (OJ 18 Mar 2026) — 2025 IFRS taxonomy, IFRS
18/19 elements, a **Calculations 1.1** validity requirement — applying
at the latest for FYs **beginning on/after 1 Jan 2026**, with **early
application allowed for FY2025** [S27]; ESMA has stated it does not
plan to amend the ESEF RTS or taxonomy in 2026 [S33]. Pin the
period from `<xbrli:period>` and confirm the ESEF generation before
declaring a defect.

**French-label / language note.** Beyond the general ESMA Reporting
Manual guidance in `esef.md` §5 (labels in the report language; English
widely recommended), **no AMF-specific French-label rule was located in
Tier-1 AMF sources**. Do not invent one. A French-language report
satisfies `ESEF.3.4.5.missingLabelForRoleInReportLanguage` with French
standard labels on every extension concept; an added English label is a
common recommendation, not a confirmed AMF rule.

## 3. Statutory annual accounts — PDF via INPI, no XBRL (honest negative)

A **verified negative**, checked against actual filing instructions:
French statutory annual-accounts filing has **no XBRL/iXBRL mandate for
the filer**; the accepted format is **PDF**.

- Since **1 January 2023** the *dépôt des comptes annuels* is done
  online on the **INPI Guichet unique** (`procedures.inpi.fr` /
  `formalites.entreprises.gouv.fr`), the single channel for company
  formalities since that date; Infogreffe no longer processes new
  formalities [S8][S10].
- Service-Public fiche **F31214** (fiche verified 11/06/2025): the
  director deposits online on the *guichet des formalités des
  entreprises* (**PDF** via the INPI Guichet unique) **or** by paper /
  in-person deposit at the *greffe du tribunal de commerce*, which
  remains permitted. The earlier "≤ 10 Mo per file, e-signed by the
  director" detail is **not corroborated** by the current fiche and is
  dropped [S8][S9].
- Legal basis: **Arrêté du 7 mai 2021** (décret 2021-300) sets the
  formats / transmission norms of the guichet unique [S10].
- **Structured data is downstream, not filer-facing.** INPI keys
  structured data (*bilans saisis*) **out of** the deposited PDFs and
  exposes them (and the PDFs) via API and Data INPI / the *Registre
  national des entreprises*. The PDF is the filed artefact; there is
  **no XBRL submission by the filer** [S11]. No filer-facing XBRL
  roadmap appears in current INPI instructions [S8][S10][S11].

If asked to "convert the annual accounts for filing at the greffe /
INPI", the correct answer is that INPI accepts a PDF, not iXBRL.

## 4. Tax — the *liasse fiscale* is EDIFACT via EDI-TDFC, not XBRL

The tax return plus accounting schedules go to the **DGFiP** under
**EDI-TDFC** (*Transfert des Données Fiscales et Comptables*), whose
format is **UN/EDIFACT** — the **INFENT** message family (INFENT DF for
the declaration/liasse, AUTACK for securisation, CONTRL for the
syntactic ack) of directory D00B — **not XBRL and not iXBRL** [S13].

- DGFiP adopted EDIFACT per the directive of 16 January 1997; since
  **April 2002 EDI-TDFC is the mandatory EDI format** — on the EDI
  channel only EDI-TDFC-norm transmissions are accepted (EFI, below,
  is the separate online-form channel) [S12].
- Data flows through an accredited *partenaire EDI* via CFT or
  sFTP/FTPS to a DGFiP ESI (Strasbourg); software carries an EDIFICAS
  conformity attestation [S12].
- **EDI-TDFC** (machine-to-machine) or **EFI** (online form) are the two
  channels; EDI-TDFC is mandatory for the *déclaration de résultats* of
  the real regimes (BIC RN, IS RN, BA RN) [S14].
- *API Entreprise* re-exposes liasse data as structured JSON — again
  structured but **not XBRL** [S11].

EDI-TDFC is wholly distinct from any iXBRL obligation; an iXBRL product
does not address the *liasse fiscale*.

## 5. Banking / insurance — ACPR DPM/xBRL via OneGate (not inline)

French prudential reporting is XBRL, but **plain xBRL on the EBA/EIOPA
DPM — not Inline XBRL**. DPM mechanics (Table Linkbase, filing
indicators, xBRL-CSV migration) live in `references/dpm.md`; this is the
French-authority pointer.

- The **ACPR** (Banque de France) collects prudential reporting on
  **OneGate** (`onegate.banque-france.fr`; test at
  `onegate-test.banque-france.fr`) [S15][S17].
- **Insurance.** The **annual** ENS communication obligation is set by
  **instruction ACPR 2023-I-02**; the ENS **submission format/modalities**
  are set by **instruction 2022-I-13** — both stated verbatim on the live
  ACPR ENS page [S18]. Solvency II quantitative states and the
  national-specific states (ENS) are submitted in **XBRL** on the EIOPA
  taxonomy and, for the ENS, an ACPR-provided taxonomy the ACPR calls
  **RAN** — a *taxonomy* name, **not** a state [S18]. Two ENS carry
  special applicability: **FR.29.01** (Solvency-II-data / internal-model
  state) and **FR.11.01** (*réserve de capitalisation*), both confirmed
  on that page [S18]. Narrative reports (RSR, SFCR, ORSA) are office
  formats (PDF/Excel/Word), **not** XBRL. Docs live on **e-SURFI
  Assurance** [S15][S17][S18].
- **Banking.** COREP/FINREP etc. are collected on the **EBA DPM**
  taxonomies (Eurofiling), LEI-identified; EBA Filing Rules apply —
  **v5.8 (25 Feb 2026) is current**; ACPR's Feb 2026 OneGate remittance
  documentation cites v5.7. This artifact churns fast: verify the
  operative version at filing date [S16].
- **Migration signal.** From the **03/2026** reference date, entry
  points previously in **xBRL-XML** must be submitted as **xBRL-CSV**
  (zip, base64 inside the OneGate XML envelope); non-conforming
  remittances are rejected [S16].

All *annule et remplace* (replace-mode) plain xBRL, **not Inline iXBRL**
— a distinct DPM pipeline. See `references/dpm.md`.

## 6. CSRD / ESRS digital tagging — taxonomy exists, mandate not in force

Careful, primary-source: digital tagging of the sustainability statement
is **not yet mandatory** for French issuers.

- **Operative primary source — Directive (EU) 2026/470 (Omnibus I).** In
  force **18 March 2026** (20th day after OJ publication 26 Feb 2026), it
  amends **CSRD Art. 29d** to **expressly suspend** the sustainability
  mark-up obligation: recital 24 states undertakings "should not be
  required to mark up their sustainability reporting" **until** those
  marking-up rules are adopted into Reg. **2019/815**; recital 25 lets a
  **Member State limit** the board's collective responsibility for the
  digitalisation of the management report to its ESEF publication
  (including mark-up) [S30]. This confirms at statute level that ESRS
  digital tagging is **not** a live French obligation.
- **The 2024 taxonomy must be reworked first.** The 30 Aug 2024 EFRAG
  ESRS Set 1 XBRL taxonomy [S23] predates the **Amended ESRS** that
  EFRAG's SRB approved **28 November 2025** (delivered to the Commission
  3 Dec 2025); it must be reworked against the revised ESRS — via the
  Commission's delegated act revising Set 1 — before any ESEF-RTS
  adoption [S31].
- EFRAG published the **ESRS Set 1 XBRL taxonomy** (and the Article 8
  EU-Taxonomy taxonomy) on **30 August 2024** and handed them to ESMA /
  the Commission [S23][S24].
- Tagging becomes mandatory only once the Commission **adopts the
  taxonomy in the ESEF RTS** — a delegated act amending Reg. 2019/815
  that ESMA must prepare. EFRAG states this explicitly and **encourages
  voluntary tagging** meanwhile [S23][S24].
- ESMA consulted on the marking-up rules in Dec 2024 and expected OJ
  publication **not before 2026**, with a two-year phase-in keyed to a
  30-June cut-off; ESAP Phase 1 collection begins July 2026 [S25].
- **XBRL France's GT ESG note (14/01/2026)** confirms it plainly: *"la
  règlementation sur la taxonomie digitale pour les états de durabilité
  n'existe pas à l'heure actuelle"*; most companies have not tagged; it
  advises anticipating the taxonomy at report-design time [S26].
- French legal frame: the *état de durabilité* sits in a distinct
  section of the *rapport de gestion* (art. L.232-6 code de commerce,
  ord. 2023-1142). Wave-1 first CSRD report = FY2024 (H1 2025); the
  FY2025 report (by 30 June 2026) is now **conditional**: Directive (EU)
  2026/470 (Omnibus I) permits Member States to exempt de-scoped wave-1
  undertakings (below the new >€450M turnover AND >1,000 employee
  thresholds) from FY2025-FY2026 reporting — check France's
  transposition (due 19 Mar 2027) for whether the exemption is
  exercised [S29][S30]. The AMF's 2024 stock-take describes
  the future digital obligation (XHTML with XBRL tags under a *nouvelle
  taxonomie digitale*) as **forthcoming** [S29].

**Caution on a secondary claim.** A French practitioner article asserts
XHTML + XBRL ESEF tagging of the sustainability statement is **already**
required for wave-1 FY2025 via the "OAM" portal [S28]. This
**overstates** the position; the Tier-1 EFRAG / ESMA sources establish
that ESRS digital tagging is not mandatory until the ESEF-RTS delegated
act is adopted [S23][S24][S25][S26]. Voluntary tagging is possible and
worth building toward, but do not tell a French issuer it is a live
obligation. (ESRS Set 1 labels are English-only at the EFRAG/ESMA
stage; the Commission handles translation on adoption.)

## 7. France-specific XBRL history (context, mostly legacy)

- **XBRL France** is a *loi-1901* non-profit founded 2005, the French
  Jurisdiction of XBRL International and a founding XBRL Europe member;
  it remains active on the ESG front (§6) [S19][S26].
- Its historic French-GAAP taxonomy — *Taxonomie Comptes Annuels* (TCA)
  **v3.0, 31/12/2010**, built on the *Plan Comptable Général* (Règlement
  CRC 99-03), CNC-conformant labels — has a **no-longer-active** working
  group, though the taxonomy remains available [S20].
- Historic fact: the TCA **was** used by **Infogreffe** for
  dematerialised XBRL deposit of *comptes sociaux* — France once had a
  live statutory-accounts XBRL channel — now **superseded** since
  Infogreffe stopped processing formalities and INPI accepts PDF (§3)
  [S20][S10].
- Framework context: the PCG is **Règlement ANC n° 2014-03**; the
  standard-setter lineage is CNC (1957) + CRC (1998) → **ANC**
  (ordonnance du 22 janvier 2009) [S21][S22]. **No current mandatory
  PCG / French-GAAP XBRL taxonomy is in production filing use** — the
  TCA is legacy [S20].

## 8. What an iXBRL product can serve today (synthesis)

- **Serveable now (true iXBRL / ESEF):** the AMF-regulated RFA /
  DEU-valant-RFA for issuers with **IFRS consolidated** accounts — XHTML
  + inline primary statements + block-tagged notes, packaged `.zip` /
  `.xbri`, filed on ONDE (directly or via diffuseur), archived on
  info-financiere.fr. The core live iXBRL market [S1][S2][S5][S6][S7][S27].
- **Formatting only, not tagging:** RFA **not** IFRS-consolidated → plain
  XHTML [S2][S7].
- **Not served by iXBRL:** statutory *dépôt* (PDF via INPI) [S8][S9][S11];
  *liasse fiscale* (EDIFACT via EDI-TDFC) [S12][S13]; ACPR
  banking/insurance (plain xBRL on DPM via OneGate) [S16][S17].
- **Prepare-ahead (not yet mandatory):** ESRS/CSRD sustainability-
  statement tagging — taxonomy exists, mandate pending the ESEF-RTS
  delegated act; voluntary tagging is possible today [S23][S25][S26].

## 9. Arelle / validation notes (France layer)

- **Listed-issuer path is pure ESEF** — validate against the ESEF
  disclosure system exactly as in `esef.md` / `validation.md`. Base
  taxonomy = ESEF/IFRS (Reg. 2019/815 as amended by 2025/19 and, for
  the 2025 taxonomy, **Reg. (EU) 2026/283** — applying for FYs from
  1 Jan 2026 with early FY2025 option and requiring the instance +
  extension to be valid under **Calculations 1.1**) [S5][S27]. The AMF accepts the package as `.zip`
  **or** `.xbri` (inlineXbrlDocumentSet), layout per DOC-2007-03 Annexe
  1 [S2] — use the same package harness / Calc 1.1 mode as other ESEF
  NCAs.
- **Non-IFRS-consolidated RFA:** plain XHTML, no XBRL — check
  well-formed XHTML only [S2][S7].
- **ACPR is a different profile:** EBA/EIOPA DPM taxonomies (Eurofiling),
  plain xBRL not inline, OneGate, xBRL-XML today → xBRL-CSV from 03/2026.
  Use EBA/EIOPA taxonomy packages + the current EBA Filing Rules
  (v5.8 as of Feb 2026), **not** the ESEF disclosure system
  [S16][S17][S18]. See `references/dpm.md`.
- **No Arelle / XBRL path** for statutory accounts (PDF via INPI)
  [S9][S11] or the *liasse fiscale* (EDIFACT/INFENT) [S12][S13] — do not
  attempt iXBRL validation there.
- **ESRS / CSRD is prepare-ahead only:** the EFRAG ESRS Set 1 taxonomy
  exists (English-only labels) for voluntary tagging, but is not yet an
  adopted ESEF-RTS taxonomy, so there is no mandatory validation profile
  yet [S23][S25][S26].

## 10. Stakeholders and governance (the French institutional map)

Who owns each layer of electronic business reporting in France, and how
they interlock. Detail lives in the sections cited — this is only the map.

- **Business register & publication organ — INPI + BODACC.** The **INPI**
  runs the *Registre national des entreprises* and the Guichet unique
  that receives the *dépôt des comptes annuels* and keys structured data
  out of the deposited PDFs (§3). Official publicity of acts registered
  in the RNE — including account deposits — is given by the **BODACC**
  (*Bulletin officiel des annonces civiles et commerciales*, bodacc.fr)
  [S32]. No filer-facing XBRL layer sits here.
- **Digital-business-reporting programme — no SBR-Nederland analogue.**
  France has **no** single national SBR programme on one taxonomy; the
  nearest actor is **XBRL France** (loi-1901 jurisdiction body, §7), and
  structured filing is split by domain across the DGFiP (§4) and ACPR
  (§5). State this gap rather than imply an SBR equivalent [S19].
- **Accounting standards setter — ANC.** The *Autorité des normes
  comptables* sets French GAAP (the PCG, Règlement ANC 2014-03); lineage
  CNC→CRC→ANC (§7) [S21].
- **Taxonomy author / governance.** For the only inline mandate, **ESMA**
  authors the ESEF RTS taxonomy the Commission adopts into Reg. 2019/815,
  on an **annual IFRS-taxonomy cadence**, published in the EU Official
  Journal / ESMA's ESEF pages (§2, §9). The legacy French **TCA** (XBRL
  France) is **no longer maintained** (§7) [S20].
- **Tax authority (structured filing) — DGFiP.** Runs the *liasse
  fiscale* via EDI-TDFC in UN/EDIFACT — structured but not XBRL (§4).
- **Securities regulator (NCA) — AMF.** France's Transparency-Directive
  NCA; receives ESEF filings on ONDE and archives them on
  info-financiere.fr (§2).
- **Financial-sector overlay — ACPR (Banque de France).** Collects
  banking/insurance prudential reporting as plain xBRL on the EBA/EIOPA
  DPM via OneGate (§5).

They interlock only loosely: AMF/ESEF, DGFiP/EDI-TDFC, ACPR/DPM and
INPI/PDF are **separate rails** on different formats with no unifying
digital-reporting institution — which is why this file routes each
obligation to its own channel (§1).

## 11. Relation to EU reporting (ESEF and CSRD context)

France is an EU Member State; the France layer sits on the EU rails in
`esef.md`. Delta-only — cross-references, not duplication.

- **ESEF / Transparency-Directive transposition.** ESEF applies through
  the AMF as NCA under the TD (2004/109/CE, rev. 2013/50/UE), with
  info-financiere.fr as France's TD storage mechanism (§2). No national
  *inline* format competes with ESEF — unlike the Dutch SBR/KvK route,
  France adds only document-typology and deposit mechanics on top of the
  common ESEF rules (§2, `esef.md`).
- **Coexistence with national structured regimes.** The non-ESEF French
  structured filings (EDI-TDFC tax §4; ACPR DPM §5; INPI PDF §3) are
  **not** iXBRL and do not overlap ESEF — they coexist on separate rails
  (§1, §10).
- **CSRD / ESRS trajectory — now expressly suspended.** **Directive (EU)
  2026/470** (Omnibus I, in force 18 Mar 2026) amends CSRD Art. 29d to
  suspend sustainability mark-up until Reg. 2019/815 is updated, and lets
  a Member State limit board responsibility for the digital management
  report; the 2024 EFRAG taxonomy must first be reworked against the
  Amended ESRS (approved 28 Nov 2025) [S30][S31]. Not a live French
  obligation — build toward it, do not tell an issuer it is mandatory
  (§6, §8).

## 12. Honest gaps (do not assert beyond these)

- **ONDE successor.** The current AMF text (DOC-2007-03, 02/2025) still
  designates **ONDE**; no renamed/replacement system was surfaced [S2].
- **OJ date of the ESRS ESEF-RTS delegated act** (the mandatory-tagging
  trigger) is not fixed; ESMA said "not before 2026" with a
  30-June-keyed phase-in [S25].
- **French-language ESEF labels.** No AMF-specific French-label rule was
  located; `esef.md` §5 general guidance stands (§2).
- **INPI XBRL roadmap.** INPI keys structured data out of PDFs [S11];
  no announced plan to move filers to structured/XBRL submission was
  found — treated as absent, not confirmed-absent-by-statement.
- **info-financiere.fr as formal "OAM"** — resolved: the AMF ESEF FAQ
  [S5] confirms the OAM designation and names **DILA** as its operator;
  the earlier Tier-3-only sourcing concern no longer applies.
- **ESRS mark-up now statutorily suspended.** Directive (EU) 2026/470
  (Omnibus I, in force 18 Mar 2026) suspends the sustainability mark-up
  until Reg. 2019/815 is updated, and the underlying taxonomy must be
  reworked against the Amended ESRS (SRB approval 28 Nov 2025) — so no
  mandatory ESRS tagging profile exists yet [S30][S31] (§6, §11).

## 13. Primary sources

Verify the operative version of every cited rule at filing date.

- **[S1]** AMF — *Formats et modalités de dépôt des RFA et DEU valant RFA à compter du 1er janvier 2022* — <https://www.amf-france.org/fr/actualites-publications/actualites/formats-et-modalites-de-depot-des-rapports-financiers-annuels-et-des-documents-denregistrement>
- **[S2]** Instruction **AMF DOC-2007-03** (v. 02/2025) — modalités de dépôt de l'information réglementée — <https://www.amf-france.org/sites/institutionnel/files/private/2025-02/instruction-amf-doc-2007-03-bon-pour-publication-v2bis.pdf>
- **[S4]** AMF — *Je dépose de l'information en dehors d'une opération financière* — <https://www.amf-france.org/fr/espace-professionnels/societes-cotees-et-emetteurs/mes-relations-avec-lamf/deposer-de-linformation-financiere-et-extra-financiere/en-dehors-dune-operation>
- **[S5]** AMF — *ESEF : vos questions fréquentes* — <https://www.amf-france.org/fr/actualites-publications/dossiers-thematiques/esef/esef-vos-questions-frequentes>
- **[S6]** AMF — *ESEF : les émetteurs au rendez-vous dès la première année* — <https://www.amf-france.org/fr/actualites-publications/actualites/esef-les-emetteurs-au-rendez-vous-des-la-premiere-annee>
- **[S7]** AMF — *Guide de l'information périodique des sociétés cotées* (déc. 2024) — <https://www.amf-france.org/sites/institutionnel/files/private/2024-12/2016-05-decembre-2024.pdf>
- **[S8]** INPI — *Dépôt des comptes annuels* — <https://www.inpi.fr/realiser-demarches/formalites-dentreprises/depot-comptes-annuels>
- **[S9]** Service-Public Entreprendre — *Dépôt des comptes annuels d'une société* (F31214) — <https://entreprendre.service-public.gouv.fr/vosdroits/F31214>
- **[S10]** INPI — *Textes réglementaires du Guichet unique* (Arrêté du 7 mai 2021) — <https://www.inpi.fr/ressources/formalites-dentreprises/textes-reglementaires-du-guichet-unique>
- **[S11]** INPI — *Documentation technique API comptes annuels* (V4/V5) — <https://www.inpi.fr/sites/default/files/2025-06/documentation%20technique%20API_comptes_annuels%20v5.pdf>
- **[S12]** DGFiP — *Cahier des charges EDI-TDFC Volume II (2025)* — <https://www.impots.gouv.fr/sites/default/files/media/1_metier/3_partenaire/edi/cdc_edi_tdfc/2025/volume_ii_tdfc_2025.pdf>
- **[S13]** DGFiP — *Cahier des charges EDI-TDFC Volume IV (2026)* — <https://www.impots.gouv.fr/sites/default/files/media/1_metier/3_partenaire/edi/cdc_edi_tdfc/2026/volume_iv_tdfc_2026.pdf>
- **[S14]** DGFiP — *Obligations de téléprocédures* — <https://www.impots.gouv.fr/professionnel/obligations-de-teleprocedures-0>
- **[S15]** ACPR — *Guide formalités, reportings et notifications (organismes d'assurance)* — <https://acpr.banque-france.fr/fr/professionnels/lacpr-vous-accompagne/parcours-fintech/contenus-pedagogiques/formalites-reportings-et-notifications/guide-formalites-reportings-et-notifications-pour-les-organismes-dassurance>
- **[S16]** eSurfi Banque — *Format de remise Banque* — <https://esurfi.banque-france.fr/fr/esurfi-banque/informations-techniques/documentation-technique/format-de-remise-banque>
- **[S17]** ACPR — *Pilier 3 : le format de communication Solvabilité II* — <https://acpr.banque-france.fr/fr/reglementation/focus-sur-la-reglementation/assurance/solvabilite-ii/pilier-3-le-format-de-communication-des-informations-solvabilite-ii>
- **[S18]** ACPR — *Pilier 3 : les exigences nationales complémentaires (ENS)* — <https://acpr.banque-france.fr/fr/reglementation/focus-sur-la-reglementation/assurance/solvabilite-ii/pilier-3-les-exigences-nationales-complementaires>
- **[S19]** XBRL France — *À propos* — <https://www.xbrlfrance.org/?page_id=15>
- **[S20]** XBRL France — *Taxonomie Comptes Annuels (TCA)* — <https://www.xbrlfrance.org/?page_id=124>
- **[S21]** ANC — *Recueils des normes comptables / Plan Comptable Général* — <https://www.anc.gouv.fr/normes-comptables-francaises/recueils-des-normes-comptables>
- **[S22]** Revue Française de Comptabilité — *Un référentiel comptable qui fait autorité* — <https://revuefrancaisedecomptabilite.fr/un-referentiel-comptable-qui-fait-autorite/>
- **[S23]** EFRAG — *EFRAG publishes the ESRS Set 1 XBRL Taxonomy* (30 Aug 2024) — <https://www.efrag.org/sites/default/files/sites/webpublishing/SiteAssets/2024-08-30%20EFRAG%20publishes%20the%20ESRS%20Set%201%20XBRL%20Taxonomy%20.pdf>
- **[S24]** EFRAG — *ESRS XBRL Taxonomy* (concluded project) — <https://www.efrag.org/en/projects/esrs-xbrl-taxonomy/concluded>
- **[S25]** ESMA — *CP: ESEF RTS marking-up rules for sustainability reports & financial notes* (Dec 2024) — <https://www.esma.europa.eu/sites/default/files/2024-12/ESMA32-2009130576-3024_CP_ESEF_RTS_-_marking_up_rules_for_sustainability_reports_and_financial_notes_and_EEAP_RTS_-_amendments.pdf>
- **[S26]** XBRL France GT ESG — *Points d'attention pour la digitalisation des rapports de durabilité* (14/01/2026) — <https://www.xbrlfrance.org/wp-content/uploads/2026/02/Taxonomie-ESG-Points-dattention-et-recommandations-XBRL-France_v1def.pdf>
- **[S27]** Commission Delegated Regulation (EU) 2026/283 of 12 Dec 2025 (adopted as C(2025) 8507; OJ 18 Mar 2026) — 2025 ESEF taxonomy update; Calc 1.1; IFRS 18/19 — <https://eur-lex.europa.eu/eli/reg_del/2026/283/oj>
- **[S33]** ESMA — *ESMA support ESEF implementation with updated taxonomy* (21 Apr 2026; states no ESEF RTS/taxonomy amendment planned in 2026) — <https://www.esma.europa.eu/press-news/esma-news/esma-support-esef-implementation-updated-taxonomy>
- **[S28]** Réglementation Environnement (blog, **Tier 3 — overstated**) — *CSRD juin 2026 : deuxième rapport, contrôle AMF* — <https://www.reglementation-environnement.com/csrd-premiers-rapports-large-companies-juin-2026-amf-sanctions/>
- **[S29]** AMF — *Bilan 2024 du reporting de durabilité des sociétés cotées* — <https://www.amf-france.org/sites/institutionnel/files/private/2024-12/rapport-amf-2024-bilan-reporting-durabilite-des-societes-cotees_fr.pdf>
- **[S30]** Directive **(EU) 2026/470** (Omnibus I), 24 Feb 2026, OJ L 26 Feb 2026 — amends CSRD Art. 29d (recital 24: mark-up suspended until Reg. 2019/815 updated; recital 25: Member-State board-responsibility limit) — <https://eur-lex.europa.eu/eli/dir/2026/470/oj/eng>
- **[S31]** EFRAG — *EFRAG provides its technical advice on draft simplified (Amended) ESRS to the European Commission* (EFRAG SRB approval 28 Nov 2025; delivered 3 Dec 2025) — <https://www.efrag.org/en/news-and-calendar/news/efrag-provides-its-technical-advice-on-draft-simplified-esrs-to-the-european-commission>
- **[S32]** BODACC — *Bulletin officiel des annonces civiles et commerciales* (publicité des actes enregistrés au RNE) — <https://www.bodacc.fr/>

For anything ESEF-general, return to `esef.md`. When a question concerns
a rule version newer than this file cites, or a French mechanism not
covered here, say so and link the primary source rather than guessing.
