# XBRL Dimensions (XDT) — Hypercubes, Axes, and Dimensional Contexts

A bare XBRL fact is one-dimensional (concept × context × unit). Real reporting is multi-dimensional — by segment, share class, maturity bucket, counterparty. **XBRL Dimensions 1.0** ("XDT") adds orthogonal slicing via hypercubes attached to primary items, with dimension values carried in the `xbrli:segment` or `xbrli:scenario` container. Every regulator (ESMA, SEC, EBA, EIOPA, KvK/SBR) builds on the same XDT model; only the placement policy and axis choices vary.

## The XDT model

XBRL Dimensions 1.0 is a Recommendation dated **2012-01-25** (corrected
errata edition of the 2006-09-18 Recommendation). The xbrldt namespace
is `http://xbrl.org/2005/xbrldt`; the instance namespace `xbrldi` is
`http://xbrl.org/2006/xbrldi`.

Core definitions (XDT §2):

- **Primary item declaration** — an element in `xbrli:item`
  substitution group that is *not* a hypercube and *not* a dimension;
  this is what carries fact values.
- **Hypercube** — abstract element, substitution group
  `xbrldt:hypercubeItem`. A set of dimensions that together defines an
  admissible space of contexts for one or more primary items.
- **Dimension** — abstract element, substitution group
  `xbrldt:dimensionItem`. Two flavours: explicit (members are
  taxonomy-defined QNames) and typed (members are XML element values).
- **Domain / member** — for explicit dimensions, members are
  item-substitution-group concepts wired through `dimension-domain`
  and `domain-member` relationships.

### Linkbase arcroles

All six declared in the xbrldt schema and used on `link:definitionArc`
only.

| Role | Full URI |
|---|---|
| has-hypercube (positive) | `http://xbrl.org/int/dim/arcrole/all` |
| has-hypercube (negative) | `http://xbrl.org/int/dim/arcrole/notAll` |
| hypercube → dimension | `http://xbrl.org/int/dim/arcrole/hypercube-dimension` |
| dimension → domain root | `http://xbrl.org/int/dim/arcrole/dimension-domain` |
| domain → member | `http://xbrl.org/int/dim/arcrole/domain-member` |
| dimension → default member | `http://xbrl.org/int/dim/arcrole/dimension-default` |

## "Axis" naming convention

**Axis**, **Domain**, **Member** are **not** XDT spec vocabulary — XDT uses "dimensions", "domains", "members". "Axis" is a naming convention adopted by the major standard taxonomies. SEC *EDGAR XBRL Filing Guide* (Sept 2024, §3.5): *"in this document as in all SEC standard taxonomies a taxonomy-defined dimension is called an Axis"*. The IFRS Taxonomy follows the same convention: every explicit dimension declaration in `full_ifrs-cor_2024-03-27.xsd` ends in `Axis` (e.g. `ifrs-full:ConsolidatedAndSeparateFinancialStatementsAxis`, `ifrs-full:RetrospectiveApplicationAndRetrospectiveRestatementAxis`). Treat "Axis" as a label suffix synonymous with "explicit dimension"; it never appears in the XDT spec or in instance documents.

## Explicit vs typed dimensions

**Explicit dimension** — domain members are taxonomy-defined QNames.
An instance reports a value via `xbrldi:explicitMember`:

```xml
<xbrldi:explicitMember dimension="us-gaap:StatementBusinessSegmentsAxis">
  acme:AviationSegmentMember
</xbrldi:explicitMember>
```

XDT §3.1.4.3.2 requires the `dimension` attribute to be the QName of
an explicit dimension declaration and the element content to be the
QName of a member of that dimension's domain.

**Typed dimension** — the domain is described by an arbitrary XML
Schema element. The dimension declaration carries
`xbrldt:typedDomainRef` as an `xs:anyURI` containing an XPointer
fragment identifier pointing to the global element declaration of the
value type:

```xml
<xs:element name="CounterpartyId" id="ct_id"
            substitutionGroup="xbrldt:dimensionItem"
            type="xbrli:stringItemType"
            abstract="true"
            xbrli:periodType="duration"
            xbrldt:typedDomainRef="schema.xsd#ct_id_value"/>
```

