# Factory overview

Vier Rollen: Librarian (Coach/Katalog), Builder (Candidate), Merge-Agent (Risk-Gates), Deploy-Controller (Canary/Rollback).

GitHub ist System of Record. Releases sind immutable. Subscriptions stehen in `registry/agent-subscriptions.yaml`.
