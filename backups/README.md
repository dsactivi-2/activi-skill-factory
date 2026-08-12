# Backups

Drei Ebenen:

1. **Git** — dieses private Repo ist System of Record. Kein Force-Push auf `main`/Tags.
2. **Nächtliches Bundle** — Workflow `backup-mirror.yml` legt `git bundle` + Tree-Tarball 90 Tage als Artifact ab.
3. **Optionaler Mirror** — zweites privates Repo via `MIRROR_REPO` + `MIRROR_TOKEN`.

Release-Zips bleiben am GitHub Release. Last-known-good steht in `registry/last-known-good.yaml`.
