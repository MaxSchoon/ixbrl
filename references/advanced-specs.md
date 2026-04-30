# Advanced XBRL Specs — Generic Links, Functions Registry, Versioning

Every namespace URI, element name, and arcrole below was verified against the specifications listed under **Sources**.

## Generic Links 1.0

### What it extends

XBRL 2.1 defines five "standard" linkbases — presentation, calculation, definition, label, reference — built on W3C XLink, each with predetermined semantics (e.g., `link:calculationArc` must connect two `xbrli:item` concepts per XBRL 2.1 §5).

**Generic Links 1.0** (XBRL International Recommendation, 22 June 2009) "generalises this by providing a link type with no predefined semantics or constraints." Per §1: *"one quickly finds oneself wishing to use the power of XLink to associate information with, and express relationships between XML elements that are not XBRL concepts."*

Generic Links lets a spec author build new relationships — between facts, resources, or arbitrary XML elements anywhere in the DTS — without inventing a new XLink language each time. It is the plumbing layer for nearly every post-2008 XBRL specification.

### gen:* elements and arcs

The Generic Links specification defines two concrete elements:

- `<gen:link>` — an XBRL extended link in the substitution group of `xl:extended` capable of carrying arbitrary children.
- `<gen:arc>` — an arc in the substitution group of `xl:arc` that establishes a relationship between resources or locators inside a `<gen:link>`.

Verified `gen` namespace URI: **`http://xbrl.org/2008/generic`**
(Table 1 of the Recommendation; this column is normative). The
companion error namespace is `http://xbrl.org/2008/generic/error`
(prefix `xbrlgene`), which carries codes such as
`xbrlgene:nonAbsoluteArcRoleURI`,
`xbrlgene:missingRoleRefForLinkRole`, and
`xbrlgene:violatedCyclesConstraint`.

> Generic Links 1.0 itself does **not** define a `gen:reference`
> element — it only defines the link and the arc.
> References-as-resources are the job of the companion specification
> below.

### Generic Labels and Generic References

Generic Links sits at the centre of a three-spec cluster on
specifications.xbrl.org under "Generic Links":

- **Generic Labels 1.0** — Recommendation, 24 October 2011. Lets you attach a label resource to *any* XML element, not just an XBRL concept. Verified namespace: **`http://xbrl.org/2008/label`**.
- **Generic References 1.0** — Recommendation, also 24 October 2011 (sibling of Generic Labels). Same idea for references to authoritative literature.

Both depend on Generic Links 1.0 as their substrate.

A common point of confusion for new implementers: regulator-issued
taxonomies often refer to "generic labels" without specifying that
this is a separate XBRL spec. If you see `link:linkbase` declaring a
`gen:link` with `roleType` `http://www.xbrl.org/2008/role/link` and
`label` resources in the `http://xbrl.org/2008/label` namespace, that
is the Generic Labels 1.0 mechanism — not standard `link:label`.

### Use cases (Formula, Table Linkbase, Versioning)

Generic Links is the substrate for almost every modern XBRL extension
that needs custom relationships:

- **Formula 1.0** — variable sets, filters, and assertions are wired together with generic arcs.
- **Table Linkbase 1.0** — table, breakdown, and definition node hierarchies are entirely generic-link-based; the table linkbase has no native XLink syntax of its own.
- **Versioning 1.0** — concept-correspondence and label/reference event identifiers ride on top of Generic Links.
- **Generic Preferred Label 1.0** — listed as a separate spec group on specifications.xbrl.org and built on Generic Links.
- Regulator-specific linkbases — ESEF anchoring relationships, EDGAR custom relationships, and EBA filing rules all extend the same `gen:link` / `gen:arc` substrate.

The dependency chain is explicit in the Versioning Base 1.0
Recommendation §1.1: *"This specification depends upon … Generic Link
Specification, Generic Label Specification, Generic Reference
Specification."*

## XBRL Functions Registry

### Purpose

