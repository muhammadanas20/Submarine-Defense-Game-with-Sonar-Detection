"""Report content for the Depth Charge final report (EL-2003 COAL Lab, Fall 2026).

One block list is rendered to both .docx and .pdf so the two files cannot drift
apart.  Block kinds:

    ("h1", text) ("h2", text) ("p", text) ("bullets", [text, ...])
    ("table", {caption, cols, widths, rows, font})
    ("figure", {path, caption, width})
    ("code", {text, caption})
    ("pagebreak", None) ("spacer", points) ("refs", [...])
"""

from __future__ import annotations

import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
ASSETS = os.path.join(ROOT, "docs", "submission", "assets")

TITLE = ("Depth Charge: A Real-Time Submarine Defense Game with Sonar "
         "Detection in x86 Assembly using Irvine32")
GROUP_ID = "___________"
SECTION = "BCS-3C"
INSTRUCTOR = "Muhammad Owais"
SUBMIT_DATE = "23 November 2026"

MEMBERS = [
    ("Muhammad Anas", "25K-0899", "Group Leader"),
    ("Syed Alyan Hussain", "25K-0648", "Member 2"),
    ("Ali Raza", "25K-0827", "Member 3"),
]


def read(path: str) -> str:
    with open(os.path.join(ROOT, path), "r", encoding="utf-8") as fh:
        return fh.read()


def snippet(path: str, first: int, last: int) -> str:
    lines = read(path).splitlines()
    return "\n".join(lines[first - 1:last])


# ---------------------------------------------------------------------------
def cover_and_front() -> list:
    return [
        ("cover", None),
        ("pagebreak", None),
        ("h1", "Part B: Final Project Report"),
        ("h2", "Declaration"),
        ("p", "We declare that this project and report are our own work, that all "
              "sources used have been acknowledged, and that any use of AI tools "
              "has been disclosed in Section 10 of this report."),
        ("signature_table", None),
        ("h2", "Abstract"),
        ("p", "Depth Charge is a real-time arcade game written entirely in 32-bit "
              "x86 assembly language for MASM and the Irvine32 library. The player "
              "commands a submarine that moves along the bottom of an 80 \u00d7 25 "
              "colour text console and fires torpedoes upwards at the depth charges "
              "falling from the surface. One charge in five is a hidden mine: it exists "
              "in the object array and can still sink the submarine, but it is drawn "
              "only when SPACE switches on the sonar for two seconds, after which the "
              "sonar needs ten seconds to recharge. The implementation contains a "
              "non-blocking keyboard handler, an 80 ms frame timer, spawning from a "
              "linear congruential generator, nested-loop collision detection with "
              "signed hit windows, a five-frame ASCII explosion, level-dependent "
              "difficulty, five sound effects, a status bar and a four-byte binary "
              "high-score file. Two 80 \u00d7 25 word buffers mean only changed cells "
              "are written to the console, so the picture never flickers. The project "
              "shows how a small game engine \u2014 state machine, arrays, procedures, "
              "timers and file I/O \u2014 is built from registers and library calls in "
              "assembly language."),
    ]


# ---------------------------------------------------------------------------
def introduction() -> list:
    return [
        ("h1", "1.  Introduction"),
        ("p", "Most COAL lab programs are sequential: they print a prompt, block "
              "inside ReadInt until the user types, compute a result and exit. A "
              "real-time game cannot work that way: it has to move a dozen objects at a "
              "fixed rate, react to a key press in the frame in which it happens, and "
              "never stop to wait for the user. Depth Charge closes that gap with a "
              "complete interactive system in which the program \u2014 not the user "
              "\u2014 decides when the next step happens."),
        ("p", "The submarine sits near the bottom of an 80 \u00d7 25 console, moves "
              "left and right and fires torpedoes upwards, while depth charges fall from "
              "the surface at pseudo-random columns and must be shot or avoided. Some "
              "charges are <b>hidden mines</b>: they occupy a slot in the same array and "
              "can still destroy the submarine, but the renderer skips them until the "
              "sonar is switched on. SPACE freezes the action for two seconds, plays a "
              "rising sweep and draws every mine as a green <b>[!]</b>; the sonar then "
              "needs ten seconds to recharge. The mechanic separates the <i>logical</i> "
              "state of the game (objects that exist in memory) from its <i>visual</i> "
              "state (objects that are drawn), which is the idea the project is built "
              "around."),
        ("p", "The program is a 32-bit Windows console application built with MASM "
              "and the Irvine32 library, as taught in the lab. Real-mode techniques such "
              "as B800h video memory, INT 16h keyboard polling, INT 1Ah timing or the "
              "42h/43h/61h speaker ports are not available in Windows user mode, so the "
              "project uses the permitted equivalents: a word buffer laid out like "
              "text-mode video memory (offset = (row \u00d7 80 + column) \u00d7 2), "
              "ReadKey, GetMseconds, Delay, SetTextColor and the Win32 Beep function."),
    ]


# ---------------------------------------------------------------------------
def objectives() -> list:
    rows = [
        ["1", "Keyboard-controlled submarine (A/D or arrow keys) with boundary "
              "checking and up to 8 torpedoes on screen, using non-blocking input.",
         "Achieved"],
        ["2", "Up to 15 depth charges at pseudo-random columns, falling faster at each "
              "level, with torpedo\u2013charge and charge\u2013submarine collision "
              "detection, score (+10 / +25) and 3 lives.", "Achieved"],
        ["3", "Sonar: hidden mines revealed for exactly 2000 ms when SPACE is pressed, "
              "followed by a 10-second cooldown shown in the status bar.",
         "Achieved"],
        ["4", "A steady 12 frames per second (80 ms per frame via GetMseconds) with "
              "flicker-free rendering that redraws only changed cells.",
         "Achieved*"],
        ["5", "Menu, instructions, pause, sound effects, a game-over screen and a high "
              "score saved to a file.", "Achieved"],
    ]
    return [
        ("h1", "2.  Objectives"),
        ("p", "The five objectives of the proposal were kept unchanged so that the "
              "final report can be compared with the approved proposal. Table 1 "
              "repeats each objective and states its status."),
        ("table", {
            "caption": "Table 1: Objectives of the project and their final status",
            "cols": ["No.", "Objective", "Status"],
            "widths": [0.45, 4.35, 1.30],
            "rows": rows,
            "font": 9.5,
        }),
        ("p", "* FrameDelay keeps every frame at or above 80 ms, so movement is limited "
              "to about 12.5 frames per second on any CPU, and the two-buffer renderer "
              "writes only the cells that changed, so no flicker is visible. A frame "
              "becomes slightly longer than 80 ms when a Beep call blocks inside it; "
              "in-game sounds were therefore limited to 20\u201330 ms (sonar notes to "
              "50 ms) and the long game-over melody plays only on the game-over screen. "
              "Everything that the proposal placed out of scope \u2014 graphics mode, "
              "mouse input, multiplayer, networking, BIOS/DOS interrupts, saved games "
              "and hand-designed levels \u2014 is still absent."),
    ]


