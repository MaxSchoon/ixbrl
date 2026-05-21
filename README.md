# iXBRL Skill

A vendor-neutral skill for working with **Inline XBRL (iXBRL)** and the
underlying XBRL stack — covering the major regulators (SEC EDGAR, ESMA
ESEF, UK FRC / Companies House / HMRC, Dutch SBR / KvK / AFM, EBA, EIOPA),
the IFRS Accounting Taxonomy, FASB US-GAAP, and the Arelle validation
toolchain.

Built for the people who actually file: accountants, auditors,
controllers, investor-relations teams, banking and insurance
supervisory-reporting analysts, and the engineers who write the code
that produces their iXBRL.

## What this skill gives you

- **`SKILL.md`** — first principles, regulator routing, and the
  validation pipeline. Loaded automatically when the skill triggers.
- **Live filing corpus routing** — directs agents to
  <https://filings.xbrl.org/> for country-filtered ESEF/UKSEF examples
  such as Netherlands (`NL`) filings, with viewer output, xBRL-JSON,
  report packages, and validation messages.
- **`references/`** — load on demand:
  - `spec.md` — Inline XBRL 1.1, XBRL 2.1, XDT (Dimensions),
    Transformation Registry 4, calculation linkbase semantics.
  - `taxonomies.md` — IFRS, ESEF, US-GAAP / DEI / SRT, UK FRC Suite,
    Dutch NT / SBR, EBA & EIOPA DPM, plus EDINET / CNMV / SBR-AU / MCA.
  - `esef.md` — ESEF legal basis, Reporting Manual rules, anchoring,
    block tagging, report package, NCAs, and `ESEF.*` error codes.
  - `sec-edgar.md` — SEC iXBRL phase-in, EDGAR Filer Manual sections,
    DEI cover-page tagging, `EFM.6.05.*` codes, recent rules
    (Pay-Versus-Performance, cybersecurity disclosure, tailored
    shareholder reports).
  - `validation.md` — Arelle CLI, plugins, formula linkbase, Calc 1.1,
    a master list of `ESEF.*` / `EFM.*` / `xbrl.*` / `xbrldie:*` error
    codes with root cause and fix, and 25 anti-patterns that pass
    syntax but fail review.
- **`scripts/validate_with_arelle.sh`** — wraps `arelleCmdLine` with
  the right plugin chain per profile (`esef`, `efm`, `ukfrc`, `hmrc`,
  `core`).
- **`scripts/check_facts.py`** — pure-Python pre-flight that catches
  cheap-to-detect issues (missing `decimals`, dangling continuation
  chains, undefined contexts/units, non-ISO currency measures,
  `decimals="INF"` abuse, inconsistent duplicate facts) before you
  spend cycles in Arelle.

## Source discipline

Every factual claim in this skill is tied to a primary source from the
issuer or standard-setter (xbrl.org, ifrs.org, esma.europa.eu, sec.gov,
fasb.org, frc.org.uk, sbr-nl.nl, eba.europa.eu, eiopa.europa.eu, the
Arelle GitHub repository). Each `references/*.md` ends with a
`Sources` list of the URLs consulted. Versions and rule numbers were
verified at the time of writing — re-check the publisher's page before
relying on a specific version for a regulated filing.

## Install

This is an AI-agent skill — a self-contained directory of markdown and
scripts that any agent harness supporting the
[skill convention](https://skills.sh) can load.

### Manual install

Drop the directory under your agent's skills root. Common locations
include `~/.<agent>/skills/ixbrl/` or a project-local
`.agents/skills/ixbrl/`. Most harnesses auto-discover the skill from
the `name` and `description` in the SKILL.md frontmatter.

### Install via the skills CLI

`SKILL.md` lives at the root of this public repo, so any runtime with
the [`skills`](https://www.skills.sh) CLI can install it directly:

```bash
npx skills add MaxSchoon/ixbrl
```

skills.sh has no separate submission step — its directory is populated
from CLI install telemetry. The skill becomes discoverable (via
`npx skills find ixbrl`) and climbs the listing as people install it
with the command above.

## Compatibility

The skill is harness-agnostic. It works with any AI-agent runtime that:

1. Loads skills from a directory of markdown files with YAML
   frontmatter (`name`, `description`).
2. Routes user requests to relevant skills based on the description.
3. Lets the agent read additional reference files on demand.

That includes terminal-based coding agents, IDE-integrated agents,
chat-based agents, and SDK-built custom agents. The skill makes no
assumptions about which model or vendor you use — only about the
skill-loading convention.

The bundled scripts require Python 3.10+, `lxml`, and (for full
validation) `pip install arelle-release`. The skill is useful even
without those dependencies — the references work on their own.

## License

MIT — see [`LICENSE`](LICENSE). Third-party attribution notices are in
[`NOTICE`](NOTICE).

## Disclaimer

This skill is **not** legal, accounting, audit, or filing advice. iXBRL
filings carry regulatory consequence; always verify against the live
publisher source before relying on a specific rule for a regulated
filing. The skill lowers the cost of getting to the right page of the
right manual; it does not replace professional judgement.

## Contributing

Issues and pull requests welcome. Two principles:

1. **Source discipline.** Every new factual claim must cite a primary
   authoritative URL the contributor has actually fetched.
2. **Generality.** This is a public, vendor-neutral skill. No
   product-specific naming, no internal jargon, no jurisdiction-narrow
   shortcuts presented as universal.
