<!--
Thanks for contributing to the iXBRL skill! Keep PRs focused — one logical
change each. Cite a primary source (spec section or regulator publication you
actually fetched) for every factual claim you add or change. See CONTRIBUTING.md.
-->

## What this changes

<!-- A short summary. Link any related issue (e.g. "Closes #12"). -->

## Type of change

- [ ] Spec-citation correction (skill said X, the spec/regulator says Y)
- [ ] Regulator update (new ESEF / EFM / FRC / SBR / NT / DPM version)
- [ ] Scaffold change (`assets/` — skeleton, schema, linkbases, package)
- [ ] Trigger fix (skill fires when it shouldn't / misses when it should)
- [ ] Script change (`scripts/check_facts.py`, `scripts/validate_with_arelle.sh`)
- [ ] Docs / structure
- [ ] Other:

## Source citations

<!--
For every technical claim added or changed, cite the section or URL you
actually fetched, with its version/date — e.g. `iXBRL 1.1 §13.1.2`,
`EFM 6.5.21`, `ESEF Reporting Manual G.4.1.3`, or a pinned regulator URL.
Update the `Sources` list at the end of the affected references/*.md.
-->

-

## Checklist

- [ ] One logical change; focused diff
- [ ] Primary-source citation (spec section or pinned URL) for every new/changed claim
- [ ] `Sources` list updated in the affected `references/*.md`
- [ ] Language stays vendor-/harness-neutral (product behaviour labelled as such)
- [ ] `SKILL.md` still under 32 KiB and the frontmatter `description` under 1024 chars
- [ ] Asset integrity, if `assets/` touched:
      `xmllint --noout assets/*.xml assets/*.xsd assets/*.xhtml`
      cross-file refs resolve (`python3 tests/check_skill.py`)
- [ ] Scripts still compile / run:
      `python3 -m py_compile scripts/check_facts.py`
      `python3 scripts/check_facts.py assets/ixbrl-skeleton.xhtml`
- [ ] Honest-gap notes preserved or added where a claim couldn't be verified

## Notes for the reviewer

<!-- Anything that helps review: a tricky citation, an intentional gap, a
     multi-agent review you ran, etc. -->
