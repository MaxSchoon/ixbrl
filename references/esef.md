# European Single Electronic Format (ESEF) — Reference

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*


Working reference for iXBRL annual financial reports under the EU ESEF mandate. Verify the operative version of every cited rule against the live source at filing date.

## 1. Legal basis

The ESEF mandate is established by **Commission Delegated Regulation
(EU) 2019/815 of 17 December 2018**, supplementing **Directive
2004/109/EC** (Transparency Directive) with regulatory technical
standards (RTS) on a single electronic reporting format. The Regulation
has been amended several times — the consolidated version applicable
from 1 January 2025 incorporates **Commission Delegated Regulation (EU)
2025/19** of 26 September 2024 (the 2024 taxonomy update).

**Scope.** Issuers whose securities are admitted to trading on an EU
regulated market and that are subject to the Transparency Directive's
annual financial report obligation — in practice EU listed-issuer
parent entities preparing IFRS consolidated annual financial reports.

**Article-level requirements:**

- **Article 3** — Issuers must prepare the **entire annual financial report in XHTML format** (single human-readable rendering).
- **Article 4** — Where the AFR contains **IFRS consolidated financial statements**, issuers must **mark up those statements** (Art. 4(1)), covering at a minimum the disclosures specified in **Annex II** (Art. 4(2)) — the Annex II Table 2 block-tagging obligation applying from financial years beginning on or after 1 January 2022. Markup uses the **XBRL markup language** and a taxonomy whose elements are those of the **core taxonomy** (Annex VI plus the presentation, calculation, label and definition linkbases, per Art. 2(1)); where it is not appropriate to use a core element under Annex IV point 4, the issuer must create **extension taxonomy elements** in accordance with Annex IV (Art. 4(4)). Article 4 does not itself impose Inline XBRL; that requirement sits in Article 6.
- **Article 6** — Common rules on markups: markups made under Articles 4 and 5 must be **embedded in the XHTML annual financial report using the Inline XBRL specifications set out in Annex III** (Art. 6(a)), and must respect the **marking up and filing rules set out in Annex IV** (Art. 6(b)).
- **Article 8** — Effective dates: detailed primary-statement tagging from financial years beginning on or after 1 January 2020; block tagging of notes from financial years beginning on or after 1 January 2022. (Some Member States including the Netherlands took a one-year deferral, so first NL filings landed in 2022.)

**Annex II** lists IFRS disclosures subject to mandatory tagging — Table
1 (detailed tagging from 2020) and Table 2 (block tagging from 2022).
**Annex III** sets the applicable specifications: the Inline XBRL
instance document must be valid against **Inline XBRL 1.1** and conform
to the **XBRL Units Registry** (point 1); extension taxonomy files must
be valid against **XBRL 2.1** and **XBRL Dimensions 1.0** (point 2); the
report is submitted as a single reporting package conforming to **Report
Packages 1.0** (point 3, as amended by Delegated Regulation (EU)
2023/2686); and, as added by Delegated Regulation (EU) 2025/19, the
instance must be valid against the **Calculations 1.1** specification
(point 5). **Annex IV** (Marking up and filing rules) contains the
technical mark-up specification: §9(b) is the wider-narrower anchoring
obligation for extension elements. **Annex VI** lists the core ESEF
taxonomy concepts.

## 2. The ESEF Reporting Manual

ESMA's principal interpretive guidance, republished annually as
**ESMA32-60-254**. Current edition is the **2025 update**, hosted at
https://www.esma.europa.eu/document/esef-reporting-manual.

The Manual is **not a regulation** — it has no direct legal force —
but national competent authorities and the ESEF Conformance Suite use
it operationally, so non-conformance materially raises filing risk.

**Structure.** Numbered "Guidance" items in a hierarchical scheme
(`1.1`, `1.4.1`, `2.2.6`, `3.1.3`):

- **Section 1** — Scope, multilingual reporting, extensions, anchoring, block tagging.
- **Section 2** — Technical iXBRL construction (contexts, units, transformations, hidden facts, CSS/HTML constraints, report packages).
- **Section 3** — Extension taxonomy construction (DTS structure, labels, presentation, calculation, dimensional validity).
- **Section 4** — Filings without IFRS consolidated statements (XHTML-only).

