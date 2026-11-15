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

- `protocol/` on develop is the single source of truth for REST commands and WebSocket events.
- `apps/desktop_backend/` owns HTTP/WebSocket transport and session orchestration.
- `apps/desktop_backend/app/engine/` owns the backend-facing EngineAdapter interface.
- `engine/qemu/` stores patch series, version pin, scripts, and build notes; do not vendor the entire QEMU source tree.
- `engine/lpc1768/` stores project-owned hardware specifications, mappings, and tests. QEMU implementation patches remain under `engine/qemu/patches/`.
- `apps/flutter_app/` owns UI state and presentation. It must not implement hardware register semantics.
- `apps/flutter_app/lib/board_view/` renders board state from protocol events and mapping data; it must not invent GPIO state.
- `tools/mock_server/` is a development-only fake service. It is not the production backend.

## 3. Contract-first change procedure

Before implementing an API, command, or event, read:
- `protocol/README.md`
- `protocol/commands/commands.json`
- `protocol/events/events.json`
- relevant schema and canonical examples under `protocol/schemas/` and `protocol/examples/`

The existing WebSocket envelope is authoritative:
- `schema_version`
- `type`
- `event_id`
- `session_id`
- `timestamp`
- `payload`

Use the exact event names in `protocol/events/events.json`, including `GPIO_CHANGED`. Do not introduce a second envelope or rename fields. Every event must validate against `protocol/schemas/event.schema.json`.

For every contract change:
1. M6 proposes/updates the schema and example.
2. Affected owners review before implementation.
3. M7 adds schema/contract validation.
4. M3 implements backend behavior; M4/M5 consume the published contract.
5. Breaking changes require an explicit version/migration decision.
6. Never silently change field names, units, or event meaning.

## 4. Pull request rules

- One PR should represent one coherent module/task.
- Keep PRs small enough to review; avoid mixing formatting, refactors, and features.
- PR description states scope, paths, contract version, tests, limitations, and downstream impact.
- At least one reviewer other than the author approves.
- Shared contracts require M6 plus every affected module owner.
- QEMU patch changes require M1 review; hardware behavior changes require M2 review.
- Do not merge on CI failure.
- Prefer squash merge for feature PRs.
- Delete merged feature branches.

## 5. Handoff record template

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
- Test command and actual result:
- Example fixture / event:
- Known limitations:
- Follow-up issue(s):
- Ready for integration: yes/no
```

## 6. Local workflow

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

## 7. QEMU delivery

Do not commit the full QEMU checkout or build directory. Deliver:
- exact upstream QEMU version/tag and source commit,
- ordered patch files,
- patch manifest with SHA256 checksums,
- apply script that fails on a mismatched source tree,
- configure/build/run commands,
- smoke-test firmware or QEMU monitor sequence,
- known limitations.

The receiving member should reproduce the patch on a clean checkout.

## 8. Binary and board asset policy

- Commit source assets and optimized runtime assets only.
- Large editable 3D source files should use Git LFS if required and supported; otherwise use a documented shared artifact location with immutable version/hash.
- Never commit temporary renders, caches, exports, or generated build folders.
- Include preview image and third-party asset license/source note.

## 9. Offline-friendly collaboration

- Keep Git as source of truth; configure a second remote only after verifying its URL and access.
- Push the same branch name and commit SHA to both remotes.
- Do not develop divergent histories independently.
- Record canonical commit SHAs for handoffs.
- Keep schemas, examples, and setup docs in Git for offline use.
