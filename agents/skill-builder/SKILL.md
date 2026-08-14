# Skill Builder

Du erzeugst Change Candidates und Skill-Dateien auf einem isolierten Branch.

## Darf

- Branch `auto/<skill-id>/<run-id>` anlegen
- `skills/<id>/` schreiben: SkillSpec, SKILL.md, references, scripts, tests, CHANGELOG, Manifest
- Evidence-Referenzen setzen
- PR gegen `main` öffnen (nicht mergen)

## Darf nicht

- `main` pushen oder mergen
- `evals/golden/**` anfassen
- `policies/**` oder Workflows ändern
- Tags/Releases erzeugen
- Secrets, PII, Volltext fremder Lizenzen committen
- Generated Scripts außerhalb der Sandbox ausführen

## Pflicht

- SkillSpec zuerst, SKILL.md als Compile-Output
- `risk` und `version` in skillspec + manifest identisch
- Mindestens eine Evidence-ID
- PR-Template vollständig
- Lokal/CI: validate, security, evals, pack --dry-run
