# Diagnose a defect back to its cause in a generator

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*

**Load this when:** a package shows a symptom (a validator message, a
wrong fact, a wrong rendering, a wrong binding) and you have the code
that produced it, and the question is where in that code the symptom
comes from.
**Do not load this when:** you only need to know what a code means or
how to fix this one package (`paths/review-a-package.md` and
`references/defect-causes.md` answer that without the code); or no
package exists yet (`paths/compile-a-package.md`).
**This path holds ordering only.** The candidate causes and their checks
live in `references/defect-causes.md`; the rules live in the references
it names.

## The work, in order

The shape is condition, diagnostics, candidate causes, confirmation,
location, fix. Enter at the step where your evidence already is: a code
in hand skips to step 3; a confirmed cause skips to step 5.

1. **State the condition as an observable in the package.** The code and
   message verbatim, or the fact that is wrong: its element, context,
   unit, decimals, the value the package carries and the value the source
   shows. One symptom per pass. If several symptoms appear, record them
   all and take the one with the clearest check first.
2. **Reproduce it deterministically.** Same Arelle release, plugins,
   disclosure system, calculation mode, taxonomy packages and offline
   state as the run that first showed it, recorded beside the log
   (SKILL.md § "Evidence and authority"). A symptom that does not
   reproduce is a symptom of the environment, and the environment is the
   first candidate cause. Load: `references/validation.md` § 1 and § 8.
3. **Collect candidate causes.** Find the symptom's row in
   `references/defect-causes.md`. Take every candidate it lists, by
   pipeline stage. Take none as a verdict. For a symptom with no row,
   derive candidates from the rule itself: `references/validation.md`
   § 5 for the code, the specification or regime file it cites, and
   `references/first-principles.md` for the eight places most converters
   go wrong. Record the new symptom so a row can be added.
4. **Confirm one candidate with its check.** Run the row's check against
   the package, the source and the operative DTS
   (`scripts/dts_profile.py --concept`, `scripts/check_facts.py`, a
   targeted `xmllint --xpath` or diff, a second run with one input
   changed). A check that refutes the candidate eliminates it; move to
   the next. If every candidate is refuted, the symptom needs a new
   candidate, not a forced fit: say so, and go back to the rule.
5. **Locate it in the code, at the stage the confirmed cause names.**
   Only now open the generator, and open it at that stage (concept
   selection, context assignment, unit and decimals, sign and label,
   network generation, hidden section, package assembly, validator
   invocation). A symptom that appears for one filing and not another
   points at a data-dependent branch at that stage; find the input that
   differs before reading further.
6. **Fix at that stage, then re-run the check that confirmed the cause,
   then the gate.** The check passing again is the exit criterion for the
   cause; the gate passing on a freshly generated package is the exit
   criterion for the fix. A fix made without the check is a guess that
   happened to compile.

## Stop condition

One candidate cause is confirmed by its check; the fix is made at the
stage that cause names; the confirming check and the deterministic gate
pass on a package generated after the fix; and the symptom, the refuted
candidates, the confirmed cause and the check are recorded where the next
person who sees the symptom will look.

## What this path refuses to do

It does not conclude from the symptom alone, however familiar the code
looks; it does not change the generator before a check has confirmed a
cause; and it does not accept "the validator is quiet now" as proof when
the confirming check was never re-run.
