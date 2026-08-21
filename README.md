# iXBRL Skill

An open, primary-source-grounded skill for working with **Inline XBRL (iXBRL)** and the
underlying XBRL stack, covering the major regulators (SEC EDGAR, ESMA
ESEF, UK FRC / Companies House / HMRC, Dutch SBR / KvK / AFM, EBA, EIOPA),
the IFRS Accounting Taxonomy, FASB US-GAAP, and the Arelle validation
toolchain.

Built for the people who actually file: accountants, auditors,
controllers, investor-relations teams, banking and insurance
supervisory-reporting analysts, and the engineers who write the code
that produces their iXBRL.

## What this skill gives you

An agent that reviews a filing has one job: tell you what is wrong, and be
right. Everything here serves that.

The skill is not a library you call. It is knowledge the agent loads when it
needs it, and scripts it runs when knowing is not enough.

### The entry point

`SKILL.md` loads automatically when the skill triggers. It holds the routing
logic, the rules every path shares, and the skill's own attribution and
editing notes, and no domain reference material: match what is in front of the agent to one of four
paths or to the reference index, pin the profile and the period before any
judgment, then go to the reference that answers the question.

It stays under 32 KiB because a file the runtime truncates is a file that lies
to you. Depth lives in `references/`, which load only when the body points at
them. That is the whole design.

### The paths

`SKILL.md` opens with an intake keyed on what is in front of the agent and
routes it to one of four short paths under `paths/`: review a package,
compile a package, diagnose a defect back to its cause in a generator, run
improvement rounds against a corpus. A path holds the order of work, the
reference to load at each step and an observable stop condition, and no
domain facts; the facts live in the references it names.

### The references

Load one. Do not load them all.

| Read this | When you need |
|---|---|
| `first-principles.md` | The eight things that decide whether tagged output is right, in any jurisdiction |
| `spec.md` | Inline XBRL 1.1, XBRL 2.1, XDT, Transformation Registry, calculation semantics |
| `types.md` | QNames, item types, concept attributes |
| `structure.md` | Linkbases, roles, tuples, OIM, instance pointers |
| `dts.md` | How a DTS works and how to read one: discovery, entry points, packages and catalogs, fact to concept to label to statement, six regulator DTSs compared by measurement, valid time vs acceptance window |
| `dimensions.md` | Hypercubes, axes, default members, `xbrldie:*` errors |
| `advanced-specs.md` | Generic links, Functions Registry, Versioning |
| `registries.md` | Label Role Registry, Data Types Registry, URI conventions |
| `taxonomies.md` | Which taxonomy applies, which version, who issues it |
| `esef.md` | ESEF legal basis, anchoring, block tagging, `ESEF.*` codes |
| `esef-block-tags.md` | Every Annex II mandatory block-tag element, both tables |
| `dpm.md` | EBA and EIOPA DPM, Table Linkbase, filing indicators |
| `conversion.md` | Turning a PDF or Word document into faithful iXBRL |
| `viewer.md` | Preparing and driving the Arelle iXBRL Viewer for review |
| `validation.md` | Arelle CLI, plugins, Calc 1.1, and every error code with its cause and fix |

### The jurisdictions

One file per regime, under `references/jurisdictions/`. Each opens with a
profile table, because most jurisdictions run more than one filing regime and
picking the wrong one wastes the whole review, and each carries a *DTS and
vintages* table: the releases, their entry points and packages, the
financial years they are for, and the deposit window in which the receiver
accepts them, with a source per row.

| File | Regime |
|---|---|
| `nl-sbr.md` | KvK Handelsregister, AFM, SBR Dutch GAAP |
| `uk-frc.md` | Companies House, HMRC CT600, FCA/UKSEF, Irish Revenue |
| `sec-edgar.md` | SEC EDGAR, EFM, operating companies and funds |
| `dk-erst.md` | Erhvervsstyrelsen, ÅRL, Regnskab channels, DKFIN |
| `fi-prh.md` | PRH digital financial statements |
| `de-hgb.md` | E-Bilanz, Offenlegung, ESEF via BaFin |
| `fr-amf.md` | AMF ESEF, and the French obligations that are not XBRL |
| `be-nbb.md` | NBB Central Balance Sheet Office, FSMA, Biztax |

A jurisdiction that has no XBRL obligation says so plainly. That is worth as
much as a rule, and harder to find.

### The scripts

Knowing the rules is not the same as checking the file. Three scripts do that.

