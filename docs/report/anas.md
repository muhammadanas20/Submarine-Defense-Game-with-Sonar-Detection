# Report section draft — Muhammad Anas (25K-0899)

**Review required:** this is an AI-assisted draft describing the repository code. Personalize it, verify every statement, and add your own build/test evidence before submission.

## Responsibilities and implementation

My area is the main program, shared data contract, frame loop, input, submarine movement, torpedoes, collisions, pause, reset, and integration. `main` initializes the console and saved record, then alternates between the menu and a round. `InitGame` resets all round state while preserving the high score. `GameLoop` runs input, updates, collisions, rendering, and frame delay according to `gameState`.

`HandleInput` uses non-blocking `ReadKey`, supports letters and arrows, checks unsigned movement boundaries, and handles fire, sonar, pause, and ESC. Pause remembers whether normal play or sonar was interrupted. When resuming sonar, the paused duration is added to its start timestamp so the reveal is not shortened.

`FireTorpedo` searches eight fixed slots and enforces a three-frame cooldown. `UpdateTorpedoes` moves active shots upward and frees slots above the playfield. `CheckCollisions` compares coordinates in memory, including the one-row crossing case, awards +10/+25 through Ali's procedure, starts Alyan's explosion, and processes at most one submarine hit per frame.

## Design decisions

I used a single BYTE state instead of separate game loops. Fixed arrays and a four-byte structure make every object loop similar. The outer collision loop uses ECX and the inner loop uses EDX so their counters do not conflict. `REP STOSB` clears object arrays and explosion timers on replay. The frame delay sleeps only for the remaining part of the 80 ms target; blocking sounds may lengthen a frame, so the project does not claim hard real-time behavior.

## Testing evidence

The integrated source was assembled with MASM 6.14, linked as a Win32 console executable, and exercised under Wine on 3 November 2026. A separate harness passed 1,090 checks against the actual procedures. Visual Studio 2022 and the native lab PC remain unverified. My next evidence task is to record the exact lab environment and complete the movement, collision, pause, replay, and long-run rows in the acceptance checklist.

## Integration and reflection

The completion PR integrates all three folders and removes temporary stubs. I must review the shared pause variables with Alyan and the score/life calls with Ali. The main lesson is that a procedure contract includes register preservation, state transitions, and reset behavior—not only the procedure name.

## AI-use / source disclosure

AI assistance was used to complete and review integration code and prepare this draft, building on the repository's AI-assisted proposal and member guides. I will disclose this according to the instructor's policy and will not present unreviewed generated text or code as unaided work. Primary references are the course outline, Irvine32 library documentation, and Microsoft MASM/Win32 documentation.
