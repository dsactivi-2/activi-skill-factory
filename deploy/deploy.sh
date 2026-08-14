#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# shellcheck disable=SC1091
source deploy/lib.sh
stage="${1:-}"
if [[ "${stage}" != "--stage" ]]; then
  echo "usage: $0 --stage canary|progressive" >&2
  exit 2
fi
stage_name="${2:?stage name required}"
targets="$(tr -d '[:space:]' < dist/deploy-targets.txt || echo 0)"
if [[ "${targets}" == "0" ]]; then
  echo "ok deploy ${stage_name} (no targets)"
  exit 0
fi
echo "ERROR: production targets exist but deploy controller is not wired yet" >&2
exit 1
