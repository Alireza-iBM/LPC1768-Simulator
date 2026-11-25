# Repository Instructions for AI Coding Agents

Before making any change, read [docs/AI_AGENT_GUIDE.md](docs/AI_AGENT_GUIDE.md).

This repository is an existing LPC1768 IDE and QEMU-based software-simulator project. It is not a blank template.

Mandatory rules:
1. Inspect Git status, branches, recent history and the actual source/tests before editing.
2. Continue from existing work; do not scaffold or rewrite the project from scratch.
3. QEMU is the selected engine. Do not migrate to Renode.
4. Preserve the existing Flutter frontend, FastAPI backend, EngineInterface, shared protocol, tests and team branches.
5. Treat protocol schemas/catalogs/examples as the single source of truth for cross-module APIs/events.
6. Never overwrite another member's work, force-push, reset hard, clean untracked files or delete branches without explicit approval.
7. Do not claim planned features are implemented. Report exact tests and limitations.
8. For the current branch/PR state, read docs/BRANCH_STATUS.md and verify live GitHub state before integration.
9. Do not merge draft/conflicting/unverified PRs. Follow the repository's PR workflow.

If any instruction conflicts with an explicit newer decision from the project owner, stop and ask for clarification rather than guessing.
