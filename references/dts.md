# The Discoverable Taxonomy Set (DTS): how it works, how to read one, how it moves in time

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*

**Load this when:** the question is which concept a fact binds to, which label in which role and language, which network a concept is in, whether a QName is declared at all, which taxonomy release was operative for a report, or how to resolve a `schemaRef` offline.

**Do not load this when:** the question is how the linkbases are wired in general (`references/structure.md`), or is dimensional design (`references/dimensions.md`), or is a regime's filing rule (the jurisdiction file).

Load this when the question is "which concept does this fact bind to", "which
label, in which role and language", "which network is this concept in", "is this
QName even declared", "which taxonomy version was operative for this report",
or "how do I resolve a `schemaRef` offline". It is the layer beneath every
jurisdiction file: they tell you *which* DTS; this file tells you what a DTS is
and how to interrogate it. Run `scripts/dts_profile.py` to do the interrogating.

**Last verified (UTC): 2026-08-21.** Every count in the comparison table was
produced on that date by `scripts/dts_profile.py` from the JSON it emits; the
concept, abstract, presentation, calculation, XDT-arcrole, label and reference
counts were cross-checked against Arelle 2.41.7 on the same entry points (the
typed-dimension, role-type, distinct-label-role and generic-link rows were
not, and are the tool's own reading); the specification citations were read
from the live documents the same day (Sources).

## Contents

- [What a DTS is](#what-a-dts-is)
- [The discovery pointers](#the-discovery-pointers)
- [Entry points, packages, catalogs](#entry-points-packages-catalogs)
- [Nodes: what a DTS declares](#nodes-what-a-dts-declares)
- [Edges: the networks](#edges-the-networks)
- [From a fact to its concept, its label, its statement](#from-a-fact-to-its-concept-its-label-its-statement)
- [Six DTSs compared, measured](#six-dtss-compared-measured)
- [Bi-temporal: valid time and acceptance window](#bi-temporal-valid-time-and-acceptance-window)
- [Working with `scripts/dts_profile.py`](#working-with-scriptsdts_profilepy)
- [Gotchas that cost real filings](#gotchas-that-cost-real-filings)
- [Vocabulary used by every jurisdiction table](#vocabulary-used-by-every-jurisdiction-table)
- [Sources](#sources)

## What a DTS is

XBRL 2.1 defines it in the glossary (section 1.4): "A DTS is a collection of
taxonomy schemas and linkbases. The bounds of a DTS are such that the DTS
includes all taxonomy schemas and linkbases that can be discovered by following
links or references in the taxonomy schemas and linkbases included in the
DTS". The self-reference is the point: it is a closure, not one-hop
reachability. Section 3.2 gives the procedure: "The bounds of a DTS are
determined by starting from some set of documents (instance, taxonomy schema,
or linkbase) and following DTS discovery rules." Two consequences are easy to
get wrong:

- **The instance is a starting point but not a member.** "Although an XBRL
  instance can be the starting point for DTS discovery, the XBRL instance
  itself is not part of the DTS." (3.2) The schemas and linkbases used as
  starting points *are* members.
- **Discovery is a closure, and it is mandatory.** "All references to Taxonomy
  Schemas and linkbases MUST be resolved when determining the DTS supporting
  an XBRL instance." (3.2) A processor that cannot resolve one pointer has not
  loaded the DTS; what it loaded is a different, smaller taxonomy, and every
  verdict it gives is about that smaller thing.

Cite section 3.2 for the discovery rules and section 1.4 for the definition.
There is no section 3.2.1; the spec's 3.2 has no sub-sections.

Everything a fact depends on lives in this closure. The fact's QName must name
a concept declared by a schema in the DTS; the concept's labels, references,
presentation position, calculation weights and dimensional membership are all
arcs in linkbases of the DTS. "Not in the DTS" therefore means "has no
meaning in this report", whatever the element name looks like.

## The discovery pointers

Every pointer below is one of the rules in XBRL 2.1 section 3.2. A walker
follows each, resolves the `href` against the document it appears in, strips
the fragment, and adds the target to the set until nothing new appears. Each
row also names the way that pointer fails in practice, because the failure is
what you will be diagnosing.

| Pointer | Appears in | Pulls in | How it fails in practice |
|---|---|---|---|
| `link:schemaRef/@xlink:href` | an instance; in Inline XBRL inside `ix:references` in the `<head>` | the entry-point schema (XBRL 2.1 section 4.2: at least one is required) | href points at a file that is not where the filer's package put it (the bundled scaffold deliberately does this: `assets/ixbrl-skeleton.xhtml` names `example-extension.xsd`, which does not ship) |
| `link:linkbaseRef/@xlink:href` | an instance (section 4.3), or a schema's `xs:annotation/xs:appinfo` | one linkbase; the `xlink:role` says which kind (`…/presentationLinkbaseRef` and so on) | an extension schema that forgets the role, or a linkbase reachable only from an instance so that the taxonomy alone never sees it |
| `xs:import/@schemaLocation`, `xs:include/@schemaLocation` | a schema | another schema; import crosses namespaces, include does not | two distinct hazards: an `xs:import` that names a namespace and no `schemaLocation` resolves only through a catalog or cache (the profiler reports it as unresolved); and a *relative* `schemaLocation` resolves only while the package layout is intact (the FRC core imports its ten modules by paths such as `../../../cd/2026-01-01/business/bus-2026-01-01.xsd`, so a single copied file walks nowhere) |
| `link:roleRef/@xlink:href`, `link:arcroleRef/@xlink:href` | a linkbase, or an instance (for footnote links only, sections 4.4 and 4.5) | the schema that declares a custom role or arcrole | a calculation linkbase using the Calc 1.1 arcrole without an `arcroleRef` to `https://www.xbrl.org/2023/calculation-1.1.xsd` |
| `link:loc/@xlink:href` | any extended link | the schema the locator points into | a locator whose fragment names an id nothing declares; the profiler reports these as "id not declared in that document" |
| embedded linkbases | `//xsd:schema/xsd:annotation/xsd:appinfo/*` | linkbases written inside the schema | a walker that only follows `linkbaseRef` never sees them; the NT/KvK 2025 NL-GAAP entry point carries four |
| `xs:redefine` | nowhere | nothing | "since `<redefine>` is prohibited in Taxonomy Schemas it cannot play a role in DTS discovery" (3.2) |

XBRL Dimensions adds no discovery rule. XDT explicitly imports the 2.1
terminology ("DTS (discoverable taxonomy set) … As defined by [XBRL 2.1]",
XDT section 1.3). `@xbrldt:typedDomainRef` is an href to an element declaration
that must already be in the DTS; pointing outside it is the error
`xbrldte:OutOfDTSSchemaError`, not a discovery trigger. The profiler follows it
anyway so that the failure is reported rather than silent.

## Entry points, packages, catalogs

**An entry point is a set of URLs, not a file.** Taxonomy Packages 1.0 section
3.2.2: "An entry point is a set of URLs that define a logical starting point
for the DTS discovery process". One `tp:entryPoint` may list several
`tp:entryPointDocument` elements and "the combined set of URLs provided will
be used for the starting point". A package may declare many entry points, and
they are different DTSs: the KvK 2025 package declares five (three
annual-report entry points by accounting basis, plus `kvk-cor` and `kvk-all`
for browsing); the FRC suite has one per accounting framework; the ÅRL package
declares 24. Nothing in a schema marks it as an entry point (XBRL
International's own guidance: "entry points are through any .xsd file with no
specific distinction; however, all .xsd files are not entry points"), so the
manifest is the only place the list exists.

**Core, module, extension** are architecture conventions, not spec terms.
XBRL International publishes no normative definition of "module" or "core
schema". The usage this skill follows: a *core* schema declares the shared
concept set (`full_ifrs-cor`, `frc-core`, `bw2-titel9-cor`, `fsa`); a *module*
is a schema a core imports or an entry point assembles; an *extension* is the
filer's own schema, which imports the regulator's entry point. XBRL
International's Taxonomy Guidance Document distinguishes three extension
regimes, and the regimes in this skill span all three: no extensions (FRC,
classic NT, ÅRL), limited extensions, unrestricted extensions (ESEF, KvK iXBRL,
SEC).

**A taxonomy package** (Taxonomy Packages 1.0 section 3.1) is a zip with one
top-level directory containing `META-INF/taxonomyPackage.xml` (required) and
optionally `META-INF/catalog.xml`. The manifest carries `tp:identifier`,
`tp:version`, `tp:publicationDate`, the entry points, and optionally a
`tp:versioningReport`.

**The catalog is what makes a DTS resolve offline.** `catalog.xml` is an OASIS
XML Catalog restricted to `rewriteURI` entries; "if you are about to fetch this
remote URI, use this local file instead". Three rules decide whether a rewrite
applies:

1. **Longest matching `uriStartString` wins** (XML Catalogs 1.1 section 7.2.2).
   A package can remap a whole release directory and carve out one
   subdirectory with a longer entry.
2. **Relative `rewritePrefix` values resolve against the catalog's own
   location**, which is inside `META-INF`, so they "will typically need to
   start with `../`" (Taxonomy Packages section 3.3.1 note).
3. **In a report package, remappings apply only if the package is also a
   taxonomy package.** Report Packages 1.0 section 6 (Remappings): "If there is no
   `META-INF/taxonomyPackage.xml` file then `META-INF/catalog.xml` is
   ignored." An `.xbri` that carries a catalog and no manifest resolves
   nothing locally, and that is specified behaviour.

Some regimes make the catalog the *only* route. Every Danish instance must
start its `schemaRef` with `http://archprod.service.eogs.dk/taxonomy/` (ERST
rule `TH01`), and that host returns 404 for every path: the namespace is an
identifier, the package is the distribution. The NT namespaces on
`nltaxonomie.nl` do resolve, but the skill's own experience is that remote
fetches there are a recurring source of flaky validation; pass the packages.

**Versioning reports are authored, not computed.** XBRL Versioning 1.0 defines
"an XML syntax for an XBRL Versioning Report" documenting "the differences
between two DTSs, the From DTS and the To DTS". The Foundation publishes them;
ESMA and the SEC do not require filers to consume them; ERST publishes a
machine diff zip per release instead. The versioning primer's own limit: "it is
not possible in general to reliably reproduce the To DTS given the From DTS and
a Versioning Report". Use one as a reading aid for what changed, never as the
ground truth of either DTS.

## Nodes: what a DTS declares

**Concepts.** A concept is a global `xs:element` whose substitution-group
chain reaches `xbrli:item` or `xbrli:tuple` (XBRL 2.1 section 5.1.1), or
`xbrldt:hypercubeItem` / `xbrldt:dimensionItem` (XDT). Decide membership by
walking the chain, never by the literal attribute: the NT interposes
`sbr:presentationItem` and similar groups, and an element whose chain goes
nowhere is a schema helper, not a concept. The attributes that decide tagging:

| Attribute | Decides | Notes |
|---|---|---|
| `type` | the value space and the item-type bucket (monetary, shares, pure, decimal, string, textBlock, date, boolean, domain, enumeration) | regimes add their own types: FRC `headingItemType` / `guidanceItemType` / `groupingItemType`, ÅRL `cvrItemType` / `LegalEntityIdentifierItemType`; the profiler reports those under their own name |
| `xbrli:periodType` | `instant` or `duration`; the context the fact must carry | concept-driven, never document-driven (`first-principles.md` section 3) |
| `xbrli:balance` | `debit` or `credit` on monetary concepts; the sign convention every calculation consumer applies | the FRC suite states that the label, not the balance, decides sign (its design document, section 12.4); read the regime file before assuming |
| `abstract="true"` | a heading or grouping node that can never carry a fact | ESEF: never anchor to one |
| `nillable` | whether `xsi:nil="true"` is allowed on the fact | SBR forbids nil on facts by filing rule regardless |
| `xbrldt:typedDomainRef` | marks a dimension as typed and names its domain element | explicit dimensions have no such attribute and take members from `domain-member` arcs |

**Role types and arcrole types** (sections 5.1.3 and 5.1.4) declare the
extended link roles (ELRs) and custom arcroles a DTS may use, each with
`link:usedOn` naming the elements they may appear on and, for arcroles, the
required `cyclesAllowed`. The ELR is how a taxonomy partitions its networks by
the part of a financial statement they relate to (the idiom XBRL 2.1
illustrates in section 5.2.3, Example 47).

**Resources** carry content rather than point at it: `link:label` (with
`xml:lang` and a role), `link:reference` (with parts such as `ref:Name`,
`ref:Number`, `ref:Paragraph`, `ref:IssueDate`, or regime-specific parts like
the FRC's `Schedule` and `HomeCountry` or ÅRL's `Publisher` and `Clause`), and
the generic-link resources of formula and generic labels.

## Edges: the networks

A linkbase is a directed graph (`structure.md` § Mental model): locators and
resources are nodes, arcs are edges labelled by `xlink:arcrole`, extended links
group them under an ELR. The five standard linkbases and the generic layer
differ in what their edges mean.

**Presentation** (`parent-child`). Parent to child, ordered by `@order`; the
root of each ELR's tree is the locator that is never a target. `@preferredLabel`
on the arc selects the label role for that position: the same concept renders
as "Cash at beginning of period" under `periodStartLabel` in one row and
"Cash at end of period" under `periodEndLabel` in another. A `@use="prohibited"`
arc removes an inherited relationship; `@priority` decides between competing
arcs. A presentation locator "MUST only point to Concepts" (section 5.2.4.1),
which is why the tree is pure concept structure. Depth varies by regime:
eleven levels in IFRS 2025 and FRC 2026, nine in ÅRL, and two in the KvK
NL-GAAP entry point, whose statement trees are built by the filer's extension.

**Calculation** (`summation-item`). Parent to child with `@weight` of `1` or
`-1`. Two arcrole URIs exist and they are different specifications:
`http://www.xbrl.org/2003/arcrole/summation-item` is Calc 1.0 (XBRL 2.1
section 5.2.5) and `https://xbrl.org/2023/arcrole/summation-item` is Calc 1.1,
declared through an `arcroleRef` to `calculation-1.1.xsd`. IFRS 2025 carries
only the 1.1 arcrole (1 312 arcs); ESEF 2019 through 2022 are Calc 1.0, ESEF
2024 and 2025 are Calc 1.1. Two regimes ship **no calculation linkbase at all**:
the FRC suite (its design document says why) and the ÅRL taxonomy, which
enforces arithmetic with XBRL Formula value assertions carrying Assertion
Severity. A reviewer who expects `xbrl.5.2.5.2` inconsistencies from those
DTSs will see none and learn nothing; the arithmetic check lives elsewhere.

**Definition.** Standard arcroles (`general-special`, `essence-alias`,
`requires-element`, `similar-tuples`) are rare in practice. The definition
linkbase is where XBRL Dimensions lives: `all` / `notAll` from a primary item
to a hypercube, `hypercube-dimension`, `dimension-domain`, `domain-member`
(recursive), `dimension-default`. Two things about this layer are routinely
mis-modelled:

- **A dimensional relationship set is not confined to one ELR.**
  `@xbrldt:targetRole` on an arc continues the set in another extended link
  role (XDT section 2.4, partitioning of a dimensional relationship set
  across base sets). The ÅRL 20251001 entry point has 353 such arcs and
  the FRC 2026 FRS 102 entry point 2 356; bucketing hypercubes per ELR
  under-reports their reach in both.
- **Regimes add arcroles of their own.** ESEF anchoring is a definition arc
  with the ESMA `wider-narrower` arcrole (exact URIs in `esef.md` § Anchoring);
  the FRC declares `…/general/types/arcroles/inflow`, `/outflow` and
  `/crossref`, used 168, 102 and 100 times in its core, which carry cash-flow
  direction and cross-reference information a standard processor ignores.

**Label** (`concept-label`) and **reference** (`concept-reference`). Concept
to resource. The pair that identifies a label is (role, `xml:lang`), and in
some regimes (ELR, role, lang): ÅRL gives a concept a *different* label per
statement through ELR-shaped custom roles such as
`http://xbrl.dcca.dk/role/400.00/BalanceSheetAccountForm`.

**Generic links** (`gen:link`, arcrole `element-label`, role
`http://www.xbrl.org/2008/role/label`) label things that are not concepts: the
ELRs themselves (that is where "[210000] Statement of financial position"
comes from), enumeration values, and assertion messages. A resolver that walks
only `concept-label` never finds a statement name. **Formula** resources
(`valueAssertion`, `existenceAssertion`, filters, variables) also travel as
generic links; ÅRL ships 45 value assertions and 11 existence assertions in
one entry point, ESEF ships the LEI and filing-indicator assertions.

## From a fact to its concept, its label, its statement

This is the procedure the whole file exists for. Every step reads the DTS; none
guesses.

1. **QName to concept.** Expand the fact's `name` with the namespaces in scope
   (the prefix is arbitrary; the namespace URI is the identity), then find the
   global element with that namespace and local name in a schema of the DTS.
   Not found means the fact carries no concept semantics (`validation.md`
   section 6, item 26: `ix11.12.1.2:missingReferences`). The recurring
   mis-binding is picking a prefix the concept does not live under: four of the
   five Dutch statement placeholders are `bw2-titel9:`, the cash-flow one is
   `rj:` (the cash flow statement is an RJ requirement, not a statutory one),
   and two placeholders the RTS names do not exist in any published schema.
   `scripts/dts_profile.py <entry> --concept <prefix:Name>` answers this in one
   command.
2. **Concept to label.** Follow `concept-label` arcs to `link:label` resources
   and filter by (role, language). Fall back deliberately, and differently per
   regime, because role coverage is sparse: IFRS 2025 has 5 403 standard labels
   but 242 `totalLabel`, 43 `periodStartLabel` and no `verboseLabel` at all;
   the FRC has standard, documentation, verbose and terse plus two deprecation
   roles, no negated, total or period roles, with Welsh at near-parity to
   English; ÅRL has five roles, Danish authoritative and 374
   concepts with no English label; the NT ships nl, en, de, fr but
   `documentation` only in nl and en. Fall back to the standard role, then to
   the regime's authoritative language, and never to a role the DTS does not
   author.
3. **Label in a rendering context.** When the concept sits in a presentation
   tree, the arc's `preferredLabel` overrides step 2. A negated role
   (`negatedLabel`, `negatedTerseLabel`, `negatedTotalLabel`, `negatedNetLabel`,
   from the Label Role Registry) flips the *displayed* sign and leaves the fact
   unchanged (`first-principles.md` section 2).
4. **Concept to statement.** Regimes encode statement membership differently,
   and reading the wrong signal is silent:
   - **IFRS / ESEF**: the six-digit number in the ELR URI and definition
     (`[210000]` statement of financial position, `[310000]` profit or loss by
     function, `[8xxxxx]` notes, `[9xxxxx]` axes, lettered suffixes for the
     tables inside a note). Stable across vintages and between the IFRS and
     ESMA URI shapes.
   - **FRC**: a framework-suffixed role URI with a numbered definition,
     `…/roles/IncomeStatementFRS102` = "202 - Income Statement (FRS 102)"; one
     core holds every framework's ELRs and the entry point picks which
     presentation linkbases attach.
   - **KvK iXBRL**: **the ELR name means nothing** (it is under the filer's
     domain); what is normative is the *root element* of each presentation ELR,
     fixed by RTS Annex IV (`bw2-titel9:BalanceSheetTitle`,
     `rj:CashFlowStatementTitle`, `ifrs-full:StatementOfFinancialPositionAbstract`
     and so on). Read the root, never the name.
   - **ÅRL**: numbered role URIs (`…/role/400.00/BalanceSheetAccountForm`) and
     label roles shaped like them, so the same concept reads differently in
     the credit-institution and insurance balance sheets.
5. **Concept to arithmetic and dimensions.** Calculation parents and weights
   come from the `summation-item` arcs of the DTS's calculation base sets,
   which are separate from the presentation base sets and need not share a
   role URI with the network being rendered; the presentation ELR is
   rendering context only. Dimensional validity comes from the hypercube
   reachable through `all` / `notAll` from the primary item, followed
   across `targetRole`. Where a regime has no
   calculation linkbase, the arithmetic is in formula assertions or nowhere.

## Six DTSs compared, measured

Measured 2026-08-21 with `scripts/dts_profile.py`, infrastructure boundary not
followed, and cross-checked against Arelle 2.41.7 loading the same entry point
with the same packages: concepts by substitution root, abstracts, presentation
arcs and networks, calculation arcs, every XDT arcrole, labels and references
agreed exactly on IFRS, US-GAAP, FRC and ÅRL, and on NL and ESEF differed by
one concept (the LEI element hosted on `xbrl.org`, behind the boundary). The
US-GAAP row is the standard entry point and was fetched live; the others were
read from the regulators' packages.

| Measure | IFRS 2025 full | ESEF 2024 `esef_cor` | US-GAAP 2025 std | FRC 2026 FRS 102 | KvK 2025 NL-GAAP ext | ÅRL 20251001 account form by nature |
|---|---|---|---|---|---|---|
| Documents in closure | 332 (51 schemas, 281 linkbases) | 50 (4 + 46) | 407 (126 + 281) | 56 (15 + 41) | 68 (7 + 61) | 119 (12 + 107) |
| Concepts (items / dimensions / hypercubes) | 5 512 (5 217 / 144 / 151) | 5 338 (5 053 / 139 / 146) | 18 647 (17 977 / 293 / 377) | 7 995 (7 651 / 158 / 186) | 6 735 (6 459 / 271 / 5) | 4 087 (3 907 / 84 / 96) |
| Abstract concepts | 1 654 | 1 585 | 6 327 | 3 744 | 951 | 764 |
| Typed dimensions | 0 | 0 | 10 | 27 | 175 | 56 |
| Presentation networks / arcs / max depth | 68 / 6 605 / 11 | 0 (relationships live in `esef_all`) | 111 / 33 585 / 17 | 15 / 7 295 / 11 | 1 / 11 / 2 | 23 / 2 807 / 9 |
| Calculation arcs (arcrole) | 1 312 (Calc 1.1) | 0 | 6 526 (Calc 1.1) | **0 (none shipped)** | 0 (filer builds them) | **0 (formula instead)** |
| Definition arcs (prohibited excluded) / with `targetRole` | 4 245 / 0 | 7 683 / 0 | 31 960 / 0 | 12 506 / 2 356 (+39 prohibited) | 5 803 / 0 | 3 015 / 353 |
| Non-XDT definition arcroles | none | none | six deprecation arcroles (`dep-concept-deprecatedConcept` 134, `dep-dimensionallyQualifiedConcept-deprecatedConcept` 397, …), `essence-alias` 9 | `inflow` 168, `outflow` 102, `crossref` 100 | none | none |
| Label resources / distinct roles / languages | 11 293 / 11 / en | 11 171 / 11 / en (24 languages via the package entry points) | 19 575 / 6 / en-US (no `documentation`: that and the references ship only in the `-all` entry point) | 17 108 / 6 / en, cy | 44 122 / 11 / nl, en, fr, de | 9 155 / 43 (5 standard plus 38 ELR-shaped) / da, en |
| Reference resources | 7 527 | 5 892 | 0 in `std` (in `-all` only) | 7 513 | 12 020 | 2 452 |
| Generic extended links / formula resources | 80 / 0 | 9 / 442 | 0 / 0 | 0 / 0 | 29 / 47 | 53 / 268 (45 value + 11 existence assertions, 143 fact variables) |
| Role types declared | 204 | 23 | 665 | 418 | 9 | 384 |
| Extension policy | open (Foundation's "Essential" entry points exist to be extended) | open, anchoring required | open, anchoring not required | **closed**: widen and disclose, analysis dimensions | open, anchoring required | **closed** for ÅRL; extensions only on the IFRS/ESEF companion |
| Release cadence, version token | annual, namespace date `YYYY-MM-DD` (2025-03-27); **no 2026 release** | per RTS amendment, namespace date; ESEF 2024 (Reg (EU) 2025/19) for FY2025, ESEF 2025 (Reg (EU) 2026/283) from FY2026, early application for FY2025 allowed | annual GRT, `YYYY` in namespace | annual suite, `YYYY-01-01` | annual KvK set, `YYYY-12-31`; classic NT `ntNN/YYYYMMDD` | annual, `YYYY1001`; package on `erhvervsstyrelsen.dk` |

Note on US-GAAP: the `std` entry point (`us-gaap-entryPoint-std-2025.xsd`)
was fetched live from `xbrl.fasb.org` and `xbrl.sec.gov` (403 + 4 documents)
and deliberately omits documentation labels, references and the deprecated
elements; `us-gaap-entryPoint-all-2025.xsd` carries them. Profile the one you
actually load, and say which. The SEC state/province schema (`stpr`, 65
concepts) enters this closure only through locators in a linkbase
**embedded** in `us-gaap-2025.xsd`; a walk that reads embedded linkbases but
does not follow their locators misses it, which is how this table's first
draft read 65 short of Arelle.

What the numbers mean for tagging:

- **Depth and presentation ownership differ by an order of magnitude.** IFRS,
  FRC and ÅRL ship the statement trees; the KvK NL-GAAP entry point ships one
  eleven-arc, two-level network and expects the filer's extension to build
  every statement under the RTS root elements. The NT also carries 175 typed
  dimensions against none in IFRS or ESEF, so its dimensional contexts are
  built from typed members far more often. A conversion pipeline that "reuses the
  taxonomy's presentation" has nothing to reuse in the Dutch iXBRL tree.
- **Where arithmetic lives is regime-specific.** IFRS and ESEF 2024+ use Calc
  1.1; the FRC has no calculation linkbase and decides sign by label; ÅRL
  enforces sums by formula. Calc 1.0 vs 1.1 is an arcrole URI, visible in the
  profile, and decides how duplicate facts and rounding are judged
  (`validation.md` section 4).
- **Dimensions are the substrate everywhere, but their reach is encoded
  differently.** FRC and ÅRL rely heavily on `targetRole`; IFRS, ESEF and NL
  do not use it at all. A profiler or mapper that ignores it is correct on
  three regimes and wrong on two.
- **Languages are an entry-point or package property, not a flag.** ESEF's 24
  languages arrive through per-language entry points in the package; loading
  `esef_cor.xsd` bare yields English only. Welsh and Danish are first-class in
  their regimes and a hard-coded `en` silently mislabels a filing.
- **Closed taxonomies push entity-specific lines into dimensions and
  disclosure**, not into extension concepts, which changes what "the right
  concept" means: in the FRC suite the right answer to a line the taxonomy
  lacks is the nearest wider concept plus an analysis dimension, never a new
  element.

## Bi-temporal: valid time and acceptance window

A DTS has two clocks, and a review that conflates them calls correct filings
defective.

- **Valid time** is the set of financial years a release is *for*. It is set
  by the instrument that binds the release: an EU delegated regulation for
  ESEF ("financial years beginning on or after 1 January 2025" for ESEF 2024,
  Reg (EU) 2025/19 article 2; on or after 1 January 2026 for ESEF 2025, Reg
  (EU) 2026/283, with early application for FY2025), the RTS for KvK, the
  suite's accounting-standard versions for the FRC, the yearly release for
  ÅRL, the FASB release for US-GAAP.
- **Acceptance window** (transaction time) is the deposit-date interval in
  which the receiver takes a report built on that release. It is set by the
  receiver and is usually wider than valid time: KvK accepts "any of the three
  most recent KVK taxonomy versions" and explicitly allows "this year's report
  using last year's taxonomy, or this year's taxonomy for last year's report";
  Companies House accepts the 2022 to 2026 FRC suites from April 2026 while
  HMRC retires each suite by accounting-period end; ERST *recommends* the 2025
  or 2024 taxonomy and ships embedded controls for six vintages back to
  20201001; ESMA lets each new ESEF version be applied early by derogation.

Three consequences:

1. **Pin both dates before judging a report.** The financial year from
   `<xbrli:period>` selects the rule edition; the intended deposit date selects
   what the receiver will accept. `SKILL.md` step 2 says to ask for the deposit
   date; this file says where the answer is looked up: the *DTS and vintages*
   table in the jurisdiction file.
2. **The release is identified by its namespace date, not by its marketing
   name.** "ESEF 2024" has namespace date `2024-03-27` and is mandated by a
   regulation numbered 2025/19; "KVK taxonomy 2025" is `2025-12-31`; the FRC
   "2026 suite" is `2026-01-01`; ÅRL "2025" is `20251001`. Quote the namespace
   date from the report's `schemaRef`, and the instrument that binds it, or
   quote nothing.
3. **The controls applied to a vintage can move after publication.** ERST
   back-ports its current formula package (`frm_injection/`) into older
   vintages, so a 2022-vintage filing is validated at the receiver against
   2025 controls; the FRC's "latest and penultimate" use policy is stricter
   than either receiver's acceptance table. A validation run is reproducible
   only with its packages and cache recorded (`SKILL.md`, "A validation result
   is only reproducible with the inputs that produced it").

Per-regime tables with links, valid time, acceptance window and status, all in
one vocabulary (next section but one): `jurisdictions/nl-sbr.md`,
`jurisdictions/uk-frc.md`, `jurisdictions/dk-erst.md`,
`jurisdictions/sec-edgar.md`, `jurisdictions/fi-prh.md`,
`jurisdictions/be-nbb.md`, `jurisdictions/de-hgb.md`, and for IFRS and ESEF
`esef.md` § DTS and vintages.

## Working with `scripts/dts_profile.py`

The script walks the closure with lxml only and the same parsing logic
offline and online; what differs between runs is the inputs (packages,
cache, network), which decide the closure and the unresolved list, so pin
them for a reproducible profile. It never validates: Arelle validates,
this describes. Three
commands cover most questions.

**Profile an entry point from the regulator's packages (offline, reproducible):**

```bash
python3 scripts/dts_profile.py \
  https://www.nltaxonomie.nl/kvk/2025-12-31/kvk-annual-report-nlgaap-ext.xsd \
  --package kvk-2025_taxonomie.zip --package bw2-titel9_taxonomie.zip \
  --package rj-2025_taxonomie.zip --package ncgc-2022_taxonomie.zip \
  --package wnt-2025_taxonomie.zip --package ww-2025_taxonomie.zip \
  --offline
```

Expect a Markdown report with sections Documents, Discovery pointers,
Concepts, Role and arcrole types, Presentation, Calculation, Definition and
dimensions, Labels, References, Generic links, and the deepest presentation
networks. Exit code `0` means every discovered document resolved; `1` means the
profile was produced but lists at least one `UNRESOLVED` document or locator;
`2` is a usage error. `--json` gives the same data as a machine-readable
object, which is how two releases are diffed.

**Answer "what is concept X" from the DTS, not from memory:**

```bash
python3 scripts/dts_profile.py <entry-point-or-package> --concept ifrs-full:Revenue
```

Prints the declaration (type, period, balance, substitution chain), every label
by role and language, every reference with its parts, and the concept's
presentation, calculation and definition edges per ELR with their attributes.
The prefix is resolved through the prefix each schema declares for its own
namespace; `{namespace}Local` and a bare unique local name also work.

**Start from a package, an instance or an Inline XBRL document:**

```bash
python3 scripts/dts_profile.py XBRL20251001-20251120.zip \
  --entry-point entryDanishGAAPBalanceSheetAccountFormIncomeStatementByNature --offline
python3 scripts/dts_profile.py report.xbri            # reports/ inside the package are the starts
python3 scripts/dts_profile.py filing.xhtml           # follows ix:references/link:schemaRef
```

A package that declares several entry points is refused without
`--entry-point`, and the refusal lists them: merging them silently would
profile a DTS nobody files against.

Reading the output:

- `Boundary (infrastructure, not followed)` lists the `xbrl.org` / `w3.org`
  schemas (instance, linkbase, XDT, DTR, LRR, generic links). They carry no
  reporting concepts; `--follow-infrastructure` walks them if you must. The
  one reporting concept that lives there is the LEI taxonomy's element, which
  is why an ESEF or NL profile reads one concept short of Arelle.
- `Unresolved locators` is broken down by cause. "non-concept id" is normal:
  generic labels point at role types. "XPointer child-sequence form" is a
  limit of this tool (it resolves shorthand and `element(id)` pointers only,
  not `element(/1/14)`). "document not in the closure" and "id not declared"
  are findings about the taxonomy.
- `by_source` tells you whether bytes came from a package, the disk cache or
  the network. Record it beside any number you cite; the cache is an input.

## Gotchas that cost real filings

- **A namespace is not a download location.** ÅRL's host 404s by design;
  `nltaxonomie.nl` flakes; `xbrl.ifrs.org` disables directory listing. Resolve
  through packages, and treat a fetch failure as "unresolved", never as "not in
  the DTS".
- **`esef_cor.xsd` has concepts, `esef_all.xsd` (2017 to 2024) or
  `esef_ias_1.xsd` / `esef_ifrs_18.xsd` (2025) have the relationships.** A
  profile or a viewer built on the filer entry point alone shows zero
  presentation networks, which is correct and surprising.
- **The third KvK entry point changed name between vintages:**
  `kvk-annual-report-other-gaap.xsd` (2024-12-31) became
  `kvk-annual-report-other.xsd` (2025-12-31), and both vintages are accepted at
  once. Constants keyed on one name are wrong for the other year.
- **`kvk:LegalEntitySize` is a fact, not an entry-point selector.** All four
  official size-class example packages import the same
  `kvk-annual-report-nlgaap-ext.xsd`; size-specific `kvk-rpt-jaarverantwoording-*`
  entry points belong to the classic NT tree only.
- **Two RTS placeholders do not exist.** `bw2-titel9:ManagementReportTitle` and
  `bw2-titel9:OtherInformationTitle` are named in RTS Annex IV (2025 and 2026)
  and declared in no published schema. Resolve every QName against the DTS
  before emitting it.
- **"Version 2026" may be documented before it is published, and a
  regulation may be in force before the publisher's page says so.** RTS 2026
  and RM 2026 name `kvk/2026-12-31/` URLs that returned 404 on 2026-08-21;
  NT21 had alfa and bèta directories but no final one; the IFRS Foundation
  issued no 2026 taxonomy. In the other direction, ESMA's April 2026 notice
  that it "does not plan to amend the ESEF RTS or taxonomy in 2026" reads as
  if ESEF 2025 were unmandated, while Reg (EU) 2026/283 (adopted 12 December
  2025, OJ 18 March 2026) already binds it from FY2026. A documented
  namespace is a promise; a 200 on the entry point, and the OJ, are the
  facts.
- **Calc 1.0 and Calc 1.1 are different arcroles.** A processor checking
  only the other arcrole reports no inconsistencies, which reads as a pass
  and is nothing of the kind. The arcrole URI in the profile tells you which
  you have; IFRS 2025, ESEF 2024+ and US-GAAP 2025 are 1.1.
- **A `.xbri` catalog without a manifest is inert** (Report Packages section
  6). If offline resolution "does not work", check for
  `META-INF/taxonomyPackage.xml` before anything else.
- **TLS on a bare Python.** python.org macOS builds ship no CA bundle; the
  profiler says so and names the fix (`certifi`, `SSL_CERT_FILE`, or
  `--package` / `--offline`). Arelle's own fetches have the same dependency.

## Vocabulary used by every jurisdiction table

One term per concept, so the tables are comparable across regimes:

| Term | Meaning | Not to be confused with |
|---|---|---|
| **Release** | one published taxonomy set, identified by its namespace date or version token (`2024-03-27`, `2026-01-01`, `20251001`, `nt20/20251210`) | the marketing name ("ESEF 2024", "2026 suite") or the regulation number |
| **Entry point** | the set of URLs that starts discovery for one DTS (Taxonomy Packages section 3.2.2) | the core schema; the package |
| **Package** | the taxonomy-package zip with its manifest and catalog | a report package (`.xbri`) |
| **Valid time** | the financial years the release is made for, and the instrument that says so | the publication date |
| **Accepted at deposit** | the interval of deposit dates in which the receiver accepts a report on this release, and the rule that says so | valid time; the publisher's "current" label |
| **Status** (on the table's verification date) | `current`, `accepted`, `pre-release`, `published, not mandated`, `superseded`, `retired`, `not yet published` | |

Column order for every *DTS and vintages* table: Release, Entry point(s),
Package, Valid time, Accepted at deposit, Status, Source. A claim without a
primary source in the last column is a gap to fill, not a row to keep.

## Sources

All fetched 2026-08-21.

- XBRL 2.1 REC 2003-12-31 with corrected errata 2013-02-20: https://www.xbrl.org/Specification/XBRL-2.1/REC-2003-12-31/XBRL-2.1-REC-2003-12-31+corrected-errata-2013-02-20.html (DTS definition section 1.4; discovery rules section 3.2; schemaRef and linkbaseRef sections 4.2 and 4.3; roleRef / arcroleRef in instances 4.4 and 4.5; concept definitions 5.1.1; roleType 5.1.3; arcroleType 5.1.4; redefine 5.1.5; linkbases 5.2; presentation locators 5.2.4.1; calculation 5.2.5)
- XBRL Dimensions 1.0 REC 2006-09-18 with corrected errata 2012-01-25: https://www.xbrl.org/specification/dimensions/rec-2012-01-25/dimensions-rec-2006-09-18+corrected-errata-2012-01-25.html (terminology section 1.3; targetRole section 2.4; typedDomainRef 2.5.2)
- Taxonomy Packages 1.0 REC 2016-04-19: https://www.xbrl.org/Specification/taxonomy-package/REC-2016-04-19/taxonomy-package-REC-2016-04-19.html (layout 3.1; entry points 3.2.2; versioning report 3.2.4.1; catalog 3.3)
- Report Packages 1.0 REC 2023-09-22 with corrected errata 2025-03-11: https://www.xbrl.org/Specification/report-package/REC-2023-09-22+corrected-errata-2025-03-11/report-package-REC-2023-09-22+corrected-errata-2025-03-11.html (remappings section 6)
- XBRL Versioning 1.0 Base REC 2013-02-27: https://www.xbrl.org/specification/versioning-base/rec-2013-02-27/versioning-base-rec-2013-02-27.html ; Versioning Primer 1.0 PWD 2011-10-19 (the "not possible in general to reliably reproduce the To DTS" limit): https://www.xbrl.org/WGN/versioning-primer/PWD-2011-10-19/versioning-primer-WGN-PWD-2011-10-19.html
- Calculations 1.1 arcrole schema: https://www.xbrl.org/2023/calculation-1.1.xsd
- XML Catalogs 1.1 (OASIS, 2005), rewrite entries section 7.2.2: https://www.oasis-open.org/committees/download.php/14809/xml-catalogs.html
- XBRL International guidance: taxonomy publication and packages https://www.xbrl.org/guidance/taxonomy-publication/ ; https://www.xbrl.org/guidance/taxonomy-packages/ ; taxonomy reuse https://www.xbrl.org/guidance/taxonomy-reuse/ ; XBRL Taxonomy Guidance Document v1.2 https://www.xbrl.org/guidance-files/XBRLTaxonomyGuidanceDocument-v1.2.pdf
- Arelle (Apache-2.0), the cross-check processor: https://github.com/Arelle/Arelle
- IFRS Foundation, "Using the IFRS digital taxonomies: the taxonomy architecture" (2026 edition) and the 2025 release page: https://www.ifrs.org/issued-standards/ifrs-taxonomy/
- ESMA ESEF taxonomy landing page and ESEF 2025 documentation: https://www.esma.europa.eu/issuer-disclosure/european-single-electronic-format ; Reg (EU) 2025/19 on EUR-Lex
- FRC, "XBRL Tagging Guide – FRC Taxonomies 2026" v13.0 and the FRC taxonomy design document; entry points under https://xbrl.frc.org.uk/
- SBR Handelsregister: RTS 2025 / 2026, Reporting Manual 2026, FAQ 2026-07-10, all at https://www.sbr-nl.nl/sbr-domeinen/handelsregister ; schemas under https://www.nltaxonomie.nl/
- Erhvervsstyrelsen ÅRL taxonomy 20251001 package: https://erhvervsstyrelsen.dk/sites/default/files/2025-11/XBRL20251001-20251120.zip ; Kontroller corpus (rules TH01, FR83)
- FASB US-GAAP Financial Reporting Taxonomy 2025: https://xbrl.fasb.org/us-gaap/2025/

> Items not freshly fetched in this run and stated on the authority of the
> jurisdiction files: the exact ESEF `wider-narrower` arcrole URIs (`esef.md`),
> the Label Role Registry roles (`registries.md`), SBR's nil and footnote
> filing rules (`jurisdictions/nl-sbr.md`).
