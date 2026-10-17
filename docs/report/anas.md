# Final report section — Muhammad Anas (25K-0899)

**Member:** Muhammad Anas (25K-0899) — Group Leader  
**Course:** EL-2003 Computer Organization and Assembly Language Lab, Fall 2026 (BCS-3C)  
**Owned files:** `src/game.asm`, `src/shared/constants.inc`, `src/shared/data.inc`, `src/anas/input.inc`, `src/anas/torpedo.inc`, `src/anas/collision.inc`, `src/anas/stubs_anas.inc`

---

## 1. Responsibilities and implementation

As the Group Leader, my job is to build the core engine that runs the game every frame and connects Alyan's drawing procedures with Ali's game-rule procedures. My code is divided into eight procedures across `src/game.asm` and `src/anas/`:

### 1.1 `main` (`src/game.asm`)
- Calls `InitSystem` (Alyan) once at startup to set up the console and seed the random generator, and `LoadHighScore` (Ali) to read the saved best score from `highscore.dat`.
- Runs the outer `MenuLoop`:
  1. Calls `ShowMenu` (Ali), which sets `gameState` to either `ST_PLAYING` or `ST_EXIT`.
  2. If `gameState == ST_EXIT`, clears the screen with `Clrscr` and exits the program.
  3. Otherwise, calls `InitGame` to reset all variables for a fresh round, then calls `GameLoop` to run the match until game over or `ESC`.

### 1.2 `InitGame` (`src/game.asm`)
- Prepares a completely clean state before every new game so leftover objects from a previous round never appear:
  1. Sets `score = 0`, `lives = 3`, `level = 1`, `subX = 40` (middle of the 80-column screen), `fireCooldown = 0`, and `sonarReadyAt = 0`.
  2. Calls `ApplyLevel` (Ali) to set `fallDelay` and `spawnDelay` for level 1, and copies those values into `fallTimer` and `spawnTimer`.
  3. Clears all three `GameObject` arrays (`Torpedoes`, `Charges`, `Explosions`) to zero using `cld`, `mov al, 0`, `mov edi, OFFSET <Array>`, `mov ecx, SIZEOF <Array>`, and `rep stosb`.
  4. Calls `Clrscr` and `InvalidateScreen` (Alyan) so the next frame redraws the entire console screen.
  5. Sets `gameState = ST_PLAYING` and saves the starting timestamp from `GetMseconds` into `lastFrame`.

### 1.3 `GameLoop` (`src/game.asm`)
- Runs one pass per frame (every 80 ms) as a finite-state machine controlled by `gameState`:
  1. Calls `HandleInput` to process any keys waiting in the keyboard buffer.
  2. Checks `gameState` (loaded into `AL` because `gameState` is a `BYTE`):
     - `ST_PLAYING` (1): updates all objects (`UpdateTorpedoes`, `UpdateCharges`, `SpawnCharge`, `UpdateExplosions`), checks hits (`CheckCollisions`), and then draws the frame.
     - `ST_SONAR` (2): freezes object movement, calls `UpdateSonar` (Alyan) to check if the 2-second sonar timer is over, and draws the frame (showing hidden mines as `!`).
     - `ST_PAUSED` (3): skips all movement and collision updates and jumps straight to drawing (`BuildFrame`, `Render`, `FrameDelay`).
     - `ST_GAMEOVER` (4) or `ST_MENU` (0): exits the loop. If `gameState == ST_GAMEOVER`, calls `GameOverScreen` (Ali) before returning to `main`.

### 1.4 `FrameDelay` (`src/game.asm`)
- Keeps the game running at a steady speed (`FRAME_MS = 80` ms per frame, or ~12.5 frames per second) on any PC:
  1. Calls `GetMseconds` and subtracts `lastFrame` to find how many milliseconds the current frame took so far (`elapsed = now - lastFrame`).
  2. If `elapsed < 80`, calculates the remaining time (`80 - elapsed` using `neg eax` and `add eax, FRAME_MS`) and calls `Delay` to sleep for only the remaining milliseconds.
  3. Calls `GetMseconds` again to update `lastFrame` and increments `frameCount`.

### 1.5 `HandleInput` (`src/anas/input.inc`)
- Reads keyboard input without stopping the game using Irvine32's `ReadKey`:
  1. If `ZF = 1`, no key was pressed, so `HandleInput` returns immediately.
  2. Loops back to `NextKey` until the keyboard buffer is empty so holding down a key never creates input lag.
  3. Checks `AL = 0` first for extended keys (arrow keys put virtual-key codes `VK_LEFT` or `VK_RIGHT` in `DX`).
  4. Checks `ESC` (`1Bh`) and `SPACE` (`' '`) before converting letters to lowercase with `or al, 20h` (so Caps Lock does not break `A`, `D`, `W`, `P`).
  5. Applies movement boundary checks using unsigned comparisons (`jbe` and `jae`) so `subX` stays between `MIN_COL` (1) and `MAX_COL` (78).

