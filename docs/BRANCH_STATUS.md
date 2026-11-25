# Branch and Integration Status

Reviewed against GitHub on 2026-11-25. Refresh after merges.

## Repository
- Repository: Alireza-iBM/LPC1768-Simulator
- Default branch: main
- Main HEAD observed: 198feac7101fa3cd52bb802c8c7ab3597bf8d23e
- Main contains initial desktop backend merge, PR #4.

## Branches observed

| Branch | Observed state | Guidance |
|---|---|---|
| main | Stable baseline; initial FastAPI backend merged | Release branch; do not work directly |
| develop | Shared integration branch; diverged from main | Reconcile; do not blindly fast-forward |
| feature/desktop-backend | Initial backend; PR #4 merged to main | Historical; do not re-merge |
| feature/m3-qemu-process-manager | QemuProcessManager, lifecycle integration and tests; 5 commits ahead/1 behind main | Important pending work; resolve PR #7 conflict before merge |
| feature/m1-qemu-core | Generic Cortex-M3 QEMU PoC and firmware tests | Not proof of complete LPC1768 machine |
| feature/shared-protocol-v1 | Shared protocol baseline; no unique commits ahead of main in comparison | Historical; do not recreate schemas |
| docs/modular-delivery-v1 | Delivery docs/mock server branch; no unique commits ahead of main in comparison | Check current main/develop before copying |
| test/hastishamsini | Test branch; purpose not established | Inspect before use |

## Pull requests observed
- PR #4: feature/desktop-backend to main; merged.
- PR #7: feature/m3-qemu-process-manager to main; opened during this review; GitHub reported mergeable=false. Do not merge until history/conflicts are reconciled and tests run.
- PR #6 titled Develop: open at review time; inspect exact base/head and changed files before acting.
- PR #5: Cortex-M3 QEMU execution PoC; inspect current state before assuming changes are in main.

## Backend merge decision
Do not merge feature/desktop-backend separately: PR #4 already brought that foundation into main.

The process-manager branch descends from the original backend feature and adds process lifecycle/shutdown handling and tests. Preserve it, but PR #7 was not mergeable against main at review time. Resolve by bringing current main into a dedicated integration branch or a reviewed cherry-pick/rebase, then run the full backend test suite. Do not force-push or rewrite the shared branch without owner approval.

The process manager is not a completed QEMU EngineAdapter. Real QEMU execution, firmware loading, QMP/GDB integration and state/event mapping still need separate verification.

## Safe workflow
- Normal task branches from up-to-date develop.
- Feature PRs target develop.
- Release PRs target main only after integration and review.
- Do not delete old branches until their commits are accounted for.
- Never force-push shared branches.
- Before integrating, compare base/head, inspect changed files, check PR status and run tests.
