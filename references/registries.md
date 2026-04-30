# XBRL Registries — LRR, DTR, and URI Resolution

XBRL 2.1 (2003) is deliberately minimal: seven label roles, a small set of item types, a linkbase mechanism. Real-world filings (ESEF, US-GAAP, IFRS, SBR) need more. XBRL International publishes those extensions through **registries** — versioned, community-maintained lists of URIs and types that act as de facto standards. This file covers the two most consequential — **Label Role Registry (LRR)** and **Data Types Registry (DTR)** — plus URI resolution (xsi, xml:base, XML Catalogs).

XBRL International registries index: https://specifications.xbrl.org/spec-group-index-registries.html — lists LRR, DTR, Units Registry, Functions Registry, and the separately versioned Inline XBRL Transformation Registry.

## Label Role Registry (LRR)

### Purpose

XBRL 2.1 §5.2.2.2.2 defines exactly seven standard label roles:
`label`, `terseLabel`, `verboseLabel`, `totalLabel`,
`periodStartLabel`, `periodEndLabel`, `documentation`. The LRR
registers additional `<link:label>` `xlink:role` URIs that taxonomy
authors and renderers have agreed on across jurisdictions. The current
version is **LRR 2.0**, published at
https://specifications.xbrl.org/registries/lrr-2.0/ (work-product
index: https://specifications.xbrl.org/work-product-index-registries-lrr-2.0.html).

The most operationally important roles in the LRR are the
**negated-label** family. They tell a renderer to flip the displayed
sign of a fact while leaving the underlying XBRL value untouched —
essential because XBRL signs follow a concept's `xbrli:balance`,
which often disagrees with how the figure is presented in a printed
statement (e.g., expenses presented as positive deductions).

### Negated-label roles (verified URIs)

All from base `http://www.xbrl.org/2009/role/`:

- `negatedLabel` — `http://www.xbrl.org/2009/role/negatedLabel`
- `negatedTerseLabel` — `http://www.xbrl.org/2009/role/negatedTerseLabel`
- `negatedTotalLabel` — `http://www.xbrl.org/2009/role/negatedTotalLabel`
- `negatedPeriodStartLabel` — `http://www.xbrl.org/2009/role/negatedPeriodStartLabel`
- `negatedPeriodEndLabel` — `http://www.xbrl.org/2009/role/negatedPeriodEndLabel`
- `negatedNetLabel` — `http://www.xbrl.org/2009/role/negatedNetLabel`
- `netLabel` — `http://www.xbrl.org/2009/role/netLabel`

> **Honest gap note:** A `negatedVerboseLabel` was not present in the
> registry contents fetched. Treat its existence as unverified; the
> verified negated set is the six above plus
> `netLabel` / `negatedNetLabel`. The LRR also intentionally does not
> register `*PeriodEndTotalLabel`-style negated variants — instead it
> offers `positivePeriodEndTotalLabel`,
> `negativePeriodEndTotalLabel`, etc.

### Other LRR roles (verified)

Sign-conditional balance labels (base `http://www.xbrl.org/2009/role/`):

- `positivePeriodStartLabel`, `positivePeriodEndLabel`, `positivePeriodStartTotalLabel`, `positivePeriodEndTotalLabel`
- `negativePeriodStartLabel`, `negativePeriodEndLabel`, `negativePeriodStartTotalLabel`, `negativePeriodEndTotalLabel`

Lifecycle and reference roles:

- `restatedLabel` — `http://www.xbrl.org/2006/role/restatedLabel` (note the 2006 base — older than the rest)
- `deprecatedLabel`, `deprecatedDateLabel` — `http://www.xbrl.org/2009/role/...`
- `commonPracticeRef`, `nonauthoritativeLiteratureRef`, `recognitionRef` — reference resource roles

OIM-era property roles (base `https://www.xbrl.org/2022/role/`):

- `property`, `propertyWithLang`

Legacy `us-gaap` negated roles (`http://xbrl.us/us-gaap/role/label/...`)
and Japanese EDINET roles
(`http://info.edinet-fsa.go.jp/jp/fr/gaap/role/...`) are also
registered for backward compatibility.

The LRR additionally registers **arc-roles**, including:

