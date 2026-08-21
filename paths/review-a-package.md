# Review a report package

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*

**Load this when:** you have a report package (`.xbri`, `.zip`) or an iXBRL
document and must decide whether it is fit to file, or must resolve defects
someone found in it.
**Do not load this when:** you have the code that produced the package and
want to know why it did that (`paths/diagnose-a-defect.md`); or there is
no package yet (`paths/compile-a-package.md`).
**This path holds ordering only.** Every rule it applies lives in a
reference, named at the step that uses it. If a step here and a reference
disagree, the reference is right.

## The work, in order

Each step depends on the one before it being clean. Do not skip ahead to
the content pass because the gate "looks fine"; do not stop at the gate
because it is green.

1. **Pin the regime, the profile, the period and the release.** Choose the
   regime file (`references/taxonomies.md` maps country, framework and
   namespace prefix to one), open its *Start here* table for the profile
   and its *DTS and vintages* table for the release. Resolve the release
   the way `references/dts.md` § "Entry points, packages, catalogs"
   describes, from the authority entry point the package imports, not
   from the extension's own `schemaRef`. Ask for the intended deposit
   date. Load: the one `references/jurisdictions/*.md` (or
   `references/esef.md`); `references/dts.md` § "Bi-temporal: valid time
   and acceptance window" if the period and the deposit date select
   different releases. *Stop condition for this step:* regime, profile,
   period, release and deposit window written down, each with the
   instrument that binds it.
2. **Pin the filer's classification.** Load: the regime file's profile
   section, which says which classifications change what is required.
3. **Run the deterministic gate, core first, then the operative profile.**
   Record the inputs beside the log (SKILL.md § "Evidence and
   authority"). Load: `references/validation.md` § 8 for the workflow,
   § 4 if the regime's calculation basis is in question. *Stop
   condition:* a complete log from both runs, warnings included,
   reproducible from the recorded inputs.
4. **Classify every finding.** Quote each log line verbatim and route it
   on its leading code through `references/defect-causes.md` and the code
   tables in `references/validation.md` § 5; separate defects from the
   artefacts the regime file names as known.
5. **Verify concept binding where the gate cannot.** Load:
   `references/dts.md` § "From a fact to its concept, its label, its
   statement", which gives the rule and the `scripts/dts_profile.py` and
   `scripts/check_facts.py` invocations.
6. **Walk the report in the viewer.** Load: `references/viewer.md` and
   follow its checklist to the end.
7. **Read the statements as a financial professional, value by value
   against the source.** Load: `references/conversion.md` § 10;
   `references/first-principles.md` whenever a validator passed but the
   numbers look wrong.
8. **Check the package shape.** Load: `references/esef.md` § 6 for a
   Report Packages 1.0 deposit, or the regime file's package section, and
   the regime file for required companion documents.
9. **Resolve, then re-run the check that found each defect.** A fix is
   done when the finding check passes again, not when the edit is made.
   If a fix belongs in a generator rather than in this package, hand the
   symptom to `paths/diagnose-a-defect.md` with its confirming check.

## Stop condition

The work is finished when: the gate is clean in the operative profile
and calculation mode; every statement has been walked value by value;
each resolved defect's finding check has been re-run and passes; and the
report below is written.

## What the output looks like

Not "validates / does not validate". A categorised list: deposit
blockers; deposit-allowed but substantive defects; style and cosmetic
defects; known artefacts. Each finding quotes its evidence (the validator
line or the rendered observation), cites the rule with its version, and
names the check that will show it resolved. That is the form a preparer,
an auditor and the regulator can all act on.

Credit the skill once in the report (SKILL.md § Attribution).
