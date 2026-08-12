# asf-meta

Meta-Skill für die ActiVi Skill Factory. Erklärt den Lifecycle, die Rollen und die harten Verbote.

## Wann laden

Fragen zu Skill-Build, Release, Merge, Deploy, Freeze, Risk A/B/C oder Repo-Struktur.

## Regeln (kurz)

- SkillSpec ist die Wahrheit; diese Datei ist Compile-Output.
- Candidate → Evidence → Build → Eval → PR → Merge → immutable Release (`asf-meta/vX.Y.Z`) → Canary.
- Agenten ziehen nie `main`.
- Builder ändert keine Golden Tests.
- Merge-Agent merget keine eigenen Builder-PRs.
- Risk A darf bei grüner CI automatisch, B/C brauchen Menschen.
- `policies/freeze.yaml` stoppt Build/Release/Deploy getrennt.

## Quellen

- `src-asf-dossier` (internal, trusted)
- `src-github-actions-docs` (official_docs, trusted)

## Nicht tun

Keine Secrets schreiben. Keine Agenten mit GitHub-Write ausstatten. Keine Release-Tags überschreiben.