- `parent-child` — `http://www.xbrl.org/2013/arcrole/parent-child`
- ESMA's `wider-narrower` for ESEF anchoring — `http://www.esma.europa.eu/xbrl/esef/arcrole/wider-narrower`
- 2023 OIM arc-roles: `instant-inflow`, `instant-outflow`, `instant-contra`, `instant-accrual`, `trait-concept`, `class-subclass`, `trait-domain`.

> **Honest gap note:** `commentaryGuidance` / `disclosureGuidance` /
> `exampleGuidance` / `presentationGuidance` / `measurementGuidance` /
> `definitionGuidance` / `placementGuidance` were **not present** in
> the LRR 2.0 content fetched. They appear to be a US-GAAP / FASB
> Reference Guide convention rather than registered LRR roles.

### Adoption

Negated labels are mandatory presentation infrastructure in **ESEF**
(ESMA Inline XBRL filings) and **US-GAAP** (FASB Taxonomy uses both LRR
`negatedLabel` and the legacy `xbrl.us` variants). **IFRS Taxonomy**
uses the LRR `totalLabel`, `periodStartLabel`, `periodEndLabel` and the
negated variants for sign presentation. The `wider-narrower` arc-role
is unique to ESEF and is the spine of issuer-extension anchoring.

## Data Types Registry (DTR)

### Purpose

The DTR registers XML Schema simple/complex item types used in XBRL
taxonomies that go beyond the core types in the XBRL 2.1 instance
schema (`monetaryItemType`, `decimalItemType`, `stringItemType`, etc.).
The registry is published at http://www.xbrl.org/dtr/dtr.xml;
specification/process pages live at
https://specifications.xbrl.org/work-product-index-registries-dtr-1.1.html.

The registry XML carries the version date **2024-01-31**, and **all
current entries share a single namespace URI**:
`http://www.xbrl.org/dtr/type/2024-01-31` (typical prefix `dtr-types`
or `dtr`). The conventional module split (`types`, `numeric`,
`structure`) is recorded as metadata on each entry rather than as
separate namespaces in this revision.

### Types module (verified contents)

- `textBlockItemType` — narrative HTML-fragment tagging (the most heavily used DTR type globally)
- `escapedItemType` — escaped markup
- `xmlItemType`, `xmlNodesItemType` — embedded XML
- `domainItemType` — used as the type of dimension domain members
- `noLangTokenItemType`, `noLangStringItemType` — language-neutral string/token
- `gYearListItemType` — list of gregorian years
- `dateTimeItemType` — DTR-flavoured datetime

### Numeric module (verified contents)

Quantity types: `percentItemType`, `perShareItemType`, `areaItemType`,
`volumeItemType`, `weightItemType`, `massItemType`, `lengthItemType`,
`energyItemType`, `powerItemType`, `memoryItemType`,
`temperatureItemType`, `pressureItemType`, `frequencyItemType`,
`speedItemType`, `planeAngleItemType`, `voltageItemType`,
`electricCurrentItemType`, `electricChargeItemType`, `forceItemType`,
`irradianceItemType`, `insolationItemType`, `flowItemType`,
`massFlowItemType`.

Monetary variants: `noDecimalsMonetaryItemType`,
`nonNegativeMonetaryItemType`, `nonNegativeNoDecimalsMonetaryItemType`.

Sustainability/ESRS-relevant ratios: `ghgEmissionsItemType`,
`monetaryPerLengthItemType`, `monetaryPerAreaItemType`,
`monetaryPerVolumeItemType`, `monetaryPerDurationItemType`,
`monetaryPerEnergyItemType`, `monetaryPerMassItemType`,
`energyPerMonetaryItemType`, `ghgEmissionsPerMonetaryItemType`,
`volumePerMonetaryItemType`.

> **Honest gap note:** `decimal2ItemType` / `decimal4ItemType`
> (sometimes seen in older drafts) are **not** in the current
> registry.

### Structure module (SQNames and prefixed content)

These types underpin the Open Information Model (OIM) and CSV/JSON
report formats:

