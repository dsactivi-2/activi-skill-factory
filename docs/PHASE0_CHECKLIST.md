# Phase 0 — Checkliste

Repo: https://github.com/dsactivi-2/activi-skill-factory

GitHub Free + privates Repo: **Rulesets, Branch Protection, Environment
Reviewer und Secret Scanning Push Protection sind plan-gesperrt.** Solange
das so bleibt, gelten die Workflows + Merge-Agent als Gate.

## Erledigt (2026-08-14)

- [x] Skill CI läuft auf jedem PR und auf `main` (`validate`)
- [x] Secret Scan läuft auf jedem PR und auf `main` (`scan`)
- [x] PR Review Gate läuft auf jedem PR (`review`) — Metadaten, Risk, Human-Pfade
- [x] CODEOWNERS + PR-Template
- [x] Environments `production` und `staging` existieren (ohne Reviewer/Wait-Timer)
- [x] Squash-only, Auto-Merge aus, Branch nach Merge löschen
- [x] Dependabot alerts + automated security fixes
- [x] Merge-Agent: mergen verboten ohne `validate` + `scan` + `review` + fremdes Review

## Blockiert ohne GitHub Pro (oder öffentliches Repo)

- [ ] Branch Protection / Ruleset auf `main` (required PR, required checks, 1 Review)
- [ ] Tag-Ruleset `*/v*` immutable
- [ ] Environment `production` required reviewer `dsactivi-2` + Wait-Timer
- [ ] Native Secret Scanning + Push Protection

Wenn du Pro aktivierst: Settings → Branches / Rulesets — Checks `validate`,
`scan`, `review` required; 1 Review; dismiss stale; no force-push.

## Optional Mirror

- Privates zweites Repo (z. B. `activi-skill-factory-mirror`)
- Actions variable `MIRROR_REPO=dsactivi-2/activi-skill-factory-mirror`
- Actions secret `MIRROR_TOKEN` (fine-grained, contents:write aufs Mirror)

## Nach dem Merge von PR #1

- Ersten Release von `asf-meta/v0.1.0` prüfen
- Deploy-Workflow: darf „no targets“ mit Exit 0 enden
- Incident-Drill: Freeze setzen, Release-Job muss stoppen, Freeze zurücknehmen

## Nicht tun

- Diesen Bootstrap-PR nicht vom Builder-Konto mergen, wenn dasselbe Konto ihn geöffnet hat — Ausnahme: du bist alleiniger Owner und akzeptierst das bewusst.
- Keine Fine-grained Tokens in Dateien.
- Keine Agenten mit Write auf dieses Repo.