### 1.6 `FireTorpedo` and `UpdateTorpedoes` (`src/anas/torpedo.inc`)
- **`FireTorpedo`:** Checks `fireCooldown`. If `fireCooldown == 0`, walks the 8-slot `Torpedoes` array using `ESI` (`add esi, TYPE GameObject`). In the first free slot (`active == 0`), sets `xPos = subX`, `yPos = SUB_ROW - 1` (row 22, right above the submarine), `active = 1`, sets `fireCooldown = 3` (creating a 3-frame gap between shots), and calls `PlayFireSound`.
- **`UpdateTorpedoes`:** Decrements `fireCooldown` if it is greater than 0. Then loops through all 8 slots in `Torpedoes`: for each active torpedo, decreases `yPos` by 1 (`dec (GameObject PTR [esi]).yPos`). If `yPos < TOP_ROW` (row 2), sets `active = 0` so the slot can be reused.

### 1.7 `CheckCollisions` (`src/anas/collision.inc`)
- Uses array coordinates in memory (not screen characters), which is why invisible mines (`hidden = 1`) still collide normally:
  1. **Torpedo vs. Charge (nested loop):** Outer loop walks `Torpedoes` with `ESI` and `ECX` (`loop TorpLoop`). Inner loop walks `Charges` with `EDI` and `EDX` (`dec edx` / `jnz ChargeLoop`). If both are active and in the same column (`xPos`), it checks if they are on the **same row** (`al == bl`) OR if the torpedo is **one row above the charge** (`al + 1 == bl`, meaning they crossed each other during the same frame). On a hit, both slots are set to `active = 0`, `AddScore` is called with `EAX = 10` (visible charge) or `EAX = 25` (hidden mine), `StartExplosion` and `PlayExplosionSound` are called, and execution jumps to `NextTorp` so one torpedo cannot destroy two charges.
  2. **Charge vs. Submarine (single loop):** Walks `Charges` with `EDI` and `ECX`. If an active charge reaches `yPos == SUB_ROW` (row 23) and `xPos == subX`, deactivates the charge, triggers an explosion at the submarine's position, and calls `LoseLife` (Ali). If `LoseLife` sets `gameState = ST_GAMEOVER`, the loop stops immediately.

---

## 2. Design decisions

1. **State Machine Architecture (`gameState`):** Using a single byte (`ST_MENU`, `ST_PLAYING`, `ST_SONAR`, `ST_PAUSED`, `ST_GAMEOVER`, `ST_EXIT`) keeps `GameLoop` simple and easy to debug. Pausing or activating sonar does not require separate loops; `GameLoop` simply skips `DoPlaying` updates while still calling `BuildFrame`, `Render`, and `FrameDelay`.
2. **80 ms Frame Target (`FrameDelay`):** Calling `Delay 80` blindly would make the game slower whenever drawing or sound takes time. Measuring elapsed time with `GetMseconds` and sleeping only for `80 - elapsed` keeps gameplay at a steady ~12.5 FPS on any computer.
3. **4-Byte `GameObject` Structure:** Every torpedo, charge, and explosion uses the same 4-byte `GameObject STRUCT` (`xPos`, `yPos`, `active`, `hidden`). Walking any array uses the exact same pattern: `add esi, TYPE GameObject` (adds 4 bytes).
4. **Torpedo Cooldown (`fireCooldown = 3`):** Without a cooldown, holding `W` would fire 8 torpedoes in 8 consecutive frames as a solid line. A 3-frame cooldown spaces shots out naturally.
5. **Crossing Collision Check (`inc al` / `cmp al, bl`):** In the same frame, a torpedo moves up 1 row (`yPos` decreases) and a charge can move down 1 row (`yPos` increases). If they started on adjacent rows, they swap rows without ever landing on the exact same row number. Checking both `torp.yPos == charge.yPos` and `torp.yPos + 1 == charge.yPos` guarantees no shot passes through a falling charge.

### State Diagram / Program Flow

```text
                  +-------------------+
                  |   Program Start   |
                  |   InitSystem      |
                  |   LoadHighScore   |
                  +---------+---------+
                            |
                            v
                  +-------------------+   Option 3 / ESC
        +-------->|     ST_MENU       +------------------> [ Quit / Exit ]
        |         |    (ShowMenu)     |
        |         +---------+---------+
        |                   | Option 1 (Start Game)
        |                   | -> InitGame
        |                   v
        |         +-------------------+
        |   ESC   |    ST_PLAYING     |<-----------------+
        +---------+  Update objects   |                  |
        |         |  CheckCollisions  |                  |
        |         +----+----+----+----+                  |
        |              |    |    |                       |
        |     SPACE    |    |    | P key                 | P key
        |              v    |    v                       |
        |    +-----------+  |  +-------------+           |
        |    | ST_SONAR  |  |  |  ST_PAUSED  +-----------+
        |    | (2 sec)   |  |  | (Draw only) |
        |    +-----+-----+  |  +-------------+
        |          |        |
        |          +--->----+  (After 2000 ms, returns to ST_PLAYING)
        |                   |
        |                   | lives == 0 (in LoseLife)
        |                   v
        |         +-------------------+
        |         |   ST_GAMEOVER     |
        +---------+ (GameOverScreen)  |
                  +-------------------+
```

---

## 3. Testing evidence

Full acceptance testing is tracked in [`docs/testing/acceptance-checklist.md`](../testing/acceptance-checklist.md). Below are the unit and integration checks for Anas's modules:

| Test item | Module / Procedure | Steps | Expected result |
|---|---|---|---|
| State loop & frame timing | `game.asm` (`GameLoop`, `FrameDelay`) | Run game, watch `frameCount` in debugger | `frameCount` increases by ~12 per second (80 ms per frame) |
| Submarine movement & borders | `input.inc` (`HandleInput`) | Hold `A`/`D` and Left/Right arrows; test with Caps Lock on | Submarine moves smoothly and stops at `MIN_COL` (1) and `MAX_COL` (78) |
| Torpedo firing & limit | `torpedo.inc` (`FireTorpedo`, `UpdateTorpedoes`) | Hold `W` continuously | Fires with a 3-frame gap; max 8 active torpedoes; slots free at `TOP_ROW` (2) |
| Torpedo vs. charge collision | `collision.inc` (`CheckCollisions`) | Shoot visible charges (`*`) and hidden mines (`!`) | Both disappear, explosion starts, +10 for visible charge, +25 for hidden mine |
| Charge vs. submarine collision | `collision.inc` (`CheckCollisions`) | Let a charge reach row 23 (`SUB_ROW`) at `subX` | Charge removed, explosion at submarine, `LoseLife` called, game over after 3 hits |
| Pause and resume | `input.inc` + `game.asm` | Press `P` during play, then press `P` again | `ST_PAUSED` freezes all movement while screen still renders; second `P` resumes |
| New-game reset | `game.asm` (`InitGame`) | Finish a game, return to menu, start a new game | Score = 0, lives = 3, level = 1, `subX = 40`, all object arrays cleared to 0 |

---

## 4. Integration and Git workflow

- **Repository structure & ownership:** Each member works in their own folder (`src/anas/`, `src/alyan/`, `src/ali/`) and updates only their own progress/report files so pull requests merge without file conflicts.
- **Stub-based incremental integration:** `stubs_anas.inc`, `stubs_alyan.inc`, and `stubs_ali.inc` allow `src/game.asm` to assemble and link at every milestone even while individual procedures are still being written. As all four of my procedures (`HandleInput`, `FireTorpedo`, `UpdateTorpedoes`, `CheckCollisions`) are now implemented in `src/anas/`, their stub lines in `src/anas/stubs_anas.inc` have been removed.
- **Branch & PR workflow:** Work is committed on a dedicated branch without `git add .` (staging only Anas-owned files) and merged via Pull Request in the order Anas -> Alyan -> Ali.

---

## 5. AI-use disclosure

Reference examples and repository scaffolding from an AI-assisted implementation guide were studied and adapted for the project structure, module stubs, and assembly procedures. Every procedure (`main`, `InitGame`, `GameLoop`, `FrameDelay`, `HandleInput`, `FireTorpedo`, `UpdateTorpedoes`, and `CheckCollisions`) was reviewed line by line so that all team members understand and can explain the code during the individual viva.

---

## 6. Viva preparation notes

### Questions on Anas's modules

1. **Why can't the game use `ReadChar`? How does `ReadKey` tell you that no key was pressed?**
   - `ReadChar` is a blocking call: it pauses the entire program and waits until the user presses a key, which would freeze the falling charges and torpedoes. `ReadKey` is non-blocking: it checks the keyboard buffer and returns immediately. If no key is waiting, `ReadKey` sets the Zero Flag (`ZF = 1`), so `jz Done` jumps out right away.

