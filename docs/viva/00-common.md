# Common viva guide — Depth Charge

**Course:** EL-2003 COAL Lab, Fall 2026  
**Team:** Muhammad Anas (25K-0899), Syed Alyan Hussain (25K-0648), Ali Raza (25K-0827)

Read this page first. Then read your own member guide and skim the other two. The viva can ask about the whole program, not only your folder.

## 1. Explain the project in 30 seconds

> Depth Charge is a single-player 80 × 25 console game in 32-bit x86 assembly. I move a submarine, fire torpedoes, and avoid falling depth charges. Some charges are hidden mines. Sonar reveals them for two seconds. The game has score, three lives, nine levels, pause, sound, and a saved high score. We used MASM, Irvine32, fixed arrays, procedures, and a simple game loop.

Do not say it uses DOS video memory or BIOS interrupts. It is a Windows console program. Irvine32 and Windows API calls provide console input/output, timing, files, and sound.

## 2. The five jobs in every frame

```text
Read keys -> Move objects -> Check hits -> Draw changed cells -> Wait
```

1. **Input:** `HandleInput` checks waiting keys without blocking.
2. **Update:** torpedoes move up; charges sometimes move down; a new charge may spawn; explosions age.
3. **Collisions:** compare object coordinates in memory, not screen pixels.
4. **Render:** build a complete frame in `ScreenBuf`, then compare it with `PrevBuf`.
5. **Delay:** sleep for the remaining part of the 80 ms frame target.

`GameLoop` in `src/game.asm` controls this order. `gameState` decides whether object updates run.

| State | Value | Meaning |
|---|---:|---|
| `ST_MENU` | 0 | Menu is outside the gameplay loop |
| `ST_PLAYING` | 1 | Normal updates and drawing |
| `ST_SONAR` | 2 | Objects frozen; hidden mines visible |
| `ST_PAUSED` | 3 | Objects frozen; pause message visible |
| `ST_GAMEOVER` | 4 | Save record and show final score |
| `ST_EXIT` | 5 | Leave the program |

`P` remembers whether the game was playing or in sonar. If sonar was active, its start time is shifted forward by the paused duration, so pausing does not consume the two-second reveal. The ten-second recharge is wall-clock time and continues during an ordinary pause.

## 3. The one structure everyone uses

```asm
GameObject STRUCT
    xPos    BYTE 0
    yPos    BYTE 0
    active  BYTE 0
    hidden  BYTE 0
GameObject ENDS
```

- Size = **4 bytes**. `TYPE GameObject` is 4.
- `active = 0` means the slot is free.
- `hidden = 1` means a mine is invisible during normal drawing.
- Hidden does **not** mean inactive. Collision code still checks it.
- Torpedoes: 8 × 4 = 32 bytes.
- Charges: 15 × 4 = 60 bytes.
- Explosions: 5 × 4 = 20 bytes, plus five separate timer bytes.

Example: if `ESI` points to `Charges[0]`, `add esi, TYPE GameObject` points to `Charges[1]`. Adding 1 would point inside the first object, not to the next object.

## 4. Screen memory is not the Windows video card

Each screen cell is one WORD:

```text
low byte  = ASCII character
high byte = colour attribute
cell index = row * 80 + column
byte offset = cell index * 2
```

Example: row 5, column 10 → `(5 × 80 + 10) × 2 = 820` bytes from the start of `ScreenBuf`.

The buffer has `80 × 25 = 2000` WORDs = **4000 bytes**. This resembles old text-mode layout, but it is ordinary program memory. `Gotoxy`, `SetTextColor`, and `WriteChar` update the Windows console. We never write directly to `B800h`.

The bottom-right cell is not printed because writing there can scroll some consoles. The renderer still copies the blank cell into `PrevBuf`; it simply never sends that cell to the console.

## 5. Course-outline mapping — what we actually used

