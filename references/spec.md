# Inline XBRL 1.1 + XBRL 2.1 Reference

Inline XBRL embeds XBRL facts inside an XHTML host document — one file serves both the human reader and the structured-data consumer.

## ix:* elements

| Element | Purpose | Key attributes |
|---|---|---|
| `ix:header` | Container for non-rendered XBRL infrastructure. One per Inline XBRL document set target. Holds `ix:hidden`, `ix:references`, `ix:resources`. | `target` |
| `ix:references` | Wraps `link:schemaRef` / `link:linkbaseRef` pointing to the DTS. | `id`, `target` |
| `ix:resources` | Holds `xbrli:context`, `xbrli:unit`, `link:roleRef`, `link:arcroleRef`, footnote linkbase resources. | — |
| `ix:hidden` | Facts that must exist in XBRL but aren't visibly rendered (e.g., DEI cover-page facts). Children: `ix:nonFraction`, `ix:nonNumeric`, `ix:fraction`, `ix:tuple`. | — |
| `ix:nonFraction` | Numeric fact with single value. | `name`, `contextRef`, `unitRef`, `decimals` or `precision`, `scale`, `sign`, `format`, `target`, `tupleRef`, `order`, `id`, `nil` |
| `ix:nonNumeric` | Non-numeric fact (string, date, boolean, anyURI, QName). | `name`, `contextRef`, `format`, `escape`, `continuedAt`, `target`, `tupleRef`, `order`, `id`, `nil` |
| `ix:fraction` | Fraction-typed numeric fact. Exactly one `ix:numerator`, one `ix:denominator`. | `name`, `contextRef`, `unitRef`, `target`, `tupleRef`, `order`, `id`, `nil` |
| `ix:numerator` / `ix:denominator` | Children of `ix:fraction`. | `format`, `scale`, `sign`, `nil` |
| `ix:continuation` | Tail segment of a fact whose visible content spans non-contiguous DOM regions. | `id`, `continuedAt` |
| `ix:exclude` | Removes its sub-tree from the fact value (e.g., remove a footnote marker from inside a tagged paragraph). | — |
| `ix:footnote` | Inline-rendered footnote resource. | `id`, `footnoteRole`, `xml:lang`, `continuedAt` |
| `ix:relationship` | Declares fact-to-footnote (or fact-to-fact) arcs. | `arcrole`, `linkRole`, `fromRefs`, `toRefs`, `order` |
| `ix:tuple` | Inline tuple parent grouping ordered child facts. | `name`, `tupleID`, `tupleRef`, `order`, `target` |

## Key fact attributes

- `contextRef` — IDREF to `xbrli:context` (entity + period + dimensions). Required on every fact.
- `unitRef` — IDREF to `xbrli:unit`. Required on numeric facts.
- `decimals` — Reported precision as decimal places (positive: digits after decimal; negative: rounding scale, e.g., `-3` = thousands; `INF` = exact).
- `precision` — Significant digits. Mutually exclusive with `decimals` on the same fact.
- `scale` — Inline-only multiplier as a power of 10 applied to the rendered text before producing the canonical XBRL value. E.g., `scale="3"` on rendered "1,234" yields fact `1234000`.
- `sign` — `-` to negate the parsed value (Inline-only; pairs with parentheses formatting in HTML).
- `format` — QName of a TRR transform (e.g., `ixt:numdotdecimal`) that converts rendered text to canonical XBRL lexical form.
- `escape` — On `ix:nonNumeric`: `true` keeps inner XHTML markup as part of the fact value; `false` (default) takes text content only.
- `continuedAt` — IDREF chain pointer to the next `ix:continuation` (or `ix:footnote`) segment.
- `target` — Names an output document target so a single Inline document can produce multiple XBRL reports.

## decimals vs precision

`decimals` counts digits relative to the decimal point (negative for rounding to thousands/millions); `precision` counts significant digits regardless of magnitude. XBRL 2.1 §4.6.3–4.6.4 makes them mutually exclusive on a single fact.

**Exactly one of `decimals` or `precision` is required on every non-nil numeric fact.** Nil-valued facts (`xsi:nil="true"`) must omit both. SEC EDGAR and Dutch SBR require `decimals`, forbid `precision`, and forbid `decimals="INF"`.

## Transformation Registry (TRR 4)

The Transformation Registry defines named transformations (QNames in the `ixt` namespace) that Inline XBRL processors apply to rendered text to derive canonical XBRL lexical values — handling locale formatting, date orderings, sign conventions, boolean text.

**TRR 4** is the current registered version (Recommendation, namespace `http://www.xbrl.org/inlineXBRL/transformation/2022-02-16`).

Categories and representative names:

- **Numbers**: `ixt:numdotdecimal`, `ixt:numcommadecimal`, `ixt:num-dot-decimal-apos`, `ixt:numdotdecimalin`, `ixt:numunitdecimal`, `ixt:zerodash`, `ixt:nocontent`, `ixt:fixed-zero`, `ixt:fixed-empty`.
- **Dates**: `ixt:datedaymonthyear`, `ixt:datemonthdayyear`, `ixt:dateyearmonthday`, `ixt:datedaymonthyearen`, `ixt:datemonthyear`, `ixt:dateyearmonth`, `ixt:dateerayearmonthdayjp`.
- **Booleans**: `ixt:booleanfalse`, `ixt:booleantrue`.

