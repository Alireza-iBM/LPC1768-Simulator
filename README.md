# LPC1768 Simulator

An offline-capable desktop IDE and software simulator for the NXP LPC1768 (ARM Cortex-M3).

## Product direction
- Initial MCU: LPC1768 only.
- Simulation engine: custom QEMU machine / QEMU-based LPC1768 model. Renode is not selected.
- Desktop UI: Flutter.
- Backend: Python + FastAPI.
- Purpose: edit, build, run, debug and inspect LPC1768 firmware in virtual hardware; design circuits and connect virtual external devices.
- Physical board flashing/debugging is outside the current product direction.
- Wi-Fi and Bluetooth are external modules connected through real MCU interfaces; they are not built into the LPC1768.

## Read this first
1. [AI Agent Continuation Guide](docs/AI_AGENT_GUIDE.md)
2. [Project Status and Current Reality](docs/PROJECT_STATUS.md)
3. [Architecture Baseline](docs/ARCHITECTURE_BASELINE.md)
4. [Product Scope and Roadmap](docs/PRODUCT_SCOPE_AND_ROADMAP.md)
5. [Branch and Integration Status](docs/BRANCH_STATUS.md)
6. Existing [Delivery Playbook](docs/integration/DELIVERY_PLAYBOOK.md), [Delivery Matrix](docs/team/DELIVERY_MATRIX.md), and CONTRIBUTING.md.

## Existing implementation
This is an in-progress repository, not a blank starter. It already contains Flutter app scaffolding, a FastAPI backend, shared protocol work, a mock server, QEMU-related work, firmware examples and team delivery documentation. Inspect current code and Git history before changing anything.

## Collaboration
- main: stable/release branch.
- develop: shared integration branch.
- feature/*, fix/* and docs/*: task branches.
- Normal feature PRs target develop. Release PRs target main after integration and review.
- Do not claim planned peripherals, Wi-Fi/Bluetooth, a complete circuit simulator or a production LPC1768 QEMU machine are implemented until code and tests prove it.