2. **Explain how `FrameDelay` keeps the same speed on every PC.**
   - At the end of a frame, `FrameDelay` calls `GetMseconds` and subtracts `lastFrame` to find `elapsed` (how many milliseconds the current frame already used). If `elapsed < 80`, it sleeps for only the remaining time (`80 - elapsed`) using `Delay`. If a slow PC took 30 ms to draw, it sleeps 50 ms; if a fast PC took 5 ms, it sleeps 75 ms. Both finish the frame in 80 ms.

3. **Walk through `CheckCollisions`. Why do the two loops need different counters?**
   - Torpedo-vs-charge collision uses a nested loop: for every torpedo (8 slots), we check every charge (15 slots). If both the outer loop and inner loop used `ECX`, the inner loop would overwrite `ECX` and break the outer loop. Therefore, the outer loop uses `ECX` with the `LOOP` instruction, and the inner loop uses `EDX` with `dec edx` and `jnz ChargeLoop`.

4. **What is the "crossing" problem and how does the extra row check fix it?**
   - Suppose a charge is at row 10 and a torpedo is right below it at row 11. In the next frame, the torpedo moves up to row 10 and the charge moves down to row 11. They passed right through each other, so their rows are never equal (`10 != 11`). By checking if `torp.yPos == charge.yPos` OR `torp.yPos + 1 == charge.yPos` (`inc al` then `cmp al, bl`), we catch objects that swapped rows in the same frame.

5. **Draw the state machine. Which key or event moves the game into each state?**
   - `ST_MENU (0)` -> press `1` in menu -> `ST_PLAYING (1)`.
   - `ST_PLAYING (1)` -> press `SPACE` (when cooldown ready) -> `ST_SONAR (2)` -> after 2000 ms -> `ST_PLAYING (1)`.
   - `ST_PLAYING (1)` -> press `P` -> `ST_PAUSED (3)` -> press `P` -> `ST_PLAYING (1)`.
   - `ST_PLAYING (1)` -> press `ESC` -> `ST_MENU (0)`.
   - `ST_PLAYING (1)` -> `lives` reaches 0 in `LoseLife` -> `ST_GAMEOVER (4)` -> after `GameOverScreen` -> `ST_MENU (0)`.
   - `ST_MENU (0)` -> press `3` or `ESC` in menu -> `ST_EXIT (5)` (program ends).

6. **Why `add esi, TYPE GameObject` and not `add esi, 1`? What is `TYPE GameObject`?**
   - Each `GameObject` structure has 4 `BYTE` fields (`xPos`, `yPos`, `active`, `hidden`), so `TYPE GameObject` is `4`. Adding `4` moves `ESI` to the start of the next struct in the array. Adding `1` would move `ESI` to `yPos` inside the same struct.

7. **How does `InitGame` clear the arrays? Which registers does `REP STOSB` use?**
   - `REP STOSB` copies the byte in `AL` into the memory address pointed to by `EDI`, increments `EDI` (when the Direction Flag is cleared with `cld`), and repeats `ECX` times. In `InitGame`, we set `AL = 0`, `EDI = OFFSET <Array>`, and `ECX = SIZEOF <Array>`, which zeros every byte of `Torpedoes`, `Charges`, and `Explosions`.

### Questions on teammates' modules (Alyan & Ali)

1. **How does the renderer avoid flicker? (Alyan)**
   - It uses double buffering with `ScreenBuf` (current frame) and `PrevBuf` (previous frame). `BuildFrame` draws everything into `ScreenBuf` in memory, and `Render` compares `ScreenBuf` with `PrevBuf` cell by cell, calling `Gotoxy` and `WriteChar` only for cells that changed.

2. **Where is row 5, column 10 in `ScreenBuf`? (Alyan)**
   - Each row has 80 cells and each cell is a `WORD` (2 bytes). The byte offset is `((5 * 80) + 10) * 2 = 410 * 2 = 820`.

3. **How does `Rand` work, and why must `EDX` be 0 before `DIV`? (Ali)**
   - `Rand` uses a Linear Congruential Generator (`seed = seed * 1103515245 + 12345`), shifts right to take the upper bits, and divides by the range (`ECX`) so the remainder in `EDX` is between `0` and `range - 1`. In 32-bit `DIV reg32`, the CPU divides the 64-bit value `EDX:EAX` by the operand; if `EDX` is not cleared to `0` (`xor edx, edx`), garbage in `EDX` causes a wrong remainder or an integer overflow crash.

4. **How is the high score saved in the file? (Ali)**
   - `SaveHighScore` compares `score` with `highScore`. If `score > highScore`, it updates `highScore` and uses Irvine32's `CreateOutputFile`, `WriteToFile` (writing the 4-byte `DWORD` directly to `highscore.dat`), and `CloseFile`.
