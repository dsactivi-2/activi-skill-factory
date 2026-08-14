## Change

- **Skill:**
- **Mode:** BUILD_NEW / UPDATE_EXISTING / POLICY / META
- **Risk:** A / B / C
- **Run ID:**
- **Base version → target version:**

## Evidence

- Source IDs:
- Claims (kurz):
- Primärquelle:

## Erwartete Wirkung

-

## Evals

- [ ] Golden unverändert (oder separater Human-PR)
- [ ] `./ci/validate_skills.sh`
- [ ] `./ci/security_gate.sh`
- [ ] `./ci/run_evals.sh`
- [ ] `./ci/package_skills.sh --dry-run`

## Gates

- [ ] Kein Freeze aktiv
- [ ] Keine Secrets/PII
- [ ] Builder ≠ Merger
- [ ] Risk C: Human + production environment

## Rollback

Last-known-good Ziel:
