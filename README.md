# Depth Charge — Submarine Defense with Sonar Detection

A text-mode, 80 × 25 submarine defense game for the **EL-2003 Computer Organization and Assembly Language Lab**, Fall 2026 (BCS-3C). The project is organized for three members to work in parallel, following the attached Anas implementation guide.

> **Starter state:** this is the Week 0 / A1 repository scaffold. `src/game.asm` is a small Irvine32 smoke-test program; it is not yet the finished game. The `stubs_*.inc` files keep planned procedures available while the team implements each module. Replace the smoke-test `main` as work proceeds through A2–A8.

## Team and course

- **Group leader:** Muhammad Anas (25K-0899)
- **Member 2:** Syed Alyan Hussain (25K-0648)
- **Member 3:** Ali Raza (25K-0827)
- **Instructor:** Muhammad Owais
- **Course:** EL-2003 COAL Lab, Fall 2026
- **Planned demo:** Monday, 23 November 2026
- **Repository:** <https://github.com/muhammadanas20/Submarine-Defense-Game-with-Sonar-Detection>

## Repository layout

```text
Submarine-Defense-Game-with-Sonar-Detection/
├── .github/
│   ├── CODEOWNERS
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/
│   ├── guides/                 Attached implementation guide
│   ├── progress/               Per-member weekly logs
│   ├── proposal/               Proposal outline
│   ├── report/                 Per-member final-report sections
│   └── testing/                Acceptance checklist
├── src/
│   ├── game.asm                The only assembly entry point
│   ├── shared/                 Shared constants and game data
│   ├── anas/                   Loop, input, torpedoes, collisions
│   ├── alyan/                  Rendering, HUD, explosions, sonar
│   └── ali/                    Random, menus, charges, sound, score, save file
├── Project.sln                 Visual Studio 2022 solution (Win32 / x86)
├── Project.vcxproj             MASM project; expects Irvine32 at C:\Irvine
└── Project.vcxproj.filters     Solution Explorer grouping
```

## Build requirements

This project is for **Windows**, not a Linux assembler. You need:

1. Visual Studio 2022 with **Desktop development with C++** and the **MASM build customization** installed.
2. The course Irvine32 files/library in `C:\Irvine` (`Irvine32.inc`, `Irvine32.lib`, and required support files).
3. An x86/Win32 build configuration. Irvine32 is a 32-bit library.

### Build the Week 0 scaffold

1. Open `Project.sln` in Visual Studio.
2. Select **Debug | Win32** (or **Release | Win32**).
3. Build the solution, then run it. The starter should print:
   `Depth Charge skeleton builds and runs OK`
4. If your lab uses a different Irvine folder, update the MASM include path and linker library path locally. Coordinate with the group before committing project-file changes; the plan asks members not to commit changes to `Project.*` after initial setup.

The project files are supplied as a VS2022-compatible starting point because no Irvine/Visual Studio template was included with the guide. Confirm the project settings against your instructor's lab template before relying on them. This workspace cannot run the Windows Irvine32 build, so the scaffold has **not** been assembled or runtime-tested here.

## Module ownership and integration contract

| Area | Owner | Main files |
|---|---|---|
| Main loop, frame timing, input, submarine, torpedoes, collisions, integration | Anas | `src/game.asm`, `src/anas/`, `src/shared/` |
| Drawing, HUD, explosions, sonar | Alyan | `src/alyan/` |
| Random numbers, menu, charges, sound, score, high score | Ali | `src/ali/` |

`src/shared/constants.inc` and `src/shared/data.inc` are shared contracts. Discuss changes with all members; Anas maintains these files. Each person edits their own module folder and their own `docs/progress/<name>.md` / `docs/report/<name>.md`.

Stub procedures are declared in `src/<owner>/stubs_<owner>.inc`. When a real procedure is implemented, remove **only that procedure's** `*_STUB` line from the corresponding stub file to avoid duplicate definitions. Keep the remaining stubs until their real implementations are ready.

## Git workflow

- Week 0: push the initial starter structure to `main` once.
- Thereafter: create one branch per week's work, commit small buildable changes, and open a pull request.
- Suggested branch: `week1-anas`; suggested PR title: `Week 1 – Anas – A2 A3`.
- Review each PR's changed files; merge in the order Anas → Alyan → Ali, then build and play before announcing that the group can sync.
- **Do not use `git add .` for weekly work.** Stage only your own paths. The one-time Week 0 initial commit is the exception in the guide.
- See [`CONTRIBUTING.md`](CONTRIBUTING.md) and the attached guide for the detailed commands and schedule.

## Milestones

| Milestone | Date | Whole-game target |
|---|---:|---|
| M1 | 25 Oct 2026 | Program/menu run; submarine moves without flicker; random numbers work |
| M2 | 8 Nov 2026 | Playable core: torpedoes, charges, hits, explosions, score, lives, HUD |
| M3 | 18 Nov 2026 | Sonar/mines, sound, levels, pause, high score, game-over screen |
| M4 / v1.0 | 22 Nov 2026 | Lab-PC test checklist passed; report ready for demo |
| Demo | 23 Nov 2026 | Individual viva and project demonstration |

## AI-use disclosure

The course guide requires AI assistance to be disclosed in the final report. This initial repository scaffold and some documentation were AI-assisted. Review, adapt, understand, and test every source file; keep the disclosure in the final report accurate to the work actually used. A draft disclosure is in `docs/report/anas.md`.

## Gameplay target (planned)

The final game is a state-driven Irvine32 console game with an 80 × 25 screen. Planned controls: **A/D** or **←/→** to move, **W** to fire, **SPACE** for sonar, **P** to pause, and **ESC** to return to the menu. See `docs/testing/acceptance-checklist.md` for the test targets.