**Eleven consequential rules every preparer/auditor should know:**

1. **Guidance 1.4.1 — Anchoring extension elements wider.** Each extension concept used in primary statements must be anchored to the closest **wider** ESEF/IFRS taxonomy concept. Anchoring is not required for extensions used only in notes/accounting policies.
2. **Guidance 1.2.2 — IFRS elements not yet in the ESEF taxonomy.** Where the IFRS Taxonomy contains an element corresponding to a disclosure but the ESEF taxonomy does not yet include it, the issuer *should* define an extension element whose name, label and XBRL characteristics correspond to those of the IFRS element (ESMA's worked example: `issuer_prefix:PropertyPlantAndEquipmentIncludingRightofuseAssets` mirroring `ifrs-full:PropertyPlantAndEquipmentIncludingRightofuseAssets`). Rollover: as soon as the element is included in the ESEF core taxonomy as published in the EU Official Journal, the issuer adopts the ESEF element — and uses it for the comparative figures in the current report too, since the RTS requires every number in a declared currency presented in the primary financial statements, comparatives included, to be marked up.
3. **Guidance 1.9 — Block tagging.** Issuers shall, as a minimum, mark up the information in the IFRS consolidated financial statements — headers and titles included — with the Annex II `textBlockItemType` elements (1.9.1). Where one disclosure corresponds to more than one Annex II element of different granularity, preparers should apply each of them and multi-tag the information to the extent that matches its accounting meaning, rather than choosing between the wider and the narrower element (1.9.1). ESMA recommends that the lowest level of block-tagging granularity be the individual table within a note: the tag goes on the whole table, not on selected rows or columns (1.9.2). A disclosure with no corresponding Annex II element need not be block tagged, and no extension element need be created for it (1.9.3). Mandatory Annex II elements take precedence over the optional Annex VI elements even where an Annex VI element has a closer accounting meaning (footnote 21).
4. **Guidance 2.2.5 — Tagging of dashes and empty fields.** Dashes representing zero use a transformation (`ixt:fixed-zero`); truly empty cells are tagged with `xsi:nil="true"`.
5. **Guidance 2.2.6 — Readability after extraction.** Word and number ordering, spacing, and tabular structure of block-tagged content must be machine-readable in a way that is faithful to the visual report.
6. **Guidance 2.6.1 — Report Package conformance.** The submitted ZIP must conform to the XBRL Taxonomy/Report Package Specification.
7. **RTS Annex IV §9(b) — Narrower anchoring.** Where an extension concept combines two or more core taxonomy concepts, it must be anchored to **each** narrower base concept in addition to its wider anchor.
8. **Section 3.4 series — Labels.** Each extension carries a standard label in the entity's reporting language; preferred-label roles supplied where presentation arcs require them.
9. **Guidance 3.1.2 — Correct ESEF taxonomy entry point.** The DTS must import the ESEF entry point matching the financial year.
10. **Guidance 2.4 — Hidden facts.** Facts in `ix:hidden` must either be transformable element types or carry the specific `-esef-ix-hidden` style tying them to a visible value; hidden non-transformable facts must not duplicate visible content.
11. **Guidance 1.2.1 — Non-endorsed IFRS elements are for third-country issuers only.** The ESEF taxonomy contains all elements of the IFRS Taxonomy regardless of their endorsement status in the EU, but the elements corresponding to IFRS not endorsed by the EU exist solely to let third-country issuers listed in the EU (equivalence under Commission Decision 2008/961/EC) comply. EU issuers should under no circumstances use those elements to tag their consolidated financial statements, because doing so would breach Regulation (EC) No 1606/2002 by cross-reference to Annex IV §3 of the RTS.

### 2.1 ESEF audit and assurance

ESEF has a stronger auditor-involvement model than Dutch KvK SBR Report
Packages. The closest sources are the **Commission Interpretative
Communication 2020/C 379/01** and the **CEAOB Guidelines on auditors'
involvement on financial statements in ESEF** (adopted 9 November
2021).

The Commission's position: Union law requires statutory auditors to
provide an audit opinion on whether the financial statements included
in the annual financial report comply with the relevant ESEF statutory
requirements, and that opinion belongs in the audit report. CEAOB then
turns that into practical audit-work expectations.

For ESEF review work, treat the auditor's ESEF procedures as covering:

- Understanding the issuer's ESEF preparation process and related
  controls, including whether conversion is outsourced or tool-driven.
- Verifying that all financial statements in the AFR are prepared in
  XHTML.
- If the audited version was not originally prepared in ESEF format,
  reconciling the XHTML financial statements to the audited version for
  full alignment.
- Obtaining sufficient appropriate evidence over required and
  voluntary markups.
- Verifying completeness of required primary-statement numeric tagging
  and Annex II note block tagging.
- Testing whether selected taxonomy elements have the closest
  accounting meaning, whether extensions comply with Annex IV, and
  whether markups comply with Annex III / Annex IV.
- Considering risks that marked-up information does not correspond to
  the human-readable layer, including wrong period, currency, sign,
  scale, context, concept selection, or extension use.

This is different from a pure technical-validation pass. Software
validation is evidence, not the audit conclusion: CEAOB also expects
materiality, risk assessment, communication of misstatements, written
representations, documentation, and audit-report consequences where
material ESEF non-compliance exists or the auditor cannot obtain
sufficient appropriate evidence.

ESMA treats the ESEF filing as the official annual financial report for
Transparency Directive purposes. If a PDF or other convenience version
is also published, do not treat it as the filed AFR; use it only as a
cross-check and make clear which version is authoritative. National
competent authorities may add local mechanics — for example electronic
signature requirements or portal-specific submission rules — but they
do not displace the EU-level XHTML / iXBRL obligations.

## 3. Block tagging vs detailed tagging

ESEF imposes **two complementary regimes** on issuers preparing IFRS
consolidated AFRs:

- **Detailed tagging** (Article 4 + Annex II Table 1; mandatory from FY2020). Each numeric line item in the four primary statements — Statement of Financial Position, Statement of P&L / OCI, Statement of Changes in Equity, Statement of Cash Flows — is tagged with an `ix:nonFraction` pointing to the matching IFRS or extension concept. Contexts, units (`iso4217:EUR`), decimals, signs all required. Calculation linkbase relationships must reconcile (subject to rounding).
- **Block tagging** (Article 6 + Annex II Table 2; mandatory from FY2022). Entire note disclosures are wrapped in `ix:nonNumeric` text-block elements with `escape="true"`. The aim is structured retrieval of narrative — auditors should expect explicit tags like `ifrs-full:DisclosureOfBasisOfPreparationOfFinancialStatementsExplanatory` plus *escaped* HTML preserving tables, lists, and headings inside the block.

A typical narrative block tag:

```html
<ix:nonNumeric
   name="ifrs-full:DisclosureOfRevenueExplanatory"
   contextRef="c-Group-2025"
   escape="true">
  <h3>Note 4. Revenue</h3>
  <p>Revenue is recognised when control of the goods or services...</p>
  <table>...</table>
</ix:nonNumeric>
```

Block tags must satisfy Manual Guidance 2.2.6 (readability after
extraction) and 2.2.7 (proper application of the escape attribute).

## 4. Anchoring

Anchoring links **extension concepts** (entity-specific concepts) back
to the standard taxonomy. Implemented as an **XBRL definition-linkbase
relationship** using the dedicated arcrole
**`http://www.xbrl.org/2018/arcrole/wider-narrower`** (the
`esef:wider-narrower` arc) — the only XBRL relationship developed
specifically for ESEF.

**Rules:**

- **Wider anchoring (Manual 1.4.1).** Every extension in primary statements anchors to the **closest wider** IFRS/ESEF base concept. Example: an extension `Flight equipment` anchors wider to `ifrs-full:PropertyPlantAndEquipment`.
- **Narrower anchoring (RTS Annex IV §9(b)).** Where an extension **combines two or more** core concepts (e.g., `Share capital and share premium`), it must additionally anchor narrower to **each** component base concept. Direction of the arc always runs **from wider to narrower** concept.
- **Subtotals.** A pure subtotal of other lines in the same primary statement is exempt from wider anchoring (Annex IV §10) — but must still participate in the calculation linkbase.
- **Notes / accounting policies.** Manual 1.4.1 explicitly **does not require** anchoring of extensions used only in narrative notes.

Practical: when an extension is genuinely an aggregation, supply both
wider AND narrower anchors. When it is a true specialisation of a
single base concept, supply only the wider anchor. **Never anchor an
extension to an abstract concept** — Arelle raises
`ESEF.3.3.1.ExtensionConceptAnchoredToAbstractConcept`.

## 5. Extension taxonomies

**Naming and URI conventions:**

- **Prefix:** issuer-chosen short prefix unique within the report, typically the issuer's ticker or LEI-derived identifier in lowercase.
- **Namespace URI:** stable, dereferenceable HTTP URI under the issuer's domain (e.g., `https://www.example-issuer.com/xbrl/2025-12-31`). Versioning by reporting date is common.
- **Schema/linkbase filenames:** date-stamped, regex-enforced patterns: `{base}-{date}_cal.xml`, `{base}-{date}_def.xml`, `{base}-{date}_lab-{lang}.xml`, `{base}-{date}_pre.xml`; report basename `{base}-{date}-{version}-{lang}`.
- **Role types:** declared in the schema with unique role URIs and used consistently across presentation, calculation, and definition linkbases. A **single extended link role used for all four primary statements** is rejected (`ESEF.3.4.7.singleExtendedLinkRoleUsedForAllPFSs`).

**Label languages.** Standard labels in the **language of the report**
for every extension. English labels widely recommended (and many NCAs
prefer it). Missing labels raise
`ESEF.3.4.5.missingLabelForRoleInReportLanguage`.

**ESEF Conformance Suite** — maintained by ESMA and reissued most
years. Targeted at software vendors but the de facto reference for what
NCAs (and Arelle) actually check. Each rule has at least one valid and
one invalid test sample. The current edition is the **ESEF Conformance
Suite 2025**, published 21 April 2026, which ESMA describes as 215
packages grouped into 68 tests:
https://www.esma.europa.eu/document/esef-conformance-suite-2025

**ESEF Taxonomy 2025** was published the same day
(https://www.esma.europa.eu/document/esef-taxonomy-2025, package
`esef_taxonomy-2025_12_31.zip`). Its entry points sit under
https://www.esma.europa.eu/taxonomy/2025-03-27/ — a core entry point
(`esef_cor.xsd`) plus two alternative entry points, `esef_ias_1.xsd`
and `esef_ifrs_18.xsd`, allowing an issuer to report under either IAS 1
or IFRS 18. The 2025 package is aimed at 2026 IFRS consolidated
financial statements; the RTS in force for FY2025 reports remains
2019/815 as amended by Delegated Regulation (EU) 2025/19, so entry-point
matching still keys on the financial year. IFRS 18 is effective for
financial years beginning on or after 1 January 2027 with early
application permitted, the availability of the IFRS 18 entry point
imposes no obligation to adopt it earlier, and IFRS 18 and IFRS 19
elements may be used only once those standards are formally endorsed at
EU level. ESMA has stated that it does not plan to amend the ESEF RTS or
taxonomy in 2026, so do not assume a further annual release.

**Common rejection grounds:** invalid LEI in the context entity scheme,
mismatched ESEF entry point, untagged Annex II elements, anchoring
failures, calculation inconsistencies, hidden facts that fail the
`-esef-ix-hidden` discipline, external CSS / JS references.

## 6. Report package

ESMA-mandated submissions are XBRL **Report Packages** built on the
**Taxonomy Packages 1.0 Recommendation** (REC-2016-04-19) extended by
the **Report Packages 1.0** specification.

**ZIP structure (taxonomy-package half):**

- A single top-level directory inside the ZIP (no `__MACOSX`, no `.DS_Store`, no PDFs at root).
- A mandatory `META-INF/` directory containing:
  - `taxonomyPackage.xml` — the manifest, with at minimum a `<tp:identifier>` URI; in practice also name, version, publisher, publisherCountry (ISO 3166-1 alpha-2, e.g., `NL`, not `Netherlands`), and `<tp:entryPoint>` elements pointing at the issuer's extension entry-point schema.
  - `catalog.xml` — optional but standard; remaps public taxonomy URIs to local files inside the package.

**Report-package half (Report Packages 1.0):**

- A `reports/` directory at the top level.
- **Single-file iXBRL:** one `.xhtml` (or `.html`/`.htm`) directly in `reports/`.
- **Multi-file iXBRL document set:** multiple `.xhtml` files inside a single subfolder of `reports/` — the subfolder signals that the files form one logical report.

Arelle's ESEF plugin enforces report-package layout via codes such as
`ESEF.2.6.1.reportIncorrectlyPlacedInPackage`,
`ESEF.2.6.2.reportSetIncorrectlyPlacedInPackage`,
`ESEF.2.6.3.incorrectNamingConventionReportPackageReportFile`,
`ESEF.2.6.3.disallowedReportPackageFileExtension`.

## 7. National competent authority specifics

ESEF is harmonised but each Member State runs its own filing portal
(Officially Appointed Mechanism, "OAM").

- **Netherlands — AFM.** Issuers with NL as home Member State file annual and semi-annual reports through the AFM portal; published in the AFM's register of financial reporting. NL took a one-year deferral, so first ESEF filings covered FY2021 reports submitted in 2022. NL-listed IFRS issuers also work alongside the **NL Taxonomie** maintained by SBR Netherlands — relevant for non-IFRS Dutch GAAP filings via KVK rather than ESEF.
- **Germany — BaFin / Bundesanzeiger.** ESEF reports submitted to **Bundesanzeiger** under the Transparency Directive Implementation Act. The Bundesanzeiger forwards filings to the Unternehmensregister. BaFin enforces the format and may impose fines for non-compliance.
- **France — AMF / ONDE.** French issuers file via AMF's **ONDE** extranet. (There is no AMF portal called "eMagine"; canonical filing channel is ONDE.)
- **Italy — CONSOB.** Filings via CONSOB infrastructure and the Italian Business Register. XBRL Italy publishes preferred national extensions for banks and insurers.
- **Spain — CNMV.** Full AFR in XHTML, with iXBRL tagging of IFRS consolidated primary statements. Spain additionally requires **electronic signatures** of auditors and administrators on the filed report.
- **Belgium — FSMA.** Filings through **eCorporate**; the public store is **STORI**, exposing the AFR as a ZIP report package (XBRL inside) plus optional XHTML/PDF copies. STORI publishes submissions automatically without FSMA pre-review.

## 8. Common ESEF validation errors

Codes verbatim from the Arelle ESEF plugin
(`arelle/plugin/validate/ESEF/`); all but
`ESEF.2.6.3.disallowedReportPackageFileExtension`, which is raised from
the plugin's `__init__.py`, sit in `ESEF_Current/ValidateXbrlFinally.py`:

| Code | What it detects | Manual / RTS link |
|---|---|---|
| `ESEF.2.1.1.nonLEIContextScheme` / `invalidIdentifierFormat` / `invalidIdentifier` | Context `xbrli:identifier/@scheme` is not `http://standards.iso.org/iso/17442` (warning), or the identifier is not a well-formed LEI / fails the ISO 17442 check-digit test (error) | RTS Annex IV §2 / Manual §2.1.1 |
| `ESEF.2.1.3.scenarioContainsNonDimensionalContent` / `segmentUsed` | Use of `xbrli:segment` or non-dimensional `xbrli:scenario` content | Manual §2.1.3 |
| `ESEF.2.2.1.precisionAttributeUsed` | `precision` attribute on numeric facts | Manual §2.2.1 |
| `ESEF.2.2.3.incorrectTransformationRuleApplied` | Wrong ixt transformation or wrong namespace | Manual §2.2.3 |
| `ESEF.2.2.4.inconsistentDuplicateNumericFactInInlineXbrlDocument` | Same fact tagged twice with different numeric values | Manual §2.2.4 |
| `ESEF.2.2.6.escapedHTMLUsedInBlockTagWithSpecialCharacters` / `textContentOrdering` | Block tag content fails readability requirement | Manual §2.2.6 |
| `ESEF.2.4.1.IxHiddenStyleDisallowed` / `factInHiddenSectionNotInReport` / `transformableElementIncludedInHiddenSection` | Misuse of `ix:hidden` | Manual §2.4.1 |
| `ESEF.2.5.2.undefinedLanguageForTextFact` / `taggedTextFactOnlyInLanguagesOtherThanLanguageOfAReport` | Text fact missing `xml:lang` or only in a non-report language | Manual §2.5.2 |
| `ESEF.2.5.4.externalCssFileForSingleIXbrlDocument` / `displayNoneUsedToHideTaggedFacts` | External CSS or `display:none` to hide tagged facts | Manual §2.5.4 |
| `ESEF.2.6.3.incorrectNamingConventionReportPackageReportFile` / `disallowedReportPackageFileExtension` | Report-package filename violation | Manual §2.6.3 |
| `ESEF.3.1.2.incorrectEsefTaxonomyVersionUsed` / `requiredEntryPointNotImported` | Wrong-year ESEF entry point in the DTS | Manual §3.1.2 |
| `ESEF.3.3.1.ExtensionConceptAnchoredToAbstractConcept` | Extension anchored to an abstract base concept | Manual §3.3.1 / Annex IV §9 |
| `ESEF.3.4.5.missingLabelForRoleInReportLanguage` | Extension lacks a standard label in the report language | Manual §3.4.5 |
| `ESEF.3.4.7.singleExtendedLinkRoleUsedForAllPFSs` | A single ELR used to organise all four primary statements | Manual §3.4.7 |

Forward-looking: from the ESEF Taxonomy 2025 onward the DTS may import
either the IAS 1 or the IFRS 18 entry point, so
`requiredEntryPointNotImported` becomes a two-way check once issuers
report under IFRS 18. That is not a current validation trigger.

NCA post-filing review reports (notably AMF) consistently flag
**incorrect signs**, **calculation inconsistencies**, and
**inappropriate extensions** as the highest-frequency substantive
errors.

## Sources

- https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32019R0815
- https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02019R0815-20250101
- https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202500019
- https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52020XC1110(01)
- https://finance.ec.europa.eu/document/download/ce847777-0caa-47e1-8a9a-fcac34943878_en?filename=211109-ceaob-esef-guidelines-auditors_en.pdf
- https://www.esma.europa.eu/sites/default/files/library/esma32-60-254_esef_reporting_manual.pdf
- https://www.esma.europa.eu/document/esef-reporting-manual
- https://www.esma.europa.eu/document/esef-conformance-suite-2025
- https://www.esma.europa.eu/document/esef-taxonomy-2025
- https://www.esma.europa.eu/issuer-disclosure/electronic-reporting
- https://github.com/Arelle/Arelle/tree/master/arelle/plugin/validate/ESEF
- https://www.xbrl.org/Specification/taxonomy-package/REC-2016-04-19/taxonomy-package-REC-2016-04-19.html
- https://www.xbrl.org/guidance/esef-rules-anchoring-extensions/
- https://www.xbrl.org/guidance/esef-rules-anchoring-extensions-examples/
- https://www.afm.nl/en/sector/effectenuitgevende-ondernemingen/financiele-en-duurzaamheidsverslaggeving/jaarlijkse-verslaggeving-in-esef
- https://www.fsma.be/sites/default/files/media/files/2021-12/fsma_2021_19_en.pdf
- https://www.fsma.be/en/stori-belgian-official-mechanism-storage-regulated-information
- https://www.amf-france.org/en/professionals/management-companies/my-relations-amf/submit-annual-reports-amf
