# Compile a report package

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*

**Load this when:** you are producing an iXBRL report package from a source
document (PDF, DOCX, accounts export) or from a data model, by hand or
with coding agents, and no package exists yet.
**Do not load this when:** a package exists and the question is whether
it is right (`paths/review-a-package.md`); or a generator already exists
and produces wrong output (`paths/diagnose-a-defect.md`).
**This path holds ordering only.** The rules live in the references it
names; the scaffolds live in `assets/`.

## The work, in order

The order is forced by dependencies: nothing can be tagged before the
DTS is pinned, nothing can be packaged before the networks exist, and
nothing counts as done until the review path passes on the result.

1. **Pin the regime, the profile, the period and the release.** Same as
   the review path's step 1, including how the release is resolved.
   Load: `references/taxonomies.md` to choose the regime file; that
   file's *Start here* and *DTS and vintages* tables; `references/dts.md`
   § "Bi-temporal: valid time and acceptance window". *Stop condition for
   this step:* the entry point URL and the taxonomy package(s) to load
   are written down and resolve
   (`scripts/dts_profile.py <entry> --package ... --offline` exits 0).
2. **Fix the filer's classification and scope, and the metadata facts the
   regime requires.** Load: the regime file's profile section.
3. **Establish the statement inventory and the fidelity contract.** Load:
   `references/conversion.md` § 1 to § 5.
4. **Map every line to a concept, from the operative DTS, never from
   memory.** Load: `references/dts.md` § "From a fact to its concept, its
   label, its statement" for the lookup; `references/types.md` for item
   types and attributes; `references/esef.md` § 4 and § 5 or the regime
   file for when an extension is allowed and how it must be built;
   `references/first-principles.md` § 2 and § 3 before deciding signs and
   period types.
5. **Build contexts, units, decimals and dimensions.** Load:
   `references/first-principles.md` § 1 and § 4; `references/dimensions.md`;
   `references/spec.md`.
6. **Generate the networks.** Start from the scaffolds in `assets/`, each
   annotated with the rule it implements. Load: `references/conversion.md`
   § 6 and § 7; `references/structure.md`.
7. **Apply the regime's tagging obligations.** Load:
   `references/esef-block-tags.md` for ESEF, the regime file's tagging
   section otherwise; `references/conversion.md` § 8 for the hidden
   section; `references/spec.md` for the transformation registry.
8. **Assemble the package.** Apply the generator-stamp policy in SKILL.md
   § Attribution before any hash or signature is taken. Load:
   `references/esef.md` § 6 for Report Packages 1.0, or the regime file's
   package section; `assets/taxonomyPackage.xml` and `assets/catalog.xml`.
9. **Hand the result to `paths/review-a-package.md`** and run it to its
   stop condition. Defects it finds that trace to how the package was
   generated go to `paths/diagnose-a-defect.md`.

## Stop condition

The package is finished when the review path's stop condition is met on
it. This path adds no stop condition of its own, on purpose: a compiled
package that has not been reviewed is not finished.

## Before handing over

The failures a validator does not catch are catalogued, each with the
check that shows it, in `references/defect-causes.md` § "Symptoms with no
validator message". Run that table against the package before step 9;
the review path will run it again, and finding nothing twice is the
point.
