# Local Development Workflow

## One-time clone

```bash
git clone https://github.com/Alireza-iBM/LPC1768-Simulator.git
cd LPC1768-Simulator
git remote -v
git switch develop
```

If `develop` does not exist yet, the project lead must create it from the approved baseline before contributors begin shared integration.

## Start a task

```bash
git switch develop
git pull --ff-only origin develop
git switch -c feature/M4-dashboard-api
```

Replace the branch suffix with your member ID and task.

## Keep your branch current

```bash
git fetch origin
git rebase origin/develop
```

If a rebase becomes confusing, stop and ask for help; do not force-push shared branches.

## Before push

```bash
git status --short
git diff --check
git diff --stat
git add <only-related-paths>
git commit -m "feat(<module>): <short description>"
git push -u origin HEAD
```

## Pull request

- Base: `develop`
- Compare: your feature branch
- Include handoff details from `docs/integration/DELIVERY_PLAYBOOK.md`.
- Wait for review and required checks.
- Do not merge your own PR unless explicitly authorized by project policy.

## Offline / secondary remote

Use a secondary remote only if the project lead has announced its canonical URL:

```bash
git remote add backup <approved-remote-url>
git fetch backup
git push backup HEAD
```

Do not change `origin` or push to an unverified remote. Compare branch tips before switching remotes.

## Troubleshooting

- Wrong branch: `git branch --show-current`
- Uncommitted changes: `git status`
- Changed files: `git diff --name-only`
- Remote configuration: `git remote -v`
- Commit identity: `git config user.name` and `git config user.email`
