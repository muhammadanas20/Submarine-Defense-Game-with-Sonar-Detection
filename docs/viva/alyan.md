# Viva guide — Syed Alyan Hussain (25K-0648)

**Your area:** console setup, screen buffers, changed-cell rendering, HUD, explosions, sonar.  
**Files:** `src/alyan/`.

Read `00-common.md` first. Be ready to explain both your drawing code and why hidden objects still collide.

## 1. Your 30-second introduction

> I draw the game without clearing the whole console every frame. BuildFrame paints objects into a WORD array. Render compares it with the previous frame and prints only changed cells. I also draw the status bar, animate explosions, and control the sonar reveal and recharge.

## 2. Procedure map

| Procedure | Input | Result |
|---|---|---|
| `InitSystem` | None | Seeds random, sets title, hides cursor |
| `PutCell` | `DH/DL` row/col, `AL` char, `AH` colour | Writes one WORD into `ScreenBuf` |
| `PutString` | `ESI` string, `DH/DL`, `AH` colour | Writes text into the buffer |
| `ClearBuffer` | None | Fills current buffer with blank WORDs |
| `InvalidateScreen` | None | Fills previous buffer with `FFFFh` |
| `DrawBorders` | None | Adds top/bottom ASCII borders |
| `BuildFrame` | Shared game data | Complete next frame in memory |
| `Render` | Two buffers | Prints changed cells; copies current to previous |
| `PutNumber` | `EAX` value, `DH/DL`, `BL` colour | Five decimal characters in the buffer |
| `DrawHUD` | Score/lives/level/state | Status row and pause message |
| `StartExplosion` | `AL` col, `AH` row | Finds a free effect slot, timer = 5 |
| `UpdateExplosions` | Effect timers | Decrements timers and frees expired slots |
| `DrawExplosions` | Effect slots | Chooses character/colour from lookup tables |
| `StartSonar` | Ready request from input | Sets sonar state and start time |
| `UpdateSonar` | Start time | Plays sweep once; ends after about 2 s; sets recharge |

## 3. Buffer example to memorize

`ScreenBuf` and `PrevBuf` each contain 2000 WORDs.

```text
row 5, column 10
index = 5*80 + 10 = 410
byte offset = 410*2 = 820
```

If `AL='U'` and `AH=ATTR_SUB`, `PutCell` stores both in one WORD. `MOVZX` converts the row/column bytes to 32-bit values before arithmetic. `IMUL ebx,ebx,80` calculates the row start. Scale `*2` changes a cell index into a byte offset.

`PutCell` also checks row < 25 and column < 80, so a bad coordinate cannot write outside the buffer.

## 4. Why two buffers reduce flicker

1. `ClearBuffer` clears memory, not the console.
2. `BuildFrame` draws HUD, borders, submarine, torpedoes, visible charges, and explosions.
3. `Render` compares each cell with `PrevBuf`.
4. Equal cells are skipped.
5. Changed cells use `Gotoxy`, `SetTextColor`, and `WriteChar`.
6. `REP MOVSD` copies the complete current buffer to the previous buffer.

There are 2000 WORDs but only 1000 DWORD copies because one DWORD contains two WORDs.

**Why `FFFFh` in InvalidateScreen?** After a menu or `Clrscr`, the old buffer no longer describes the console. `FFFFh` forces every normal cell to look changed on the next render.

**Why skip the last cell?** Printing row 24, column 79 can scroll the console. The border and control text stop before it.

## 5. HUD and decimal conversion

The HUD shows score, lives, level, and sonar status. `PutNumber` converts a number to five digits:

1. Save `EDX` because it holds the column and `DIV` will change it.
2. Divide by 10.
3. Remainder is the last digit; add `'0'` to make ASCII.
4. Store digits from right to left in a six-byte `LOCAL` buffer.
5. Restore the position and call `PutString`.

Example: 123 → digits `'0' '0' '1' '2' '3'` followed by zero terminator.

`LOCAL digits[6]:BYTE` creates temporary stack space. MASM uses a stack frame (`EBP`) for the procedure. This is a small, real use of the course's stack-frame topic.

The HUD is designed for scores up to 99999. The score variable itself is a DWORD; the simple five-digit display is a stated presentation limit.

## 6. Explosion trace

`StartExplosion` receives column in `AL`, row in `AH`. It searches five slots. If all are busy, only the visual effect is skipped; the hit and score still happen.

Timer values and characters:

| Timer | Table index | Character |
|---:|---:|---|
| 5 | 4 | `@` |
| 4 | 3 | `#` |
| 3 | 2 | `*` |
| 2 | 1 | `+` |
| 1 | 0 | `.` |

The game updates explosions before collision checks. A new hit draws timer 5 in that frame, then four more frames count down to 1. The next update frees the slot. Explosions freeze with the rest of the objects during sonar/pause.

`[esi+ebx*TYPE GameObject]` demonstrates base-plus-index-scaled addressing. `TYPE GameObject` is 4.

## 7. Sonar trace

1. Input accepts `SPACE` only in normal play and only when ready.
2. `StartSonar` sets `ST_SONAR`, saves the start time, clears `sonarPlayed`.
3. The loop skips object updates.
4. The first `UpdateSonar` builds and renders the revealed frame, then plays the rising sweep once.
5. Hidden charges are drawn as green `!` only while the state is sonar.
6. After about 2000 ms, state returns to playing and `sonarReadyAt = now + 10000`.
7. The HUD shows `ACTIVE`, whole seconds remaining, or `READY`.

The sweep is about 250 ms and is included in the two-second interval because the start time is saved before the sound. Timing is checked at frame boundaries, so it is approximate, not a hardware guarantee.

**Pause fix:** Anas's input code shifts `sonarStart` forward by the paused duration. Your `UpdateSonar` then naturally gives the remaining reveal time.

## 8. Likely questions and short answers

**Is this double buffering in the graphics-card sense?** It is the same idea—build then present—but implemented with console character cells, not a GPU swap chain.

**Why not optional `RenderFast`?** The ordinary comparison loop is easier to debug and explain. The proposal's core requirement is changed-cell drawing, which this provides.

**Where is the hidden flag checked?** In `BuildFrame`. Collision code does not use it to decide whether an object exists.

**Why does `REP MOVSD` use 1000, not 2000?** It copies DWORDs. Two WORD cells fit in one DWORD.

**What happens if `ClearBuffer` forgets `CLD`?** If the direction flag were set, `EDI` would move backward and corrupt memory. `CLD` guarantees forward movement.

**Why does `GetMseconds` require resetting `AH` before text?** A procedure may change `EAX`; do not assume a colour previously placed in `AH` survives.

**Why can't you draw during `ST_PAUSED` and skip input?** The player must still be able to resume or exit. The loop skips updates, not input.

## 9. Practical task before viva

- Show the WORD at row 5, column 10 in Memory.
- Break at `Render` and show an unchanged cell being skipped.
- Change `score` to 123 in the debugger and explain the five HUD characters.
- Start an explosion and watch its timer go 5 → 0.
- Activate sonar with a hidden charge present and point to the `hidden` branch.
- Explain why the bottom-right cell remains blank.

## 10. Limitations you can state confidently

- The console must be at least 80 × 25; the program draws that area rather than implementing resizable graphics.
- Five HUD digits are a simple display choice.
- Timing depends on the OS frame loop.
- The optimized `REPE CMPSW` version is intentionally absent.
