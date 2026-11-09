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
