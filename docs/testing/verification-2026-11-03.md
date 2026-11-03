# Verification record — 3 November 2026

This record separates tests actually run in the development workspace from tests that still require the course's native Windows lab PC.

## Environment used

| Item | Value |
|---|---|
| Host | Linux sandbox, x86-64 |
| Windows compatibility layer | Wine 10.0 |
| Assembler | Microsoft Macro Assembler 6.14.8444 (`ml.exe`, MASM32 distribution) |
| Linker | LLVM `lld-link` 19.1.7, target MachineX86 |
| Library | Kip Irvine's Irvine32 package, official `Irvine.zip` (2019 archive) |
| Console host | `xterm` on Xvfb |
| Source | `src/game.asm` and included modules from branch `complete-simple-game` |

This is **not** Visual Studio 2022 and **not** the lab PC. The legacy MASM/LDLL toolchain was used to verify that the assembly source assembles, links, and runs as a 32-bit Windows console program.

## Build commands

The production source was assembled with:

```text
ml.exe /nologo /c /coff /W3 /Zi ^
  /I <Irvine-folder> /I <repo>\src ^
  /Fo<output>\game.obj <repo>\src\game.asm
```

It was linked with:

```text
lld-link /NOLOGO /MACHINE:X86 /SUBSYSTEM:CONSOLE /ENTRY:main ^
  /SAFESEH:NO /OUT:<output>\DepthCharge.exe ^
  /LIBPATH:<Irvine-folder> game.obj Irvine32.lib Kernel32.Lib User32.Lib
```

Result: assembly exit code 0; link exit code 0; output identified as `PE32 executable for MS Windows (console), Intel i386`.

The Visual Studio project was updated to use entry point `main` and `ImageHasSafeExceptionHandlers=false`, matching the requirements of this legacy assembly/Irvine link.

## Procedure harness

A separate assembly harness included the real production procedures and replaced only the program entry point. It did not reimplement the game logic in Python. It exercised the actual MASM procedures and Irvine32/Windows services.

Final result:

```text
Checks: 1090
FAILED, total failures: 0
ALL CHECKS PASSED
```

The count includes 1,000 repeated random-range checks. It is not a claim of 1,090 distinct features.

| Area | Checks performed | Result |
|---|---|---|
| Shared layout | GameObject size; array byte sizes; screen-buffer size | Passed |
| New-game reset | Score/lives/level/position/state/timers/arrays/high-score preservation | Passed |
| Random | Repeatable seed; 1,000 range checks; zero-range guard | Passed |
| Charges | Spawn timer, top row, 15-slot capacity, fall timer, sea-bed removal | Passed |
| Torpedoes | Fire position, cooldown, normal flight count, full-array guard, top removal | Passed |
| Collisions | Visible +10, hidden +25, crossing hit, object deactivation, explosion start | Passed |
| Lives | One submarine hit per frame, recenter, game over at zero | Passed |
| Score/levels | 190+10 threshold, level 2 delays, level 9 cap and delays | Passed |
| Explosions | Position, first character, five-frame lifetime, timer cleanup | Passed |
| Rendering | PutCell offset, hidden mine invisible/visible, HUD digits, PrevBuf copy, skipped last cell | Passed |
| Input | Capital/lowercase letters, arrows, both boundaries, pause block, resume, sonar request, ESC | Passed |
| Pause during sonar | Remembered state and sonar-start extension | Passed |
| Sonar | Start state, end state, approximately 10-second recharge | Passed |
| Frame delay | Counter increment and elapsed time at least the frame target | Passed |
| High score | Save/load round trip, lower-score preservation, invalid-write failure, short-file recovery | Passed |

Evidence image: `evidence/logic-checks-2026-11-03.png`.

The harness source was kept as a development validation artifact and is not part of the student game build. The student-facing test procedure is the manual acceptance checklist.

## Console smoke test

The executable was run under Wine in an xterm console. Observed:

- Menu title, three options, high score, and choice prompt displayed.
- Instructions opened and returned to the menu.
- Start entered gameplay with HUD, borders, submarine, and control hints.
- Pause displayed `PAUSED - press P to resume` and froze object updates.
- Torpedo firing and movement were visible.
- Sonar state could be entered from gameplay.

Evidence images: `evidence/menu-2026-11-03.png`, `evidence/gameplay-2026-11-03.png`, `evidence/sonar-2026-11-03.png`, `evidence/pause-sonar-2026-11-03.png`.

The xterm host background may differ from a native Windows console. Colour/flicker acceptance must still be checked on the lab machine.

## Not tested here

- Visual Studio 2022 Debug/Release Win32 build.
- Native Windows 10/11 lab PC.
- Audible speaker/headphone output for all five effects.
- Ten-minute continuous-play soak test on lab hardware.
- Lab-account file permissions and restart persistence.
- Instructor-specific Irvine/template variations.

These items remain unchecked in `acceptance-checklist.md`. Do not convert them to passes without recording the actual machine, date, result, and evidence.
