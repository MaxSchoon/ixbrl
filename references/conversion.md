# Converting a source document to faithful iXBRL — Reference

Most iXBRL is not authored from scratch. It is *converted*: a finished
set of financial statements already exists as a PDF, a Word file, or a
layout produced by accounts-production software, and that document must
become a single XHTML file carrying XBRL facts.

Conversion is where filings quietly go wrong. A converted file can pass
every validator and still be a poor filing, because validators check
*syntax and DTS wiring*, not *whether the iXBRL faithfully represents
the financial statements a human prepared*. This reference is the
"up-close" discipline: what a reviewer who actually reads the statements
will notice, even when Arelle is silent.

## Contents

1. The fidelity contract
2. Preserve presentation hierarchy — use abstract concepts
3. Periods, dates, and column headers
4. Tagging completeness — there is no "half-tagged" statement
5. The statement of changes in equity (roll-forward matrices)
6. Calculation completeness and weight derivation
7. Label discipline — reuse, don't reinvent
8. The hidden section — what genuinely belongs there
9. What a representative filing actually contains
10. The content-level review pass (checklist)

---

## 1. The fidelity contract

The converted iXBRL has two obligations, and they are equally binding:

- **To the machine consumer** — every datum is a correctly tagged,
  correctly typed, correctly contextualised XBRL fact.
- **To the human reader** — the rendered XHTML still *is* the financial
  statements: same line items, same order, same groupings, same
  headings, same dates, same columns.

A conversion that satisfies the first and breaks the second is a defect,
even with a clean validation report. The most common failure mode is a
converter that treats the source as a flat list of numbers to be tagged
and discards everything that gave those numbers meaning — section
headings, indentation, the period a column belongs to, the date a
balance sheet was struck. Treat the source document's structure as data
to be carried across, not formatting to be normalised away.

## 2. Preserve presentation hierarchy — use abstract concepts

Financial statements are hierarchical: a statement has sections,
sections have groupings, groupings have line items, and line items roll
up into subtotals and totals. That hierarchy is information. If the
conversion flattens it — every row at the same level, no grouping — the
file loses the structure an analyst, a renderer, and the next preparer
all rely on.

The XBRL mechanism for modelling structure is the **abstract concept**.
An abstract concept (`abstract="true"` in the schema, substitution group
`xbrli:item`, conventionally `xbrli:stringItemType`) is never reported
as a fact — it carries no value. Its only job is to be a structural
parent in the **presentation linkbase**, so the presentation tree mirrors
the visual hierarchy of the statement:

```text
StatementOfFinancialPositionAbstract   (abstract — statement root)
  AssetsAbstract                       (abstract — section header)
    NonCurrentAssetsAbstract           (abstract — grouping header)
      PropertyPlantAndEquipment        (line item — a real fact)
      IntangibleAssets                 (line item — a real fact)
    NonCurrentAssets                   (subtotal — a real fact)
  ...
```

Rules of thumb:

- Every visible heading or grouping label in the source ("Fixed
  assets", "Current liabilities", "Equity attributable to owners of the
  parent") maps to an abstract concept, not to nothing.
- The presentation linkbase tree should reproduce the statement's
  indentation. If a reader could redraw the statement from your
  presentation tree, the structure survived the conversion.
- Most regimes (ESEF among them) require every tagged concept to appear
  in at least one presentation link. Building the presentation tree
  properly is not optional polish — it is part of a conformant filing.
- Abstracts are never anchored and never tagged; they are taxonomy
  structure only.

A flattened presentation linkbase is the structural equivalent of
deleting every heading from the printed accounts. It usually passes
validation. It is still wrong.

## 3. Periods, dates, and column headers

A balance sheet is struck *at a date*; an income statement covers *a
period*. Those dates are not decoration — they define the `xbrli:context`
each fact lives in, and they are themselves disclosures.

- Every column header in the source ("31 December 2025", "2024") is a
  context. Map each one before tagging; never let a date silently
  disappear because the converter only kept the numbers.
- Period type is concept-driven (see SKILL.md §3): balance-sheet
  concepts are `instant`; flow concepts (income, OCI, cash flow, changes
  in equity movements) are `duration`. The column a number sits under
  tells you *which* instant or duration; the concept tells you which
  *kind*.
- The balance-sheet date frequently appears only once, as a heading
  spanning the statement. Losing it is a classic conversion bug: the
  facts still carry a context, but the human-readable report no longer
  tells the reader as of when. Keep the heading; tag the date as a fact
  too if the taxonomy has a concept for it (often a mandated hidden
  fact — see §8).
- Comparative columns are mandatory in most frameworks. A conversion
  that tags only the current year has dropped half the statement.

## 4. Tagging completeness — there is no "half-tagged" statement

A primary statement is either fully tagged or it is defective. "Most of
the balance sheet is tagged" is not a state a filing should ever be in,
because a consumer cannot tell a deliberately omitted line from a missed
one.

Concretely, for every primary statement:

- Every **line item** carries a fact.
- Every **subtotal and total** carries a fact — including the ones
  preparers most often skip because they feel "derived": *total equity*
  / shareholders' equity, total assets, total liabilities and equity,
  result before tax, result for the period.
- Every **column** (current year, comparatives) is tagged, not just the
  current year.

The "half-tagged" failure is invisible from a distance — the file
opens, the validator is happy — and obvious up close: a reviewer reads
down the balance sheet, reaches "Shareholders' equity", and finds no
tag. The fix is procedural, not technical: tag a statement by walking
every row and every column, not by tagging the numbers that happened to
be easy to locate.

## 5. The statement of changes in equity (roll-forward matrices)

The statement of changes in equity is the most under-tagged primary
statement, because it is not a list — it is a **matrix**:

- **Columns** are equity components: issued capital, share premium,
  revaluation reserve, other reserves, retained earnings, equity
  attributable to owners of the parent, non-controlling interests, and
  total equity.
- **Rows** are movements: opening balance, profit for the period, other
  comprehensive income, dividends, share issues, transfers, closing
  balance.

Every **cell** is a fact. The columns are modelled with a dimension (an
equity-components axis); each cell's context carries the relevant
`xbrldi:explicitMember`. The total-equity column is typically the
dimension default (no member emitted — see SKILL.md §5). Opening and
closing balances are `instant`; the movement rows are `duration`.

Tagging only the total column, or only the closing balances, is the
"half-tagged roll-forward" — it leaves most of the statement dark.
Walk the full grid: *components × movements*, every cell.

The arithmetic of the matrix runs two ways, and **neither belongs in the
calculation linkbase**:

- *Down each column* — opening + movements = closing — is a **roll-forward
  across the instant/duration period boundary**. Summation-item arcs bind
  only contributing facts that are *c-equal*: same context, i.e. same
  period **and** dimensions (XBRL 2.1 §5.2.5.2). This restriction is **not
  lifted by Calc 1.1** — its "dimensional alignment" binding still requires
  the period aspect to match. Opening (instant, start), movements
  (duration) and closing (instant, end) live in three different periods,
  so they never bind under either Calc 1.0 or 1.1. (Cross-period
  calculations are the stated aim of **Calculations 2.0**, but as of 2026
  that work has only a 2019 *Requirements* document and **no
  specification** — so it cannot be used for an actual filing.)
- *Across the columns* — components sum to total equity — is **dimensional
  domain aggregation** over the equity-components axis, not a line-item
  summation. Calc arcs cannot point at dimension members at all.

So author the SoCE with the **presentation linkbase plus dimensions**,
and give it **no calculation role**:

- Put the same equity concept under both the `periodStartLabel` and the
  `periodEndLabel` preferred-label roles to document the opening→closing
  roll-forward. ESEF Reporting Manual Guidance 3.4.8 prescribes exactly
  this for the cross-period and cross-dimension relationships the
  calculation linkbase "cannot be used to" express.
- Model the components as dimension members; the total-equity column is
  the domain default.

Forcing the SoCE into the calculation linkbase is a positive error, not
merely wasted effort: the cells never bind, and where a same-period
network (e.g. the balance-sheet equity calc) overlaps the SoCE context it
yields **false-positive calculation inconsistencies** that ESEF Guidance
3.4.1 says to disregard. Both ESEF and the Dutch KvK / SBR taxonomy model
the statement of changes in equity dimensionally and in presentation;
neither defines a SoCE calculation link — and this holds equally for a
consolidated SoCE and a separate (company-only) SoCE.

## 6. Calculation completeness and weight derivation

The calculation linkbase is where conversion errors become arithmetically
visible. Two failures dominate.

**Incomplete calc trees.** Each subtotal in a statement needs a
calculation network whose children are *all* of its components. A P&L
where only "gross operating result" has calculation children — and
"operating result", "result before tax", and "result for the period"
have none — is a half-built calc tree. Every subtotal gets its own
summation network; every line item appears under the subtotal it rolls
into.

This rule is about *same-period* subtotals (balance sheet, income
statement, cash-flow sections). **Cross-period movement schedules are the
exception** — a statement of changes in equity, or a PP&E / provisions
roll-forward (opening + movements = closing), is **not** wired with calc
arcs, because the operands span the instant/duration period boundary and
never bind (see §5). Don't "complete" a calc tree by forcing a roll-
forward subtotal into it; that creates spurious inconsistencies, not
coverage.

**Weights inconsistent with balance type.** A calculation arc's `weight`
is not free choice. XBRL 2.1 §5.1.1.2 requires the weight's sign to be
consistent with the `balance` attributes of the parent (summation) and
child (item) concepts:

- Parent and child have the **same** balance (both `credit`, or both
  `debit`) → `weight="1"`.
- Parent and child have **opposite** balances → `weight="-1"`.

Worked example — gross operating result (a `credit`-balance subtotal):

| Child            | `balance` | vs parent | `weight` |
|------------------|-----------|-----------|----------|
| Net revenue      | credit    | same      | `1`      |
| Cost of sales    | debit     | opposite  | `-1`     |

So `GrossOperatingResult = (+1)·NetRevenue + (-1)·CostOfSales`. If you
find yourself wanting a weight that contradicts this table, the real
error is upstream — usually a wrong `balance` on an extension concept,
or a sign flipped on a fact to fix visible parentheses (see SKILL.md §2).
Fix the cause, not the weight.

Every subtotal's children must also reconcile numerically within the
`decimals` tolerance; mismatched rounding across calc-tree levels fires
`xbrl.5.2.5.2` (see `validation.md` §4 and §6).

## 7. Label discipline — reuse, don't reinvent

The label linkbase is small and easy, which is exactly why conversions
abuse it.

**Do not re-author base-taxonomy labels.** Concepts from the regulator's
taxonomy (IFRS, US-GAAP, the NL taxonomy, the FRC suite) already carry
official standard labels in the required language. Adding your own
`label`-role resource for a base concept is wrong on three counts: it
duplicates the DTS, it risks silently diverging from the official
wording, and it suggests to a reviewer that you changed a concept's
meaning. Only **extension concepts** — concepts you defined because no
base concept fit — need labels you author.

**When you do author a label, match the source document.** An extension
concept's standard label should be the line-item description *exactly as
it reads in the financial statements you converted*. That wording is the
entity's own, and it is the basis on which an auditor or NCA reviewer
judges what the concept means. A paraphrased or invented label ("Other
operating income, net" when the accounts say "Sundry income") breaks the
audit trail between the printed report and the XBRL.

**Add only the label roles you actually use.** A label linkbase scaffold
will show the full set of roles — `terseLabel`, `verboseLabel`,
`totalLabel`, `periodStartLabel`, `periodEndLabel`, `negatedLabel`,
`documentation` — to demonstrate the mechanism. That is a catalogue, not
a template to replicate on every concept. Add a `totalLabel` only if the
concept is presented as a total row; a `periodStartLabel` only if it
appears as an opening balance; a `negatedLabel` only if you present it
with a flipped sign. Roles attached "just in case" are dead weight that
later readers must reason about.

## 8. The hidden section — what genuinely belongs there

SKILL.md §8 warns what must *not* go in `ix:hidden`. The positive case
matters just as much, because conversions also *under*-use it.

`ix:hidden` is the correct home for facts that genuinely exist for XBRL
purposes but have no natural place in the rendered statements:

- **Taxonomy-mandated entity metadata** with no verbatim visible home —
  registered name, registration number, legal form, document/report
  type, and the period-end date as a date-typed fact when the report
  only shows it inside a heading.
- **Non-numeric classification or selection facts** that drive how the
  filing is interpreted but are not a line in any statement — for
  example an entity-size class (in the Dutch taxonomy, members such as
  `kvk-cor:LegalEntitySizeLargeMember`), a reporting-framework choice, or
  a consolidated-versus-company-only indicator. These are real, required
  facts; they simply have no row to sit on, so they belong in
  `ix:hidden` rather than being omitted.

Discipline for the hidden section:

- Only non-numeric, non-transformable facts. Numeric facts in
  `ix:hidden` are an ESEF violation (`ESEF.2.4.1`).
- If a hidden fact's value *also* appears as visible text, the better
  fix is to tag it inline at that visible occurrence. Where it must stay
  hidden, ESEF and EFM require it to be tied to the visible text via the
  `-esef-ix-hidden` / `-sec-ix-hidden` CSS style.
- Keep it minimal and deliberate. `ix:hidden` is for facts that have no
  visible home — not a place to tidy away anything you would rather not
  show.

## 9. What a representative filing actually contains

When you build or test a conversion pipeline, do not validate it against
the simplest possible accounts (a single-page micro-entity statement —
e.g. a Dutch art. 2:408 BW simplified deposit — with no cash flow
statement, no changes-in-equity matrix, and no extension concepts). Such
a filing exercises almost none of the hard parts, so passing it proves
very little.

A *representative* filing — the kind a real pipeline must handle —
contains:

- A full set of primary statements: balance sheet, income statement,
  statement of comprehensive income / OCI, **statement of changes in
  equity**, and a **cash flow statement**.
- At least one **comparative period** column on every statement.
- **Extension concepts** for line items the base taxonomy does not
  cover, each **anchored** to base concepts where the regime requires it
  (see SKILL.md §6 and `esef.md` §4–§5).
- **Dimensional data** — at minimum the equity-components axis of the
  changes-in-equity statement, often operating segments as well.
- **Notes**, detail-tagged or block-tagged according to the regime (see
  `esef-block-tags.md`).

If a conversion has only ever been exercised on a toy filing, treat its
"it validates" as untested for everything in this list.

## 10. The content-level review pass (checklist)

After the validators are clean, do one pass that no validator does:
read the rendered statements as a financial professional and check the
substance. From a distance a converted filing usually looks fine; this
pass is what catches the up-close errors.

- **Structure survived.** Every heading, grouping, date, and column from
  the source is still present and in the right place. Nothing flattened.
- **Completeness.** Every line and every column of every primary
  statement carries a fact. Count rows × columns if unsure.
- **Totals exist.** Total assets, total equity / shareholders' equity,
  total liabilities and equity, result before tax, result for the
  period — each is tagged, not just the line items above it.
- **Balance-sheet identity.** Assets = Equity + Liabilities, and total
  equity itself is a tagged fact.
- **Changes in equity.** Opening + movements = closing holds down every
  component column *and* the total column; every cell of the matrix is
  tagged.
- **Cash flow.** Operating + investing + financing movements, plus
  opening cash, reconcile to closing cash.
- **Calc trees complete.** Every subtotal has a summation network
  covering all of its children; weights match the balance-type table in
  §6; nothing fires `xbrl.5.2.5.2`.
- **Period types.** Instant for balance-sheet concepts, duration for
  flows — for every fact.
- **Signs.** Each canonical value matches the as-reported number;
  credit/debit concepts are not sign-inverted to fix visible
  parentheses.
- **Extensions.** Each extension concept is anchored where required,
  appears in the presentation and calculation linkbases, and carries a
  label that matches the source wording.
- **Hidden section.** Only non-rendered metadata and classification
  facts; no numerics; minimal.

If any item fails, the filing is not done — regardless of what the
validation report says.

## Sources

- Inline XBRL 1.1, REC 2013-11-18 (errata 2024-12-17):
  https://www.xbrl.org/Specification/inlineXBRL-part1/REC-2013-11-18/
- XBRL 2.1, REC 2003-12-31 (errata 2013-02-20), §5.1.1.2 (balance) and
  §5.2.4–§5.2.5 (presentation and calculation linkbases):
  https://www.xbrl.org/Specification/XBRL-2.1/REC-2003-12-31/XBRL-2.1-REC-2003-12-31+corrected-errata-2013-02-20.html
- XBRL Calculations 1.1, REC 2023-02-22:
  https://www.xbrl.org/Specification/calculation-1.1/REC-2023-02-22/calculation-1.1-REC-2023-02-22.html
- XBRL Dimensions 1.0, REC 2012-01-25:
  https://www.xbrl.org/Specification/dimensions/REC-2012-01-25/dimensions-REC-2012-01-25.html
- ESMA ESEF Reporting Manual (presentation, anchoring, hidden-section
  rules): https://www.esma.europa.eu/ — see `esef.md` for section detail.
