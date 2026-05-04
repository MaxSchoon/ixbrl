# QNames, SQNames, NCNames, Substitution Groups, and Item Types

Every claim below is tied to a specification fetched live; URLs listed under **Sources**.

## NCName

An **NCName** ("non-colonized name") is the lexical building block for every namespace prefix and every local part in XML. W3C *Namespaces in XML 1.0* defines it as XML production [4]:

> `NCName ::= Name - (Char* ':' Char*)` — "An XML Name, minus the ':'"

Operationally:

- It is an XML `Name` (must start with a letter or `_`, followed by letters, digits, `.`, `-`, `_`, and certain Unicode combining/extender characters per the XML 1.0 `Name` production).
- It contains **no colon**.
- It cannot start with a digit, `-`, or `.`.
- Hyphens, underscores and periods are allowed in the interior.

In XBRL filings, the **`id`** attribute of every fact (`ix:nonFraction`,
`ix:nonNumeric`), every context, every unit, and every concept's
`@name` must be a valid NCName. Concept local names such as `Assets`,
`RevenueFromContractsWithCustomers`, or `bw2-titel9` (when used as a
*prefix*) are NCNames.

## QName (lexical and value space)

A **QName** ("qualified name") is defined by *Namespaces in XML 1.0*,
productions [7]–[11]:

```text
QName         ::= PrefixedName | UnprefixedName
PrefixedName  ::= Prefix ':' LocalPart
UnprefixedName::= LocalPart
Prefix        ::= NCName
LocalPart     ::= NCName
```

Two distinct concepts must be kept apart:

- **Prefixed name (lexical form)** — the literal `prefix:localPart` you see in an XML document, e.g., `bw2-titel9:Assets` or `ifrs-full:Revenue`. The prefix is a placeholder.
- **Expanded name (value-space form)** — the pair *(namespace URI, local name)*. The Namespaces spec defines it as "a pair consisting of a namespace name and a local name". This is what an XML processor compares for identity. Two prefixed names with different prefixes resolve to the **same** expanded name if both prefixes are bound to the same namespace URI.

Prefix binding happens via `xmlns:prefix="URI"` attributes (production
[2] `PrefixedAttName ::= 'xmlns:' NCName`) and the default-namespace
binding `xmlns="URI"` (production [3]). Bindings have lexical scope:
they apply to the element on which they are declared and all descendants
until overridden.

Two normative constraints from the Namespaces spec are relevant for
filings:

- **NSC: Prefix Declared** — every prefix used in a `QName` (in start-tags, end-tags, and attribute names) **MUST** be declared in scope. An undeclared prefix is a namespace-well-formedness error before XBRL validation runs.
- **NSC: No Prefix Undeclaring** — in XML 1.0, you cannot un-declare a non-default prefix. Re-declaring a prefix shadows the previous binding within the new subtree.

For attribute names: an unprefixed attribute is **not** in any namespace
(it is in "no namespace") — this differs from elements, where a
default namespace applies to unprefixed names.

## xs:QName, xs:NCName, xs:Name (XML Schema datatypes)

*XML Schema Part 2: Datatypes* defines built-in types whose value
spaces match the productions above:

- **`xs:Name`** — derived from `xs:token`; value space is the XML 1.0 `Name` production.
- **`xs:NCName`** — derived from `xs:Name`; value space is the *Namespaces in XML 1.0* `NCName` production. Used wherever XML Schema needs a non-colonized identifier (e.g., `@name` on `xs:element` declarations).
- **`xs:QName`** — a **primitive** datatype. Its **value space** is the set of (namespace URI, local name) pairs (i.e., expanded names). Its **lexical space** is the *Namespaces in XML 1.0* `QName` production. A schema processor that encounters a value of type `xs:QName` resolves the prefix using the in-scope namespace bindings of the element on which the value appears. **Moving an `xs:QName`-typed value to a different element can change its meaning** if the prefix bindings differ.

XBRL relies on this resolution rule for `@type`, `@substitutionGroup`,
and several attributes that carry concept references (e.g.,
`xbrldi:explicitMember/@dimension`).

