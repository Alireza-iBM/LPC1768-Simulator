
#!/usr/bin/env bash

set -e

PROJECT_NAME="LPC1768-Simulator"

echo "Creating $PROJECT_NAME project structure..."

# Application directories
mkdir -p apps/flutter_app/lib/core
mkdir -p apps/flutter_app/lib/features
mkdir -p apps/flutter_app/lib/simulator
mkdir -p apps/flutter_app/lib/board_view
mkdir -p apps/flutter_app/lib/settings
mkdir -p apps/flutter_app/test

mkdir -p apps/desktop_backend/app/api
mkdir -p apps/desktop_backend/app/websocket
mkdir -p apps/desktop_backend/app/sessions
mkdir -p apps/desktop_backend/app/engine
mkdir -p apps/desktop_backend/app/adapters
mkdir -p apps/desktop_backend/app/services
mkdir -p apps/desktop_backend/tests

# QEMU and LPC1768 engine
mkdir -p engine/qemu/patches
mkdir -p engine/qemu/scripts

mkdir -p engine/lpc1768/memory
mkdir -p engine/lpc1768/gpio
mkdir -p engine/lpc1768/nvic
mkdir -p engine/lpc1768/timers
mkdir -p engine/lpc1768/uart

mkdir -p engine/common/registers
mkdir -p engine/common/events
mkdir -p engine/common/debug

# Shared protocol and mock data
mkdir -p protocol/schemas
mkdir -p protocol/commands
mkdir -p protocol/events
mkdir -p protocol/examples
mkdir -p protocol/mock_data

# Firmware examples
mkdir -p firmware/examples/minimal_startup
mkdir -p firmware/examples/gpio_output
mkdir -p firmware/examples/gpio_input
mkdir -p firmware/examples/led_blink
mkdir -p firmware/examples/external_interrupt
mkdir -p firmware/linker_scripts

# Tests
mkdir -p tests/engine
mkdir -p tests/hardware
mkdir -p tests/backend
mkdir -p tests/frontend
mkdir -p tests/integration
mkdir -p tests/fixtures

# Scripts
mkdir -p scripts

# Documentation
mkdir -p docs/architecture
mkdir -p docs/api
mkdir -p docs/hardware
mkdir -p docs/integration
mkdir -p docs/team
mkdir -p docs/development

# Application package placeholders
touch apps/flutter_app/README.md
touch apps/desktop_backend/README.md
touch apps/desktop_backend/requirements.txt
touch apps/desktop_backend/app/__init__.py

# Engine documentation
touch engine/qemu/README.md
touch engine/lpc1768/README.md
touch engine/common/README.md

# Firmware documentation
touch firmware/README.md

# Root documentation
touch docs/architecture/README.md
touch docs/api/README.md
touch docs/hardware/README.md
touch docs/integration/README.md
touch docs/team/README.md
touch docs/development/README.md

# Protocol placeholders
touch protocol/schemas/README.md
touch protocol/commands/README.md
touch protocol/events/README.md
touch protocol/examples/README.md
touch protocol/mock_data/README.md

# Test documentation
touch tests/README.md

# Root README
cat > README.md <<'EOF'
# LPC1768 Simulator

An offline desktop simulator for the NXP LPC1768 microcontroller
based on the ARM Cortex-M3 architecture.

## Platforms
- Windows
- Linux

## Architecture
- Flutter Desktop frontend
- Python FastAPI backend
- Custom QEMU-based LPC1768 machine and hardware model
- Shared protocol and mock data

## Project Status
MVP development.

See CONTRIBUTING.md for development and integration rules.
EOF

# Contribution rules
cat > CONTRIBUTING.md <<'EOF'
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
EOF

# Git ignore
cat > .gitignore <<'EOF'
# OS
.DS_Store
Thumbs.db
Desktop.ini

# Editors
.vscode/
.idea/
*.swp
*.swo

# Python
__pycache__/
*.py[cod]
.venv/
venv/
.env
.pytest_cache/
.mypy_cache/
.ruff_cache/
dist/
build/
*.egg-info/

# Flutter / Dart
.dart_tool/
.packages
.pub-cache/
.pub/
.flutter-plugins
.flutter-plugins-dependencies
.flutter-plugins
build/

# C / C++ / QEMU
*.o
*.a
*.so
*.dll
*.exe
*.elf
*.hex
*.bin
*.map
*.d
*.su

# Keil / IDE outputs
Objects/
Listings/
*.uvguix.*
*.uvoptx
*.uvprojx.user

# Logs and temporary files
*.log
*.tmp
*.bak

# Local configuration and credentials
.env.*
!.env.example
secrets/
credentials/
EOF

# Shared ownership and integration document
cat > docs/team/OWNERSHIP.md <<'EOF'
# Module Ownership

| Member | Module | Main directory |
|---|---|---|
| M1 | QEMU Core / CPU | engine/qemu |
| M2 | LPC1768 Hardware Model | engine/lpc1768 |
| M3 | Desktop Backend | apps/desktop_backend |
| M4 | Flutter Frontend | apps/flutter_app |
| M5 | Hardware Visualization | apps/flutter_app/lib/board_view |
| M6 | Protocol & Integration | protocol, docs/integration |
| M7 | QA / Validation / Release | tests, scripts, docs/development |

Module ownership does not mean exclusive access.
Shared interface changes must be reviewed with the affected owners.
EOF

# Keep empty directories visible to Git
find . -type d -empty -exec touch {}/.gitkeep \;

echo
echo "Project structure created successfully."
echo "Next: review the generated structure and initialize Git."
