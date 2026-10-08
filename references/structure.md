# XBRL Structural Model: DTS, XLink, Linkbases, OIM

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*

**Load this when:** the question is how a taxonomy is wired: XLink locators, arcs and resources, what each of the five standard linkbases does, role and arcrole types, tuples, the footnote model, the OIM serialisations, the Project Tavi draft (formerly OIM Taxonomy), nil policy, or the pointers an instance may carry.

**Do not load this when:** you need the discovery closure itself, offline resolution, or which release was operative for a period (`references/dts.md`), or you are designing dimensional structure (`references/dimensions.md`).

## Contents

- [Mental model: linkbases are directed graphs](#mental-model-linkbases-are-directed-graphs)
- [DTS: Discoverable Taxonomy Set](#dts-discoverable-taxonomy-set)
- [XLink primitives in XBRL](#xlink-primitives-in-xbrl)
- [The five standard linkbases](#the-five-standard-linkbases)
- [Role types and arcrole types](#role-types-and-arcrole-types)
- [Tuples (legacy)](#tuples-legacy)
- [Footnotes: XBRL model vs iXBRL `ix:footnote`](#footnotes-xbrl-model-vs-ixbrl-ixfootnote)
- [Open Information Model (OIM)](#open-information-model-oim)
- [Project Tavi: the next-generation model (draft)](#project-tavi-the-next-generation-model-draft)
- [Versioning](#versioning)
- [Nil values and per-regulator policy](#nil-values-and-per-regulator-policy)
- [`link:schemaRef` / `linkbaseRef` / `roleRef` / `arcroleRef` in instances](#linkschemaref--linkbaseref--roleref--arcroleref-in-instances)
- [Sources](#sources)

## Mental model: linkbases are directed graphs

Every XBRL linkbase is a **directed graph**.

- **Nodes** are XLink **locators** (`link:loc`) pointing at concepts in
  schemas, plus XLink **resources** (`link:label`, `link:reference`,
  `link:footnote`) carrying inline content.
- **Edges** are XLink **arcs** (`link:presentationArc`,
  `link:calculationArc`, `link:definitionArc`, `link:labelArc`,
  `link:referenceArc`, `link:footnoteArc`), each labelled with an
  `xlink:arcrole` URI that names the relationship type.
- **Containers** are XLink **extended links** (`link:presentationLink`,
  `link:calculationLink`, `link:definitionLink`, `link:labelLink`,
  `link:referenceLink`, `link:footnoteLink`), each carrying an
  `xlink:role` URI that names the *Extended Link Role* (ELR), a
  partition of the graph into per-statement views.

Read any XBRL question through "which graph, which arcrole, which ELR?" Confusion usually dissolves.

**Nesting rules** in an instance flow from this model:

- A `link:presentationLink` (extended link) contains zero-or-more `link:loc` elements (locators), zero-or-more `link:label` / `link:reference` / `link:footnote` resources, and zero-or-more `link:*Arc` arcs that connect locators to other locators or resources by `xlink:label`.
- Inside an instance: `xbrli:context > xbrli:entity > xbrli:identifier`; `xbrli:context > xbrli:period > (xbrli:instant | xbrli:startDate + xbrli:endDate | xbrli:forever)`; `xbrli:context > xbrli:scenario > (xbrldi:explicitMember | xbrldi:typedMember)*` (in ESEF, scenario only).
- Inside a hypercube graph (definition linkbase): primary item → `all`/`notAll` → hypercube → `hypercube-dimension` → dimension → `dimension-domain` → domain → `domain-member` → member (recursive). See `references/dimensions.md`.
- Tuples nest concept declarations: a tuple's `complexType` contains the child item declarations directly; instance documents nest the child elements inside the tuple parent.

## DTS: Discoverable Taxonomy Set

A **Discoverable Taxonomy Set (DTS)** is the closure of taxonomy
schemas and linkbases reachable from a starting point via a fixed set
of discovery pointers (definition: XBRL 2.1 §1.4; rules: §3.2):
`xs:include`, `xs:import`, `link:linkbaseRef` (in an instance or in a
schema's `appinfo`), `link:roleRef`, `link:arcroleRef`,
`link:schemaRef` in an instance, the `xlink:href` of every locator, and
linkbases embedded in a schema's `appinfo`. The instance is a starting
point but not a member; the DTS is the transitive closure.

Every fact references a concept by QName, and that concept must be declared by a schema in the DTS. A missing `link:schemaRef`, `link:linkbaseRef`, or `xs:import` produces an unresolved concept and the instance fails Arelle / XBRL Formula validation. When a fact appears as `xbrl.5.1.5` "concept not found" or "schema not in DTS", the first question is: "is the taxonomy in the DTS?"

The full treatment, including entry points, packages and catalogs, how
a fact resolves to its concept, label and statement, a measured
comparison of six regulator DTSs, the bi-temporal model, and
`scripts/dts_profile.py` to walk a DTS yourself, is
`references/dts.md`.

## XLink primitives in XBRL

XBRL linkbases are XLink 1.1 documents. XBRL 2.1 §3.5 specialises
XLink for taxonomies. The relevant XLink element types
(`xlink:type` attribute values) used in XBRL:

- `simple` is used on `link:schemaRef`, `link:linkbaseRef`, `link:roleRef`, `link:arcroleRef` (one-shot pointers).
- `extended` is used on the linkbase containers: `link:presentationLink`, `link:calculationLink`, `link:definitionLink`, `link:labelLink`, `link:referenceLink`, `link:footnoteLink` (XBRL 2.1 §3.5.3).
- `locator` is used on `link:loc` to point at a concept in a schema via `xlink:href`.
- `resource` is used on `link:label`, `link:reference`, `link:footnote`.
- `arc` is used on `link:presentationArc`, `link:calculationArc`, `link:definitionArc`, `link:labelArc`, `link:referenceArc`, `link:footnoteArc`.

The XLink attributes XBRL relies on are `xlink:href`, `xlink:label`,
`xlink:from`, `xlink:to`, `xlink:role`, `xlink:arcrole`, `xlink:show`,
`xlink:actuate` (W3C XLink 1.1).

## The five standard linkbases

XBRL 2.1 defines five standard linkbase types plus a footnote linkbase
that lives inside instances.

### Label linkbase

Container: `link:labelLink` (extended). Resources: `link:label` (with
`xml:lang`). Arc: `link:labelArc` carrying arcrole
`http://www.xbrl.org/2003/arcrole/concept-label`.

Standard label-role URIs (from XBRL 2.1 §5.2.2.2.2):

- `http://www.xbrl.org/2003/role/label` (default)
- `http://www.xbrl.org/2003/role/terseLabel`
- `http://www.xbrl.org/2003/role/verboseLabel`
- `http://www.xbrl.org/2003/role/totalLabel`
- `http://www.xbrl.org/2003/role/periodStartLabel`
- `http://www.xbrl.org/2003/role/periodEndLabel`
- `http://www.xbrl.org/2003/role/documentation`

> The `negatedLabel` / `negatedTerseLabel` / `negatedPeriodStartLabel`
> / `negatedPeriodEndLabel` / `negatedTotalLabel` roles originate from
> the **Label Role Registry (LRR)**, an XBRL International registry,
> not from XBRL 2.1 itself. They are widely supported and used in
> ESEF / IFRS / US-GAAP.

### Presentation linkbase

Container: `link:presentationLink`. Arc: `link:presentationArc`.
Arcrole: `http://www.xbrl.org/2003/arcrole/parent-child`. The optional
`@preferredLabel` attribute on the presentation arc selects which
label role is rendered for the child concept (XBRL 2.1 §5.2.4.2.1).

### Calculation linkbase

Container: `link:calculationLink`. Arc: `link:calculationArc`. Arcrole:
`http://www.xbrl.org/2003/arcrole/summation-item`. Each arc carries a
`@weight` attribute (`1.0`, `-1.0`, etc.). Calc 1.0 is fact-level;
XBRL Calc 1.1 (a separate spec) reframes inconsistencies through OIM
rounding (see `references/validation.md` §4).

### Definition linkbase

Container: `link:definitionLink`. Arc: `link:definitionArc`. The
standard definition arcroles enumerated in XBRL 2.1 §5.2.6.2:

- `http://www.xbrl.org/2003/arcrole/general-special`
- `http://www.xbrl.org/2003/arcrole/essence-alias`
- `http://www.xbrl.org/2003/arcrole/similar-tuples` (§5.2.6.2.3)
- `http://www.xbrl.org/2003/arcrole/requires-element`

XBRL Dimensions (XDT) adds further arcroles
(`hypercube-dimension`, `dimension-domain`, `domain-member`,
`dimension-default`, `all`, `notAll`) on definition arcs. See
`references/dimensions.md`.

### Reference linkbase

Container: `link:referenceLink`. Resource: `link:reference`. Arc:
`link:referenceArc`. Arcrole:
`http://www.xbrl.org/2003/arcrole/concept-reference`. The
`link:reference` resource carries part elements such as `ref:Name`,
`ref:Number`, `ref:Paragraph`, `ref:Section`, `ref:Pages` (namespace
`http://www.xbrl.org/2003/ref`). Reference linkbases anchor each
concept to the authoritative source (e.g., paragraph of an accounting
standard).

## Role types and arcrole types

XBRL 2.1 §5.1.3 defines `link:roleType` (custom Extended Link Roles,
ELRs) and §5.1.4 defines `link:arcroleType` (custom arcroles). Both
declarations live in a schema and contain `link:usedOn` children
listing the elements where the role/arcrole may appear (e.g.,
`link:presentationArc`, `link:calculationArc`).

The `@cyclesAllowed` attribute is **required** on `link:arcroleType`
and its enumeration is exactly `any | undirected | none`.
`link:roleRef` and `link:arcroleRef` propagate these declarations into
linkbases and instances that consume them.

Issuers create custom ELRs to carve presentation/calculation/definition networks into per-statement views (Balance Sheet ELR, Income Statement ELR, Note 14 ELR). Every regulator (ESEF, EDGAR, SBR, KvK) uses this mechanism to keep statement networks isolated and auditable.

## Tuples (legacy)

XBRL 2.1 §4.9 defines tuples: elements in the `xbrli:tuple`
substitution group that group a set of related child items into a
single compound fact. The spec defines duplicate tuples in §4.10.
Tuples were the original mechanism for repeated structures (subsidiary
listings, share-class breakdowns) and predate XBRL Dimensions.

Modern reporting taxonomies prefer dimensions. ESEF rule
**`ESEF.2.4.1.tupleElementUsed`** flags any use of a tuple as an error.
SEC EDGAR EFM similarly discourages tuples.

## Footnotes: XBRL model vs iXBRL `ix:footnote`

XBRL 2.1 §4.11 defines the footnote model. Footnotes live inside an
instance, in a `link:footnoteLink` extended link with
`xlink:role="http://www.xbrl.org/2003/role/link"`. The footnote text
is a `link:footnote` resource with `xml:lang` and
`xlink:role="http://www.xbrl.org/2003/role/footnote"`. The connecting
arc is `link:footnoteArc` with arcrole
`http://www.xbrl.org/2003/arcrole/fact-footnote`.

```xml
<link:footnoteArc xlink:type="arc"
                  xlink:from="fact1"
                  xlink:to="footnote1"
                  xlink:arcrole="http://www.xbrl.org/2003/arcrole/fact-footnote"/>
```

Inline XBRL 1.1 introduces inline analogues: `ix:footnote` for the
footnote text inside the host XHTML, and `ix:relationship` for
connecting facts to footnotes (listed as one of the three substantive
new features in iXBRL 1.1).

> Per-regulator: SBR forbids footnotes entirely (rule `FR-NL-6.01`).

## Open Information Model (OIM)

The XBRL Open Information Model is the syntax-neutral data model for
XBRL: facts, dimensions, contexts, units expressed without commitment
to XML, JSON, or CSV serialization. Indexed at
https://specifications.xbrl.org/work-product-index-open-information-model-open-information-model-1.0.html.
The OIM is the foundation that the three serializations below all
conform to.

### xBRL-XML

The original XBRL 2.1 instance syntax. Inline XBRL is, semantically,
a transformation of XHTML into the same xBRL-XML model.

### xBRL-JSON

A JSON serialization of the OIM. Indexed under the OIM 1.0 family.
Modern viewers and downstream tools commonly consume xBRL-JSON when
they want a structured fact list rather than parsing XHTML.

### xBRL-CSV

A CSV serialization of the OIM, designed for high-volume regulatory
reporting. EBA's DPM 2.0 framework adopts xBRL-CSV; reports with a
reference date on or after **31 March 2026** must be submitted and
resubmitted in xBRL-CSV. MiCA, Pillar 3 and Instant Payments reports
are xBRL-CSV regardless of reference date, and DORA is plain CSV.

For an iXBRL skill, OIM matters because:

- Inline XBRL is one of the "input syntaxes" the OIM normalises into the same fact set.
- xBRL-JSON is what Arelle and modern viewers emit when downstream tools want a structured fact list.
- Calc 1.1 leverages OIM rounding semantics rather than XBRL 2.1 fact-level decimals.

## Project Tavi: the next-generation model (draft)

Project Tavi 1.0 is XBRL International's draft of the next generation
of the XBRL standard: one syntax-independent model for taxonomies
*and* reports, serialised for now in JSON. It was called "OIM
Taxonomy" until the September 2026 draft; "Project Tavi" is itself a
working title that XBRL International will replace with a formal name,
so search the work-product index in Sources under either name.

**Status, and what it changes for a filing today: nothing.** The only
edition is the Public Working Draft of 1 September 2026. It says it
is "not recommended for use in production systems, and may change
significantly prior to finalisation"; XBRL International advises
vendors not to invest development resources in a new specification
before Candidate Recommendation, which Tavi has not reached. No
regulator accepts or requires it. So:

- Review, validate and fix every iXBRL or xBRL-XML filing against
  XBRL 2.1, Dimensions 1.0, Inline XBRL 1.1 and the regime's manual;
  departing from a Tavi rule is not a defect in a filing.
- Cite Tavi by edition (`PWD-2026-09-01`) and section, and say it is a
  draft. Before relying on anything here, open the work-product index
  in Sources: a later draft or the new name supersedes this section.
- Every Tavi namespace and error code carries the draft date
  (`xbrl` = `https://xbrl.org/PWD/2026-09-01`, errors under
  `oimte` = `https://xbrl.org/PWD/2026-09-01/oimtaxonomy/error`). Code
  that hard-wires them breaks at the next draft; key them on the
  edition. `oimte:*` codes are Tavi-draft codes, not the
  `oime:` / `oimce:` codes of the OIM 1.0 and OIM Common specifications, which
  Tavi reuses for JSON syntax and prefix errors.
- Tool support is experimental and may track a different edition.
  Arelle's `OimTaxonomy` plugin (checked 2026-10-08) binds the
  pre-draft `https://xbrl.org/2025` namespace and an `abstractObject`
  that the PWD renamed `headingObject`, so its output is not evidence
  of what the PWD requires.

**How familiar XBRL 2.1 constructs map onto the PWD model**, for
reading the draft or the published demos (all section numbers are
PWD-2026-09-01's):

| XBRL 2.1 / Dimensions / iXBRL | Tavi PWD object | Change worth knowing |
|---|---|---|
| Taxonomy schema + linkbases + instance | one `xbrlModel` per JSON document, with `documentInfo` (§ 4–5) | a *module* defines objects in one namespace and imports others; a *compiled model* is the resolved, single-file form |
| `xs:element` item with `abstract="true"` | `headingObject` (§ 5.3) | headings are not concepts; one used as a fact's dimension member is an error |
| Item concept | `conceptObject` (§ 5.4) | `periodType` gains `none` (no period dimension allowed); datatypes such as `xbrlr:monetary` derive from XML Schema types, not from the 2003 item types (§ 11.1.2, § 14.2) |
| `balance` attribute | `xbrla:balance` property (§ 15.3.1) | a property from the built-in accounting model, not core |
| Extended link role | `groupObject` + `groupContentObject` (§ 10.1–10.2) | `groupURI` keeps the old role URI for backward compatibility |
| Arcs in an extended link | `networkObject` of `relationshipObject`s (§ 10.3–10.4) | arcroles become relationship types; `xbrl:parent-child` keeps its 2003 arcrole URI |
| Presentation `preferredLabel` | `xbrl:preferredLabel` property (§ 14.3.3) | may sit on the whole network as well as on one relationship |
| Calculation `summation-item` | `xbrl:summation-item` (§ 14.1.2) | still a placeholder: planned weights of +1 or −1 only, a `reconciliation` property, and calculations bound to cubes to stop bleed-through |
| Hypercube (`all` / `notAll`) | `cubeObject` with a `cubeType` (§ 5.9, § 14.5) | a cube names its core dimensions too (concept, period, entity, unit, language); exclusion is a negative cube |
| Label and reference roles | `labelType` / `referenceType` QNames (§ 14.6–14.7) | the 2003 and Link Role Registry roles stay available by QName; labels can ship as a separate label bundle |
| Context + unit + fact | `factObject` with `factDimensions` (§ 8.3) | no contexts: period, entity and unit are dimensions of the fact |
| `ix:nonFraction` / `ix:nonNumeric` in XHTML | `xbrl:inline-XBRL-1.1` fact map (§ 9.3, § 16.3) | processors MUST support the xBRL-XML and xBRL-JSON fact maps but only MAY support the Inline XBRL one, and § 16.3 is four short paragraphs; the HTML element id becomes a fact value source (§ 8.7, locator `xbrl:htmlElementId`) |

For a generator or converter, the practical consequence is the
Inline XBRL row: an iXBRL pipeline keeps producing Inline XBRL 1.1,
and Tavi consumes it through a fact map. Pin the draft before writing
code that emits Tavi JSON; gaps go to XBRL International through the
comment channel the work-product index names for the open draft.

## Versioning

XBRL Versioning 1.0 is a separate XBRL International specification.
Indexed at
https://specifications.xbrl.org/work-product-index-versioning-versioning-1.0.html.
The versioning report communicates concept renames, deprecations,
namespace migrations, and other taxonomy diffs between two taxonomy
versions. Adoption is uneven: IFRS Foundation publishes versioning
reports for their taxonomy releases; SEC EDGAR and ESEF do not require
filers to consume them.

## Nil values and per-regulator policy

`xsi:nil="true"` is an XML Schema construct. In XBRL it asserts that
a concept is reported but has no value; the element appears in the
instance with no content. The `xsi:nil` attribute itself is W3C XML
Schema; XBRL 2.1 does not redefine it.

Per-regulator policy (validate against the current Reporting Manual /
Filer Manual at filing time, since policy here is precise and changes
by manual revision):

- **SBR (Dutch)** forbids `xsi:nil="true"` on facts (rule `FR-NL-5.07`).
- **ESEF** permits `xsi:nil` for empty cells in tagged tables under conditions in the ESEF Reporting Manual §2.2.5.
- **SEC EDGAR** discourages `xsi:nil` and EFM rejects nil values on most tagged facts.

## `link:schemaRef` / `linkbaseRef` / `roleRef` / `arcroleRef` in instances

XBRL 2.1 §4.2, §4.3, §3.5.2.4, §3.5.2.5 govern these four
instance-side pointers:

- **`link:schemaRef`**: required, simple link, points at a taxonomy schema. The `xlink:href` is the entry-point schema URL. `xlink:type` MUST be `simple`. There must be at least one in any XBRL instance.
- **`link:linkbaseRef`**: optional simple link pointing at a linkbase that should be added to the DTS for this instance only. The standard `xlink:role` values include:
  - `http://www.xbrl.org/2003/role/presentationLinkbaseRef`
  - `http://www.xbrl.org/2003/role/calculationLinkbaseRef`
  - `http://www.xbrl.org/2003/role/definitionLinkbaseRef`
  - `http://www.xbrl.org/2003/role/labelLinkbaseRef`
  - `http://www.xbrl.org/2003/role/referenceLinkbaseRef`
- **`link:roleRef`**: declares any custom `xlink:role` URIs used by the instance's footnote links. Points at the `link:roleType` declaration in a schema.
- **`link:arcroleRef`**: declares any custom `xlink:arcrole` URIs used by the instance's footnote arcs. Points at the `link:arcroleType` declaration in a schema.

In an Inline XBRL document, these four elements live inside
`ix:references` in the host XHTML's `<head>` and behave identically to
the equivalents in a standalone xBRL-XML instance.

## Sources

- https://www.xbrl.org/Specification/XBRL-2.1/REC-2003-12-31/XBRL-2.1-REC-2003-12-31+corrected-errata-2013-02-20.html (DTS §3.1, XLink usage §3.5, linkbase definitions §5.2, role/arcrole types §5.1.3 / §5.1.4, tuples §4.9, footnotes §4.11, instance refs §4.2 / §4.3)
- https://www.w3.org/TR/xlink11/ (XLink 1.1: `xlink:type`, `xlink:href`, `xlink:label`, `xlink:from`, `xlink:to`, `xlink:role`, `xlink:arcrole`, `xlink:show`, `xlink:actuate`)
- https://specifications.xbrl.org/work-product-index-inline-xbrl-inline-xbrl-1.1.html (Inline XBRL 1.1 work-product index)
- https://www.xbrl.org/Specification/inlineXBRL-part1/REC-2013-11-18/inlineXBRL-part1-REC-2013-11-18.html (`ix:footnote`, `ix:relationship`)
- https://specifications.xbrl.org/work-product-index-open-information-model-open-information-model-1.0.html (OIM 1.0 work-product index)
- https://specifications.xbrl.org/work-product-index-versioning-versioning-1.0.html (Versioning 1.0 work-product index)
- https://www.xbrl.org/Specification/tavi/PWD-2026-09-01/tavi-PWD-2026-09-01.html (Project Tavi 1.0, Public Working Draft 1 September 2026, read 2026-10-08: status §1, namespaces §2.4, documentInfo §4, heading and concept §5.3–5.4, cube §5.9, fact §8.3, fact value source §8.7, fact maps §9.3 and §16, groups and networks §10, summation-item placeholder §14.1.2, cube types §14.5, balance §15.3.1)
- https://specifications.xbrl.org/work-product-index-open-information-model-tavi.html (Project Tavi work-product index: current edition, OIM Taxonomy Requirements 2025-12-17, demos)
- https://www.xbrl.org/next-generation-xbrl-the-first-public-working-draft/ (XBRL International, 2 September 2026: temporary name, no vendor investment before Candidate Recommendation)
- https://xbrl.us/events/xii-tavi-260902/ (comment period 2 September – 16 October 2026; Data Amplified 26–27 October)
- https://github.com/Arelle/Arelle/tree/master/arelle/plugin/OimTaxonomy (experimental plugin; `XbrlConst.py` binds `https://xbrl.org/2025`, read 2026-10-08)

> Items not freshly fetched in this run, mentioned because they are
> part of the asked-for scope; re-verify against the current regulator
> manual before relying on them: ESEF rule
> `ESEF.2.4.1.tupleElementUsed`; SBR rules `FR-NL-5.07` and
> `FR-NL-6.01`; ESEF Reporting Manual §2.2.5 nil-value policy; LRR
> negated-label roles. The `ESEF.*` codes are also separately verified
> in `references/validation.md` against the Arelle source.
