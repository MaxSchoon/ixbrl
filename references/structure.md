# XBRL Structural Model — DTS, XLink, Linkbases, OIM

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
  `xlink:role` URI that names the *Extended Link Role* (ELR) — a
  partition of the graph into per-statement views.

Read any XBRL question through "which graph, which arcrole, which ELR?" — confusion usually dissolves.

**Nesting rules** in an instance flow from this model:

- A `link:presentationLink` (extended link) contains zero-or-more `link:loc` elements (locators), zero-or-more `link:label` / `link:reference` / `link:footnote` resources, and zero-or-more `link:*Arc` arcs that connect locators to other locators or resources by `xlink:label`.
- Inside an instance: `xbrli:context > xbrli:entity > xbrli:identifier`; `xbrli:context > xbrli:period > (xbrli:instant | xbrli:startDate + xbrli:endDate | xbrli:forever)`; `xbrli:context > xbrli:scenario > (xbrldi:explicitMember | xbrldi:typedMember)*` (in ESEF, scenario only).
- Inside a hypercube graph (definition linkbase): primary item → `all`/`notAll` → hypercube → `hypercube-dimension` → dimension → `dimension-domain` → domain → `domain-member` → member (recursive). See `references/dimensions.md`.
- Tuples nest concept declarations: a tuple's `complexType` contains the child item declarations directly; instance documents nest the child elements inside the tuple parent.

## DTS — Discoverable Taxonomy Set

A **Discoverable Taxonomy Set (DTS)** is the closure of taxonomy
schemas and linkbases reachable from a starting point via a fixed set
of discovery pointers. XBRL 2.1 §3.1 lists them: `xs:include`,
`xs:import`, `link:linkbaseRef`, `link:roleRef`, `link:arcroleRef`,
`link:schemaRef` in an instance, plus the `xlink:href` of every
locator. The DTS is the transitive closure.

Every fact references a concept by QName, and that concept must be declared by a schema in the DTS. A missing `link:schemaRef`, `link:linkbaseRef`, or `xs:import` produces an unresolved concept and the instance fails Arelle / XBRL Formula validation. When a fact appears as `xbrl.5.1.5` "concept not found" or "schema not in DTS", the first question is: "is the taxonomy in the DTS?"

## XLink primitives in XBRL

XBRL linkbases are XLink 1.1 documents. XBRL 2.1 §3.5 specialises
XLink for taxonomies. The relevant XLink element types
(`xlink:type` attribute values) used in XBRL:

- `simple` — used on `link:schemaRef`, `link:linkbaseRef`, `link:roleRef`, `link:arcroleRef` (one-shot pointers).
- `extended` — used on the linkbase containers: `link:presentationLink`, `link:calculationLink`, `link:definitionLink`, `link:labelLink`, `link:referenceLink`, `link:footnoteLink` (XBRL 2.1 §3.5.3).
- `locator` — used on `link:loc` to point at a concept in a schema via `xlink:href`.
- `resource` — used on `link:label`, `link:reference`, `link:footnote`.
- `arc` — used on `link:presentationArc`, `link:calculationArc`, `link:definitionArc`, `link:labelArc`, `link:referenceArc`, `link:footnoteArc`.

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
`dimension-default`, `all`, `notAll`) on definition arcs — see
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

XBRL 2.1 §4.9 defines tuples — elements in the `xbrli:tuple`
substitution group that group a set of related child items into a
single compound fact. The spec defines duplicate tuples in §4.10.
Tuples were the original mechanism for repeated structures (subsidiary
listings, share-class breakdowns) and predate XBRL Dimensions.

Modern reporting taxonomies prefer dimensions. ESEF rule
**`ESEF.2.4.1.tupleElementUsed`** flags any use of a tuple as an error.
SEC EDGAR EFM similarly discourages tuples.

## Footnotes — XBRL model vs iXBRL `ix:footnote`

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
connecting facts to footnotes — listed as one of the three substantive
new features in iXBRL 1.1.

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
reporting. EBA's DPM 2.0 framework adopts xBRL-CSV; reports
referencing periods on or after **31 March 2026** must be filed in
xBRL-CSV under the EBA reporting framework migration.

For an iXBRL skill, OIM matters because:

- Inline XBRL is one of the "input syntaxes" the OIM normalises into the same fact set.
- xBRL-JSON is what Arelle and modern viewers emit when downstream tools want a structured fact list.
- Calc 1.1 leverages OIM rounding semantics rather than XBRL 2.1 fact-level decimals.

