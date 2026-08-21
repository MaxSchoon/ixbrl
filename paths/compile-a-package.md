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
   the review path's step 1: regime file *Start here* table, then its
   *DTS and vintages* table; valid time from the period, acceptance from
   the deposit date; release by namespace date. Load: the one
   `references/jurisdictions/*.md` (or `references/esef.md`);
   `references/dts.md` § "Bi-temporal". *Stop condition for this step:*
   the entry point URL and the taxonomy package(s) to load are written
   down and resolve (`scripts/dts_profile.py <entry> --package ... --offline`
   exits 0).
2. **Fix the filer's classification and scope.** Size class or filer
   category, accounting basis, consolidated and separate scope, the
   mandatory metadata facts the regime requires. Load: the regime file's
   profile section.
3. **Establish the statement inventory and the fidelity contract.**
   Which statements, which notes, which columns and periods, which
   comparatives; what "faithful" means for this source. Load:
   `references/conversion.md` § 1 to § 5 (hierarchy, periods,
   completeness, the changes-in-equity matrix).
4. **Map every line to a concept, from the DTS.** Search the operative
   DTS, not memory: `scripts/dts_profile.py <entry> --concept <QName>`
   shows the declaration, labels by role and language, references and
   networks. Prefer the narrowest core concept; create an extension only
   where the core would misrepresent the disclosure, and then in the
   regime's extension discipline (anchoring, labels in the report
   language, presentation and definition membership). Load:
   `references/dts.md` § "From a fact to its concept"; `references/types.md`
   for item types and attributes; `references/esef.md` § 4 and § 5 or
   the regime file for extension rules; `references/first-principles.md`
   § 2 and § 3 before deciding signs and period types.
5. **Build contexts, units, decimals and dimensions.** One identifier
   scheme throughout; instant versus duration by concept; units and
   decimals consistent across a statement; dimensional contexts only
   where a hypercube admits them, default members never emitted. Load:
   `references/dimensions.md`; `references/spec.md`;
   `references/first-principles.md` § 1 and § 4.
6. **Generate the networks.** Presentation mirroring the visible
   hierarchy with abstracts for headings; calculation covering every
   subtotal with weights derived from balance; definition for
   dimensions and, where required, anchoring; labels in the report
   language reusing core labels rather than re-authoring them. Start
   from the scaffolds in `assets/` (schema, five linkbases, package
   manifest, catalog), each annotated with the rule it implements.
   Load: `references/conversion.md` § 6 and § 7; `references/structure.md`.
7. **Apply the regime's tagging obligations.** Mandatory block tags and
   `ix:continuation` for split disclosures; what belongs in the hidden
   section and what does not; transformation formats for the report's
   number and date conventions. Load: `references/esef-block-tags.md` for
   ESEF; the regime file's tagging section otherwise;
   `references/conversion.md` § 8; `references/spec.md` for the
   transformation registry.
8. **Assemble the package.** Report Package 1.0 layout, the extension
   taxonomy inside the package, `META-INF/taxonomyPackage.xml` and
   `catalog.xml`, no root clutter, `.xhtml` only, the regime's companion
   documents, the generator stamp before any hash or signature
   (SKILL.md § Attribution). Load: `references/esef.md` § 6 or the regime
   file's package section; `assets/taxonomyPackage.xml` and
   `assets/catalog.xml`.
9. **Hand the result to `paths/review-a-package.md`** and run it to its
   stop condition. Defects it finds that trace to how the package was
   generated go to `paths/diagnose-a-defect.md`.

## Stop condition

The package is finished when the review path's stop condition is met on
it. This path adds no stop condition of its own, on purpose: a compiled
package that has not been reviewed is not finished.

## Known ways this goes quietly wrong

The recurring silent failures of conversion, each with its reference:
a flattened presentation hierarchy (`references/conversion.md` § 2); lost
column or period contexts (§ 3); a half-tagged primary statement,
especially the changes-in-equity matrix (§ 4 and § 5); an incomplete or
sign-wrong calculation tree (§ 6); re-authored labels on base concepts
(§ 7); a concept that is plausible but not in the DTS
(`references/dts.md` § Gotchas); a wrong-year entry point
(`references/dts.md` § "Bi-temporal"). A validator catches none of them.