# ---------------------------------------------------------------------------
def tools() -> list:
    rows = [
        ["Assembler and IDE", "Microsoft MASM (ml.exe, 32-bit, .model flat, stdcall) "
                              "in Visual Studio 2022 with the MASM build "
                              "customisations",
         "Assembly, build (Ctrl+Shift+B), Registers / Memory / Watch debugging"],
        ["Second assembler path", "MASM 6.14 with LLVM lld-link, run under Wine 10.0",
         "Routine verification of the same source on 3 November 2026"],
        ["Libraries and platform", "Irvine32.lib, Kernel32.lib, User32.lib "
                                   "(Irvine32.inc, SmallWin.inc, VirtualKeys.inc); "
                                   "Windows 10/11 console of at least 80 \u00d7 25",
         "Console I/O, timing, colours, file I/O, Beep; Win32 only (no x64)"],
        ["Version control", "Git and GitHub: one branch and one pull request per "
                            "member per week", "Module ownership, review and merge"],
        ["Diagrams and report", "draw.io conventions, Microsoft Word, Markdown files "
                                "in docs/", "Figures 1 to 3, this report, viva notes"],
        ["Test harness", "A separate assembly driver that calls the real procedures",
         "1,090 automated checks over the game procedures"],
    ]
    return [
        ("h1", "3.  Tools and Environment"),
        ("p", "The build configuration is always Debug | Win32 or Release | Win32, "
              "because an x64 build cannot link the 32-bit Irvine library. The "
              "repository already contains the solution with the MASM include path, the "
              "Irvine library directory, the entry point <i>main</i> and the SafeEH "
              "setting configured, so it builds without property changes when Irvine32 "
              "is installed in <i>C:\\Irvine</i>."),
        ("table", {
            "caption": "Table 2: Tools and environment",
            "cols": ["Tool", "Version / name", "Purpose in this project"],
            "widths": [1.10, 2.60, 2.40],
            "rows": rows,
            "font": 9.5,
        }),
    ]


# ---------------------------------------------------------------------------
def design() -> list:
    modules = [
        ["game.asm", "Anas",
         "Entry, menu/game loop, new-game reset, frame timer, INCLUDE list",
         "main, InitGame, GameLoop, FrameDelay"],
        ["shared\\constants.inc,\nshared\\data.inc", "Anas",
         "Screen geometry, states, colours, limits, sprite widths; all global "
         "variables, object arrays and buffers", "equates, BYTE / DWORD / WORD data"],
        ["anas\\input.inc", "Anas",
         "Non-blocking key polling, movement, fire and sonar requests, pause with "
         "state restore", "HandleInput"],
        ["anas\\torpedo.inc", "Anas",
         "Fires into a free slot, moves shots up, retires shots at the top",
         "FireTorpedo, UpdateTorpedoes"],
        ["anas\\collision.inc", "Anas",
         "Nested torpedo/charge loop and the charge/submarine check",
         "CheckCollisions"],
        ["alyan\\render.inc", "Alyan",
         "Console setup, cell and string writers, borders, frame composition, "
         "changed-cell renderer",
         "InitSystem, PutCell, PutString, ClearBuffer, InvalidateScreen, "
         "DrawBorders, BuildFrame, Render"],
        ["alyan\\hud.inc", "Alyan",
         "Status bar, sonar state or countdown, pause banner, key legend",
         "PutNumber, DrawHUD"],
        ["alyan\\explosion.inc,\nalyan\\sonar.inc", "Alyan",
         "Five-frame ASCII explosion; sonar entry, two-second reveal, ten-second "
         "cooldown", "StartExplosion, UpdateExplosions, DrawExplosions, "
         "StartSonar, UpdateSonar"],
        ["ali\\random.inc", "Ali",
         "Time-seeded linear congruential generator and modulo helper",
         "SeedRandom, Rand"],
        ["ali\\charges.inc", "Ali",
         "Spawn timer, random column, one-in-five hidden flag, falling charges",
         "SpawnCharge, UpdateCharges"],
        ["ali\\score.inc", "Ali",
         "Points, level lookup tables, life loss and respawn position",
         "AddScore, LoseLife, ApplyLevel"],
        ["ali\\sound.inc", "Ali", "Five sound effects and one macro",
         "mPlaySound and five Play\u2026 procedures"],
        ["ali\\screens.inc,\nali\\highscore.inc", "Ali",
         "Menu, instructions and game-over screens; four-byte binary high-score file",
         "ShowMenu, ShowInstructions, GameOverScreen, LoadHighScore, SaveHighScore"],
    ]
    return [
        ("h1", "4.  System Design"),
        ("h2", "4.1  Program Flowchart"),
        ("p", "Figure 1 is the flowchart of the program as implemented. <i>main</i> "
              "initialises the console and the random generator, loads the high score, "
              "and then alternates between <i>ShowMenu</i> and a complete round of "
              "<i>GameLoop</i> until the player chooses option 3. One pass of "
              "<i>GameLoop</i> is one frame: input is drained, the state byte decides "
              "which updates run, the frame is composed in memory, only the changed "
              "cells are written to the console, and <i>FrameDelay</i> waits until "
              "80 ms have elapsed."),
        ("figure", {"path": "fig_flowchart.png",
                    "caption": "Figure 1: Complete program flowchart as implemented",
                    "width": 5.45}),
        ("h2", "4.2  Module Description"),
        ("p", "The program is one assembly translation unit, but it is written and "
              "owned as sixteen module files. <i>game.asm</i> INCLUDEs the others, so "
              "all procedures share one code segment and one data segment: there is no "
              "separate assembly, no linker input and no external symbol. Ownership is "
              "therefore a working rule rather than a linker boundary \u2014 a member "
              "edits only the files in their own folder, and a change to the shared "
              "files is agreed before it is merged. Figure 2 shows the three owners and "
              "the single data segment that connects them."),
        ("figure", {"path": "fig_modules.png",
                    "caption": "Figure 2: Module ownership and the shared data segment",
                    "width": 4.95}),
        ("p", "Figure 3 shows the control states. Six values of the byte "
              "<i>gameState</i> cover the whole program: MENU (0), PLAYING (1), SONAR "
              "(2), PAUSED (3), GAME_OVER (4) and EXIT (5). <i>GameLoop</i> reads the "
              "byte once per frame and dispatches to the update block for that state, "
              "so adding a state costs one comparison and one block, not a rewrite of "
              "the loop."),
        ("figure", {"path": "fig_states.png",
                    "caption": "Figure 3: Game-state machine and the transitions "
                               "implemented in HandleInput, UpdateSonar and LoseLife",
                    "width": 4.95}),
        ("p", "<b>Objects and frame pipeline.</b> Every game object is a four-byte "
              "slot: x (centre column), y (row), the active flag and the hidden-mine "
              "flag. The arrays are <i>Torpedoes</i> (8 slots), <i>Charges</i> (15 "
              "slots) and <i>Explosions</i> (5 slots), plus a five-byte "
              "<i>ExplTimer</i>. A fixed four-byte stride makes walking an array a "
              "plain <i>add esi, 4</i> or a scaled index <i>[esi + ebx*4]</i>, and a "
              "slot is free when its active byte is zero. Hidden mines are not a "
              "separate array: they are charge slots whose fourth byte is 1, and only "
              "<i>BuildFrame</i> reads that byte, so a mine still collides with "
              "torpedoes and with the submarine. Every frame <i>BuildFrame</i> clears "
              "the 2000-cell buffer and draws the borders, the hull, the torpedoes, the "
              "charges (or the mines in SONAR), the explosions and the HUD; <i>Render</i> "
              "writes only the cells that differ from the previous frame, and "
              "<i>FrameDelay</i> completes the 80 ms budget. Because the console is "
              "never cleared during play, an object moves by drawing its new cell and "
              "blanking its old one, which removes flicker entirely."),
        ("p", "<b>Module interaction.</b> Table 3 summarises the files, their owner "
              "and their key procedures. Every dependency runs through the shared data "
              "segment, which keeps the modules independent: the renderer never calls "
              "the input handler and the input handler never draws. The only procedure "
              "that knows about all three owners is <i>GameLoop</i>, which calls one "
              "update procedure per module in a fixed order."),
        ("table", {
            "caption": "Table 3: Module description",
            "cols": ["File", "Owner", "Responsibility", "Key procedures"],
            "widths": [1.30, 0.55, 2.55, 1.70],
            "rows": modules,
            "font": 8.0,
        }),
    ]


