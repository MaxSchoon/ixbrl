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

1. **Pin the regime, the profile, the period and the release.** Read the
   period from `<xbrli:period>`; read the release from the `schemaRef`
   namespace date and `META-INF/taxonomyPackage.xml`; ask for the
   intended deposit date. Open the regime file's *Start here* table and
   choose the filing profile, then its *DTS and vintages* table to check
   that the release is valid for the period and accepted at deposit.
   Load: the one `references/jurisdictions/*.md` for the regime
   (`references/esef.md` for an ESEF filing); `references/dts.md`
   § "Bi-temporal: valid time and acceptance window" if the two clocks
   disagree. State all four back before opening the file in earnest.
   *Stop condition for this step:* regime, profile, period, release and
   deposit window written down, with the instrument that binds each.
2. **Pin the filer's classification.** Size class, filer category, IFRS
   versus national GAAP, consolidated versus separate scope: it changes
   which absences are defects. Load: the regime file's profile section.
3. **Run the deterministic gate, core first.**
   `scripts/validate_with_arelle.sh <pkg> core`, then the operative
   profile, with `--packages` for the operative taxonomy and the
   calculation mode the regime prescribes. Capture every message,
   warnings included. Record the Arelle release, plugins, command line,
   packages and offline state beside the log (SKILL.md § "Evidence and
   authority"). Load: `references/validation.md` § 8 for the workflow and
   § 4 if the regime's calculation basis is in question.
   *Stop condition:* a complete log from both runs, reproducible from the
   recorded inputs.
4. **Classify every finding.** Route each code through
   `references/defect-causes.md` (symptom, what the package shows,
   candidate causes, the confirming check, where the rule lives) and the
   code tables in `references/validation.md` § 5. Separate real defects
   from known artefacts the regime file names (dual-scope calculation
   cross-binding, prefix-by-design noise, diagnostic-only warnings). Quote
   the log line verbatim and route on its leading code.
5. **Verify concept binding where the gate cannot.** Every fact's QName
   must resolve to a concept declared in the operative DTS:
   `scripts/dts_profile.py <entry> --package <pkg.zip> --concept <QName>`
   for any concept in doubt; `scripts/check_facts.py <file>` for
   contexts, units, decimals and continuations. Load:
   `references/dts.md` § "From a fact to its concept, its label, its
   statement".
6. **Walk the report in the viewer.** Generate an Arelle iXBRL Viewer and
   follow its checklist: highlight tagged facts, click each
   primary-statement subtotal to read its calculation network, search
   for hidden facts, sample a dozen facts across statements for period,
   unit, decimals, scale and dimensional context. Load:
   `references/viewer.md`.
7. **Read the statements as a financial professional.** Does the balance
   sheet balance, do the cash-flow categories reconcile, are signs
   consistent, do extension concepts make accounting sense, do the
   period-end metadata facts match the statements. Walk every statement
   value by value against the source where one exists. Load:
   `references/conversion.md` § 10; `references/first-principles.md`
   whenever a validator passed but the numbers look wrong.
8. **Check the package shape.** Root clutter, `.html` versus `.xhtml`,
   `META-INF/taxonomyPackage.xml` and, for Report Packages 1.0,
   `META-INF/reportPackage.json`; the regime's required companion
   documents (the Dutch auditor's report as a separate tagged document).
   Load: `references/esef.md` § 6, or the regime file's package section.
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
