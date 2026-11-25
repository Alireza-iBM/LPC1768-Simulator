# Branch and Integration Status

Reviewed against GitHub on 2026-11-25. Refresh after merges.

## Repository
- Repository: Alireza-iBM/LPC1768-Simulator
- Default branch: main
- Main contains PR #4 (initial FastAPI backend) and PR #8 (project/AI-agent continuation baseline).

## Branches observed
| Branch | Observed state | Guidance |
|---|---|---|
| main | Stable baseline; initial FastAPI backend and project continuation docs | Release branch; do not work directly |
| develop | Shared integration branch; diverged from main at review | Reconcile; do not blindly fast-forward |
| feature/desktop-backend | Initial backend; PR #4 merged | Historical; do not re-merge |
| feature/m3-qemu-process-manager | Source branch for QemuProcessManager and backend tests | Preserved; PR #7 superseded/closed; do not delete |
| integration/m3-backend-process-manager | Re-applies the backend process-manager changes on current main | PR #9 pending review and tests |
| feature/m1-qemu-core | Generic Cortex-M3 QEMU PoC and firmware tests | Not proof of a complete LPC1768 machine |
| feature/shared-protocol-v1 | Shared protocol baseline; no unique commits ahead of main in earlier comparison | Historical; inspect before copying |
| docs/modular-delivery-v1 | Delivery docs/mock server branch; no unique commits ahead of main in earlier comparison | Inspect current main/develop before copying |
| docs/ai-agent-continuation-baseline | Documentation branch merged as PR #8 | Historical; its changes are now on main |
| test/hastishamsini | Test branch; purpose not established | Inspect before use |

## Pull requests observed
- PR #4: feature/desktop-backend to main; merged.
- PR #8: AI-agent continuation baseline; merged into main.
- PR #7: original process-manager PR; closed as superseded, not merged. Original source branch preserved.
- PR #9: integration/m3-backend-process-manager to main; open and awaiting review/tests.
- PR #6 titled Develop: open at review time; inspect exact base/head and changed files before acting.
- PR #5: Cortex-M3 QEMU execution PoC; inspect current state before assuming changes are in main.

## Backend integration
The initial backend from PR #4 is already in main. Do not merge feature/desktop-backend again.

The QemuProcessManager and its tests were carried from feature/m3-qemu-process-manager into integration/m3-backend-process-manager, a new branch based on current main. This avoids forcing or rewriting the original shared branch history. PR #9 contains 21 backend files and is intentionally not marked complete.

No CI workflow/status checks were present for PR #9 at the time of review, and a clean local checkout/test run was unavailable in the execution environment. Run the complete backend suite before merging PR #9. Inspect dependency installation, API compatibility, process cleanup and shutdown behavior.

QemuProcessManager is process-lifecycle infrastructure, not a completed QEMU EngineAdapter. Real QEMU execution, firmware loading, QMP/GDB integration and state/event mapping still need separate verification.

## Safe workflow
- Normal task branches from up-to-date develop.
- Feature PRs target develop.
- Release PRs target main only after integration and review.
- Do not delete old branches until commits are accounted for.
- Never force-push shared branches.
- Before integrating, compare base/head, inspect changed files, check PR status and run tests.
