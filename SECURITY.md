# Security

## Melden

Sicherheitsprobleme **nicht** als öffentliches Issue. Direkt an den Repo-Owner (`dsactivi-2`).

## Grenzen

- Skills und Evidence dürfen keine Secrets, Tokens oder PII enthalten.
- Generated Scripts laufen nur in der CI-Sandbox: kein Netzwerk, Timeout, kein Secret-Env.
- Agent-Runtimes bekommen keine GitHub-Write-Tokens.
- Production nutzt nur immutable Releases (Tag + SHA-256), nie `main`.

## Gates

Jeder PR durchläuft `ci/security_gate.sh`:

- bekannte Secret-Muster
- private Key-Header
- Freeze-Datei syntaktisch gültig
- keine Schreibversuche auf `evals/golden/` durch Builder-Pfade (PR-Label / Pfadcheck)

Risk-C-Änderungen brauchen menschliches Review und das Environment `production`.

## Incident

1. `policies/freeze.yaml` → betroffene Flag auf `true`
2. Rollouts stoppen, Last-Known-Good wiederherstellen
3. Artifact/Source quarantänen, Release als `blocked` markieren — nie überschreiben
4. Audit: Run-ID, SHA, Manifest, Source-Snapshot
