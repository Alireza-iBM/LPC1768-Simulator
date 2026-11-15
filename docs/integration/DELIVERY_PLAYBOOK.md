# Modular Delivery Playbook

## 1. Source of truth

- `main`: stable, demonstrable releases only.
- `develop`: shared integration branch.
- `feature/<member>-<short-task>`: normal work.
- `fix/<member>-<short-task>`: bug fixes.
- `docs/<short-task>`: documentation/process changes.
- `hotfix/<short-task>`: urgent release fixes, merged to main and back to develop.

Never work directly on `main` or `develop`. All PRs target `develop`, except release/hotfix PRs explicitly approved by the project lead.

## 2. Keep module boundaries clear

- `protocol/` is the contract source of truth, not a duplicate of implementation code.
- `apps/desktop_backend/` owns HTTP/WebSocket transport and session orchestration.
- `apps/desktop_backend/app/engine/` owns the backend-facing EngineAdapter interface.
- `engine/qemu/` stores patch series, scripts, version pin, and build notes; do not vendor the entire QEMU source tree.
- `engine/lpc1768/` stores project-owned hardware specifications, mappings, and tests. QEMU implementation patches remain under `engine/qemu/patches/`.
- `apps/flutter_app/` owns UI state and presentation. It must not implement hardware register semantics.
- `apps/flutter_app/lib/board_view/` renders board state from protocol events and mapping data; it must not invent GPIO state.
- `tools/mock_server/` is a development-only fake service. It is not the production backend.

## 3. Contract-first change procedure

For every REST route, command, or WebSocket event:
1. M6 proposes/updates the schema and example under `protocol/`.
2. Affected owners review the change before implementation.
3. M7 adds schema/contract validation.
4. M3 implements backend behavior; M4/M5 consume the published contract.
5. If a change is breaking, increment protocol major version and document migration. Additive optional fields may be minor changes. Bug fixes/documentation are patch changes.
6. Never silently rename fields, change units, or change event meaning.

Every message should carry:
- `protocol_version`
- `type`
- `message_id`
- `timestamp` (UTC ISO-8601)
- `session_id` when session-scoped
- `payload`

Use event names in the form `domain.resource_action`, e.g. `gpio.pin_changed`.

## 4. Pull request rules

- One PR should represent one coherent module/task.
- Keep PRs small enough to review; avoid mixing formatting, refactors, and features.
- PR description must state scope, paths, contract version, tests, screenshots/logs where useful, limitations, and downstream impact.
- At least one reviewer other than the author approves.
- Shared contracts require M6 plus every affected module owner.
- QEMU patch changes require M1 review; hardware behavior changes require M2 review.
- Do not merge on CI failure.
- Prefer squash merge for feature PRs to keep history readable.
- Delete merged feature branches.

## 5. Handoff record template

Copy this into the PR description or issue:

```markdown
## Handoff
- Module / task:
- Sending owner:
- Receiving owner(s):
- PR / commit:
- Contract version:
- Files and public interfaces changed:
- Clean checkout setup:
- Run command:
- Test command and result:
- Example fixture / event:
- Known limitations:
- Follow-up issue(s):
- Ready for integration: yes/no
```

## 6. Local setup and commands

From repository root:

```bash
git switch develop
git pull --ff-only origin develop
git switch -c feature/M3-session-api
```

Before opening PR:

```bash
git status --short
git diff --check
```

Run the checks documented by the touched module. Do not claim a test passed unless it was actually run.

After merge:

```bash
git switch develop
git pull --ff-only origin develop
git branch -d feature/M3-session-api
```

## 7. QEMU delivery specifically

Do not commit the full QEMU checkout or build directory.
Deliver:
- exact upstream QEMU version/tag and source commit,
- ordered patch files,
- patch manifest with SHA256 checksums,
- apply script that fails on a mismatched source tree,
- configure/build/run commands,
- smoke-test firmware or QEMU monitor command sequence,
- known limitations.

The receiving member should be able to reproduce the patch on a clean checkout.

## 8. Binary and board asset policy

- Commit source assets and optimized runtime assets only.
- Large editable 3D source files should use Git LFS if they are genuinely required in the repository and the team has LFS access; otherwise use a documented shared artifact location and record immutable version/hash.
- Never commit temporary renders, caches, exports, or generated build folders.
- Include a small preview image and a license/source note for third-party assets.

## 9. Offline-friendly collaboration

Because connectivity to GitHub may be unreliable:
- Keep Git as the source of truth; configure a second remote only after verifying its URL and access.
- Push the same branch name and commit SHA to both remotes.
- Do not independently develop divergent histories on two remotes.
- Use signed release tags or recorded commit SHAs to identify the canonical handoff.
- Keep schema/examples and setup docs in the repository so work can continue offline after clone.
