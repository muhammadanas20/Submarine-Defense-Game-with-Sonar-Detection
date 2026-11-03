# Proposal-to-implementation notes

The submitted proposal remains the design target. This page records small, explicit implementation decisions so the viva answer matches the code.

| Proposal item | Implementation status | Note |
|---|---|---|
| 80 × 25 console area | Implemented | Console must be at least this size; no resizable graphics |
| A/D, arrows, W, SPACE, P, ESC | Implemented | P also works during sonar; ESC does not save the round |
| 8 torpedo slots, 3-frame cooldown | Implemented | Normal flight usually holds about 7; capacity guard tested at 8 |
| 15 charges, about 20% hidden | Implemented | Simple LCG modulo; not cryptographic randomness |
| +10 / +25, 3 lives, level every 200 | Implemented | Level cap 9; lookup-table delays |
| Sonar 2 s, recharge 10 s | Implemented | Frame-boundary, best-effort timing; pause extends active sonar |
| Changed-cell renderer | Implemented | Ordinary CMP loop; optional REPE CMPSW fast path omitted |
| Five-frame explosions | Implemented | Five slots; effect skipped only if all slots busy |
| Five Beep effects | Implemented | Blocking tones; audible device test pending |
| Menu/instructions/pause/game over | Implemented | Key flushing at transitions |
| highscore.dat | Implemented | Four-byte DWORD; saved at game over only; simple non-atomic write |
| PROTO/INVOKE, USES, stack, LOCAL | Implemented | Win32 calls, procedure saves, sound macro, PutNumber local buffer |
| REP STOSB/STOSW/MOVSD | Implemented | Reset, clear, and previous-frame copy |
| Recursion / inline assembly / extended arithmetic | Not used | Not required by the proposal; not added merely to name-drop topics |

## Timing honesty

`GetMseconds` and `Delay` provide an 80 ms frame target. Windows scheduling, console output, and blocking `Beep` can lengthen a frame. Sonar/cooldown checks happen at frame boundaries. The project therefore says “about two seconds” and “target 12.5 FPS,” not a hardware real-time guarantee.

## High-score honesty

The file is written only when a round ends through game over and the score is higher. ESC abandons the round. A failed write leaves the previous in-memory record and shows an error. Because the simple implementation truncates the target file directly, an interrupted write can leave a short file; the next load treats that as zero. Atomic rename was left out to keep the file code short.

## Verification honesty

Compatibility assembly/link, procedure checks, and console smoke tests were run under Wine. Visual Studio 2022, native lab hardware, audible output, and the ten-minute lab soak test are still pending. See the dated verification record and acceptance checklist.
