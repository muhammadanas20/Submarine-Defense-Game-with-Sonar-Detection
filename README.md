# Depth Charge — Submarine Defense with Sonar Detection

A simple, single-player **80 × 25 text-console game** written in **x86 assembly (MASM + Irvine32)** for EL-2003 Computer Organization and Assembly Language Lab, Fall 2026.

**Status:** this revision has not been built or run on Windows. Test the changes before using them for submission. Earlier tests mentioned below apply only to the previous revision. The latest changes (renaming the `Pause`/`Resume` labels that newer MASM rejects, and the redrawn submarine/depth-charge art) were checked statically only: sprite widths against the geometry constants, every string against the 80-column layout, label/`call` resolution per procedure, and a reserved-word scan over all 215 identifiers. Build with **Ctrl+Shift+B** in Visual Studio and play a round before submitting. The code has been assembled, linked, and exercised in a Windows compatibility environment. Final Visual Studio/lab-PC acceptance and individual member review are still required. See [Verification](docs/testing/verification-2026-11-03.md).

## Team and course

| Role | Name | Roll number | Main responsibility |
|---|---|---|---|
| Group leader | Muhammad Anas | 25K-0899 | Loop, input, submarine, torpedoes, collisions, integration |
| Member 2 | Syed Alyan Hussain | 25K-0648 | Drawing, HUD, explosions, sonar |
| Member 3 | Ali Raza | 25K-0827 | Random numbers, charges, screens, score, sound, high score |

- **Course:** EL-2003 COAL Lab, BCS-3C, FAST-NUCES Karachi
- **Instructor:** Mr. Muhammad Owais
- **Proposal:** [PDF](docs/proposal/COAL%20project%20proposal.pdf) · [Outline and implementation notes](docs/proposal/proposal-outline.md)
- **Planned demo:** 23 November 2026, subject to the instructor's schedule

## How to play

You control the green submarine — an 11-cell hull `<=-[ooo]-=>` with the `_!_` conning tower and periscope drawn on the row above — near the bottom of the screen. Avoid falling depth charges `(@)` and shoot them with torpedoes `^`. Some charges are hidden mines: they are real objects in memory but are not drawn during normal play. Sonar reveals them as green `[!]` marks.

Every sprite is one line of text drawn centred on the object's `x`, so each design has an odd number of cells. The art strings live in `src/alyan/render.inc` and their widths/hit windows live next to each other in `src/shared/constants.inc` (`SUB_W`/`SUB_HALF`, `SAIL_W`, `CHG_W`/`CHG_HALF`, `MINE_W`, `SUB_HIT`, `TORP_HIT`); movement, drawing and collision all read those constants, so a redesign only needs the string plus its width.

| Key | Action |
|---|---|
| `A` / `D` or Left / Right | Move left / right; capital letters also work |
| `W` | Fire a torpedo |
| `SPACE` | Activate sonar when ready |
| `P` | Pause / resume, including during sonar |
| `ESC` | Return to the menu without saving the current round |
| Menu `1` / `2` / `3` | Start / instructions / exit |

Rules:

- 3 lives; a charge hitting the submarine costs one life.
- Visible charge: **+10** points. Hidden mine: **+25** points.
- Level increases every 200 points, up to level 9.
- Higher levels use shorter spawn and fall delays.
- Sonar freezes object movement for about 2 seconds, then recharges for 10 seconds.
- A new high score is saved at **game over**, not when leaving with `ESC`.
- After game over, press any key to return to the menu.

The frame target is 80 ms (about 12.5 frames/second). Blocking Windows `Beep` calls can make an individual frame longer; this is a simple course project, not a hard real-time engine.

## Build and run on Windows

### Requirements

1. Windows 10/11.
2. Visual Studio 2022 or 2026 with **Desktop development with C++**, the matching MSVC toolset and MASM build customizations. The 2026 configuration is not yet tested.
3. The course's **32-bit Irvine32** package in `C:\Irvine`, including:
   - `Irvine32.inc`, `SmallWin.inc`, `VirtualKeys.inc`
   - `Irvine32.lib`, `Kernel32.lib`, `User32.lib`
4. A console window/buffer of at least 80 columns and 25 rows. The game draws an 80 × 25 area.

### Steps

1. Clone or download this repository.
2. Open **`Project.sln`** in Visual Studio (opening just the folder does not guarantee that the solution is loaded).
3. Select **Debug | Win32** or **Release | Win32**. Do not select x64.
4. Build with **Ctrl+Shift+B**.
5. Run with **Ctrl+F5**.
6. The executable is created at `bin\Win32\Debug\DepthCharge.exe` or `bin\Win32\Release\DepthCharge.exe`.

The project already sets the MASM include path, Irvine library path, entry point `main`, and disables SafeEH for the legacy assembly objects. If the instructor's Irvine folder is different, change the two `C:\Irvine` paths in the project properties for the selected configuration.

### If the build fails