## Versioning

XBRL Versioning 1.0 is a separate XBRL International specification.
Indexed at
https://specifications.xbrl.org/work-product-index-versioning-versioning-1.0.html.
The versioning report communicates concept renames, deprecations,
namespace migrations, and other taxonomy diffs between two taxonomy
versions. Adoption is uneven — IFRS Foundation publishes versioning
reports for their taxonomy releases; SEC EDGAR and ESEF do not require
filers to consume them.

## Nil values and per-regulator policy

`xsi:nil="true"` is an XML Schema construct. In XBRL it asserts that
a concept is reported but has no value — the element appears in the
instance with no content. The `xsi:nil` attribute itself is W3C XML
Schema; XBRL 2.1 does not redefine it.

Per-regulator policy (validate against the current Reporting Manual /
Filer Manual at filing time, since policy here is precise and changes
by manual revision):

- **SBR (Dutch)** — forbids `xsi:nil="true"` on facts (rule `FR-NL-5.07`).
- **ESEF** — permits `xsi:nil` for empty cells in tagged tables under conditions in the ESEF Reporting Manual §2.2.5.
- **SEC EDGAR** — discourages `xsi:nil` and EFM rejects nil values on most tagged facts.

## `link:schemaRef` / `linkbaseRef` / `roleRef` / `arcroleRef` in instances

XBRL 2.1 §4.2, §4.3, §3.5.2.4, §3.5.2.5 govern these four
instance-side pointers:

- **`link:schemaRef`** — required, simple link, points at a taxonomy schema. The `xlink:href` is the entry-point schema URL. `xlink:type` MUST be `simple`. There must be at least one in any XBRL instance.
- **`link:linkbaseRef`** — optional simple link pointing at a linkbase that should be added to the DTS for this instance only. The standard `xlink:role` values include:
  - `http://www.xbrl.org/2003/role/presentationLinkbaseRef`
  - `http://www.xbrl.org/2003/role/calculationLinkbaseRef`
  - `http://www.xbrl.org/2003/role/definitionLinkbaseRef`
  - `http://www.xbrl.org/2003/role/labelLinkbaseRef`
  - `http://www.xbrl.org/2003/role/referenceLinkbaseRef`
- **`link:roleRef`** — declares any custom `xlink:role` URIs used by the instance's footnote links. Points at the `link:roleType` declaration in a schema.
- **`link:arcroleRef`** — same role for custom arcroles used in the instance's footnote arcs.

In an Inline XBRL document, these four elements live inside
`ix:references` in the host XHTML's `<head>` and behave identically to
the equivalents in a standalone xBRL-XML instance.

## Sources

- https://www.xbrl.org/Specification/XBRL-2.1/REC-2003-12-31/XBRL-2.1-REC-2003-12-31+corrected-errata-2013-02-20.html (DTS §3.1, XLink usage §3.5, linkbase definitions §5.2, role/arcrole types §5.1.3 / §5.1.4, tuples §4.9, footnotes §4.11, instance refs §4.2 / §4.3)
- https://www.w3.org/TR/xlink11/ (XLink 1.1 — `xlink:type`, `xlink:href`, `xlink:label`, `xlink:from`, `xlink:to`, `xlink:role`, `xlink:arcrole`, `xlink:show`, `xlink:actuate`)
- https://specifications.xbrl.org/work-product-index-inline-xbrl-inline-xbrl-1.1.html (Inline XBRL 1.1 work-product index)
- https://www.xbrl.org/Specification/inlineXBRL-part1/REC-2013-11-18/inlineXBRL-part1-REC-2013-11-18.html (`ix:footnote`, `ix:relationship`)
- https://specifications.xbrl.org/work-product-index-open-information-model-open-information-model-1.0.html (OIM 1.0 work-product index)
- https://specifications.xbrl.org/work-product-index-versioning-versioning-1.0.html (Versioning 1.0 work-product index)

> Items not freshly fetched in this run, mentioned because they are
> part of the asked-for scope; re-verify against the current regulator
> manual before relying on them: ESEF rule
> `ESEF.2.4.1.tupleElementUsed`; SBR rules `FR-NL-5.07` and
> `FR-NL-6.01`; ESEF Reporting Manual §2.2.5 nil-value policy; EBA
> xBRL-CSV cutover date; LRR negated-label roles. The `ESEF.*` codes
> are also separately verified in `references/validation.md` against
> the Arelle source.