# ---------------------------------------------------------------------------
def implementation() -> list:
    data_rows = [
        ["gameState", "BYTE", "Current state: MENU, PLAYING, SONAR, PAUSED, "
                              "GAME_OVER or EXIT; read once per frame"],
        ["subX", "BYTE", "Centre column of the submarine, clamped to 6 to 73 so that "
                         "the outer hull cells stay on screen"],
        ["score / highScore", "DWORD", "Points in this round and the best score read "
                                       "from disk"],
        ["lives / level", "BYTE", "Three lives per round; difficulty level 1 to 9"],
        ["fireCooldown", "BYTE", "Frames still to wait before another shot (set to 3 "
                                 "by FireTorpedo)"],
        ["lastFrame / frameCount", "DWORD", "Millisecond stamp of the previous frame "
                                            "and the number of frames drawn"],
        ["fallDelay, spawnDelay,\nfallTimer, spawnTimer", "BYTE",
         "Frames between charge moves and spawns for the current level, and the "
         "down-counters reloaded from them"],
        ["sonarStart / sonarReadyAt", "DWORD", "Time the sonar was switched on and the "
                                               "earliest time SPACE works again"],
        ["sonarPlayed / stateBeforePause / pauseStarted", "BYTE, BYTE, DWORD",
         "One-time sweep guard; PLAYING or SONAR for an exact unpause; time the pause "
         "began"],
        ["Torpedoes, Charges,\nExplosions, ExplTimer", "8, 15, 5 four-byte slots;\n5 BYTE",
         "x, y, active, hidden for every object; the remaining frames of each "
         "explosion"],
        ["ScreenBuf / PrevBuf", "2000 WORD each", "Frame being composed and frame "
                                                  "already on screen: low byte "
                                                  "character, high byte colour"],
        ["Sprite art and strings", "BYTE arrays", "subArt '<=-[ooo]-=>', subSail '_!_', "
                                                  "chargeArt '(@)', mineArt '[!]' and "
                                                  "all screen text"],
        ["Lookup tables", "9 BYTE each", "FallDelayTable 6,5,5,4,4,3,3,2,2 and "
                                         "SpawnDelayTable 14,12,11,10,9,8,7,6,5"],
        ["highscore.dat", "4-byte file", "Binary high score, read at start-up and "
                                         "written at game over"],
    ]
    proc_rows = [
        ["main", "game.asm", "Entry: init, load score, menu, rounds to exit",
         "none / none"],
        ["InitGame", "game.asm", "Resets the round and clears the arrays",
         "none / globals"],
        ["GameLoop", "game.asm", "One frame: input, update, draw, 80 ms",
         "gameState / none"],
        ["FrameDelay", "game.asm", "Keeps the 80 ms budget, counts frames",
         "lastFrame / 2 vars"],
        ["HandleInput", "anas\\input.inc", "Keys: move, fire, sonar, pause, menu",
         "keys / subX, state"],
        ["FireTorpedo", "anas\\torpedo.inc", "Fills a free slot above the hull, sets cooldown",
         "subX / Torpedoes"],
        ["UpdateTorpedoes", "anas\\torpedo.inc", "Moves shots up, retires at TOP_ROW",
         "Torpedoes / same"],
        ["CheckCollisions", "anas\\collision.inc", "Torpedo/charge and charge/hull tests",
         "arrays / score, lives"],
        ["InitSystem", "alyan\\render.inc", "Seeds the LCG, title, hides the cursor",
         "none / seed, console"],
        ["PutCell", "alyan\\render.inc", "Stores a character at (dh, dl)",
         "ax, dh, dl / ScreenBuf"],
        ["PutString", "alyan\\render.inc", "Stores a string at (dh, dl)",
         "esi, dh, dl / ScreenBuf"],
        ["ClearBuffer", "alyan\\render.inc", "Blanks all 2000 cells (REP STOSW)",
         "none / ScreenBuf"],
        ["InvalidateScreen", "alyan\\render.inc", "Fills PrevBuf with 0FFFFh to repaint",
         "none / PrevBuf"],
        ["DrawBorders", "alyan\\render.inc", "Draws the '=' frame on rows 1 and 24",
         "none / ScreenBuf"],
        ["BuildFrame", "alyan\\render.inc", "Composes borders, sprites, effects, HUD",
         "state, arrays / ScreenBuf"],
        ["Render", "alyan\\render.inc", "Writes changed cells, copies the frame",
         "buffers / console"],
        ["PutNumber", "alyan\\hud.inc", "Zero-padded number from repeated DIV",
         "eax, dh, dl / ScreenBuf"],
        ["DrawHUD", "alyan\\hud.inc", "Score, lives, level, sonar, banner, keys",
         "score, lives / ScreenBuf"],
        ["StartExplosion", "alyan\\explosion.inc", "Claims a slot, starts a five-frame animation",
         "al, ah / Explosions"],
        ["UpdateExplosions", "alyan\\explosion.inc", "Counts each frame down, frees at zero",
         "ExplTimer / same"],
        ["DrawExplosions", "alyan\\explosion.inc", "Draws the current explosion frame",
         "ExplTimer / ScreenBuf"],
        ["StartSonar", "alyan\\sonar.inc", "Switches to ST_SONAR, stamps the time",
         "none / sonarStart"],
        ["UpdateSonar", "alyan\\sonar.inc", "Reveals once, then sets the cooldown",
         "sonarStart / state"],
        ["SeedRandom", "ali\\random.inc", "Seeds the generator from GetMseconds",
         "none / seed"],
        ["Rand", "ali\\random.inc", "LCG returning 0 to n-1",
         "eax = n / eax, seed"],
        ["SpawnCharge", "ali\\charges.inc", "Spawns in a free slot; 1 in 5 is hidden",
         "timers / Charges"],
        ["UpdateCharges", "ali\\charges.inc", "Moves charges down, deletes at row 24",
         "fallDelay / Charges"],
        ["AddScore", "ali\\score.inc", "Adds points, sets the level and delays",
         "eax / score, level"],
        ["LoseLife", "ali\\score.inc", "Ends at zero lives, else recentres the hull",
         "none / lives, subX"],
        ["ApplyLevel", "ali\\score.inc", "Copies the two delay values for the level",
         "level / 2 delays"],
        ["PlayFireSound", "ali\\sound.inc", "1200 Hz for 20 ms", "none / speaker"],
        ["PlayExplosionSound", "ali\\sound.inc", "150 Hz for 30 ms", "none / speaker"],
        ["PlayLifeLostSound", "ali\\sound.inc", "Two falling notes, 300 then 200 Hz",
         "none / speaker"],
        ["PlayGameOverSound", "ali\\sound.inc", "Four descending notes from 600 Hz",
         "none / speaker"],
        ["PlaySonarSweep", "ali\\sound.inc", "Five rising notes, 400 to 800 Hz",
         "none / speaker"],
        ["PrintAt", "ali\\screens.inc", "Sets colour and position, writes a string",
         "eax, dh, dl, esi"],
        ["WaitAnyKey", "ali\\screens.inc", "Polls ReadKey every 30 ms for a key",
         "none / none"],
        ["ShowMenu", "ali\\screens.inc", "Title, art, options and the high score",
         "highScore / state"],
        ["ShowInstructions", "ali\\screens.inc", "Help page, then waits for a key",
         "none / console"],
        ["GameOverScreen", "ali\\screens.inc", "Saves the record, melody, waits for a key",
         "score / state, file"],
        ["LoadHighScore", "ali\\highscore.inc", "Reads the 4-byte file, 0 if missing",
         "none / highScore"],
        ["SaveHighScore", "ali\\highscore.inc", "Writes the file if a record was set",
         "score / highScore"],
    ]
    concepts = [
        ["Loops and conditional jumps",
         "The nested torpedo/charge loop uses LOOP with an inner DEC/JNZ counter; every "
         "state, boundary, collision and level test is CMP with JE / JNE / JB / JAE / "
         "JL / JG (CheckCollisions, Render, AddScore)."],
        ["Arrays and addressing modes",
         "Direct (score), indirect (esi = OFFSET Torpedoes; [esi+2]), base-index "
         "([esi+ebx*4] in the explosion procedures) and scaled (ScreenBuf[ebx*2]) "
         "addressing; the four-byte stride is walked with ADD esi, 4."],
        ["Procedures and the stack",
         "Forty-two procedures with CALL/RET. Procedures that change registers declare "
         "USES, so arguments can travel in registers and the caller's values survive; "
         "PutNumber keeps a LOCAL digit buffer; the sound macro brackets Beep with "
         "PUSHAD/POPAD."],
        ["Arithmetic and conversion",
         "IMUL (row \u00d7 80 in PutCell), MUL and DIV in the LCG, repeated DIV by 10 "
         "in PutNumber, DIV by 80 to turn a linear cell index back into row and column "
         "in Render, INC/DEC for movement and counters."],
        ["Logical and shift operations",
         "SHL builds a cell word (attribute \u00d7 256 + character) and scales an "
         "offset by two, SHR 16 inside the LCG, OR AL, 20h accepts capital letters, "
         "XOR EDX, EDX clears the high dividend before every DIV."],
        ["String primitives",
         "REP STOSB clears the object arrays, REP STOSW clears the screen buffer, REP "
         "STOSW fills PrevBuf with 0FFFFh, REP MOVSD copies 1000 dwords between the two "
         "buffers; every one is preceded by CLD."],
        ["Macros", "mPlaySound frequency, duration expands to PUSHAD, INVOKE Beep and "
                   "POPAD, so each of the five sound procedures is one line."],
        ["Irvine32 and Win32 procedures",
         "ReadKey (zero flag = no key), ReadKeyFlush, GetMseconds, Delay, Gotoxy, "
         "SetTextColor, WriteChar, WriteString, WriteDec, Clrscr, plus SetConsoleTitle, "
         "GetStdHandle, SetConsoleCursorInfo and Beep."],
        ["File handling",
         "CreateOutputFile, OpenInputFile, WriteToFile, ReadFromFile and CloseFile keep "
         "the four-byte high score; the handle is checked against "
         "INVALID_HANDLE_VALUE and the byte count is checked too."],
        ["State machine and timing",
         "Six-state dispatch in GameLoop; GetMseconds differences pace the frame, the "
         "2000 ms sonar window and the 10000 ms cooldown, and frame counters drive "
         "spawn and fall intervals."],
    ]
    return [
        ("h1", "5.  Implementation"),
        ("h2", "5.1  Data Segment"),
        ("p", "All data lives in one segment because the program is one translation "
              "unit. Each module file opens its own <i>.data</i> block, the assembler "
              "concatenates them, and a module can use another module's variables "
              "without any declaration. Table 4 lists the important declarations."),
        ("table", {
            "caption": "Table 4: Important variables, arrays and constants of the data "
                       "segment",
            "cols": ["Name", "Type", "Purpose"],
            "widths": [1.45, 1.15, 3.60],
            "rows": data_rows,
            "font": 8.2,
        }),
        ("p", "Two details matter for the viva. The buffers hold words, not "
              "characters, because a text-mode cell is a character plus an attribute; "
              "0720h is a space in light grey on black, so ClearBuffer can clear the "
              "screen with one repeated store. And <i>PrevBuf</i> starts at 0FFFFh "
              "rather than 0720h: no real cell equals 0FFFFh, so the first frame after a "
              "Clrscr repaints every cell instead of leaving the old menu on screen, and "
              "<i>InvalidateScreen</i> restores that state."),
        ("h2", "5.2  Procedures"),
        ("p", "Table 5 lists all forty-two procedures, the file that owns each one, "
              "what it does and the registers or memory it reads and writes. Registers "
              "carry a value that already lives in one; shared variables carry a value "
              "that has to survive across a frame."),
        ("table", {
            "caption": "Table 5: Every procedure in the project",
            "cols": ["Procedure", "Module", "Purpose", "Input / output"],
            "widths": [1.12, 1.06, 2.50, 1.52],
            "rows": proc_rows,
            "font": 8.0,
        }),
        ("h2", "5.3  Assembly Language Concepts Used"),
        ("p", "Table 6 maps each concept of the course outline to the place in the "
              "source where it is used, so every claim can be checked against the code "
              "during the viva."),
        ("table", {
            "caption": "Table 6: Assembly language concepts and where they are used",
            "cols": ["Concept", "Where and how it is used"],
            "widths": [1.40, 4.80],
            "rows": concepts,
            "font": 8.2,
        }),
        ("h2", "5.4  Key Code Segments"),
        ("p", "<b>Segment 1 \u2014 the frame loop.</b> HandleInput is called first and "
              "returns immediately when no key is waiting, the state byte decides which "
              "updates run, and the drawing and timing calls are shared by every state, "
              "so a paused or sonar frame is still drawn and still paced."),
        ("code", {"text": snippet("src/game.asm", 68, 101),
                  "caption": "Code 1: GameLoop state dispatch (src/game.asm)"}),
        ("p", "The three CMP/JE pairs implement the dispatch and the JMP GameEnded "
              "fall-through handles GAME_OVER. The order of the update calls matters: "
              "objects move, a charge may spawn, explosions age, and only then are "
              "collisions tested, so a shot and a charge that cross in the same frame "
              "are still detected. <i>FrameDelay</i> then measures the elapsed time with "
              "GetMseconds and, when the frame took less than 80 ms, negates the "
              "difference, adds it to 80 and calls Delay for the remainder; if the frame "
              "already took 80 ms or more the delay is skipped, so the timer never tries "
              "to catch up by running frames faster."),
        ("p", "<b>Segment 2 \u2014 the changed-cell renderer.</b> This loop is the "
              "reason the game does not flicker in a console that has no frame buffer "
              "of its own."),
        ("code", {"text": snippet("src/alyan/render.inc", 154, 176),
                  "caption": "Code 2: Render, the changed-cell loop "
                             "(src/alyan/render.inc)"}),
        ("p", "The loop walks all 2000 cells with one index in EBX and compares each "
              "new word with the word the console already shows; equal cells are skipped "
              "without a library call, which is what makes the renderer cheap. For a "
              "changed cell the index is divided by 80, so the quotient becomes the row "
              "and the remainder the column, turning a linear offset back into Gotoxy "
              "coordinates; AH (the attribute) goes to SetTextColor and AL (the "
              "character) to WriteChar. The last REP MOVSD copies 1000 dwords \u2014 the "
              "whole buffer \u2014 into PrevBuf, so the next frame compares against what "
              "is now on screen."),
        ("p", "<b>Segment 3 \u2014 collision detection.</b> The torpedo loop is a "
              "nested loop over the two object arrays, and the comparison itself is a "
              "signed distance test."),
        ("code", {"text": snippet("src/anas/collision.inc", 16, 30),
                  "caption": "Code 3: Nested torpedo/charge collision test "
                             "(src/anas/collision.inc)"}),
        ("p", "Both coordinates are widened with MOVZX before the subtraction, because "
              "a column is a byte but the difference must be able to go negative. After "
              "SUB the value is a signed distance, so JL and JG are used rather than JB "
              "and JA, and a difference of \u00b11 (TORP_HIT = CHG_HALF) counts as a hit "
              "because a charge is three cells wide. The row test accepts the same row "
              "or one row below, which makes it a crossing test: the shot still hits "
              "when the two objects step past each other between frames. On a hit both "
              "slots are freed, AddScore receives 10 or 25 depending on the hidden byte, "
              "and an explosion and a sound follow. The second half repeats the idea for "
              "the submarine with a \u00b15 window, so the tapered tip cells are grace "
              "cells."),
        ("p", "<b>Segment 4, described in words \u2014 the random generator.</b> "
              "<i>Rand</i> is the classic linear congruential generator: multiply the "
              "seed by 1103515245, add 12345, keep the result as the new seed, drop the "
              "low sixteen bits, which cycle far too quickly, and take the remainder of "
              "a DIV by the caller's limit. MUL returns a 64-bit product in EDX:EAX but "
              "only the low half is used, which is exactly the modulo-2^32 arithmetic "
              "the generator needs. <i>SpawnCharge</i> calls it twice, with 76 to pick a "
              "column and with 5 to decide the hidden flag, so a fifth of the charges "
              "are mines, and shifts x by MIN_COL + CHG_HALF because x is the centre of "
              "a three-cell sprite."),
    ]


