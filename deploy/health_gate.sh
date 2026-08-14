#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# shellcheck disable=SC1091
source deploy/lib.sh
stage="${2:-unknown}"
targets="$(tr -d '[:space:]' < dist/deploy-targets.txt || echo 0)"
if [[ "${targets}" == "0" ]]; then
  echo "ok health ${stage} (no targets)"
  exit 0
fi
echo "ERROR: production targets exist but health gate is not wired yet" >&2
exit 1