| Message / symptom | Check |
|---|---|
| Cannot open `Irvine32.inc` | MASM → General → Include Paths must contain the Irvine folder and `$(ProjectDir)src` |
| Cannot open `Irvine32.lib` | Linker → General → Additional Library Directories must contain the Irvine folder |
| Unresolved external symbol | Confirm Win32, the correct Irvine library, and `kernel32.lib;user32.lib` |
| SafeEH error | Linker → Advanced → Image Has Safe Exception Handlers = **No** |
| Entry-point error | Linker → Advanced → Entry Point = **main** |
| `error A2008: syntax error` reported on the line *after* a label | The label name is a MASM reserved word. `PAUSE` is an x86 instruction and `RESUME` is the `.TRY`/`.FINALLY` operator, and reserved words are case-insensitive, so `Pause:`/`Resume:` in `anas\input.inc` build with MASM 6.14 but fail with the newer `ml.exe` in Visual Studio 2022/2026. They are now `PauseGame:`/`UnpauseGame:`; never name a label, variable, or procedure a bare instruction or directive name (or disable the keyword with `OPTION NOKEYWORD:<name>`) |
| Submarine or charge art looks shifted | The art string in `alyan\render.inc` and the `*_W`/`*_HALF` constants in `shared\constants.inc` must agree, and each sprite must stay an odd number of cells wide |
| Game area is cut off | Enlarge the console window/buffer to at least 80 × 25 |
| No sound | Check Windows volume and output device; muted sound does not stop gameplay |

`highscore.dat` is a small binary file created in the program's **current working directory**. With the supplied Visual Studio project this is normally the project folder. It is ignored by Git. If saving fails, the game-over screen shows a permission message.

## Source layout

```text
src/
├── game.asm                 Main, InitGame, GameLoop, FrameDelay, INCLUDE list
├── shared/
│   ├── constants.inc        Screen sizes, states, colours, object limits
│   └── data.inc             shared variables and byte arrays
├── anas/
│   ├── input.inc            Non-blocking keys, movement, pause, sonar request
│   ├── torpedo.inc          Fire and move torpedoes
│   └── collision.inc        Torpedo/charge and charge/submarine hits
├── alyan/
│   ├── render.inc           Console setup, ASCII art, screen buffers, changed-cell drawing
│   ├── hud.inc              Score/lives/level/sonar status and pause message
│   ├── explosion.inc        Five-frame ASCII explosion
│   └── sonar.inc            Two-second reveal and ten-second recharge
└── ali/
    ├── random.inc           Small linear congruential generator
    ├── screens.inc          Menu, instructions, game over
    ├── charges.inc          Spawn and fall logic
    ├── sound.inc            Five Beep sound effects and one small macro
    ├── score.inc            Points, lives, level lookup tables
    └── highscore.inc        Four-byte high-score file
```

There is **one assembly translation unit**: `game.asm` includes the `.inc` files. The old temporary stub files have been removed because all planned procedures now have real implementations.

## Documentation for submission and viva

- [Common viva guide: how the whole game works](docs/viva/00-common.md)
- [Anas's viva guide](docs/viva/anas.md)
- [Alyan's viva guide](docs/viva/alyan.md)
- [Ali's viva guide](docs/viva/ali.md)
- [IEEE-style team report draft](docs/report/final-report.md) — review and personalize before submission
- [Manual acceptance checklist](docs/testing/acceptance-checklist.md)
- [Actual verification record](docs/testing/verification-2026-11-03.md)
- [Contribution and PR rules](CONTRIBUTING.md)

### Word / PDF copies

Generated copies are in [`docs/submission/`](docs/submission/):

- [Team report draft (PDF)](docs/submission/Depth_Charge_Report_Draft.pdf) · [DOCX](docs/submission/Depth_Charge_Report_Draft.docx)
- [Combined viva guide (PDF)](docs/submission/Depth_Charge_Viva_Guide.pdf) · [DOCX](docs/submission/Depth_Charge_Viva_Guide.docx)
- Individual viva PDFs: [Anas](docs/submission/Viva_Guide_Anas.pdf), [Alyan](docs/submission/Viva_Guide_Alyan.pdf), [Ali](docs/submission/Viva_Guide_Ali.pdf)

The course outline requires a written report and individual viva. The report draft is a team starting point, not proof that every member has reviewed the code. Each member must understand their own module and the common game loop, run the demo, and follow the instructor's individual-report instructions.

## Deliberately simple design

- Fixed arrays: 8 torpedoes, 15 charges, 5 explosions.
- One-line ASCII sprites, each drawn centred on the object's `x`; every width, border clamp and hit window comes from one block of constants in `shared\constants.inc`.
- Each slot uses four bytes: x, y, active and hidden. The code uses offsets 0 to 3 and moves four bytes to the next slot.
- Short procedures with comments and predictable register inputs/outputs.
- Two screen buffers; only changed cells are sent to the console.
- Ordinary `CMP`/conditional jumps instead of an optional optimized renderer.
- Simple lookup tables for nine levels.
- One small sound macro; no audio files, graphics library, mouse, networking, or saved games.

The optional `RenderFast` / `REPE CMPSW` upgrade from the guide is **not** included. Recursion, inline assembly, and extended arithmetic are also not forced into the game because the proposal does not need them. The viva guide maps the concepts actually used to the course outline.

## Verification summary

On 3 November 2026 the production source was assembled with Microsoft MASM 6.14, linked as a PE32 Windows console executable with LLVM `lld-link`, and run under Wine 10.0. A separate assembly validation harness passed **1,090 checks** against the real game procedures. Menu/gameplay/pause were also exercised in a console.

This is **not** a claim of a Visual Studio 2022 build, native Windows lab-PC test, audible speaker test, or ten-minute lab soak test. Those remain on the acceptance checklist.

## Academic integrity and AI disclosure

This integration used AI assistance to complete and review code and prepare documentation, following the repository's existing AI-assisted proposal/guides. The simple implementation is intended for study and adaptation. Members must review every procedure they present, disclose AI use as required by the instructor, and never claim unreviewed generated work as unaided individual work.

Do not commit access tokens, personal Visual Studio files, build output, or `highscore.dat`.