## SQName (XBRL OIM)

The **Open Information Model (OIM) 1.0** Recommendation
(2021-10-13) introduces the concept of **prefixed content** to
describe values whose lexical form embeds a namespace prefix that must
be resolved against an external prefix-to-URI map rather than via XML
namespace declarations. The OIM lists, as prefixed content, values
whose datatype is or derives from:

- `xs:QName`
- `xbrli:QNameItemType`
- `dtr-type:SQNameType` / `dtr-type:SQNameItemType`
- `dtr-type:SQNamesType` / `dtr-type:SQNamesItemType`

The OIM states that "in an XML document, the map of prefixes to
namespace URIs is provided by namespace bindings (see [XML Names]).
Other formats based on this model typically use a **prefix map**." This
prefix-map mechanism is what makes **SQName** ("structured QName")
usable across xBRL-XML, xBRL-JSON, and xBRL-CSV: the same conceptual
`prefix:localname` lexical token is resolved through whichever
prefix-binding mechanism the serialization provides.

Key distinctions vs. `xs:QName`:

- `xs:QName` is resolved exclusively through XML namespace declarations in scope. It cannot survive a serialization to JSON or CSV that has no XML namespace machinery.
- SQName values use the **same lexical syntax** but carry their resolution rule in OIM rather than XML Schema. Equality is defined post-resolution: "the values are the same after resolving prefixes to namespace URIs" (OIM §5).

For accountants this matters because the *same fact* tagged with a
QName-typed value in xBRL-XML and an SQName-typed value in xBRL-JSON is
considered an equal fact only after both prefixes are resolved to the
canonical namespace URI.

## Substitution groups

XML Schema's **substitution group** mechanism lets one element
declaration substitute for another (the "head") wherever the head is
permitted, provided the substitute's type derives from the head's type.
XBRL builds its concept system on this mechanism.

Verified directly from `xbrl-instance-2003-12-31.xsd`:

```xml
<element name="item"  type="anyType" abstract="true"/>
<element name="tuple" type="anyType" abstract="true"/>
```

Both are abstract heads, both typed `anyType`. Verified directly from
`xbrldt-2005.xsd`:

```xml
<element name="hypercubeItem" abstract="true"
         substitutionGroup="xbrli:item" type="xbrli:stringItemType"
         xbrli:periodType="duration"/>
<element name="dimensionItem" abstract="true"
         substitutionGroup="xbrli:item" type="xbrli:stringItemType"
         xbrli:periodType="duration"/>
```

Verified from the linkbase schema (`xbrl-linkbase-2003-12-31.xsd`):

```xml
<element name="part" type="anySimpleType" abstract="true"/>
```

Roles in a filing:

- **`xbrli:item`** — head of every reportable simple concept. A concept declared `substitutionGroup="xbrli:item"` becomes a fact-bearing element in instances.
- **`xbrli:tuple`** — head for tuple concepts (groupings of facts that must occur together as a parent element rather than via dimensions). Tuple concepts have a `complexType` extending the tuple machinery; their `@type` is itself, not an item type.
- **`xbrldt:hypercubeItem`** — head for hypercubes (XDT cubes). Substitutes for `xbrli:item`.
- **`xbrldt:dimensionItem`** — head for dimensions (explicit and typed). Substitutes for `xbrli:item`.
- **`link:part`** — head for reference-resource parts used in reference linkbases (e.g., `ref:Number`, `ref:Paragraph`).

A taxonomy concept declaration must point its `@substitutionGroup` at
one of these heads (or at another concept that ultimately derives from
one).

## Item types — canonical catalog

The following types are confirmed as `complexType` declarations in
`xbrl-instance-2003-12-31.xsd` (verified by direct inspection of the
fetched schema). **Types not confirmed in the standard schema are
explicitly flagged.**

### Monetary

- `xbrli:monetaryItemType` — must be combined with an ISO 4217 currency unit (e.g., `iso4217:EUR`). Carries `xbrli:periodType` and may carry `xbrli:balance="debit|credit"`.

