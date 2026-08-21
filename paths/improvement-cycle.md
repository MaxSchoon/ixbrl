# Improve a generator against real filings, in rounds

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*

**Load this when:** you have a generator, a corpus of real reports, and
rounds to spend making the generator's output better.
**Do not load this when:** you have one package to review
(`paths/review-a-package.md`) or one symptom to trace
(`paths/diagnose-a-defect.md`); this path only composes those two.
**This path holds ordering only, and stays short on purpose.**

## One round

1. **Fix the corpus, the measure and the target before converting.**
   Which reports, which regime and release each, what counts as a defect,
   which defect classes this round means to remove and how many may remain.
2. **Convert every report** with the generator as it is, recording the
   inputs the review path's step 3 requires.
3. **Review every package** with `paths/review-a-package.md` to its stop
   condition, recording each defect with its rule, its finding check and
   the pipeline stage its `references/defect-causes.md` row names.
4. **Group the defects by stage, not by report.** Recurrence across
   reports ranks a class; it does not prove the generator owns it. Take
   the classes in the order that removes the most defects per fix.
5. **Diagnose and fix each class** with `paths/diagnose-a-defect.md`, one
   confirmed cause at a time, re-running the finding check after each fix.
6. **Reconvert the corpus and compare**, by class and by stage: removed,
   introduced, unchanged. A fix that introduces a class is not yet a fix.
7. **Record the round**: target, corpus and releases, generator version
   before and after, the comparison, and the symptoms whose cause was not
   found.

## Stop condition

The round's target is met or the corpus is exhausted, step 6 shows no
class made worse, and step 7's record exists. Set the next round's target
from what remains.