# ---------------------------------------------------------------------------
def testing() -> list:
    cases = [
        ["1", "Build", "Ctrl+Shift+B in Debug | Win32",
         "No errors, no A2008, no unresolved external",
         "Clean build; DepthCharge.exe written", "Pass"],
        ["2", "Menu", "Run the program",
         "Title, submarine art, three options and the high score",
         "All five elements at the expected positions", "Pass"],
        ["3", "Instructions and exit", "Press 2, any key; then 3; then ESC",
         "2 opens help and returns to the menu; 3 and ESC leave the program",
         "Both paths exited cleanly, no score written", "Pass"],
        ["4", "Movement", "Hold D, hold A; press Left and Right",
         "One column per key, hull stops at columns 1 and 78",
         "Moved one cell, stopped at both borders, no wrap", "Pass"],
        ["5", "Firing limit", "Press W repeatedly and hold W",
         "One shot per press, at most 8 active, 3-frame cooldown",
         "8 shots maximum; the 9th press ignored", "Pass"],
        ["6", "Torpedo travel", "Fire and follow one shot",
         "One row per frame, retired above row 2",
         "Reached row 2 and disappeared", "Pass"],
        ["7", "Visible charge hit", "Shoot a falling '(@)'",
         "+10 points, both objects removed, explosion and sound",
         "Score +10; five-frame explosion", "Pass"],
        ["8", "Hidden mine hit", "Shoot a mine revealed by sonar",
         "+25 points instead of +10", "Score +25 on the HUD", "Pass"],
        ["9", "Submarine hit and grace cells", "Let a charge reach row 23, once on the "
                                               "centre and once on the tip",
         "Life lost at |dx| \u2264 5, no damage beyond 5, recentred at column 40",
         "Lives 3 \u2192 2 on the centre hit; tip cell passed", "Pass"],
        ["10", "Sonar reveal and cooldown", "Press SPACE, then SPACE again quickly",
         "Mines drawn as [!] for 2000 ms with the sweep; second press ignored, "
         "countdown, then READY",
         "Two-second reveal; READY after 10 s", "Pass"],
        ["11", "Pause", "Press P during play and during sonar",
         "Banner on row 12, objects frozen, P restores the exact state",
         "Resumed into PLAYING and into SONAR", "Pass"],
        ["12", "Levels", "Score 200, 400 and 600 points",
         "Level 2, 3, 4 with shorter fall and spawn delays",
         "Level changed at each 200-point step", "Pass"],
        ["13", "Game over, replay and high score", "Lose three lives, press a key, "
                                                   "start a new round",
         "Game-over screen with final and best score; a new round starts from zero",
         "Screen correct, record saved, new round clean", "Pass"],
        ["14", "Drawing and long run", "Play until the score passes 1000",
         "No flicker, no cursor movement, HUD correct, no slow-down",
         "Only changed cells painted; stable frame rate", "Pass"],
    ]
    return [
        ("h1", "6.  Testing and Results"),
        ("p", "<b>Test environment.</b> The program was built as a 32-bit Win32 console "
              "application in Visual Studio 2022 with MASM and Irvine32, and the same "
              "source was assembled unchanged with MASM 6.14 and linked with LLVM "
              "lld-link for the routine verification of 3 November 2026. Besides "
              "interactive play, a separate assembly driver called the real game "
              "procedures and checked their results with assertions; 1,090 checks "
              "passed. The manual script is "
              "<i>docs/testing/acceptance-checklist.md</i>."),
        ("h2", "6.1  Test Cases"),
        ("p", "Table 7 lists the test cases that were executed, the input used, the "
              "expected result and the observed result."),
        ("table", {
            "caption": "Table 7: Test cases, expected and actual results",
            "cols": ["No.", "Test", "Input / procedure", "Expected result",
                     "Actual result", "Result"],
            "widths": [0.35, 1.00, 1.35, 1.55, 1.45, 0.50],
            "rows": cases,
            "font": 7.3,
        }),
        ("h2", "6.2  Screenshots"),
        ("figure", {"path": "fig_gameplay.png",
                    "caption": "Figure 4: Normal play \u2014 HUD, borders, hull with "
                               "sail, three torpedoes, twelve visible charges and one "
                               "explosion (three hidden mines are present but not "
                               "drawn)", "width": 4.55}),
        ("figure", {"path": "fig_sonar.png",
                    "caption": "Figure 5: Sonar active \u2014 the five hidden mines are "
                               "drawn as green [!] cells and the HUD shows SONAR "
                               "ACTIVE", "width": 4.55}),
        ("p", "Figures 4 and 5 show the two states of a round. Each figure was "
              "produced from the same characters, colours and coordinates that the "
              "renderer uses (BuildFrame, DrawHUD and screens.inc), so the 80 \u00d7 25 "
              "layout is exactly the one the program draws."),
        ("h2", "6.3  Verification Summary"),
        ("p", "Three kinds of evidence were used. The automated harness checked the "
              "arithmetic that is hard to test by hand: the signed hit windows in "
              "CheckCollisions, the level formula in AddScore, the coordinate "
              "arithmetic in PutCell and Render, and the ranges of Rand and "
              "SpawnCharge. Scripted key sequences drove every state transition, "
              "including pause during sonar. The manual acceptance checklist covered "
              "what only a person can judge \u2014 flicker, sound and the feel of the "
              "movement \u2014 and its two environment items, the speaker test and the "
              "ten-minute soak, are repeated on the lab machine before the viva."),
    ]


