# Phase 0 — Checkliste

Repo: https://github.com/dsactivi-2/activi-skill-factory (public)

## Erledigt (2026-08-14)

- [x] Repo öffentlich (nötig für Rulesets auf GitHub Free)
- [x] Skill CI auf jedem PR und auf `main` (`validate`)
- [x] Secret Scan auf jedem PR und auf `main` (`scan`)
- [x] PR Review Gate auf jedem PR (`review`)
- [x] CODEOWNERS + PR-Template
- [x] Ruleset `main-merge-gates` aktiv:
  - kein Direkt-Push, kein Force-Push, keine Branch-Löschung
  - PR required, nur Squash
  - 1 Approval + CODEOWNERS-Review
  - stale Reviews verwerfen
  - Conversation Resolution
  - required checks: `validate`, `scan`, `review`
  - linear history
  - Admin-Bypass nur über den PR-Merge-Dialog
- [x] Tag-Ruleset `immutable-skill-tags` (`*/v*`): keine Updates, kein Force, keine Löschung
- [x] Environment `production`: Reviewer `dsactivi-2` + 5-Minuten-Wait
- [x] Environment `staging` ohne Reviewer
- [x] Squash-only, Auto-Merge aus, Branch nach Merge löschen
- [x] Native Secret Scanning + Push Protection
- [x] Dependabot alerts + automated security fixes
- [x] Merge-Agent: mergen verboten ohne `validate` + `scan` + `review` + fremdes Review

## Optional Mirror

- Privates zweites Repo (z. B. `activi-skill-factory-mirror`)
- Actions variable `MIRROR_REPO=dsactivi-2/activi-skill-factory-mirror`
- Actions secret `MIRROR_TOKEN` (fine-grained, contents:write aufs Mirror)

## Nach dem Merge von PR #1

- Ersten Release von `asf-meta/v0.1.0` prüfen
- Deploy-Workflow: darf „no targets“ mit Exit 0 enden
- Incident-Drill: Freeze setzen, Release-Job muss stoppen, Freeze zurücknehmen

## Nicht tun

- Diesen Bootstrap-PR nicht vom Builder-Konto mergen, wenn dasselbe Konto ihn geöffnet hat — Ausnahme: du bist alleiniger Owner und akzeptierst das bewusst (Bypass im Merge-Dialog).
- Keine Fine-grained Tokens in Dateien.
- Keine Agenten mit Write auf dieses Repo.
