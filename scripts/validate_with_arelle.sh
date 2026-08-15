#!/usr/bin/env bash
# Validate an iXBRL document or report package with Arelle.
#
# Usage:
#   validate_with_arelle.sh <file-or-zip> [profile] [extra arelleCmdLine args...]
#
# Profiles:
#   esef   — ESEF (ESMA) validation rules
#   efm    — SEC EDGAR Filer Manual validation rules
#   ukfrc  — UK FRC / Companies House (HMRC joint-filing disclosure system)
#   hmrc   — HM Revenue & Customs (same gate; JFCVC/HMRC checks)
#   dk     — Denmark Erhvervsstyrelsen (ÅRL; DBA disclosure system)
#   core   — XBRL 2.1 + Inline 1.1 only (no jurisdiction overlay)
#
# Extra args are passed through to arelleCmdLine — e.g. a local taxonomy
# package for offline DTS resolution:
#   validate_with_arelle.sh statements.xhtml core --packages sbr-taxonomy.zip
# or a Danish vintage override:
#   validate_with_arelle.sh report.xhtml dk --disclosureSystem arl-2024-multi-target-preview
#
# Requires: Python 3.10+, `pip install arelle-release`
#
# What this does:
#   - Accepts a single .xhtml/.html file, an iXBRL document set folder, or
#     a Report Package .zip / .xbri through Arelle's --file entry point.
#   - Loads the inlineXbrlDocumentSet plugin so calc/dimension validation
#     sees embedded reports as a single instance.
#   - Picks the right Arelle plugin chain per profile, and selects the
#     plugin's disclosure system where the plugin gates its checks on one
#     (validate/UK runs its JFCVC/HMRC checks only under the `hmrc`
#     disclosure system; validate/DBA under an `arl-*` system).

set -euo pipefail

INPUT="${1:?Usage: validate_with_arelle.sh <file-or-zip> [profile] [extra args...]}"
PROFILE="${2:-core}"
shift $(( $# >= 2 ? 2 : 1 ))

if ! command -v arelleCmdLine >/dev/null 2>&1; then
  echo "arelleCmdLine not found. Install with: pip install arelle-release" >&2
  exit 127
fi

EXTRA_ARGS=()
case "$PROFILE" in
  esef)  PLUGINS="validate/ESEF|inlineXbrlDocumentSet|XbrlPackage" ;;
  efm)   PLUGINS="validate/EFM|inlineXbrlDocumentSet" ;;
  ukfrc) PLUGINS="validate/UK|inlineXbrlDocumentSet"
         EXTRA_ARGS+=(--disclosureSystem hmrc) ;;
  hmrc)  PLUGINS="validate/UK|inlineXbrlDocumentSet"
         EXTRA_ARGS+=(--disclosureSystem hmrc) ;;
  dk)    PLUGINS="validate/DBA|inlineXbrlDocumentSet"
         EXTRA_ARGS+=(--disclosureSystem arl-2025-multi-target-preview) ;;
  core)  PLUGINS="inlineXbrlDocumentSet" ;;
  *) echo "Unknown profile: $PROFILE" >&2; exit 2 ;;
esac

exec arelleCmdLine \
  --plugins "$PLUGINS" \
  --validate \
  --file "$INPUT" \
  --logFormat "[%(messageCode)s] %(message)s" \
  ${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"} \
  "$@"