XDT §2.5.2.1 mandates that `xbrldt:typedDomainRef` MUST contain a
fragment identifier conformant with XPointer §3.2 and must resolve to
a global element declaration in the DTS. Reports use
`xbrldi:typedMember` whose child element is an instantiation of the
referenced element:

```xml
<xbrldi:typedMember dimension="eba:CounterpartyId">
  <eba:ct_id_value>LEI:529900T8BM49AURSDO55</eba:ct_id_value>
</xbrldi:typedMember>
```

## Default members

A dimension MAY declare exactly one default member via a
`dimension-default` arc (XDT §2.7.1). The default member is
*implicit*: an instance MUST NOT include an `xbrldi:explicitMember`
whose value is the default for its dimension. Doing so raises
`xbrldie:DefaultValueUsedInInstanceError`.

SEC EDGAR XBRL Filing Guide §10.7.1 presentation rule: *"If the default member of an Axis does not appear in an effective presentation relationship base set, then the only facts that can be displayed by that presentation base set are facts in contexts having a non-defaulted member on that Axis."* §5.6 (formerly EFM v68 §6.8.19): do not declare "Total" domain members — the default member fills that role. SEC reports emit the default member's QName only in *presentation* arcs and `xbrldi:explicitMember` only for non-default values.

## Segment vs scenario placement

XDT §2.3.2 places `@xbrldt:contextElement` **on the has-hypercube arc**
(i.e., `all` / `notAll` arcs from primary item to hypercube) — **not**
on `hypercube-dimension` arcs. The attribute is declared as an
`xs:token` restricted to `segment` or `scenario`. It tells the
dimensional processor which container in the instance context
(`xbrli:segment` or `xbrli:scenario`) must contain the dimension
values for the hypercube to validate.

ESEF picks one: **scenario only.** ESEF Reporting Manual §2.1.3:
*"Extension taxonomy MUST set xbrli:scenario as context element on
definition arcs with `http://xbrl.org/int/dim/arcrole/all` and
`http://xbrl.org/int/dim/arcrole/notAll` arcroles. xbrli:segment
container MUST NOT be used in contexts."* The Arelle ESEF validator
emits two error codes against this rule (confirmed in
`arelle/plugin/validate/ESEF/ESEF_Current/ValidateXbrlFinally.py`):

- `ESEF.2.1.3.segmentUsed` — *xbrli:segment container MUST NOT be used in contexts*.
- `ESEF.2.1.3.scenarioContainsNonDimensionalContent` — *xbrli:scenario in contexts MUST NOT contain any other content than defined in XBRL Dimensions specification*.

In ESEF, `xbrli:scenario` may contain only `xbrldi:explicitMember` and
`xbrldi:typedMember`; nothing else.

## Open vs closed hypercubes

`@xbrldt:closed` is declared on has-hypercube arcs as `xs:boolean`
with **default `false`** (XDT §2.3.3). Semantics:

- `closed="false"` (open, the default) — additional dimensions in the indicated container are tolerated; the hypercube's enumerated dimensions must still validate, but the context may contain dimensions outside the set.
- `closed="true"` (closed) — the indicated container (`segment` or `scenario` per `@xbrldt:contextElement`) must contain *only* dimensions from this hypercube and *exactly* the declared dimensions; any unexpected dimension value invalidates the hypercube.

Closed hypercubes are how regulators express "this primary item may
only be reported with these dimensions and no others."

## Dimensional validity errors

Instance-level errors (XDT §3.2 — `xbrldie:` namespace):