### Numeric (general)

- `xbrli:decimalItemType`
- `xbrli:floatItemType`
- `xbrli:doubleItemType`
- `xbrli:integerItemType`
- `xbrli:nonNegativeIntegerItemType`
- `xbrli:nonPositiveIntegerItemType`
- `xbrli:positiveIntegerItemType`
- `xbrli:negativeIntegerItemType`
- `xbrli:longItemType`, `xbrli:intItemType`, `xbrli:shortItemType`, `xbrli:byteItemType`
- `xbrli:unsignedLongItemType`, `xbrli:unsignedIntItemType`, `xbrli:unsignedShortItemType`, `xbrli:unsignedByteItemType`

### Special XBRL numeric

- `xbrli:sharesItemType` — must be combined with the unit `xbrli:shares`.
- `xbrli:pureItemType` — must be combined with the unit `xbrli:pure` (dimensionless ratios).

### Text/string

- `xbrli:stringItemType`
- `xbrli:normalizedStringItemType`
- `xbrli:tokenItemType`
- `xbrli:languageItemType`
- `xbrli:NameItemType`
- `xbrli:NCNameItemType`

> **Not present** in `xbrl-instance-2003-12-31.xsd`:
> `xbrli:NMTOKENItemType`, `xbrli:NMTOKENSItemType`,
> `xbrli:textBlockItemType`. The "text-block" idiom used for narrative
> tagging in IFRS, US-GAAP, and ESEF taxonomies is supplied by the
> **Data Types Registry (DTR)** — typically
> `dtr-type:textBlockItemType`, declared in the XBRL DTR rather than
> the core instance schema. Treat block-tagging types as DTR-sourced,
> not core-XBRL-sourced.

### Date/time

- `xbrli:dateItemType`
- `xbrli:timeItemType`
- `xbrli:dateTimeItemType`
- `xbrli:durationItemType`
- `xbrli:gYearItemType`
- `xbrli:gMonthItemType`
- `xbrli:gDayItemType`
- `xbrli:gYearMonthItemType`
- `xbrli:gMonthDayItemType`

> **Not confirmed** as standalone item types in the core schema:
> `xbrli:dayItemType`, `xbrli:monthItemType`, `xbrli:yearItemType`. The
> canonical XBRL types for partial dates are the gregorian-prefixed
> forms (`gYear`, `gMonth`, `gDay`). Do not use unverified
> `dayItemType` / `monthItemType` / `yearItemType` names.

### Other

- `xbrli:booleanItemType`
- `xbrli:QNameItemType`
- `xbrli:anyURIItemType`
- `xbrli:base64BinaryItemType`
- `xbrli:hexBinaryItemType`

### Fractions

- `xbrli:fractionItemType` — facts of this type are reported in `xbrli:fraction` elements (numerator/denominator), not as a simple value.

## Concept declaration attributes that depend on item type

Verified from the core instance schema and XBRL 2.1:

- **`xbrli:periodType`** — required attribute on every concept in substitution group `xbrli:item`. Values: `instant` (point in time, e.g., balance-sheet items) or `duration` (period flow, e.g., revenue, cash flows).
- **`xbrli:balance`** — optional. Values `debit` or `credit`. Per XBRL 2.1, only valid on concepts whose type derives from `xbrli:monetaryItemType`.
- **`abstract`** (XML Schema `xs:element/@abstract`) — boolean. Abstract concepts cannot appear as facts in instances; they exist purely to anchor presentation/calculation hierarchies.
- **`nillable`** — XML Schema element attribute. XBRL taxonomies typically declare concepts `nillable="true"` so a concept may appear with `xsi:nil="true"` (used in XBRL Dimensions and to assert "no value reported"). The XML Schema default for `nillable` is `false`; XBRL taxonomy authors set it explicitly.
- **`substitutionGroup`** — must (transitively) derive from `xbrli:item` for fact-bearing concepts, or `xbrli:tuple` for tuple concepts. Hypercubes use `xbrldt:hypercubeItem`; dimensions use `xbrldt:dimensionItem` (both still ultimately substitute for `xbrli:item`).
- **`type`** — must derive from one of the item types above. For tuple concepts the `@type` is a complex type local to the tuple declaration.

