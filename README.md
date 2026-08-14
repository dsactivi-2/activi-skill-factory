# ActiVi Skill Factory

Privates System of Record für versionierte AI-Skills.

Nichts schreibt produktiv. Alles läuft **Candidate → Evidence → Build → Eval → PR → Merge → immutable Release → Canary → Rollout**.

Agenten ziehen **nie** `main`. Sie bekommen nur Digest-geprüfte Releases über Subscriptions.

## Rollen

| Rolle | Darf | Darf nicht |
| --- | --- | --- |
| Builder | Branch, Skill-Dateien, Manifest, Changelog | Golden Tests, `main`, mergen |
| Librarian | Katalog, Coverage, Quellen, Coach-Kommentare | Produktiv schreiben, mergen |
| Merge-Agent | PR prüfen, Risk-A mergen wenn CI grün | Eigene Builder-PRs mergen |
| Deploy-Controller | Release lesen, Canary, Health, Rollback | GitHub schreiben, Releases überschreiben |

## Schnellstart (lokal)

```bash
python3 -m pip install --user pyyaml jsonschema
./ci/validate_skills.sh
./ci/security_gate.sh
./ci/run_evals.sh
./ci/package_skills.sh --dry-run
```

## Layout

```text
skills/<id>/     SkillSpec + kompiliertes SKILL.md + Tests
evals/golden/    geschützte Golden Cases (nicht Builder)
registry/        Index, Subscriptions, Last-Known-Good
policies/        Risk, Sources, Security, Freeze
agents/          Librarian, Builder, Merge, Deploy
ci/              Validate, Evals, Package, Release
deploy/          Canary, Health, Rollback
```

## Versionierung

Tag: `<skill-id>/vMAJOR.MINOR.PATCH`  
Risk A → PATCH · B → MINOR · C/Breaking → MAJOR  
Release = Tag + `skill.zip` + Manifest + SHA-256. Nie überschreiben.

## Phase 0 — nach dem Merge (menschlich)

Branch Protection, Environments und Secret Scanning setzt **kein** Agent.
Siehe [docs/PHASE0_CHECKLIST.md](docs/PHASE0_CHECKLIST.md).

## Status

Bootstrap auf `bootstrap/phase-0`. Noch kein automatischer Agent-Rollout an Produktionsagenten.
