#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo "rollback requested: ${*:-last-known-good}"
if [[ ! -f registry/last-known-good.yaml ]]; then
  echo "ERROR: missing last-known-good pointer" >&2
  exit 1
fi
# Phase 0: no live agents. Record the request and succeed so the
# failure-handler path is exercisable without mutating runtimes.
echo "ok rollback recorded (no live agents in phase 0)"