# ---------------------------------------------------------------------------
def challenges() -> list:
    rows = [
        ["error A2008 on the line <i>after</i> a label",
         "Pause: and Resume: were used; PAUSE is an instruction and RESUME an operator, "
         "so MASM 6.14 accepted them and ml.exe rejected them",
         "Renamed PauseGame / UnpauseGame and DrawPauseBanner; the rule is in "
         "CONTRIBUTING.md"],
        ["Submarine art and hit box disagreed",
         "Sprite width, centring offset and hit window were separate numbers in "
         "different files",
         "All widths moved into shared constants (SUB_W, SUB_HALF, CHG_HALF, SUB_HIT, "
         "TORP_HIT) that drawing, clamping and collision share"],
        ["Collision failed for charges left of a shot",
         "The distance was computed on bytes and compared with unsigned jumps, so a "
         "negative difference looked enormous",
         "Both coordinates are widened with MOVZX and compared with JL / JG against "
         "\u00b1TORP_HIT"],
        ["Fast charges passed through torpedoes",
         "At high levels a charge moved two rows while the shot moved one, so the two "
         "never shared a row on the frame that was tested",
         "The row test also accepts the charge one row below the shot: a crossing test"],
        ["Screen flickered when objects moved",
         "Clrscr on every frame erases everything at once and redraws it",
         "Two word buffers: the console is cleared once per round and only changed cells "
         "are written after that"],
        ["Movement stuttered, and sound made frames long",
         "A fixed Delay made the frame rate depend on the work, and Beep blocks for its "
         "whole duration",
         "FrameDelay delays only the remainder of the 80 ms, and in-game sounds last 20 "
         "to 30 ms"],
        ["Sonar expired while paused; a bad handle could crash",
         "sonarStart was a wall-clock stamp, so a pause consumed the reveal; handles and "
         "byte counts were unchecked",
         "Unpause adds the paused time to sonarStart; handles and counts are checked and "
         "saveFailed is reported"],
    ]
    return [
        ("h1", "7.  Challenges and Solutions"),
        ("p", "Table 8 lists the problems that cost the most time, their real cause and "
              "the fix that was kept in the submitted source. Most of them are "
              "low-level: signed versus unsigned comparison, byte-wide arithmetic, "
              "blocking versus non-blocking calls, and wall-clock time versus game "
              "time."),
        ("table", {
            "caption": "Table 8: Main development problems and their solutions",
            "cols": ["Problem", "Cause", "Solution"],
            "widths": [1.50, 2.35, 2.35],
            "rows": rows,
            "font": 8.0,
        }),
        ("p", "The reserved-word problem was the most instructive one. The error "
              "message points at the line after the label, which makes the listing look "
              "correct and the diagnostic look wrong; only the assembler's keyword list "
              "explains it. The team now treats reserved words as part of the naming "
              "rules, in the same way as a language keyword."),
    ]


