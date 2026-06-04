# Reviewing with the Arelle iXBRL Viewer

Use the Arelle iXBRL Viewer as the **visual review workbench**, not as
a replacement for validation. The viewer is the tool that makes
content-level defects visible — sign conventions, scope mis-tagging,
orphan presentation arcs, dimensional context drift — that no
validator catches. Validate first (see SKILL.md "Standard validation
pipeline"), then use the viewer for the content pass.

The viewer is published as an Arelle plugin plus a JavaScript bundle:

- **Source repository:** <https://github.com/Arelle/ixbrl-viewer>
- **Docs (ReadTheDocs):** <https://arelle-ixbrl-viewer.readthedocs.io/en/latest/>
- **User guide:** <https://arelle-ixbrl-viewer.readthedocs.io/en/latest/user_guides/user_guide.html>

## Preparing a viewer

Generate the viewer with the `iXBRLViewerPlugin` plugin before doing
the content review:

```bash
python3 /path/to/Arelle/arelleCmdLine.py \
  --plugins=/abs/path/to/iXBRLViewerPlugin \
  -f report.xhtml \
  --save-viewer report-viewer.xhtml \
  --viewer-url https://cdn.jsdelivr.net/npm/ixbrl-viewer@<version>/iXBRLViewerPlugin/viewer/dist/ixbrlviewer.js
```

For Inline XBRL document sets, also load `inlineXbrlDocumentSet`, pass
the document-set JSON to `-f`, and write `--save-viewer` to an output
directory. Document-set and stub viewers must be served over HTTP —
browser security restrictions prevent loading them from `file:` URLs.

Pin the viewer JavaScript to the same major version, and the same or
later minor version, as the plugin that prepared the viewer metadata.
Use a local or downloaded `ixbrlviewer.js` instead of the CDN when
external network fetches are not acceptable. If the source XHTML must
remain unchanged, use **stub viewer mode** when all facts and
footnotes already have `id` attributes.

## Review checklist

Walk these in order. Each step builds on the prior.

- **Highlight tagged facts.** Turn on **Highlight XBRL Elements**.
  Namespace colours reveal which taxonomy or extension supplied each
  concept. An unexpected colour distribution (e.g. extension red where
  base-taxonomy green should dominate) is an early signal of
  over-extension.
- **Fact inspector pass.** Click each fact and inspect concept,
  dimensions, date/range, value, accuracy (`decimals`), scale, entity,
  labels, references, anchoring, calculations, footnotes, and section
  placement. Sample at least: every primary-statement subtotal, every
  dimensioned fact, every fact with `decimals="INF"`, every fact in
  `ix:hidden`.
- **Document summary.** Compare fact counts, hidden fact counts,
  concepts, dimensions, members, and included files against the
  expected filing scope. A primary-statement count that doesn't
  reconcile to the printed accounts is a defect.
- **Search and filter.** Find facts by taxonomy labels, references,
  concept type, hidden/visible status, period, namespace, unit, scale,
  dimensions, and calculation relationships. Useful filters for review:
  - All facts where the concept is abstract (should be zero — abstracts
    are never tagged on a fact).
  - All facts with `decimals="INF"` (audit each one — see SKILL.md
    "First principles" §1).
  - All facts in `ix:hidden` (each must have a visible counterpart or
    a defensible reason — see SKILL.md "First principles" §8).
- **Duplicate-fact cycle.** When the inspector reports more than one
  occurrence of a fact, cycle through them. Inconsistent duplicate
  values are a filing defect, not a display issue (`ESEF.2.2.4.*`,
  EFM equivalents).
- **Export to Excel.** For tables in a language the reviewer does not
  read fluently, export tagged tables. The export includes document
  descriptions alongside concept and dimension labels, which makes
  scope-tagging defects visible side-by-side with the rendered values.
- **Calc 1.1 toolbar.** Enable **Calculations v1.1** when the
  regulator accepts Calc 1.1. Inspect calculation relationships for
  subtotal completeness and sign errors. For SBR Dutch GAAP (where
  Calc 1.0 is normative), treat any Calc 1.1 cross-scope warning as
  diagnostic, not blocking — see `nl-sbr.md` §4.2.
- **Review mode for drafts.** For partially tagged or incomplete
  drafts, enable viewer review mode with `--viewer-feature-review` or
  `?review=true` in the URL. Review mode highlights untagged numbers
  and dates instead of namespace-based fact colours, making the
  remaining tagging work visible.

## What the viewer does **not** tell you

The viewer is a visualisation of what was tagged. It does not catch:

- Whether the value mapped into the correct dimensional context
  (consolidated vs separate scope; see `nl-sbr.md` §4.3).
- Whether the rendered XHTML is faithful to the source document
  (number transcription errors, omitted comparatives).
- Whether the entity-metadata facts match the filer's actual
  identification (registered name, registration number, registered
  office).
- Whether the calculation linkbase covers every subtotal that the
  rendered statements show.

For those, walk the rendered statements as a financial professional
(see `conversion.md` §10) and cross-check against the source.
