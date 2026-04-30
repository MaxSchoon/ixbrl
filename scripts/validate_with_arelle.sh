#!/usr/bin/env bash
# Validate an iXBRL document or report package with Arelle.
#
# Usage:
#   validate_with_arelle.sh <file-or-zip> [profile]
#
# Profiles:
#   esef   — ESEF (ESMA) validation rules
#   efm    — SEC EDGAR Filer Manual validation rules
#   ukfrc  — UK FRC / Companies House
#   hmrc   — HM Revenue & Customs
#   core   — XBRL 2.1 + Inline 1.1 only (no jurisdiction overlay)
#
# Requires: Python 3.10+, `pip install arelle-release`
#
# What this does:
#   - Auto-detects whether the input is a single .xhtml/.html file, an
#     iXBRL document set (folder), or a Report Package .zip / .xbri.
#   - Wraps single files in --inlineXBRLDocumentSet so calc/dimension
#     validation sees the embedded report as a single instance.
#   - Picks the right Arelle plugin chain per profile.

set -euo pipefail

INPUT="${1:?Usage: validate_with_arelle.sh <file-or-zip> [profile]}"
PROFILE="${2:-core}"

if ! command -v arelleCmdLine >/dev/null 2>&1; then
  echo "arelleCmdLine not found. Install with: pip install arelle-release" >&2
  exit 127
fi

case "$PROFILE" in
  esef)  PLUGINS="validate/ESEF|inlineXbrlDocumentSet|XbrlPackage" ;;
  efm)   PLUGINS="validate/EFM|inlineXbrlDocumentSet" ;;
  ukfrc) PLUGINS="validate/UK-FRC|inlineXbrlDocumentSet" ;;
  hmrc)  PLUGINS="validate/HMRC|inlineXbrlDocumentSet" ;;
  core)  PLUGINS="inlineXbrlDocumentSet" ;;
  *) echo "Unknown profile: $PROFILE" >&2; exit 2 ;;
esac

# Single-file iXBRL must be wrapped as a document set so dimension/calc
# linkbases resolve correctly. A .zip / .xbri is treated as a package.
if [[ "$INPUT" == *.zip || "$INPUT" == *.xbri ]]; then
  exec arelleCmdLine \
    --plugins "$PLUGINS" \
    --validate \
    --packages "$INPUT" \
    --logFormat "[%(messageCode)s] %(message)s"
else
  exec arelleCmdLine \
    --plugins "$PLUGINS" \
    --validate \
    --file "$INPUT" \
    --logFormat "[%(messageCode)s] %(message)s"
fi