The Functions Registry is a curated catalogue of XPath 2.0 functions
with XBRL-specific semantics — operating on facts, contexts, units,
periods, dimensions, and concept properties. It exists because XBRL
Formula and Table Linkbase need to ask questions XPath cannot natively
answer ("what is the period type of this fact?", "what is the value
of dimension D on fact F?"). The registry index page is
https://specifications.xbrl.org/registries/functions-registry-1.0/index.html,
last updated 2024-02-20 according to the page header.

The registry currently contains roughly **158 entries** — 121 with
status `REC` (Recommendation) and 37 with status `CR` (Candidate
Recommendation, primarily the newer `f:` and `r:` Open-Information-
Model functions added 2023-05-25).

The Function Definition Recommendation (24 October 2011) governs the
metadata format used by every entry; the Function Conformance
Recommendation (22 June 2009) governs how implementations are tested.

### Function categories with verified examples

Three function namespaces are present in the registry:

- `xfi` — XBRL Functions for Instances. Verified namespace URI: **`http://www.xbrl.org/2008/function/instance`**.
- `xff` — XBRL Formula Functions (a smaller library, e.g., uncovered-aspect helpers).
- `xfm` — XBRL math functions added 29 October 2018 (REC).
- `f:` and `r:` — newer OIM-era functions in Candidate Recommendation status.

Function categories with verified QNames and signatures (each lifted
directly from the registry table):

**Context — period/entity/unit:**

- `xfi:context($item as schema-element(xbrli:item)) returns element(xbrli:context)`
- `xfi:period($item as schema-element(xbrli:item)) returns element(xbrli:period)`
- `xfi:period-start($period) returns xs:dateTime`
- `xfi:period-end($period) returns xs:dateTime`
- `xfi:is-instant-period($period) returns xs:boolean`
- `xfi:entity($item) returns element(xbrli:entity)`
- `xfi:identifier-value($identifier) returns xs:token`
- `xfi:identifier-scheme($identifier) returns xs:anyURI`
- `xfi:unit($item) returns element(xbrli:unit)?`
- `xfi:unit-numerator($unit) returns element(xbrli:measure)+`
- `xfi:unit-denominator($unit) returns element(xbrli:measure)*`

**Concept introspection:**

- `xfi:is-numeric($concept as xs:QName) returns xs:boolean`
- `xfi:is-non-numeric($concept as xs:QName) returns xs:boolean`

**Aspect equality (used heavily by Formula filters):**

- `xfi:s-equal`, `xfi:u-equal`, `xfi:v-equal`, `xfi:c-equal`, `xfi:p-equal`, `xfi:pc-equal`, `xfi:pcu-equal` — node-set aspect comparisons.
- `xfi:duplicate-item`, `xfi:duplicate-tuple`.

**Formula uncovered-aspect helpers:**

- `xff:uncovered-aspect($aspect, $dimension?) returns xs:anyType?`
- `xff:has-fallback-value($variable as xs:QName) returns xs:boolean`
- `xff:uncovered-dimensional-aspects() returns xs:QName*`

**Math (xfm, 2018):** `xfm:exp`, `xfm:log`, `xfm:pow`, `xfm:sqrt`,
`xfm:sin`, `xfm:atan2`, etc.

**OIM-era (CR 2023):** `f:period`, `f:period-type`,
`f:period-is-instant`, `f:has-dimension($fact, $dimension as xs:QName)`,
`f:dimension-value($fact, $dimension)`, `f:entity-identifier`,
`f:unit-numerators`, `f:decimals`, `r:facts()`, `r:non-nil-facts()`.

> **Honest gap note:** Function names commonly cited in older XBRL
> literature — `xfi:concept-balance`, `xfi:concept-period-type`,
> `xfi:fact-explicit-dimension-value` — are *not* present in the
> entries verified in the index table. They likely live in the
> **Dimensional Functions** add-on or in `xfi`'s schema module rather
> than the headline registry index. Treat any such name as unverified
> until you cross-check the registry XML at
> https://xbrl.org/functionregistry/functionregistry.xml.

### How taxonomies use them

Two consumption surfaces:

1. **Formula 1.0 assertions and filters.** A `va:valueAssertion` test, a `cf:conceptName` filter, or a `gf:generalFilter` body is an XPath 2.0 expression that may invoke any registered function. Example pattern: `xfi:period-end($v) gt xs:dateTime("2024-12-31T00:00:00")`.
2. **Table Linkbase node selectors.** Aspect-node and rule-node bodies use the same XPath dialect; functions like `xfi:period-instant` and `xff:uncovered-aspect` drive the cell coordinates.

For filers, this is mostly invisible — the regulator's filing rules
are encoded as Formula linkbases and the validator (Arelle, UBmatrix,
etc.) evaluates them against the submitted instance. But when a rule
fails, the error trace will name the specific `xfi:` function that
returned the unexpected value, and that is when a preparer needs to
know what these functions actually compute.

## XBRL Versioning 1.0

### Versioning report structure

Versioning 1.0 is published as a **modular** Recommendation set (all
dated 27 February 2013):

- **Versioning Base** — Recommendation
- **Versioning Concept Use** — Recommendation
- **Versioning Concept Details** — Recommendation
- **Versioning Dimensions** — Recommendation

Two further documents (Relationship Sets and Versioning Report
Content) sit at Public Working Draft status only.

A versioning report is an XML document whose root is `<ver:report>`.
Verified `ver` namespace URI from Table 1 of the Versioning Base
Recommendation: **`http://xbrl.org/2013/versioning-base`**. The
companion error namespace is `http://xbrl.org/2013/versioning-base/error`
(prefix `vere`).

Per Versioning Base §2, a report uses a three-tier hierarchy:

- **Assignments** (`<ver:assignment>`) — group changes by Assignment Category (e.g., equivalent meaning, technical only).
- **Actions** (`<ver:action>`) — describe one logical migration step.
- **Events** (`<ver:event>`) — the atomic, machine-actionable changes inside an action.

The report also names a **From DTS** and a **To DTS** (the two
taxonomy versions being compared) via `<ver:fromDTS>` and
`<ver:toDTS>` identifiers, plus optional `<ver:reportRef>` elements
linking related reports.

### Action types

Versioning Base defines only two Event types in the base layer:

- `<ver:namespaceRename>` — Namespace Rename Event.
- `<ver:roleChange>` — Role Change Event.

Everything else is delegated to extension modules:

- **Versioning Concept Use** — concept additions, deletions, and changes in concept *use* (e.g., abstract→concrete).
- **Versioning Concept Details** — XML Schema attribute changes (type changes, substitution group), XBRL concept attribute changes (balance, period type), label events, reference events, tuple content model events, and concept-correspondence linking. Error codes include `vercde:invalidConceptCorrespondence`, `vercde:invalidConceptLabelIdentifier`, `vercde:invalidConceptReferenceIdentifier`.
- **Versioning Dimensions** — dimension and hypercube-specific events.

Together these cover the practical migration scenarios filers
encounter: a concept being renamed across namespaces, a balance
flipping from credit to debit, a label being retired, a dimension
domain changing, or a tuple gaining a new permitted child.

### Adoption status

> **Honest gap note:** Primary regulator websites confirming exactly
> which authorities ship versioning reports with each annual taxonomy
> release were not freshly fetched in this run. The Versioning Base
> contributor list does include Haiko Philipp of the IFRS Foundation,
> consistent with industry practice that the IFRS Foundation publishes
> versioning reports alongside annual IFRS Taxonomy releases — but
> treat that as a strong but unverified expectation rather than a cited
> fact. Re-verify against the IFRS Foundation taxonomy publication
> page at filing time.

What is verified from the spec text itself: Versioning 1.0 is a stable
Recommendation as of 2013 with formal conformance machinery (the
conformance suite at
`xbrl.org/2011/versioning-conformance-suite-2011-10-19.zip`).

For filers, the practical importance is unchanged regardless of
regulator adoption: when a taxonomy renames `IncomeTaxExpense` to
`ProfitOrLossIncomeTaxExpense` between FY2024 and FY2025 versions, a
versioning report — if the issuer publishes one — gives tooling a
deterministic mapping so prior-period comparatives can be re-tagged
automatically rather than re-mapped by hand. Where no versioning
report exists, that diff has to be reconstructed manually from release
notes, which is the dominant cost in annual taxonomy migrations.

## Sources

- https://specifications.xbrl.org/specifications.html
- https://specifications.xbrl.org/spec-group-index-generic-links.html
- https://www.xbrl.org/specification/gnl/rec-2009-06-22/gnl-rec-2009-06-22.html
- https://www.xbrl.org/specification/genericlabels/rec-2011-10-24/genericlabels-rec-2011-10-24.html
- https://specifications.xbrl.org/work-product-index-generic-links-generic-links-1.0.html
- https://specifications.xbrl.org/spec-group-index-registries.html
- https://specifications.xbrl.org/work-product-index-registries-functions-registry-1.0.html
- https://specifications.xbrl.org/registries/functions-registry-1.0/index.html
- https://xbrl.org/functionregistry/functionregistry.xml
- https://www.xbrl.org/specification/functiondefinition/rec-2011-10-24/functiondefinition-rec-2011-10-24.html
- https://specifications.xbrl.org/spec-group-index-group-versioning.html
- https://www.xbrl.org/specification/versioning-base/rec-2013-02-27/versioning-base-rec-2013-02-27.html
- https://www.xbrl.org/specification/versioning-concept-details/rec-2013-02-27/versioning-concept-details-rec-2013-02-27.html
- https://www.xbrl.org/specification/versioning-concept-use/rec-2013-02-27/versioning-concept-use-rec-2013-02-27.html
- https://www.xbrl.org/specification/versioning-dimensions/rec-2013-02-27/versioning-dimensions-rec-2013-02-27.html
