# Contribution Guidelines

## Branches
- main: stable versions only
- develop: shared development branch
- feature/<member>-<task>: individual work branches
- fix/<member>-<task>: bug fixes

## Rules
1. Never commit directly to main or develop.
2. Each task must have a clear owner.
3. Every feature must be tested before opening a Pull Request.
4. All API and event changes must follow protocol/schemas.
5. Do not commit build outputs, binaries, secrets or local configuration.
6. Pull Requests must target develop.
7. At least one other team member must review a Pull Request.
8. Resolve merge conflicts locally before requesting final approval.
9. Do not silently change shared interfaces.
10. Mock implementations must be clearly identified and replaceable.

## Pull Request checklist
- [ ] Scope is clear
- [ ] Tests pass
- [ ] Protocol compatibility checked
- [ ] No unrelated changes
- [ ] Documentation updated
- [ ] Mock behavior identified, if applicable