## SQName usage in xBRL-JSON and xBRL-CSV

In OIM-based JSON and CSV serializations, prefixes are not declared via
`xmlns:` attributes (there is no XML element to attach them to).
Instead, the report carries an explicit prefix-to-URI map. The OIM
characterizes it as: "Other formats based on this model typically use a
**prefix map**". Per the OIM Recommendation, concept references and
other prefixed content (e.g., dimension members, enumeration values)
are written as SQName lexical tokens (`prefix:localname`), and
processors resolve those tokens against the report's prefix map.

The practical implication for filings:

- The same concept may legitimately appear with different prefixes across two reports of the same taxonomy as long as the resolved expanded name is identical.
- Equality of fact concept, equality of dimension members, and equality of `xs:QName`-typed fact values are all defined on the resolved (URI, local-name) pair.
- A missing or wrong entry in the JSON/CSV prefix map produces a prefix-resolution error analogous to "NSC: Prefix Declared" in XML — but raised by the OIM processor, not the XML parser.

## Common QName errors

The classes of errors that surface during validation, in roughly the
order an XML/XBRL toolchain encounters them:

1. **Undeclared prefix.** The lexical form `pref:Local` appears but no in-scope `xmlns:pref` binding exists. Caught by the XML namespace processor before XBRL validation; violates *Namespaces in XML 1.0* `[NSC: Prefix Declared]`.
2. **Local part is not an NCName.** Examples: leading digit (`1Asset`), embedded colon (`Cash:Equivalent`), starts with `-` or `.`. Caught by the XML parser via the `Name`/`NCName` productions.
3. **Prefix is not an NCName.** Same rules as local parts; the prefix is itself produced from `NCName` (production [10]).
4. **Wrong prefix for the intended URI** (e.g., using `rj:Assets` when the concept actually lives in `bw2-titel9:` for Dutch GAAP). The XML is well-formed and the QName is valid, but the *expanded name* refers to a concept that does not exist. Caught by XBRL validation as "concept not found in DTS".
5. **Re-binding a prefix mid-document.** Legal per *Namespaces in XML 1.0* (the inner binding shadows), but a frequent source of human error — facts inside the inner subtree resolve to a different namespace than identical-looking facts outside it.
6. **Default-namespace confusion on attributes.** A default namespace declaration (`xmlns="..."`) **does not** apply to unprefixed attribute names. Authors who assume it does end up with attributes in "no namespace" rather than the intended namespace.
7. **`xs:QName`-typed value evaluated in the wrong scope.** Because `xs:QName` resolution depends on the in-scope namespace bindings *of the element where the value appears*, copying such a value across documents (or across XSL transforms) without preserving bindings silently changes its meaning.
8. **SQName prefix not in the OIM prefix map.** The JSON/CSV analogue of (1): the lexical token is well-formed but the prefix has no entry in the report's `namespaces` map.

For an iXBRL pipeline, errors (1)–(3) are caught by the XML parser, (4)
by the DTS resolver, (5)–(7) by careful schema-aware processing, and
(8) by the OIM processor when ingesting xBRL-JSON or xBRL-CSV exports.

## Sources

- https://www.w3.org/TR/xml-names/
- https://www.w3.org/TR/xmlschema-2/
- https://www.xbrl.org/Specification/XBRL-2.1/REC-2003-12-31/XBRL-2.1-REC-2003-12-31+corrected-errata-2013-02-20.html
- https://www.xbrl.org/2003/xbrl-instance-2003-12-31.xsd
- https://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd
- https://www.xbrl.org/2005/xbrldt-2005.xsd
- https://www.xbrl.org/Specification/dimensions/REC-2012-01-25/dimensions-REC-2012-01-25.html
- https://www.xbrl.org/Specification/oim/REC-2021-10-13/oim-REC-2021-10-13.html