- `SQNameType`, `SQNamesType` (XML Schema simple types)
- `SQNameItemType`, `SQNamesItemType` (xbrli item types)
- `prefixedContentType`, `prefixedContentItemType`
- `guidanceItemType`

An "SQName" is a string-form qualified name (`prefix:local`) that
carries its own prefix-to-namespace bindings — designed so that fact
values which are themselves QNames can survive serialisation in
non-XML formats. See `references/types.md` §SQName for the OIM
mechanism in detail.

### Adoption

`textBlockItemType` is the workhorse for narrative tagging in **ESEF**
(block-tagging of notes under ESMA's Annex II), **US-GAAP** (full
footnote tagging is mandatory), and the **IFRS Taxonomy**.
`percentItemType` types ratios; `perShareItemType` types EPS /
dividend-per-share concepts. The numeric quantity types (mass, energy,
GHG emissions) are central to the ESRS/CSRD digital taxonomy and to
IFRS S1/S2 sustainability reporting.

## URI resolution conventions in XBRL

### xsi attributes

`http://www.w3.org/2001/XMLSchema-instance` (prefix `xsi`) is core XML
Schema, not XBRL-specific, but two attributes appear constantly in
iXBRL output:

- `xsi:nil="true"` on `ix:nonFraction` / `ix:nonNumeric` to express an explicitly absent fact (paired with `xsi:nil`-aware concept declarations).
- `xsi:type` to override the static type when a generic element carries a more specific DTR type.

### xml:base

The W3C `xml:base` attribute lets an element override the base URI
used to resolve any relative URI references in its subtree. In XBRL
linkbases that uses `xlink:href`, this would change which target
document an arc resolves to.

ESEF prohibits both `xml:base` and the HTML `<base>` element in inline
reports (`ESEF.2.4.2.htmlOrXmlBaseUsed`). Filers must therefore not
rely on relative-URI rebasing inside the iXBRL document; all `href`
and `src` values must resolve directly. This is one of the items
processors flag during ESEF conformance checking.

### XML Catalogs and taxonomy packages

The XBRL Taxonomy Packages 1.0 specification (REC-2016-04-19) requires
a `META-INF/catalog.xml` inside every package zip. That file is a
**restricted subset of the OASIS XML Catalogs specification** and is
limited to `<rewriteURI>` entries. Each entry has:

- `uriStartString` — the public URL prefix to match
- `rewritePrefix` — the replacement (typically a relative path like `../www.example.com/taxonomy/...`)

Resolution uses the **longest matching prefix**. The result is that a
processor opening the package can resolve a public URL such as
`http://www.example.com/taxonomy/2025/entry.xsd` to a file inside the
zip without any network access. This is what makes Arelle and other
validators able to load a taxonomy package offline, and it is why
production validators pin `webCache.recheck = "never"` once a package
is installed.

The package spec deliberately does **not** allow `<rewriteSystem>` or
other catalog mechanisms, keeping behaviour predictable across
implementations.

### DNS-resolvable taxonomy URIs

XBRL namespaces are URIs, not URLs — the standard does not require
them to dereference. But ESEF treats issuer extension taxonomies as
web resources: each filing's extension namespace and its entry-point
URL ought to be resolvable so that downstream consumers (regulators,
data aggregators, the European Single Access Point) can fetch and
cache them.

Practical consequences for taxonomy authors:

- The extension namespace authority (the host part of the namespace URI) should be a domain the issuer controls and that resolves in DNS.
- If the namespace URI also serves as the schema's location hint, hosting the schema at that URL is good practice (and is assumed by some consumers).
- In code paths that *generate* a filing, do not gate generation on live DNS resolution — transient failures break otherwise-valid output. DNS validation belongs at the user-input boundary (taxonomy registration), not in the iXBRL writer.

## Sources

- https://specifications.xbrl.org/spec-group-index-registries.html
- https://specifications.xbrl.org/work-product-index-registries-lrr-2.0.html
- https://specifications.xbrl.org/registries/lrr-2.0/
- https://specifications.xbrl.org/work-product-index-registries-dtr-1.1.html
- http://www.xbrl.org/dtr/dtr.xml
- https://www.xbrl.org/Specification/taxonomy-package/REC-2016-04-19/taxonomy-package-REC-2016-04-19.html
