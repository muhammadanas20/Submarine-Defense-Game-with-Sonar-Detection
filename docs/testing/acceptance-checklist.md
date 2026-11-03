# Whole-game acceptance checklist

Run this on the lab PC with the final integrated build. A checked box must be supported by a real test. Compatibility-environment results are recorded separately in [verification-2026-11-03.md](verification-2026-11-03.md); they do not replace this lab checklist.

**Lab test environment:** OS __________ · PC __________ · Visual Studio __________ · Irvine32 __________ · Configuration __________ · Date __________ · Tester __________

| Done | Test | Expected result | Owner | Actual result / evidence |
|---|---|---|---|---|
| [ ] | Visual Studio build | Debug and Release Win32 build without errors | Anas | |
| [ ] | Menu | Three options and high score; 2 opens instructions; 3/ESC exits | Ali | |
| [ ] | Movement | A/D and arrows move; stops at columns 1 and 78; capitals work | Anas | |
| [ ] | Firing | W fires with a gap; slots are reused; full-array guard does not crash | Anas | |
| [ ] | Charges | Random columns; about 1 in 5 hidden; 15-slot cap; fall timer works | Ali | |
| [ ] | Hits | Visible +10, hidden +25; crossing hit works at high level too | Anas | |
| [ ] | Explosion | Short ASCII animation at the hit position; slots free again | Alyan | |
| [ ] | Lives/game over | One life per submarine hit frame; game over after third life | Ali/Anas | |
| [ ] | Levels | Level changes at 200-point boundaries; cap 9; delays shrink | Ali | |
| [ ] | Sonar | SPACE freezes objects about 2 s, shows green !, then 10 s recharge | Alyan | |
| [ ] | Pause in play | P freezes objects; P resumes; W does not fire while paused | Anas | |
| [ ] | Pause in sonar | P pauses; resume returns to sonar with remaining reveal time | Anas/Alyan | |
| [ ] | Sounds | Five distinct effects on lab audio; muted audio does not break play | Ali | |
| [ ] | High score | New record survives program restart; tie is not called new | Ali | |
| [ ] | File errors | Missing file starts at 0; read-only folder shows save error | Ali | |
| [ ] | Drawing | No obvious flicker/scroll; HUD correct; bottom-right not printed | Alyan | |
| [ ] | Replay | Game over → menu → new game resets all round state | Anas | |
| [ ] | ESC | Returns to menu without saving the abandoned round | Anas/Ali | |
| [ ] | Long run | Ten minutes of play/replay without crash or growing lag | All | |

## Defect log

| ID | Date | Steps / observed result | Expected result | Owner | Fix PR / retest |
|---|---|---|---|---|---|
| | | | | | |

## Sign-off

- Anas: __________ Date: __________
- Alyan: __________ Date: __________
- Ali: __________ Date: __________

Do not sign until the rows you own have actual evidence.
