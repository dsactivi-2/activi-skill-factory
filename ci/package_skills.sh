#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ "${1:-}" == "--dry-run" ]]; then
  python3 ci/asf.py package --dry-run
else
  python3 ci/asf.py package
fi
