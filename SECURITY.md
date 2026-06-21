# Security Policy

This repository is an AI-agent skill: markdown reference material, runnable
iXBRL/XBRL scaffolds (`assets/`), and small, dependency-light Python and
shell validation helpers (`scripts/`). It executes no network calls on its
own and ships no secrets. The realistic risk surface is:

1. **Filing-integrity defects** — a rule, instruction, or scaffold in the
   skill that would lead an agent (or a person) to produce a **non-compliant**
   iXBRL/XBRL filing for any supported regulator (SEC EDGAR, ESMA ESEF, UK
   FRC / Companies House / HMRC, Dutch SBR / KvK / AFM, EBA, EIOPA). We treat
   these with the same seriousness as a security bug, because the downstream
   consequence is regulatory.
2. **Scaffold safety** — a template in `assets/` that passes `xmllint` /
   Arelle locally but produces output a regulator's validator rejects, or
   that resolves cross-file references to the wrong target.
3. **Script safety** — any way `scripts/check_facts.py` or
   `scripts/validate_with_arelle.sh` could be made to do something unexpected
   with a crafted input document.
4. **Supply chain** — the GitHub Actions workflows and their pinned actions.

## Reporting a vulnerability

**Please do not open a public issue for a security or filing-integrity
problem.** Instead, use one of:

- **GitHub private vulnerability reporting** — the "Report a vulnerability"
  button under the repository's **Security** tab (preferred; keeps the
  report private until a fix ships).
- **Email** — **contact@doc2ixbrl.com**, subject line starting `SECURITY:`.

Include: what's wrong, the file/line or validator code involved, the impact
(e.g. "would produce an ESEF filing that fails `ESEF.2.2.1`"), and a
primary-source citation (spec section or regulator publication) if the issue
is a correctness/compliance claim.

## What to expect

- Acknowledgement within a few working days.
- An assessment, and — for confirmed issues — a fix on a private branch,
  merged once verified.
- Credit in the release notes if you'd like it (tell us your preferred name).

## Scope notes

This skill is **not** legal, accounting, audit, or filing advice (see the
README disclaimer). A report that the skill is "not a substitute for an
auditor" is out of scope; a report that a specific rule, scaffold, or
instruction is **wrong** and would cause a non-compliant filing is firmly in
scope.
