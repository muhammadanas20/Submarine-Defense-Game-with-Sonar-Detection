# Project proposal outline — Depth Charge

**Status:** Completed outline aligned with `docs/proposal/COAL project proposal.pdf` (submitted 15 October 2026).

## Cover information

- Course: EL-2003 Computer Organization and Assembly Language Lab, Fall 2026
- Section: BCS-3C
- Project: Depth Charge — Submarine Defense with Sonar Detection
- Group leader: Muhammad Anas (25K-0899)
- Members: Syed Alyan Hussain (25K-0648); Ali Raza (25K-0827)
- Instructor: Muhammad Owais

## 1. Problem / motivation

Most introductory assembly exercises run top-to-bottom and stop at blocking input calls to wait for the user. Interactive programs cannot stop to wait; they must poll the keyboard, update multiple objects in memory, check collisions, and draw frames at a steady rate. **Depth Charge** applies core x86 assembly concepts taught in EL-2003 COAL Lab—registers, indexed array addressing, `STRUCT` layouts, unsigned comparisons, string instructions (`REP STOSB`, `REP STOSW`, `REP MOVSD`), procedures, and file I/O—to build a complete real-time console game in Irvine32. Its sonar mechanic also separates the logical state of objects in memory (`hidden = 1` mines) from their visual state on screen.

## 2. Objectives

- Build an 80 × 25 text-mode game in x86 assembly using the course Irvine32 environment.
- Practice procedure calls, arrays/structures, keyboard polling, timing, comparisons, state machines, and file I/O.
- Integrate separately owned modules through a shared procedure/data contract and Git pull requests.

## 3. Game overview

The player controls a submarine (`U`) moving left and right along row 23 (`MIN_COL = 1` to `MAX_COL = 78`) using **A/D** or the **Left/Right arrow keys**, and fires torpedoes (`^`) upward with **W** (up to 8 active torpedoes at once with a 3-frame cooldown). Enemy depth charges (`*`) spawn in random columns at the top and fall toward the submarine. About 1 in 5 charges are hidden mines (`hidden = 1`) that are invisible during normal play but can still hit the submarine or be destroyed by torpedoes. Pressing **SPACE** activates **Sonar Mode** for 2 seconds (`2000 ms`), freezing object movement, playing a rising sonar sweep sound, and revealing all hidden mines as green `!` characters, followed by a 10-second (`10000 ms`) sonar cooldown. Visible charges award **+10 points**, hidden mines award **+25 points**, and the level increases every 200 points (up to level 9), making charges spawn and fall faster. The player starts with **3 lives**; losing all 3 lives triggers the Game Over screen and saves any new high score to `highscore.dat`. Pressing **P** pauses or resumes the game, and **ESC** returns to the main menu.

## 4. Technical approach

- Target platform: Windows x86 (Win32), Visual Studio 2022 with MASM build customizations, Irvine32 (`C:\Irvine`).
- Screen: 80 columns × 25 rows; frame duration: 80 ms (~12.5 FPS) timed with `GetMseconds` and `Delay`.
- State values and shared object arrays: `src/shared/constants.inc` and `src/shared/data.inc`.
- Module boundaries and ownership: `README.md`.

## 5. Team responsibilities

| Member | Planned responsibility | Evidence / deliverables |
|---|---|---|
| Muhammad Anas (25K-0899) | Main loop, state machine, 80 ms frame timing, non-blocking keyboard input, submarine movement, torpedoes, collision detection, new-game reset, pause, integration | `src/game.asm`, `src/shared/`, `src/anas/input.inc`, `src/anas/torpedo.inc`, `src/anas/collision.inc`, `docs/progress/anas.md`, `docs/report/anas.md` |
| Syed Alyan Hussain (25K-0648) | Double-buffered screen rendering (`ScreenBuf`/`PrevBuf`), HUD/status bar, explosion animations, sonar mode and hidden-mine rendering | `src/alyan/render.inc`, `src/alyan/hud.inc`, `src/alyan/explosion.inc`, `src/alyan/sonar.inc`, `docs/progress/alyan.md`, `docs/report/alyan.md` |
| Ali Raza (25K-0827) | LCG random number generator, menu/instructions/game-over screens, charge spawning and movement, Win32 `Beep` sounds, score/lives/levels, `highscore.dat` file I/O | `src/ali/random.inc`, `src/ali/screens.inc`, `src/ali/charges.inc`, `src/ali/sound.inc`, `src/ali/score.inc`, `src/ali/highscore.inc`, `docs/progress/ali.md`, `docs/report/ali.md` |

## 6. Schedule and milestones

- **M1 (25 Oct 2026):** Program and menu run; submarine moves smoothly without flicker; random numbers work.
- **M2 (8 Nov 2026):** Core gameplay complete: torpedoes, falling charges, collisions, explosions, score, lives, and HUD.
- **M3 (18 Nov 2026):** Full features integrated: sonar and hidden mines, sounds, levels, pause, high-score file, and game-over screen.
- **M4 / v1.0 (22 Nov 2026):** Full acceptance checklist passed on a lab PC; final report ready for the 23 Nov 2026 demo.

## 7. Testing and evaluation

Use `docs/testing/acceptance-checklist.md`. Record the machine, Visual Studio/Irvine setup, build configuration, test date, expected result, actual result, and any defect for each test.

## 8. Risks and mitigations

- **Git merge conflicts:** Mitigated by giving each member a separate directory (`src/anas/`, `src/alyan/`, `src/ali/`) and staging only owned files instead of `git add .`.
- **Unfinished dependencies blocking builds:** Mitigated with `stubs_anas.inc`, `stubs_alyan.inc`, and `stubs_ali.inc` so the project always assembles and links.
- **Console flicker and scrolling:** Mitigated by comparing `ScreenBuf` with `PrevBuf` (drawing only changed cells) and skipping the bottom-right cell (row 24, col 79).
- **Torpedoes passing through fast charges:** Mitigated in `CheckCollisions` by checking both the same row and one row above (`inc al` / `cmp al, bl`).
- **Blocking input or long sounds freezing gameplay:** Mitigated by polling with `ReadKey` (`ZF` check) and keeping in-game `Beep` tones short (<= 30 ms).

## 9. References and disclosure

- K. R. Irvine, *Assembly Language for x86 Processors*, 8th ed., Pearson, 2019.
- Microsoft Learn, *Microsoft Macro Assembler (MASM) Reference* and *Win32 Console / Beep API*.
- AI-use disclosure: AI tools were used to scaffold the initial repository structure, implementation guides, and documentation templates. All retained code and documentation are reviewed, understood, and disclosed in `docs/report/anas.md`.
