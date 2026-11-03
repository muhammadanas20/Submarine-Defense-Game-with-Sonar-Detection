# Viva guide — Muhammad Anas (25K-0899)

**Your area:** main loop, state, timing, input, submarine, torpedoes, collisions, reset, integration.  
**Files:** `src/game.asm`, `src/shared/`, `src/anas/`.

Read `00-common.md` first. Use these answers as study notes, then explain them in your own words.

## 1. Your 30-second introduction

> I connect the three modules. My main procedure starts the console and loads the high score. InitGame resets a round. GameLoop reads input, updates objects, checks collisions, draws, and waits. I also handle movement, firing, pause, and the coordinate comparisons that decide hits.

## 2. Procedure map

| Procedure | Input | What it changes / returns |
|---|---|---|
| `main` | Program start | Menu → new round → game loop → menu/exit |
| `InitGame` | None | Resets round data; keeps `highScore` |
| `GameLoop` | Current `gameState` | Runs frames until menu or game over |
| `FrameDelay` | `lastFrame` timestamp | Waits remaining frame time; updates `lastFrame`, `frameCount` |
| `HandleInput` | Console key queue | Changes position/state or fires/requests sonar |
| `FireTorpedo` | `subX`, `fireCooldown` | Uses one free torpedo slot if allowed |
| `UpdateTorpedoes` | Torpedo array | Moves active shots up; frees top-exit slots |
| `CheckCollisions` | Torpedo/charge arrays, `subX` | Deactivates hit objects; calls score/life/effect procedures |

## 3. Walk through `GameLoop`

```text
HandleInput
  PLAYING -> UpdateTorpedoes -> UpdateCharges -> SpawnCharge
             -> UpdateExplosions -> CheckCollisions -> draw
  SONAR   -> UpdateSonar -> draw
  PAUSED  -> draw only
  MENU/GAMEOVER -> leave loop
```

Input and drawing still happen during pause and sonar. Only object movement/collision updates are skipped. If the last life is lost, the loop goes to game-over handling instead of continuing normal play.

**Viva answer:** “A state variable is simpler than separate loops for every mode. Each frame checks the state and runs only the appropriate work.”

## 4. Input and movement

`ReadKey` is non-blocking in Irvine32: `ZF=1` means no key. The procedure drains waiting keys so old repeats do not build a long lag queue.

- `AL=0` marks a special key; `DX` contains the virtual-key code.
- `VK_LEFT` and `VK_RIGHT` handle arrows.
- `OR al,20h` converts ASCII uppercase letters to lowercase.
- `ESC` and `SPACE` are checked before that conversion.
- Movement is allowed only in `ST_PLAYING`.
- Left boundary: `cmp subX, MIN_COL` then `jbe` prevents going below 1.
- Right boundary: `cmp subX, MAX_COL` then `jae` prevents going above 78.

**Why unsigned jumps?** Coordinates are non-negative BYTE values. `JB/JAE` and `JBE/JA` express unsigned boundaries correctly.

## 5. Pause during sonar

`stateBeforePause` remembers `ST_PLAYING` or `ST_SONAR`. `pauseStarted` stores the time.

On resume from sonar:

```text
pausedTime = now - pauseStarted
sonarStart = sonarStart + pausedTime
gameState = ST_SONAR
```

The elapsed sonar time therefore excludes the pause. This is a small fix over the original guide, which only paused normal play.

## 6. Torpedo trace

Assume `subX=40`, all slots free, cooldown 0.

1. `FireTorpedo` finds slot 0.
2. It writes `xPos=40`, `yPos=22`, `active=1`.
3. It sets `fireCooldown=3` and plays a short tone.
4. The next three update frames decrease the cooldown.
5. Each update decreases active torpedoes' rows by one.
6. A shot moving above `TOP_ROW` becomes inactive.

The array has eight slots. With the three-frame firing gap and roughly twenty rows of flight, normal play usually holds about seven shots; the eight-slot guard is still tested by filling the array in the validation harness. “Up to eight” is a capacity limit, not a promise that eight are always reachable in ordinary play.

## 7. Collision trace

### Torpedo versus charge

For each active torpedo, check every active charge:

1. Columns must match.
2. Rows match **or** the torpedo is one row above the charge.
3. Deactivate both objects.
4. Add 10 points, or 25 if `hidden=1`.
5. Start an explosion and play its sound.
6. Move to the next torpedo so one shot cannot score twice.

The outer loop uses `ECX`; the inner loop uses `EDX`. If both used `ECX`, the inner loop would destroy the outer count.

### Why check one row above?

Suppose a torpedo is at row 11 and a charge at row 10 in the same column. After both move, they swap to rows 10 and 11. Equality alone misses the crossing. The extra `torpedoRow + 1 == chargeRow` check catches that one-row crossing. Objects move at most one row per update, so a larger sweep is unnecessary.

### Charge versus submarine

An active charge at `SUB_ROW` and the current `subX` hits. The code removes it, starts an explosion, and calls `LoseLife`. It stops checking submarine hits for that frame, so a cluster cannot take several lives in one frame.

## 8. Reset and string instructions

`InitGame` resets score, lives, level, position, cooldowns, sonar variables, pause variables, and frame count. It keeps `highScore`.

`REP STOSB` writes `AL` to `[EDI]`, advances `EDI`, and repeats `ECX` times. With `AL=0`, it clears each object array and `ExplTimer`. `CLD` makes the pointer move forward.

**Why clear `ExplTimer` too?** Clearing only `active` would leave old countdown bytes. A later slot reuse should start from a clean, predictable state.

## 9. Likely questions and short answers

**Why not `ReadChar`?** It waits for a key and would stop the game while waiting.

**Why 80 ms?** `1000 / 80 = 12.5` frames per second, slow enough for a text console and simple assembly loops.

**What if a frame takes more than 80 ms?** Do not sleep; continue. The project does not try to catch up with multiple object steps.

**Why fixed arrays?** The maximum object count is known. Fixed slots avoid heap allocation and make indexing easy to explain.

**What is `SIZEOF Torpedoes`?** 32 bytes: eight objects × four bytes.

**What is the difference between `SIZEOF` and `LENGTHOF`?** `SIZEOF` is bytes; `LENGTHOF` is element count. For `Torpedoes`, they are 32 and 8.

**Why does `CheckCollisions` not read the screen?** Screen characters are only a view. Logical coordinates and flags are the source of truth, including for hidden mines.

**What does your module call from Alyan?** `InitSystem`, `InvalidateScreen`, `BuildFrame`, `Render`, `UpdateExplosions`, `StartExplosion`, `StartSonar`, `UpdateSonar`.

**What does it call from Ali?** Menu/game-over, random setup through `InitSystem`, charge updates/spawn, score/life/level, sounds, and high-score load.

## 10. Practical task before viva

- Build Win32 and run from the menu.
- Break at `HandleInput`, press `D`, and watch `subX` increase.
- Break at `FireTorpedo` and inspect the four bytes written.
- Force two objects into the crossing positions in the debugger and step `CheckCollisions`.
- Pause during sonar and explain the two shared pause variables.
- Show one `REP STOSB` clearing an array in the Memory window.

## 11. Limitations you can state confidently

- Timing is best-effort, not real-time guaranteed.
- One submarine hit is processed per frame to avoid instant multi-life loss.
- The game saves only at game over, not on ESC.
- The optional fast string-compare renderer was left out to keep the code easy to explain.