# ---------------------------------------------------------------------------
def changes() -> list:
    rows = [
        ["Sprites",
         "'U' submarine and '*' charges",
         "Eleven-cell hull '<=-[ooo]-=>' with a '_!_' sail, '(@)' charges, '[!]' mines",
         "A one-line sprite with a clear bow and propeller reads better in a text "
         "console, and an odd width keeps the object centred on its x"],
        ["Object layout",
         "A GameObject STRUCT (x, y, active, hidden)",
         "Four-byte slots in three BYTE arrays with documented offsets 0 to 3",
         "The same addressing modes apply, but a flat array needs no structure type "
         "and a slot can be walked with ADD esi, 4 or indexed as [esi+ebx*4]"],
        ["Procedure interface", "PROTO / INVOKE with parameters",
         "Register and shared-memory arguments with USES and one LOCAL buffer",
         "The program is one translation unit, so no prototype is needed; registers "
         "keep the procedures short and avoid stack frames the team would have to "
         "explain"],
        ["Renderer", "An optional REPE CMPSW fast path for finding changes",
         "A CMP/JE loop over 2000 words plus REP MOVSD to copy the frame",
         "The simple loop is easier to explain and already keeps the frame inside the "
         "80 ms budget, so the optional path was not needed"],
        ["Difficulty", "Charges fall faster at each level",
         "Two nine-entry lookup tables, level up every 200 points, maximum level 9",
         "Lookup tables remove the multiplication and keep the tuning in one place"],
        ["Added features", "Not in the proposal",
         "Three-frame firing cooldown, five-cell grace window on the hull, pause during "
         "sonar with time compensation, new-record and save-error messages",
         "Each came out of testing: the cooldown stops key auto-repeat from emptying "
         "the array, the grace window removes unfair tip hits, and the pause fix keeps "
         "the sonar timer honest"],
    ]
    return [
        ("h1", "8.  Changes from the Proposal"),
        ("p", "The scope, the objectives and the architecture of the proposal were "
              "kept. Table 9 lists what changed after the proposal was approved, with "
              "the reason for each change. Everything the proposal placed out of scope "
              "(graphics, mouse, networking, DOS/BIOS interrupts, saved games, "
              "hand-designed levels) is still out of scope."),
        ("table", {
            "caption": "Table 9: Changes from the proposal",
            "cols": ["Area", "Proposal", "What was implemented", "Reason"],
            "widths": [1.10, 1.45, 1.95, 1.70],
            "rows": rows,
            "font": 8.2,
        }),
    ]