| Code | Meaning | Typical fix |
|---|---|---|
| `xbrldie:PrimaryItemDimensionallyInvalidError` | Fact's primary item is reported with a context that does not satisfy the DRS for the hypercubes it belongs to. | Check the fact's hypercube DRS; remove illegal dimension values or add the missing required ones. |
| `xbrldie:DefaultValueUsedInInstanceError` | An `xbrldi:explicitMember` reports the dimension's default member explicitly. | Remove the explicit default — defaults are implicit. |
| `xbrldie:IllegalTypedDimensionContentError` | The XML inside `xbrldi:typedMember` does not validate against the schema referenced by `xbrldt:typedDomainRef`. | Fix the typed-dimension XML to match the referenced element declaration. |
| `xbrldie:RepeatedDimensionInInstanceError` | Same dimension reported twice in the same context's segment/scenario. | Remove the duplicate `xbrldi:explicitMember` / `xbrldi:typedMember`. |
| `xbrldie:ExplicitMemberNotExplicitDimensionError` | `xbrldi:explicitMember/@dimension` references a typed dimension. | Use `xbrldi:typedMember` instead. |
| `xbrldie:TypedMemberNotTypedDimensionError` | `xbrldi:typedMember/@dimension` references an explicit dimension. | Use `xbrldi:explicitMember` instead. |
| `xbrldie:ExplicitMemberUndefinedQNameError` | The QName content of `xbrldi:explicitMember` is not a member of the dimension's domain. | Use a domain member that is in scope via `dimension-domain` / `domain-member` arcs. |

Taxonomy-level errors (XDT §4 — `xbrldte:` namespace, distinct from
`xbrldie:`) include:

- `xbrldte:HasHypercubeMissingContextElementAttributeError`
- `xbrldte:HypercubeElementIsNotAbstractError`
- `xbrldte:DimensionElementIsNotAbstractError`
- `xbrldte:TooManyDefaultMembersError`
- `xbrldte:TypedDomainRefError`
- `xbrldte:TypedDimensionURIError`
- `xbrldte:OutOfDTSSchemaError`
- `xbrldte:DRSDirectedCycleError`
- `xbrldte:TargetRoleNotResolvedError`
- `xbrldte:PrimaryItemPolymorphismError`

## How dimensions show up in each regime

**ESEF / IFRS** — most-used axes (all in the `ifrs-full` namespace,
taxonomy 2024-03-27):

- `ifrs-full:ConsolidatedAndSeparateFinancialStatementsAxis`
- `ifrs-full:RetrospectiveApplicationAndRetrospectiveRestatementAxis`
- `ifrs-full:ClassesOfFinancialAssetsAxis`, `ifrs-full:ClassesOfFinancialLiabilitiesAxis`
- `ifrs-full:ClassesOfOrdinarySharesAxis`
- `ifrs-full:ContinuingAndDiscontinuedOperationsAxis`
- `ifrs-full:CarryingAmountAccumulatedDepreciationAmortisationAndImpairmentAndGrossCarryingAmountAxis`

**SEC EDGAR (us-gaap + srt + dei)** — the EDGAR XBRL Filing Guide
spends its dimensions chapter on a small set:

- `us-gaap:StatementBusinessSegmentsAxis` with members like custom `acme:AviationSegmentMember`
- `us-gaap:StatementClassOfStockAxis` (default `us-gaap:ClassOfStockDomain`)
- `srt:ConsolidationItemsAxis` — used to report consolidating, eliminations, parent-only
- `srt:RangeAxis` (members `srt:MinimumMember`, `srt:MaximumMember`, `srt:WeightedAverageMember`)
- `dei:LegalEntityAxis` — for parent and subsidiaries; the default is "all entities consolidated"

**Dutch SBR / KvK** — uses the same XDT machinery via the NT
(Nederlandse Taxonomie) entry points; `bw2-titel9` defines line items,
and member axes are declared in extension/structure schemas (see KvK
iXBRL deposit and NT taxonomy on sbr-nl.nl).

**EBA DPM (COREP/FINREP) and EIOPA Solvency II** — heavily
*typed-dimension* rather than explicit. Counterparty IDs, deal IDs,
and instrument IDs are typed dimensions whose `xbrldt:typedDomainRef`
points to schema-validated string or pattern types.

## Authoring an extension hypercube — checklist

