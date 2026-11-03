# Report section draft — Syed Alyan Hussain (25K-0648)

**Review required:** this is an AI-assisted draft describing the repository code. Personalize it, verify every statement, and add your own build/test evidence before submission.

## Responsibilities and implementation

My area is console setup, the two screen buffers, changed-cell rendering, the HUD, explosions, and sonar. `BuildFrame` clears a 2000-WORD memory buffer and draws borders, objects, explosions, and the HUD. `Render` compares it with `PrevBuf` and sends only changed cells to the console, then copies the frame with `REP MOVSD`. The bottom-right cell is never printed to avoid scrolling.

`PutCell` converts row/column coordinates into a WORD offset and checks screen bounds. `PutNumber` converts a value to five decimal digits using repeated division by ten and a small `LOCAL` stack buffer. `DrawHUD` shows score, lives, level, sonar status, and a pause message. Explosions use five fixed slots and a five-entry character/colour table. Sonar changes the state, reveals hidden charges, plays the sweep once, and starts a ten-second recharge after the reveal.

## Design decisions

I used ordinary cell-by-cell comparison rather than the optional `REPE CMPSW` fast renderer because it is easier to trace in the debugger. Hidden mines are skipped only by drawing code; their active flags and coordinates remain available to collisions. The HUD is drawn last so the pause message remains readable over objects. The five-digit score display is a simple presentation limit.

## Testing evidence

The integrated source passed assembly/link and a 1,090-check harness under Wine, including buffer offsets, hidden-mine visibility, HUD digits, previous-buffer copying, explosion lifetime, and sonar state. A console smoke test showed the menu, gameplay, and pause message. Native Windows flicker, colour appearance, and audible sonar sweep still require lab-PC verification. I will add screenshots and exact environment details only after running those tests.

## Integration and reflection

My procedures read Anas's state/object data and Ali's score/lives/level data. Pause during sonar required a shared contract: input remembers the previous state and adjusts the sonar start time. The main lesson is the difference between logical object state and visual representation.

## AI-use / source disclosure

AI assistance was used to implement and review this module and prepare this draft, following the repository's AI-assisted guides. I will review every procedure, disclose assistance as required, and submit only work I can explain. References include the course outline, Irvine32 console procedures, and Microsoft MASM documentation.
