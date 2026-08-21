# Improve a generator against real filings, in rounds

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*

**Load this when:** you have a generator, a corpus of real reports, and
rounds to spend making the generator's output better.
**Do not load this when:** you have one package to review
(`paths/review-a-package.md`) or one symptom to trace
(`paths/diagnose-a-defect.md`); this path only composes those two.
**This path holds ordering only, and stays short on purpose.** If it
grows past a page it is restating the paths it composes.

## One round

1. **Fix the corpus and the measure before converting.** Which reports,
   which regime and release each, and what counts as a defect (a gate
   message in the operative profile, a value-by-value deviation from the
   source, a binding the DTS does not support). Write the round's target
   down: which defect classes it means to remove, and how many of each
   may remain.
2. **Convert every report in the corpus** with the generator as it is,
   recording the inputs the review path's step 3 requires.
3. **Review every package** with `paths/review-a-package.md` to its
   stop condition. Record each defect with its rule, its finding check,
   and the stage of the pipeline it points at.
4. **Group the defects by stage, not by report.** A defect class that
   appears across reports is a generator fault; one that appears in a
   single report is usually that report's. Take the classes in the order
   that removes the most defects per fix.
5. **Diagnose and fix each class** with `paths/diagnose-a-defect.md`,
   one confirmed cause at a time, re-running the finding check after each
   fix.
6. **Reconvert the corpus and compare.** Defects removed, defects
   introduced, defects unchanged, by class and by stage; the gate's
   messages before and after; the value-by-value deviations before and
   after. A fix that removes one class and introduces another is not yet
   a fix.
7. **Record the round** so the next round can tell whether this one
   worked: the target, the corpus and releases, the generator's version
   before and after, the comparison, and the symptoms whose cause was not
   found.

## Stop condition

The round's target is met or the corpus is exhausted, the comparison in
step 6 shows no class made worse, and step 7's record exists. Then set
the next round's target from the defects that remain.