1. Declare the hypercube element (`substitutionGroup="xbrldt:hypercubeItem"`, `abstract="true"`).
2. Declare each new dimension element (`substitutionGroup="xbrldt:dimensionItem"`, `abstract="true"`); for typed dimensions add `xbrldt:typedDomainRef`.
3. In a definition link with the right `xlink:role`, draw an `all` (or `notAll`) arc from the primary item(s) to the hypercube. Set `@xbrldt:contextElement="scenario"` (ESEF/IFRS practice) and decide `@xbrldt:closed`.
4. Draw `hypercube-dimension` arcs from the hypercube to each dimension.
5. For each explicit dimension, draw a `dimension-domain` arc to the domain root, then `domain-member` arcs to each usable member; mark non-usable members with `@xbrldt:usable="false"` on the arc.
6. If the dimension has a default, draw a single `dimension-default` arc; do *not* re-emit the default explicitly in instance contexts.

## Pitfalls and review checklist

1. Emitting the default member explicitly — fires `xbrldie:DefaultValueUsedInInstanceError`. Remove it from the context.
2. Putting dimensions in `xbrli:segment` for an ESEF filing — fires `ESEF.2.1.3.segmentUsed`. Move to `scenario`.
3. Putting non-dimensional XML in `xbrli:scenario` for ESEF — fires `ESEF.2.1.3.scenarioContainsNonDimensionalContent`. Strip everything except `xbrldi:*Member`.
4. Using `xbrldi:explicitMember` for a typed dimension or vice versa — fires `xbrldie:ExplicitMemberNotExplicitDimensionError` / `TypedMemberNotTypedDimensionError`.
5. Same dimension twice in one context — fires `xbrldie:RepeatedDimensionInInstanceError`. Merge or pick one.
6. Forgetting `@xbrldt:contextElement` on an `all` / `notAll` arc — fires `xbrldte:HasHypercubeMissingContextElementAttributeError`. The attribute is mandatory.
7. Declaring a "Total" custom member on a SEC filing — violates EDGAR XBRL Filing Guide §5.6 (formerly EFM v68 §6.8.19); use the existing default member instead.
8. Presenting an axis without showing the default member — facts in the default context become invisible per EDGAR XBRL Filing Guide §10.7.1. Either show the default in the presentation tree, or accept that only non-default facts will render.
9. `xbrldt:typedDomainRef` without an XPointer fragment — fires `xbrldte:TypedDimensionURIError`.
10. Two `dimension-default` arcs for the same dimension — fires `xbrldte:TooManyDefaultMembersError`. Only one default per dimension.

## Sources

- https://specifications.xbrl.org/work-product-index-group-dimensions-dimensions.html
- https://www.xbrl.org/specification/dimensions/rec-2012-01-25/dimensions-rec-2006-09-18+corrected-errata-2012-01-25-clean.html
- http://www.xbrl.org/2005/xbrldt-2005.xsd
- https://raw.githubusercontent.com/Arelle/Arelle/master/arelle/plugin/validate/ESEF/ESEF_Current/ValidateXbrlFinally.py
- https://www.esma.europa.eu/document/esef-reporting-manual
- https://www.esma.europa.eu/sites/default/files/library/esma32-60-254_esef_reporting_manual.pdf
- https://www.sec.gov/info/edgar/edmanuals.htm
- https://www.sec.gov/files/edgar/filermanual/edgarfm-vol2-v77.pdf
- https://www.sec.gov/files/edgar/xbrl-guide.pdf
- https://xbrl.ifrs.org/taxonomy/2024-03-27/full_ifrs/labels/lab_full_ifrs-en_2024-03-27.xml
- https://www.eba.europa.eu/risk-and-data-analysis/reporting-frameworks/dpm-data-dictionary

**Coverage notes:** The IFRS Taxonomy Architecture document and the
FASB Taxonomy Architecture Guide were not directly retrievable when
this reference was prepared (FASB returned 403, IFRS Foundation
download paths returned 404 for guessed URLs); the "Axis is a taxonomy
convention, not an XDT term" claim is grounded in the SEC EDGAR XBRL
Filing Guide §3.5 and corroborated by every Axis-suffixed element in
the IFRS 2024-03-27 labels linkbase. The current SEC XBRL validation
rules — historically labelled "EFM 6.5/6.6" — now live in the *EDGAR
XBRL Filing Guide* (xbrl-guide.pdf) rather than EFM Volume II; the
older EFM section numbers are preserved as parenthetical "(Formerly
EFM v68 § 6.6.x)" cross-references in the new Guide.