Example:

```xml
<ix:nonFraction name="us-gaap:Revenues" contextRef="c1" unitRef="usd"
                decimals="-3" format="ixt:numdotdecimal" scale="3">1,234</ix:nonFraction>
```

Produces canonical fact value `1234000`.

## XBRL 2.1 contexts

`xbrli:context` carries the dimensional anchor for facts (XBRL 2.1 §4.7).

- `entity` — Required `<xbrli:identifier scheme="...">value</xbrli:identifier>`. The `scheme` is an absolute URI naming the identifier authority (e.g., LEI scheme, SEC CIK URL); the body is the entity's identifier within that scheme.
- `period` — Exactly one of:
  - `<xbrli:instant>YYYY-MM-DD</xbrli:instant>` (point in time, e.g., balance-sheet date),
  - `<xbrli:startDate>…</xbrli:startDate><xbrli:endDate>…</xbrli:endDate>` (duration, for flow concepts),
  - `<xbrli:forever/>` (no temporal bound).
- `scenario` — Optional. Reporting scenario context (budget vs. actual). Used by XDT for typed/explicit dimension members on flow-type concepts.
- `segment` — Optional. Entity sub-classification (business unit, geography). Used by XDT for dimensions tied to the reporting entity itself.

## XBRL 2.1 units

`xbrli:unit` declares the measurement (XBRL 2.1 §4.8).

- **Single measure**: `<xbrli:measure>iso4217:EUR</xbrli:measure>` — one QName from a measure namespace. Monetary facts must use ISO 4217 currency codes via the `iso4217` namespace (`iso4217:EUR`, `iso4217:USD`). Pure-number ratios use `xbrli:pure`; share counts use `xbrli:shares`.
- **Divide**: composite units like EUR/share — `iso4217:EUR` ÷ `xbrli:shares`.

```xml
<xbrli:unit id="usdPerShare">
  <xbrli:divide>
    <xbrli:unitNumerator><xbrli:measure>iso4217:USD</xbrli:measure></xbrli:unitNumerator>
    <xbrli:unitDenominator><xbrli:measure>xbrli:shares</xbrli:measure></xbrli:unitDenominator>
  </xbrli:divide>
</xbrli:unit>
```

Numeric concepts of `monetaryItemType` MUST use a unit whose single
measure is in the `iso4217` namespace.

## XBRL Dimensions (XDT)

XDT layers analytical axes onto XBRL 2.1 contexts (XDT §1–§3).

- **Hypercubes** (`xbrldt:hypercubeItem`) bundle a set of dimension axes that constrain a primary item. Linked from the definition linkbase via `hypercube-dimension`, `domain-member`, `dimension-domain`, `dimension-default` arcroles.
- **Explicit dimensions** — Axis whose members are pre-enumerated `xbrli:item` domain members; carried as `<xbrldi:explicitMember dimension="qn">qn:Member</xbrldi:explicitMember>`.
- **Typed dimensions** — Axis whose member values are open-ended XML simple types (e.g., property IDs); carried as `<xbrldi:typedMember dimension="qn"><ext:Element>value</ext:Element></xbrldi:typedMember>`.
- **all vs notAll** — `xbrldt:all` arc states the primary item MUST report against the hypercube's axes; `xbrldt:notAll` excludes a sub-cube. Closed hypercubes (`@xbrldt:closed="true"`) restrict to the listed members only.
- **Default members** — A `dimension-default` arc names the implicit member when an explicit dimension is absent from the context. A fact reported without that explicit dimension is treated as if it carried the default.
- **Segment vs scenario placement** — Each dimension is bound to either `xbrli:segment` or `xbrli:scenario` via `xbrldt:contextElement` on the hypercube-dimension arc; mismatched placement is a DTS error.

## Calculation linkbase weights

Calculation arcs (XBRL 2.1 §5.2.5) use arcrole `summation-item` to assert that a parent fact equals the weighted sum of its children within the same context (matching period type, entity, dimensions). `@weight` is a non-zero decimal — typically **+1** when the child contributes with the parent's natural sign, **−1** when it reverses sign (contra accounts, deductions in subtotals).

Weights validate only when child concepts have compatible **balance** types (debit/credit). Balance assignment on `monetaryItemType` concepts drives sign convention: asset-balance child into asset-balance parent → `weight="1"`; credit-balance contra into debit-balance subtotal → `weight="-1"`.

A processor reports a **calculation inconsistency** (not an error) when the parent fact differs from the weighted sum of child facts beyond rounding implied by `decimals`/`precision`. Resolve inconsistencies before filing in regimes that mandate calc-linkbase compliance (ESEF, Dutch SBR, SEC EDGAR for primary statements).

**Calculations 1.1** (2024) clarifies behavior under dimensions and is more permissive in narrow cases. Check the target regulator's manual for the required version.

## Sources

- https://www.xbrl.org/Specification/inlineXBRL-part1/REC-2013-11-18/inlineXBRL-part1-REC-2013-11-18.html
- https://specifications.xbrl.org/work-product-index-inline-xbrl-transformation-registry-4.html
- https://www.xbrl.org/Specification/XBRL-2.1/REC-2003-12-31/XBRL-2.1-REC-2003-12-31+corrected-errata-2013-02-20.html
- https://www.xbrl.org/Specification/XDT/REC-2006-09-18/XDT-REC-2006-09-18.html