| Script | Catches | Cost |
|---|---|---|
| `scripts/check_facts.py` | Missing `decimals`, dangling continuation chains, undefined contexts and units, non-ISO currency measures, a finite `decimals` that zeroes reported digits | Milliseconds, no network, standard library plus `lxml` |
| `scripts/dts_profile.py` | What the taxonomy actually declares: unresolved `schemaRef`s and locators, concepts by type and period, label roles and languages, calculation arcrole (1.0 vs 1.1), dimensions and `targetRole`, presentation depth; and everything the DTS says about one concept (`--concept`) | Seconds from a package offline; minutes for a first online walk of US-GAAP, cached after |
| `scripts/validate_with_arelle.sh` | Everything the regulator's own validator catches | An Arelle run |

Run the cheap one first. It finds the errors that would waste an Arelle cycle,
and it never touches the network.

### The scaffolds

`assets/` holds a complete, valid iXBRL skeleton with its extension schema and
all four linkbases, plus a taxonomy package and catalog. They are not
illustrations. They pass `xmllint`, and CI keeps them passing, because a broken
example teaches the wrong thing with total confidence.

## Source discipline

Every factual claim in this skill is tied to a primary source from the
issuer or standard-setter (xbrl.org, ifrs.org, esma.europa.eu, sec.gov,
fasb.org, frc.org.uk, sbr-nl.nl, eba.europa.eu, eiopa.europa.eu,
Arelle's GitHub repositories, and the Arelle iXBRL Viewer
documentation). Each `references/*.md` ends with a
`Sources` list of the URLs consulted. Versions and rule numbers were
verified at the time of writing; re-check the publisher's page before
relying on a specific version for a regulated filing.

## Install

This is an AI-agent skill: a self-contained directory of markdown and
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

skills.sh has no separate submission step; its directory is populated
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
assumptions about which model or vendor you use, only about the
skill-loading convention.

The bundled scripts require Python 3.10+, `lxml`, and (for full
validation) `pip install arelle-release`. The skill is useful even
without those dependencies; the references work on their own.

## License

Dual-licensed by content type: **Apache-2.0** for code (`scripts/`,
`tests/`; see [`LICENSE`](LICENSE)) and **CC BY 4.0** for content
(`SKILL.md`, `references/`, `assets/`; see
[`LICENSE-CONTENT`](LICENSE-CONTENT)).

**If you redistribute or publicly share this material, or an adaptation of it**,
attribution is a licence condition (CC BY 4.0 §3(a), Apache-2.0 §4):

> iXBRL Skill by Max Schoon (Doc2iXBRL), https://github.com/MaxSchoon/ixbrl,
> licensed under CC BY 4.0. [Modified. | Unmodified.]

**If you use it** (to review filings, generate report packages, or inform
software you write yourself), you must credit it:

> Uses the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — https://doc2ixbrl.com

Exact rules per context, including when *not* to stamp a filing, are in
[`ATTRIBUTION.md`](ATTRIBUTION.md). Machine-readable terms: [`rsl.xml`](rsl.xml)
(RSL 1.0) and [`llms.txt`](llms.txt).

Previously published under MIT; see [`NOTICE`](NOTICE) for the relicensing
history and what it does and does not change. Third-party notices are in
[`NOTICE`](NOTICE).

## Disclaimer

This skill is **not** legal, accounting, audit, or filing advice. iXBRL
filings carry regulatory consequence; always verify against the live
publisher source before relying on a specific rule for a regulated
filing. The skill lowers the cost of getting to the right page of the
right manual; it does not replace professional judgement.

## Contributing

Issues and pull requests welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md)
for the full workflow, the [issue templates](.github/ISSUE_TEMPLATE) for the
right place to file, and [`SUPPORT.md`](SUPPORT.md) for where to get help. Two
principles govern every change:

1. **Source discipline.** Every new factual claim must cite a primary
   authoritative source: a spec section or a regulator publication URL the
   contributor has actually fetched.
2. **Generality.** This is a public, openly licensed skill. No
   product-specific naming, no internal jargon, no jurisdiction-narrow
   shortcuts presented as universal.

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md). To
report a security or filing-integrity problem privately, see
[`SECURITY.md`](SECURITY.md).

## Contact

Questions, collaboration, or corrections: **contact@doc2ixbrl.com**. For
anything that could affect filing integrity (a rule or scaffold in the
skill that would produce a non-compliant filing), please report it
privately (see [`SECURITY.md`](SECURITY.md)) before opening a public
issue.
