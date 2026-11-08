# Whole-game acceptance checklist

Run on a lab PC with the final integrated build. Record the actual build/tool environment and result for every row. This checklist follows the attached implementation guide; a checked box should be supported by a real test.

**Test environment:** OS __________ · PC __________ · Visual Studio __________ · Irvine32 __________ · Configuration __________ · Date __________

| Done | Test | Expected result | Owner | Actual result / evidence |
|---|---|---|---|---|
| [ ] | Build | Clean MASM build in Visual Studio (Debug \| Win32) with no `error A2008: syntax error`; no label/variable is a MASM reserved word such as `pause` or `resume` | Anas | |
| [ ] | Menu | Three options, high score, and the green submarine art (`<=-[ooo]-=>` with the `_!_` sail above it) under the title; option 2 opens instructions; option 3 / ESC exits | Ali | |
| [ ] | Movement | A/D and arrow keys move the submarine; the outer tip cells of the 11-cell hull stop at columns 1 and 78 without lag | Anas | |
| [ ] | Firing | W fires; at most 8 torpedoes are active; cooldown creates a small gap; the `^` never disappears behind the sail | Anas | |
| [ ] | Charges | `(@)` charges appear in random columns and never overlap a border; about 1 in 5 are hidden mines | Ali | |
| [ ] | Hits | Visible charge gives +10 and hidden mine +25; test at a high level too | Anas | |
| [ ] | Explosion | Explosion animates for approximately 5 frames | Alyan | |
| [ ] | Lives / game over | One life is lost per submarine hit; a charge that only grazes the tip cell does not sink you; game over follows the last life | Ali | |
| [ ] | Levels | Level increases every 200 points; charges get faster | Ali | |
| [ ] | Sonar | SPACE pauses movement for 2 seconds, marks hidden mines with `[!]`, plays sweep sound, then has 10-second cooldown | Alyan | |
| [ ] | Pause | P pauses/resumes with the `== PAUSED - press P to resume ==` banner centred on row 12; objects do not move while paused | Anas | |
| [ ] | Sounds | Fire, explosion, sonar, life-lost, and game-over sounds are distinct | Ali | |
| [ ] | High score | Saved high score remains after restarting the program | Ali | |
| [ ] | Drawing | No visible flicker; HUD is correct throughout play | Alyan | |
| [ ] | Replay | Game over → menu → new game resets score, lives, and all object arrays | Anas | |
| [ ] | Long run | Ten minutes of play without crash or noticeable slowdown | All | |

## Defect log

| ID | Date | Steps / observed result | Expected result | Owner | Fix PR / retest |
|---|---|---|---|---|---|
| | | | | | |
