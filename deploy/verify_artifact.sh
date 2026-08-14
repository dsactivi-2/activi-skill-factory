#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# shellcheck disable=SC1091
source deploy/lib.sh
targets="$(tr -d '[:space:]' < dist/deploy-targets.txt || echo 0)"
if [[ "${targets}" == "0" ]]; then
  echo "ok verify_artifact (no targets — skip digest)"
  exit 0
fi
echo "ERROR: production targets exist but artifact verify is not wired yet" >&2
exit 1