| Course topic | Where to show it | Simple explanation |
|---|---|---|
| IDE, assemble, debug, run | `Project.sln`, Win32 build | MASM makes an OBJ; linker makes an EXE |
| Data definition and strings | `data.inc`, `screens.inc` | BYTE/WORD/DWORD and zero-terminated text |
| MOV, MOVZX, LEA | `render.inc`, `hud.inc` | Copy data, extend a byte safely, take an address |
| Flags and conditional jumps | input, collisions, timers | `CMP` sets flags; `JE/JB/JAE/JNZ` choose a path |
| Indirect/index addressing | object loops, `ScreenBuf[ebx*2]` | A register holds an address or index |
| Arrays and loops | torpedoes, charges, explosions | Fixed slots avoid dynamic memory allocation |
| Procedures and stack | every module; `USES`, `CALL`, `RET` | Reusable code; save/restore registers |
| Stack frame and LOCAL | `PutNumber` | Temporary digit string belongs to this call |
| Shift and rotate topic | `SHL` for colour, `SHR` in random | Shift bits left/right; rotate is not needed |
| Multiply/divide | row offset, LCG, digits, level | `MUL/IMUL` and `DIV` with correct EDX setup |
| String instructions | `REP STOSB/STOSW`, `REP MOVSD` | Clear arrays/buffers and copy a frame |
| Structures and scaling | `GameObject`, explosion indexing | `TYPE` gives the element size |
| Macros | `mPlaySound` | Expand a small save/Beep/restore pattern |
| OS services | Irvine32 and Windows API | Console, timing, files, and Beep |

Not every listed course topic must appear in one project. This game does not use recursion, inline assembly, extended multiword arithmetic, or the optional `REPE CMPSW` renderer. Saying that honestly is better than inventing a feature.

## 6. Questions every member should answer

**Why x86 and not x64?**  
The course library is Irvine32. Its procedures and library are 32-bit, so the project uses Win32 and 32-bit registers.

**Why is there one `.asm` file but many `.inc` files?**  
`INCLUDE` inserts source text before assembly. It split work by owner without creating separate linking contracts. There is still one assembled source unit.

**Why not call `Clrscr` every frame?**  
Clearing and redraw­ing everything causes flicker and unnecessary console calls. We clear only the memory buffer and print changed cells.

**Why can a hidden mine hit me?**  
The renderer checks `hidden`; the collision procedure checks `active` and coordinates. The object remains in the array.

**Why does `DIV` need `EDX = 0` here?**  
Unsigned 32-bit `DIV` divides the 64-bit value `EDX:EAX`. For these small unsigned dividends, the upper half must be zero. Otherwise the result can be wrong or the quotient can overflow.

**What does `USES eax ecx` do?**  
MASM generates pushes at procedure entry and matching pops before return. The caller's values in those registers are preserved. It does not automatically preserve registers not listed.

**Does `USES` preserve flags?**  
No. Do not assume `ZF` or `CF` survives a procedure call unless its contract explicitly says so.

**Why is the frame rate a target, not a guarantee?**  
The OS schedules other programs, console calls take time, and `Beep` blocks. The loop waits for the remaining time when possible; it cannot guarantee hard real-time deadlines.

**Where is the high score saved?**  
In `highscore.dat` in the current working directory. It stores one four-byte DWORD in little-endian binary form, not readable decimal text.

**What happens when I press ESC during a round?**  
The round ends and the menu returns. The current score is not saved. Saving happens at game over, as described in the instructions.

## 7. Three-minute demonstration script

1. Show the menu and high score. Open instructions, return, then start.
2. Move with both letters and arrow keys. Touch both boundaries.
3. Fire several torpedoes. Point out the small firing gap.
4. Let charges fall. Explain that `*` is visible and hidden mines are in memory.
5. Press `SPACE`. Point to `SONAR ACTIVE` and any green `!` marks.
6. Press `P` during sonar, wait, then resume. Explain the remembered state.
7. Hit a charge if possible; show the explosion and score change.
8. Lose three lives or use the debugger to demonstrate `LoseLife` honestly.
9. Show game over and the saved high score. Restart the program to show persistence.
10. Start a new round and show score 0, lives 3, level 1, and empty arrays.

If random play does not produce a hit during the short demo, use a prepared debugger state and say it is a controlled test. Do not pretend a random event was guaranteed.

## 8. Debugger questions you may be asked

- Put a breakpoint at `DoPlaying` and step through one frame.
- Watch `subX`, `score`, `lives`, `level`, and `gameState`.
- Open Memory at `Charges` and identify four bytes per object.
- Open Memory at `ScreenBuf` and find a known character/colour WORD.
- Break at `Hit` in `collision.inc` and explain which two objects matched.
- Break at `Rand` and show `EDX` cleared before `DIV`.
- Break at `SaveHighScore` and show the four-byte write.

## 9. Honest preparation checklist

- [ ] I built the exact commit on my own/lab Windows PC.
- [ ] I can draw the frame loop without looking.
- [ ] I can explain every procedure in my own folder.
- [ ] I read the other two members' summaries.
- [ ] I ran the manual tests and recorded real results.
- [ ] I personalized my report and disclosed AI assistance.
- [ ] I can explain a limitation instead of guessing.
