# Phase 0 — menschliche Checkliste

Der Bootstrap-Agent darf diese Schritte **nicht** selbst setzen. Einmal im GitHub-UI (oder via Org-Admin) erledigen, **bevor** Auto-Merge oder Agent-CD angehen.

Repo: https://github.com/dsactivi-2/activi-skill-factory

## 1. Branch Protection für `main`

Settings → Rules → Rulesets (bevorzugt) oder Branch protection:

- keine direkten Pushes auf `main`
- Pull Request required
- required checks: `validate` (Skill CI)
- 1 Review für alles außer reinen Docs; Risk B/C immer Review
- dismiss stale reviews
- keine Self-Approval
- linear history, squash merge only
- force push aus, deletions aus

## 2. Tag-Ruleset

- Pattern: `*/v*`
- immutable / no force update
- nur `github-actions[bot]` oder Release-Job darf Tags anlegen

## 3. Environments

- `staging` — optional, keine Reviewer nötig
- `production` — required reviewers: `dsactivi-2`
- Wait timer nach Bedarf (z. B. 5 min für Deploy)

Der Release- und Deploy-Workflow referenziert `environment: production`.
Ohne Environment schlagen die Jobs fehl — das ist Absicht.

## 4. Security

- Secret scanning an
- Push protection an
- Dependabot alerts an (Config liegt unter `.github/dependabot.yml`)

## 5. Optional Mirror

- Privates zweites Repo anlegen (z. B. `activi-skill-factory-mirror`)
- Actions variable `MIRROR_REPO=dsactivi-2/activi-skill-factory-mirror`
- Actions secret `MIRROR_TOKEN` (fine-grained, contents:write aufs Mirror)

## 6. Nach dem Merge dieses PRs

- Ersten Release von `asf-meta/v0.1.0` prüfen
- Deploy-Workflow: darf „no targets“ mit Exit 0 enden
- Incident-Drill: Freeze setzen, Release-Job muss stoppen, Freeze zurücknehmen

## Nicht tun

- Diesen Bootstrap-PR nicht vom Builder-Konto mergen, wenn dasselbe Konto ihn geöffnet hat — Ausnahme: du bist alleiniger Owner und akzeptierst das bewusst.
- Keine Fine-grained Tokens in Dateien.
- Keine Agenten mit Write auf dieses Repo.