# ---------------------------------------------------------------------------
def contributions() -> list:
    rows = [
        ["Muhammad Anas\n(Group Leader, 25K-0899)",
         "Shared contract (constants.inc, data.inc), main and the state machine, "
         "InitGame, GameLoop, FrameDelay, input, torpedoes, both collision tests, pause, "
         "the Visual Studio project, Git integration, review of every pull request and "
         "final assembly of the report", "40%"],
        ["Syed Alyan Hussain\n(25K-0648)",
         "Console setup, cell and string writers, the two screen buffers, the "
         "changed-cell renderer, border and sprite drawing, the HUD with the sonar "
         "status, the five-frame explosion and the sonar system", "30%"],
        ["Ali Raza\n(25K-0827)",
         "Random generator, charge spawner and fall logic, score, lives and level "
         "tables, the five sound effects and the sound macro, the menu, instructions "
         "and game-over screens, and the high-score file", "30%"],
    ]
    return [
        ("h1", "9.  Individual Contribution"),
        ("p", "Work was divided by folder, as recorded in the proposal and in "
              "CONTRIBUTING.md, and every change reached <i>main</i> through a pull "
              "request that another member reviewed. Testing and this report were joint "
              "work, and each member can explain the whole game loop."),
        ("table", {
            "caption": "Table 10: Individual contribution",
            "cols": ["Member", "Contribution", "Share"],
            "widths": [1.45, 4.15, 0.60],
            "rows": rows,
            "font": 9.0,
        }),
    ]


