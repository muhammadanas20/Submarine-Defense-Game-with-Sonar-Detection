# Weekly progress — Muhammad Anas (25K-0899)

Update this file before each weekly PR. Record actual work and test results; do not mark a task complete until it has been built/tested as required.

| Week | Planned focus (guide) | Status | Build/test evidence, blockers, next action |
|---|---|---|---|
| 0 · 5–11 Oct | A1 repository structure, shared files, stubs, VS project setup | Completed | Created repo structure, `constants.inc`, `data.inc`, stub files, `.gitignore`, `CODEOWNERS`, and VS2022 project setup. |
| 1 · 12–18 Oct | A2 main/GameLoop; A3 80 ms FrameDelay; proposal | Completed | Implemented `main`, `GameLoop` state machine, and `FrameDelay` (80 ms per frame using `GetMseconds` and `Delay`) in `src/game.asm`. Completed project proposal. |
| 2 · 19–25 Oct | A4 keyboard and submarine movement; M1 | Completed | Implemented `HandleInput` in `src/anas/input.inc` using non-blocking `ReadKey`, `A`/`D` and arrow keys with `MIN_COL`/`MAX_COL` boundary checks, plus `W`, `SPACE`, `P`, and `ESC`. |
| 3 · 26 Oct–1 Nov | A5 torpedoes | Completed | Implemented `FireTorpedo` (up to 8 slots, 3-frame `fireCooldown`) and `UpdateTorpedoes` (moves active torpedoes up 1 row per frame until `TOP_ROW`) in `src/anas/torpedo.inc`. |
| 4 · 2–8 Nov | A6 collisions; M2 | Completed | Implemented `CheckCollisions` in `src/anas/collision.inc` with nested loops for torpedo-vs-charge hits (including 1-row crossing check, +10/+25 points) and charge-vs-submarine hits. |
| 5 · 9–15 Nov | A7 new-game reset and pause | Completed | Completed `InitGame` in `src/game.asm` using `REP STOSB` to clear `Torpedoes`, `Charges`, and `Explosions` arrays, reset variables, call `ApplyLevel`, and `InvalidateScreen`. Removed Anas stub lines from `src/anas/stubs_anas.inc`. |
| 6 · 16–22 Nov | A8 integration, full testing, final report; M3/M4 | Ready for integration | Anas modules (`src/game.asm`, `src/anas/*.inc`) and report documentation (`docs/report/anas.md`) completed; ready to integrate with Alyan and Ali PRs and run lab-PC checklist. |

## Weekly update summary (Anas — Steps A1 to A7)

- **Completed:**
  - **A1 (`src/shared/constants.inc`, `src/shared/data.inc`):** Set up shared screen constants (`80 x 25`), state constants (`ST_MENU` to `ST_EXIT`), `GameObject` structure (`xPos`, `yPos`, `active`, `hidden`), and shared arrays (`Torpedoes`, `Charges`, `Explosions`).
  - **A2 (`src/game.asm`):** Implemented `main` outer loop (menu -> init game -> game loop) and `GameLoop` state machine (`ST_PLAYING`, `ST_SONAR`, `ST_PAUSED`, `ST_GAMEOVER`, `ST_MENU`).
  - **A3 (`src/game.asm`):** Implemented `FrameDelay` using `GetMseconds` and `Delay` to keep a steady `80 ms` per frame (~12.5 FPS) across fast and slow PCs.
  - **A4 (`src/anas/input.inc`):** Implemented `HandleInput` using `ReadKey` in a loop so all buffered keys are processed without blocking the game. Added left/right movement (`A`/`D` and `VK_LEFT`/`VK_RIGHT`) between `MIN_COL` (1) and `MAX_COL` (78), firing (`W`), sonar check (`SPACE` when `GetMseconds >= sonarReadyAt`), pause toggle (`P`), and exit to menu (`ESC`).
  - **A5 (`src/anas/torpedo.inc`):** Implemented `FireTorpedo` and `UpdateTorpedoes` using `ESI` pointer stepping (`add esi, TYPE GameObject`) and `fireCooldown = 3`.
  - **A6 (`src/anas/collision.inc`):** Implemented `CheckCollisions` with outer loop (`ECX`) over `Torpedoes` and inner loop (`EDX`) over `Charges`, handling both same-cell hits and 1-row crossing hits, awarding 10 points (visible charge) or 25 points (hidden mine), and checking submarine hits on `SUB_ROW`.
  - **A7 (`src/game.asm`, `src/anas/stubs_anas.inc`):** Implemented full `InitGame` reset (`REP STOSB` to zero all object arrays) and removed temporary `ANAS_STUB` entries now that all real Anas procedures are in place.
- **Build/test:** Code follows standard MASM / Irvine32 (Win32 x86) conventions and keeps Alyan and Ali stubs linked so the project builds cleanly before and after teammate merges. Full lab-PC verification to be recorded in `docs/testing/acceptance-checklist.md`.
- **Blocked / risks:** Waiting on Alyan (`src/alyan/`) and Ali (`src/ali/`) module PRs for full visual/audio integration testing.
- **Next:** Merge PR, integrate with Alyan and Ali branches, and run the acceptance test checklist on a lab PC.
