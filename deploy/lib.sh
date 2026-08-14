#!/usr/bin/env bash
# shared helpers for deploy/*.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 - <<'PY'
from pathlib import Path
import sys
import yaml
root = Path(".")
freeze = yaml.safe_load((root / "policies" / "freeze.yaml").read_text())
if freeze.get("deployment_freeze"):
    print(f"ERROR: deployment_freeze is true ({freeze.get('reason') or 'no reason'})", file=sys.stderr)
    sys.exit(1)
subs = yaml.safe_load((root / "registry" / "agent-subscriptions.yaml").read_text()) or {}
agents = subs.get("agents") or {}
n = 0
for agent, body in agents.items():
    for skill, spec in (body.get("skills") or {}).items():
        if spec.get("auto_update"):
            n += 1
Path("dist").mkdir(exist_ok=True)
Path("dist/deploy-targets.txt").write_text(str(n) + "\n")
print(f"eligible auto-update bindings: {n}")
PY