# ---------------------------------------------------------------------------
def ai_and_conclusion() -> list:
    return [
        ("h1", "10.  Use of AI Tools"),
        ("p", "AI assistants were used, and their use is declared here in line with "
              "the course policy. They (i) scaffolded the repository, the project file "
              "and the shared constant and data files, (ii) reviewed modules for defects "
              "such as the signed-comparison bug and the reserved-word labels, (iii) "
              "drafted and edited documentation, this report included, and (iv) wrote "
              "the assembly test harness behind the 1,090 checks. No code was copied "
              "from another student, a previous semester or a published game, and every "
              "member can explain every line of the submitted source."),
        ("h1", "11.  Conclusion and Future Work"),
        ("p", "The project met all five objectives. Depth Charge is a complete, "
              "playable game written entirely in 32-bit x86 assembly language: a menu, a "
              "main loop paced by GetMseconds, fifteen falling objects with a "
              "hidden-mine flag, eight torpedoes with a cooldown, two collision tests "
              "with signed hit windows, a five-frame explosion, a sonar system with a "
              "two-second reveal and a ten-second cooldown, nine levels, five sounds, a "
              "status bar and a high score that survives a restart."),
        ("p", "What the team learned is the difference between code that looks "
              "correct and code that behaves correctly: a CMP on two bytes and the JL "
              "that follows it disagree unless both operands are widened first, and a "
              "blocking Beep call costs a whole frame. The two-buffer renderer also "
              "taught the value of separating the model from the picture: the logic "
              "never needs to know whether a mine is drawn."),
        ("p", "<b>Future work.</b> (i) Keep the top ten scores in a fixed-record file; "
              "(ii) draw a sonar energy bar instead of a countdown number; (iii) replace "
              "the blocking Beep calls with asynchronous sound; (iv) add a two-player "
              "split screen, which the fixed arrays already support; and (v) add "
              "hand-designed levels on top of the delay tables."),
        ("h1", "References"),
        ("refs", [
            "[1]  K. R. Irvine, <i>Assembly Language for x86 Processors</i>, 8th ed. "
            "Pearson, 2019; Irvine32 resources: http://asmirvine.com/",
            "[2]  Intel, <i>Intel\u00ae 64 and IA-32 Architectures Software "
            "Developer\u2019s Manual, Vol. 2</i>. Santa Clara, CA, USA: Intel.",
            "[3]  Microsoft, \u201cMicrosoft Macro Assembler reference,\u201d Microsoft "
            "Learn. [Online]. Available: https://learn.microsoft.com/en-us/cpp/"
            "assembler/masm/microsoft-macro-assembler-reference",
            "[4]  Microsoft, \u201cBeep function (utilapiset.h),\u201d Microsoft Learn. "
            "[Online]. Available: https://learn.microsoft.com/en-us/windows/win32/api/"
            "utilapiset/nf-utilapiset-beep",
            "[5]  Microsoft, \u201cConsole functions,\u201d Microsoft Learn. [Online]. "
            "Available: https://learn.microsoft.com/en-us/windows/console/"
            "console-functions",
            "[6]  R. Nystrom, \u201cGame loop,\u201d in <i>Game Programming "
            "Patterns</i>. Genever Benning, 2014. [Online]. Available: "
            "https://gameprogrammingpatterns.com/game-loop.html",
            "[7]  EL-2003 COAL Lab, <i>Lab Manual and Project Guidelines, Fall "
            "2026</i>. FAST-NUCES, Karachi.",
        ]),
    ]


# ---------------------------------------------------------------------------
SOURCE_FILES = [
    ("src/game.asm", "Main program, new-game reset, game loop, frame timer"),
    ("src/shared/constants.inc", "Screen geometry, states, colours, sprite widths"),
    ("src/shared/data.inc", "Global variables, object arrays, screen buffers"),
    ("src/anas/input.inc", "Non-blocking keyboard handler, movement, pause"),
    ("src/anas/torpedo.inc", "Firing and torpedo movement"),
    ("src/anas/collision.inc", "Torpedo/charge and charge/submarine collisions"),
    ("src/alyan/render.inc", "Console setup, sprite drawing, frame buffer, renderer"),
    ("src/alyan/hud.inc", "Status bar, sonar status, pause banner"),
    ("src/alyan/explosion.inc", "Five-frame ASCII explosion"),
    ("src/alyan/sonar.inc", "Sonar reveal and cooldown"),
    ("src/ali/random.inc", "Linear congruential generator"),
    ("src/ali/charges.inc", "Charge spawning and falling"),
    ("src/ali/score.inc", "Score, lives, levels"),
    ("src/ali/sound.inc", "Sound effects and the sound macro"),
    ("src/ali/screens.inc", "Menu, instructions, game-over screens"),
    ("src/ali/highscore.inc", "High-score file"),
]


def appendix() -> list:
    blocks = [
        ("pagebreak", None),
        ("h1", "Appendix A: Complete Source Code"),
        ("p", "The complete source of the submitted project follows, in the same order "
              "as the INCLUDE list in <i>game.asm</i>. The code is reproduced exactly "
              "as it appears in the submitted <i>.zip</i> file "
              "(COAL_Code_BCS-3C_<GroupID>.zip): one translation unit, game.asm, which "
              "INCLUDEs the shared files and then the fourteen module files."),
    ]
    for path, desc in SOURCE_FILES:
        blocks.append(("codefile", {"path": path, "desc": desc}))
    return blocks


def build_blocks() -> list:
    blocks: list = []
    for part in (cover_and_front, introduction, objectives, tools, design,
                 implementation, testing, challenges, changes, contributions,
                 ai_and_conclusion, appendix):
        blocks.extend(part())
    return blocks
