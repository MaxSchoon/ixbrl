# Monthly maintenance cycle

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*

Taxonomies, filing rules and mandates move every month somewhere. A skill
that states them is only as good as the last time someone re-read the
sources. This is the routine that does the re-reading, and the gates that
decide whether what it changed may land.

It is one routine with five tasks. It runs once per calendar month.

## Contents

- [When it runs](#when-it-runs)
- [The five tasks](#the-five-tasks)
- [The hillclimb](#the-hillclimb)
- [Gates](#gates)
- [Landing](#landing)
- [The cycle record](#the-cycle-record)

## When it runs

- **Due** at 09:00 Europe/Amsterdam on the first day of each month. The
  time is wall-clock time in that zone, so it stays 09:00 across the change
  to and from summer time.
- **Done** for a month once `maintenance/cycles/YYYY-MM.md` for that month
  is on `main`. That file is the only marker; nothing else counts.
- **Checked by code first.** The scheduler that starts a cycle decides with
  a deterministic check whether a cycle is due (the month has no record on
  `main` and none is running), and starts nothing otherwise. A missed first
  of the month is picked up by the next check; two cycles never run at once;
  a cycle that died without a record is started again.

## The five tasks

Every task reads the sources listed for it in `maintenance/sources.json`,
primary sources only, and sets `checked_on` for each source it re-read.

1. **Jurisdictions.** For every regime the skill covers, re-read the
   regulator's release pages and update the *DTS and vintages* table of its
   reference: a new release becomes a new row; a status, an acceptance
   window or an end date changes in place. **A historical row is never
   removed**: its valid time and acceptance window are what a review of an
   older filing needs (`tests/eval_skill.py` refuses a dropped row).
2. **New mandates.** Sweep the mandate-discovery sources for any regime
   that introduces or changes an iXBRL or XBRL obligation: a new filing
   form, a new filer population, a new taxonomy. A binding obligation gets
   its own reference under `references/jurisdictions/` (the shape
   `tests/check_reference_structure.py` enforces), a row in the SKILL.md
   reference index, its name among the description's trigger terms, and a
   topic in `maintenance/sources.json`. A draft or a proposal gets a dated
   note where it applies, never a file of its own.
3. **Topics.** Re-read the specification body and the validator's releases
   (Inline XBRL, OIM, Calculations, taxonomy and report packages, the next
   draft model) and update `references/spec.md`, `references/structure.md`,
   `references/dts.md` and `references/validation.md`.
4. **Skill craft.** Re-read the published guidance on writing and
   evaluating skills, from the agent vendors, the open specification and
   recent papers. Record a verdict per new practice in the cycle record:
   adopted, adapted or rejected, with the reason and the source. A practice
   that names one runtime is adopted only in a vendor-neutral form
   (`CONTRIBUTING.md` § Discipline).
5. **Hillclimb.** Improve how the skill routes and triggers, measured by
   `tests/eval_skill.py` (next section).

## The hillclimb

The eval scores three things without a model in the loop: whether the
description wins a query against neighbouring skills, whether the reference
index sends a query to the file that answers it, and whether each file still
states the facts it must. Cases are split into `train` and held-out `test`
(`evals/cases.json`); the bars live in `evals/baseline.json`.

- **One lever per round** (for example the wording of index rows, or the
  description), chosen by reading train failures only.
- **Held-out cases are never read while editing** and never copied into the
  skill; the eval fails a held-out query that appears in the skill text.
- **A round is accepted** when train improves and no held-out metric falls
  below its value before the round. The declared slack in the eval absorbs
  rank shifts that a new reference row causes; it is not room for a round.
- **Stop** after three rounds without a train gain, or at the first round
  that would lower a held-out metric (that round is reverted).
- **A wrong expectation is fixed in the case, not in the skill**, and only
  for train cases; held-out cases are append-only.
- **Freeze** after the last accepted round:
  `python3 tests/eval_skill.py --freeze --reason "cycle YYYY-MM: ..."`. A
  freeze never lowers a bar, records the measured scores, and is required
  after any change to the eval harness, which the eval detects.

The result of a cycle is the held-out delta, written in the cycle record.

## Gates

A cycle's pull request lands only when all of these pass:

```bash
python3 tests/check_skill.py
python3 tests/check_reference_structure.py
python3 tests/check_section_refs.py
python3 tests/check_sources.py --max-age 40
python3 tests/eval_skill.py --check
python3 -m unittest discover -s tests -p 'test_*.py'
npx --yes markdownlint-cli2@0.18.1
```

plus every other check CI runs. `--max-age 40` is the cycle's own bar:
every source was re-read within the last 40 days. CI runs the registry check
without it.

## Landing

One pull request per cycle, from a branch cut from current `main`. It
carries the cycle record, an independent review, and every CI check green;
it merges only when it is not behind `main`. Commits and pull requests say
what changed and why, with sources; they carry no tool or assistant
attribution.

## The cycle record

`maintenance/cycles/YYYY-MM.md`, one per month, in this order: what was
re-read, what changed and where (with sources), new mandates found or the
statement that none were, skill-craft verdicts, the hillclimb rounds with
their train and held-out scores, and the pull request that landed it.
