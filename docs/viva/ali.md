# Viva guide — Ali Raza (25K-0827)

**Your area:** random numbers, charges/mines, menus, score/lives/levels, sound, high-score file.  
**Files:** `src/ali/`.

Read `00-common.md` first. Be ready to explain unsigned division and the difference between a hidden object and an inactive object.

## 1. Your 30-second introduction

> I provide the game rules and content. My random generator chooses charge columns and hidden mines. Timers control spawning and falling. I update score, lives, and level, show the menu and game-over screen, play short Beep effects, and save the best score to a four-byte file.

## 2. Procedure map

| Procedure | Input | Result |
|---|---|---|
| `SeedRandom` | Clock | Initializes `seed` |
| `Rand` | `EAX` = positive range | `EAX` = 0 through range−1 |
| `SpawnCharge` | Spawn timer, free charge slot | New visible charge or hidden mine |
| `UpdateCharges` | Fall timer | Moves active charges down every N frames |
| `AddScore` | `EAX` = points | Adds score and recalculates level |
| `LoseLife` | Submarine hit | Decrements life; game over at zero; otherwise recenter |
| `ApplyLevel` | `level` | Copies fall/spawn delays from tables |
| `ShowMenu` | Key queue | Start, instructions, or exit state |
| `ShowInstructions` | None | Rules/controls; waits for a key |
| `GameOverScreen` | Final score | Saves record, shows result, waits, returns to menu |
| `Play...Sound` | Event | Blocking Windows Beep tone(s) |
| `LoadHighScore` | File | Valid DWORD or zero |
| `SaveHighScore` | Score vs record | Writes only a new record; reports failure |

## 3. Random numbers

The generator is a small linear congruential generator (LCG):

```text
seed = (seed * 1103515245 + 12345) mod 2^32
value = seed >> 16
result = value mod range
```

- `MUL ecx` produces `EDX:EAX`; keeping low `EAX` gives modulo `2^32` naturally.
- `SHR eax,16` uses upper bits, which are less visibly patterned in this simple LCG.
- `XOR edx,edx` clears the upper dividend before `DIV ebx`.
- The remainder in `EDX` becomes the return value in `EAX`.
- Range 78 gives 0–77; adding `MIN_COL` gives columns 1–78.
- Range 5 gives 0–4; result 0 marks about 20% as hidden.
- A zero range returns zero instead of dividing by zero.

This is pseudo-random game logic, not cryptography. Modulo can introduce a tiny bias; that is acceptable for this course game and not worth a complex rejection algorithm.

## 4. Charge timers

`spawnTimer` counts frames until the next spawn. At level 1, `spawnDelay=14`, so a new charge appears about every 1.12 seconds.

`fallTimer` counts frames until all active charges move one row. At level 1, `fallDelay=6`, so a charge steps about every 480 ms.

A charge starts at row 2. At row 24 it becomes inactive. Submarine collision is checked at row 23 before it reaches the sea bed.

If all 15 slots are full, spawning is skipped. The game does not allocate more memory.

## 5. Score, lives, and levels

```text
level = score / 200 + 1, maximum 9
```

Examples:

| Score | Level |
|---:|---:|
| 0–199 | 1 |
| 200–399 | 2 |
| 400–599 | 3 |
| 1600 or more | 9 |

`ApplyLevel` uses index `level−1`:

```text
fall delays:  6, 5, 5, 4, 4, 3, 3, 2, 2
spawn delays: 14,12,11,10, 9, 8, 7, 6, 5
```

Smaller number = fewer frames to wait = faster game. The current countdown is not forcibly reset on level-up; the new delay applies when that timer next reloads.

`LoseLife` plays the life-lost tones, decrements lives, and either sets game over or recenters the submarine at column 40. Anas's collision code limits submarine hits to one per frame.

## 6. Sound macro

```asm
mPlaySound MACRO frequency, duration
    pushad
    INVOKE Beep, frequency, duration
    popad
ENDM
```

A macro is expanded by the assembler; it is not a runtime procedure call. `PUSHAD/POPAD` save the eight general-purpose registers around the Windows call.

`Beep` blocks until the tone finishes:

| Event | Tone pattern |
|---|---|
| Fire | 1200 Hz, 20 ms |
| Explosion | 150 Hz, 30 ms |
| Life lost | 300 Hz 120 ms, then 200 Hz 180 ms |
| Game over | Four descending notes |
| Sonar | 400, 500, 600, 700, 800 Hz, 50 ms each |

Normal-play tones are short. Sonar already freezes objects. Life-lost/game-over tones can lengthen a frame; the game does not claim hard real-time timing. Muting audio does not change the rules.

## 7. High-score file trace

The file contains exactly one DWORD, four bytes, little-endian. Score 250 is stored as bytes `FA 00 00 00`, not the text `"250"`.

### Load

1. Set `highScore=0` first.
2. `OpenInputFile`; missing file is a normal first-run case.
3. Read four bytes.
4. Check carry flag and byte count.
5. Close the handle.
6. A short/unreadable file leaves zero.

### Save

1. Clear `newRecord` and `saveFailed`.
2. Compare score with the old record using unsigned `JBE`.
3. If not higher, return.
4. Create/truncate the file and write four bytes.
5. Check the written count and close the handle.
6. Only after a successful write update `highScore` and set `newRecord`.
7. On failure, keep the old in-memory record and show a message.

This fixes the guide's equality-message bug: tying an old record is not announced as a new record.

The simple version does not use an atomic temporary-file rename. A power loss or disk-full error during overwrite can damage the small file; the next load detects a short file and returns zero. That is a stated limitation, not a hidden feature.

## 8. Menus and game over

Menus use direct console output because objects are not moving. `Delay 30` in the wait loop avoids a full-CPU busy loop. `ReadKeyFlush` discards old gameplay/menu keys at screen transitions.

Game over saves first, then displays final score, high score, and only the correct new-record/error message. It waits for a fresh key and returns to the menu. ESC during play intentionally does not save.

## 9. Likely questions and short answers

**Why must EDX be zero before DIV?** The dividend is `EDX:EAX`; these unsigned values fit in EAX, so the upper half is zero.

**What if the file does not exist?** High score starts at zero; no crash.

**Why binary instead of text?** One DWORD is simple and fixed-size. Text would require parsing and formatting.

**Why save only at game over?** That is the proposed rule and keeps file writes out of the frame loop.

**Why is `hidden` separate from `active`?** A mine must remain logically present while visually hidden.

**Why lookup tables for levels?** Nine fixed difficulty values are easier to read and adjust than nine branches.

**Why does `PUSHAD` not save flags?** It saves general registers only. This sound macro does not promise to preserve flags.

**What does your module use from Anas?** Shared state, `subX`, game-loop calls, and collision events that call `AddScore`/`LoseLife`.

**What uses your data in Alyan's module?** The renderer draws `Charges`; the HUD reads score/lives/level and sonar readiness.

## 10. Practical task before viva

- Call `Rand(78)` repeatedly in the debugger and check the range.
- Watch a charge's four bytes change from inactive to active.
- Set score to 190, add 10, and show level 2 and the new table delays.
- Show the four bytes of score 250 in Memory and in `highscore.dat`.
- Delete the file, restart, and show high score zero.
- Explain why a tied score does not print `NEW HIGH SCORE`.

## 11. Limitations you can state confidently

- The random generator is for gameplay, not security.
- Sound is blocking and device-dependent.
- The high-score write is simple, not atomic.
- The HUD's five-digit display is separate from the DWORD score storage.
